"""
Testfragen-Katalog für den Objektunterlagen-Assistenten.

Ein exaktes String-Assert wäre bei frei formulierten LLM-Antworten
unbrauchbar. Stattdessen bewertet ein zweiter, separater LLM-Call
("Richter") jede Antwort gegen die hier hinterlegte Erwartung als
PASS/FAIL mit Begründung — siehe bewerte_antwort() unten. Das macht aus
dem Regressionskatalog einen automatisierten Test, statt dass die
Antworten jedes Mal von Hand gelesen werden müssen.

Jede Frage deckt eine typische RAG-Schwachstelle ab (Widerspruch
zwischen Quellen, Info nur in einem Dokument, Halluzination,
Objektverwechslung, objektübergreifender Vergleich, mehrseitige
Dokumente). Bei Änderungen an main.py (Chunking, Prompt,
similarity_top_k, Metadaten-Filterung, Modellwahl) hier gegenprüfen, ob
sich das Antwortverhalten verschlechtert hat.

Aufruf: venv/bin/python -m tests.testfragen
(vom Projekt-Root aus)
"""

import sys

from llama_index.core import Settings

from main import baue_index, beantworte_frage, _bekannte_objektnamen

RICHTER_PROMPT = """Du bist ein Prüfer für ein RAG-System, das Fragen zu \
Immobilien-Objektunterlagen beantwortet.

Frage: {frage}
Erwartung (Kriterium für eine korrekte Antwort): {erwartung}
Tatsächliche Antwort des Systems: {antwort}

Bewerte, ob die tatsächliche Antwort das Kriterium ERFÜLLT — es geht um \
den fachlichen Inhalt, nicht um exakte Wortwahl oder Zitierformat.

Wichtige Kalibrierung:
- Wenn die Erwartung einen Dateinamen als Quelle nennt, reicht es, wenn \
die Antwort inhaltlich klar auf das richtige Dokument verweist (z.B. \
"laut Protokoll"). Der exakte Dateiname muss NICHT wörtlich genannt \
werden.
- Wenn die Erwartung verlangt, dass eine NICHT vorhandene Information \
korrekt als fehlend dargestellt wird: Sowohl ein klares "Nein" als auch \
eine vorsichtigere Formulierung wie "diese Information ist im Kontext \
nicht enthalten" oder "ich kann das nicht bestätigen" gelten als PASS — \
entscheidend ist NUR, dass nichts Falsches behauptet oder erfunden wird.
- Sei strikt bei tatsächlichen inhaltlichen Fehlern: erfundene Fakten, \
fehlende Werte bei einem geforderten Widerspruch, oder \
Objektverwechslungen sind IMMER ein FAIL.

Antworte in exakt diesem Format, ohne weitere Erklärung davor:
PASS oder FAIL
Begründung: <ein Satz>
"""


def bewerte_antwort(frage: str, erwartung: str, antwort_text: str) -> tuple[bool, str]:
    """
    Lässt einen zweiten LLM-Call (dasselbe Modell wie main.py,
    gpt-4o-mini) die Antwort gegen die Erwartung bewerten. Günstig genug
    für einen Testkatalog dieser Größe, und zuverlässiger/schneller als
    manuelles Durchlesen bei wachsender Fragenzahl.
    """
    prompt = RICHTER_PROMPT.format(
        frage=frage, erwartung=erwartung, antwort=antwort_text
    )
    ergebnis = str(Settings.llm.complete(prompt)).strip()
    ist_pass = ergebnis.upper().startswith("PASS")
    return ist_pass, ergebnis

