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
            "objekt1_sonnenblick_protokoll.txt — diese Info steht "
            "nirgendwo sonst."
        ),
    },
    {
        "frage": "Wie hoch ist der Kaufpreis der Wohnung Gartenhof?",
        "kategorie": "Einfacher Fakt (Kontrollfrage)",
        "erwartung": "229.000 EUR, Quelle objekt2_gartenhof_expose.txt.",
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
            "Welches der drei Objekte hat die beste Energieeffizienzklasse?"
        ),
        "kategorie": "Vergleich über mehrere Objekte",
        "erwartung": (
            "Ahornhöhe (Klasse A) ist am besten, vor Gartenhof (C) und "
            "Sonnenblick (D). Testet, ob similarity_top_k genug Kontext "
            "aus allen drei Objekten liefert, um einen vollständigen "
            "Vergleich zu ermöglichen."
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
