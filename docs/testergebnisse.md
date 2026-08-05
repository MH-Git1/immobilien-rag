# Testergebnisse — Objektunterlagen-Assistent

Dieses Dokument protokolliert Testläufe des RAG-Systems mit Zeitstempel,
damit sich ein Ergebnis-Snapshot später einem bestimmten Code-Stand
zuordnen lässt. Quelle der Fragen: `tests/testfragen.py`.

---

## Lauf vom 2026-08-05 20:40 (CEST) — PDF-Corpus, 8 Objekte

**Was sich seit dem letzten Lauf geändert hat:**

- Datenbasis auf **32 PDF-Dokumente** erweitert (8 fiktive Objekte ×
  4 Dokumenttypen: Exposé, Energieausweis, Protokoll,
  **Teilungserklärung neu dazugekommen**). Objekte 1-3 (Sonnenblick,
  Gartenhof, Ahornhöhe) sind die bisherigen; Objekte 4-8 (Lindenpark,
  Seeblick, Kastanienhof, Rosenhügel, Birkenallee) sind neu.
- Dokumente sind jetzt **echte PDFs** (`data_pdf/`, per `reportlab`
  generiert im Stil real recherchierter Vorlagen — stawag-Energieausweis,
  WEG-Wissen-Protokoll), nicht mehr reiner `.txt`.
- **Wichtiger Bugfix unterwegs gefunden:** `SimpleDirectoryReader` hatte
  ohne das Paket `llama-index-readers-file` PDFs nicht als solche
  erkannt und stattdessen rohe PDF-Binärdaten in den Index geschrieben
  (kein extrahierter Text) — nach Installation des fehlenden Pakets und
  Neuaufbau des Index behoben.
- `similarity_top_k` von 6 auf **12** erhöht (8 statt 3 Objekte, eine
  Vergleichsfrage kann Kontext aus bis zu 8 Energieausweisen brauchen).
- Postgres-Tabelle umbenannt zu `immobilien_chunks_v2` (alte Tabelle mit
  dem `.txt`-Corpus bleibt unberührt bestehen, wird aber nicht mehr
  verwendet).
- Aktuell 32 Chunks (1 Dokument = 1 Chunk — die Dokumente sind trotz
  realistischerer Formatierung noch unter der 1024-Token-Grenze).

**Ergebnis: 10 von 11 Testfällen wie erwartet, 1 Teilerfolg mit echter
Erkenntnis.**

| # | Kategorie | Ergebnis |
|---|---|---|
| 1 | Widerspruch zwischen Quellen (Sonnenblick, Wohnfläche) | ✅ |
| 2 | Info nur in einem Dokument (Sonnenblick, Fahrstuhl) | ✅ |
| 3 | Einfacher Fakt (Gartenhof, Kaufpreis) | ✅ |
| 4 | Negativ-Fakt (Gartenhof, kein Fahrstuhl) | ✅ |
| 5 | Halluzinationstest (Ahornhöhe, Sauna) | ✅ |
| 6 | Cross-Objekt-Verwechslung (Gartenhof, Rücklage) | ✅ |
| 7 | Vergleich über 8 Objekte (Energieeffizienzklasse) | ✅ — alle 8 korrekt, Seeblick (A+) richtig als bestes Objekt |
| 8 | Info nur in Teilungserklärung (Lindenpark, Garten-Sondernutzungsrecht) | ✅ |
| 9 | Widerspruch zwischen Quellen (Kastanienhof, Baujahr) | ⚠️ **Teilerfolg** — siehe unten |
| 10 | Cross-Objekt-Verwechslung, ähnliche Neubauten (Birkenallee vs. Rosenhügel, PV-Anlage) | ✅ |
| 11 | Halluzinationstest (Seeblick, Concierge-Service) | ✅ |

### Befund zu Test #9 — Widerspruchserkennung ist nicht immer zuverlässig

**Frage:** In welchem Jahr wurde das Gebäude Kastanienhof gebaut?

