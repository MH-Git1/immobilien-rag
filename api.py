"""
Web-API für den Objektunterlagen-Assistenten.

Dünner FastAPI-Wrapper um main.py: baut den Index einmal beim Start
und beantwortet Fragen über einen HTTP-Endpunkt, statt wie
interaktive_schleife() in main.py über die Konsole. Nutzt dieselbe
beantworte_frage()-Funktion wie die Konsolen-Variante und der
Testkatalog (tests/testfragen.py) — Filterung, Prompt und
Antwortverhalten sind identisch.
"""

import base64
import os
import re
import secrets
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, Form, UploadFile
from fastapi.staticfiles import StaticFiles
from llama_index.readers.file import PDFReader
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

import extraktion
from main import DATA_DIR, baue_index, beantworte_frage, _bekannte_objektnamen

# Wird beim Start einmal befüllt (siehe lifespan unten), damit der Index
# nicht bei jeder Anfrage neu geladen wird.
zustand: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    zustand["index"] = baue_index()
    zustand["bekannte_objekte"] = _bekannte_objektnamen()
    yield


app = FastAPI(title="Objektunterlagen-Assistent", lifespan=lifespan)


class BasicAuthMiddleware(BaseHTTPMiddleware):
    """
    Einfacher Zugriffsschutz für die öffentlich erreichbare Deployment-
    Instanz (siehe render.yaml / README, Abschnitt Deployment). Greift
    nur, wenn BASIC_AUTH_USER und BASIC_AUTH_PASSWORD gesetzt sind — im
    lokalen Betrieb (keine dieser Variablen in .env) bleibt die App wie
    bisher ungeschützt erreichbar.
    """

    async def dispatch(self, request, call_next):
        erwarteter_benutzer = os.getenv("BASIC_AUTH_USER")
        erwartetes_passwort = os.getenv("BASIC_AUTH_PASSWORD")
        if not erwarteter_benutzer or not erwartetes_passwort:
            return await call_next(request)

        header = request.headers.get("authorization", "")
        if header.startswith("Basic "):
            try:
                benutzer, passwort = (
                    base64.b64decode(header[6:]).decode("utf-8").split(":", 1)
                )
            except Exception:
                benutzer, passwort = "", ""
            if secrets.compare_digest(
                benutzer, erwarteter_benutzer
            ) and secrets.compare_digest(passwort, erwartetes_passwort):
                return await call_next(request)

        return Response(
            status_code=401,
            headers={"WWW-Authenticate": 'Basic realm="Objektunterlagen-Assistent"'},
        )


app.add_middleware(BasicAuthMiddleware)


class FrageRequest(BaseModel):
    frage: str


class Quelle(BaseModel):
    dateiname: str
    score: float


class FrageResponse(BaseModel):
    antwort: str
    objekt: str | None
    quellen: list[Quelle]


@app.post("/api/frage")
def frage_stellen(request: FrageRequest) -> FrageResponse:
    antwort, objekt = beantworte_frage(
        zustand["index"], request.frage, zustand["bekannte_objekte"], herkunft="web"
    )
    quellen = [
        Quelle(
            dateiname=node.metadata.get("file_name", "unbekannt"),
            score=node.score or 0.0,
        )
        for node in antwort.source_nodes
    ]
    return FrageResponse(antwort=str(antwort), objekt=objekt, quellen=quellen)


@app.get("/api/objekte")
def objekte_auflisten() -> list[str]:
    return sorted(zustand["bekannte_objekte"])


@app.get("/api/kennzahlen")
def kennzahlen_auflisten() -> list[dict]:
    """
    Strukturiert extrahierte Kennzahlen (Kaufpreis, Wohnfläche, ...) je
    Dokument, siehe extraktion.py -- bewusst pro Quelldokument, nicht
    pro Objekt zusammengeführt, damit Widersprüche zwischen Quellen
    (z.B. abweichende Wohnflächen-Angabe) sichtbar bleiben.
    """
    return extraktion.alle_kennzahlen()


@app.get("/api/kennzahlen/{objekt_name}")
def kennzahlen_fuer_objekt(objekt_name: str) -> list[dict]:
    return extraktion.kennzahlen_fuer_objekt(objekt_name)


def _slug(text: str) -> str:
    """
    Wandelt einen frei eingegebenen Objektnamen in eine dateiname- und
    metadatentaugliche Kurzform um (z.B. "Musterstraße 12" ->
    "musterstrasse-12"). Dieselbe Form wird als objekt_name-Metadatenfeld
    verwendet, damit Metadaten-Filterung (_erkenne_objekt in main.py) und
    Dateiname konsistent bleiben.
    """
    ersetzungen = str.maketrans("äöü", "aou")
    text = text.strip().lower().replace("ß", "ss").translate(ersetzungen)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text or "objekt"


class UploadErgebnis(BaseModel):
    dateiname: str
    seiten: int


class UploadResponse(BaseModel):
    objekt: str
    hochgeladen: list[UploadErgebnis]


@app.post("/api/upload")
async def dokumente_hochladen(
    objekt_name: str = Form(...), dateien: list[UploadFile] = File(...)
) -> UploadResponse:
    """
    Nimmt mehrere PDFs für ein Objekt entgegen, speichert sie in
    DATA_DIR (wie der bestehende Corpus) und fügt sie inkrementell in
    den laufenden Index ein (index.insert), statt den kompletten Index
    neu zu bauen. Der Objektname wird zu einem Slug normalisiert
    (siehe _slug) und sowohl im Dateinamen als auch im
    objekt_name-Metadatenfeld verwendet, damit ein späterer kompletter
    Neuaufbau (SimpleDirectoryReader + _objekt_metadata in main.py) den
    gleichen Objektnamen wieder erkennt.
    """
    objekt_slug = _slug(objekt_name)
    pdf_reader = PDFReader()
    ergebnisse = []

    for datei in dateien:
        original_name = Path(datei.filename or "dokument.pdf").stem
        original_name = re.sub(r"[^a-zA-Z0-9-]+", "-", original_name).strip("-")
        zielpfad = Path(DATA_DIR) / f"hochgeladen_{objekt_slug}_{original_name}.pdf"
        if zielpfad.exists():
            zielpfad = zielpfad.with_stem(f"{zielpfad.stem}_{int(time.time() * 1000)}")

        inhalt = await datei.read()
        zielpfad.write_bytes(inhalt)

        seiten = pdf_reader.load_data(zielpfad)
        for seite in seiten:
            seite.metadata["objekt_name"] = objekt_slug
            seite.metadata["file_name"] = zielpfad.name
            zustand["index"].insert(seite)

        voller_text = "\n".join(seite.text for seite in seiten)
        extraktion.extrahiere_und_speichere(objekt_slug, zielpfad.name, voller_text)

        ergebnisse.append(UploadErgebnis(dateiname=zielpfad.name, seiten=len(seiten)))

    if objekt_slug not in zustand["bekannte_objekte"]:
        zustand["bekannte_objekte"].append(objekt_slug)

    return UploadResponse(objekt=objekt_slug, hochgeladen=ergebnisse)


# Frontend als statische Dateien ausliefern (index.html unter "/").
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
