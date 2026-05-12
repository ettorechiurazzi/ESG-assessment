from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
import copy

# ─── Brand palette ───────────────────────────────────────────────────────────
NAVY       = RGBColor(0x0D, 0x2B, 0x55)   # deep ocean blue — backgrounds
TEAL       = RGBColor(0x00, 0x7A, 0x87)   # sea teal — accents / headings
AQUA       = RGBColor(0x4F, 0xC3, 0xD4)   # light aqua — highlights
SAND       = RGBColor(0xF5, 0xF0, 0xE8)   # warm sand — light bg
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
CHARCOAL   = RGBColor(0x2C, 0x2C, 0x2C)
RED_TAG    = RGBColor(0xC0, 0x39, 0x2B)
YELLOW_TAG = RGBColor(0xE6, 0x7E, 0x22)
GREEN_TAG  = RGBColor(0x27, 0xAE, 0x60)
STAR_TAG   = RGBColor(0xF3, 0x9C, 0x12)

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
    # background bar
    box(slide, l + 4.1, t + 0.05, bar_w, 0.28, RGBColor(0xDD,0xDD,0xDD))
    # filled bar
    fill_w = bar_w * (score / max_score)
    col = GREEN_TAG if score >= 3 else (YELLOW_TAG if score >= 2 else RED_TAG)
    box(slide, l + 4.1, t + 0.05, fill_w, 0.28, col)
    txt(slide, f"{score}/{max_score}", l + 4.1 + bar_w + 0.1, t + 0.02,
        0.5, 0.35, size=12, color=CHARCOAL, bold=True)


