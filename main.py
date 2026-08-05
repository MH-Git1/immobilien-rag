"""
Objektunterlagen-Assistent (Stufe 2)

Liest alle Dokumente aus data/ ein, baut daraus einen Vektor-Index in
Postgres (pgvector, siehe docker-compose.yml) und beantwortet Fragen
dazu interaktiv in der Konsole, jeweils mit Quellenangabe.
"""

import os
from dotenv import load_dotenv
import psycopg2

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings,
    PromptTemplate,
)
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.vector_stores.postgres import PGVectorStore

# API-Key aus .env laden (siehe .env-Datei, nicht in Git)
load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError(
        "OPENAI_API_KEY nicht gefunden. Bitte in der .env-Datei setzen "
        "(OPENAI_API_KEY=sk-...)."
    )

# Günstige, für dieses Projektstadium ausreichend starke Modelle statt
# der teureren LlamaIndex-Standardmodelle.
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4o-mini")

DATA_DIR = "data"

# Postgres/pgvector-Zugangsdaten aus .env (siehe docker-compose.yml für
# den lokalen Container). embed_dim=1536 passt zu text-embedding-3-small.
PG_TABLE_NAME = "immobilien_chunks"
PG_EMBED_DIM = 1536

# Wie viele Chunks pro Frage aus dem Vektorspeicher geholt werden.
# Standard wäre 2 — bei objektübergreifenden Vergleichsfragen (z.B.
# "welches der drei Objekte hat...") reicht das nicht, weil dann Chunks
# aus allen drei Objekten gebraucht werden. Bei aktuell 9 Chunks insgesamt
# (1 Dokument = 1 Chunk bei dieser Dokumentgröße) ist 6 ein guter
# Kompromiss: deckt Vergleichsfragen zuverlässig ab, ohne bei jeder Frage
# den kompletten Datenbestand in den Prompt zu packen.
SIMILARITY_TOP_K = 6

# Angepasster Antwort-Prompt: weist das Modell explizit an, Widersprüche
# zwischen Quellen offenzulegen statt sich stillschweigend für eine Angabe
# zu entscheiden, und nichts zu erfinden, was nicht im Kontext steht.
QA_PROMPT = PromptTemplate(
    "Kontextinformationen aus den Objektunterlagen sind unten angegeben.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Beantworte die folgende Frage ausschließlich anhand der obigen "
    "Kontextinformationen.\n"
    "- Wenn verschiedene Quellen im Kontext unterschiedliche Angaben zum "
    "gleichen Sachverhalt machen, weise das explizit aus: nenne beide Werte "
    "und die jeweilige Quelle (Dateiname).\n"
    "- Wenn die Information nicht im Kontext enthalten ist, sage das "
    "ausdrücklich, anstatt zu raten oder Informationen zu erfinden.\n"
    "Frage: {query_str}\n"
    "Antwort: "
)


def _pg_verbindungsparameter() -> dict:
    """Liest die Postgres-Zugangsdaten aus den Umgebungsvariablen (.env)."""
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "database": os.getenv("POSTGRES_DB", "immobilien_rag"),
        "user": os.getenv("POSTGRES_USER", "immobilien_rag"),
        "password": os.getenv("POSTGRES_PASSWORD", "immobilien_rag"),
    }


def _baue_pgvector_store() -> PGVectorStore:
    """
    Verbindet sich mit dem Postgres-Container (siehe docker-compose.yml)
    und liefert einen PGVectorStore. LlamaIndex legt darüber automatisch
    die Tabelle "data_<PG_TABLE_NAME>" an (inkl. pgvector-Extension),
    falls sie noch nicht existiert.
    """
    params = _pg_verbindungsparameter()
    return PGVectorStore.from_params(
        host=params["host"],
        port=params["port"],
        database=params["database"],
        user=params["user"],
        password=params["password"],
        table_name=PG_TABLE_NAME,
        embed_dim=PG_EMBED_DIM,
    )


def _anzahl_vorhandener_chunks() -> int:
    """
    Prüft direkt per SQL, ob in Postgres schon eingebettete Chunks liegen.
    Damit entscheidet baue_index(), ob der Index neu gebaut (und dabei
    kostenpflichtig neu embedded) oder einfach aus der Datenbank geladen
    werden kann.
    """
    tabelle = f"data_{PG_TABLE_NAME}"
    params = _pg_verbindungsparameter()
    conn = psycopg2.connect(**params)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT EXISTS (SELECT FROM information_schema.tables "
                "WHERE table_name = %s)",
                (tabelle,),
            )
            if not cur.fetchone()[0]:
                return 0
            cur.execute(f'SELECT COUNT(*) FROM "{tabelle}"')
            return cur.fetchone()[0]
    finally:
        conn.close()


