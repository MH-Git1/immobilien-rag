const verlauf = document.getElementById("verlauf");
const leerzustand = document.getElementById("leerzustand");
const formular = document.getElementById("frage-formular");
const eingabe = document.getElementById("frage-eingabe");
const sendenButton = document.getElementById("senden-button");

function nachrichtHinzufuegen(html, klasse) {
  const el = document.createElement("div");
  el.className = `nachricht ${klasse}`;
  el.innerHTML = html;
  verlauf.appendChild(el);
  el.scrollIntoView({ behavior: "smooth", block: "end" });
  return el;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

async function frageSenden(frage) {
  leerzustand.style.display = "none";
  nachrichtHinzufuegen(`<div class="blase">${escapeHtml(frage)}</div>`, "frage");

  const ladeBlase = nachrichtHinzufuegen(
    `<div class="blase ladeanzeige"><span></span><span></span><span></span></div>`,
    "antwort"
  );

  eingabe.disabled = true;
  sendenButton.disabled = true;

  try {
    const response = await fetch("/api/frage", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ frage }),
    });

    if (!response.ok) {
      throw new Error(`Server-Fehler (${response.status})`);
    }

    const daten = await response.json();

    let inhalt = "";
    if (daten.objekt) {
      inhalt += `<div class="objekt-badge">Gefiltert auf Objekt: ${escapeHtml(daten.objekt)}</div>`;
    }
    inhalt += `<div class="blase">${escapeHtml(daten.antwort)}</div>`;
    if (daten.quellen && daten.quellen.length > 0) {
      inhalt += `<div class="quellen">${daten.quellen
        .map(
          (q) =>
            `<span class="quelle-chip">${escapeHtml(q.dateiname)} · ${(q.score * 100).toFixed(0)}%</span>`
        )
        .join("")}</div>`;
    }
    inhalt += `<button class="kopieren-button" data-antwort="${escapeHtml(daten.antwort)}">Kopieren</button>`;
    ladeBlase.innerHTML = inhalt;
  } catch (fehler) {
    ladeBlase.innerHTML = `<div class="blase">Entschuldigung, es ist ein Fehler aufgetreten: ${escapeHtml(fehler.message)}</div>`;
  } finally {
    eingabe.disabled = false;
    sendenButton.disabled = false;
    eingabe.focus();
  }
}

formular.addEventListener("submit", (ereignis) => {
  ereignis.preventDefault();
  const frage = eingabe.value.trim();
  if (!frage) return;
  eingabe.value = "";
  frageSenden(frage);
});

document.querySelectorAll(".beispiel-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    frageSenden(chip.textContent);
  });
});

// Event-Delegation statt Listener pro Nachricht, da Antwort-Elemente
// erst zur Laufzeit über innerHTML entstehen.
verlauf.addEventListener("click", async (ereignis) => {
  const button = ereignis.target.closest(".kopieren-button");
  if (!button) return;

  try {
    await navigator.clipboard.writeText(button.dataset.antwort);
    button.textContent = "Kopiert ✓";
    button.disabled = true;
    setTimeout(() => {
      button.textContent = "Kopieren";
      button.disabled = false;
    }, 1500);
  } catch (fehler) {
    button.textContent = "Kopieren fehlgeschlagen";
  }
});

// --- Tabs ---

document.querySelectorAll(".tab-button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".tab-button").forEach((b) => b.classList.remove("aktiv"));
    document.querySelectorAll(".tab-inhalt").forEach((t) => t.classList.remove("aktiv"));
    button.classList.add("aktiv");
    document.getElementById(`${button.dataset.tab}-tab`).classList.add("aktiv");
  });
});

// --- Upload ---

const objektEingabe = document.getElementById("objekt-eingabe");
const objektListe = document.getElementById("objekt-liste");
const dropZone = document.getElementById("drop-zone");
const dateiEingabe = document.getElementById("datei-eingabe");
const dateiListeEl = document.getElementById("datei-liste");
const uploadButton = document.getElementById("upload-button");

