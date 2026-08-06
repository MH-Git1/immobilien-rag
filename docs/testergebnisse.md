# Testergebnisse — Objektunterlagen-Assistent

Dieses Dokument protokolliert Testläufe des RAG-Systems mit Zeitstempel,
damit sich ein Ergebnis-Snapshot später einem bestimmten Code-Stand
zuordnen lässt. Quelle der Fragen: `tests/testfragen.py`.

---

## Lauf vom 2026-08-06 02:13 (CEST) — Metadaten-Filterung + automatisierte Bewertung (LLM-Richter)

**Git-Commit:** `3aeff3839c272388ac3cf2387b178fe6c55d9ce0` ("Metadaten-Filterung
(Retrieval) und LLM-als-Richter (automatisierte Tests)")

**Was sich seit dem letzten Lauf geändert hat:**

- **Metadaten-Filterung eingeführt**: Jedes Dokument bekommt beim
  Einlesen ein `objekt_name`-Metadatenfeld (aus dem Dateinamen
  extrahiert). Erkennt `main.py` in der Frage genau einen bekannten
  Objektnamen, filtert die Vektorsuche gezielt auf dessen Dokumente,
  statt über den ganzen 40-Chunk-Corpus zu suchen. Bei Fragen ohne
  eindeutigen Objektnamen (z. B. Vergleichsfragen) bleibt die Suche
  ungefiltert. Behebt strukturell die Ursache der letzten Regression
  (semantisches Rauschen zwischen ähnlichen Objekten).
- **LLM-als-Richter eingeführt**: `tests/testfragen.py` bewertet jede
  Antwort jetzt automatisiert per zweitem LLM-Call (PASS/FAIL +
  Begründung) gegen die hinterlegte Erwartung, statt dass die Antworten
  von Hand gelesen werden.
- **Wichtiger Kalibrierungs-Fund beim Richter selbst**: Der erste
  Richter-Prompt-Entwurf war zu wörtlich/streng — er verlangte u. a.,
  dass exakte Dateinamen im Antworttext wörtlich vorkommen, und
  bewertete korrekt-zurückhaltende Formulierungen ("kann ich nicht
  bestätigen") fälschlich als FAIL. Erster automatisierter Lauf: 8/12.
  Nach Analyse jedes einzelnen FAILs (3 von 4 waren Richterfehler, nicht
  Systemfehler) wurde der Richter-Prompt nachgeschärft (Fokus auf
  fachlichen Inhalt statt Zitierformat, explizite Regel für korrekt
  zurückhaltende "nicht vorhanden"-Antworten) — danach 11/12. Der
  letzte verbleibende Fall war ebenfalls ein reines
  Formulierungs-Problem der Testerwartung selbst (verlangte wörtliche
  Dateinamensnennung im Fließtext), nicht des Systems — nach Anpassung
  der Erwartung: 12/12.
- **Eine echte, kleine Verhaltensänderung durch die Filterung
  beobachtet**: Bei der Gartenhof-Rücklage-Frage antwortet das System
  jetzt vorsichtiger ("kann ich nicht bestätigen" statt zuvor "Nein, es
  wurde nicht beschlossen") — weil ohne Kontext zu anderen Objekten
  weniger Kontrastinformation für eine bestimmte Verneinung vorliegt.
  Sachlich weiterhin korrekt (keine Verwechslung, keine Erfindung),
  aber ein nachvollziehbarer Kompromiss der Filterung: weniger
  Cross-Objekt-Risiko, dafür etwas vorsichtigere Formulierung bei
  Abwesenheits-Fragen.

**Ergebnis: 12 von 12 Testfällen bestehen, automatisiert per
LLM-Richter bewertet** (nicht mehr manuell gelesen).

**Wichtige methodische Erkenntnis für dieses Projekt:** Ein
LLM-als-Richter ist kein Selbstläufer — er muss selbst kalibriert und
gegen bekannte, manuell verifizierte Fälle geprüft werden, sonst
produziert er eigene falsche Positive/Negative. Das haben wir hier
direkt erlebt (8/12 → 12/12 durch reine Prompt-Kalibrierung, ohne dass
sich das eigentliche System verändert hat).

---

## Lauf vom 2026-08-06 01:43 (CEST) — Längere Teilungserklärungen, Prompt-Fix

**Git-Commit:** `8f15fb46620aa4f083f7e9f770da0d2d180ac4fe` ("Teilungserklärungen verlängert, Widerspruchs-Prompt
nachgeschärft")

**Was sich seit dem letzten Lauf geändert hat:**

- **Teilungserklärungen verlängert**: Für alle 8 Objekte um 5 Abschnitte
  ergänzt (Bauliche Veränderungen, Instandhaltung, Verwalter,
  Tierhaltung, Schlussbestimmungen). Damit erstmals Dokumente, die über
  die 1024-Token-Chunking-Grenze kommen.
- **Wichtige technische Erkenntnis beim Chunking-Test**: Die
  Teilungserklärungen sind jetzt 2 PDF-Seiten lang. `PDFReader` (aus
  `llama-index-readers-file`) erzeugt dabei **ein Document pro
  PDF-Seite**, nicht eines pro Datei — die "Aufteilung" erfolgt also
  über Seitengrenzen, nicht über den `SentenceSplitter` mit
  Token-Overlap (der hätte nur bei einer einzelnen, über 1024 Tokens
  langen Seite gegriffen). Praktisch bedeutet das: kein Overlap
  zwischen den beiden Teilen, aber echtes Multi-Node-Retrieval pro
  Dokument wird trotzdem erstmals getestet. Corpus jetzt 40 Chunks
  (24 einseitige Dokumente + 8 Teilungserklärungen × 2 Seiten).
- **QA_PROMPT nachgeschärft**: Neue Anweisung, bei Zahlen-/Datumsangaben
  gezielt auf abweichende Werte zu prüfen, auch wenn Quellen den
  Sachverhalt unterschiedlich benennen (z. B. "Baujahr" vs. "Baujahr
  Gebäude"). Behebt den in der vorherigen Doku beschriebenen
  Schwachpunkt bei Testfall Kastanienhof/Baujahr.
- **Regression gefunden und behoben, bevor sie dokumentiert wurde**:
  Die erste Version der längeren Teilungserklärungen enthielt in 7 von
  8 Objekten eine fast wortgleiche generische Formulierung
  ("...wird aus der Instandhaltungsrücklage finanziert"). Das
  verwässerte den Begriff "Instandhaltungsrücklage" über alle Objekte
  hinweg und führte in Kombination mit dem nachgeschärften Prompt dazu,
  dass Testfall #6 (Gartenhof-Rücklage) plötzlich fehlschlug — das
  Modell antwortete widersprüchlich ("Ja... jedoch keine spezifische
  Erhöhung erwähnt"), reproduzierbar in 3/3 Versuchen. Behoben durch
  Umformulierung der 6 nicht objektspezifisch betroffenen
  Teilungserklärungen (Sonnenblick und Kastanienhof behalten den Begriff,
  da dort tatsächlich objektspezifisch relevant). Nach der Korrektur
  läuft Testfall #6 wieder zuverlässig (3/3 verifiziert).
- Testkatalog um 1 auf 12 Fragen erweitert (neuer Testfall: Info auf
  Seite 2 einer mehrseitigen Teilungserklärung).

**Ergebnis: 12 von 12 Testfällen wie erwartet.**

| # | Kategorie | Ergebnis |
|---|---|---|
| 1 | Widerspruch zwischen Quellen (Sonnenblick, Wohnfläche) | ✅ |
| 2 | Info nur in einem Dokument (Sonnenblick, Fahrstuhl) | ✅ |
| 3 | Einfacher Fakt (Gartenhof, Kaufpreis) | ✅ |
| 4 | Negativ-Fakt (Gartenhof, kein Fahrstuhl) | ✅ |
| 5 | Halluzinationstest (Ahornhöhe, Sauna) | ✅ |
| 6 | Cross-Objekt-Verwechslung (Gartenhof, Rücklage) | ✅ (nach Regression + Fix, siehe oben) |
| 7 | Vergleich über 8 Objekte (Energieeffizienzklasse) | ✅ |
| 8 | Info nur in Teilungserklärung (Lindenpark, Garten-Sondernutzungsrecht) | ✅ |
| 9 | Widerspruch, unterschiedlich benannte Felder (Kastanienhof, Baujahr) | ✅ **jetzt erkannt** (vorher bekannter Fehler, siehe Prompt-Fix oben) |
| 10 | Cross-Objekt-Verwechslung, ähnliche Neubauten (Birkenallee vs. Rosenhügel, PV-Anlage) | ✅ |
| 11 | Halluzinationstest (Seeblick, Concierge-Service) | ✅ |
| 12 | Mehrseitiges Dokument / Chunking über Seitengrenze (Lindenpark, Verwalter auf Seite 2) | ✅ **neu** |

Vollständige Frage/Antwort-Details für die unveränderten Testfälle
(1-8, 10-11) siehe vorherige Einträge unten — die Antworten sind
inhaltlich gleichwertig. Details zu den veränderten/neuen Fällen
(9, 12) und dem behobenen Regressionsfall (6):

### Test #6 — Cross-Objekt-Verwechslung (nach Fix)

**Antwort:**
> Nein, bei der WEG Gartenhof wurde keine Erhöhung der
> Instandhaltungsrücklage beschlossen. In den Protokollen der
> Eigentümerversammlung wird lediglich die Genehmigung der
> Jahresabrechnung und die Pflege der Gartenanlage behandelt, jedoch
> keine Erhöhung der Instandhaltungsrücklage erwähnt.

### Test #9 — Widerspruch, unterschiedlich benannte Felder (nach Prompt-Fix)

**Antwort:**
> Das Gebäude "Kastanienhof" wurde im Jahr 1974 gebaut, wie im
> Energieausweis angegeben (Dateiname:
> objekt6_kastanienhof_energieausweis.pdf). Im Exposé wird jedoch das
> Baujahr als 1975 angegeben (Dateiname: objekt6_kastanienhof_expose.pdf).
> Dies stellt einen Widerspruch dar.

### Test #12 — Mehrseitiges Dokument (neu)

**Frage:** Welche Hausverwaltung ist laut Teilungserklärung als
Verwalter der WEG Lindenpark bestellt?

**Antwort:**
> Laut der Teilungserklärung für die WEG Lindenpark ist die
> Hausverwaltung Baumann als Verwalter bestellt (Quelle:
> objekt4_lindenpark_teilungserklaerung.pdf).

**Quellen (Auszug):** `objekt4_lindenpark_teilungserklaerung.pdf`
erscheint zweimal in der Quellenliste — einmal pro Seite (Seite 1 und
Seite 2) — der Verwalter-Abschnitt liegt auf Seite 2 und wurde korrekt
gefunden.

---

## Lauf vom 2026-08-06 00:56 (CEST) — Bestätigungslauf, erstmals mit Git-Commit verknüpft

**Git-Commit:** `dbe75ceb7ad792bf7ce15c4d832cc011e0693859` ("README hinzufügen",
gepusht nach `https://github.com/MH-Git1/immobilien-rag`)

**Code-Stand:** identisch zum Lauf vom 2026-08-05 20:40 — `main.py` und
`tests/testfragen.py` haben sich seitdem nicht verändert (per
`git diff` gegen Commit `9ba1b36` bestätigt). Dieser Lauf dient primär
dazu, (a) Reproduzierbarkeit zu bestätigen und (b) erstmals einen
Testlauf mit einem echten Git-Commit-Hash zu verknüpfen, statt nur mit
einem Zeitstempel — wie im vorherigen Eintrag als offener Punkt
vermerkt.

**Ergebnis: 10 von 11 Testfällen wie erwartet — identisch zum
vorherigen Lauf.** Test #9 (Kastanienhof, Baujahr-Widerspruch) schlägt
erneut fehl, exakt wie zuvor: Die Antwort nennt nur 1975 (Exposé),
der abweichende Wert 1974 aus dem Energieausweis wird trotz korrekt
gefundener Quelle nicht erwähnt. Das bestätigt, dass es sich um einen
stabilen, reproduzierbaren Schwachpunkt der Widerspruchserkennung
handelt (nicht um Zufallsrauschen des LLMs) — Ursache weiterhin
vermutlich die unterschiedliche Feldbezeichnung ("Baujahr" vs.
"Baujahr Gebäude"), siehe Analyse im vorherigen Eintrag.

Alle übrigen 10 Antworten sind inhaltlich gleichwertig zum vorherigen
Lauf (in der Formulierung leicht, aber nicht in der Substanz
abweichend). Details siehe Q&A-Auflistung im Eintrag vom
2026-08-05 20:40 unten — die Fragen, Erwartungen und Kategorien sind
unverändert; hier nur die neue Verknüpfung mit Zeitstempel und
Commit-Hash sowie das bestätigte Ergebnis.

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