def baue_index() -> VectorStoreIndex:
    """
    Liefert den Vektor-Index — entweder aus Postgres geladen oder neu
    gebaut und dort gespeichert.

    Persistenz: Anders als bei der lokalen SimpleVectorStore-Variante ist
    die Datenbank selbst der persistente Speicher — es gibt keinen
    separaten "storage/"-Ordner mehr. Enthält die Tabelle bereits Chunks,
    wird direkt darauf aufgesetzt (VectorStoreIndex.from_vector_store),
    ohne erneut zu embedden. Wichtig: Wenn sich Dateien in data/ ändern,
    merkt das System das NICHT von selbst — dazu die Tabelle leeren
    (z.B. `docker compose down -v` für einen kompletten Reset) oder
    PG_TABLE_NAME ändern, damit neu gebaut wird.

    Ablauf beim Neubau (Chunking + Embedding) ist identisch zur
    SimpleVectorStore-Variante:
    1. SimpleDirectoryReader liest jede Datei als ein "Document"-Objekt
       ein (Text + Metadaten, u.a. der Dateiname unter "file_name").
    2. VectorStoreIndex.from_documents() übernimmt intern zwei Schritte:
       a) Chunking: Jedes Document wird in kleinere "Nodes" (Textabschnitte)
          zerlegt. Standardmäßig verwendet LlamaIndex dafür den
          SentenceSplitter mit fester Chunk-Größe und Overlap
          (Standard: chunk_size=1024 Tokens, chunk_overlap=200 Tokens).
       b) Embedding: Für jeden Chunk wird über die OpenAI-Embedding-API
          ein Vektor berechnet (hier: text-embedding-3-small). Die
          Vektoren werden diesmal nicht mehr lokal im Arbeitsspeicher,
          sondern über den PGVectorStore direkt in Postgres geschrieben.
    """
    vector_store = _baue_pgvector_store()

    anzahl = _anzahl_vorhandener_chunks()
    if anzahl > 0:
        print(f"Lade bestehenden Index aus Postgres ({anzahl} Chunks) ...")
        return VectorStoreIndex.from_vector_store(vector_store)

    dokumente = SimpleDirectoryReader(DATA_DIR).load_data()
    print(f"{len(dokumente)} Dokument(e) aus '{DATA_DIR}/' eingelesen.")

    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        dokumente, storage_context=storage_context
    )
    print("Index in Postgres (pgvector) gespeichert.")
    return index


def interaktive_schleife(index: VectorStoreIndex) -> None:
    """
    Erlaubt es, wiederholt Fragen an den Index zu stellen.

    query_engine.query() läuft in zwei Schritten ab:
    1. Retrieval: Die Frage wird ebenfalls in einen Vektor umgewandelt
       (Embedding). Per Kosinus-Ähnlichkeit werden die "similarity_top_k"
       ähnlichsten Chunks per pgvector aus Postgres geholt. LlamaIndex-
       Standard wäre 2; wir setzen SIMILARITY_TOP_K=6 (siehe oben), weil
       2 Chunks für objektübergreifende Vergleichsfragen nicht reichen.
    2. Generation: Die gefundenen Chunks werden zusammen mit der Frage
       als Kontext an das LLM (hier: gpt-4o-mini, siehe Settings.llm)
       geschickt, das daraus die Antwort formuliert.

    Die Quellenangabe kommt aus response.source_nodes: Jeder verwendete
    Chunk (Node) trägt die Metadaten seines Ursprungs-Dokuments (u.a.
    file_name) mit sich, weil SimpleDirectoryReader diese beim Einlesen
    an jedes Document angehängt hat und sie beim Chunking an die
    Nodes vererbt werden.
    """
    query_engine = index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K)
    query_engine.update_prompts({"response_synthesizer:text_qa_template": QA_PROMPT})

    print("\nObjektunterlagen-Assistent bereit. Stelle deine Fragen.")
    print("Zum Beenden 'exit' oder 'quit' eingeben.\n")

    while True:
        frage = input("Frage: ").strip()
        if not frage:
            continue
        if frage.lower() in {"exit", "quit"}:
            print("Auf Wiedersehen.")
            break

        antwort = query_engine.query(frage)

        print(f"\nAntwort: {antwort}\n")
        print("Quellen:")
        for node in antwort.source_nodes:
            dateiname = node.metadata.get("file_name", "unbekannt")
            score = node.score
            print(f"  - {dateiname} (Ähnlichkeit: {score:.3f})")
        print()


if __name__ == "__main__":
    index = baue_index()
    interaktive_schleife(index)
