"""
Erzeugt die Objektunterlagen als PDF in data_pdf/, im Stil der
recherchierten echten Vorlagen (stawag-Energieausweis, WEG-Wissen-
Protokoll): Kopfzeile mit Gesetzesverweis, Fußnoten, klare
Abschnittsgliederung. Inhalte sind vollständig erfunden (siehe
objektdaten.py).

Aufruf: venv/bin/python scripts/generate_pdfs.py
"""

import os

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)

from objektdaten import OBJEKTE

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "data_pdf")

# --- Styles, angelehnt an die echten Vorlagen (Kopfzeile mit
# Gesetzesverweis, kleine Fußnoten, klare Sektionsüberschriften) ---
_styles = getSampleStyleSheet()
STYLE_TITLE = ParagraphStyle(
    "TitelDoc", parent=_styles["Title"], fontSize=15, spaceAfter=4,
)
STYLE_KOPFZEILE = ParagraphStyle(
    "Kopfzeile", parent=_styles["Normal"], fontSize=8, textColor=colors.grey,
    spaceAfter=10,
)
STYLE_SECTION = ParagraphStyle(
    "Section", parent=_styles["Heading2"], fontSize=11, spaceBefore=12,
    spaceAfter=4,
)
STYLE_BODY = ParagraphStyle(
    "Body", parent=_styles["Normal"], fontSize=9.5, leading=13.5,
)
STYLE_FOOTNOTE = ParagraphStyle(
    "Footnote", parent=_styles["Normal"], fontSize=7, textColor=colors.grey,
    leading=9,
)

TABLE_STYLE = TableStyle([
    ("FONTSIZE", (0, 0), (-1, -1), 9),
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.lightgrey),
])


def _feld_tabelle(zeilen):
    """Baut eine zweispaltige Tabelle Label/Wert (überspringt None-Werte)."""
    daten = [(f"{label}:", wert) for label, wert in zeilen if wert]
    tab = Table(daten, colWidths=[5.5 * cm, 10.5 * cm])
    tab.setStyle(TABLE_STYLE)
    return tab


def _dokument(dateiname, story):
    pfad = os.path.join(OUTPUT_DIR, dateiname)
    doc = SimpleDocTemplate(
        pfad, pagesize=A4,
        topMargin=2 * cm, bottomMargin=2 * cm,
        leftMargin=2.2 * cm, rightMargin=2.2 * cm,
    )
    doc.build(story)
    return dateiname


def render_expose(objekt):
    e = objekt["expose"]
    story = [
        Paragraph("EXPOSÉ", STYLE_TITLE),
        Paragraph(
            f'Wohnung "{objekt["name"]}"<br/>{objekt["adresse"]}',
            STYLE_KOPFZEILE,
        ),
        Paragraph("Objektbeschreibung", STYLE_SECTION),
        Paragraph(e["beschreibung"], STYLE_BODY),
        Paragraph("Eckdaten", STYLE_SECTION),
        _feld_tabelle([
            ("Wohnfläche", e["wohnflaeche"]),
            ("Zimmer", e["zimmer"]),
            ("Baujahr", e["baujahr"]),
            ("Etage", e["etage"]),
            ("Kaufpreis", e["kaufpreis"]),
            ("Hausgeld (monatlich)", e["hausgeld"]),
            ("Stellplatz", e["stellplatz"]),
            ("Bezugsfrei ab", e["bezugsfrei"]),
        ]),
        Paragraph("Ausstattung", STYLE_SECTION),
    ]
    for punkt in e["ausstattung"]:
        story.append(Paragraph(f"– {punkt}", STYLE_BODY))
    story += [
        Paragraph("Lage", STYLE_SECTION),
        Paragraph(e["lage"], STYLE_BODY),
        Paragraph("Kontakt", STYLE_SECTION),
        Paragraph(
            f'Bonorum Immobilien GmbH<br/>Ansprechpartner: {e["kontakt_name"]}'
            f'<br/>Tel: {e["kontakt_tel"]}<br/>E-Mail: {e["kontakt_email"]}',
            STYLE_BODY,
        ),
        Spacer(1, 0.6 * cm),
        Paragraph(
            "Diese Angaben beruhen auf den Unterlagen des Verkäufers und "
            "wurden nach bestem Wissen zusammengestellt. Irrtümer und "
            "Zwischenverkauf vorbehalten.",
            STYLE_FOOTNOTE,
        ),
    ]
    dateiname = f'{objekt["id"]}_{objekt["name"].lower()}_expose.pdf'
    return _dokument(dateiname, story)


