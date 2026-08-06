"""
Gemeinsame Postgres-Verbindungsparameter, genutzt von main.py (Vektor-
Index) und protokoll.py (Anfrage-Protokoll) — eigenes Modul, damit
protokoll.py main.py nicht importieren muss (main.py wiederum ruft
protokoll.py auf, das würde sonst einen Zirkelimport erzeugen).
"""

import os


def verbindungsparameter() -> dict:
    """Liest die Postgres-Zugangsdaten aus den Umgebungsvariablen (.env)."""
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": os.getenv("POSTGRES_PORT", "5432"),
        "database": os.getenv("POSTGRES_DB", "immobilien_rag"),
        "user": os.getenv("POSTGRES_USER", "immobilien_rag"),
        "password": os.getenv("POSTGRES_PASSWORD", "immobilien_rag"),
    }
