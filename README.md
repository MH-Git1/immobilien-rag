# Immobilien-RAG-Projekt (Objektunterlagen-Assistent)

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
5. **Antwort**: Wird zusammen mit den verwendeten Quelldokumenten (inkl. Ähnlichkeits-Score) in der Konsole ausgegeben.

## Tech-Stack

- Python 3.12
- [LlamaIndex](https://www.llamaindex.ai/) als RAG-Framework
- Postgres + [pgvector](https://github.com/pgvector/pgvector) als Vektorspeicher (via Docker)
- OpenAI: `text-embedding-3-small` (Embeddings), `gpt-4o-mini` (LLM)
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
python main.py
```

Das Skript baut beim ersten Start den Vektor-Index auf (Embedding aller
Dokumente in `data_pdf/`) und speichert ihn in Postgres. Bei
weiteren Starts wird der bestehende Index geladen, ohne neu zu
embedden.

## Projektstruktur

```
data_pdf/               32 PDF-Dokumente: 8 fiktive Objekte × 4 Dokumenttypen
                         (Exposé, Energieausweis, Protokoll, Teilungserklärung)
scripts/objektdaten.py  Strukturierte Daten für alle Objekte
scripts/generate_pdfs.py  Generiert die PDFs aus objektdaten.py (reportlab)
main.py                 Index-Aufbau, Query Engine, interaktive Konsolen-Schleife
tests/testfragen.py     Regressions-Testkatalog (11 Fragen)
docs/testergebnisse.md  Dokumentierte Testläufe mit Zeitstempel
docker-compose.yml      Postgres + pgvector Container
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
einbinden, automatisierte Bewertung der Testantworten.
