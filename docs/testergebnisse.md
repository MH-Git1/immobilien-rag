# Testergebnisse — Objektunterlagen-Assistent

Dieses Dokument protokolliert Testläufe des RAG-Systems mit Zeitstempel,
damit sich ein Ergebnis-Snapshot später einem bestimmten Code-Stand
zuordnen lässt. Quelle der Fragen: `tests/testfragen.py`.

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
