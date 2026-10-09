import json
import os
from datetime import datetime, timezone
from pathlib import Path

import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI(title="Pantaleo Brand Checker")

PROPOSALS_FILE = Path("proposals.json")

SYSTEM_PROMPT = """Sei il brand guardian interno di Nicola Pantaleo S.p.A. Verifica la coerenza dei contenuti di comunicazione rispetto alla knowledge base ufficiale del brand. Non riscrivi i contenuti. Diagnostichi con precisione citando le parole specifiche del testo. Rispondi SOLO in JSON valido senza markdown senza backtick senza testo prima o dopo.

Formato risposta JSON:
{"verdict":"ok|warn|fail","summary":"frase max 12 parole","dimensions":[{"name":"nome dimensione","status":"ok|warn|fail","note":"2-3 righe di spiegazione","issues":[{"level":"ok|warn|fail","text":"dettaglio specifico citando il testo"}]}]}

Le 5 dimensioni da verificare sempre:
1. Posizionamento e identità — heritage, territorialità pugliese, tono istituzionale
2. Prodotto e claim — claim vietati, claim approvati, certificazioni usate correttamente
3. Tono di voce — registro, precisione, assenza di enfasi vuota
4. Impieghi e abbinamenti — usi del prodotto coerenti con quelli ufficiali
5. Accuratezza fattuale — nessuna affermazione inventata o non verificabile

KNOWLEDGE BASE:

IDENTITÀ: Nicola Pantaleo S.p.A., Fasano di Puglia (BR), dal 1890. 4 generazioni. 150 ettari uliveti propri. 30 mercati. Certificazioni: IGP Olio di Puglia (solo prodotto IGP), IFS Food, Biologico ICEA, Kosher, Halal, ISO 9001.

GAMMA PRODOTTI ONLINE:
- IGP Olio di Puglia: certificato IGP, disciplinare con soglia minima polifenoli totali ≥300ppm e biofenoli attivi ≥250ppm, uso crudo e cucina pregiata
- Biologico 100% Italiano: certificato bio ICEA, "secondo natura"
- 100% Italiano: selezione accurata oli italiani pregiati, crudo e cottura
- Selezione Oro: olive più pregiate, "dalla nostra alla vostra tavola", uso crudo privilegiato
- Rusticano: "bontà dell'olio appena franto", carattere rustico e intenso
- OroNovo: "carattere fresco e deciso"
- Bio Young: biologico 250ml, famiglie e bambini, "l'olio Bio dedicato alla salute di chi ami"
- Zero: estratto a freddo, senza pesticidi residui — unico prodotto per cui è corretto usare "estratto a freddo" come claim differenziante
- Aromatizzati: limone, peperoncino, agrumi, tartufo nero, basilico, aglio
- Squeezable/Squeeze Me: 750ml e 500ml
- Kit degustazione: Buono a crudo, Da 0 a 100, Dalla frittura all'assaggio, Mediterraneo classico

CLAIM VIETATI (mai usare):
- "prima spremitura" — requisito obbligatorio per tutti gli EVO, non differenziante
- "spremuto a freddo" — idem
- "light" — fuorviante, tutti gli oli hanno stesso apporto calorico
- "dietetico" — fuorviante
- superlative assoluti non documentati
- certificazione IGP attribuita a prodotti non IGP

VOCABOLARIO APPROVATO: fruttato, pungente, amaro (accezione positiva), retrogusto di carciofo crudo, floreale, armonico, corposo, genuino, delicato, mandorlato, erbaceo. Heritage: "dal 1890", "quattro generazioni", "terra di Puglia", "Fasano". Benefici documentati: digeribilità, sostanze fenoliche antiossidanti, acido oleico, dieta mediterranea (fonte Ancel Keys), biofenoli e Regolamento europeo 432/2012 (solo per IGP).

IMPIEGHI UFFICIALI:
- Crudo (IGP, Selezione Oro, premium): pinzimoni, bruschette, verdure cotte e crude, legumi, carni rosse arrosto, pesci bolliti, insalate, tartare, vinaigrette, maionese
- Cottura (classico, 100% italiano, rusticano): fritture ortaggi, fritture pesce, cotolette, pizze, focacce, rustici, dolci, sughi, zuppe
- Famiglia/bambini (Bio Young, classico): pastine, minestre di verdure
- Aromatizzati: basilico→pasta e verdure; limone→pesce e carpacci; aglio→bruschette e zuppe; tartufo→risotti e paste; agrumi→pesce e crudité; peperoncino→sughi e carni
- EVO Pantaleo resiste fino a 180°C, adatto alla frittura

TONO DI VOCE: autorevole ma accessibile, divulgativo senza tecnicismi, prima persona plurale, nessuna enfasi promozionale vuota, radici pugliesi esplicite, precisione nelle affermazioni, italiano istituzionale corretto.

RICETTE BLOG — categorie: Antipasti e zuppe, Primi, Secondi e piatti unici, Dolci, Salse e contorni. Ogni ricetta associa un prodotto specifico.

ANTI-GREENWASHING: non usare "sostenibile" senza pratiche documentate, non inventare premi, non attribuire proprietà mediche assolute.

CONFORMITÀ NORMATIVA — D.Lgs. 162/2024 (Green Claims) e Codice del Consumo aggiornato:

D.Lgs. 162/2024 (recepimento Direttiva UE 2024/825/UE "Empowering Consumers for Green Transition") — in vigore:
- VIETATI i claim ambientali generici privi di prova verificabile e certificazione di terza parte riconosciuta: "sostenibile", "eco-friendly", "verde", "naturale", "a basso impatto ambientale", "rispettoso del clima", "biodegradabile", "carbon neutral", "a emissioni zero", "rispettoso della natura" e locuzioni equivalenti.
- Ogni claim di sostenibilità deve essere: specifico (riferito a un aspetto preciso del prodotto o processo), verificabile (basato su evidenza scientifica o dati misurabili), certificato da ente accreditato o schema ufficiale riconosciuto dall'UE o dalle autorità nazionali.
- Le etichette volontarie di sostenibilità non approvate da schemi pubblici o riconosciuti sono vietate (art. 6-bis Direttiva 2005/29/CE come modificata).
- Impegni futuri sull'ambiente (es. "entro il 2030 saremo carbon neutral") sono illeciti se non accompagnati da piano chiaro, misurabile, verificabile e reso pubblico.
- Claim comparativi ambientali (es. "più sostenibile di X") richiedono prove documentate e metodo di confronto trasparente.

Codice del Consumo (D.Lgs. 206/2005 e successive modificazioni):
- Art. 21 (Azioni ingannevoli): vietate affermazioni false o idonee a indurre in errore anche per omissione, incluse quelle su caratteristiche ambientali o sociali del prodotto.
- Art. 22 (Omissioni rilevanti): omettere informazioni decisive che modificherebbero la scelta del consumatore medio è pratica commerciale scorretta.
- Art. 23 lett. (a): sono in ogni caso ingannevoli le affermazioni di aderenza a un codice di condotta che il professionista non rispetta.
- Sanzioni AGCM fino a 10 milioni di euro per pratiche commerciali scorrette; per violazioni di claim ambientali sanzionate ai sensi del D.Lgs. 162/2024, fino al 4% del fatturato annuo.

Applicazione pratica per i testi Pantaleo:
- "Naturale" come claim generico è potenzialmente fuorviante — non usare isolato; se necessario, ancorare a certificazione specifica (es. "biologico certificato ICEA").
- "Sostenibile" o "ecologico" solo con riferimento esplicito a pratica documentata (es. "agricoltura biologica certificata", "150 ettari coltivati senza pesticidi di sintesi").
- Le certificazioni Biologico ICEA, IGP, ISO 9001, Kosher, Halal sono claim legittimi — citarle sempre correttamente senza estenderle a prodotti non certificati.
- Non usare "a km zero", "a basso impatto", "green" o simili senza prova."""


