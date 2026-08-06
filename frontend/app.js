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