def tag_box(slide, tag, l, t):
    colors = {"🔴": RED_TAG, "🟡": YELLOW_TAG, "🟢": GREEN_TAG, "⭐": STAR_TAG}
    labels = {"🔴": "ABSENT", "🟡": PARTIAL", "🟢": SOLID", "⭐": LEADER"}
    # find matching key
    col = YELLOW_TAG
    lbl = ""
    for k in colors:
        if k in tag:
            col = colors[k]
            lbl = labels[k]
            break
    b = box(slide, l, t, 1.1, 0.3, col)
    txt(slide, lbl, l + 0.05, t + 0.02, 1.0, 0.28, size=10, bold=True,
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
txt(s, "Mare Gioioso", 0.4, 1.5, 12, 1.2,
    size=54, bold=True, color=WHITE)
txt(s, "Fish Possible — Brand ESG Assessment per il CEO", 0.4, 2.9, 10, 0.6,
    size=20, color=AQUA, italic=True)

multiline(s, [
    ("Settore: Ittico — pesce fresco, lavorato, confezionato, GDO", False, RGBColor(0xCC,0xDD,0xFF)),
    ("Sede: Monopoli (BA) — distribuzione nazionale", False, RGBColor(0xCC,0xDD,0xFF)),
    ("Data analisi: Maggio 2026", False, RGBColor(0xCC,0xDD,0xFF)),
], l=0.4, t=3.6, w=9, h=1.2, size=15, color=RGBColor(0xCC,0xDD,0xFF))

box(s, 0, 6.5, 13.33, 1.0, RGBColor(0x08,0x1E,0x3F))
txt(s, "Confidenziale — Solo uso interno", 0.4, 6.6, 12, 0.4,
    size=11, color=RGBColor(0x88,0x99,0xBB), italic=True)
txt(s, "14 / 30", 11.5, 6.55, 1.5, 0.45,
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
    ("04", "Benchmark Competitivo"),
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

# Left column — facts
box(s, 0.4, 1.3, 5.8, 5.7, WHITE)
box(s, 0.4, 1.3, 5.8, 0.55, TEAL)
txt(s, "Chi è Mare Gioioso", 0.55, 1.38, 5.5, 0.45,
    size=14, bold=True, color=WHITE)

facts = [
    "🏭  Fondata 2016 — Sebastiano Gioioso (40 anni di esperienza)",
    "📍  HQ: Monopoli (BA) — 2 stabilimenti + Torre Canne (BR)",
    "🚢  70+ pescherecci in conferimento esclusivo",
    "⚖️   20.000+ tonnellate/anno movimentate",
    "🛒  ~80% fatturato da GDO",
    "🎣  Gamma: fresco, confezionato, Pronti a cuocere,",
    "      Antipasti di mare, Sushi ready-to-eat",
    "🍽️   Ristorante Porta De Mä — Chef stellato Angelo Sabatelli",
    "🏆  Gambero Rosso — Imprese Vincenti",
    "🌐  Tuttofood 2026 — Pad. 4, Stand L20",
]
multiline(s, facts, l=0.55, t=2.0, w=5.5, h=4.8,
          size=12, color=CHARCOAL, line_spacing=17)

# Right column — positioning
box(s, 6.7, 1.3, 6.2, 2.6, NAVY)
txt(s, '"Fish Possible"', 6.9, 1.5, 5.8, 0.7,
    size=32, bold=True, color=AQUA, align=PP_ALIGN.CENTER)
txt(s, "La promessa: qualità ittica accessibile,\ntracciabile, innovativa — radicata in Puglia",
    6.9, 2.3, 5.8, 0.9, size=14, color=WHITE, align=PP_ALIGN.CENTER)

box(s, 6.7, 4.1, 6.2, 2.9, WHITE)
box(s, 6.7, 4.1, 6.2, 0.45, AQUA)
txt(s, "Tensione strategica ESG", 6.85, 4.16, 5.8, 0.4,
    size=13, bold=True, color=NAVY)
multiline(s, [
    "✅  Base operativa solida (certificazioni, flotta, R&S)",
    "⚠️   Narrativa pubblica ESG assente o frammentata",
    "💡  Fa più di quanto racconta",
], l=6.85, t=4.65, w=5.9, h=2.0, size=13, color=CHARCOAL, line_spacing=20)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — ESG: ENVIRONMENTAL
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, GREEN_TAG)
txt(s, "02 — Analisi ESG  |  E — Environmental", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)

# Tag
box(s, 10.5, 0.15, 2.5, 0.75, RGBColor(0x1D,0x8A,0x48))
txt(s, "🟡  PARTIAL", 10.55, 0.22, 2.4, 0.55,
    size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# Left: what exists
box(s, 0.4, 1.3, 6.0, 5.7, WHITE)
box(s, 0.4, 1.3, 6.0, 0.5, GREEN_TAG)
txt(s, "✅  Cosa c'è", 0.55, 1.36, 5.7, 0.4, size=13, bold=True, color=WHITE)
multiline(s, [
    "• Certificazione MSC (pesca sostenibile) — Chain of Custody",
    "• Certificazione ASC (acquacoltura responsabile)",
    "• ISO 14001 — Sistema di Gestione Ambientale",
    "• Certificazione IFS Food — sicurezza di filiera",
    "• Centro depurazione molluschi Torre Canne",
    "  (14 vasche, tecnologia moderna)",
    "• Ami e palangari per pesce spada (tecnica selettiva)",
    "• Confezionamento in atmosfera modificata (MAP)",
    "  → riduzione sprechi / shelf life estesa",
], l=0.55, t=1.95, w=5.8, h=4.8, size=12, color=CHARCOAL, line_spacing=17)

# Right: what's missing
box(s, 6.9, 1.3, 6.0, 5.7, WHITE)
box(s, 6.9, 1.3, 6.0, 0.5, RED_TAG)
txt(s, "❌  Cosa manca (pubblicamente)", 7.05, 1.36, 5.7, 0.4,
    size=13, bold=True, color=WHITE)
multiline(s, [
    "• Nessun KPI ambientale pubblico",
    "  (emissioni CO₂, consumi energetici, scarti)",
    "• Flotta: zero comunicazione su consumo",
    "  carburante, emissioni, piani di transizione",
    "• Centro Torre Canne: nessun dato pubblico",
    "  su performance idrica o ambientale",
    "• Packaging: nessuna dichiarazione di",
    "  riciclabilità o materiali usati",
    "• Carbon footprint logistica: dato assente",
    "  (20.000 t/anno su scala nazionale)",
], l=7.05, t=1.95, w=5.8, h=4.8, size=12, color=CHARCOAL, line_spacing=17)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — ESG: SOCIAL
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, TEAL)
txt(s, "02 — Analisi ESG  |  S — Social", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)
box(s, 10.5, 0.15, 2.5, 0.75, RGBColor(0x00,0x5F,0x6B))
txt(s, "🟢  SOLID", 10.55, 0.22, 2.4, 0.55,
    size=20, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# 4 asset cards
cards = [
    ("🎓 Partnership Accademiche",
     "Unibo · Uniba (Vet. Med.) · ABAP Institute · ITS Agroalimentare Puglia\n→ R&S su qualità, sicurezza alimentare, trasferimento competenze"),
    ("🐟 Radicamento Territoriale",
     "70+ pescherecci pugliesi · porti: Monopoli, Mola, Brindisi, Otranto, Gallipoli\n→ Filiera corta, identità meridionale autentica"),
    ("🍽️ Porta De Mä — Ristorante Stellato",
     "Chef Angelo Sabatelli · Monopoli, Piazza Garibaldi\n→ Valorizzazione territorio + brand ambassador premium"),
    ("📱 Presenza Social",
     "Instagram @maregioioso: 4.419 follower, 852 post\nLinkedIn · Facebook (video pescherecci)\n→ Community attiva ma non orientata ESG"),
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

# Bottom note
box(s, 0.4, 6.9, 12.5, 0.4, RGBColor(0xFF,0xF3,0xCD))
txt(s, "⚠️  [Non verificato] Condizioni di lavoro a bordo dei pescherecci e welfare dipendenti: dato non disponibile pubblicamente",
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

# 3 columns
cols_data = [
    ("✅ Cosa c'è", GREEN_TAG, [
        "IFS Food — audit periodici di terza parte",
        "ISO 14001 — revisione processi ambientali",
        "Founder-led: governance chiara e stabile",
        "Presenza strutturata in fiere internazionali",
        "(Tuttofood, Seafood Summit)",
        "Certificazioni implicano Chain of Custody",
        "verificata da enti terzi accreditati",
    ]),
    ("⚠️ Rischi latenti", YELLOW_TAG, [
        "Dipendenza da 70 pescherecci terzi:",
        "nessun Supplier Code of Conduct pubblico",
        "Nessun audit dei conferenti comunicato",
        "Governance concentrata su singola figura",
        "(founder-CEO): successione non indirizzata",
        "Nessun advisory board ESG o",
        "responsabile sostenibilità dedicato",
    ]),
    ("❌ Assente", RED_TAG, [
        "Sustainability Report (nessuna edizione)",
        "Codice etico pubblico",
        "Organigramma management pubblico",
        "Policy su conflitti di interesse",
        "Bilancio certificato accessibile",
        "Metriche di governance pubblicate",
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
box(s, 0, 0, 13.33, 1.1, RGBColor(0x7D,0x3C,0x98))
txt(s, "03 — Gap di Comunicazione e Percezione", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)

gaps = [
    ("GAP 1", "L'Operativo non è Narrativa",
     "Certificazioni, partnership, tecniche selettive di pesca esistono ma non sono\n"
     "organizzate in un hub ESG pubblico. Il sito non ha sezione 'Sostenibilità'.\n"
     "→ Invisibili ai buyer GDO che usano scorecard ESG per i fornitori."),
    ("GAP 2", "La Flotta come Rischio non Gestito",
     "70 pescherecci terzi = principale punto di vulnerabilità reputazionale.\n"
     "Nessun codice di condotta, nessun audit dei conferenti comunicato.\n"
     "→ Silenzio su sicurezza a bordo, lavoro, conformità IUU."),
    ("GAP 3", "Social Media: Vetrina, non Dialogo ESG",
     "852 post Instagram, ma mix editoriale quasi tutto product-driven.\n"
     "Storie di pescatori, retroscena Torre Canne, pillole certificazioni: assenti.\n"
     "→ Opportunità non sfruttata con comunità già consolidata."),
    ("GAP 4", "Percezione Mediata Solo dalla Stampa di Settore",
     "Zero recensioni consumatore finale rilevate su piattaforme generaliste.\n"
     "L'identità ESG percepita si regge su fonti di parte (comunicati, trade press).\n"
     "→ Brand ESG fragile: nessuna comunità di stakeholder che lo valida."),
]
for i, (num, title, body) in enumerate(gaps):
    col = i % 2
    row = i // 2
    lx = 0.4 + col * 6.5
    ty = 1.3 + row * 2.8
    box(s, lx, ty, 6.1, 2.6, WHITE)
    box(s, lx, ty, 0.9, 2.6, RGBColor(0x7D,0x3C,0x98))
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
txt(s, "04 — Benchmark Competitivo — Panel Settore Ittico Italia", 0.5, 0.2, 12, 0.7,
    size=24, bold=True, color=WHITE)

# Table header
headers = ["Competitor", "E — Environ.", "S — Social", "G — Govern.", "Posizionamento"]
col_w   = [3.2, 2.0, 2.0, 2.0, 3.9]
col_x   = [0.2]
for w in col_w[:-1]:
    col_x.append(col_x[-1] + w + 0.05)

for j, (h, w, x) in enumerate(zip(headers, col_w, col_x)):
    box(s, x, 1.2, w, 0.45, NAVY)
    txt(s, h, x + 0.05, 1.25, w - 0.1, 0.38,
        size=12, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

# Table rows
rows = [
    ("Mare Gioioso ★",
     ("🟡", YELLOW_TAG), ("🟢", GREEN_TAG), ("🟡", YELLOW_TAG),
     "Base solida; narrativa ESG assente"),
    ("Nieddittas",
     ("⭐", STAR_TAG), ("🟢", GREEN_TAG), ("🟢", GREEN_TAG),
     "Leader ASC molluschi; TV campaign; wetland"),
    ("Cromaris",
     ("⭐", STAR_TAG), ("🟢", GREEN_TAG), ("⭐", STAR_TAG),
     "Sustainability Report CSRD; KPI misurabili"),
    ("Lepore Mare",
     ("🟢", GREEN_TAG), ("🟡", YELLOW_TAG), ("🟡", YELLOW_TAG),
     "Bontonno: palangari + packaging riciclabile"),
    ("Fiorital",
     ("🟡", YELLOW_TAG), ("🟡", YELLOW_TAG), ("🟡", YELLOW_TAG),
     "DYP anti-spreco; ESG complessiva generica"),
    ("Renna Srl",
     ("🟡", YELLOW_TAG), ("🟡", YELLOW_TAG), ("🟡", YELLOW_TAG),
     "Qualità premium; ESG generica"),
    ("Alles Fisch",
     ("🔴", RED_TAG), ("🔴", RED_TAG), ("🔴", RED_TAG),
     "B2B puro; nessuna comunicazione ESG"),
]
tag_lbl = {"🔴": "ABSENT", "🟡": "PARTIAL", "🟢": "SOLID", "⭐": "LEADER"}

for i, row in enumerate(rows):
    ty = 1.75 + i * 0.68
    bg_c = RGBColor(0xE8,0xF4,0xE8) if row[0].startswith("Mare") else (
           WHITE if i % 2 == 0 else RGBColor(0xF5,0xF5,0xF5))
    box(s, col_x[0], ty, col_w[0], 0.6, bg_c)
    txt(s, row[0], col_x[0] + 0.08, ty + 0.12, col_w[0] - 0.1, 0.4,
        size=12, bold=row[0].startswith("Mare"), color=NAVY)
    for k, (emoji, col) in enumerate([row[1], row[2], row[3]]):
        box(s, col_x[k+1], ty, col_w[k+1], 0.6, bg_c)
        box(s, col_x[k+1] + 0.3, ty + 0.12, 1.3, 0.35, col)
        txt(s, tag_lbl.get(emoji, ""), col_x[k+1] + 0.32, ty + 0.14,
            1.26, 0.32, size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    box(s, col_x[4], ty, col_w[4], 0.6, bg_c)
    txt(s, row[4], col_x[4] + 0.08, ty + 0.1, col_w[4] - 0.1, 0.45,
        size=11, color=CHARCOAL, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — RACCOMANDAZIONI: QUICK WINS
# ═══════════════════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
bg(s, SAND)
box(s, 0, 0, 13.33, 1.1, GREEN_TAG)
txt(s, "05 — Raccomandazioni  |  Quick Wins  (<6 mesi)", 0.5, 0.2, 12, 0.7,
    size=26, bold=True, color=WHITE)

qws = [
    ("QW 1", "Pagina Sostenibilità sul Sito",
     "Creare hub 'Sostenibilità' su maregioioso.it:\n"
     "• Certificazioni con logo ufficiali + link enti certificatori\n"
     "• Scheda centro Torre Canne con dati operativi\n"
     "• Partnership universitarie\n"
     "→ Costo: basso | Impatto: immediato su buyer GDO e stampa",
     "< 3 mesi"),
    ("QW 2", "Piano Editoriale ESG sui Social",
     "30% contenuti Instagram/Facebook orientati ESG:\n"
     "• Video pescatori a bordo (tecniche, sicurezza)\n"
     "• Retroscena centro depurazione Torre Canne\n"
     "• Pillole certificazioni, infografiche\n"
     "→ Formato: Reels | Costo: basso | Comunità già esistente",
     "< 6 mesi"),
    ("QW 3", "Fact Sheet KPI Ambientali Auto-dichiarati",
     "Comunicato stampa con primi dati concreti:\n"
     "• % prodotto certificato MSC/ASC\n"
     "• % packaging riciclabile\n"
     "• N. pescatori nella rete conferente\n"
     "• Tonnellate molluschi depurate/anno\n"
     "→ Rompe il pattern della comunicazione vaga",
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
    ("SG 1", "Sustainability Report Formale", "12–24 mesi",
     "Prima pubblicazione report (formato leggero, 20-30 pp)\n"
     "Standard: GRI o VSME (PMI-friendly, EFRAG)\n"
     "Focus prioritario: emissioni CO₂, energia, scarti\n"
     "→ Requisito emergente nei tender GDO (Coop, Esselunga, Carrefour)"),
    ("SG 2", "Supplier Code of Conduct per la Flotta", "12–18 mesi",
     "Codice vincolante per i 70 pescherecci conferenti:\n"
     "sicurezza ISM Code, divieto pesca IUU, selettività attrezzi,\n"
     "lavoro marittimo MLC 2006\n"
     "→ Trasforma dipendenza da vulnerabilità a punto di forza"),
    ("SG 3", "Carbon Footprint Logistica (Scope 3)", "18–36 mesi",
     "20.000 t/anno distribuite nazionalmente\n"
     "Partner: Bureau Veritas, DNV\n"
     "Identifica tratte ad alto impatto, ottimizzazione carichi\n"
     "→ Discriminante competitivo GDO entro 2027-28"),
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

# Differenziazione box
box(s, 9.1, 1.3, 3.9, 5.55, NAVY)
box(s, 9.1, 1.3, 3.9, 0.55, AQUA)
txt(s, "💡 Differenziazione", 9.2, 1.35, 3.7, 0.45,
    size=13, bold=True, color=NAVY)
txt(s, '"La Filiera\ndel Pescatore"', 9.2, 2.0, 3.6, 1.0,
    size=22, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s,
    "QR code sulla vaschetta GDO:\n\n"
    "• Nome del peschereccio\n"
    "• Porto di conferimento\n"
    "• Tecnica di pesca\n"
    "• Specie + giorno di pesca\n\n"
    "→ Nessun competitor nel panel\n"
    "   presidia questo territorio.\n\n"
    "→ Tracciabilità = storia umana\n"
    "   = ESG autentico e inimitabile",
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
     "Valori coerenti con operativo; narrativa ESG non strutturata pubblicamente"),
    ("ESG Coverage — Environmental", 2, 5,
     "Certificazioni presenti; nessun KPI pubblico; flotta e logistica non comunicate"),
    ("ESG Coverage — Social", 3, 5,
     "Partnership accademiche solide; radicamento territoriale autentico"),
    ("ESG Coverage — Governance", 2, 5,
     "IFS/ISO presenti; nessun documento ESG pubblico; dipendenza filiera non gestita"),
    ("Communication–Perception Gap", 2, 5,
     "Stampa di settore positiva; percezione consumatore finale non rilevabile"),
    ("Competitor Positioning", 3, 5,
     "Sopra Alles Fisch/Renna; pari Lepore Mare; distante da Nieddittas/Cromaris"),
]
for i, (dim, score, mx, note) in enumerate(dimensions):
    ty = 1.25 + i * 0.88
    txt(s, dim, 0.4, ty, 4.5, 0.45, size=13, bold=True, color=WHITE)
    # bar bg
    box(s, 5.0, ty + 0.08, 4.5, 0.3, RGBColor(0x1A,0x40,0x70))
    fill = 4.5 * score / mx
    col = GREEN_TAG if score >= 3 else (YELLOW_TAG if score >= 2 else RED_TAG)
    box(s, 5.0, ty + 0.08, fill, 0.3, col)
    txt(s, f"{score}/{mx}", 9.6, ty + 0.05, 0.6, 0.38,
        size=14, bold=True, color=col, align=PP_ALIGN.CENTER)
    txt(s, note, 10.3, ty + 0.05, 2.8, 0.42,
        size=10, color=AQUA, italic=True, wrap=True)

# Total
box(s, 0.3, 6.55, 12.7, 0.75, TEAL)
txt(s, "SCORE TOTALE", 0.6, 6.65, 4.0, 0.55,
    size=18, bold=True, color=WHITE)
txt(s, "14 / 30", 5.0, 6.58, 3.0, 0.65,
    size=28, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "Buona base operativa — urgente strutturare la comunicazione ESG",
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
        "Pagina Sostenibilità su maregioioso.it",
        "Primo fact sheet KPI auto-dichiarati",
        "Piano editoriale ESG social media",
    ]),
    ("FASE 2", "3–12 mesi", GREEN_TAG, [
        "Supplier Code of Conduct per la flotta",
        "Pilota QR code 'Filiera del Pescatore'",
        "su 1-2 referenze GDO flagship",
        "Avvio misurazione carbon footprint",
    ]),
    ("FASE 3", "12–36 mesi", TEAL, [
        "Primo Sustainability Report (GRI/VSME)",
        "Carbon footprint Scope 3 certificata",
        "Candidatura premi ESG di settore",
        "(MSC Partnership, Seafood Summit Award)",
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

# Closing quote
box(s, 0.3, 6.55, 12.7, 0.75, RGBColor(0x08,0x1E,0x3F))
txt(s,
    '"Mare Gioioso fa più di quanto racconta. Il compito dei prossimi 6 mesi è colmare questo gap."',
    0.5, 6.6, 12.4, 0.55, size=13, color=AQUA, italic=True, align=PP_ALIGN.CENTER)


# ─── Save ────────────────────────────────────────────────────────────────────
out = "/home/user/ESG-assessment/mare-gioioso-esg-deck-ceo.pptx"
prs.save(out)
print(f"Saved: {out}")
