"""
MotionMind — BCG-Style Deck
Wearable + Camera + App integrated system.
BCG design language: white/off-white base, deep teal/charcoal accents,
heavy typography hierarchy, structured frameworks.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ─────────────────────────────────────────────────
# BCG COLOR PALETTE
# ─────────────────────────────────────────────────
BCG_GREEN    = RGBColor(0x00, 0x73, 0x5C)   # BCG signature dark green
BCG_TEAL     = RGBColor(0x00, 0xA8, 0x8A)   # mid teal
BCG_LIME     = RGBColor(0x6C, 0xC2, 0x4A)   # lime accent
BCG_CHARCOAL = RGBColor(0x1A, 0x1A, 0x2E)   # near-black
BCG_DARK     = RGBColor(0x2C, 0x2C, 0x3E)   # dark slate
BCG_MID      = RGBColor(0x4A, 0x4A, 0x6A)   # mid gray-blue
BCG_GRAY     = RGBColor(0x8A, 0x8A, 0x9A)   # light gray
BCG_SILVER   = RGBColor(0xD8, 0xD8, 0xE4)   # silver rule
BCG_OFFWHITE = RGBColor(0xF5, 0xF5, 0xF7)   # off-white bg
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
BCG_ORANGE   = RGBColor(0xE8, 0x6A, 0x1A)   # warm orange accent
BCG_RED      = RGBColor(0xC0, 0x39, 0x2B)   # alert red
BCG_GOLD     = RGBColor(0xF0, 0xA5, 0x00)   # gold

# Slide dimensions — widescreen 16:9
W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

# ─────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────

def rect(slide, x, y, w, h, color, line_color=None, line_w=0):
    s = slide.shapes.add_shape(1, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    if line_color:
        s.line.color.rgb = line_color
        s.line.width = Pt(line_w)
    else:
        s.line.fill.background(); s.line.width = 0
    return s

def rr(slide, x, y, w, h, color):
    """Rounded rectangle."""
    s = slide.shapes.add_shape(5, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    s.line.fill.background(); s.line.width = 0
    return s

def tb(slide, text, x, y, w, h, size=12, bold=False, color=BCG_CHARCOAL,
       align=PP_ALIGN.LEFT, italic=False, name="Calibri", wrap=True):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.word_wrap = wrap
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold
    r.font.italic = italic; r.font.color.rgb = color
    r.font.name = name
    return box

def mtb(slide, lines, x, y, w, h, size=11, color=BCG_CHARCOAL,
        bold_idx=None, align=PP_ALIGN.LEFT, name="Calibri", sp=4):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.word_wrap = True
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_before = Pt(sp if i > 0 else 0)
        r = p.add_run(); r.text = line
        r.font.size = Pt(size)
        r.font.bold = (bold_idx is not None and i in bold_idx)
        r.font.color.rgb = color; r.font.name = name
    return box

def rule(slide, x, y, w, color=BCG_GREEN, h_pt=2):
    rect(slide, x, y, w, Pt(h_pt), color)

def slide_num(slide, n, total=13):
    tb(slide, f"{n}", W - Inches(0.6), H - Inches(0.38),
       Inches(0.45), Inches(0.3), size=9, color=BCG_GRAY, align=PP_ALIGN.RIGHT)

def bcg_footer(slide, text="MotionMind  ·  Confidential  ·  March 2026"):
    rect(slide, 0, H - Inches(0.32), W, Inches(0.32), BCG_GREEN)
    tb(slide, text, Inches(0.4), H - Inches(0.3),
       W - Inches(1.2), Inches(0.28), size=9, color=WHITE)

def white_bg(slide):
    rect(slide, 0, 0, W, H, WHITE)

def offwhite_bg(slide):
    rect(slide, 0, 0, W, H, BCG_OFFWHITE)

def dark_bg(slide):
    rect(slide, 0, 0, W, H, BCG_CHARCOAL)

def bcg_header(slide, title, subtitle=None):
    """Standard BCG page header — left green bar + title."""
    rect(slide, 0, 0, Inches(0.22), H, BCG_GREEN)
    tb(slide, title,
       Inches(0.38), Inches(0.28),
       W - Inches(0.9), Inches(0.72),
       size=30, bold=True, color=BCG_CHARCOAL, name="Calibri")
    if subtitle:
        rule(slide, Inches(0.38), Inches(1.02), W - Inches(0.76), BCG_GREEN, h_pt=2)
        tb(slide, subtitle,
           Inches(0.38), Inches(1.1),
           W - Inches(0.9), Inches(0.42),
           size=13, color=BCG_MID, italic=True)

def kf_box(slide, label, value, sub, x, y, w=Inches(2.7), h=Inches(1.55),
           accent=BCG_GREEN):
    rect(slide, x, y, w, h, BCG_OFFWHITE, line_color=BCG_SILVER, line_w=0.5)
    rect(slide, x, y, w, Pt(4), accent)
    tb(slide, value, x + Inches(0.12), y + Inches(0.18),
       w - Inches(0.24), Inches(0.6),
       size=30, bold=True, color=accent, align=PP_ALIGN.LEFT)
    tb(slide, label, x + Inches(0.12), y + Inches(0.78),
       w - Inches(0.24), Inches(0.38),
       size=11, bold=True, color=BCG_CHARCOAL)
    tb(slide, sub, x + Inches(0.12), y + Inches(1.12),
       w - Inches(0.24), Inches(0.35),
       size=9, color=BCG_GRAY)

def bar(slide, x, y, w, h, color, label=None, val_label=None):
    rect(slide, x, y, w, h, color)
    if val_label:
        tb(slide, val_label, x, y - Inches(0.32),
           w, Inches(0.3), size=10, bold=True,
           color=color, align=PP_ALIGN.CENTER)
    if label:
        tb(slide, label, x, y + h + Inches(0.04),
           w, Inches(0.36), size=9,
           color=BCG_MID, align=PP_ALIGN.CENTER)

def dot(slide, x, y, r, color):
    c = slide.shapes.add_shape(9, x - r, y - r, r*2, r*2)
    c.fill.solid(); c.fill.fore_color.rgb = color
    c.line.fill.background()

def tag(slide, text, x, y, color=BCG_GREEN, text_color=WHITE, w=Inches(1.6), h=Inches(0.32)):
    rr(slide, x, y, w, h, color)
    tb(slide, text, x + Inches(0.08), y + Inches(0.04),
       w - Inches(0.12), h - Inches(0.06),
       size=9, bold=True, color=text_color, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)

# Full-left dark panel
rect(s, 0, 0, Inches(7.5), H, BCG_CHARCOAL)
rect(s, 0, 0, Inches(0.18), H, BCG_GREEN)

# Logo / product name
tb(s, "MotionMind",
   Inches(0.4), Inches(1.1),
   Inches(6.8), Inches(1.4),
   size=62, bold=True, color=WHITE, name="Calibri")

tb(s, "The Integrated Child Development System",
   Inches(0.4), Inches(2.52),
   Inches(6.8), Inches(0.7),
   size=20, color=BCG_TEAL, bold=False)

rule(s, Inches(0.4), Inches(3.32), Inches(4.8), BCG_TEAL, h_pt=2)

tb(s,
   "A wearable sensor band + camera gesture system + AI platform\n"
   "that detects developmental gaps in children ages 3–11\n"
   "and prescribes exactly what to do — at zero parent effort.",
   Inches(0.4), Inches(3.5),
   Inches(6.7), Inches(1.5),
   size=15, color=BCG_SILVER)

# 3 system pillars on left
for i, (icon, label) in enumerate([
    ("◉", "Wearable Band  ·  Handgrip · Muscle · Motion"),
    ("◎", "Camera System  ·  Hand-Tracking · Gesture"),
    ("◈", "AI Platform    ·  Gap Detection · Prescription"),
]):
    py = Inches(5.25) + i * Inches(0.52)
    tb(s, icon, Inches(0.4), py, Inches(0.4), Inches(0.44),
       size=14, color=BCG_TEAL, bold=True)
    tb(s, label, Inches(0.85), py + Inches(0.03), Inches(6.2), Inches(0.4),
       size=12, color=BCG_SILVER)

# Right panel — system diagram (text-based)
rect(s, Inches(7.5), 0, Inches(5.83), H, BCG_OFFWHITE)

tb(s, "The System",
   Inches(7.75), Inches(0.55),
   Inches(5.3), Inches(0.5),
   size=18, bold=True, color=BCG_CHARCOAL)
rule(s, Inches(7.75), Inches(1.08), Inches(5.1), BCG_GREEN, h_pt=1.5)

# System diagram boxes
sys_items = [
    (BCG_GREEN,   "⌚  WEARABLE BAND",
     "Handgrip strength  ·  Muscle EMG\n"
     "Accelerometer  ·  Gyroscope\n"
     "Worn on wrist / forearm during play"),
    (BCG_TEAL,    "📷  CAMERA SYSTEM",
     "21-pt hand skeleton (MediaPipe)\n"
     "Body gesture tracking\n"
     "Works on any tablet/phone camera"),
    (BCG_MID,     "🤖  AI PLATFORM",
     "Real-time gap scoring\n"
     "Developmental profile generation\n"
     "Household activity prescription"),
    (BCG_LIME,    "👨‍👩‍👧  PARENT + CLINICIAN",
     "Weekly body report card\n"
     "Pediatrician PDF / EHR integration\n"
     "OT referral pathway"),
]
for i, (col, title, body) in enumerate(sys_items):
    sy = Inches(1.35) + i * Inches(1.44)
    rect(s, Inches(7.75), sy, Inches(5.1), Inches(1.3), WHITE,
         line_color=col, line_w=1.2)
    rect(s, Inches(7.75), sy, Inches(0.14), Inches(1.3), col)
    tb(s, title, Inches(7.98), sy + Inches(0.1),
       Inches(4.8), Inches(0.38), size=12, bold=True, color=col)
    tb(s, body, Inches(7.98), sy + Inches(0.52),
       Inches(4.8), Inches(0.7), size=10.5, color=BCG_MID)
    if i < 3:
        tb(s, "↓", Inches(10.0), sy + Inches(1.3),
           Inches(0.5), Inches(0.2), size=11, bold=True,
           color=BCG_GREEN, align=PP_ALIGN.CENTER)

tb(s, "BCG-Style Investor Deck  ·  Stanford CIM206  ·  March 2026",
   Inches(7.75), H - Inches(0.45),
   Inches(5.3), Inches(0.35),
   size=9, color=BCG_GRAY)

bcg_footer(s)
slide_num(s, 1)


# ═══════════════════════════════════════════════════════
# SLIDE 2 — EXECUTIVE SUMMARY (BCG "so what" page)
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Executive Summary",
           "MotionMind addresses a $103B market with a hardware + software system that has no direct competitor.")

# 3-column "situation / complication / resolution" BCG framework
scr = [
    ("SITUATION",
     BCG_CHARCOAL, BCG_OFFWHITE,
     [
         "6 hrs/day screen time for US children",
         "Only 18% meet movement guidelines",
         "8M+ children ages 0–11 showing developmental symptoms",
         "1 in 6 children have a developmental disability",
         "Parents see the problem but have nothing to act with",
     ]),
    ("COMPLICATION",
     WHITE, BCG_CHARCOAL,
     [
         "Screen management tools don't address body development",
         "Clinical OT is inaccessible until symptoms are severe",
         "No product detects gaps AND prescribes intervention",
         "Wearables for children don't exist in this space",
         "The developmental window (ages 3–7) closes silently",
     ]),
    ("RESOLUTION",
     BCG_GREEN, WHITE,
     [
         "MotionMind = wearable band + camera + AI platform",
         "Detects 7/8 developmental gaps in real time",
         "Prescribes gap-closing activities at zero parent effort",
         "Works on hardware families already own + a $49 band",
         "Launch-ready under FDA General Wellness (Jan 2026)",
     ]),
]

col_w = Inches(4.1)
for i, (title, text_col, bg_col, items) in enumerate(scr):
    cx = Inches(0.38) + i * (col_w + Inches(0.12))
    cy = Inches(1.62)
    rect(s, cx, cy, col_w, Inches(5.45), bg_col,
         line_color=BCG_SILVER, line_w=0.5)
    tb(s, title, cx + Inches(0.18), cy + Inches(0.15),
       col_w - Inches(0.3), Inches(0.44),
       size=13, bold=True, color=text_col if bg_col != BCG_CHARCOAL else BCG_TEAL)
    rule(s, cx + Inches(0.18), cy + Inches(0.62), col_w - Inches(0.36),
         BCG_TEAL if bg_col == BCG_CHARCOAL else (WHITE if bg_col == BCG_GREEN else BCG_GREEN),
         h_pt=1)
    for j, item in enumerate(items):
        iy = cy + Inches(0.82) + j * Inches(0.76)
        bullet_col = (BCG_TEAL if bg_col == BCG_CHARCOAL
                      else (WHITE if bg_col == BCG_GREEN else BCG_GREEN))
        tb(s, "—", cx + Inches(0.18), iy,
           Inches(0.22), Inches(0.36), size=11, bold=True, color=bullet_col)
        tb(s, item, cx + Inches(0.42), iy,
           col_w - Inches(0.58), Inches(0.64),
           size=11, color=text_col)

bcg_footer(s); slide_num(s, 2)


# ═══════════════════════════════════════════════════════
# SLIDE 3 — THE PROBLEM (QUANTIFIED)
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "The Problem Is Quantified — and Compounding",
           "Every metric points to the same gap. The developmental window is closing without intervention.")

# 5 KF boxes top
kf_data = [
    ("Screen time daily", "6 hrs", "Average US child ages 8–12", BCG_CHARCOAL),
    ("Movement deficit", "82%", "Children NOT meeting movement guidelines", BCG_RED),
    ("Symptomatic children", "8M+", "US ages 0–11 showing developmental gaps", BCG_ORANGE),
    ("Parental resignation", "28%", "Give in to screens weekly to avoid meltdown (Lurie, 2025)", BCG_MID),
    ("Dependency multiplier", "1.7×", "Screen-as-reward increases dependency", BCG_GREEN),
]
for i, (label, val, sub, col) in enumerate(kf_data):
    kx = Inches(0.38) + i * Inches(2.56)
    kf_box(s, label, val, sub, kx, Inches(1.62), w=Inches(2.42), h=Inches(1.55), accent=col)

# The reinforcing trap — visual chain
rect(s, Inches(0.38), Inches(3.4), W - Inches(0.76), Inches(0.08), BCG_SILVER)
tb(s, "THE REINFORCING TRAP", Inches(0.38), Inches(3.22),
   Inches(5), Inches(0.35), size=10, bold=True, color=BCG_GRAY)

trap_steps = ["Screen", "Dopamine\nhit", "Meltdown\nat off", "Screen\nto manage",
              "Screen =\ncurrency", "Relationship\nerodes", "Deeper\ndependency"]
trap_cols = [BCG_MID, BCG_ORANGE, BCG_RED, BCG_MID, BCG_ORANGE, BCG_RED, BCG_CHARCOAL]
step_w = Inches(1.62)
for i, (step, col) in enumerate(zip(trap_steps, trap_cols)):
    sx = Inches(0.38) + i * (step_w + Inches(0.06))
    rect(s, sx, Inches(3.55), step_w, Inches(0.95), col)
    tb(s, step, sx + Inches(0.1), Inches(3.62),
       step_w - Inches(0.2), Inches(0.82),
       size=10, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    if i < 6:
        tb(s, "→", sx + step_w, Inches(3.72),
           Inches(0.1), Inches(0.42), size=11, bold=True,
           color=BCG_GRAY, align=PP_ALIGN.CENTER)

# Bottom: 3 stakeholder impact boxes
impacts = [
    ("Child impact",
     "Motor gaps form silently by age 6.\nCan't hold pencil → ADHD label.\nPhysical identity as 'not athletic' locks in."),
    ("Parent impact",
     "Exhausted + resigned by age 8–11.\nNo tool to act with.\nRelationship damage compounds."),
    ("System impact",
     "$14.1T lifetime toll of untreated childhood adversity.\n$9B+ annual early intervention spend.\nAll reactive — nothing is preventive."),
]
for i, (title, body) in enumerate(impacts):
    ix = Inches(0.38) + i * Inches(4.3)
    rect(s, ix, Inches(4.72), Inches(4.1), Inches(2.3), BCG_OFFWHITE,
         line_color=BCG_SILVER, line_w=0.5)
    rule(s, ix, Inches(4.72), Inches(4.1), BCG_GREEN, h_pt=3)
    tb(s, title, ix + Inches(0.15), Inches(4.88),
       Inches(3.8), Inches(0.38), size=12, bold=True, color=BCG_GREEN)
    tb(s, body, ix + Inches(0.15), Inches(5.32),
       Inches(3.8), Inches(1.55), size=11, color=BCG_MID)

bcg_footer(s); slide_num(s, 3)


# ═══════════════════════════════════════════════════════
# SLIDE 4 — MARKET SIZE (BCG waterfall-style)
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Market Sizing — A $103B Opportunity with Clear White Space",
           "MotionMind sits at the intersection of three converging markets.")

# TAM / SAM / SOM visual — nested boxes
rect(s, Inches(0.38), Inches(1.62), Inches(7.0), Inches(5.45), BCG_OFFWHITE,
     line_color=BCG_SILVER, line_w=0.5)

# TAM
rect(s, Inches(0.5), Inches(1.74), Inches(6.76), Inches(5.2), RGBColor(0xE8, 0xF5, 0xF1),
     line_color=BCG_GREEN, line_w=1)
tb(s, "TAM — Child developmental health + rehab + digital health",
   Inches(0.65), Inches(1.85), Inches(5.5), Inches(0.38),
   size=11, bold=True, color=BCG_GREEN)
tb(s, "$103B by 2034 (7% CAGR)",
   Inches(0.65), Inches(2.22), Inches(3.5), Inches(0.35),
   size=18, bold=True, color=BCG_GREEN)

# SAM
rect(s, Inches(0.7), Inches(2.72), Inches(6.16), Inches(3.8), RGBColor(0xD0, 0xEF, 0xE6),
     line_color=BCG_TEAL, line_w=1)
tb(s, "SAM — US families with children 0–11 showing symptoms",
   Inches(0.88), Inches(2.82), Inches(5.2), Inches(0.35),
   size=11, bold=True, color=BCG_TEAL)
tb(s, "$14–18B addressable",
   Inches(0.88), Inches(3.16), Inches(3.5), Inches(0.35),
   size=16, bold=True, color=BCG_TEAL)

# SOM
rect(s, Inches(0.92), Inches(3.66), Inches(5.52), Inches(2.72), RGBColor(0xB8, 0xE8, 0xD8),
     line_color=BCG_MID, line_w=1)
tb(s, "SOM — Early adopter parents + pediatric OT network",
   Inches(1.1), Inches(3.76), Inches(5.0), Inches(0.35),
   size=11, bold=True, color=BCG_MID)
tb(s, "$850M–$1.2B (Year 3–5)",
   Inches(1.1), Inches(4.12), Inches(3.5), Inches(0.35),
   size=14, bold=True, color=BCG_MID)
tb(s, "8M symptomatic US children × ~$120 ARPU",
   Inches(1.1), Inches(4.5), Inches(4.5), Inches(0.35),
   size=10, color=BCG_GRAY, italic=True)

# White space callout
rect(s, Inches(1.1), Inches(5.08), Inches(5.1), Inches(0.88),
     BCG_GREEN)
tb(s, "WHITE SPACE:  Between Bark/Screen Time (mgmt) and clinical OT — nobody serves the pre-clinical family.",
   Inches(1.25), Inches(5.18), Inches(4.8), Inches(0.65),
   size=11, bold=True, color=WHITE)

# Right — market breakdown bars
tb(s, "Adjacent market segments",
   Inches(7.7), Inches(1.62), Inches(5.3), Inches(0.38),
   size=12, bold=True, color=BCG_CHARCOAL)
rule(s, Inches(7.7), Inches(2.02), Inches(5.1), BCG_GREEN, h_pt=1)

bar_data = [
    ("Kids apps",        "$16B",  5.1, BCG_GREEN),
    ("Parenting apps",   "$6B",   1.9, BCG_TEAL),
    ("Parental ctrl sw", "$4.2B", 1.33, BCG_MID),
    ("Child rehab",      "$103B", 5.1, BCG_CHARCOAL),
    ("Early interv.",    "$9B",   2.9, BCG_ORANGE),
    ("Wearable health",  "$60B",  5.1, BCG_LIME),
]
max_bar_w = Inches(4.6)
for i, (label, val, rel, col) in enumerate(bar_data):
    by = Inches(2.22) + i * Inches(0.76)
    bw = max_bar_w * (rel / 5.1)
    rect(s, Inches(7.7), by + Inches(0.08), bw, Inches(0.46), col)
    tb(s, label, Inches(7.7), by,
       Inches(2.8), Inches(0.32), size=10, color=BCG_MID)
    tb(s, val, Inches(7.7) + bw + Inches(0.1), by + Inches(0.1),
       Inches(1.2), Inches(0.36), size=11, bold=True, color=col)

bcg_footer(s); slide_num(s, 4)


# ═══════════════════════════════════════════════════════
# SLIDE 5 — THE SYSTEM (WEARABLE + CAMERA + APP)
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "The MotionMind System — Three Integrated Layers",
           "Wearable band + camera gesture system + AI platform. Not just an app.")

# 3 layer cards
layers = [
    {
        "num": "01", "color": BCG_GREEN, "bg": RGBColor(0xE8, 0xF5, 0xF1),
        "title": "WEARABLE BAND",
        "sub": "Hardware · $49 MSRP · Worn on wrist/forearm",
        "sensors": [
            ("Handgrip strength",    "Force sensor · measures grip force in Newtons · key fine motor predictor"),
            ("Muscle activity (EMG)","Surface electromyography · detects muscle engagement quality"),
            ("Accelerometer",        "3-axis · captures reach speed, movement amplitude, tremor"),
            ("Gyroscope",            "Wrist rotation, forearm pronation/supination"),
            ("Skin conductance",     "Arousal / stress proxy · flags dysregulation during play"),
        ],
        "why": "Captures what camera cannot: force, muscle quality, and physiological state.",
    },
    {
        "num": "02", "color": BCG_TEAL, "bg": RGBColor(0xD8, 0xF0, 0xEB),
        "title": "CAMERA SYSTEM",
        "sub": "Software · Any front-facing camera · No extra hardware",
        "sensors": [
            ("Hand skeleton (21pt)", "Google MediaPipe Hands · <10ms latency · real-time on mobile"),
            ("Body pose tracking",   "Full-body landmark detection · gross motor + vestibular assessment"),
            ("Gesture scoring",      "Pinch precision, reach accuracy, bilateral coordination"),
            ("Visual-motor timing",  "Reaction latency between visual cue and motor response"),
            ("Facial attention",     "Engagement proxy — flags passive vs. active interaction"),
        ],
        "why": "Captures spatial and gesture quality. Pairs with wearable for full-body picture.",
    },
    {
        "num": "03", "color": BCG_MID, "bg": RGBColor(0xED, 0xED, 0xF5),
        "title": "AI PLATFORM",
        "sub": "Cloud + on-device · Gap scoring + prescription engine",
        "sensors": [
            ("Gap detection engine", "Fuses wearable + camera data → scores 7/8 developmental inputs"),
            ("Developmental profile","Auto-generated gap profile after first session"),
            ("Activity Rx engine",   "Prescribes household activities matched to detected gap"),
            ("Progress tracking",    "Longitudinal scoring — tracks gap closure over weeks/months"),
            ("Clinician dashboard",  "PDF report + FHIR export for pediatrician / OT"),
        ],
        "why": "Turns raw sensor data into parent-readable, clinician-shareable developmental intelligence.",
    },
]

card_w = Inches(4.1)
for i, layer in enumerate(layers):
    cx = Inches(0.38) + i * (card_w + Inches(0.14))
    cy = Inches(1.62)
    rect(s, cx, cy, card_w, Inches(5.45), layer["bg"],
         line_color=layer["color"], line_w=1)
    rect(s, cx, cy, card_w, Inches(0.62), layer["color"])
    tb(s, layer["num"], cx + Inches(0.15), cy + Inches(0.1),
       Inches(0.5), Inches(0.45), size=16, bold=True, color=WHITE)
    tb(s, layer["title"], cx + Inches(0.65), cy + Inches(0.12),
       card_w - Inches(0.8), Inches(0.38), size=14, bold=True, color=WHITE)
    tb(s, layer["sub"], cx + Inches(0.15), cy + Inches(0.68),
       card_w - Inches(0.3), Inches(0.32), size=9.5, color=layer["color"],
       italic=True)
    rule(s, cx + Inches(0.15), cy + Inches(1.02),
         card_w - Inches(0.3), layer["color"], h_pt=1)
    for j, (sensor, desc) in enumerate(layer["sensors"]):
        sy = cy + Inches(1.15) + j * Inches(0.68)
        dot(s, cx + Inches(0.3), sy + Inches(0.17), Inches(0.065), layer["color"])
        tb(s, sensor, cx + Inches(0.45), sy,
           card_w - Inches(0.6), Inches(0.28),
           size=10.5, bold=True, color=BCG_CHARCOAL)
        tb(s, desc, cx + Inches(0.45), sy + Inches(0.28),
           card_w - Inches(0.6), Inches(0.35),
           size=9, color=BCG_MID)
    rect(s, cx, cy + Inches(4.88), card_w, Inches(0.57), layer["color"])
    tb(s, layer["why"], cx + Inches(0.15), cy + Inches(4.95),
       card_w - Inches(0.3), Inches(0.42),
       size=10, bold=True, color=WHITE)

bcg_footer(s); slide_num(s, 5)


# ═══════════════════════════════════════════════════════
# SLIDE 6 — DEVELOPMENTAL GAP COVERAGE MATRIX
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Developmental Gap Coverage — MotionMind vs. Alternatives",
           "Only MotionMind closes 7/8 gaps. The 8th (relational) requires a human — nothing changes that.")

# Legend
for i, (label, col) in enumerate([
    ("Fully covered", BCG_GREEN),
    ("Partially covered", BCG_TEAL),
    ("Prescribe to close", BCG_LIME),
    ("Not covered", BCG_RED),
]):
    lx = Inches(0.38) + i * Inches(3.1)
    rect(s, lx, Inches(1.62), Inches(0.22), Inches(0.22), col)
    tb(s, label, lx + Inches(0.3), Inches(1.6), Inches(2.6), Inches(0.3),
       size=10, color=BCG_MID)

# Table
headers2 = ["Developmental Input", "Camera\n(gesture)", "Wearable\n(band)", "Combined\nMotionMind", "Tablet\napp", "OT\nclinic"]
col_ws2 = [Inches(2.9), Inches(1.62), Inches(1.62), Inches(1.88), Inches(1.62), Inches(1.62)]
col_xs2 = []
cx2 = Inches(0.38)
for w in col_ws2:
    col_xs2.append(cx2); cx2 += w

# header row
rect(s, Inches(0.38), Inches(2.0), sum(col_ws2), Inches(0.52), BCG_CHARCOAL)
for j, (h, xs, ws) in enumerate(zip(headers2, col_xs2, col_ws2)):
    tb(s, h, xs + Inches(0.08), Inches(2.04),
       ws - Inches(0.1), Inches(0.44),
       size=10, bold=True, color=WHITE,
       align=PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT)

rows2 = [
    # gap name             cam   wear  mm    tab   ot
    ("Fine motor precision",      "PART","FULL","FULL","NO",  "FULL"),
    ("Handgrip strength",         "NO",  "FULL","FULL","NO",  "FULL"),
    ("Muscle quality (EMG)",      "NO",  "FULL","FULL","NO",  "PART"),
    ("Gross motor activation",    "FULL","PART","FULL","NO",  "FULL"),
    ("Body schema / spatial",     "FULL","PART","FULL","NO",  "FULL"),
    ("Visual-motor integration",  "FULL","PART","FULL","NO",  "FULL"),
    ("Vestibular",                "PART","PART","FULL","NO",  "FULL"),
    ("Relational",                "NO",  "NO",  "NO", "NO",  "FULL"),
]

cell_colors = {
    "FULL": BCG_GREEN, "PART": BCG_TEAL, "RX": BCG_LIME,
    "NO": BCG_RED,
}

for i, (gap, *cells) in enumerate(rows2):
    ry = Inches(2.52) + i * Inches(0.56)
    bg2 = BCG_OFFWHITE if i % 2 == 0 else WHITE
    rect(s, Inches(0.38), ry, sum(col_ws2), Inches(0.54), bg2)
    # last row — relational — special treatment
    is_last = (i == len(rows2) - 1)
    tb(s, gap,
       col_xs2[0] + Inches(0.1), ry + Inches(0.1),
       col_ws2[0] - Inches(0.15), Inches(0.36),
       size=11, bold=is_last, color=BCG_CHARCOAL if not is_last else BCG_GRAY,
       italic=is_last)
    for j, (cell, xs, ws) in enumerate(zip(cells, col_xs2[1:], col_ws2[1:])):
        cw2 = Inches(0.62); ch2 = Inches(0.3)
        offset_x = xs + (ws - cw2) / 2
        offset_y = ry + Inches(0.12)
        rect(s, offset_x, offset_y, cw2, ch2,
             cell_colors.get(cell, BCG_GRAY))
        label_col = WHITE if cell in ("FULL","NO") else BCG_CHARCOAL
        tb(s, cell, offset_x, offset_y,
           cw2, ch2, size=9, bold=True, color=label_col,
           align=PP_ALIGN.CENTER)

# score row
rect(s, Inches(0.38), Inches(7.02), sum(col_ws2), Inches(0.42), BCG_CHARCOAL)
scores = ["SCORE", "5/8", "6/8", "7/8", "0/8", "8/8"]
for j, (sc, xs, ws) in enumerate(zip(scores, col_xs2, col_ws2)):
    tb(s, sc, xs + Inches(0.08), Inches(7.06),
       ws - Inches(0.1), Inches(0.32),
       size=11, bold=True,
       color=BCG_TEAL if j in (1,2) else (BCG_LIME if j==3 else (BCG_GREEN if j==3 else WHITE)),
       align=PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT)

# fix score colors
score_cols = [WHITE, BCG_TEAL, BCG_TEAL, BCG_LIME, BCG_RED, BCG_GRAY]
for j, (sc, xs, ws, scol) in enumerate(zip(scores, col_xs2, col_ws2, score_cols)):
    tb(s, sc, xs + Inches(0.08), Inches(7.06),
       ws - Inches(0.1), Inches(0.32),
       size=11, bold=(j != 0),
       color=scol,
       align=PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT)

bcg_footer(s); slide_num(s, 6)


# ═══════════════════════════════════════════════════════
# SLIDE 7 — SCIENCE & CLINICAL VALIDATION
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Science Backbone — Every Claim Is Cited",
           "The evidence base spans motor neuroscience, pediatric OT, and digital health meta-analyses.")

evidence2 = [
    ("VMI — Beery & Beery, 2010",
     BCG_GREEN,
     "Visual-Motor Integration deficits are among the earliest predictors of fine motor delay "
     "and academic readiness. The Beery VMI (6th ed.) is the gold-standard OT assessment. "
     "MotionMind's camera system directly measures VMI in real time — no clinic visit required."),
    ("Visual-proprioceptive coupling\n— PLOS One, 2020",
     BCG_TEAL,
     "Children ages 4–8 rely heavily on visual cues in spatial and motor tasks — a fundamentally "
     "different integration profile from adults. Gesture + hand-tracking interaction uniquely "
     "targets this critical developmental window."),
    ("Embodied learning meta-analysis\n44 studies, SMD = 0.41, p<.01 (2025)",
     BCG_MID,
     "Technology-based embodied learning (body-in-the-loop interaction) produces significant "
     "developmental gains across 44 studies. MotionMind's gesture system is the first to pair "
     "embodied play with real-time wearable biometric feedback."),
    ("Grip strength as motor predictor\n— J. Child Neurology, 2022",
     BCG_GREEN,
     "Handgrip strength in children ages 4–11 is a validated predictor of overall motor "
     "development, coordination, and school readiness. Below-norm grip is detectable 18+ months "
     "before clinical referral. MotionMind's force sensor captures this continuously."),
    ("EMG in pediatric motor assessment\n— Dev. Medicine & Child Neurology",
     BCG_TEAL,
     "Surface EMG is an established OT tool for assessing muscle recruitment quality in children "
     "with DCD (Developmental Coordination Disorder). Wearable consumer EMG is now achievable "
     "at <$50 BOM — same technology used in Myo armband (Thalmic Labs)."),
    ("Heckman Equation — Nobel 2000",
     BCG_CHARCOAL,
     "7–12× ROI on early developmental intervention. The earlier the detection, the higher the "
     "return. MotionMind enables detection at ages 3–5 — before clinical thresholds are crossed. "
     "This is the economic case for payer coverage via IDEA codes."),
]

card_w2 = Inches(4.0)
card_h2 = Inches(2.2)
for idx, (title, col, body) in enumerate(evidence2):
    ci = idx % 3
    ri = idx // 3
    cx3 = Inches(0.38) + ci * (card_w2 + Inches(0.19))
    cy3 = Inches(1.62) + ri * (card_h2 + Inches(0.15))
    rect(s, cx3, cy3, card_w2, card_h2, BCG_OFFWHITE,
         line_color=BCG_SILVER, line_w=0.5)
    rect(s, cx3, cy3, Inches(0.1), card_h2, col)
    rect(s, cx3, cy3, card_w2, Pt(3), col)
    tb(s, title, cx3 + Inches(0.2), cy3 + Inches(0.1),
       card_w2 - Inches(0.3), Inches(0.62),
       size=11, bold=True, color=col)
    tb(s, body, cx3 + Inches(0.2), cy3 + Inches(0.78),
       card_w2 - Inches(0.3), Inches(1.3),
       size=10, color=BCG_MID)

bcg_footer(s); slide_num(s, 7)


# ═══════════════════════════════════════════════════════
# SLIDE 8 — COMPETITIVE LANDSCAPE (2×2)
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Competitive Positioning — MotionMind Owns the Uncontested Quadrant",
           "No competitor combines real-time biometric sensing with gap-specific developmental prescription.")

# 2×2 matrix
mx = Inches(1.8); my = Inches(1.6)
mw = Inches(9.5); mh = Inches(5.5)

# quadrant backgrounds
rect(s, mx,        my,        mw/2, mh/2, RGBColor(0xF5, 0xF5, 0xF7))  # BL
rect(s, mx+mw/2,   my,        mw/2, mh/2, RGBColor(0xF5, 0xF5, 0xF7))  # BR
rect(s, mx,        my+mh/2,   mw/2, mh/2, RGBColor(0xF0, 0xF8, 0xF4))  # TL
rect(s, mx+mw/2,   my+mh/2,   mw/2, mh/2, RGBColor(0xE4, 0xF4, 0xED))  # TR — MotionMind quadrant

# axes
rect(s, mx, my+mh/2-Pt(1), mw, Pt(2), BCG_SILVER)  # horizontal
rect(s, mx+mw/2-Pt(1), my, Pt(2), mh, BCG_SILVER)  # vertical

# axis labels
tb(s, "← Low Developmental Detection →",
   mx, my + mh + Inches(0.1), mw, Inches(0.35),
   size=11, color=BCG_GRAY, align=PP_ALIGN.CENTER)
tb(s, "HIGH\nDetection",
   mx - Inches(1.35), my, Inches(1.2), mh/2,
   size=10, color=BCG_GRAY, align=PP_ALIGN.RIGHT)
tb(s, "LOW\nDetection",
   mx - Inches(1.35), my + mh/2, Inches(1.2), mh/2,
   size=10, color=BCG_GRAY, align=PP_ALIGN.RIGHT)
tb(s, "Hardware Only / No Prescription",
   mx, my - Inches(0.45), mw/2, Inches(0.38),
   size=10, color=BCG_GRAY, align=PP_ALIGN.CENTER)
tb(s, "Hardware + Software + Prescription",
   mx + mw/2, my - Inches(0.45), mw/2, Inches(0.38),
   size=10, color=BCG_GRAY, align=PP_ALIGN.CENTER)

# quadrant labels
for (qx, qy, qtxt, qcol) in [
    (mx + Inches(0.15),      my + mh/2 + Inches(0.1), "Sensor-rich,\nno prescription", BCG_GRAY),
    (mx + mw/2 + Inches(0.15), my + mh/2 + Inches(0.1), "MotionMind\nTERRITORY", BCG_GREEN),
    (mx + Inches(0.15),      my + Inches(0.1),          "Low detection,\nno prescription", BCG_GRAY),
    (mx + mw/2 + Inches(0.15), my + Inches(0.1),        "Partial detection,\nno prescription", BCG_GRAY),
]:
    tb(s, qtxt, qx, qy, mw/2 - Inches(0.3), Inches(0.55),
       size=10, bold=(qcol == BCG_GREEN), color=qcol)

# Plot competitors
competitors2 = [
    # name               x_frac y_frac  col
    ("MotionMind ★",      0.78,  0.78,  BCG_GREEN,   True),
    ("Nex Playground",    0.18,  0.65,  BCG_MID,     False),
    ("Osmo",              0.30,  0.40,  BCG_MID,     False),
    ("GoNoodle",          0.08,  0.22,  BCG_GRAY,    False),
    ("Apple Screen Time", 0.05,  0.12,  BCG_GRAY,    False),
    ("Kinect / Xbox",     0.22,  0.55,  BCG_MID,     False),
    ("Pediatric OT",      0.88,  0.90,  BCG_TEAL,    False),
    ("Fitbit / Garmin",   0.15,  0.72,  BCG_ORANGE,  False),
]
for (name, xf, yf, col, star) in competitors2:
    px = mx + mw * xf
    py = my + mh * (1 - yf)
    r2 = Inches(0.115) if star else Inches(0.085)
    dot(s, px, py, r2, col)
    tb(s, name, px + Inches(0.15), py - Inches(0.18),
       Inches(1.8), Inches(0.35),
       size=9.5, bold=star, color=col)

bcg_footer(s); slide_num(s, 8)


# ═══════════════════════════════════════════════════════
# SLIDE 9 — PRODUCT ARCHITECTURE & DEMO FLOW
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Product Architecture — How It Works End-to-End",
           "From first wear to developmental prescription in one session. Zero clinical expertise required.")

# Top: 5-step flow
steps2 = [
    ("01", BCG_GREEN,    "Onboard",
     "3-min OT-designed\nparent setup.\nChild profile created."),
    ("02", BCG_TEAL,     "Sense",
     "Band worn on wrist.\nCamera activated.\nAll sensors live."),
    ("03", BCG_MID,      "Play",
     "Child plays gesture\ngame. Body + hand\ntracked in real time."),
    ("04", BCG_GREEN,    "Detect",
     "AI fuses wearable +\ncamera data → scores\n7 developmental gaps."),
    ("05", BCG_CHARCOAL, "Prescribe",
     "App delivers activity\nRx + weekly body\nreport card to parent."),
]

sw2 = Inches(2.3)
for i, (num, col, title, body) in enumerate(steps2):
    sx2 = Inches(0.38) + i * (sw2 + Inches(0.1))
    sy2 = Inches(1.62)
    rect(s, sx2, sy2, sw2, Inches(2.8), BCG_OFFWHITE,
         line_color=col, line_w=1)
    rect(s, sx2, sy2, sw2, Inches(0.5), col)
    tb(s, num, sx2 + Inches(0.12), sy2 + Inches(0.08),
       Inches(0.5), Inches(0.36), size=14, bold=True, color=WHITE)
    tb(s, title, sx2 + Inches(0.65), sy2 + Inches(0.1),
       sw2 - Inches(0.78), Inches(0.36), size=12, bold=True, color=WHITE)
    tb(s, body, sx2 + Inches(0.15), sy2 + Inches(0.65),
       sw2 - Inches(0.3), Inches(1.95), size=11, color=BCG_MID)
    if i < 4:
        tb(s, "→", sx2 + sw2, sy2 + Inches(1.15),
           Inches(0.12), Inches(0.5), size=16, bold=True,
           color=BCG_GREEN, align=PP_ALIGN.CENTER)

# Middle: data flow diagram
tb(s, "DATA ARCHITECTURE", Inches(0.38), Inches(4.6),
   Inches(6), Inches(0.35), size=10, bold=True, color=BCG_GRAY)
rule(s, Inches(0.38), Inches(4.97), W - Inches(0.76), BCG_SILVER, h_pt=1)

data_boxes = [
    (Inches(0.38),  "WEARABLE\nSENSORS",
     "Grip · EMG\nAccel · Gyro\n10Hz sampling",  BCG_GREEN),
    (Inches(3.25),  "CAMERA\nSYSTEM",
     "21-pt hand\nBody pose\n30fps", BCG_TEAL),
    (Inches(6.12),  "ON-DEVICE\nAI FUSION",
     "Gap scoring\nProfile engine\n<200ms latency", BCG_MID),
    (Inches(8.99),  "CLOUD\nPLATFORM",
     "Longitudinal data\nClinician dashboard\nAnon. research DB", BCG_CHARCOAL),
    (Inches(11.1),  "PARENT /\nCLINICIAN",
     "App report card\nPDF / FHIR\nOT referral", BCG_GREEN),
]
for bx2, title2, body2, col2 in data_boxes:
    rect(s, bx2, Inches(5.1), Inches(2.6), Inches(1.95), BCG_OFFWHITE,
         line_color=col2, line_w=1)
    rect(s, bx2, Inches(5.1), Inches(2.6), Pt(3), col2)
    tb(s, title2, bx2 + Inches(0.12), Inches(5.18),
       Inches(2.35), Inches(0.5), size=10, bold=True, color=col2)
    tb(s, body2, bx2 + Inches(0.12), Inches(5.72),
       Inches(2.35), Inches(1.15), size=9.5, color=BCG_MID)

# arrows between data boxes
for i in range(4):
    ax2 = Inches(0.38) + (i+1) * Inches(2.72) - Inches(0.05)
    tb(s, "→", ax2, Inches(5.8), Inches(0.22), Inches(0.42),
       size=13, bold=True, color=BCG_GREEN, align=PP_ALIGN.CENTER)

# COPPA / security note
rect(s, Inches(0.38), Inches(7.1), W - Inches(0.76), Inches(0.22),
     RGBColor(0xE8, 0xF5, 0xF1))
tb(s, "🔒  COPPA 2025 compliant · Biometric data encrypted on-device · "
      "No 3rd-party analytics · Parent-only account · "
      "FDA General Wellness (Jan 2026) · $53,088/violation architecture",
   Inches(0.55), Inches(7.13), W - Inches(1.1), Inches(0.2),
   size=9, color=BCG_GREEN)

bcg_footer(s); slide_num(s, 9)


# ═══════════════════════════════════════════════════════
# SLIDE 10 — GO-TO-MARKET & BUSINESS MODEL
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Business Model & Go-to-Market",
           "Hardware + software revenue. Three parallel GTM tracks from day one.")

# Left: revenue model table
tb(s, "REVENUE MODEL",
   Inches(0.38), Inches(1.62), Inches(5.8), Inches(0.38),
   size=12, bold=True, color=BCG_CHARCOAL)
rule(s, Inches(0.38), Inches(2.02), Inches(5.8), BCG_GREEN, h_pt=1.5)

rev_rows = [
    ("Wearable Band (hardware)",   "$49 MSRP",     "~$22 COGS",   "Launch"),
    ("App — Free tier",            "$0",            "CAC driver",  "Launch"),
    ("App — Premium subscription", "$9.99/mo",      "Gap Rx library + report", "Launch"),
    ("School / library license",   "$499/site/yr",  "B2B channel", "Q3 2026"),
    ("Clinical PDF + FHIR",        "$29/provider/mo","EHR integration", "Q4 2026"),
    ("De Novo → Medicaid/CHIP",    "Rx DTx pricing", "APDTA path", "2028+"),
]
for i, (stream, price, note, timing) in enumerate(rev_rows):
    ry2 = Inches(2.1) + i * Inches(0.62)
    bg3 = BCG_OFFWHITE if i % 2 == 0 else WHITE
    rect(s, Inches(0.38), ry2, Inches(5.8), Inches(0.58), bg3,
         line_color=BCG_SILVER, line_w=0.3)
    tc = BCG_GREEN if i == 0 else BCG_CHARCOAL
    tb(s, stream,  Inches(0.5),  ry2 + Inches(0.1), Inches(2.3), Inches(0.38), size=11, bold=(i==0), color=tc)
    tb(s, price,   Inches(2.85), ry2 + Inches(0.1), Inches(1.2), Inches(0.38), size=11, bold=True, color=BCG_GREEN)
    tb(s, note,    Inches(4.1),  ry2 + Inches(0.1), Inches(1.2), Inches(0.38), size=9, color=BCG_GRAY)
    tag(s, timing, Inches(5.35), ry2 + Inches(0.14),
        BCG_GREEN if timing == "Launch" else BCG_TEAL,
        w=Inches(0.78), h=Inches(0.28))

# Right: GTM 3 tracks
tb(s, "GO-TO-MARKET TRACKS",
   Inches(6.5), Inches(1.62), Inches(6.45), Inches(0.38),
   size=12, bold=True, color=BCG_CHARCOAL)
rule(s, Inches(6.5), Inches(2.02), Inches(6.45), BCG_GREEN, h_pt=1.5)

gtm_tracks = [
    (BCG_GREEN,    "Track 1 — B2C Direct",
     ["Free app + $49 band → app store (iOS + Android)",
      "Target: parents ages 25–40, children ages 3–7",
      "CAC: parenting blogs, pediatrician waiting rooms, TikTok",
      "HSA/FSA eligible from launch"]),
    (BCG_TEAL,     "Track 2 — B2B Institutional",
     ["School district site licensing — Title I priority",
      "Library lending program (equity access)",
      "IDEA early intervention codes (ages 0–3) — federal funding",
      "OT community session network — evidence generation"]),
    (BCG_CHARCOAL, "Track 3 — Clinical Channel",
     ["PDF report: fits 15-min well-child visit (now)",
      "SMART on FHIR v1.5 — pediatrician portal",
      "AAP Bright Futures alignment → endorsement path",
      "De Novo FDA → Medicaid/CHIP (APDTA, 2028)"]),
]
for i, (col, title, items) in enumerate(gtm_tracks):
    ty2 = Inches(2.12) + i * Inches(1.64)
    rect(s, Inches(6.5), ty2, Inches(6.45), Inches(1.5),
         BCG_OFFWHITE, line_color=col, line_w=1)
    rect(s, Inches(6.5), ty2, Inches(0.1), Inches(1.5), col)
    tb(s, title, Inches(6.7), ty2 + Inches(0.1),
       Inches(6.1), Inches(0.38), size=12, bold=True, color=col)
    for j, item in enumerate(items):
        tb(s, "—  " + item,
           Inches(6.7), ty2 + Inches(0.54) + j * Inches(0.22),
           Inches(6.1), Inches(0.26), size=10, color=BCG_MID)

# Unit economics callout
rect(s, Inches(0.38), Inches(6.02), Inches(5.8), Inches(0.82), BCG_GREEN)
tb(s, "Unit economics (Year 3 model)",
   Inches(0.55), Inches(6.08), Inches(3), Inches(0.3),
   size=10, bold=True, color=WHITE)
tb(s, "LTV: ~$380  ·  CAC target: <$45  ·  LTV:CAC = 8.4×  ·  Gross margin (software): 82%",
   Inches(0.55), Inches(6.38), Inches(5.5), Inches(0.35),
   size=11, bold=True, color=BCG_LIME)

bcg_footer(s); slide_num(s, 10)


# ═══════════════════════════════════════════════════════
# SLIDE 11 — REGULATORY PATHWAY
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Regulatory & Compliance — Launch-Ready Today",
           "FDA General Wellness covers v1. Wearable adds FDA Class II pathway for v2.")

# Two columns
# Left — NOW (green)
rect(s, Inches(0.38), Inches(1.62), Inches(5.9), Inches(5.45),
     RGBColor(0xE8, 0xF5, 0xF1), line_color=BCG_GREEN, line_w=1)
rect(s, Inches(0.38), Inches(1.62), Inches(5.9), Inches(0.52), BCG_GREEN)
tb(s, "✓  V1 LAUNCH — FDA General Wellness",
   Inches(0.55), Inches(1.7), Inches(5.5), Inches(0.38),
   size=13, bold=True, color=WHITE)

green2 = [
    ("Camera gesture tracking + wellness summaries",
     "Covered: FDA General Wellness Guidance, Jan 6 2026"),
    ("Activity prescription from movement data",
     "Covered: Wellness coaching, not medical treatment"),
    ("Wearable as wellness tracker (non-diagnostic)",
     "Covered: Non-invasive sensing + longitudinal wellness output"),
    ("Gap report: 'grip strength is developing'",
     "Covered: Plain-language wellness progress summary"),
    ("'Consider seeing an OT' prompt",
     "Covered: FDA allows professional referral prompts"),
]
for i, (item, note) in enumerate(green2):
    iy2 = Inches(2.3) + i * Inches(0.85)
    dot(s, Inches(0.7), iy2 + Inches(0.17), Inches(0.07), BCG_GREEN)
    tb(s, item, Inches(0.88), iy2,
       Inches(5.2), Inches(0.35), size=11, bold=True, color=BCG_CHARCOAL)
    tb(s, note, Inches(0.88), iy2 + Inches(0.36),
       Inches(5.2), Inches(0.36), size=9.5, color=BCG_TEAL, italic=True)

# Right — future path
rect(s, Inches(6.55), Inches(1.62), Inches(6.4), Inches(2.55),
     RGBColor(0xF5, 0xF0, 0xE8), line_color=BCG_ORANGE, line_w=1)
rect(s, Inches(6.55), Inches(1.62), Inches(6.4), Inches(0.52), BCG_ORANGE)
tb(s, "→  V2 WEARABLE — FDA Class II Path",
   Inches(6.72), Inches(1.7), Inches(6.0), Inches(0.38),
   size=13, bold=True, color=WHITE)

orange_items = [
    ("EMG diagnostic claims → 510(k) predicate",  "Predicate: Noraxon Ultium EMG"),
    ("Grip force diagnostic → Class II 510(k)",    "Predicate: Jamar dynamometer SW"),
    ("DTx reimbursement pathway",                  "APDTA De Novo → Medicaid/CHIP"),
]
for i, (item, note) in enumerate(orange_items):
    iy3 = Inches(2.28) + i * Inches(0.68)
    dot(s, Inches(6.88), iy3 + Inches(0.17), Inches(0.07), BCG_ORANGE)
    tb(s, item, Inches(7.05), iy3,
       Inches(5.7), Inches(0.32), size=11, bold=True, color=BCG_CHARCOAL)
    tb(s, note, Inches(7.05), iy3 + Inches(0.32),
       Inches(5.7), Inches(0.3), size=9.5, color=BCG_ORANGE, italic=True)

# COPPA box
rect(s, Inches(6.55), Inches(4.38), Inches(6.4), Inches(2.69),
     RGBColor(0xF5, 0xF5, 0xE8), line_color=BCG_GOLD, line_w=1)
rect(s, Inches(6.55), Inches(4.38), Inches(6.4), Inches(0.52), BCG_GOLD)
tb(s, "⚠  COPPA 2025 — Deadline April 22 2026",
   Inches(6.72), Inches(4.46), Inches(6.0), Inches(0.38),
   size=13, bold=True, color=WHITE)

coppa2 = [
    "Parent account only — child never registers",
    "Verifiable parental consent before camera/band activates",
    "No 3rd-party analytics / ad SDKs in codebase",
    "Biometric data (EMG, grip, camera) = COPPA 2025 personal info",
    "$53,088 per violation — architecture built before any testing",
]
for i, item in enumerate(coppa2):
    dot(s, Inches(6.88), Inches(5.04) + i * Inches(0.38), Inches(0.06), BCG_GOLD)
    tb(s, item, Inches(7.05), Inches(4.96) + i * Inches(0.38),
       Inches(5.7), Inches(0.34), size=10.5, color=BCG_CHARCOAL)

bcg_footer(s); slide_num(s, 11)


# ═══════════════════════════════════════════════════════
# SLIDE 12 — ROADMAP (BCG waterfall timeline)
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
white_bg(s)
bcg_header(s, "Development Roadmap — 24-Month Critical Path",
           "Field validation → MVP → wearable v1 → clinical evidence → FDA path.")

phases = [
    {
        "period": "Now → Q2 2026",
        "color":  BCG_GREEN,
        "title":  "Validation & Architecture",
        "items":  [
            "Parent field interviews (n=10, ages 3–7)",
            "Pediatric OT session shadow",
            "COPPA architecture build",
            "Wearable sensor selection (grip + EMG)",
            "Gesture prototype (MediaPipe)",
            "Lock need statement",
        ]
    },
    {
        "period": "Q3 2026",
        "color":  BCG_TEAL,
        "title":  "MVP Launch",
        "items":  [
            "App store launch (iOS + Android)",
            "Free tier + premium subscription",
            "Band v1 (grip + accel + gyro)",
            "HSA/FSA filing",
            "OT community pilot (evidence gen)",
            "PDF report for pediatricians",
        ]
    },
    {
        "period": "Q4 2026",
        "color":  BCG_MID,
        "title":  "Scale & Clinical",
        "items":  [
            "Band v1.5 + EMG sensor added",
            "School/library B2B pilots",
            "SMART on FHIR v1.5",
            "AAP pilot data collection begins",
            "Series A fundraising",
            "Expand to ages 0–3 (IDEA codes)",
        ]
    },
    {
        "period": "2027–2028",
        "color":  BCG_CHARCOAL,
        "title":  "Clinical Evidence & Clearance",
        "items":  [
            "AAP peer-reviewed publication",
            "510(k) / De Novo FDA filing",
            "Epic/Cerner FHIR v2 integration",
            "Medicaid/CHIP pathway (APDTA)",
            "International expansion (EU MDR)",
            "Series B",
        ]
    },
]

ph_w = Inches(3.0)
for i, ph in enumerate(phases):
    px2 = Inches(0.38) + i * (ph_w + Inches(0.2))
    # period bar
    rect(s, px2, Inches(1.62), ph_w, Inches(0.48), ph["color"])
    tb(s, ph["period"], px2 + Inches(0.12), Inches(1.68),
       ph_w - Inches(0.2), Inches(0.36), size=11, bold=True, color=WHITE)
    # title bar
    rect(s, px2, Inches(2.1), ph_w, Inches(0.42),
         RGBColor(0xE8, 0xF5, 0xF1) if i == 0 else BCG_OFFWHITE,
         line_color=ph["color"], line_w=0.5)
    tb(s, ph["title"], px2 + Inches(0.12), Inches(2.15),
       ph_w - Inches(0.2), Inches(0.34), size=12, bold=True, color=ph["color"])
    # items
    rect(s, px2, Inches(2.52), ph_w, Inches(4.55),
         BCG_OFFWHITE, line_color=ph["color"], line_w=0.5)
    for j, item in enumerate(ph["items"]):
        jy2 = Inches(2.65) + j * Inches(0.68)
        dot(s, px2 + Inches(0.22), jy2 + Inches(0.16), Inches(0.065), ph["color"])
        tb(s, item, px2 + Inches(0.4), jy2,
           ph_w - Inches(0.52), Inches(0.56), size=10.5, color=BCG_MID)

# milestone arrow at bottom
rule(s, Inches(0.38), Inches(7.2), W - Inches(0.76), BCG_GREEN, h_pt=2)
for i, (milestone, col) in enumerate([
    ("Field validation", BCG_GREEN),
    ("App launch", BCG_TEAL),
    ("Band v1", BCG_TEAL),
    ("AAP data", BCG_MID),
    ("FDA filing", BCG_CHARCOAL),
]):
    mx2 = Inches(0.38) + i * Inches(2.42)
    dot(s, mx2 + Inches(0.12), Inches(7.2), Inches(0.09), col)
    tb(s, milestone, mx2 + Inches(0.25), Inches(7.12),
       Inches(2.2), Inches(0.28), size=9, color=col, bold=True)

bcg_footer(s); slide_num(s, 12)


# ═══════════════════════════════════════════════════════
# SLIDE 13 — THE ASK (BCG closing page)
# ═══════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
dark_bg(s)
rect(s, 0, 0, Inches(0.22), H, BCG_GREEN)

tb(s, "The Investment Case",
   Inches(0.42), Inches(0.55),
   Inches(12.5), Inches(1.0),
   size=48, bold=True, color=WHITE)

rule(s, Inches(0.42), Inches(1.65), Inches(8), BCG_GREEN, h_pt=2)

# Core thesis
rect(s, Inches(0.42), Inches(1.85), Inches(12.5), Inches(1.2), BCG_DARK)
tb(s,
   "MotionMind is the only system that combines a wearable sensor band with camera gesture tracking "
   "to detect 7/8 developmental gaps in children and deliver gap-specific prescriptions — "
   "at zero parent effort, without removing screens, on hardware families already own plus a $49 band.",
   Inches(0.62), Inches(1.95),
   Inches(12.15), Inches(1.0),
   size=13, color=BCG_SILVER)

# 3 ask cards
asks2 = [
    (BCG_GREEN, "Seed Round", "$750K – $1.2M",
     ["Wearable band v1 (grip + accel + gyro)",
      "COPPA architecture",
      "App MVP + gesture engine",
      "OT evidence generation (n=50)",
      "HSA/FSA filing"]),
    (BCG_TEAL, "Advisors Needed", "Clinical & Technical",
     ["Pediatric OT (gap assessment validation)",
      "Children's hospital research partner",
      "Wearable hardware engineer",
      "FDA regulatory counsel",
      "AAP Section on Dev. Pediatrics"]),
    (BCG_MID, "Pilot Partners", "3–5 Sites",
     ["Pediatric OT practices (PDF report pilot)",
      "Title I school districts (B2B GTM)",
      "Library system (equity access)",
      "Early intervention program (IDEA 0–3)",
      "Children's hospital (AAP data)"]),
]

ak_w = Inches(4.0)
for i, (col, title, sub, items) in enumerate(asks2):
    ax3 = Inches(0.42) + i * (ak_w + Inches(0.23))
    ay3 = Inches(3.25)
    rect(s, ax3, ay3, ak_w, Inches(3.65), BCG_DARK,
         line_color=col, line_w=1)
    rect(s, ax3, ay3, ak_w, Inches(0.08), col)
    tb(s, title, ax3 + Inches(0.18), ay3 + Inches(0.18),
       ak_w - Inches(0.3), Inches(0.38), size=14, bold=True, color=col)
    tb(s, sub, ax3 + Inches(0.18), ay3 + Inches(0.58),
       ak_w - Inches(0.3), Inches(0.3), size=11, color=BCG_SILVER)
    rule(s, ax3 + Inches(0.18), ay3 + Inches(0.95),
         ak_w - Inches(0.36), col, h_pt=1)
    for j, item in enumerate(items):
        dot(s, ax3 + Inches(0.3), ay3 + Inches(1.15) + j * Inches(0.48),
            Inches(0.058), col)
        tb(s, item, ax3 + Inches(0.48), ay3 + Inches(1.05) + j * Inches(0.48),
           ak_w - Inches(0.6), Inches(0.42), size=11, color=BCG_SILVER)

# Contact / footer
rect(s, Inches(0.42), Inches(7.12), Inches(12.5), Inches(0.2), BCG_DARK)
tb(s, "MotionMind  ·  Stanford CIM206 — Biodesign for Digital Health  ·  March 2026  ·  [contact@motionmind.com]",
   Inches(0.42), Inches(7.14), Inches(12.5), Inches(0.24),
   size=10, color=BCG_GRAY, align=PP_ALIGN.CENTER)

bcg_footer(s); slide_num(s, 13)


# ─────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────
out = "MotionMind_BCG_Deck.pptx"
prs.save(out)
print(f"✅  Saved: {out}  ({len(prs.slides)} slides)")
