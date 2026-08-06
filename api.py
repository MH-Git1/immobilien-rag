"""
Web-API für den Objektunterlagen-Assistenten.

Dünner FastAPI-Wrapper um main.py: baut den Index einmal beim Start
und beantwortet Fragen über einen HTTP-Endpunkt, statt wie
interaktive_schleife() in main.py über die Konsole. Nutzt dieselbe
beantworte_frage()-Funktion wie die Konsolen-Variante und der
Testkatalog (tests/testfragen.py) — Filterung, Prompt und
Antwortverhalten sind identisch.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from main import baue_index, beantworte_frage, _bekannte_objektnamen

# Wird beim Start einmal befüllt (siehe lifespan unten), damit der Index
# nicht bei jeder Anfrage neu geladen wird.
zustand: dict = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    zustand["index"] = baue_index()
    zustand["bekannte_objekte"] = _bekannte_objektnamen()
    yield


app = FastAPI(title="Objektunterlagen-Assistent", lifespan=lifespan)


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
        zustand["index"], request.frage, zustand["bekannte_objekte"]
    )
    quellen = [
        Quelle(
            dateiname=node.metadata.get("file_name", "unbekannt"),
            score=node.score or 0.0,
        )
        for node in antwort.source_nodes
    ]
    return FrageResponse(antwort=str(antwort), objekt=objekt, quellen=quellen)


# Frontend als statische Dateien ausliefern (index.html unter "/").
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