let ausgewaehlteDateien = [];

async function bekannteObjekteLaden() {
  try {
    const response = await fetch("/api/objekte");
    const objekte = await response.json();
    objektListe.innerHTML = objekte
      .map((name) => `<option value="${escapeHtml(name)}"></option>`)
      .join("");
  } catch (fehler) {
    // Datalist ist nur eine Komfortfunktion — bei Fehler einfach leer lassen.
  }
}

function uploadButtonAktualisieren() {
  uploadButton.disabled =
    ausgewaehlteDateien.length === 0 || objektEingabe.value.trim() === "";
}

function dateiListeRendern() {
  dateiListeEl.innerHTML = ausgewaehlteDateien
    .map(
      (eintrag, index) => `
      <li class="datei-eintrag" data-index="${index}">
        <span class="name">${escapeHtml(eintrag.datei.name)}</span>
        <span class="status ${eintrag.statusKlasse || ""}">${eintrag.status}</span>
        ${eintrag.entfernbar ? '<button class="entfernen" aria-label="Entfernen">×</button>' : ""}
      </li>`
    )
    .join("");
  uploadButtonAktualisieren();
}

function dateienHinzufuegen(fileList) {
  Array.from(fileList).forEach((datei) => {
    if (datei.type !== "application/pdf") return;
    const bereitsDrin = ausgewaehlteDateien.some(
      (e) => e.datei.name === datei.name && e.datei.size === datei.size
    );
    if (bereitsDrin) return;
    ausgewaehlteDateien.push({ datei, status: "wartet", statusKlasse: "", entfernbar: true });
  });
  dateiListeRendern();
}

dropZone.addEventListener("click", () => dateiEingabe.click());

dateiEingabe.addEventListener("change", () => {
  dateienHinzufuegen(dateiEingabe.files);
  dateiEingabe.value = "";
});

["dragover", "dragenter"].forEach((ereignis) => {
  dropZone.addEventListener(ereignis, (e) => {
    e.preventDefault();
    dropZone.classList.add("ueber-ziel");
  });
});

["dragleave", "dragend"].forEach((ereignis) => {
  dropZone.addEventListener(ereignis, () => dropZone.classList.remove("ueber-ziel"));
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("ueber-ziel");
  dateienHinzufuegen(e.dataTransfer.files);
});

dateiListeEl.addEventListener("click", (e) => {
  const button = e.target.closest(".entfernen");
  if (!button) return;
  const index = Number(button.closest(".datei-eintrag").dataset.index);
  ausgewaehlteDateien.splice(index, 1);
  dateiListeRendern();
});

objektEingabe.addEventListener("input", uploadButtonAktualisieren);

uploadButton.addEventListener("click", async () => {
  const objektName = objektEingabe.value.trim();
  if (!objektName || ausgewaehlteDateien.length === 0) return;

  uploadButton.disabled = true;
  ausgewaehlteDateien.forEach((e) => {
    e.status = "wird hochgeladen …";
    e.entfernbar = false;
  });
  dateiListeRendern();

  const formData = new FormData();
  formData.append("objekt_name", objektName);
  ausgewaehlteDateien.forEach((e) => formData.append("dateien", e.datei));

  try {
    const response = await fetch("/api/upload", { method: "POST", body: formData });
    if (!response.ok) {
      throw new Error(`Server-Fehler (${response.status})`);
    }
    await response.json();
    ausgewaehlteDateien.forEach((e) => {
      e.status = "erledigt";
      e.statusKlasse = "erledigt";
    });
    await bekannteObjekteLaden();
  } catch (fehler) {
    ausgewaehlteDateien.forEach((e) => {
      e.status = "Fehler";
      e.statusKlasse = "fehler";
    });
  }

  dateiListeRendern();
});

bekannteObjekteLaden();
