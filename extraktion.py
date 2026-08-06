"""
Strukturierte Kennzahlen-Extraktion aus Objektunterlagen -- ergänzt die
freitext-basierte RAG-Suche um klassisch durchsuchbare/aggregierbare
Felder (Kaufpreis, Wohnfläche, ...). Läuft einmalig pro Dokument bei
dessen Einlesen (main.py: baue_index / api.py: Upload), nicht pro
Anfrage -- analog zum Chunking/Embedding.

Bewusst pro Dokument statt pro Objekt zusammengeführt: Exposé und
Energieausweis nennen z.B. teils leicht abweichende Wohnflächen (siehe
docs/testergebnisse.md). Ein zusammengeführter Datensatz würde diesen
Widerspruch stillschweigend auflösen -- widerspricht der Grundidee
dieses Projekts, Widersprüche zwischen Quellen sichtbar zu halten.
"""

from pydantic import BaseModel, Field
import psycopg2

from llama_index.core import PromptTemplate, Settings

from db import verbindungsparameter

TABELLE = "objekt_kennzahlen"

EXTRAKTIONS_PROMPT = PromptTemplate(
    "Extrahiere die folgenden Kennzahlen aus diesem Auszug einer "
    "Immobilien-Objektunterlage, falls jeweils im Text genannt. Lasse "
    "ein Feld leer (null), wenn der Wert nicht im Text steht -- rate "
    "nicht und übernimm keine Werte aus anderen Objekten.\n\n"
    "Achtung bei 'baujahr': Das ist ausschließlich das Baujahr des "
    "Gebäudes selbst. Ein Beurkundungsdatum, eine Urkundenrollennummer "
    "(z.B. 'UR-Nr. 884/1998') oder das Datum einer Teilungserklärung "
    "sind KEIN Baujahr, auch wenn eine Jahreszahl darin vorkommt -- nur "
    "übernehmen, wenn der Text das Baujahr des Gebäudes explizit "
    "nennt.\n\n{text}"
)


class ObjektKennzahlen(BaseModel):
    kaufpreis_eur: float | None = Field(None, description="Kaufpreis in Euro")
    wohnflaeche_qm: float | None = Field(None, description="Wohnfläche in Quadratmetern")
    zimmer: float | None = Field(None, description="Anzahl Zimmer")
    baujahr: int | None = Field(None, description="Baujahr des Gebäudes")
    energieeffizienzklasse: str | None = Field(
        None, description="Energieeffizienzklasse, z.B. 'A+', 'B', 'D'"
    )
    hausgeld_eur_monatlich: float | None = Field(None, description="Monatliches Hausgeld in Euro")
    etage: str | None = Field(None, description="Stockwerk/Etage der Einheit")


def sicherstelle_tabelle() -> None:
    conn = psycopg2.connect(**verbindungsparameter())
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS {TABELLE} (
                    id SERIAL PRIMARY KEY,
                    objekt_name TEXT NOT NULL,
                    dateiname TEXT NOT NULL UNIQUE,
                    kaufpreis_eur NUMERIC,
                    wohnflaeche_qm NUMERIC,
                    zimmer NUMERIC,
                    baujahr INT,
                    energieeffizienzklasse TEXT,
                    hausgeld_eur_monatlich NUMERIC,
                    etage TEXT,
                    extrahiert_am TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
        conn.commit()
    finally:
        conn.close()


def extrahiere_und_speichere(objekt_name: str, dateiname: str, text: str) -> None:
    """
    Läuft fehlertolerant: ein Problem bei der Extraktion (z.B. Timeout,
    unerwartetes LLM-Format) darf nie den Ingestion-Vorgang abbrechen --
    die Kennzahlen sind eine Zusatzfunktion, kein kritischer Pfad wie
    Chunking/Embedding.
    """
    try:
        kennzahlen = Settings.llm.structured_predict(
            ObjektKennzahlen, EXTRAKTIONS_PROMPT, text=text
        )
    except Exception as fehler:
        print(f"[Kennzahlen-Extraktion fehlgeschlagen für {dateiname}: {fehler}]")
        return

    try:
        conn = psycopg2.connect(**verbindungsparameter())
        try:
            with conn.cursor() as cur:
                cur.execute(
                    f"""
                    INSERT INTO {TABELLE}
                        (objekt_name, dateiname, kaufpreis_eur, wohnflaeche_qm,
                         zimmer, baujahr, energieeffizienzklasse,
                         hausgeld_eur_monatlich, etage)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (dateiname) DO UPDATE SET
                        objekt_name = EXCLUDED.objekt_name,
                        kaufpreis_eur = EXCLUDED.kaufpreis_eur,
                        wohnflaeche_qm = EXCLUDED.wohnflaeche_qm,
                        zimmer = EXCLUDED.zimmer,
                        baujahr = EXCLUDED.baujahr,
                        energieeffizienzklasse = EXCLUDED.energieeffizienzklasse,
                        hausgeld_eur_monatlich = EXCLUDED.hausgeld_eur_monatlich,
                        etage = EXCLUDED.etage,
                        extrahiert_am = now()
                    """,
                    (
                        objekt_name,
                        dateiname,
                        kennzahlen.kaufpreis_eur,
                        kennzahlen.wohnflaeche_qm,
                        kennzahlen.zimmer,
                        kennzahlen.baujahr,
                        kennzahlen.energieeffizienzklasse,
                        kennzahlen.hausgeld_eur_monatlich,
                        kennzahlen.etage,
                    ),
                )
            conn.commit()
        finally:
            conn.close()
    except Exception as fehler:
        print(f"[Kennzahlen-Speicherung fehlgeschlagen für {dateiname}: {fehler}]")


_SPALTEN = [
    "objekt_name",
    "dateiname",
    "kaufpreis_eur",
    "wohnflaeche_qm",
    "zimmer",
    "baujahr",
    "energieeffizienzklasse",
    "hausgeld_eur_monatlich",
    "etage",
]

# NUMERIC-Spalten kommen von psycopg2 als decimal.Decimal zurück und
# werden von FastAPI dadurch als String statt als Zahl serialisiert
# (z.B. "112.0" statt 112.0) -- im Frontend sah man dadurch hässliche
# Werte wie "112.0 m²" statt "112 m²". Explizite float()-Konvertierung
# hier behebt das an der Quelle, ohne das Frontend anzufassen.
_NUMERISCHE_FELDER = {"kaufpreis_eur", "wohnflaeche_qm", "zimmer", "hausgeld_eur_monatlich"}


def _zeile_aufbereiten(row: tuple) -> dict:
    eintrag = dict(zip(_SPALTEN, row))
    for feld in _NUMERISCHE_FELDER:
        if eintrag[feld] is not None:
            eintrag[feld] = float(eintrag[feld])
    return eintrag


def kennzahlen_fuer_objekt(objekt_name: str) -> list[dict]:
    conn = psycopg2.connect(**verbindungsparameter())
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT {', '.join(_SPALTEN)} FROM {TABELLE} "
                "WHERE objekt_name = %s ORDER BY dateiname",
                (objekt_name,),
            )
            return [_zeile_aufbereiten(row) for row in cur.fetchall()]
    finally:
        conn.close()


def alle_kennzahlen() -> list[dict]:
    conn = psycopg2.connect(**verbindungsparameter())
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"SELECT {', '.join(_SPALTEN)} FROM {TABELLE} "
                "ORDER BY objekt_name, dateiname"
            )
            return [_zeile_aufbereiten(row) for row in cur.fetchall()]
    finally:
        conn.close()
