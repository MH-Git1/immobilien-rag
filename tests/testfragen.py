"""
Testfragen-Katalog für den Objektunterlagen-Assistenten.

Das sind keine automatischen Pass/Fail-Tests im klassischen Sinn — die
Antworten kommen vom LLM und sind frei formuliert, ein exaktes
String-Assert wäre unbrauchbar. Stattdessen ist das ein
Regressionskatalog: Jede Frage deckt eine typische RAG-Schwachstelle ab
(Widerspruch zwischen Quellen, Info nur in einem Dokument, Halluzination,
Objektverwechslung, objektübergreifender Vergleich). Bei Änderungen an
main.py (Chunking, Prompt, similarity_top_k, Modellwahl) hier gegenprüfen,
ob sich das Antwortverhalten verschlechtert hat.

Aufruf: venv/bin/python -m tests.testfragen
(vom Projekt-Root aus)
"""

from main import baue_index, QA_PROMPT, SIMILARITY_TOP_K

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
            "09.11.2023 nennen, mit Quelle "
            "objekt1_sonnenblick_protokoll.pdf — diese Info steht "
            "nirgendwo sonst."
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
        "kategorie": "Widerspruch zwischen Quellen (neu)",
        "erwartung": (
            "Leichte Abweichung: Exposé nennt Baujahr 1975, "
            "Energieausweis nennt Baujahr Gebäude 1974. Sollte beide "
            "Werte mit Quelle nennen, nicht nur einen."
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
]


def fuehre_tests_aus() -> None:
    index = baue_index()
    query_engine = index.as_query_engine(similarity_top_k=SIMILARITY_TOP_K)
    query_engine.update_prompts(
        {"response_synthesizer:text_qa_template": QA_PROMPT}
    )

    for i, testfall in enumerate(TESTFRAGEN, start=1):
        antwort = query_engine.query(testfall["frage"])
        quellen = [
            node.metadata.get("file_name", "unbekannt")
            for node in antwort.source_nodes
        ]

        print(f"[{i}/{len(TESTFRAGEN)}] {testfall['kategorie']}")
        print(f"Frage:     {testfall['frage']}")
        print(f"Erwartung: {testfall['erwartung']}")
        print(f"Antwort:   {antwort}")
        print(f"Quellen:   {quellen}")
        print("-" * 70)


if __name__ == "__main__":
    fuehre_tests_aus()