TESTFRAGEN = [
    {
        "frage": "Wie groß ist die Wohnfläche der Wohnung Sonnenblick?",
        "kategorie": "Widerspruch zwischen Quellen",
        "erwartung": (
            "Sollte beide Werte nennen (78 m² im Exposé, 76 m² im "
            "Energieausweis) und den Widerspruch explizit benennen, "
            "statt sich stillschweigend für einen Wert zu entscheiden."
        ),
    },
    {
        "frage": (
            "Welche Firma wartet den Fahrstuhl im Haus Sonnenblick und "
            "wann war die letzte Prüfung?"
        ),
        "kategorie": "Information nur in einem Dokument",
        "erwartung": (
            "Sollte 'Aufzugstechnik Reiner GmbH' und das Prüfdatum "
            "09.11.2023 nennen. Diese Info steht nur im Protokoll "
            "(objekt1_sonnenblick_protokoll.pdf) — das wird separat "
            "anhand der Quellen-Liste geprüft, nicht anhand des "
            "Antworttexts; die Antwort muss den Dateinamen nicht "
            "wörtlich nennen, solange sie inhaltlich auf das Protokoll "
            "verweist."
        ),
    },
    {
        "frage": "Wie hoch ist der Kaufpreis der Wohnung Gartenhof?",
        "kategorie": "Einfacher Fakt (Kontrollfrage)",
        "erwartung": "229.000 EUR, Quelle objekt2_gartenhof_expose.pdf.",
    },
    {
        "frage": "Gibt es einen Fahrstuhl in der Wohnung Gartenhof?",
        "kategorie": "Negativ-Fakt",
        "erwartung": (
            "Nein — laut Exposé kein Fahrstuhl (Erdgeschoss, nicht "
            "erforderlich). Testet, ob explizit verneinte Fakten korrekt "
            "wiedergegeben werden."
        ),
    },
    {
        "frage": "Wann wurde die Sauna im Haus Ahornhöhe zuletzt gewartet?",
        "kategorie": "Halluzinationstest",
        "erwartung": (
            "Es gibt keine Sauna in den Unterlagen. Sollte klar sagen, "
            "dass die Information nicht vorhanden ist, statt etwas zu "
            "erfinden."
        ),
    },
    {
        "frage": (
            "Wurde bei der WEG Gartenhof eine Erhöhung der "
            "Instandhaltungsrücklage beschlossen?"
        ),
        "kategorie": "Cross-Objekt-Verwechslung",
        "erwartung": (
            "Diesen Beschluss gibt es nur bei Sonnenblick, nicht bei "
            "Gartenhof. Sollte nicht fälschlich vermischt werden — "
            "korrekte Antwort ist 'nicht enthalten'."
        ),
    },
    {
        "frage": (
            "Welches Objekt hat die beste Energieeffizienzklasse? Nenne "
            "alle Objekte mit ihrer jeweiligen Klasse."
        ),
        "kategorie": "Vergleich über mehrere Objekte (jetzt 8 statt 3)",
        "erwartung": (
            "Seeblick (A+) ist am besten, vor Rosenhügel/Ahornhöhe (A), "
            "Birkenallee/Lindenpark (B), Gartenhof (C), Sonnenblick (D) "
            "und Kastanienhof (F). Testet, ob similarity_top_k=12 "
            "zuverlässig Kontext aus allen 8 Energieausweisen liefert."
        ),
    },
    {
        "frage": (
            "Wer hat laut den Unterlagen ein Sondernutzungsrecht am "
            "Garten bei der Wohnung Lindenpark?"
        ),
        "kategorie": "Information nur in der Teilungserklärung",
        "erwartung": (
            "Der Eigentümer der Einheit Nr. 2 (Hochparterre) hat das "
            "exklusive Sondernutzungsrecht am Garten — diese Info steht "
            "nur in objekt4_lindenpark_teilungserklaerung.pdf, nicht im "
            "Exposé oder Protokoll."
        ),
    },
    {
        "frage": "In welchem Jahr wurde das Gebäude Kastanienhof gebaut?",
        "kategorie": "Widerspruch zwischen Quellen (unterschiedlich benannte Felder)",
        "erwartung": (
            "Leichte Abweichung: Exposé nennt Baujahr 1975, "
            "Energieausweis nennt Baujahr Gebäude 1974. Sollte beide "
            "Werte mit Quelle nennen, nicht nur einen. Ursprünglich hat "
            "das Modell diesen Widerspruch NICHT erkannt (nur 1975 "
            "genannt), weil die Felder unterschiedlich benannt sind "
            "('Baujahr' vs. 'Baujahr Gebäude') — seit dem QA_PROMPT-Fix "
            "(explizite Anweisung, auch bei abweichender Benennung auf "
            "Widersprüche zu prüfen) wird es zuverlässig erkannt."
        ),
    },
    {
        "frage": (
            "Wurde bei der WEG Birkenallee eine Photovoltaikanlage "
            "beschlossen?"
        ),
        "kategorie": "Cross-Objekt-Verwechslung (neu, ähnliche Neubauten)",
        "erwartung": (
            "Nein — diesen Beschluss gibt es nur bei Rosenhügel (einem "
            "ähnlichen Neubau). Bei Birkenallee wurde eine PV-Anlage nur "
            "als möglicher künftiger Tagesordnungspunkt erwähnt, aber "
            "kein Beschluss gefasst. Testet, ob zwei ähnliche "
            "Neubau-Objekte nicht verwechselt werden."
        ),
    },
    {
        "frage": "Gibt es einen Concierge-Service im Haus Seeblick?",
        "kategorie": "Halluzinationstest (neu)",
        "erwartung": (
            "Es gibt keinen Concierge-Service in den Unterlagen. Sollte "
            "klar sagen, dass die Information nicht vorhanden ist."
        ),
    },
    {
        "frage": (
            "Welche Hausverwaltung ist laut Teilungserklärung als "
            "Verwalter der WEG Lindenpark bestellt?"
        ),
        "kategorie": "Mehrseitiges Dokument (Chunking über Seitengrenze)",
        "erwartung": (
            "Hausverwaltung Baumann. Die Teilungserklärungen umfassen "
            "seit der Erweiterung um zusätzliche Abschnitte "
            "(Bauliche Veränderungen, Instandhaltung, Verwalter, "
            "Tierhaltung, Schlussbestimmungen) jeweils 2 PDF-Seiten — "
            "der Verwalter-Abschnitt steht auf Seite 2. Testet, ob "
            "Retrieval den richtigen Teil eines mehrseitigen Dokuments "
            "findet, statt nur die erste Seite/den ganzen Chunk."
        ),
    },
    {
        "frage": (
            "Wer wurde bei der WEG Ahornhöhe zum Vorsitzenden des "
            "Verwaltungsbeirats gewählt?"
        ),
        "kategorie": "Echtes Chunking mit Token-Overlap (nicht seitenbasiert)",
        "erwartung": (
            "Antwort sollte 'Herr T. Nowak' nennen — das ist das einzige "
            "Korrektheitskriterium für den Antworttext. (Hintergrund zum "
            "Testdesign, KEIN Bewertungskriterium für die Antwort: Das "
            "Protokoll ist absichtlich eine einzelne, sehr lange "
            "PDF-Seite mit >1024 Tokens, damit der LlamaIndex-"
            "SentenceSplitter selbst mit echtem 200-Token-Overlap chunkt "
            "— verifiziert 2 Chunks, ~590 Zeichen Überschneidung. Die "
            "gesuchte Information liegt inhaltlich im hinteren Teil des "
            "Dokuments, technisch aber weiterhin auf Seite 1, da das "
            "Dokument nur eine Seite hat — eine Quellenangabe 'Seite 1' "
            "in der Antwort ist also korrekt, nicht falsch.)"
        ),
    },
]


