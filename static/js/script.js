// static/js/script.js

const predictionEl = document.getElementById("prediction");
const sentenceEl   = document.getElementById("sentence");

const spaceBtn     = document.getElementById("space-btn");
const backspaceBtn = document.getElementById("backspace-btn");
const clearBtn     = document.getElementById("clear-btn");
const speakBtn     = document.getElementById("speak-btn");

let pollTimer = null;

// ---------- STATUS POLLING ----------
async function fetchStatus() {
    try {
        const res = await fetch("/status");
        const data = await res.json();
        predictionEl.textContent = data.prediction || "-";
        sentenceEl.textContent   = data.sentence   || "";
    } catch {}
}

function startPolling() {
    pollTimer = setInterval(fetchStatus, 180);
    fetchStatus();
}

// ---------- SERVER UPDATES ----------
async function sendUpdate(action) {
    const res = await fetch("/update_sentence", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ action })
    });
    const data = await res.json();
    sentenceEl.textContent = data.sentence;
}

// ---------- REAL AUDIO SPEAK ----------
async function requestSpeak() {
    try {
        const res = await fetch("/speak_text", { method: "POST" });
        const data = await res.json();
        if (!data.audio) return;

        const audio = new Audio(data.audio);
        audio.play();
    } catch (err) {
        console.error("Speak Request Error:", err);
    }
}


// ---------- BIND BUTTONS ----------
document.addEventListener("DOMContentLoaded", () => {
    startPolling();

    spaceBtn.addEventListener("click", () => sendUpdate("space"));
    backspaceBtn.addEventListener("click", () => sendUpdate("backspace"));
    clearBtn.addEventListener("click", () => sendUpdate("clear"));
    speakBtn.addEventListener("click", requestSpeak);

    // KEYBOARD SHORTCUTS
    window.addEventListener("keydown", (e) => {
        if (e.code === "Space") {
            e.preventDefault();
            sendUpdate("space");
        } else if (e.code === "Backspace") {
            e.preventDefault();
            sendUpdate("backspace");
        } else if (e.key === "c" || e.key === "C") {
            sendUpdate("clear");
        } else if (e.key === "s" || e.key === "S") {
            requestSpeak();
        }
    });
});
