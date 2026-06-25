import json
import os
import smtplib
import pathlib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Pantaleo Brand Checker")

BASE_DIR = pathlib.Path(__file__).parent
PROPOSALS_FILE = BASE_DIR / "proposals.json"
KB_FILE = BASE_DIR / "knowledge_base.md"

# ── helpers ──────────────────────────────────────────────────────────────────

def load_knowledge_base() -> str:
    if KB_FILE.exists():
        return KB_FILE.read_text(encoding="utf-8")
    return "Knowledge base non disponibile. Inserire il file knowledge_base.md."


def load_proposals() -> list:
    if PROPOSALS_FILE.exists():
        try:
            return json.loads(PROPOSALS_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def save_proposals(proposals: list) -> None:
    PROPOSALS_FILE.write_text(
        json.dumps(proposals, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def send_email_notification(proposal: dict) -> bool:
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASSWORD")

    if not all([host, user, password]):
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[Pantaleo Brand Checker] Nuova proposta KB: {proposal['type']}"
    msg["From"] = user
    msg["To"] = "ettore@veritable-sb.it"

    body = f"""
Nuova proposta di aggiornamento alla Knowledge Base Pantaleo.

Tipo: {proposal['type']}
Data: {proposal['timestamp']}

Descrizione:
{proposal['text']}

---
Inviata tramite Pantaleo Brand Checker — Uso interno Véritable
    """.strip()

    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(host, port) as server:
            server.ehlo()
            server.starttls()
            server.login(user, password)
            server.sendmail(user, "ettore@veritable-sb.it", msg.as_string())
        return True
    except Exception:
        return False


SYSTEM_PROMPT = """Sei il brand guardian interno di Nicola Pantaleo S.p.A. Verifica la coerenza dei contenuti di comunicazione rispetto alla knowledge base ufficiale del brand. Non riscrivi i contenuti. Diagnostichi con precisione citando le parole specifiche del testo. Rispondi SOLO in JSON valido senza markdown.

Formato risposta OBBLIGATORIO (JSON puro, nessun testo prima o dopo):
{
  "verdict": "ok|warn|fail",
  "summary": "frase max 12 parole",
  "dimensions": [
    {
      "name": "nome dimensione",
      "status": "ok|warn|fail",
      "note": "2-3 righe di analisi",
      "issues": [
        {"level": "ok|warn|fail", "text": "dettaglio specifico citando il testo"}
      ]
    }
  ]
}

Le 5 dimensioni da analizzare (nell'ordine):
1. Posizionamento e identità
2. Prodotto e claim
3. Tono di voce
4. Impieghi e abbinamenti
5. Accuratezza fattuale

Regole verdict globale:
- "ok": tutte le dimensioni ok o al massimo warn minori
- "warn": almeno una dimensione warn significativa, nessuna fail
- "fail": almeno una dimensione fail

Cita sempre le parole esatte del testo analizzato nelle note e negli issues."""


# ── schemas ───────────────────────────────────────────────────────────────────

class VerifyRequest(BaseModel):
    format: str
    products: list[str]
    content: str


class ProposeRequest(BaseModel):
    type: str
    text: str


# ── routes ────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def index():
    html_file = BASE_DIR / "static" / "index.html"
    return HTMLResponse(content=html_file.read_text(encoding="utf-8"))


@app.get("/api/kb")
async def get_kb():
    return {"content": load_knowledge_base()}


@app.post("/verify")
async def verify(req: VerifyRequest):
    if not req.content.strip():
        raise HTTPException(status_code=400, detail="Il contenuto non può essere vuoto.")

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY non configurata.")

    kb = load_knowledge_base()
    products_str = ", ".join(req.products) if req.products else "Generico/brand"

    user_message = f"""Formato comunicativo: {req.format}
Prodotti citati: {products_str}

Testo da verificare:
---
{req.content}
---

KNOWLEDGE BASE NICOLA PANTALEO S.p.A.:
---
{kb}
---

Analizza il testo rispetto alla knowledge base. Rispondi solo in JSON valido."""

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        raw = message.content[0].text.strip()

        # Strip accidental markdown fences if present
        if raw.startswith("```"):
            lines = raw.split("\n")
            raw = "\n".join(
                line for line in lines if not line.startswith("```")
            ).strip()

        result = json.loads(raw)
        return result

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=502,
            detail=f"Risposta del modello non valida (JSON malformato): {str(e)}",
        )
    except anthropic.APIStatusError as e:
        raise HTTPException(status_code=502, detail=f"Errore API Anthropic: {e.message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/propose")
async def propose(req: ProposeRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="La proposta non può essere vuota.")

    proposals = load_proposals()
    entry = {
        "id": len(proposals) + 1,
        "type": req.type,
        "text": req.text.strip(),
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
    proposals.append(entry)
    save_proposals(proposals)

    email_sent = send_email_notification(entry)

    return {
        "saved": True,
        "email_sent": email_sent,
        "id": entry["id"],
        "message": "Proposta salvata" + (" e notifica inviata." if email_sent else ". Notifica email non inviata (SMTP non configurato)."),
    }


# Mount static files last so the catch-all index route takes precedence
static_dir = BASE_DIR / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
