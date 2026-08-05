"""
Objektdaten für die PDF-Generierung (scripts/generate_pdfs.py).

8 fiktive Objekte x 4 Dokumenttypen (Exposé, Energieausweis, Protokoll,
Teilungserklärung) = 32 Dokumente. Objekte 1-3 sind die bisherigen
Test-Objekte (Sonnenblick, Gartenhof, Ahornhöhe) — deren bereits
etablierte Testfälle (Widerspruch, Info-nur-in-einem-Dokument,
Cross-Objekt-Verwechslung) bleiben unverändert erhalten. Objekte 4-8
sind neu und bringen zusätzliche Testfälle mit (siehe Kommentare unten
und tests/testfragen.py).
"""

OBJEKTE = [
    # ------------------------------------------------------------------
    # Objekt 1: Sonnenblick (bestehend)
    # Testfälle: Wohnfläche-Widerspruch Exposé/Energieausweis (78/76 m²);
    # Fahrstuhlwartung nur im Protokoll.
    # ------------------------------------------------------------------
    {
        "id": "objekt1",
        "name": "Sonnenblick",
        "adresse": "Musterstraße 12, 80331 München (Altstadt-Lehel)",
        "expose": {
            "beschreibung": (
                "Diese lichtdurchflutete 3-Zimmer-Eigentumswohnung befindet "
                "sich im 3. Obergeschoss eines gepflegten Altbaus aus dem "
                "Jahr 1962, der 2018 vollständig saniert wurde. Die Wohnung "
                "überzeugt durch einen offenen Wohn-Essbereich, einen "
                "sonnigen Süd-West-Balkon sowie hochwertige Parkettböden in "
                "allen Wohnräumen."
            ),
            "wohnflaeche": "78 m²",
            "zimmer": "3",
            "baujahr": "1962 (Sanierung 2018)",
            "etage": "3. OG von 5",
            "kaufpreis": "459.000 EUR",
            "hausgeld": "285 EUR",
            "stellplatz": "1 Tiefgaragenstellplatz (im Preis enthalten)",
            "bezugsfrei": "sofort",
            "ausstattung": [
                "Einbauküche (2019, Marke Nolte)",
                "Parkettboden in Wohn- und Schlafräumen, Fliesen in Bad und Küche",
                "Bad mit Wanne und separater Dusche, bodengleich",
                "Balkon (Süd-West-Ausrichtung, ca. 8 m²)",
                "Kellerabteil (ca. 5 m²)",
                "Fahrstuhl im Haus vorhanden",
            ],
            "lage": (
                "Ruhige Seitenstraße im beliebten Lehel, fußläufig zum "
                "Englischen Garten (ca. 10 Minuten) und zur Isar. Gute "
                "Anbindung an den ÖPNV (U-Bahn Lehel, 5 Gehminuten)."
            ),
            "kontakt_name": "Frau S. Reiter",
            "kontakt_tel": "089 / 555-0142",
            "kontakt_email": "reiter@musterwert-immobilien-beispiel.de",
        },
        "energieausweis": {
            "art": "Bedarfsausweis",
            "gebaeudetyp": "Mehrfamilienhaus, Wohnungseigentum",
            "baujahr_gebaeude": "1962",
            "baujahr_waermeerzeuger": "2019 (Gas-Brennwertkessel, zentral)",
            "wohnflaeche": "76 m²",
            "einheiten": "12",
            "endenergie": "118 kWh/(m²·a)",
            "primaerenergie": "132 kWh/(m²·a)",
            "klasse": "D",
            "heizung": "Erdgas (zentral, Etagen-Wärmemengenzähler)",
            "warmwasser": "zentral über Heizungsanlage",
            "empfehlungen": [
                "Dämmung der obersten Geschossdecke",
                "Austausch der Fenster im Bereich der Nordfassade",
                "Hydraulischer Abgleich der Heizungsanlage",
            ],
            "ausstellungsdatum": "14.03.2024",
            "gueltig_bis": "13.03.2034",
            "registriernummer": "DE-2024-9931-EAB",
        },
        "protokoll": {
            "datum": "22.04.2024",
            "beginn": "18:30 Uhr",
            "ende": "20:15 Uhr",
            "ort": "Gemeinschaftsraum im Erdgeschoss, Musterstraße 12",
            "versammlungsleiter": "Herr K. Brunner (Hausverwaltung Brunner & Partner)",
            "protokollfuehrer": "Frau L. Vogt",
            "anwesenheit": "9 von 12 Miteigentumsanteilen (78 %)",
            "tops": [
                (
                    "Genehmigung der Jahresabrechnung 2023",
                    "Die Jahresabrechnung 2023 wurde von der Verwaltung "
                    "vorgestellt und im Vorfeld an alle Eigentümer "
                    "versandt. Beschluss: Genehmigt mit 9 Ja-Stimmen, "
                    "0 Gegenstimmen, 0 Enthaltungen.",
                ),
                (
                    "Wartung und Zustand des Fahrstuhls",
                    "Der Fahrstuhl im Treppenhaus wird seit 2015 durch die "
                    "Firma Aufzugstechnik Reiner GmbH gewartet. Die letzte "
                    "Hauptprüfung durch den TÜV Süd fand am 09.11.2023 statt "
                    "und verlief ohne Beanstandungen. Der bestehende "
                    "Wartungsvertrag läuft bis 31.12.2026 und beinhaltet "
                    "zwei Wartungstermine pro Jahr sowie eine "
                    "24-Stunden-Notrufbereitschaft.",
                ),
                (
                    "Sanierung der Fassade Nordseite",
                    "Ein Kostenvoranschlag über 42.000 EUR für die "
                    "Sanierung liegt vor. Beschluss: Einholung eines "
                    "zweiten Angebots, endgültige Entscheidung auf die "
                    "nächste Versammlung vertagt.",
                ),
                (
                    "Erhöhung der Instandhaltungsrücklage",
                    "Beschluss: Die monatliche Instandhaltungsrücklage "
                    "wird ab 01.07.2024 von 45 EUR auf 55 EUR pro "
                    "Miteigentumsanteil erhöht, mit 8 Ja-Stimmen, "
                    "1 Gegenstimme, 0 Enthaltungen.",
                ),
            ],
        },
        "teilungserklaerung": {
            "notar": "Notar Dr. Andreas Hoffmann, München",
            "urkundenrolle": "UR-Nr. 884/1998 H",
            "datum": "12.06.1998",
            "einheiten_hinweis": (
                "Das Gebäude ist gemäß Aufteilungsplan in 12 "
                "Wohnungseigentumseinheiten und 12 zugehörige "
                "Tiefgaragen-Sondereigentumseinheiten aufgeteilt."
            ),
            "miteigentumsanteil": "78/1000",
            "sondereigentum": (
                "Die Wohnung im 3. Obergeschoss (Einheit Nr. 7) nebst "
                "Kellerabteil Nr. 7 und Tiefgaragenstellplatz Nr. 7."
            ),
            "gemeinschaftseigentum": (
                "Zum Gemeinschaftseigentum gehören insbesondere das "
                "Treppenhaus, der Fahrstuhl, das Dach, die Fassade sowie "
                "alle tragenden Bauteile und die zentrale Heizungsanlage."
            ),
            "kostenverteilung": (
                "Die Kosten der Verwaltung und Instandhaltung des "
                "gemeinschaftlichen Eigentums werden nach dem Verhältnis "
                "der Miteigentumsanteile umgelegt, soweit nicht "
                "verbrauchsabhängige Kosten (Heizung, Wasser) nach "
                "erfasstem Verbrauch abgerechnet werden."
            ),
            "sondernutzungsrechte": (
                "Der Eigentümer der Einheit Nr. 7 hat kein gesondertes "
                "Sondernutzungsrecht; die Gartenfläche steht allen "
                "Eigentümern zur gemeinschaftlichen Nutzung offen."
            ),
            "stimmrecht": (
                "Das Stimmrecht in der Eigentümerversammlung richtet sich "
                "nach dem Kopfprinzip: Jede Einheit hat unabhängig von "
                "ihrem Miteigentumsanteil eine Stimme."
            ),
            "bauliche_veraenderungen": (
                "Bauliche Veränderungen am Gemeinschaftseigentum sowie "
                "Maßnahmen, die über die ordnungsgemäße Instandhaltung "
                "hinausgehen, bedürfen gemäß § 20 WEG eines Beschlusses "
                "der Eigentümerversammlung. Veränderungen, die andere "
                "Wohnungseigentümer über das bei einem geordneten "
                "Zusammenleben unvermeidliche Maß hinaus beeinträchtigen, "
                "bedürfen zusätzlich der Zustimmung der betroffenen "
                "Eigentümer. Dies betrifft insbesondere Eingriffe in "
                "tragende Wände, Veränderungen der Fassade (einschließlich "
                "Balkonverglasungen und Markisen), sowie Maßnahmen an "
                "Fenstern und Rollläden, soweit deren äußeres "
                "Erscheinungsbild betroffen ist. Anträge auf bauliche "
                "Veränderungen sind der Verwaltung schriftlich mit "
                "Bauplänen und Kostenschätzung vorzulegen."
            ),
            "instandhaltung": (
                "Jeder Eigentümer ist verpflichtet, sein Sondereigentum "
                "so instand zu halten, dass anderen Eigentümern kein "
                "Nachteil entsteht. Die Instandhaltung und "
                "Instandsetzung des Gemeinschaftseigentums obliegt der "
                "Gemeinschaft der Wohnungseigentümer und wird aus der "
                "Instandhaltungsrücklage finanziert, deren Höhe die "
                "Eigentümerversammlung durch Beschluss festlegt. Kommt "
                "ein Eigentümer seiner Instandhaltungspflicht am "
                "Sondereigentum nicht nach und entsteht dadurch ein "
                "Schaden am Gemeinschaftseigentum oder an anderem "
                "Sondereigentum, haftet er hierfür nach den allgemeinen "
                "gesetzlichen Vorschriften."
            ),
            "verwalter": (
                "Die Wohnungseigentümergemeinschaft wird durch einen von "
                "der Eigentümerversammlung bestellten Verwalter "
                "vertreten (zum Zeitpunkt der Beurkundung: Hausverwaltung "
                "Brunner & Partner). Der Verwalter ist insbesondere "
                "zuständig für die Aufstellung des Wirtschaftsplans, die "
                "Erstellung der Jahresabrechnung, die Einberufung und "
                "Durchführung der Eigentümerversammlungen sowie die "
                "Umsetzung der gefassten Beschlüsse. Die Bestellung "
                "erfolgt jeweils für einen Zeitraum von bis zu fünf "
                "Jahren und kann durch die Eigentümerversammlung mit "
                "einfacher Mehrheit erneuert oder aus wichtigem Grund "
                "vorzeitig widerrufen werden."
            ),
            "tierhaltung": (
                "Die Haltung von Haustieren im Rahmen des üblichen "
                "Umfangs (insbesondere Katzen, Kleintiere sowie ein Hund "
                "je Wohneinheit) ist zulässig, sofern hierdurch keine "
                "Beeinträchtigung anderer Eigentümer oder Bewohner "
                "entsteht. Die Haltung gefährlicher oder besonders "
                "lärmintensiver Tiere sowie eine gewerbsmäßige "
                "Tierhaltung bedarf der vorherigen Zustimmung der "
                "Verwaltung."
            ),
            "schlussbestimmungen": (
                "Sollte eine Bestimmung dieser Teilungserklärung "
                "unwirksam sein oder werden, bleibt die Wirksamkeit der "
                "übrigen Bestimmungen hiervon unberührt; an die Stelle "
                "der unwirksamen Bestimmung tritt eine dem wirtschaftlich "
                "Gewollten möglichst nahekommende Regelung. Änderungen "
                "dieser Teilungserklärung bedürfen der notariellen Form "
                "sowie grundsätzlich der Zustimmung aller betroffenen "
                "Wohnungseigentümer, soweit gesetzlich nichts anderes "
                "bestimmt ist. Die Kosten dieser Urkunde sowie ihres "
                "Vollzugs trägt der jeweilige Ersterwerber der "
                "betreffenden Einheit."
            ),
        },
    },
    # ------------------------------------------------------------------
    # Objekt 2: Gartenhof (bestehend)
    # Testfälle: kein Fahrstuhl (Negativ-Fakt); keine Rücklagenerhöhung
    # im Protokoll (Cross-Objekt-Verwechslungstest gegen Sonnenblick).
    # ------------------------------------------------------------------
    {
        "id": "objekt2",
        "name": "Gartenhof",
        "adresse": "Lindenweg 7, 50667 Köln (Altstadt-Nord)",
        "expose": {
            "beschreibung": (
                "Gepflegte 2-Zimmer-Erdgeschosswohnung mit direktem Zugang "
                "zu einer eigenen Terrasse und Mitbenutzung des "
                "gemeinschaftlichen Gartens. Das Gebäude wurde 1998 "
                "errichtet und befindet sich in einem sehr guten "
                "Erhaltungszustand."
            ),
            "wohnflaeche": "54 m²",
            "zimmer": "2",
            "baujahr": "1998",
            "etage": "Erdgeschoss",
            "kaufpreis": "229.000 EUR",
            "hausgeld": "195 EUR",
            "stellplatz": "1 Außenstellplatz",
            "bezugsfrei": "01.10.2024",
            "ausstattung": [
                "Fliesenboden im Eingangsbereich, Laminat in Wohn- und Schlafzimmer",
                "Modernisiertes Bad mit Dusche (2021)",
                "Terrasse (ca. 12 m²) mit Gartenanteil",
                "Kellerabteil vorhanden",
                "Kein Fahrstuhl (nicht erforderlich, da Erdgeschoss)",
            ],
            "lage": (
                "Ruhige, grüne Wohnlage im Kölner Norden, nahe des "
                "Nordparks. Straßenbahnhaltestelle ca. 300 m entfernt."
            ),
            "kontakt_name": "Herr T. Neumann",
            "kontakt_tel": "0221 / 555-0198",
            "kontakt_email": "neumann@musterwert-immobilien-beispiel.de",
        },
        "energieausweis": {
            "art": "Verbrauchsausweis",
            "gebaeudetyp": "Mehrfamilienhaus, Wohnungseigentum",
            "baujahr_gebaeude": "1998",
            "baujahr_waermeerzeuger": "2010 (Gas-Brennwertkessel, zentral)",
            "wohnflaeche": "54 m²",
            "einheiten": "8",
            "endenergie": "89 kWh/(m²·a)",
            "primaerenergie": None,
            "klasse": "C",
            "heizung": "Erdgas (zentral)",
            "warmwasser": "zentral über Heizungsanlage",
            "empfehlungen": [],
            "ausstellungsdatum": "02.02.2024",
            "gueltig_bis": "01.02.2034",
            "registriernummer": "DE-2024-9932-EAB",
        },
        "protokoll": {
            "datum": "14.05.2024",
            "beginn": "19:00 Uhr",
            "ende": "20:30 Uhr",
            "ort": "Praxisräume Hausverwaltung Klein, Ottostraße 3, Köln",
            "versammlungsleiter": "Frau M. Klein (Hausverwaltung Klein)",
            "protokollfuehrer": "Herr D. Sander",
            "anwesenheit": "6 von 8 Miteigentumsanteilen (82 %)",
            "tops": [
                (
                    "Genehmigung der Jahresabrechnung 2023",
                    "Beschluss: Die Jahresabrechnung 2023 wird einstimmig "
                    "genehmigt (6 Ja-Stimmen).",
                ),
                (
                    "Pflege der Gartenanlage",
                    "Der Gärtnereibetrieb Grünwald übernimmt weiterhin die "
                    "Pflege der Gemeinschaftsgartenflächen. Die Kosten "
                    "bleiben unverändert bei 1.800 EUR pro Jahr.",
                ),
                (
                    "Erneuerung der Kellertüren",
                    "Beschluss: Die Kellertüren im Gemeinschaftsbereich "
                    "werden erneuert. Kostenrahmen bis 6.500 EUR genehmigt, "
                    "6 Ja-Stimmen, 0 Gegenstimmen, 0 Enthaltungen.",
                ),
                (
                    "Sonstiges",
                    "Ein Eigentümer weist auf eine defekte Außenleuchte am "
                    "Zugang zur Terrasse hin. Die Verwaltung sagt eine "
                    "kurzfristige Reparatur zu.",
                ),
            ],
        },
        "teilungserklaerung": {
            "notar": "Notarin Dr. Petra Wagner, Köln",
            "urkundenrolle": "UR-Nr. 221/1997 W",
            "datum": "03.09.1997",
            "einheiten_hinweis": (
                "Das Gebäude ist in 8 Wohnungseigentumseinheiten und "
                "8 Außenstellplätze aufgeteilt."
            ),
            "miteigentumsanteil": "54/620",
            "sondereigentum": (
                "Die Erdgeschosswohnung (Einheit Nr. 1) nebst Terrasse, "
                "Kellerabteil Nr. 1 und Außenstellplatz Nr. 1."
            ),
            "gemeinschaftseigentum": (
                "Zum Gemeinschaftseigentum gehören das Treppenhaus, das "
                "Dach, die Fassade, die Gartenanlage sowie die zentrale "
                "Heizungsanlage."
            ),
            "kostenverteilung": (
                "Verwaltungs- und Instandhaltungskosten werden nach dem "
                "Verhältnis der Miteigentumsanteile umgelegt."
            ),
            "sondernutzungsrechte": (
                "Der Eigentümer der Einheit Nr. 1 hat ein Sondernutzungsrecht "
                "an der unmittelbar angrenzenden Terrassenfläche von ca. "
                "12 m², wie im Aufteilungsplan gelb markiert."
            ),
            "stimmrecht": (
                "Das Stimmrecht richtet sich nach dem Verhältnis der "
                "Miteigentumsanteile (Wertprinzip)."
            ),
            "bauliche_veraenderungen": (
                "Bauliche Veränderungen am Gemeinschaftseigentum bedürfen "
                "gemäß § 20 WEG eines Beschlusses der "
                "Eigentümerversammlung. Veränderungen, die andere "
                "Wohnungseigentümer über das bei einem geordneten "
                "Zusammenleben unvermeidliche Maß hinaus beeinträchtigen, "
                "bedürfen zusätzlich der Zustimmung der betroffenen "
                "Eigentümer. Dies gilt insbesondere für bauliche "
                "Veränderungen an der zum Sondernutzungsrecht gehörenden "
                "Terrassenfläche, soweit diese von außen sichtbar sind "
                "(z. B. Sichtschutzwände, feste Überdachungen), sowie für "
                "Eingriffe in die Fassade oder tragende Bauteile."
            ),
            "instandhaltung": (
                "Jeder Eigentümer ist verpflichtet, sein Sondereigentum "
                "einschließlich der ihm zugewiesenen Sondernutzungsfläche "
                "so instand zu halten, dass anderen Eigentümern kein "
                "Nachteil entsteht. Die Instandhaltung und "
                "Instandsetzung des Gemeinschaftseigentums obliegt "
                "gemeinschaftlich allen Wohnungseigentümern. Die Pflege der "
                "gemeinschaftlichen Gartenanlage (außerhalb der "
                "Sondernutzungsflächen) wird durch die Gemeinschaft "
                "organisiert und aus den laufenden Hausgeldern finanziert."
            ),
            "verwalter": (
                "Die Wohnungseigentümergemeinschaft wird durch einen von "
                "der Eigentümerversammlung bestellten Verwalter "
                "vertreten (zum Zeitpunkt der Beurkundung: Hausverwaltung "
                "Klein). Der Verwalter ist insbesondere zuständig für "
                "die Aufstellung des Wirtschaftsplans, die Erstellung "
                "der Jahresabrechnung, die Einberufung und Durchführung "
                "der Eigentümerversammlungen sowie die Umsetzung der "
                "gefassten Beschlüsse. Die Bestellung erfolgt jeweils "
                "für einen Zeitraum von bis zu fünf Jahren."
            ),
            "tierhaltung": (
                "Die Haltung von Haustieren im üblichen Umfang "
                "(insbesondere Katzen, Kleintiere sowie ein Hund je "
                "Wohneinheit) ist zulässig, sofern hierdurch keine "
                "Beeinträchtigung anderer Eigentümer oder Bewohner "
                "entsteht. Insbesondere im Bereich der gemeinschaftlichen "
                "Gartenanlage ist auf die Beseitigung von "
                "Tierhinterlassenschaften zu achten. Die Haltung "
                "gefährlicher Tiere bedarf der vorherigen Zustimmung der "
                "Verwaltung."
            ),
            "schlussbestimmungen": (
                "Sollte eine Bestimmung dieser Teilungserklärung "
                "unwirksam sein oder werden, bleibt die Wirksamkeit der "
                "übrigen Bestimmungen hiervon unberührt. Änderungen "
                "dieser Teilungserklärung bedürfen der notariellen Form "
                "sowie grundsätzlich der Zustimmung aller betroffenen "
                "Wohnungseigentümer, soweit gesetzlich nichts anderes "
                "bestimmt ist. Die Kosten dieser Urkunde sowie ihres "
                "Vollzugs trägt der jeweilige Ersterwerber der "
                "betreffenden Einheit."
            ),
        },
    },
    # ------------------------------------------------------------------
    # Objekt 3: Ahornhöhe (bestehend)
    # Testfall: keine Sauna irgendwo (Halluzinationstest).
    # ------------------------------------------------------------------
    {
        "id": "objekt3",
        "name": "Ahornhöhe",
        "adresse": "Ahornweg 21, 22303 Hamburg (Winterhude)",
        "expose": {
            "beschreibung": (
                "Exklusives Penthouse im Dachgeschoss eines 2016 "
                "fertiggestellten Neubaus mit großzügiger Dachterrasse und "
                "Blick über die Dächer Winterhudes. Die Wohnung wurde "
                "durchgehend hochwertig ausgestattet und ist bezugsfertig."
            ),
            "wohnflaeche": "112 m²",
            "zimmer": "4",
            "baujahr": "2016",
            "etage": "5. OG (Penthouse) von 5",
            "kaufpreis": "875.000 EUR",
            "hausgeld": "410 EUR",
            "stellplatz": "1 Tiefgaragenstellplatz + 1 Fahrradstellplatz",
            "bezugsfrei": "nach Vereinbarung",
            "ausstattung": [
                "Fußbodenheizung in allen Räumen",
                "Bodentiefe Fenster, hochwertige Dreifachverglasung",
                "Zwei Bäder (Wanne + Dusche im Hauptbad, Dusche im Gäste-WC)",
                "Dachterrasse (ca. 45 m²) mit Süd-Ausrichtung",
                "Einbauküche (2016, Marke Siematic)",
                "Fahrstuhl im Haus vorhanden, direkter Zugang zur Wohnung",
            ],
            "lage": (
                "Beliebte Wohnlage in Winterhude, nahe Stadtpark und "
                "Alster. Sehr gute Anbindung an den ÖPNV."
            ),
            "kontakt_name": "Frau J. Petersen",
            "kontakt_tel": "040 / 555-0176",
            "kontakt_email": "petersen@musterwert-immobilien-beispiel.de",
        },
        "energieausweis": {
            "art": "Bedarfsausweis",
            "gebaeudetyp": "Mehrfamilienhaus, Wohnungseigentum (Neubau)",
            "baujahr_gebaeude": "2016",
            "baujahr_waermeerzeuger": "2016 (Luft-Wasser-Wärmepumpe, zentral)",
            "wohnflaeche": "112 m²",
            "einheiten": "14",
            "endenergie": "42 kWh/(m²·a)",
            "primaerenergie": "38 kWh/(m²·a)",
            "klasse": "A",
            "heizung": "Strom (Wärmepumpe, zentral)",
            "warmwasser": "zentral über Wärmepumpe, unterstützt durch Solarthermie",
            "empfehlungen": [],
            "ausstellungsdatum": "20.01.2024",
            "gueltig_bis": "19.01.2034",
            "registriernummer": "DE-2024-9933-EAB",
        },
        "protokoll": {
            "datum": "06.06.2024",
            "beginn": "18:00 Uhr",
            "ende": "19:45 Uhr",
            "ort": "Gemeinschaftsraum, Ahornweg 21",
            "versammlungsleiter": "Herr F. Wagner (Wagner Immobilienverwaltung)",
            "protokollfuehrer": "Frau A. Berg",
            "anwesenheit": "11 von 14 Miteigentumsanteilen (79 %)",
            "tops": [
                (
                    "Genehmigung der Jahresabrechnung 2023",
                    "Beschluss: Genehmigt mit 10 Ja-Stimmen, 0 "
                    "Gegenstimmen, 1 Enthaltung.",
                ),
                (
                    "Wartung der Wärmepumpenanlage",
                    "Die zentrale Luft-Wasser-Wärmepumpe wird jährlich "
                    "durch die Firma Klimatechnik Nord gewartet. Die "
                    "letzte Wartung erfolgte im März 2024 und verlief ohne "
                    "Beanstandungen.",
                ),
                (
                    "Reinigung und Pflege der Dachterrassen",
                    "Beschluss: Die Verwaltung beauftragt einmal jährlich "
                    "im Herbst eine fachgerechte Reinigung der "
                    "Dachrinnen durch eine externe Firma. Zustimmung mit "
                    "11 Ja-Stimmen.",
                ),
                (
                    "Fahrradstellplätze in der Tiefgarage",
                    "Beschluss: Zwei zusätzliche Fahrradstellplätze werden "
                    "eingerichtet. Kostenrahmen bis 1.200 EUR genehmigt, "
                    "9 Ja-Stimmen, 2 Gegenstimmen.",
                ),
            ],
        },
        "teilungserklaerung": {
            "notar": "Notar Dr. Christian Lorenz, Hamburg",
            "urkundenrolle": "UR-Nr. 45/2015 L",
            "datum": "18.11.2015",
            "einheiten_hinweis": (
                "Das Gebäude ist in 14 Wohnungseigentumseinheiten "
                "aufgeteilt, davon eine Penthouse-Einheit im 5. OG."
            ),
            "miteigentumsanteil": "112/1350",
            "sondereigentum": (
                "Die Penthouse-Wohnung im 5. OG (Einheit Nr. 14) nebst "
                "Dachterrasse, Kellerabteil Nr. 14, Tiefgaragenstellplatz "
                "Nr. 14 und Fahrradabstellplatz Nr. 3."
            ),
            "gemeinschaftseigentum": (
                "Zum Gemeinschaftseigentum gehören Treppenhaus, Fahrstuhl, "
                "Dach, Fassade, Tiefgarage und die zentrale "
                "Wärmepumpenanlage."
            ),
            "kostenverteilung": (
                "Die Kosten werden nach dem Verhältnis der "
                "Miteigentumsanteile verteilt, mit Ausnahme der "
                "Aufzugskosten, die nach Etagenlage gestaffelt umgelegt "
                "werden (höhere Etagen tragen einen höheren Anteil)."
            ),
            "sondernutzungsrechte": (
                "Der Eigentümer der Einheit Nr. 14 hat das ausschließliche "
                "Sondernutzungsrecht an der Dachterrasse von ca. 45 m²."
            ),
            "stimmrecht": (
                "Das Stimmrecht richtet sich nach dem Verhältnis der "
                "Miteigentumsanteile (Wertprinzip)."
            ),
            "bauliche_veraenderungen": (
                "Bauliche Veränderungen am Gemeinschaftseigentum bedürfen "
                "gemäß § 20 WEG eines Beschlusses der "
                "Eigentümerversammlung. Für die Dachterrasse der Einheit "
                "Nr. 14 gilt: Feste Aufbauten (z. B. Pergolen, "
                "Wintergärten) sowie Veränderungen, die die Statik oder "
                "die Dachabdichtung berühren, bedürfen zusätzlich der "
                "gesonderten Zustimmung der Eigentümerversammlung und "
                "eines Nachweises der statischen Unbedenklichkeit durch "
                "einen Fachplaner. Veränderungen an der Fassade, den "
                "Fenstern oder der Gebäudetechnik (insbesondere der "
                "Wärmepumpenanlage) bedürfen ebenfalls eines Beschlusses."
            ),
            "instandhaltung": (
                "Jeder Eigentümer ist verpflichtet, sein Sondereigentum "
                "so instand zu halten, dass anderen Eigentümern kein "
                "Nachteil entsteht. Die Instandhaltung und "
                "Instandsetzung des Gemeinschaftseigentums, insbesondere "
                "der zentralen Wärmepumpenanlage und des Fahrstuhls, "
                "obliegt gemeinschaftlich allen Wohnungseigentümern. Für die "
                "Dachabdichtung im Bereich der Sondernutzungsfläche "
                "Dachterrasse trägt die Gemeinschaft die Kosten der "
                "Instandhaltung, während die Reinigung der Terrasse "
                "selbst dem nutzungsberechtigten Eigentümer obliegt."
            ),
            "verwalter": (
                "Die Wohnungseigentümergemeinschaft wird durch einen von "
                "der Eigentümerversammlung bestellten Verwalter "
                "vertreten (zum Zeitpunkt der Beurkundung: Wagner "
                "Immobilienverwaltung). Der Verwalter ist insbesondere "
                "zuständig für die Aufstellung des Wirtschaftsplans, die "
                "Erstellung der Jahresabrechnung, die Einberufung und "
                "Durchführung der Eigentümerversammlungen sowie die "
                "Umsetzung der gefassten Beschlüsse."
            ),
            "tierhaltung": (
                "Die Haltung von Haustieren im üblichen Umfang ist "
                "zulässig, sofern hierdurch keine Beeinträchtigung "
                "anderer Eigentümer oder Bewohner entsteht. Das "
                "Ausführen von Hunden über die Dachterrasse anderer "
                "Einheiten ist ausgeschlossen. Die Haltung gefährlicher "
                "oder besonders lärmintensiver Tiere bedarf der "
                "vorherigen Zustimmung der Verwaltung."
            ),
            "schlussbestimmungen": (
                "Sollte eine Bestimmung dieser Teilungserklärung "
                "unwirksam sein oder werden, bleibt die Wirksamkeit der "
                "übrigen Bestimmungen hiervon unberührt. Änderungen "
                "dieser Teilungserklärung bedürfen der notariellen Form "
                "sowie grundsätzlich der Zustimmung aller betroffenen "
                "Wohnungseigentümer. Die Kosten dieser Urkunde sowie "
                "ihres Vollzugs trägt der jeweilige Ersterwerber der "
                "betreffenden Einheit."
            ),
        },
    },
    # ------------------------------------------------------------------
    # Objekt 4: Lindenpark (NEU)
    # Testfall: Sondernutzungsrecht am Garten steht NUR in der
    # Teilungserklärung, sonst nirgendwo erwähnt.
    # ------------------------------------------------------------------
    {
        "id": "objekt4",
        "name": "Lindenpark",
        "adresse": "Lindenparkweg 4, 10405 Berlin (Prenzlauer Berg)",
        "expose": {
            "beschreibung": (
                "Charmante 3-Zimmer-Wohnung im Hochparterre eines "
                "sanierten Gründerzeitbaus von 1905. Stuckdecken, "
                "Dielenboden und ein Erker prägen den Charakter dieser "
                "Wohnung im beliebten Prenzlauer Berg."
            ),
            "wohnflaeche": "89 m²",
            "zimmer": "3",
            "baujahr": "1905 (Sanierung 2016)",
            "etage": "Hochparterre",
            "kaufpreis": "620.000 EUR",
            "hausgeld": "310 EUR",
            "stellplatz": "kein Stellplatz vorhanden",
            "bezugsfrei": "01.01.2025",
            "ausstattung": [
                "Stuckdecken im Wohnzimmer und Erker",
                "Dielenboden aus Eiche, original erhalten und aufgearbeitet",
                "Modernes Bad mit Wanne (2016)",
                "Einbauküche (2020, Marke Bulthaup)",
                "Kellerabteil vorhanden",
                "Kein Fahrstuhl (Hochparterre gut zu Fuß erreichbar)",
            ],
            "lage": (
                "Ruhige Straße nahe des Helmholtzplatzes, viele Cafés und "
                "Geschäfte in unmittelbarer Nähe. Tramhaltestelle 3 "
                "Gehminuten entfernt."
            ),
            "kontakt_name": "Herr M. Krause",
            "kontakt_tel": "030 / 555-0223",
            "kontakt_email": "krause@musterwert-immobilien-beispiel.de",
        },
        "energieausweis": {
            "art": "Verbrauchsausweis",
            "gebaeudetyp": "Mehrfamilienhaus, Wohnungseigentum",
            "baujahr_gebaeude": "1905",
            "baujahr_waermeerzeuger": "2016 (Gas-Brennwertkessel, zentral)",
            "wohnflaeche": "89 m²",
            "einheiten": "10",
            "endenergie": "76 kWh/(m²·a)",
            "primaerenergie": None,
            "klasse": "B",
            "heizung": "Erdgas (zentral)",
            "warmwasser": "zentral über Heizungsanlage",
            "empfehlungen": [],
            "ausstellungsdatum": "05.03.2024",
            "gueltig_bis": "04.03.2034",
            "registriernummer": "DE-2024-9934-EAB",
        },
        "protokoll": {
            "datum": "11.04.2024",
            "beginn": "19:00 Uhr",
            "ende": "20:50 Uhr",
            "ort": "Gemeinschaftsraum im Hinterhaus, Lindenparkweg 4",
            "versammlungsleiter": "Frau S. Baumann (Hausverwaltung Baumann)",
            "protokollfuehrer": "Herr J. Fischer",
            "anwesenheit": "7 von 10 Miteigentumsanteilen (71 %)",
            "tops": [
                (
                    "Genehmigung der Jahresabrechnung 2023",
                    "Beschluss: Genehmigt mit 7 Ja-Stimmen, 0 "
                    "Gegenstimmen, 0 Enthaltungen.",
                ),
                (
                    "Instandsetzung der Hofdurchfahrt",
                    "Die Pflasterung der Hofdurchfahrt weist Schäden auf. "
                    "Beschluss: Beauftragung einer Fachfirma, Kostenrahmen "
                    "bis 8.000 EUR, 6 Ja-Stimmen, 1 Gegenstimme.",
                ),
                (
                    "Fahrradabstellanlage im Hof",
                    "Beschluss: Errichtung einer überdachten "
                    "Fahrradabstellanlage im Hinterhof, Kosten ca. "
                    "3.200 EUR, einstimmig angenommen.",
                ),
                (
                    "Sonstiges",
                    "Eine Eigentümerin bittet um regelmäßigere Reinigung "
                    "des Treppenhauses. Die Verwaltung sagt zu, das "
                    "Reinigungsintervall mit der beauftragten Firma zu "
                    "besprechen.",
                ),
            ],
        },
        "teilungserklaerung": {
            "notar": "Notarin Dr. Ines Wolter, Berlin",
            "urkundenrolle": "UR-Nr. 512/2005 W",
            "datum": "07.02.2005",
            "einheiten_hinweis": (
                "Das Gebäude ist in 10 Wohnungseigentumseinheiten "
                "aufgeteilt."
            ),
            "miteigentumsanteil": "89/980",
            "sondereigentum": (
                "Die Wohnung im Hochparterre (Einheit Nr. 2) nebst "
                "Kellerabteil Nr. 2."
            ),
            "gemeinschaftseigentum": (
                "Zum Gemeinschaftseigentum gehören Treppenhaus, Dach, "
                "Fassade, Hofdurchfahrt und die gemeinschaftliche "
                "Gartenfläche im Hinterhof."
            ),
            "kostenverteilung": (
                "Die Kosten werden nach dem Verhältnis der "
                "Miteigentumsanteile umgelegt."
            ),
            "sondernutzungsrechte": (
                "Der Eigentümer der Einheit Nr. 2 (Hochparterre) erhält "
                "das ausschließliche Sondernutzungsrecht an der "
                "Gartenfläche im Hinterhof gemäß dem als Anlage "
                "beigefügten Aufteilungsplan (dort gelb markiert). Alle "
                "übrigen Einheiten haben kein Nutzungsrecht an dieser "
                "Fläche."
            ),
            "stimmrecht": (
                "Das Stimmrecht richtet sich nach dem Verhältnis der "
                "Miteigentumsanteile (Wertprinzip)."
            ),
            "bauliche_veraenderungen": (
                "Bauliche Veränderungen am Gemeinschaftseigentum bedürfen "
                "gemäß § 20 WEG eines Beschlusses der "
                "Eigentümerversammlung. Da es sich um ein Gebäude mit "
                "denkmalrechtlich relevanter Gründerzeitfassade handelt, "
                "bedürfen Veränderungen an der Fassade, den Fenstern und "
                "dem Stuck zusätzlich der Abstimmung mit der zuständigen "
                "Denkmalschutzbehörde. Für die Sondernutzungsfläche im "
                "Garten gilt: Feste bauliche Anlagen (Gartenhäuser, "
                "Terrassenüberdachungen) bedürfen der Zustimmung der "
                "Eigentümerversammlung."
            ),
            "instandhaltung": (
                "Jeder Eigentümer ist verpflichtet, sein Sondereigentum "
                "so instand zu halten, dass anderen Eigentümern kein "
                "Nachteil entsteht. Die Instandhaltung und "
                "Instandsetzung des Gemeinschaftseigentums, insbesondere "
                "der historischen Fassade und des Dachs, obliegt "
                "gemeinschaftlich allen Wohnungseigentümern. Die Pflege der dem "
                "Sondernutzungsrecht unterliegenden Gartenfläche obliegt "
                "dem nutzungsberechtigten Eigentümer der Einheit Nr. 2."
            ),
            "verwalter": (
                "Die Wohnungseigentümergemeinschaft wird durch einen von "
                "der Eigentümerversammlung bestellten Verwalter "
                "vertreten (zum Zeitpunkt der Beurkundung: Hausverwaltung "
                "Baumann). Der Verwalter ist insbesondere zuständig für "
                "die Aufstellung des Wirtschaftsplans, die Erstellung "
                "der Jahresabrechnung, die Einberufung und Durchführung "
                "der Eigentümerversammlungen sowie die Umsetzung der "
                "gefassten Beschlüsse."
            ),
            "tierhaltung": (
                "Die Haltung von Haustieren im üblichen Umfang ist "
                "zulässig, sofern hierdurch keine Beeinträchtigung "
                "anderer Eigentümer oder Bewohner entsteht. Für die "
                "Sondernutzungsfläche im Garten gilt, dass eine "
                "gewerbsmäßige Tierhaltung sowie die Haltung von mehr "
                "als zwei Hunden je Einheit der vorherigen Zustimmung "
                "der Verwaltung bedarf."
            ),
            "schlussbestimmungen": (
                "Sollte eine Bestimmung dieser Teilungserklärung "
                "unwirksam sein oder werden, bleibt die Wirksamkeit der "
                "übrigen Bestimmungen hiervon unberührt. Änderungen "
                "dieser Teilungserklärung bedürfen der notariellen Form "
                "sowie grundsätzlich der Zustimmung aller betroffenen "
                "Wohnungseigentümer. Die Kosten dieser Urkunde sowie "
                "ihres Vollzugs trägt der jeweilige Ersterwerber der "
                "betreffenden Einheit."
            ),
        },
    },
    # ------------------------------------------------------------------
    # Objekt 5: Seeblick (NEU)
    # Wird zum Objekt mit der besten Energieeffizienzklasse (A+) —
    # relevant für die Vergleichsfrage über alle Objekte.
    # ------------------------------------------------------------------
    {
        "id": "objekt5",
        "name": "Seeblick",
        "adresse": "Uferpromenade 3, 78464 Konstanz (Bodensee)",
        "expose": {
            "beschreibung": (
                "Hochwertige 4-Zimmer-Neubauwohnung mit direktem Seeblick "
                "auf den Bodensee. Das 2023 fertiggestellte Gebäude "
                "entspricht dem KfW-Effizienzhaus-40-Standard und bietet "
                "großzügige Terrassenflächen."
            ),
            "wohnflaeche": "128 m²",
            "zimmer": "4",
            "baujahr": "2023",
            "etage": "2. OG von 4",
            "kaufpreis": "1.150.000 EUR",
            "hausgeld": "480 EUR",
            "stellplatz": "1 Tiefgaragenstellplatz mit E-Ladepunkt",
            "bezugsfrei": "sofort",
            "ausstattung": [
                "Fußbodenheizung mit Einzelraumregelung",
                "Bodentiefe Fenster mit Seeblick, Dreifachverglasung",
                "Zwei Bäder, hochwertig gefliest",
                "Terrasse (ca. 30 m²) mit Seeblick",
                "Einbauküche (2023, Marke Poggenpohl)",
                "Fahrstuhl im Haus vorhanden",
            ],
            "lage": (
                "Direkte Uferlage am Bodensee, fußläufig zur Konstanzer "
                "Altstadt (ca. 15 Minuten). Bushaltestelle 2 Gehminuten "
                "entfernt."
            ),
            "kontakt_name": "Frau C. Herrmann",
            "kontakt_tel": "07531 / 555-0311",
            "kontakt_email": "herrmann@musterwert-immobilien-beispiel.de",
        },
        "energieausweis": {
            "art": "Bedarfsausweis",
            "gebaeudetyp": "Mehrfamilienhaus, Wohnungseigentum (Neubau)",
            "baujahr_gebaeude": "2023",
            "baujahr_waermeerzeuger": "2023 (Erdwärmepumpe mit Photovoltaik-Unterstützung)",
            "wohnflaeche": "128 m²",
            "einheiten": "8",
            "endenergie": "24 kWh/(m²·a)",
            "primaerenergie": "19 kWh/(m²·a)",
            "klasse": "A+",
            "heizung": "Strom (Erdwärmepumpe, zentral, PV-unterstützt)",
            "warmwasser": "zentral über Wärmepumpe und Photovoltaikanlage",
            "empfehlungen": [],
            "ausstellungsdatum": "10.09.2023",
            "gueltig_bis": "09.09.2033",
            "registriernummer": "DE-2023-9935-EAB",
        },
        "protokoll": {
            "datum": "25.05.2024",
            "beginn": "18:30 Uhr",
            "ende": "19:50 Uhr",
            "ort": "Gemeinschaftsraum, Uferpromenade 3",
            "versammlungsleiter": "Herr P. Zimmermann (Zimmermann Hausverwaltung)",
            "protokollfuehrer": "Frau K. Roth",
            "anwesenheit": "7 von 8 Miteigentumsanteilen (88 %)",
            "tops": [
                (
                    "Genehmigung der Jahresabrechnung 2023",
                    "Da das Gebäude erst 2023 fertiggestellt wurde, "
                    "handelt es sich um die erste Jahresabrechnung. "
                    "Beschluss: Genehmigt mit 7 Ja-Stimmen.",
                ),
                (
                    "Wartung der Erdwärmepumpe und Photovoltaikanlage",
                    "Die Erdwärmepumpe und die Photovoltaikanlage auf dem "
                    "Dach werden im Rahmen der Herstellergarantie durch "
                    "die Firma Solartechnik Bodensee gewartet. Erste "
                    "Wartung planmäßig im Herbst 2024.",
                ),
                (
                    "Gestaltung der Außenanlagen",
                    "Beschluss: Ein Landschaftsgärtner wird mit der "
                    "Gestaltung der Uferpromenaden-nahen Grünflächen "
                    "beauftragt, Kostenrahmen bis 15.000 EUR, einstimmig "
                    "angenommen.",
                ),
                (
                    "Sonstiges",
                    "Keine weiteren Wortmeldungen.",
                ),
            ],
        },
        "teilungserklaerung": {
            "notar": "Notar Dr. Bernhard Kuhn, Konstanz",
            "urkundenrolle": "UR-Nr. 88/2022 K",
            "datum": "14.03.2022",
            "einheiten_hinweis": (
                "Das Gebäude ist in 8 Wohnungseigentumseinheiten "
                "aufgeteilt."
            ),
            "miteigentumsanteil": "128/1020",
            "sondereigentum": (
                "Die Wohnung im 2. OG (Einheit Nr. 4) nebst Terrasse, "
                "Kellerabteil Nr. 4 und Tiefgaragenstellplatz Nr. 4."
            ),
            "gemeinschaftseigentum": (
                "Zum Gemeinschaftseigentum gehören Treppenhaus, Fahrstuhl, "
                "Dach mit Photovoltaikanlage, Fassade und die zentrale "
                "Erdwärmepumpenanlage."
            ),
            "kostenverteilung": (
                "Die Kosten werden nach dem Verhältnis der "
                "Miteigentumsanteile umgelegt; die durch die "
                "Photovoltaikanlage erzeugten Erträge werden anteilig "
                "gutgeschrieben."
            ),
            "sondernutzungsrechte": (
                "Der Eigentümer der Einheit Nr. 4 hat ein "
                "Sondernutzungsrecht an der Terrassenfläche von ca. "
                "30 m²."
            ),
            "stimmrecht": (
                "Das Stimmrecht richtet sich nach dem Verhältnis der "
                "Miteigentumsanteile (Wertprinzip)."
            ),
            "bauliche_veraenderungen": (
                "Bauliche Veränderungen am Gemeinschaftseigentum bedürfen "
                "gemäß § 20 WEG eines Beschlusses der "
                "Eigentümerversammlung. Da das Gebäude dem "
                "KfW-Effizienzhaus-40-Standard entspricht, bedürfen "
                "Eingriffe in die Gebäudehülle (Fassade, Fenster, "
                "Dämmung) sowie an der Photovoltaikanlage und der "
                "Erdwärmepumpe zusätzlich der Zustimmung der "
                "Eigentümerversammlung und eines Nachweises, dass der "
                "energetische Standard des Gebäudes dadurch nicht "
                "beeinträchtigt wird."
            ),
            "instandhaltung": (
                "Jeder Eigentümer ist verpflichtet, sein Sondereigentum "
                "so instand zu halten, dass anderen Eigentümern kein "
                "Nachteil entsteht. Die Instandhaltung und "
                "Instandsetzung des Gemeinschaftseigentums, insbesondere "
                "der Erdwärmepumpenanlage und der Photovoltaikanlage, "
                "obliegt gemeinschaftlich allen Wohnungseigentümern. Die "
                "laufende Wartung dieser Anlagen erfolgt im Rahmen der "
                "Herstellergarantie durch eine von der Verwaltung "
                "beauftragte Fachfirma."
            ),
            "verwalter": (
                "Die Wohnungseigentümergemeinschaft wird durch einen von "
                "der Eigentümerversammlung bestellten Verwalter "
                "vertreten (zum Zeitpunkt der Beurkundung: Zimmermann "
                "Hausverwaltung). Der Verwalter ist insbesondere "
                "zuständig für die Aufstellung des Wirtschaftsplans, die "
                "Erstellung der Jahresabrechnung, die Einberufung und "
                "Durchführung der Eigentümerversammlungen sowie die "
                "Umsetzung der gefassten Beschlüsse."
            ),
            "tierhaltung": (
                "Die Haltung von Haustieren im üblichen Umfang ist "
                "zulässig, sofern hierdurch keine Beeinträchtigung "
                "anderer Eigentümer oder Bewohner entsteht. Auf der "
                "Uferpromenade und den gemeinschaftlichen Außenanlagen "
                "besteht Leinenpflicht für Hunde. Die Haltung "
                "gefährlicher Tiere bedarf der vorherigen Zustimmung der "
                "Verwaltung."
            ),
            "schlussbestimmungen": (
                "Sollte eine Bestimmung dieser Teilungserklärung "
                "unwirksam sein oder werden, bleibt die Wirksamkeit der "
                "übrigen Bestimmungen hiervon unberührt. Änderungen "
                "dieser Teilungserklärung bedürfen der notariellen Form "
                "sowie grundsätzlich der Zustimmung aller betroffenen "
                "Wohnungseigentümer. Die Kosten dieser Urkunde sowie "
                "ihres Vollzugs trägt der jeweilige Ersterwerber der "
                "betreffenden Einheit."
            ),
        },
    },
    # ------------------------------------------------------------------
    # Objekt 6: Kastanienhof (NEU)
    # Testfall: leichter Widerspruch beim Baujahr zwischen Exposé (1975)
    # und Energieausweis (1974).
    # ------------------------------------------------------------------
    {
        "id": "objekt6",
        "name": "Kastanienhof",
        "adresse": "Kastanienallee 58, 04277 Leipzig (Connewitz)",
        "expose": {
            "beschreibung": (
                "Sanierungsbedürftige 2-Zimmer-Wohnung in einem Gebäude "
                "aus dem Jahr 1975. Solide Bausubstanz, aber mit "
                "Modernisierungsbedarf bei Bad und Elektrik. Attraktiv "
                "für Kapitalanleger oder Selbstausbauer."
            ),
            "wohnflaeche": "61 m²",
            "zimmer": "2",
            "baujahr": "1975",
            "etage": "4. OG von 5",
            "kaufpreis": "138.000 EUR",
            "hausgeld": "165 EUR",
            "stellplatz": "kein Stellplatz vorhanden",
            "bezugsfrei": "nach Vereinbarung",
            "ausstattung": [
                "Original-Bad aus den 1970er Jahren, nicht modernisiert",
                "PVC-Boden im Wohnbereich",
                "Einfachverglasung teilweise noch original",
                "Kellerabteil vorhanden",
                "Kein Fahrstuhl im Haus",
            ],
            "lage": (
                "Lebendiges Wohnviertel Connewitz mit vielfältiger "
                "Gastronomie. Straßenbahnhaltestelle 4 Gehminuten "
                "entfernt."
            ),
            "kontakt_name": "Herr R. Vogel",
            "kontakt_tel": "0341 / 555-0287",
            "kontakt_email": "vogel@musterwert-immobilien-beispiel.de",
        },
        "energieausweis": {
            "art": "Verbrauchsausweis",
            "gebaeudetyp": "Mehrfamilienhaus, Wohnungseigentum",
            "baujahr_gebaeude": "1974",
            "baujahr_waermeerzeuger": "2005 (Gas-Brennwertkessel, zentral)",
            "wohnflaeche": "61 m²",
            "einheiten": "15",
            "endenergie": "198 kWh/(m²·a)",
            "primaerenergie": None,
            "klasse": "F",
            "heizung": "Erdgas (zentral)",
            "warmwasser": "zentral über Heizungsanlage",
            "empfehlungen": [
                "Austausch der Fenster (teilweise Einfachverglasung)",
                "Dämmung der Fassade",
                "Modernisierung der Heizungssteuerung",
            ],
            "ausstellungsdatum": "18.02.2024",
            "gueltig_bis": "17.02.2034",
            "registriernummer": "DE-2024-9936-EAB",
        },
        "protokoll": {
            "datum": "03.05.2024",
            "beginn": "18:00 Uhr",
            "ende": "20:05 Uhr",
            "ort": "Gemeinschaftsraum im Keller, Kastanienallee 58",
            "versammlungsleiter": "Herr W. Schulze (Hausverwaltung Schulze & Co.)",
            "protokollfuehrer": "Frau N. Braun",
            "anwesenheit": "10 von 15 Miteigentumsanteilen (67 %)",
            "tops": [
                (
                    "Genehmigung der Jahresabrechnung 2023",
                    "Beschluss: Genehmigt mit 9 Ja-Stimmen, 1 Enthaltung.",
                ),
                (
                    "Sanierungsstau — energetische Modernisierung",
                    "Die Verwaltung stellt ein Konzept zur energetischen "
                    "Sanierung (Fassadendämmung, Fensteraustausch) vor. "
                    "Geschätzte Gesamtkosten: 380.000 EUR. Beschluss: Ein "
                    "Sanierungsfahrplan wird bei einem Energieberater in "
                    "Auftrag gegeben, Kosten bis 4.500 EUR, 8 Ja-Stimmen, "
                    "2 Gegenstimmen.",
                ),
                (
                    "Erhöhung der Instandhaltungsrücklage",
                    "Angesichts des Sanierungsstaus beschließt die "
                    "Versammlung eine Erhöhung der monatlichen "
                    "Instandhaltungsrücklage von 30 EUR auf 50 EUR pro "
                    "Miteigentumsanteil ab 01.08.2024, mit 9 Ja-Stimmen, "
                    "1 Gegenstimme.",
                ),
                (
                    "Sonstiges",
                    "Ein Eigentümer bemängelt undichte Stellen am Dach. "
                    "Die Verwaltung sagt eine Begutachtung durch einen "
                    "Dachdecker zu.",
                ),
            ],
        },
        "teilungserklaerung": {
            "notar": "Notar Dr. Achim Richter, Leipzig",
            "urkundenrolle": "UR-Nr. 1102/1994 R",
            "datum": "21.04.1994",
            "einheiten_hinweis": (
                "Das Gebäude ist in 15 Wohnungseigentumseinheiten "
                "aufgeteilt."
            ),
            "miteigentumsanteil": "61/900",
            "sondereigentum": (
                "Die Wohnung im 4. Obergeschoss (Einheit Nr. 11) nebst "
                "Kellerabteil Nr. 11."
            ),
            "gemeinschaftseigentum": (
                "Zum Gemeinschaftseigentum gehören Treppenhaus, Dach, "
                "Fassade und die zentrale Heizungsanlage."
            ),
            "kostenverteilung": (
                "Die Kosten werden nach dem Verhältnis der "
                "Miteigentumsanteile umgelegt."
            ),
            "sondernutzungsrechte": "Es bestehen keine Sondernutzungsrechte.",
            "stimmrecht": (
                "Das Stimmrecht richtet sich nach dem Verhältnis der "
                "Miteigentumsanteile (Wertprinzip)."
            ),
            "bauliche_veraenderungen": (
                "Bauliche Veränderungen am Gemeinschaftseigentum bedürfen "
                "gemäß § 20 WEG eines Beschlusses der "
                "Eigentümerversammlung. Angesichts des bestehenden "
                "Sanierungsstaus (siehe Protokoll der Eigentümerversammlung "
                "vom 03.05.2024) wird ausdrücklich klargestellt, dass "
                "Maßnahmen im Rahmen des von der Eigentümerversammlung "
                "beauftragten Sanierungsfahrplans (insbesondere "
                "Fassadendämmung und Fensteraustausch) als ordnungsgemäße "
                "Instandsetzung gelten und keiner gesonderten Zustimmung "
                "einzelner Eigentümer bedürfen, sofern sie durch "
                "Mehrheitsbeschluss der Versammlung getragen werden."
            ),
            "instandhaltung": (
                "Jeder Eigentümer ist verpflichtet, sein Sondereigentum "
                "so instand zu halten, dass anderen Eigentümern kein "
                "Nachteil entsteht. Die Instandhaltung und "
                "Instandsetzung des Gemeinschaftseigentums obliegt der "
                "Gemeinschaft der Wohnungseigentümer und wird aus der "
                "Instandhaltungsrücklage finanziert. Angesichts des "
                "erhöhten Instandsetzungsbedarfs bei diesem Gebäude "
                "(Baujahr 1974) kann die Eigentümerversammlung "
                "Sonderumlagen beschließen, soweit die "
                "Instandhaltungsrücklage zur Deckung dringender "
                "Maßnahmen nicht ausreicht."
            ),
            "verwalter": (
                "Die Wohnungseigentümergemeinschaft wird durch einen von "
                "der Eigentümerversammlung bestellten Verwalter "
                "vertreten (zum Zeitpunkt der Beurkundung: Hausverwaltung "
                "Schulze & Co.). Der Verwalter ist insbesondere zuständig "
                "für die Aufstellung des Wirtschaftsplans, die "
                "Erstellung der Jahresabrechnung, die Einberufung und "
                "Durchführung der Eigentümerversammlungen sowie die "
                "Umsetzung der gefassten Beschlüsse, einschließlich der "
                "Koordination des laufenden Sanierungsfahrplans."
            ),
            "tierhaltung": (
                "Die Haltung von Haustieren im üblichen Umfang ist "
                "zulässig, sofern hierdurch keine Beeinträchtigung "
                "anderer Eigentümer oder Bewohner entsteht. Die Haltung "
                "gefährlicher oder besonders lärmintensiver Tiere bedarf "
                "der vorherigen Zustimmung der Verwaltung."
            ),
            "schlussbestimmungen": (
                "Sollte eine Bestimmung dieser Teilungserklärung "
                "unwirksam sein oder werden, bleibt die Wirksamkeit der "
                "übrigen Bestimmungen hiervon unberührt. Änderungen "
                "dieser Teilungserklärung bedürfen der notariellen Form "
                "sowie grundsätzlich der Zustimmung aller betroffenen "
                "Wohnungseigentümer. Die Kosten dieser Urkunde sowie "
                "ihres Vollzugs trägt der jeweilige Ersterwerber der "
                "betreffenden Einheit."
            ),
        },
    },
    # ------------------------------------------------------------------
    # Objekt 7: Rosenhügel (NEU)
    # Testfall: PV-Anlagen-Beschluss nur hier, nicht bei Birkenallee
    # (Cross-Objekt-Verwechslungstest zwischen zwei ähnlichen Neubauten).
    # ------------------------------------------------------------------
    {
        "id": "objekt7",
        "name": "Rosenhügel",
        "adresse": "Rosenhügelweg 9, 60437 Frankfurt am Main (Nieder-Eschbach)",
        "expose": {
            "beschreibung": (
                "Moderne 3-Zimmer-Neubauwohnung in einem 2021 errichteten "
                "Wohnkomplex. Klare Linienführung, offene Wohnküche und "
                "ein privater Balkon zeichnen diese Wohnung aus."
            ),
            "wohnflaeche": "82 m²",
            "zimmer": "3",
            "baujahr": "2021",
            "etage": "3. OG von 6",
            "kaufpreis": "510.000 EUR",
            "hausgeld": "295 EUR",
            "stellplatz": "1 Tiefgaragenstellplatz",
            "bezugsfrei": "sofort",
            "ausstattung": [
                "Fußbodenheizung",
                "Bodentiefe Fenster, Dreifachverglasung",
                "Modernes Bad mit bodengleicher Dusche",
                "Balkon (ca. 10 m², Süd-Ausrichtung)",
                "Einbauküche (2021)",
                "Fahrstuhl im Haus vorhanden",
            ],
            "lage": (
                "Ruhiges Neubaugebiet am Stadtrand, gute Anbindung an die "
                "A5. S-Bahn-Station 8 Gehminuten entfernt."
            ),
            "kontakt_name": "Herr D. Albrecht",
            "kontakt_tel": "069 / 555-0344",
            "kontakt_email": "albrecht@musterwert-immobilien-beispiel.de",
        },
        "energieausweis": {
            "art": "Bedarfsausweis",
            "gebaeudetyp": "Mehrfamilienhaus, Wohnungseigentum (Neubau)",
            "baujahr_gebaeude": "2021",
            "baujahr_waermeerzeuger": "2021 (Luft-Wasser-Wärmepumpe, zentral)",
            "wohnflaeche": "82 m²",
            "einheiten": "18",
            "endenergie": "38 kWh/(m²·a)",
            "primaerenergie": "33 kWh/(m²·a)",
            "klasse": "A",
            "heizung": "Strom (Wärmepumpe, zentral)",
            "warmwasser": "zentral über Wärmepumpe",
            "empfehlungen": [],
            "ausstellungsdatum": "12.06.2024",
            "gueltig_bis": "11.06.2034",
            "registriernummer": "DE-2024-9937-EAB",
        },
        "protokoll": {
            "datum": "19.06.2024",
            "beginn": "18:30 Uhr",
            "ende": "20:10 Uhr",
            "ort": "Gemeinschaftsraum, Rosenhügelweg 9",
            "versammlungsleiter": "Frau E. Hartmann (Hartmann Immobilienverwaltung)",
            "protokollfuehrer": "Herr S. Meyer",
            "anwesenheit": "15 von 18 Miteigentumsanteilen (83 %)",
            "tops": [
                (
                    "Genehmigung der Jahresabrechnung 2023",
                    "Beschluss: Genehmigt mit 14 Ja-Stimmen, 1 "
                    "Enthaltung.",
                ),
                (
                    "Installation einer Photovoltaikanlage auf dem Dach",
                    "Die Verwaltung stellt ein Angebot der Firma "
                    "SonnenEnergie Rhein-Main für eine "
                    "Gemeinschafts-Photovoltaikanlage auf dem Flachdach "
                    "vor. Geschätzte Kosten: 68.000 EUR, "
                    "Amortisationszeit ca. 9 Jahre. Beschluss: Die "
                    "Installation wird beauftragt, 13 Ja-Stimmen, "
                    "2 Gegenstimmen.",
                ),
                (
                    "Fahrradstellplätze",
                    "Beschluss: Erweiterung der Fahrradstellplätze in der "
                    "Tiefgarage um 10 Plätze, Kosten ca. 4.000 EUR, "
                    "einstimmig angenommen.",
                ),
                (
                    "Sonstiges",
                    "Keine weiteren Wortmeldungen.",
                ),
            ],
        },
        "teilungserklaerung": {
            "notar": "Notarin Dr. Sabine Klein, Frankfurt am Main",
            "urkundenrolle": "UR-Nr. 302/2020 K",
            "datum": "09.06.2020",
            "einheiten_hinweis": (
                "Das Gebäude ist in 18 Wohnungseigentumseinheiten "
                "aufgeteilt."
            ),
            "miteigentumsanteil": "82/1480",
            "sondereigentum": (
                "Die Wohnung im 3. OG (Einheit Nr. 9) nebst Balkon, "
                "Kellerabteil Nr. 9 und Tiefgaragenstellplatz Nr. 9."
            ),
            "gemeinschaftseigentum": (
                "Zum Gemeinschaftseigentum gehören Treppenhaus, Fahrstuhl, "
                "Dach, Fassade, Tiefgarage und die zentrale "
                "Wärmepumpenanlage."
            ),
            "kostenverteilung": (
                "Die Kosten werden nach dem Verhältnis der "
                "Miteigentumsanteile umgelegt."
            ),
            "sondernutzungsrechte": (
                "Der Eigentümer der Einheit Nr. 9 hat ein "
                "Sondernutzungsrecht an dem zugehörigen Balkon."
            ),
            "stimmrecht": (
                "Das Stimmrecht richtet sich nach dem Verhältnis der "
                "Miteigentumsanteile (Wertprinzip)."
            ),
            "bauliche_veraenderungen": (
                "Bauliche Veränderungen am Gemeinschaftseigentum bedürfen "
                "gemäß § 20 WEG eines Beschlusses der "
                "Eigentümerversammlung. Für Maßnahmen an der auf dem Dach "
                "beschlossenen Photovoltaikanlage (siehe Protokoll der "
                "Eigentümerversammlung vom 19.06.2024) sowie für "
                "Eingriffe in die Gebäudetechnik (Wärmepumpe, "
                "Dachkonstruktion) ist zusätzlich die Zustimmung der "
                "Eigentümerversammlung erforderlich. Balkonverglasungen "
                "sind einheitlich nach dem von der Verwaltung "
                "vorgegebenen Muster auszuführen."
            ),
            "instandhaltung": (
                "Jeder Eigentümer ist verpflichtet, sein Sondereigentum "
                "so instand zu halten, dass anderen Eigentümern kein "
                "Nachteil entsteht. Die Instandhaltung und "
                "Instandsetzung des Gemeinschaftseigentums, insbesondere "
                "der Wärmepumpenanlage, der Tiefgarage und der neu "
                "installierten Photovoltaikanlage, obliegt gemeinschaftlich "
                "allen Wohnungseigentümern."
            ),
            "verwalter": (
                "Die Wohnungseigentümergemeinschaft wird durch einen von "
                "der Eigentümerversammlung bestellten Verwalter "
                "vertreten (zum Zeitpunkt der Beurkundung: Hartmann "
                "Immobilienverwaltung). Der Verwalter ist insbesondere "
                "zuständig für die Aufstellung des Wirtschaftsplans, die "
                "Erstellung der Jahresabrechnung, die Einberufung und "
                "Durchführung der Eigentümerversammlungen sowie die "
                "Umsetzung der gefassten Beschlüsse."
            ),
            "tierhaltung": (
                "Die Haltung von Haustieren im üblichen Umfang ist "
                "zulässig, sofern hierdurch keine Beeinträchtigung "
                "anderer Eigentümer oder Bewohner entsteht. Die Haltung "
                "gefährlicher oder besonders lärmintensiver Tiere sowie "
                "eine gewerbsmäßige Tierhaltung bedarf der vorherigen "
                "Zustimmung der Verwaltung."
            ),
            "schlussbestimmungen": (
                "Sollte eine Bestimmung dieser Teilungserklärung "
                "unwirksam sein oder werden, bleibt die Wirksamkeit der "
                "übrigen Bestimmungen hiervon unberührt. Änderungen "
                "dieser Teilungserklärung bedürfen der notariellen Form "
                "sowie grundsätzlich der Zustimmung aller betroffenen "
                "Wohnungseigentümer. Die Kosten dieser Urkunde sowie "
                "ihres Vollzugs trägt der jeweilige Ersterwerber der "
                "betreffenden Einheit."
            ),
        },
    },
    # ------------------------------------------------------------------
    # Objekt 8: Birkenallee (NEU)
    # Ähnlicher Neubau wie Rosenhügel, aber OHNE PV-Beschluss —
    # Gegenstück für den Cross-Objekt-Verwechslungstest.
    # ------------------------------------------------------------------
    {
        "id": "objekt8",
        "name": "Birkenallee",
        "adresse": "Birkenallee 15, 01277 Dresden (Striesen)",
        "expose": {
            "beschreibung": (
                "Freundliche 2-Zimmer-Erstbezugswohnung in einem 2022 "
                "fertiggestellten Neubau. Praktischer Grundriss und "
                "moderne Ausstattung zu einem attraktiven Preis."
            ),
            "wohnflaeche": "58 m²",
            "zimmer": "2",
            "baujahr": "2022",
            "etage": "1. OG von 4",
            "kaufpreis": "245.000 EUR",
            "hausgeld": "180 EUR",
            "stellplatz": "1 Außenstellplatz",
            "bezugsfrei": "sofort",
            "ausstattung": [
                "Fußbodenheizung",
                "Fenster mit Dreifachverglasung",
                "Modernes Bad mit Dusche",
                "Balkon (ca. 6 m²)",
                "Einbauküche (2022)",
                "Kein Fahrstuhl (Neubau ohne Aufzug, nur 4 Geschosse)",
            ],
            "lage": (
                "Beliebtes Wohnviertel Striesen, gute Anbindung an die "
                "Dresdner Innenstadt (ca. 15 Minuten mit der "
                "Straßenbahn)."
            ),
            "kontakt_name": "Frau L. Winter",
            "kontakt_tel": "0351 / 555-0299",
            "kontakt_email": "winter@musterwert-immobilien-beispiel.de",
        },
        "energieausweis": {
            "art": "Bedarfsausweis",
            "gebaeudetyp": "Mehrfamilienhaus, Wohnungseigentum (Neubau)",
            "baujahr_gebaeude": "2022",
            "baujahr_waermeerzeuger": "2022 (Gas-Brennwertkessel, zentral)",
            "wohnflaeche": "58 m²",
            "einheiten": "12",
            "endenergie": "58 kWh/(m²·a)",
            "primaerenergie": "52 kWh/(m²·a)",
            "klasse": "B",
            "heizung": "Erdgas (zentral)",
            "warmwasser": "zentral über Heizungsanlage",
            "empfehlungen": [],
            "ausstellungsdatum": "27.04.2024",
            "gueltig_bis": "26.04.2034",
            "registriernummer": "DE-2024-9938-EAB",
        },
        "protokoll": {
            "datum": "08.06.2024",
            "beginn": "18:00 Uhr",
            "ende": "19:30 Uhr",
            "ort": "Gemeinschaftsraum, Birkenallee 15",
            "versammlungsleiter": "Herr O. Lange (Lange Hausverwaltung)",
            "protokollfuehrer": "Frau P. Schubert",
            "anwesenheit": "9 von 12 Miteigentumsanteilen (75 %)",
            "tops": [
                (
                    "Genehmigung der Jahresabrechnung 2023",
                    "Da das Gebäude erst 2022 fertiggestellt wurde, "
                    "handelt es sich um die zweite Jahresabrechnung. "
                    "Beschluss: Genehmigt mit 9 Ja-Stimmen.",
                ),
                (
                    "Gartenpflege",
                    "Beschluss: Beauftragung eines Gartenbaubetriebs für "
                    "die Pflege der Außenanlagen, Kosten ca. 1.500 EUR "
                    "pro Jahr, einstimmig angenommen.",
                ),
                (
                    "Briefkastenanlage",
                    "Die bestehende Briefkastenanlage wird als "
                    "ausreichend erachtet, keine Änderung erforderlich.",
                ),
                (
                    "Sonstiges",
                    "Ein Eigentümer fragt nach der Möglichkeit einer "
                    "Photovoltaikanlage auf dem Dach. Die Verwaltung "
                    "sagt zu, dies bei Bedarf für eine der nächsten "
                    "Versammlungen als eigenen Tagesordnungspunkt "
                    "vorzubereiten — ein konkreter Beschluss wurde in "
                    "dieser Versammlung nicht gefasst.",
                ),
            ],
        },
        "teilungserklaerung": {
            "notar": "Notar Dr. Frank Peters, Dresden",
            "urkundenrolle": "UR-Nr. 177/2021 P",
            "datum": "22.09.2021",
            "einheiten_hinweis": (
                "Das Gebäude ist in 12 Wohnungseigentumseinheiten "
                "aufgeteilt."
            ),
            "miteigentumsanteil": "58/700",
            "sondereigentum": (
                "Die Wohnung im 1. OG (Einheit Nr. 3) nebst Balkon und "
                "Außenstellplatz Nr. 3."
            ),
            "gemeinschaftseigentum": (
                "Zum Gemeinschaftseigentum gehören Treppenhaus, Dach, "
                "Fassade und die zentrale Heizungsanlage."
            ),
            "kostenverteilung": (
                "Die Kosten werden nach dem Verhältnis der "
                "Miteigentumsanteile umgelegt."
            ),
            "sondernutzungsrechte": (
                "Der Eigentümer der Einheit Nr. 3 hat ein "
                "Sondernutzungsrecht an dem zugehörigen Balkon."
            ),
            "stimmrecht": (
                "Das Stimmrecht richtet sich nach dem Verhältnis der "
                "Miteigentumsanteile (Wertprinzip)."
            ),
            "bauliche_veraenderungen": (
                "Bauliche Veränderungen am Gemeinschaftseigentum bedürfen "
                "gemäß § 20 WEG eines Beschlusses der "
                "Eigentümerversammlung. Die spätere Nachrüstung einer "
                "Photovoltaikanlage auf dem Dach — wie in der "
                "Eigentümerversammlung vom 08.06.2024 angeregt, aber noch "
                "nicht beschlossen — bedarf eines gesonderten "
                "Mehrheitsbeschlusses samt Kostenvoranschlag, bevor mit "
                "der Umsetzung begonnen werden darf. Veränderungen an "
                "den Balkonen sind einheitlich nach dem von der "
                "Verwaltung vorgegebenen Muster auszuführen."
            ),
            "instandhaltung": (
                "Jeder Eigentümer ist verpflichtet, sein Sondereigentum "
                "so instand zu halten, dass anderen Eigentümern kein "
                "Nachteil entsteht. Die Instandhaltung und "
                "Instandsetzung des Gemeinschaftseigentums obliegt "
                "gemeinschaftlich allen Wohnungseigentümern. Da das Gebäude erst "
                "2022 fertiggestellt wurde, bestehen für wesentliche "
                "Bauteile noch Gewährleistungsansprüche gegenüber dem "
                "Bauträger, die von der Verwaltung im Interesse der "
                "Gemeinschaft zu verfolgen sind."
            ),
            "verwalter": (
                "Die Wohnungseigentümergemeinschaft wird durch einen von "
                "der Eigentümerversammlung bestellten Verwalter "
                "vertreten (zum Zeitpunkt der Beurkundung: Lange "
                "Hausverwaltung). Der Verwalter ist insbesondere "
                "zuständig für die Aufstellung des Wirtschaftsplans, die "
                "Erstellung der Jahresabrechnung, die Einberufung und "
                "Durchführung der Eigentümerversammlungen sowie die "
                "Umsetzung der gefassten Beschlüsse."
            ),
            "tierhaltung": (
                "Die Haltung von Haustieren im üblichen Umfang ist "
                "zulässig, sofern hierdurch keine Beeinträchtigung "
                "anderer Eigentümer oder Bewohner entsteht. Die Haltung "
                "gefährlicher oder besonders lärmintensiver Tiere bedarf "
                "der vorherigen Zustimmung der Verwaltung."
            ),
            "schlussbestimmungen": (
                "Sollte eine Bestimmung dieser Teilungserklärung "
                "unwirksam sein oder werden, bleibt die Wirksamkeit der "
                "übrigen Bestimmungen hiervon unberührt. Änderungen "
                "dieser Teilungserklärung bedürfen der notariellen Form "
                "sowie grundsätzlich der Zustimmung aller betroffenen "
                "Wohnungseigentümer. Die Kosten dieser Urkunde sowie "
                "ihres Vollzugs trägt der jeweilige Ersterwerber der "
                "betreffenden Einheit."
            ),
        },
    },
]
