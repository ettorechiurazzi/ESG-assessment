from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ─── Brand palette ───────────────────────────────────────────────────────────
NAVY       = RGBColor(0x0D, 0x2B, 0x55)   # deep water blue — backgrounds
TEAL       = RGBColor(0x00, 0x7A, 0x87)   # teal — accents / headings
AQUA       = RGBColor(0x4F, 0xC3, 0xD4)   # light aqua — highlights
SAND       = RGBColor(0xF5, 0xF0, 0xE8)   # warm sand — light bg
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
CHARCOAL   = RGBColor(0x2C, 0x2C, 0x2C)
RED_TAG    = RGBColor(0xC0, 0x39, 0x2B)
YELLOW_TAG = RGBColor(0xE6, 0x7E, 0x22)
GREEN_TAG  = RGBColor(0x27, 0xAE, 0x60)
STAR_TAG   = RGBColor(0xF3, 0x9C, 0x12)
PURPLE_TAG = RGBColor(0x7D, 0x3C, 0x98)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # completely blank


# ─── Helpers ─────────────────────────────────────────────────────────────────

def bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = color

def box(slide, l, t, w, h, color, alpha=None):
    shape = slide.shapes.add_shape(1, Inches(l), Inches(t), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape

def txt(slide, text, l, t, w, h,
        size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT,
        italic=False, wrap=True):
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = wrap
    tf = txb.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txb

def multiline(slide, lines, l, t, w, h,
              size=16, color=WHITE, bold_first=False, line_spacing=None):
    """lines = list of (text, bold, color_override)"""
    txb = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    txb.word_wrap = True
    tf = txb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(lines):
        if isinstance(item, str):
            text, b, col = item, False, color
        else:
            text = item[0]
            b    = item[1] if len(item) > 1 else False
            col  = item[2] if len(item) > 2 else color
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        if line_spacing:
            p.line_spacing = Pt(line_spacing)
        run = p.add_run()
        run.text = text
        run.font.size = Pt(size)
        run.font.bold = b or (bold_first and i == 0)
        run.font.color.rgb = col


def score_bar(slide, label, score, max_score, l, t, bar_w=6.0):
    """Draw a labelled progress bar."""
    txt(slide, label, l, t, 4.0, 0.35, size=13, color=CHARCOAL, bold=False)
    box(slide, l + 4.1, t + 0.05, bar_w, 0.28, RGBColor(0xDD,0xDD,0xDD))
    fill_w = bar_w * (score / max_score)
    col = GREEN_TAG if score >= 3 else (YELLOW_TAG if score >= 2 else RED_TAG)
    box(slide, l + 4.1, t + 0.05, fill_w, 0.28, col)
    txt(slide, f"{score}/{max_score}", l + 4.1 + bar_w + 0.1, t + 0.02,
        0.5, 0.35, size=12, color=CHARCOAL, bold=True)


def tier_box(slide, tier, l, t):
    colors = {"A": TEAL, "B": YELLOW_TAG, "C": PURPLE_TAG, "★": STAR_TAG}
    labels = {"A": "TIER A", "B": "TIER B", "C": "TIER C", "★": "ACQUA AMATA"}
    col = colors.get(tier, YELLOW_TAG)
    lbl = labels.get(tier, tier)
    w = 1.5 if tier == "★" else 1.1
    box(slide, l, t, w, 0.3, col)
    txt(slide, lbl, l + 0.05, t + 0.02, w - 0.1, 0.28, size=9, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, NAVY)
box(s, 0, 0, 13.33, 1.2, TEAL)
txt(s, "ESG QUICK ASSESSMENT", 0.5, 0.25, 12, 0.7,
    size=14, bold=True, color=AQUA, align=PP_ALIGN.LEFT)

box(s, 0, 1.2, 0.12, 6.3, AQUA)
txt(s, "Acqua Amata", 0.4, 1.5, 12, 1.2,
    size=54, bold=True, color=WHITE)
txt(s, "Società Benefit pugliese — Brand ESG Assessment", 0.4, 2.9, 10, 0.6,
    size=20, color=AQUA, italic=True)

multiline(s, [
    ("Settore: Acqua minerale oligominerale — GDO, HORECA, Vending", False, RGBColor(0xCC,0xDD,0xFF)),
    ("Sede: Casamassima (BA) — Castello S.r.l., distribuzione nazionale", False, RGBColor(0xCC,0xDD,0xFF)),
    ("Data analisi: Luglio 2026", False, RGBColor(0xCC,0xDD,0xFF)),
], l=0.4, t=3.6, w=10, h=1.2, size=15, color=RGBColor(0xCC,0xDD,0xFF))

box(s, 0, 6.5, 13.33, 1.0, RGBColor(0x08,0x1E,0x3F))
txt(s, "Confidenziale — Solo uso interno · Basato su ricerca pubblica, confidence 5/10", 0.4, 6.6, 12.4, 0.4,
    size=11, color=RGBColor(0x88,0x99,0xBB), italic=True)
txt(s, "13 / 30", 11.5, 6.55, 1.5, 0.45,
    size=20, bold=True, color=AQUA, align=PP_ALIGN.RIGHT)
txt(s, "Score complessivo", 9.5, 6.62, 2.0, 0.35,
    size=10, color=RGBColor(0x88,0x99,0xBB), align=PP_ALIGN.RIGHT)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — AGENDA
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, NAVY)
txt(s, "Agenda", 0.5, 0.2, 12, 0.7, size=32, bold=True, color=WHITE)