def render_energieausweis(objekt):
    a = objekt["energieausweis"]
    story = [
        Paragraph("ENERGIEAUSWEIS für Wohngebäude", STYLE_TITLE),
        Paragraph(
            "gemäß den §§ 16 ff. Gebäudeenergiegesetz (GEG) "
            f'<br/>Objekt: Wohnung "{objekt["name"]}", {objekt["adresse"]}',
            STYLE_KOPFZEILE,
        ),
        Paragraph("Art des Ausweises", STYLE_SECTION),
        Paragraph(a["art"], STYLE_BODY),
        Paragraph("Gebäudedaten", STYLE_SECTION),
        _feld_tabelle([
            ("Gebäudetyp", a["gebaeudetyp"]),
            ("Baujahr Gebäude", a["baujahr_gebaeude"]),
            ("Baujahr Wärmeerzeuger", a["baujahr_waermeerzeuger"]),
            ("Wohnfläche (Berechnung)", a["wohnflaeche"]),
            ("Anzahl Wohneinheiten im Gebäude", a["einheiten"]),
        ]),
        Paragraph("Energetische Kennwerte", STYLE_SECTION),
        _feld_tabelle([
            (
                "Endenergiebedarf" if a["art"] == "Bedarfsausweis"
                else "Endenergieverbrauch",
                a["endenergie"],
            ),
            ("Primärenergiebedarf", a["primaerenergie"]),
            ("Energieeffizienzklasse", a["klasse"]),
        ]),
        Paragraph("Wesentliche Energieträger", STYLE_SECTION),
        _feld_tabelle([
            ("Heizung", a["heizung"]),
            ("Warmwasser", a["warmwasser"]),
        ]),
    ]
    if a["empfehlungen"]:
        story.append(
            Paragraph(
                "Empfehlungen zur Verbesserung der Energieeffizienz",
                STYLE_SECTION,
            )
        )
        for empf in a["empfehlungen"]:
            story.append(Paragraph(f"– {empf}", STYLE_BODY))
    story += [
        Paragraph("Gültigkeit", STYLE_SECTION),
        _feld_tabelle([
            ("Ausstellungsdatum", a["ausstellungsdatum"]),
            ("Gültig bis", a["gueltig_bis"]),
        ]),
        Paragraph("Aussteller", STYLE_SECTION),
        Paragraph(
            f'Ing.-Büro für Energieberatung Hoffmann'
            f'<br/>Registriernummer: {a["registriernummer"]}',
            STYLE_BODY,
        ),
        Spacer(1, 0.6 * cm),
        Paragraph(
            "Hinweis: Dieser Energieausweis dient nur der Information über "
            "die energetische Qualität des Gebäudes und ersetzt keine "
            "technische Beratung vor Ort. Erläuterungen zum Verfahren: Das "
            "GEG lässt für die Berechnung des Energiebedarfs "
            "unterschiedliche Verfahren zu, die im Einzelfall zu "
            "unterschiedlichen Ergebnissen führen können.",
            STYLE_FOOTNOTE,
        ),
    ]
    dateiname = f'{objekt["id"]}_{objekt["name"].lower()}_energieausweis.pdf'
    return _dokument(dateiname, story)


