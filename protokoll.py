"""
Protokollierung jeder Anfrage (Frage, Antwort, Latenz, geschätzte
Kosten) in einer eigenen Postgres-Tabelle — Observability-Grundlage,
u.a. um spätere Retrieval-Änderungen (z.B. Reranking) mit echten
Latenz-/Kostenzahlen vergleichen zu können, und um zu sehen, wonach
tatsächlich gefragt wird. Läuft in derselben Datenbank wie der
Vektor-Index (siehe main.py), aber in einer eigenen Tabelle, damit
RAG-Chunks und Nutzungsprotokoll getrennt bleiben.
"""

import json

import psycopg2

from db import verbindungsparameter

TABELLE = "anfrage_protokoll"

# OpenAI-Preise in USD je 1 Mio. Token, Stand August 2026
# (https://openai.com/api/pricing). Bei Preisänderungen hier anpassen —
# die berechneten Kosten sind daher als Näherung zu verstehen, nicht als
# exakte Abrechnung.
PREIS_PROMPT_PRO_1M_TOKEN = 0.15  # gpt-4o-mini, Input
PREIS_COMPLETION_PRO_1M_TOKEN = 0.60  # gpt-4o-mini, Output
PREIS_EMBEDDING_PRO_1M_TOKEN = 0.02  # text-embedding-3-small


def sicherstelle_tabelle() -> None:
    conn = psycopg2.connect(**verbindungsparameter())
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {TABELLE} (
                    id SERIAL PRIMARY KEY,
                    zeitstempel TIMESTAMPTZ NOT NULL DEFAULT now(),
                    herkunft TEXT NOT NULL,
                    frage TEXT NOT NULL,
                    antwort TEXT NOT NULL,
                    objekt_filter TEXT,
                    quellen JSONB NOT NULL,
                    prompt_tokens INT NOT NULL,
                    completion_tokens INT NOT NULL,
                    embedding_tokens INT NOT NULL,
                    geschaetzte_kosten_usd NUMERIC(10, 6) NOT NULL,
                    latenz_ms INT NOT NULL
                )
                """
            )
        conn.commit()
    finally:
        conn.close()


def _geschaetzte_kosten_usd(
    prompt_tokens: int, completion_tokens: int, embedding_tokens: int
) -> float:
    return (
        prompt_tokens * PREIS_PROMPT_PRO_1M_TOKEN
        + completion_tokens * PREIS_COMPLETION_PRO_1M_TOKEN
        + embedding_tokens * PREIS_EMBEDDING_PRO_1M_TOKEN
    ) / 1_000_000


def eintrag_schreiben(
    *,
    herkunft: str,
    frage: str,
    antwort: str,
    objekt_filter: str | None,
    quellen: list[dict],
    prompt_tokens: int,
    completion_tokens: int,
    embedding_tokens: int,
    latenz_ms: int,
) -> None:
    """
    Schreibt einen Protokolleintrag. Läuft bewusst fehlertolerant: ein
    Problem bei der Protokollierung (z.B. Tabelle fehlt noch) darf nie
    die eigentliche Fragebeantwortung zum Absturz bringen.
    """
    kosten = _geschaetzte_kosten_usd(prompt_tokens, completion_tokens, embedding_tokens)
    try:
        conn = psycopg2.connect(**verbindungsparameter())
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {TABELLE}
                        (herkunft, frage, antwort, objekt_filter, quellen,
                         prompt_tokens, completion_tokens, embedding_tokens,
                         geschaetzte_kosten_usd, latenz_ms)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        herkunft,
                        frage,
                        antwort,
                        objekt_filter,
                        json.dumps(quellen),
                        prompt_tokens,
                        completion_tokens,
                        embedding_tokens,
                        kosten,
                        latenz_ms,
                    ),
                )
            conn.commit()
        finally:
            conn.close()
    except Exception as fehler:
        print(f"[Protokollierung fehlgeschlagen: {fehler}]")