items = [
    ("01", "Snapshot del Brand"),
    ("02", "Analisi ESG — E / S / G"),
    ("03", "Gap di Comunicazione e Percezione"),
    ("04", "Benchmark Competitivo — Lista HORECA/GDO"),
    ("05", "Raccomandazioni Strategiche"),
    ("06", "Scorecard Finale"),
]
for i, (num, label) in enumerate(items):
    row = i % 3
    col = i // 3
    lx = 0.6 + col * 6.5
    ty = 1.5 + row * 1.5
    box(s, lx, ty, 0.7, 0.7, TEAL)
    txt(s, num, lx, ty + 0.1, 0.7, 0.5, size=20, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, label, lx + 0.85, ty + 0.15, 5.0, 0.5,
        size=18, bold=True, color=NAVY)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — SNAPSHOT DEL BRAND
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, NAVY)
txt(s, "01 — Snapshot del Brand", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)

box(s, 0.4, 1.3, 5.8, 5.7, WHITE)
box(s, 0.4, 1.3, 5.8, 0.55, TEAL)
txt(s, "Chi è Acqua Amata", 0.55, 1.38, 5.5, 0.45,
    size=14, bold=True, color=WHITE)

facts = [
    "💧  Fonte scoperta nel 1990 (G.A. Mazzone) — Casamassima/Adelfia (BA)",
    "📅  Riconoscimento acqua minerale 1998 — imbottigliata dal 2001",
    "🏭  Società operativa: Castello S.r.l. — Società Benefit dal 2024",
    "🏢  Gruppo: MGA Group (dal 2021) — [Non verificato]",
    "🛒  Canali: GDO, Vending, HORECA — anche private label",
    "♻️   Packaging: PET 100% riciclabile dal 2001, R-PET dal 2019",
    "📈  Volumi: ~100M bottiglie/anno (2021) → target 500M entro 2027",
    "💶  Investimento dichiarato: 20 mln € nello stabilimento",
    "🏆  Forbes 100 Eccellenze 2021, Leader Crescita 2026 (Sole24Ore)",
]
multiline(s, facts, l=0.55, t=2.0, w=5.5, h=4.8,
          size=12, color=CHARCOAL, line_spacing=17)

