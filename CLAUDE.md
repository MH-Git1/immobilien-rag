# Immobilien-RAG-Projekt (Objektunterlagen-Assistent)

## Ziel
Ein RAG-System (Retrieval Augmented Generation), das Fragen zu 
Immobilien-Objektunterlagen (Exposés, Energieausweise, Protokolle, 
Teilungserklärungen) beantwortet — mit Quellenangabe, aus welchem 
Dokument die Antwort stammt.

Zweck: Portfolio-Projekt für Bewerbungen als AI Engineer, langfristig 
möglicher Kern einer Software für die Immobilienfirma Bonorum.

## Aktueller Stand (Stufe 2)
Dokumente einlesen → in Abschnitte zerlegen (Chunking) → Embeddings 
erzeugen → in Postgres/pgvector speichern (via Docker, siehe 
docker-compose.yml) → Frage stellen → relevante Abschnitte finden → 
Antwort mit Quellenangabe generieren. Angepasster Prompt sorgt dafür, 
dass Widersprüche zwischen Quellen explizit benannt werden statt 
stillschweigend aufgelöst zu werden. Testkatalog in tests/testfragen.py.

## Tech-Stack
- Python 3.12, venv im Projektordner
- LlamaIndex als RAG-Framework
- Postgres + pgvector via Docker (docker-compose.yml), Anbindung über
  llama-index-vector-stores-postgres
- Embeddings: text-embedding-3-small, LLM: gpt-4o-mini (OpenAI)
- API-Key und DB-Zugangsdaten liegen in .env (nicht in Git, siehe .gitignore)

## Arbeitsweise
- Schrittweise vorgehen, nicht alles auf einmal generieren
- Vor jedem Implementierungsschritt kurz erklären, was er tut und warum
- Bei mehreren sinnvollen Ansätzen: Alternativen kurz nennen, nicht 
  einfach eine Variante durchziehen
- Ich bin kein reiner Hand-Programmierer, verstehe aber Konzepte und 
  will nachvollziehen können, was der Code tut — Erklärungen erwünscht, 
  keine reinen Code-Dumps ohne Kontext
- Kommentare im Code auf Deutsch oder Englisch sind beide okay

## Testdaten
Noch keine echten Bonorum-Dokumente. Start mit selbst erzeugten, 
realistischen Beispiel-Objektunterlagen (fiktive Exposés, 
Energieausweise, Protokolle) zu 3-4 fiktiven Objekten, inkl. 
bewusst eingebauter Testfälle (Informationen, die nur in einem 
Dokument stehen; leicht widersprüchliche Angaben zwischen Dokumenten).