class VerifyRequest(BaseModel):
    formato: str
    prodotti: list[str]
    contenuto: str


class ProposeRequest(BaseModel):
    tipo: str
    testo: str


def _load_proposals() -> list:
    if PROPOSALS_FILE.exists():
        try:
            return json.loads(PROPOSALS_FILE.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []


def _save_proposals(data: list) -> None:
    PROPOSALS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


@app.get("/", response_class=HTMLResponse)
async def index():
    html_path = Path("static/index.html")
    if not html_path.exists():
        raise HTTPException(status_code=404, detail="index.html not found")
    return HTMLResponse(content=html_path.read_text(encoding="utf-8"))


@app.post("/verify")
async def verify(req: VerifyRequest):
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY non configurata")

    if not req.contenuto.strip():
        raise HTTPException(status_code=400, detail="Il contenuto non può essere vuoto")

    prodotti_str = ", ".join(req.prodotti) if req.prodotti else "non specificato"
    user_message = (
        f"Formato: {req.formato}\n"
        f"Prodotti: {prodotti_str}\n\n"
        f"Contenuto da verificare:\n{req.contenuto}"
    )

    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_message}],
        )
        raw = message.content[0].text.strip()
        result = json.loads(raw)
        return JSONResponse(content=result)
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=502,
            detail="Risposta del modello non valida. Riprova.",
        )
    except anthropic.AuthenticationError:
        raise HTTPException(status_code=401, detail="ANTHROPIC_API_KEY non valida")
    except anthropic.RateLimitError:
        raise HTTPException(status_code=429, detail="Limite API raggiunto. Riprova tra poco.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante la verifica: {str(e)}")


@app.post("/propose")
async def propose(req: ProposeRequest):
    if not req.testo.strip():
        raise HTTPException(status_code=400, detail="Il testo della proposta non può essere vuoto")

    proposals = _load_proposals()
    proposals.append(
        {
            "tipo": req.tipo,
            "testo": req.testo,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    )
    _save_proposals(proposals)
    return {"ok": True, "total": len(proposals)}