def render_protokoll(objekt):
    p = objekt["protokoll"]
    story = [
        Paragraph("PROTOKOLL DER ORDENTLICHEN EIGENTÜMERVERSAMMLUNG", STYLE_TITLE),
        Paragraph(
            f'Wohnungseigentümergemeinschaft (WEG) {objekt["adresse"]}'
            f'<br/>"{objekt["name"]}"',
            STYLE_KOPFZEILE,
        ),
        Paragraph("Angaben zur Versammlung", STYLE_SECTION),
        _feld_tabelle([
            ("Datum", p["datum"]),
            ("Beginn", p["beginn"]),
            ("Ende", p["ende"]),
            ("Ort", p["ort"]),
            ("Versammlungsleiter", p["versammlungsleiter"]),
            ("Protokollführer/in", p["protokollfuehrer"]),
        ]),
        Paragraph("Anwesenheit", STYLE_SECTION),
        Paragraph(
            f'Anwesend bzw. vertreten: {p["anwesenheit"]} der Stimmrechte. '
            "Die Versammlung ist beschlussfähig.",
            STYLE_BODY,
        ),
        Paragraph("Tagesordnungspunkte", STYLE_SECTION),
    ]
    for i, (titel, text) in enumerate(p["tops"], start=1):
        story.append(Paragraph(f"TOP {i}: {titel}", STYLE_SECTION))
        story.append(Paragraph(text, STYLE_BODY))
    story += [
        Spacer(1, 0.6 * cm),
        Paragraph(
            "Nächste ordentliche Eigentümerversammlung voraussichtlich im "
            "Frühjahr 2025.",
            STYLE_FOOTNOTE,
        ),
    ]
    dateiname = f'{objekt["id"]}_{objekt["name"].lower()}_protokoll.pdf'
    return _dokument(dateiname, story)


def render_teilungserklaerung(objekt):
    t = objekt["teilungserklaerung"]
    story = [
        Paragraph("TEILUNGSERKLÄRUNG", STYLE_TITLE),
        Paragraph(
            f'gemäß § 8 Wohnungseigentumsgesetz (WEG)'
            f'<br/>Objekt: {objekt["adresse"]} — "{objekt["name"]}"',
            STYLE_KOPFZEILE,
        ),
        Paragraph("Notarielle Angaben", STYLE_SECTION),
        _feld_tabelle([
            ("Beurkundender Notar", t["notar"]),
            ("Urkundenrolle", t["urkundenrolle"]),
            ("Datum der Beurkundung", t["datum"]),
        ]),
        Paragraph("Aufteilung des Gebäudes", STYLE_SECTION),
        Paragraph(t["einheiten_hinweis"], STYLE_BODY),
        Paragraph("Miteigentumsanteil und Sondereigentum", STYLE_SECTION),
        _feld_tabelle([
            ("Miteigentumsanteil dieser Einheit", t["miteigentumsanteil"]),
        ]),
        Paragraph(t["sondereigentum"], STYLE_BODY),
        Paragraph("Gemeinschaftseigentum", STYLE_SECTION),
        Paragraph(t["gemeinschaftseigentum"], STYLE_BODY),
        Paragraph("Kostenverteilerschlüssel", STYLE_SECTION),
        Paragraph(t["kostenverteilung"], STYLE_BODY),
        Paragraph("Sondernutzungsrechte", STYLE_SECTION),
        Paragraph(t["sondernutzungsrechte"], STYLE_BODY),
        Paragraph("Stimmrecht", STYLE_SECTION),
        Paragraph(t["stimmrecht"], STYLE_BODY),
        Spacer(1, 0.6 * cm),
        Paragraph(
            "Diese Teilungserklärung regelt gemäß § 8 WEG die Aufteilung "
            "des Grundstücks in Wohnungseigentum. Änderungen bedürfen der "
            "notariellen Form und der Zustimmung der Wohnungseigentümer "
            "im gesetzlich vorgesehenen Umfang.",
            STYLE_FOOTNOTE,
        ),
    ]
    dateiname = f'{objekt["id"]}_{objekt["name"].lower()}_teilungserklaerung.pdf'
    return _dokument(dateiname, story)


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    erzeugt = []
    for objekt in OBJEKTE:
        erzeugt.append(render_expose(objekt))
        erzeugt.append(render_energieausweis(objekt))
        erzeugt.append(render_protokoll(objekt))
        erzeugt.append(render_teilungserklaerung(objekt))

    # Namenskollisionen prüfen (sollte durch objekt-ID + Typ nie passieren,
    # aber sicherheitshalber verifizieren statt anzunehmen)
    duplikate = {name for name in erzeugt if erzeugt.count(name) > 1}
    if duplikate:
        raise RuntimeError(f"Doppelte Dateinamen erzeugt: {duplikate}")

    print(f"{len(erzeugt)} PDFs erzeugt in '{OUTPUT_DIR}':")
    for name in erzeugt:
        print(f"  - {name}")


if __name__ == "__main__":
    main()