box(s, 6.7, 1.3, 6.2, 2.6, NAVY)
txt(s, 'Società Benefit', 6.9, 1.5, 5.8, 0.7,
    size=30, bold=True, color=AQUA, align=PP_ALIGN.CENTER)
txt(s, "Doppio scopo di legge: profitto + beneficio comune —\nasset legale, non solo comunicativo, dal 2024",
    6.9, 2.3, 5.8, 0.9, size=14, color=WHITE, align=PP_ALIGN.CENTER)

box(s, 6.7, 4.1, 6.2, 2.9, WHITE)
box(s, 6.7, 4.1, 6.2, 0.45, AQUA)
txt(s, "Tensione strategica ESG", 6.85, 4.16, 5.8, 0.4,
    size=13, bold=True, color=NAVY)
multiline(s, [
    "✅  Crescita commerciale ben comunicata (premi, stampa)",
    "⚠️   Performance ESG quasi interamente self-reported",
    "💡  Nessun audit terzo sui claim ambientali reperito",
], l=6.85, t=4.65, w=5.9, h=2.0, size=13, color=CHARCOAL, line_spacing=20)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — ESG: ENVIRONMENTAL
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, GREEN_TAG)
txt(s, "02 — Analisi ESG  |  E — Environmental", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)
box(s, 10.5, 0.15, 2.5, 0.75, RGBColor(0x1D,0x8A,0x48))
txt(s, "🟡  PARTIAL", 10.55, 0.22, 2.4, 0.55,
    size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

box(s, 0.4, 1.3, 6.0, 5.7, WHITE)
box(s, 0.4, 1.3, 6.0, 0.5, GREEN_TAG)
txt(s, "✅  Cosa c'è (self-reported)", 0.55, 1.36, 5.7, 0.4, size=13, bold=True, color=WHITE)
multiline(s, [
    "• Certificazione ISO 14001 — dichiarata dal 2001",
    "• Certificazione IFS FOOD — dichiarata dal 2018",
    "• Fotovoltaico: -542 t CO2/anno dichiarate",
    "• Target aziendale: -25% emissioni entro il 2026",
    "• Packaging PET 100% riciclabile dal 2001",
    "• Linea R-PET introdotta dal 2019",
    "• 100% energia da rinnovabili in stabilimento (claim)",
    "• Recupero 99% dei rifiuti (claim)",
], l=0.55, t=1.95, w=5.8, h=4.8, size=12, color=CHARCOAL, line_spacing=17)

box(s, 6.9, 1.3, 6.0, 5.7, WHITE)
box(s, 6.9, 1.3, 6.0, 0.5, RED_TAG)
txt(s, "❌  Cosa manca (pubblicamente)", 7.05, 1.36, 5.7, 0.4,
    size=13, bold=True, color=WHITE)
multiline(s, [
    "• Nessun audit terzo indipendente sui claim ambientali",
    "• % esatta di R-PET nella gamma corrente: non disponibile",
    "• ISO 9001, ISO 22000, BRC, biologico: dato non trovato",
    "• Nessun dato su prelievi/bilancio idrogeologico della falda",
    "• Nessun KPI ambientale in formato bilancio strutturato",
    "• Nessuna verifica indipendente su -25% CO2 2026",
], l=7.05, t=1.95, w=5.8, h=4.8, size=12, color=CHARCOAL, line_spacing=17)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — ESG: SOCIAL
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, TEAL)
txt(s, "02 — Analisi ESG  |  S — Social", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)
box(s, 10.5, 0.15, 2.5, 0.75, RGBColor(0x1A,0x3A,0x7A))
txt(s, "🟡  PARTIAL", 10.55, 0.22, 2.4, 0.55,
    size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

cards = [
    ("🏆 Riconoscimenti di stampa/settore",
     "Forbes 100 Eccellenze (2021) · Prodotto dell'Anno 2022 · Industria Felix\nLeader Crescita 2026 e Stelle del Sud 2024 (Sole 24 Ore/Statista)"),
    ("⚽ Sponsorizzazioni territoriali",
     "Radionorba Vodafone Battiti Live! (dal 2017)\nMain sponsor SSC Bari (almeno stagione 2022/23)"),
    ("📱 Presenza Social",
     "Instagram ~13.000 follower · Facebook ~16.500 \"mi piace\"\nLinkedIn ~4.400 follower (11-50 dipendenti dichiarati) · TikTok presente"),
    ("⚠️ Lacuna sociale",
     "Nessun dato pubblico su condizioni di lavoro, welfare,\ndiversità/inclusione o relazioni con la comunità locale"),
]
for i, (title, body) in enumerate(cards):
    col = i % 2
    row = i // 2
    lx = 0.4 + col * 6.5
    ty = 1.3 + row * 2.8
    box(s, lx, ty, 6.1, 2.5, WHITE)
    box(s, lx, ty, 6.1, 0.5, TEAL)
    txt(s, title, lx + 0.15, ty + 0.08, 5.8, 0.4,
        size=13, bold=True, color=WHITE)
    txt(s, body, lx + 0.15, ty + 0.65, 5.8, 1.7,
        size=12, color=CHARCOAL, wrap=True)

box(s, 0.4, 6.9, 12.5, 0.4, RGBColor(0xFF,0xF3,0xCD))
txt(s, "⚠️  I premi ottenuti certificano crescita/notorietà commerciale, non performance ESG in senso proprio",
    0.55, 6.93, 12.2, 0.35, size=11, color=CHARCOAL, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — ESG: GOVERNANCE
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, NAVY)
txt(s, "02 — Analisi ESG  |  G — Governance", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)
box(s, 10.5, 0.15, 2.5, 0.75, RGBColor(0x1A,0x3A,0x7A))
txt(s, "🟡  PARTIAL", 10.55, 0.22, 2.4, 0.55,
    size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

cols_data = [
    ("✅ Cosa c'è", GREEN_TAG, [
        "Società Benefit dal 2024 — asset",
        "legale vincolante, non solo comunicativo",
        "Investimento dichiarato 18 mln €",
        "(2024) per innovazione/sostenibilità",
        "Presidente CdA: Maria Mazzone",
        "Governance familiare stabile",
        "(famiglia Mazzone/Avella)",
    ]),
    ("⚠️ Incertezze", YELLOW_TAG, [
        "Ruolo Matteo Avella discordante:",
        "\"AD\" (stampa) vs \"Vicepresidente\"",
        "(LinkedIn) — non risolto",
        "Relazione d'impatto Società Benefit:",
        "non reperita pubblicamente",
        "Rapporto con MGA Group:",
        "non verificato su fonte primaria",
    ]),
    ("❌ Assente", RED_TAG, [
        "Bilancio di sostenibilità formale",
        "Codice etico pubblico",
        "Organigramma management pubblico",
        "Policy su conflitti di interesse",
        "Dati camerali completi (capitale",
        "sociale, composizione CdA)",
    ]),
]
for i, (title, col, items) in enumerate(cols_data):
    lx = 0.4 + i * 4.3
    box(s, lx, 1.3, 4.1, 5.7, WHITE)
    box(s, lx, 1.3, 4.1, 0.5, col)
    txt(s, title, lx + 0.12, 1.36, 3.9, 0.4,
        size=13, bold=True, color=WHITE)
    multiline(s, items, l=lx + 0.12, t=1.95,
              w=3.9, h=4.8, size=12, color=CHARCOAL, line_spacing=17)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — GAP DI COMUNICAZIONE
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, PURPLE_TAG)
txt(s, "03 — Gap di Comunicazione e Percezione", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)

gaps = [
    ("GAP 1", "Crescita comunicata, ESG poco misurabile",
     "Premi e classifiche (Leader Crescita, Stelle del Sud, Industria Felix)\n"
     "certificano fatturato/volumi, non performance ambientali o sociali.\n"
     "→ Rischio: comunicare 'successo' senza KPI ESG verificabili."),
    ("GAP 2", "Cifre finanziarie non riconciliate",
     "Fonti di stampa riportano fatturati incoerenti (7,7 mln 2021;\n"
     "9,2 mln Castello 2023; +43% 2021-24; +45% 2023 vs 2019).\n"
     "→ Mina la credibilità di qualunque KPI ESG relativo."),
    ("GAP 3", "Assenza di bilancio di sostenibilità formale",
     "Target dichiarati (-25% CO2 2026) e investimenti (18 mln €)\n"
     "senza un documento GRI/VSME o relazione d'impatto strutturata.\n"
     "→ Nessun KPI verificabile con metodologia riconosciuta."),
    ("GAP 4", "Ambiguità di governance",
     "Ruolo di Matteo Avella discordante tra fonti (AD vs Vicepresidente).\n"
     "Segnale minore ma reale di comunicazione societaria non coerente.\n"
     "→ Da correggere per credibilità verso stakeholder finanziari/ESG."),
]
for i, (num, title, body) in enumerate(gaps):
    col = i % 2
    row = i // 2
    lx = 0.4 + col * 6.5
    ty = 1.3 + row * 2.8
    box(s, lx, ty, 6.1, 2.6, WHITE)
    box(s, lx, ty, 0.9, 2.6, PURPLE_TAG)
    txt(s, num, lx + 0.05, ty + 0.9, 0.8, 0.4,
        size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, title, lx + 1.05, ty + 0.1, 4.9, 0.45,
        size=14, bold=True, color=NAVY)
    txt(s, body, lx + 1.05, ty + 0.65, 4.9, 1.85,
        size=11, color=CHARCOAL, wrap=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — BENCHMARK COMPETITIVO (tabella)
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, TEAL)
txt(s, "04 — Benchmark Competitivo — Lista Proposta HORECA/GDO", 0.5, 0.2, 12, 0.7,
    size=22, bold=True, color=WHITE)

headers = ["Competitor", "Tier", "Canali", "Nota ESG"]
col_w   = [2.6, 1.3, 2.8, 5.5]
col_x   = [0.2]
for w in col_w[:-1]:
    col_x.append(col_x[-1] + w + 0.05)

for j, (h, w, x) in enumerate(zip(headers, col_w, col_x)):
    box(s, x, 1.15, w, 0.42, NAVY)
    txt(s, h, x + 0.05, 1.2, w - 0.1, 0.35,
        size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

rows = [
    ("Acqua Amata ★", "★", "GDO + Vending + HORECA",
     "Società Benefit (2024); dati ESG self-reported, no audit terzo"),
    ("Acqua Orsini", "A", "GDO + HORECA (espansione)",
     "Uso misurato falde, rinnovabili; certificazioni non verificate"),
    ("Gaudianello", "A", "GDO + HORECA",
     "ISO 9001/14001/22000; filiera agricola bio certificata ICEA"),
    ("Fonte Cutolo Rionero", "A", "GDO + HORECA",
     "Marchio storico lucano, rilanciato da San Benedetto"),
    ("Fonte Margherita 1845", "A", "HORECA + porta a porta",
     "Packaging brick eco-sostenibile oltre al vetro"),
    ("Lete", "B", "GDO + HORECA + porta a porta",
     "Energia 100% verde dal 2004 (RECS); socio fondatore Coripet"),
    ("Ferrarelle", "B", "GDO + HORECA (linee dedicate)",
     "Società Benefit dal 2021; impianto proprio riciclo PET >27 mln €"),
    ("San Benedetto", "B", "GDO + HORECA (leader volume)",
     "Linea Ecogreen 100% RPET; bilancio di sostenibilità pubblicato"),
    ("Acqua Sant'Anna", "C", "GDO (leader) + HORECA",
     "Bottiglia Bio in PLA; decarbonizzazione logistica"),
    ("San Bernardo", "C", "GDO + HORECA",
     "Obiettivo \"Impatto Zero\" 2026; #1 test Gambero Rosso 2023"),
    ("Uliveto / Rocchetta", "C", "GDO + HORECA",
     "Garanzia di Origine per energia 100% solare (2024/25)"),
    ("Lauretana", "C", "GDO + HORECA premium",
     "EcoVadis Argento → Oro → Platino (anni non tutti certi)"),
]

for i, (name, tier, canali, nota) in enumerate(rows):
    ty = 1.62 + i * 0.465
    is_amata = tier == "★"
    bg_c = RGBColor(0xE8,0xF4,0xE8) if is_amata else (
           WHITE if i % 2 == 0 else RGBColor(0xF5,0xF5,0xF5))
    box(s, col_x[0], ty, col_w[0], 0.44, bg_c)
    txt(s, name, col_x[0] + 0.08, ty + 0.06, col_w[0] - 0.12, 0.34,
        size=11, bold=is_amata, color=NAVY)
    box(s, col_x[1], ty, col_w[1], 0.44, bg_c)
    tier_box(s, tier, col_x[1] + (0.1 if not is_amata else 0.0), ty + 0.08)
    box(s, col_x[2], ty, col_w[2], 0.44, bg_c)
    txt(s, canali, col_x[2] + 0.08, ty + 0.07, col_w[2] - 0.12, 0.32,
        size=10, color=CHARCOAL)
    box(s, col_x[3], ty, col_w[3], 0.44, bg_c)
    txt(s, nota, col_x[3] + 0.08, ty + 0.05, col_w[3] - 0.12, 0.36,
        size=10, color=CHARCOAL, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — RACCOMANDAZIONI: QUICK WINS
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, GREEN_TAG)
txt(s, "05 — Raccomandazioni  |  Quick Wins  (<6 mesi)", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)

qws = [
    ("QW 1", "Riconciliare le Cifre Finanziarie",
     "Pubblicare fatturato e volumi coerenti in un'unica\n"
     "fonte ufficiale (sito, comunicati), per eliminare le\n"
     "discrepanze già rilevate dalla stampa di settore.\n"
     "→ Costo: basso | Impatto: credibilità verso stakeholder",
     "< 3 mesi"),
    ("QW 2", "Certificati Online e Verificabili",
     "Pubblicare i certificati ISO 14001 e IFS FOOD con\n"
     "link diretto all'ente certificatore, non solo menzione\n"
     "testuale sul sito aziendale.\n"
     "→ Costo: basso | Impatto: immediato su buyer GDO",
     "< 3 mesi"),
    ("QW 3", "Chiarire i Ruoli di Governance",
     "Comunicare pubblicamente in modo univoco la\n"
     "composizione del CdA e i ruoli (es. Matteo Avella),\n"
     "eliminando le discordanze tra fonti.\n"
     "→ Costo: basso | Impatto: credibilità istituzionale",
     "< 6 mesi"),
]
for i, (num, title, body, timing) in enumerate(qws):
    lx = 0.3 + i * 4.35
    box(s, lx, 1.3, 4.1, 5.9, WHITE)
    box(s, lx, 1.3, 4.1, 0.5, GREEN_TAG)
    box(s, lx + 2.8, 1.35, 1.2, 0.38, RGBColor(0x1D,0x6A,0x3E))
    txt(s, timing, lx + 2.82, 1.37, 1.16, 0.34,
        size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, num, lx + 0.1, 1.36, 0.7, 0.38,
        size=13, bold=True, color=WHITE)
    txt(s, title, lx + 0.1, 1.92, 3.9, 0.5,
        size=14, bold=True, color=NAVY)
    txt(s, body, lx + 0.1, 2.55, 3.9, 4.5,
        size=11, color=CHARCOAL, wrap=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — RACCOMANDAZIONI: STRATEGIC GAPS + DIFFERENZIAZIONE
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, NAVY)
txt(s, "05 — Raccomandazioni  |  Strategic Gaps + Differenziazione", 0.5, 0.2, 12, 0.7,
    size=24, bold=True, color=WHITE)

sgs = [
    ("SG 1", "Relazione d'Impatto da Società Benefit", "12–24 mesi",
     "Prima relazione di impatto con KPI E/S/G misurabili,\n"
     "coerente con l'obbligo di legge italiano per le Società Benefit\n"
     "→ Trasforma lo status legale in narrativa verificabile"),
    ("SG 2", "Bilancio di Sostenibilità Formale (GRI/VSME)", "18–24 mesi",
     "Standard GRI o VSME (PMI-friendly, EFRAG/CSRD)\n"
     "Prioritario vista la crescita dichiarata 100M→500M bottiglie/anno\n"
     "→ Requisito emergente nei tender dei buyer GDO"),
    ("SG 3", "Audit Terzo sui Claim Ambientali", "12–18 mesi",
     "Verifica indipendente di fotovoltaico, target -25% CO2,\n"
     "% RPET e recupero rifiuti, oggi solo auto-dichiarati\n"
     "→ Trasforma i claim aziendali in dati certificati"),
]
for i, (num, title, timing, body) in enumerate(sgs):
    ty = 1.3 + i * 1.85
    box(s, 0.3, ty, 8.5, 1.7, WHITE)
    box(s, 0.3, ty, 0.7, 1.7, NAVY)
    txt(s, num, 0.3, ty + 0.55, 0.7, 0.5,
        size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, title, 1.1, ty + 0.08, 5.5, 0.45,
        size=14, bold=True, color=NAVY)
    box(s, 6.7, ty + 0.1, 1.95, 0.38, NAVY)
    txt(s, timing, 6.72, ty + 0.12, 1.9, 0.34,
        size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(s, body, 1.1, ty + 0.62, 7.5, 1.0,
        size=11, color=CHARCOAL, wrap=True)

box(s, 9.1, 1.3, 3.9, 5.55, NAVY)
box(s, 9.1, 1.3, 3.9, 0.55, AQUA)
txt(s, "💡 Differenziazione", 9.2, 1.35, 3.7, 0.45,
    size=13, bold=True, color=NAVY)
txt(s, '"Doppio Scopo\ndi Legge"', 9.2, 2.0, 3.6, 1.0,
    size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s,
    "Tra i competitor del panel,\n"
    "solo Ferrarelle condivide lo\n"
    "status di Società Benefit.\n\n"
    "→ Narrativa costruita su un\n"
    "   obbligo di legge, non solo\n"
    "   un claim di marketing.\n\n"
    "→ Rilevante sia per buyer GDO\n"
    "   sia per il canale HORECA\n"
    "   sostenibile.",
    9.2, 3.1, 3.7, 3.6, size=11, color=AQUA, wrap=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — SCORECARD FINALE
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, NAVY)
box(s, 0, 0, 13.33, 1.1, TEAL)
txt(s, "06 — Scorecard Finale", 0.5, 0.2, 12, 0.7,
    size=32, bold=True, color=WHITE)

dimensions = [
    ("Identity–Communication Alignment", 2, 5,
     "Crescita ben comunicata; ESG sostanzialmente self-reported"),
    ("ESG Coverage — Environmental", 2, 5,
     "Certificazioni e target dichiarati, nessun audit terzo reperito"),
    ("ESG Coverage — Social", 2, 5,
     "Radicamento territoriale forte; assenza dati su lavoro/persone"),
    ("ESG Coverage — Governance", 2, 5,
     "Società Benefit è asset reale; opacità su ruoli CdA e dati camerali"),
    ("Communication–Perception Gap", 2, 5,
     "Cifre finanziarie incongruenti tra fonti di stampa"),
    ("Competitor Positioning", 3, 5,
     "Ben posizionata su crescita; dietro a Ferrarelle/San Bernardo su ESG"),
]
for i, (dim, score, mx, note) in enumerate(dimensions):
    ty = 1.25 + i * 0.88
    txt(s, dim, 0.4, ty, 4.5, 0.45, size=13, bold=True, color=WHITE)
    box(s, 5.0, ty + 0.08, 4.5, 0.3, RGBColor(0x1A,0x40,0x70))
    fill = 4.5 * score / mx
    col = GREEN_TAG if score >= 3 else (YELLOW_TAG if score >= 2 else RED_TAG)
    box(s, 5.0, ty + 0.08, fill, 0.3, col)
    txt(s, f"{score}/{mx}", 9.6, ty + 0.05, 0.6, 0.38,
        size=14, bold=True, color=col, align=PP_ALIGN.CENTER)
    txt(s, note, 10.3, ty + 0.05, 2.8, 0.42,
        size=10, color=AQUA, italic=True, wrap=True)

box(s, 0.3, 6.55, 12.7, 0.75, TEAL)
txt(s, "SCORE TOTALE", 0.6, 6.65, 4.0, 0.55,
    size=18, bold=True, color=WHITE)
txt(s, "13 / 30", 5.0, 6.58, 3.0, 0.65,
    size=28, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "Buona base di crescita — ESG ancora da strutturare e certificare",
    8.2, 6.68, 4.6, 0.5, size=12, color=WHITE, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — CLOSING / NEXT STEPS
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, NAVY)
box(s, 0, 0, 13.33, 1.2, TEAL)
txt(s, "Prossimi Passi — Roadmap ESG", 0.5, 0.25, 12, 0.7,
    size=28, bold=True, color=WHITE)

phases = [
    ("FASE 1", "< 3 mesi", AQUA, [
        "Riconciliare cifre finanziarie pubbliche",
        "Pubblicare certificati verificabili online",
        "Chiarire pubblicamente i ruoli di CdA",
    ]),
    ("FASE 2", "3–18 mesi", GREEN_TAG, [
        "Audit terzo sui claim ambientali",
        "Prima relazione d'impatto Società Benefit",
        "KPI pubblici sulla crescita produttiva",
        "(100M → 500M bottiglie/anno)",
    ]),
    ("FASE 3", "18–36 mesi", TEAL, [
        "Bilancio di sostenibilità formale (GRI/VSME)",
        "Certificazioni aggiuntive (ISO 9001/22000)",
        "Narrativa strutturata sul \"doppio scopo\"",
        "di legge come Società Benefit",
    ]),
]
for i, (phase, timing, col, items) in enumerate(phases):
    lx = 0.4 + i * 4.3
    box(s, lx, 1.4, 4.0, 5.7, RGBColor(0x08,0x1E,0x3F))
    box(s, lx, 1.4, 4.0, 0.8, col)
    txt(s, phase, lx + 0.1, 1.45, 2.0, 0.42,
        size=16, bold=True, color=NAVY if col == AQUA else WHITE)
    txt(s, timing, lx + 2.1, 1.5, 1.8, 0.35,
        size=13, color=NAVY if col == AQUA else WHITE,
        align=PP_ALIGN.RIGHT, italic=True)
    multiline(s, [f"• {it}" for it in items],
              l=lx + 0.15, t=2.35, w=3.7, h=4.5,
              size=13, color=WHITE, line_spacing=22)

box(s, 0.3, 6.55, 12.7, 0.75, RGBColor(0x08,0x1E,0x3F))
txt(s,
    '"Acqua Amata cresce più velocemente di quanto certifichi. Il compito dei prossimi 12 mesi è rendere l\'ESG misurabile."',
    0.5, 6.6, 12.4, 0.55, size=13, color=AQUA, italic=True, align=PP_ALIGN.CENTER)


# ─── Save ────────────────────────────────────────────────────────────────────
out = "/home/user/ESG-assessment/acqua-amata-esg-deck-ceo.pptx"
prs.save(out)
print(f"Saved: {out}")