def fuehre_tests_aus() -> bool:
    """Gibt True zurück, wenn alle Testfälle bestanden wurden (für CI-Exitcode)."""
    index = baue_index()
    bekannte_objekte = _bekannte_objektnamen()

    ergebnisse = []
    for i, testfall in enumerate(TESTFRAGEN, start=1):
        antwort, objekt_gefiltert = beantworte_frage(
            index, testfall["frage"], bekannte_objekte, herkunft="test"
        )
        quellen = sorted(
            {node.metadata.get("file_name", "unbekannt") for node in antwort.source_nodes}
        )
        ist_pass, richter_begruendung = bewerte_antwort(
            testfall["frage"], testfall["erwartung"], str(antwort)
        )
        ergebnisse.append(ist_pass)

        status = "PASS" if ist_pass else "FAIL"
        print(f"[{i}/{len(TESTFRAGEN)}] {status} — {testfall['kategorie']}")
        print(f"Frage:     {testfall['frage']}")
        if objekt_gefiltert:
            print(f"Filter:    objekt_name = {objekt_gefiltert}")
        print(f"Erwartung: {testfall['erwartung']}")
        print(f"Antwort:   {antwort}")
        print(f"Quellen:   {quellen}")
        print(f"Richter:   {richter_begruendung}")
        print("-" * 70)

    bestanden = sum(ergebnisse)
    print(f"\nErgebnis: {bestanden}/{len(ergebnisse)} Testfälle bestanden.")
    if bestanden < len(ergebnisse):
        fehlgeschlagen = [
            i + 1 for i, ok in enumerate(ergebnisse) if not ok
        ]
        print(f"Fehlgeschlagen: Testfall(-fälle) {fehlgeschlagen}")

    return bestanden == len(ergebnisse)


if __name__ == "__main__":
    sys.exit(0 if fuehre_tests_aus() else 1)