**Erwartung:** Exposé nennt 1975, Energieausweis nennt (als "Baujahr
Gebäude") 1974 — beide Werte sollten mit Quelle genannt werden.

**Tatsächliche Antwort (3x reproduziert, konsistent):**
> Das Gebäude Kastanienhof wurde im Jahr 1975 gebaut. Diese Information
> stammt aus dem Exposé der Wohnung "Kastanienhof" (Dateiname:
> objekt6_kastanienhof_expose.pdf).

Der Energieausweis mit dem abweichenden Wert (`objekt6_kastanienhof_
energieausweis.pdf`) wurde vom Retrieval korrekt gefunden und war Teil
des Kontexts — das Modell hat den Widerspruch trotzdem nicht erkannt
und genannt.

**Vermutliche Ursache:** Bei Sonnenblick (Test #1, funktioniert)
heißt das Feld in beiden Quellen identisch "Wohnfläche". Bei
Kastanienhof heißt es im Exposé "Baujahr", im Energieausweis aber
"Baujahr Gebäude" — die leicht abweichende Formulierung scheint die
im Prompt verankerte Widerspruchserkennung ("gleicher Sachverhalt")
zu schwächen. Das ist ein reales, reproduzierbares Limit des aktuellen
Custom-Prompts, kein einmaliger Ausrutscher.

**Mögliche nächste Schritte dazu:** Prompt könnte explizit auf
"inhaltlich gleiche Angaben trotz unterschiedlicher Formulierung"
hinweisen, oder Feldnamen in den Dokumenten stärker vereinheitlichen.

---

## Lauf vom 2026-08-05 19:15 (CEST)

**Code-/Systemstand bei diesem Lauf:**

- Git-Commit: — *(noch kein Git-Repository im Projekt initialisiert;
  siehe Hinweis unten)*
- Vektorspeicher: Postgres + pgvector (Docker, `docker-compose.yml`),
  Tabelle `data_immobilien_chunks`
- Embedding-Modell: `text-embedding-3-small`
- LLM: `gpt-4o-mini`
- `similarity_top_k`: 6
- Custom-QA-Prompt aktiv (weist Modell an, Widersprüche zwischen
  Quellen explizit zu benennen und nichts zu erfinden)
- Datenbasis: 9 Dokumente / 9 Chunks (3 fiktive Objekte: Sonnenblick,
  Gartenhof, Ahornhöhe)

**Ergebnis: 7/7 Testfälle wie erwartet.**

| # | Kategorie | Ergebnis |
|---|---|---|
| 1 | Widerspruch zwischen Quellen | ✅ Beide Werte (78 m² / 76 m²) korrekt mit Quelle genannt |
| 2 | Info nur in einem Dokument | ✅ Firma + Datum korrekt, richtige Quelle |
| 3 | Einfacher Fakt (Kontrolle) | ✅ Korrekt |
| 4 | Negativ-Fakt | ✅ Korrekt verneint, mit Beleg |
| 5 | Halluzinationstest | ✅ Kein erfundener Inhalt, klare Absage |
| 6 | Cross-Objekt-Verwechslung | ✅ Keine Vermischung zwischen Objekten |
| 7 | Vergleich über mehrere Objekte | ✅ Alle drei Energieausweise korrekt einbezogen |

### Details

#### 1. Widerspruch zwischen Quellen

**Frage:** Wie groß ist die Wohnfläche der Wohnung Sonnenblick?

**Erwartung:** Sollte beide Werte nennen (78 m² im Exposé, 76 m² im
Energieausweis) und den Widerspruch explizit benennen, statt sich
stillschweigend für einen Wert zu entscheiden.

**Antwort:**
> Die Wohnfläche der Wohnung "Sonnenblick" wird in zwei verschiedenen
> Quellen unterschiedlich angegeben. Im Exposé wird die Wohnfläche mit
> 78 m² angegeben (Dateiname: objekt1_sonnenblick_expose.txt), während
> im Energieausweis eine Wohnfläche von 76 m² angegeben wird
> (Dateiname: objekt1_sonnenblick_energieausweis.txt).

**Quellen:** objekt1_sonnenblick_expose.txt, objekt1_sonnenblick_energieausweis.txt, objekt3_ahornhoehe_expose.txt, objekt1_sonnenblick_protokoll.txt, objekt2_gartenhof_expose.txt, objekt3_ahornhoehe_energieausweis.txt

---

#### 2. Information nur in einem Dokument

**Frage:** Welche Firma wartet den Fahrstuhl im Haus Sonnenblick und
wann war die letzte Prüfung?

**Erwartung:** Sollte "Aufzugstechnik Reiner GmbH" und das Prüfdatum
09.11.2023 nennen, mit Quelle objekt1_sonnenblick_protokoll.txt —
diese Info steht nirgendwo sonst.

**Antwort:**
> Die Firma, die den Fahrstuhl im Haus Sonnenblick wartet, ist die
> "Aufzugstechnik Reiner GmbH". Die letzte Hauptprüfung durch den TÜV
> Süd fand am 09.11.2023 statt. (Quelle: objekt1_sonnenblick_protokoll.txt)

**Quellen:** objekt1_sonnenblick_protokoll.txt, objekt1_sonnenblick_expose.txt, objekt1_sonnenblick_energieausweis.txt, objekt3_ahornhoehe_protokoll.txt, objekt3_ahornhoehe_expose.txt, objekt3_ahornhoehe_energieausweis.txt

---

#### 3. Einfacher Fakt (Kontrollfrage)

**Frage:** Wie hoch ist der Kaufpreis der Wohnung Gartenhof?

**Erwartung:** 229.000 EUR, Quelle objekt2_gartenhof_expose.txt.

**Antwort:**
> Der Kaufpreis der Wohnung "Gartenhof" beträgt 229.000 EUR (Quelle:
> objekt2_gartenhof_expose.txt).

**Quellen:** objekt2_gartenhof_expose.txt, objekt3_ahornhoehe_expose.txt, objekt1_sonnenblick_expose.txt, objekt2_gartenhof_energieausweis.txt, objekt2_gartenhof_protokoll.txt, objekt3_ahornhoehe_energieausweis.txt

---

#### 4. Negativ-Fakt

**Frage:** Gibt es einen Fahrstuhl in der Wohnung Gartenhof?

**Erwartung:** Nein — laut Exposé kein Fahrstuhl (Erdgeschoss, nicht
erforderlich). Testet, ob explizit verneinte Fakten korrekt
wiedergegeben werden.

**Antwort:**
> In der Wohnung "Gartenhof" gibt es keinen Fahrstuhl, da die Wohnung
> im Erdgeschoss liegt und dies als nicht erforderlich angesehen wird.
> Diese Information stammt aus dem Exposé der Wohnung "Gartenhof"
> (Dateiname: objekt2_gartenhof_expose.txt).

**Quellen:** objekt2_gartenhof_expose.txt, objekt3_ahornhoehe_expose.txt, objekt2_gartenhof_protokoll.txt, objekt3_ahornhoehe_protokoll.txt, objekt1_sonnenblick_protokoll.txt, objekt1_sonnenblick_expose.txt

---

#### 5. Halluzinationstest

**Frage:** Wann wurde die Sauna im Haus Ahornhöhe zuletzt gewartet?

**Erwartung:** Es gibt keine Sauna in den Unterlagen. Sollte klar
sagen, dass die Information nicht vorhanden ist, statt etwas zu
erfinden.

**Antwort:**
> Die Informationen im Kontext enthalten keine Angaben zur Wartung
> einer Sauna im Haus Ahornhöhe. Daher kann ich diese Frage nicht
> beantworten.

**Quellen:** objekt3_ahornhoehe_protokoll.txt, objekt3_ahornhoehe_energieausweis.txt, objekt3_ahornhoehe_expose.txt, objekt1_sonnenblick_energieausweis.txt, objekt1_sonnenblick_protokoll.txt, objekt2_gartenhof_energieausweis.txt

---

#### 6. Cross-Objekt-Verwechslung

**Frage:** Wurde bei der WEG Gartenhof eine Erhöhung der
Instandhaltungsrücklage beschlossen?

**Erwartung:** Diesen Beschluss gibt es nur bei Sonnenblick, nicht bei
Gartenhof. Sollte nicht fälschlich vermischt werden — korrekte Antwort
ist "nicht enthalten".

**Antwort:**
> Im Protokoll der Eigentümerversammlung der WEG Gartenhof (Dateiname:
> objekt2_gartenhof_protokoll.txt) wird keine Erhöhung der
> Instandhaltungsrücklage beschlossen. Daher ist die Antwort: Nein, es
> wurde keine Erhöhung der Instandhaltungsrücklage beschlossen.

**Quellen:** objekt2_gartenhof_protokoll.txt, objekt3_ahornhoehe_protokoll.txt, objekt1_sonnenblick_protokoll.txt, objekt2_gartenhof_expose.txt, objekt2_gartenhof_energieausweis.txt, objekt3_ahornhoehe_energieausweis.txt

---

#### 7. Vergleich über mehrere Objekte

**Frage:** Welches der drei Objekte hat die beste
Energieeffizienzklasse?

**Erwartung:** Ahornhöhe (Klasse A) ist am besten, vor Gartenhof (C)
und Sonnenblick (D). Testet, ob similarity_top_k genug Kontext aus
allen drei Objekten liefert, um einen vollständigen Vergleich zu
ermöglichen.

**Antwort:**
> Das Objekt mit der besten Energieeffizienzklasse ist das Penthouse
> "Ahornhöhe" mit der Energieeffizienzklasse A.
>
> Die anderen beiden Objekte haben folgende Energieeffizienzklassen:
> - Wohnung "Sonnenblick": Energieeffizienzklasse D (Quelle:
>   objekt1_sonnenblick_energieausweis.txt)
> - Wohnung "Gartenhof": Energieeffizienzklasse C (Quelle:
>   objekt2_gartenhof_energieausweis.txt)

**Quellen:** objekt3_ahornhoehe_energieausweis.txt, objekt1_sonnenblick_energieausweis.txt, objekt2_gartenhof_energieausweis.txt, objekt1_sonnenblick_expose.txt, objekt3_ahornhoehe_expose.txt, objekt2_gartenhof_expose.txt

---

## Hinweis zum Abgleich mit dem Code-Stand

Das Projekt ist aktuell **kein Git-Repository** (`git status` meldet
"not a git repository"). Ein Zeitstempel allein reicht daher noch
nicht aus, um diesen Lauf eindeutig einem Code-Stand zuzuordnen —
solange z. B. main.py parallel weiterbearbeitet wird, ist nur der
Zeitpunkt bekannt, nicht der exakte Diff.

**Empfehlung:** Git in diesem Projekt initialisieren (`git init` +
erster Commit), und ab dann bei jedem Testlauf zusätzlich den
Commit-Hash (`git rev-parse HEAD`) hier eintragen. Ab dem nächsten
Lauf wird das Format um eine Zeile "Git-Commit: `<hash>`" ergänzt,
sobald das eingerichtet ist.
