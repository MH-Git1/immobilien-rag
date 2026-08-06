# Immobilien-RAG-Projekt (Objektunterlagen-Assistent)

[![Testkatalog](https://github.com/MH-Git1/immobilien-rag/actions/workflows/tests.yml/badge.svg)](https://github.com/MH-Git1/immobilien-rag/actions/workflows/tests.yml)

Ein RAG-System (Retrieval Augmented Generation), das Fragen zu
Immobilien-Objektunterlagen (Exposés, Energieausweise,
Eigentümerversammlungs-Protokolle, Teilungserklärungen) beantwortet —
mit Quellenangabe, aus welchem Dokument die Antwort stammt.

Portfolio-Projekt zur Bewerbung als AI Engineer; langfristig möglicher
Kern einer Software für die Immobilienfirma Bonorum.

## Wie es funktioniert

```
PDF-Dokumente → Einlesen & Chunking → Embeddings → Postgres/pgvector
                                                          │
Frage → Embedding → Vektorsuche (top_k Chunks) → LLM mit Kontext → Antwort + Quellen
```

1. **Ingestion**: `SimpleDirectoryReader` liest alle PDFs aus `data_pdf/` ein und zerlegt sie in Chunks.
2. **Embedding**: Jeder Chunk wird über die OpenAI-API (`text-embedding-3-small`) in einen Vektor umgewandelt und in Postgres (Erweiterung `pgvector`) gespeichert.
3. **Retrieval**: Bei einer Frage werden die `similarity_top_k` ähnlichsten Chunks per Kosinus-Ähnlichkeit gesucht.
4. **Generation**: Ein angepasster Prompt schickt die gefundenen Chunks zusammen mit der Frage an `gpt-4o-mini`. Der Prompt weist das Modell explizit an, Widersprüche zwischen Quellen offenzulegen statt sie stillschweigend aufzulösen, und nichts zu erfinden, was nicht im Kontext steht.
5. **Antwort**: Wird inklusive der verwendeten Quelldokumente (mit Ähnlichkeits-Score) ausgegeben — entweder im Browser (Web-UI) oder in der Konsole.

**Optionales Reranking:** `main.py` unterstützt zusätzlich einen
LLM-Reranking-Schritt nach dem Retrieval (`AKTIVIERE_RERANKING=true`
in `.env`). Im Testkatalog gemessen (siehe `docs/testergebnisse.md`,
Lauf vom 2026-08-06) verschlechtert er beim aktuellen Corpus-Umfang
die Trefferquote bei objektübergreifenden Vergleichsfragen (zu
aggressives Aussieben von Kontext) — bleibt daher standardmäßig
deaktiviert, ist aber für einen künftig größeren Corpus als getestete
Option vorhanden.

## Tech-Stack

- Python 3.12
- [LlamaIndex](https://www.llamaindex.ai/) als RAG-Framework
- Postgres + [pgvector](https://github.com/pgvector/pgvector) als Vektorspeicher (via Docker)
- OpenAI: `text-embedding-3-small` (Embeddings), `gpt-4o-mini` (LLM)
- [FastAPI](https://fastapi.tiangolo.com/) als Backend für die Web-UI, schlichtes HTML/CSS/JS-Frontend ohne Framework
- `reportlab` zur Generierung der Testdokumente als PDF

## Setup

Voraussetzungen: Python 3.12, Docker, ein OpenAI-API-Key.

```bash
# 1. Virtuelle Umgebung anlegen und Abhängigkeiten installieren
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. .env anlegen
cp .env.example .env   # dann OPENAI_API_KEY eintragen

# 3. Postgres mit pgvector starten
docker compose up -d

# 4. Assistent starten
uvicorn api:app --reload   # Web-UI unter http://127.0.0.1:8000
# oder, als Konsolen-Variante:
python main.py
```

Der erste Start baut den Vektor-Index auf (Embedding aller Dokumente
in `data_pdf/`) und speichert ihn in Postgres — unabhängig davon, ob
über die Web-UI oder die Konsole gestartet wird. Bei weiteren Starts
wird der bestehende Index geladen, ohne neu zu embedden.

## Deployment

Die App läuft containerisiert (siehe `Dockerfile`) und lässt sich per
[Render](https://render.com) Blueprint (`render.yaml`) mit einer Postgres+pgvector-Datenbank
zusammen deployen:

1. Auf [render.com](https://render.com) einloggen, dann **New +** → **Blueprint** →
   dieses GitHub-Repo auswählen. Render liest `render.yaml` und legt Web-Service
   und Datenbank automatisch an.
2. Im Render-Dashboard beim Web-Service unter **Environment** die Secrets setzen,
   die bewusst nicht im Repo liegen:
   - `OPENAI_API_KEY`
   - `BASIC_AUTH_USER` / `BASIC_AUTH_PASSWORD` (einfacher Zugriffsschutz für die
     öffentlich erreichbare Instanz — ohne diese beiden Variablen bleibt die App
     ungeschützt, siehe `api.py`)
3. Deploy abwarten. Der erste Start baut den Index neu auf (Embedding aller 32
   Test-PDFs) — kostet einmalig ein paar Cent OpenAI-API-Kosten und dauert daher
   beim ersten Boot spürbar länger als bei folgenden Neustarts.

**Bekannte Einschränkung:** Die kostenlose Render-Instanz hat ein flüchtiges
Dateisystem — über die Web-UI hochgeladene Original-PDFs (`data_pdf/hochgeladen_*.pdf`)
können bei einem Neustart des Web-Service verloren gehen. Die durchsuchbaren
Inhalte (Chunks + Embeddings) bleiben davon unberührt, da sie in der separaten
Postgres-Datenbank liegen, nicht auf der Festplatte des Web-Service. Für einen
produktiven Einsatz mit dauerhafter Dateiablage wäre ein persistentes Volume
oder Objektspeicher (z. B. S3-kompatibel) der nächste Schritt.

## Beobachtbarkeit (Protokollierung)

Jede Anfrage (Konsole, Web-UI oder Testlauf) wird in der Postgres-Tabelle
`anfrage_protokoll` erfasst: Frage, Antwort, erkannter Objekt-Filter,
Quellen, Prompt-/Completion-/Embedding-Tokens, geschätzte Kosten (auf
Basis der OpenAI-Preise, siehe `protokoll.py`) und Latenz in ms. Das
`herkunft`-Feld (`web`/`konsole`/`test`) trennt echte Nutzung von
Testläufen. Beispielabfrage für eine schnelle Kostenübersicht:

```sql
SELECT herkunft, count(*), round(avg(latenz_ms)) AS avg_latenz_ms,
       round(sum(geschaetzte_kosten_usd)::numeric, 4) AS summe_kosten_usd
FROM anfrage_protokoll
GROUP BY herkunft;
```

## Strukturierte Kennzahlen-Extraktion

Neben der freitext-basierten RAG-Suche werden beim Einlesen jedes
Dokuments (Ersteinlesen wie auch Upload) zusätzlich klassisch
durchsuchbare Kennzahlen extrahiert (Kaufpreis, Wohnfläche, Zimmer,
Baujahr, Energieeffizienzklasse, Hausgeld, Etage) — per
LLM-Structured-Output (`Settings.llm.structured_predict`, siehe
`extraktion.py`), nicht per Regex, damit unterschiedliche
Formulierungen zwischen Dokumenttypen zuverlässig erkannt werden.

Bewusst **pro Dokument**, nicht pro Objekt zusammengeführt: Exposé und
Energieausweis nennen teils leicht abweichende Werte (siehe
`docs/testergebnisse.md`) — ein zusammengeführter Datensatz würde
diesen Widerspruch stillschweigend auflösen. Abrufbar über
`GET /api/kennzahlen` (alle) bzw. `GET /api/kennzahlen/{objekt_name}`.

## Projektstruktur

```
data_pdf/               32 PDF-Dokumente: 8 fiktive Objekte × 4 Dokumenttypen
                         (Exposé, Energieausweis, Protokoll, Teilungserklärung)
scripts/objektdaten.py  Strukturierte Daten für alle Objekte
scripts/generate_pdfs.py  Generiert die PDFs aus objektdaten.py (reportlab)
main.py                 Index-Aufbau, Query Engine, interaktive Konsolen-Schleife
api.py                  FastAPI-Backend für die Web-UI (nutzt main.py)
frontend/               Statisches HTML/CSS/JS-Frontend (Chat-Oberfläche)
db.py                   Gemeinsame Postgres-Verbindungsparameter
protokoll.py            Anfrage-Protokollierung (Latenz, Tokens, geschätzte Kosten)
extraktion.py           Strukturierte Kennzahlen-Extraktion (Kaufpreis, Wohnfläche, ...)
tests/testfragen.py     Regressions-Testkatalog (11 Fragen)
docs/testergebnisse.md  Dokumentierte Testläufe mit Zeitstempel
docker-compose.yml      Postgres + pgvector Container (lokale Entwicklung)
Dockerfile              Image für die Web-UI (api.py), Basis für das Deployment
render.yaml             Render Blueprint (Web-Service + Postgres/pgvector)
```

## Testdaten und Testmethodik

Die Testdaten sind vollständig erfunden (8 fiktive Immobilienobjekte), aber im Stil real
recherchierter Vorlagen (offizielle Muster-Energieausweise,
WEG-Protokoll-Vorlagen) als PDF aufgebaut, um die Dokument-Ingestion
realistisch zu testen.

Der Testkatalog (`tests/testfragen.py`) deckt gezielt typische
RAG-Schwachstellen ab:

- **Widersprüche zwischen Quellen** (z. B. leicht abweichende
  Wohnflächen-Angabe zwischen Exposé und Energieausweis)
- **Informationen, die nur in einem einzigen Dokument stehen**
- **Cross-Objekt-Verwechslung** (ähnliche Dokumente zu verschiedenen
  Objekten dürfen nicht vermischt werden)
- **Halluzinationstests** (nach nicht existierenden Fakten fragen)
- **Objektübergreifende Vergleichsfragen** (erfordert Kontext aus
  mehreren Dokumenten gleichzeitig)

Testläufe inkl. der tatsächlichen Modellantworten sind mit Zeitstempel
in `docs/testergebnisse.md` dokumentiert — dort auch ein dokumentierter
Fall, in dem die Widerspruchserkennung nicht zuverlässig funktioniert.

Testkatalog ausführen:

```bash
python -m tests.testfragen
```

## Stand des Projekts

Aktuell Stufe 2 (siehe `CLAUDE.md` für Details zur Roadmap und
Arbeitsweise). Nächste mögliche Schritte: echte Bonorum-Unterlagen
einbinden.
