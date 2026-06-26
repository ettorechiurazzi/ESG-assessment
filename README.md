# Pantaleo Brand Checker

Web app per la verifica della coerenza dei contenuti di comunicazione rispetto alla brand identity di **Nicola Pantaleo S.p.A.**

Uso interno — team comunicazione Véritable srl SB.

## Stack

- **Backend**: Python 3.11 + FastAPI
- **Frontend**: HTML/CSS/JS vanilla (nessuna dipendenza esterna)
- **AI**: Anthropic API (claude-sonnet-4-6)
- **Deploy**: Railway

## Funzionalità

- Selezione formato contenuto (Post social, Ads, Blog post, ecc.)
- Selezione multipla prodotti Pantaleo
- Analisi AI su 5 dimensioni: posizionamento, claim, tono di voce, impieghi, accuratezza fattuale
- Verdict colorato (ok / warn / fail) con card dettagliate per dimensione
- Proposta aggiornamenti alla knowledge base (salvate in `proposals.json`)

## Setup locale

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Crea .env
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

uvicorn main:app --reload
# → http://localhost:8000
```

## Deploy Railway

1. Crea progetto su [railway.app](https://railway.app)
2. Collega il repository GitHub
3. Aggiungi variabile d'ambiente `ANTHROPIC_API_KEY`
4. Il deploy parte automaticamente

## Variabili d'ambiente

| Variabile | Obbligatoria | Descrizione |
|-----------|-------------|-------------|
| `ANTHROPIC_API_KEY` | Sì | Chiave API Anthropic |
| `PORT` | No (Railway la imposta) | Porta del server |
