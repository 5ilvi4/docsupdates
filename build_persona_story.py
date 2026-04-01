"""
MotionMind — Persona Story Deck
A narrative-driven storytelling PowerPoint that follows
Lena (age 6) and her mom Maya through the MotionMind journey.
BCG-flavored design with full-bleed illustrations.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
import os

# ─────────────────────────────────────────────────
# PALETTE
# ─────────────────────────────────────────────────
GREEN      = RGBColor(0x00, 0x73, 0x5C)
TEAL       = RGBColor(0x00, 0xA8, 0x8A)
LIME       = RGBColor(0x6C, 0xC2, 0x4A)
CHARCOAL   = RGBColor(0x1A, 0x1A, 0x2E)
DARK       = RGBColor(0x2C, 0x2C, 0x3E)
MID        = RGBColor(0x4A, 0x4A, 0x6A)
SILVER     = RGBColor(0xD0, 0xD0, 0xE0)
OFFWHITE   = RGBColor(0xF5, 0xF5, 0xF7)
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
ORANGE     = RGBColor(0xE8, 0x6A, 0x1A)
GOLD       = RGBColor(0xF0, 0xA5, 0x00)

W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H
BLANK = prs.slide_layouts[6]

# ─────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────

def rect(slide, x, y, w, h, color, lc=None, lw=0):
    s = slide.shapes.add_shape(1, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    if lc:
        s.line.color.rgb = lc; s.line.width = Pt(lw)
    else:
        s.line.fill.background(); s.line.width = 0
    return s

def rr(slide, x, y, w, h, color, lc=None, lw=0):
    s = slide.shapes.add_shape(5, x, y, w, h)
    s.fill.solid(); s.fill.fore_color.rgb = color
    if lc:
        s.line.color.rgb = lc; s.line.width = Pt(lw)
    else:
        s.line.fill.background(); s.line.width = 0
    return s

def tb(slide, text, x, y, w, h, size=12, bold=False, color=CHARCOAL,
       align=PP_ALIGN.LEFT, italic=False, name="Calibri"):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = text
    r.font.size = Pt(size); r.font.bold = bold; r.font.italic = italic
    r.font.color.rgb = color; r.font.name = name
    return box

def mtb(slide, lines, x, y, w, h, sizes, bolds, colors,
        align=PP_ALIGN.LEFT, name="Calibri", spacing=6):
    box = slide.shapes.add_textbox(x, y, w, h)
    tf = box.text_frame; tf.word_wrap = True
    for i, (line, sz, bd, col) in enumerate(zip(lines, sizes, bolds, colors)):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align
        if i > 0:
            p.space_before = Pt(spacing)
        r = p.add_run(); r.text = line
        r.font.size = Pt(sz); r.font.bold = bd
        r.font.color.rgb = col; r.font.name = name
    return box

def rule(slide, x, y, w, color=GREEN, h_pt=2):
    rect(slide, x, y, w, Pt(h_pt), color)

def img(slide, path, x, y, w, h):
    if os.path.exists(path):
        slide.shapes.add_picture(path, x, y, w, h)

def footer(slide, text="MotionMind  ·  Confidential  ·  March 2026"):
    rect(slide, 0, H - Inches(0.3), W, Inches(0.3), GREEN)
    tb(slide, text, Inches(0.4), H - Inches(0.28),
       W - Inches(1.2), Inches(0.25), size=9, color=WHITE)

def slide_num(slide, n, total=10):
    tb(slide, f"{n} / {total}", W - Inches(1.0), H - Inches(0.28),
       Inches(0.9), Inches(0.25), size=9, color=WHITE,
       align=PP_ALIGN.RIGHT)

def chapter_tag(slide, text, color=GREEN):
    rr(slide, Inches(0.38), Inches(0.22), Inches(2.6), Inches(0.38), color)
    tb(slide, text, Inches(0.5), Inches(0.26), Inches(2.4), Inches(0.3),
       size=11, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

def stat_pill(slide, label, value, x, y, w=Inches(2.4), h=Inches(1.1),
              accent=GREEN):
    rr(slide, x, y, w, h, OFFWHITE, lc=accent, lw=1)
    rect(slide, x, y, w, Pt(3), accent)
    tb(slide, value, x + Inches(0.14), y + Inches(0.1),
       w - Inches(0.28), Inches(0.5), size=28, bold=True, color=accent)
    tb(slide, label, x + Inches(0.14), y + Inches(0.62),
       w - Inches(0.28), Inches(0.38), size=10, color=MID)


# ════════════════════════════════════════════════
# SLIDE 1 — STORY COVER
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)

# Left — dark panel with title
rect(s, 0, 0, Inches(5.8), H, CHARCOAL)
rect(s, 0, 0, Inches(0.18), H, GREEN)

tb(s, "A Story About",
   Inches(0.38), Inches(0.9),
   Inches(5.2), Inches(0.55),
   size=18, color=TEAL, italic=True)

tb(s, "Lena.",
   Inches(0.38), Inches(1.42),
   Inches(5.2), Inches(1.3),
   size=88, bold=True, color=WHITE, name="Calibri")

rule(s, Inches(0.38), Inches(2.82), Inches(4.6), GREEN, h_pt=2)

tb(s,
   "Age 6. Loves drawing — but her hand gives out\n"
   "after two minutes. Her mom Maya has no idea why.",
   Inches(0.38), Inches(3.0),
   Inches(5.2), Inches(1.1),
   size=15, color=SILVER)

tb(s,
   "The iPad was never designed for a 6-year-old's body.\n"
   "MotionMind is the layer that changes how kids\n"
   "interact with the screens they already use.",
   Inches(0.38), Inches(4.22),
   Inches(5.2), Inches(1.0),
   size=13, color=RGBColor(0x80, 0xC0, 0xA8))

# Product badge
rr(s, Inches(0.38), Inches(5.5), Inches(2.8), Inches(0.52), GREEN)
tb(s, "MotionMind", Inches(0.52), Inches(5.56),
   Inches(2.5), Inches(0.38), size=18, bold=True, color=WHITE)
tb(s, "Wearable Development System",
   Inches(0.38), Inches(6.1), Inches(5.2), Inches(0.35),
   size=11, color=SILVER)

# Right — illustration
img(s, "persona_01_lena_intro.png",
    Inches(5.8), 0, Inches(7.53), H)

# Subtle overlay on right image
rect(s, Inches(5.8), H - Inches(1.2), Inches(7.53), Inches(0.9),
     RGBColor(0x00, 0x00, 0x00))
tb(s, "Stanford CIM206 — Biodesign for Digital Health  ·  March 2026",
   Inches(6.1), H - Inches(1.1),
   Inches(6.9), Inches(0.35),
   size=11, color=SILVER, italic=True)

footer(s); slide_num(s, 1)


# ════════════════════════════════════════════════
# SLIDE 2 — MEET LENA & MAYA
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)

# Full-bleed illustration (left 60%)
img(s, "persona_01_lena_intro.png",
    0, 0, Inches(8.0), H)

# Dark gradient overlay on left side for text
rect(s, 0, 0, Inches(4.2), H, RGBColor(0x0A, 0x0A, 0x1A))

# Right panel
rect(s, Inches(8.0), 0, Inches(5.33), H, OFFWHITE)
rect(s, Inches(8.0), 0, Inches(0.08), H, GREEN)

chapter_tag(s, "CHAPTER 1 — THE FAMILY", GREEN)

tb(s, "Meet Lena.",
   Inches(8.2), Inches(0.55),
   Inches(4.9), Inches(0.72),
   size=40, bold=True, color=CHARCOAL)
rule(s, Inches(8.2), Inches(1.32), Inches(4.6), GREEN)

mtb(s,
    ["Age 6. Lives in San Jose.",
     "Loves drawing — but her hand gives out after 2 minutes.",
     "Her family is one of millions navigating screens",
     "without a tool to understand what her body actually needs."],
    Inches(8.2), Inches(1.45), Inches(4.85), Inches(1.5),
    [13, 13, 13, 13], [True, False, False, False],
    [CHARCOAL, MID, MID, MID],
    spacing=8)

rule(s, Inches(8.2), Inches(3.08), Inches(4.6), SILVER)

tb(s, "Meet Maya.",
   Inches(8.2), Inches(3.22),
   Inches(4.9), Inches(0.6),
   size=32, bold=True, color=CHARCOAL)

mtb(s,
    ["Age 34. Product manager. Two kids.",
     "Lena's mom.",
     "71% of parents are concerned their child spends",
     "too much time on screens — and have no idea when",
     "it becomes clinical or who to call.  (Pew Research, 2020)"],
    Inches(8.2), Inches(3.88), Inches(4.85), Inches(1.9),
    [13, 13, 13, 13, 13], [True, False, False, False, True],
    [CHARCOAL, MID, MID, MID, GREEN],
    spacing=8)

# Text on the dark left overlay
tb(s, "\"She should be\nholding her pencil\nbetter by now.\"",
   Inches(0.3), Inches(2.5),
   Inches(3.6), Inches(1.6),
   size=22, bold=True, color=WHITE, italic=True)
tb(s, "— Maya, composite parent persona\n  grounded in field research",
   Inches(0.3), Inches(4.12),
   Inches(3.6), Inches(0.55),
   size=11, color=TEAL)

footer(s); slide_num(s, 2)


# ════════════════════════════════════════════════
# SLIDE 3 — THE WORRY (MAYA'S CONCERN)
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)

rect(s, 0, 0, W, H, OFFWHITE)

# Left: text panel
rect(s, 0, 0, Inches(5.4), H, WHITE)
rect(s, 0, 0, Inches(0.18), H, ORANGE)

chapter_tag(s, "CHAPTER 2 — THE WORRY", ORANGE)

tb(s, "Maya sees it.\nThe screen isn't\nthe problem.",
   Inches(0.38), Inches(0.72),
   Inches(4.8), Inches(2.2),
   size=34, bold=True, color=CHARCOAL, name="Calibri")

rule(s, Inches(0.38), Inches(3.02), Inches(4.6), ORANGE)

# Only use stats directly from the source deck with citations
worry_items = [
    ("iPads & tablets were designed for adults — not developing hands",
     "Touchscreen interaction requires pinch/swipe → skips grip, fine motor, posture", ORANGE),
    ("54% of parents say their child is addicted to screens",
     "Source: cited in Stanford CIM206 source deck", ORANGE),
    ("93% of screen-off moments trigger conflict",
     "37% say it almost always ends in a fight (Hiniker et al., 2016)", ORANGE),
    ("28% of parents give in to screens to avoid meltdowns — multiple times/week",
     "Source: Lurie Children's Hospital, 2025", CHARCOAL),
    ("OT waitlist: 6 months in most US metro areas",
     "Field observation — no centralized data; consistent across parent reports", MID),
]
for i, (text, note, col) in enumerate(worry_items):
    ty = Inches(3.18) + i * Inches(0.72)
    rect(s, Inches(0.38), ty + Inches(0.1), Pt(3), Inches(0.32), col)
    tb(s, text, Inches(0.58), ty,
       Inches(4.6), Inches(0.35), size=12, bold=True, color=col)
    tb(s, note, Inches(0.58), ty + Inches(0.34),
       Inches(4.6), Inches(0.28), size=9.5, color=SILVER if col == MID else MID,
       italic=True)

# Right: full illustration
img(s, "persona_02_maya_concern.png",
    Inches(5.4), 0, Inches(7.93), H)

# dim bottom of image for footer
rect(s, Inches(5.4), H - Inches(0.3), Inches(7.93), Inches(0.3),
     RGBColor(0x00, 0x73, 0x5C))

footer(s); slide_num(s, 3)


# ════════════════════════════════════════════════
# SLIDE 4 — THE GAP (WHY NOTHING WORKS)
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, WHITE)
rect(s, 0, 0, Inches(0.18), H, GREEN)

chapter_tag(s, "CHAPTER 2.5 — THE MARKET GAP", MID)

tb(s, "The screen isn't the enemy.\nThe interaction design is.",
   Inches(0.38), Inches(0.68),
   W - Inches(0.76), Inches(0.9),
   size=34, bold=True, color=CHARCOAL)
rule(s, Inches(0.38), Inches(1.62), W - Inches(0.76), GREEN)

tb(s, "Every tool below was designed for adults — or for entertainment. None was built around how a child's body actually develops.",
   Inches(0.38), Inches(1.72), W - Inches(0.76), Inches(0.38),
   size=12, italic=True, color=MID)

# 5 product columns
products = [
    ("📱 Standard\nTablet Apps", RGBColor(0xCC, 0x44, 0x44),
     ["Designed for adults", "Tap & swipe only", "No grip or posture",
      "No motor output", "Score: 0/8 dev gaps"]),
    ("🔇 Screen Time\nManagement", RGBColor(0xDD, 0x77, 0x22),
     ["Controls quantity", "Ignores interaction quality",
      "No skill building", "Increases conflict",
      "Score: 0/8 dev gaps"]),
    ("🕹️ Motion Games\n(Kinect, Nex)", RGBColor(0x44, 0x88, 0xCC),
     ["Gross motor only", "No handgrip data",
      "No fine motor", "No prescription",
      "Score: 3/8 dev gaps"]),
    ("📚 Osmo / Tablet\n+ Accessories", RGBColor(0x88, 0x66, 0xAA),
     ["Visual-spatial only", "No body sensing",
      "No wearable layer", "No gap scoring",
      "Score: 2/8 dev gaps"]),
    ("🏥 Pediatric OT",  GREEN,
     ["Best clinical tool", "But: 6-month wait",
      "$150–$300/session", "Insurance barriers",
      "Score: 8/8 (inaccessible)"]),
]

col_w2 = Inches(2.44)
for i, (name, col, items) in enumerate(products):
    cx2 = Inches(0.38) + i * (col_w2 + Inches(0.08))
    rect(s, cx2, Inches(1.62), col_w2, Inches(0.52), col)
    tb(s, name, cx2 + Inches(0.1), Inches(1.65),
       col_w2 - Inches(0.2), Inches(0.48),
       size=12, bold=True, color=WHITE)
    rect(s, cx2, Inches(2.14), col_w2, Inches(4.2), OFFWHITE,
         lc=col, lw=0.5)
    for j, item in enumerate(items):
        iy2 = Inches(2.25) + j * Inches(0.74)
        is_score = item.startswith("Score")
        tb(s, item, cx2 + Inches(0.12), iy2,
           col_w2 - Inches(0.24), Inches(0.62),
           size=11, bold=is_score, color=col if is_score else MID)

# Bottom: MotionMind solves this
rect(s, Inches(0.38), Inches(6.44), W - Inches(0.76), Inches(0.72), GREEN)
tb(s,
   "MotionMind  =  Wearable band (grip + EMG)  +  Camera hand-tracking  +  AI layer  →  Transforms every screen session into developmental therapy. 7/8 gaps. At home.",
   Inches(0.58), Inches(6.56), W - Inches(1.15), Inches(0.52),
   size=13, bold=True, color=WHITE)

footer(s); slide_num(s, 4)


# ════════════════════════════════════════════════
# SLIDE 5 — THE DISCOVERY (UNBOXING + FIRST PLAY)
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)

# Full-bleed illustration
img(s, "persona_03_discovery.png",
    0, 0, W, H)

# Left text overlay
rect(s, 0, 0, Inches(5.2), H, RGBColor(0x00, 0x0A, 0x08))

rect(s, 0, 0, Inches(0.18), H, GREEN)

chapter_tag(s, "CHAPTER 3 — THE DISCOVERY", GREEN)

tb(s, "First session.",
   Inches(0.38), Inches(0.72),
   Inches(4.6), Inches(1.0),
   size=48, bold=True, color=WHITE)

rule(s, Inches(0.38), Inches(1.82), Inches(4.2), GREEN)

mtb(s,
    ["Lena wears the MotionMind band on her wrist.",
     "The hand-tracking game activates on the tablet.",
     "Google MediaPipe reads 21 hand skeleton points",
     "at <10ms latency — no special hardware needed.",
     "The band logs grip force and wrist movement live.",
     "The app scores 7 developmental gaps automatically."],
    Inches(0.38), Inches(2.0), Inches(4.6), Inches(2.5),
    [13]*6, [True, False, False, False, False, True],
    [GREEN, SILVER, SILVER, SILVER, SILVER, WHITE],
    spacing=10)

# Quote — kept as illustrative persona narrative, clearly labeled
rr(s, Inches(0.38), Inches(4.82), Inches(4.6), Inches(1.35),
   RGBColor(0x0A, 0x22, 0x1A), lc=GREEN, lw=1)
tb(s, "\"93% of parents report screen-off conflicts at\nleast occasionally. 37% say it almost always\nends in a fight.\"",
   Inches(0.56), Inches(4.92), Inches(4.3), Inches(0.9),
   size=13, color=WHITE, italic=True)
tb(s, "— Hiniker et al., 2016  (why engagement matters from minute one)",
   Inches(0.56), Inches(5.82), Inches(4.3), Inches(0.35),
   size=11, color=TEAL)

footer(s); slide_num(s, 5)


# ════════════════════════════════════════════════
# SLIDE 6 — THE INSIGHT (REPORT CARD)
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)

rect(s, 0, 0, W, H, OFFWHITE)

# Right: illustration
img(s, "persona_04_insight.png",
    Inches(6.8), 0, Inches(6.53), H)
rect(s, Inches(6.8), 0, Inches(0.08), H, GREEN)

chapter_tag(s, "CHAPTER 4 — THE INSIGHT", TEAL)

tb(s, "Maya opens\nthe report.",
   Inches(0.38), Inches(0.72),
   Inches(6.0), Inches(1.7),
   size=44, bold=True, color=CHARCOAL)

rule(s, Inches(0.38), Inches(2.5), Inches(6.0), TEAL)

tb(s, "After the first session, the app generates Lena's\ndevelopmental gap profile — automatically.\nNo clinical visit. No questionnaire.",
   Inches(0.38), Inches(2.65),
   Inches(6.0), Inches(1.0),
   size=14, color=MID)

# Gap scorecard
# NOTE: Status labels are illustrative for persona narrative.
# Specific percentage scores are pending field validation with licensed OT.
tb(s, "Illustrative gap profile — pending OT field validation:",
   Inches(0.38), Inches(3.72),
   Inches(6.0), Inches(0.28),
   size=9, italic=True, color=SILVER)

gap_data = [
    ("Fine motor precision",  "On Track",    GREEN),
    ("Handgrip strength",     "Needs Focus", ORANGE),
    ("Muscle quality",        "Needs Focus", ORANGE),
    ("Gross motor",           "On Track",    GREEN),
    ("Visual-motor",          "On Track",    GREEN),
    ("Vestibular",            "On Track",    TEAL),
]
bar_fills = [0.78, 0.52, 0.45, 0.88, 0.85, 0.68]   # visual proportions only
for i, (name, status, col) in enumerate(gap_data):
    gy2 = Inches(4.08) + i * Inches(0.49)
    bar_max = Inches(2.8)
    bar_fill = bar_max * bar_fills[i]
    rect(s, Inches(0.38), gy2 + Pt(10), bar_max, Pt(18),
         RGBColor(0xDD, 0xDD, 0xEE))
    rect(s, Inches(0.38), gy2 + Pt(10), bar_fill, Pt(18), col)
    tb(s, name, Inches(3.35), gy2,
       Inches(2.0), Inches(0.42), size=11, color=MID)
    tag_bg  = RGBColor(0xE0, 0xF5, 0xEA) if status == "On Track" else RGBColor(0xFF, 0xEE, 0xDD)
    tag_col = GREEN if status == "On Track" else ORANGE
    rr(s, Inches(5.5), gy2 + Pt(4), Inches(1.22), Pt(22), tag_bg, lc=tag_col, lw=0.5)
    tb(s, status, Inches(5.56), gy2 + Pt(6), Inches(1.1), Pt(18),
       size=9, bold=True, color=tag_col, align=PP_ALIGN.CENTER)

# Prescription — activity types are evidence-based OT practice; session length is illustrative
rr(s, Inches(0.38), Inches(7.06), Inches(6.0), Inches(0.22), GREEN)
tb(s, "Gap-matched Rx: Playdough squeeze · Finger obstacle course · Lego sorting  (OT-designed, household objects)",
   Inches(0.55), Inches(7.1), Inches(5.7), Inches(0.18),
   size=10, bold=True, color=WHITE)

# Quote — labeled as persona narrative, not a real testimonial
tb(s, "Persona narrative: \"I finally have a name for it. And a next step.\"",
   Inches(0.38), Inches(6.78), Inches(6.0), Inches(0.25),
   size=11, italic=True, color=SILVER)

footer(s); slide_num(s, 6)


# ════════════════════════════════════════════════
# SLIDE 7 — THE TRANSFORMATION
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)

# Full-bleed illustration
img(s, "persona_05_transformation.png",
    0, 0, W, H)

# Right overlay
rect(s, Inches(8.4), 0, Inches(4.93), H, RGBColor(0x00, 0x12, 0x0C))
rect(s, Inches(8.4), 0, Inches(0.12), H, LIME)

chapter_tag(s, "CHAPTER 5 — THE TRANSFORMATION", LIME)

tb(s, "Week 4.",
   Inches(8.6), Inches(0.72),
   Inches(4.6), Inches(0.72),
   size=48, bold=True, color=WHITE)

rule(s, Inches(8.6), Inches(1.5), Inches(4.3), LIME)

# Outcome framing — qualitative, grounded in OT literature
# Specific % gains are pending pilot data (Target: Q3 2026 field validation)
tb(s, "Pilot outcomes — target Q3 2026",
   Inches(8.6), Inches(1.62), Inches(4.3), Inches(0.28),
   size=10, italic=True, color=SILVER)

progress = [
    ("Grip strength",    "↑ Improving",  LIME),
    ("Fine motor",       "↑ Improving",  TEAL),
    ("Drawing sessions", "↑ Engaged",    WHITE),
    ("Screen conflicts", "↓ Reducing",   LIME),
    ("Completed tasks",  "↑ Consistent", TEAL),
]
for i, (label, val, col) in enumerate(progress):
    py = Inches(2.02) + i * Inches(0.78)
    rect(s, Inches(8.6), py, Inches(4.3), Pt(1), RGBColor(0x20, 0x40, 0x30))
    tb(s, val, Inches(8.6), py + Pt(2),
       Inches(1.7), Inches(0.52), size=22, bold=True, color=col)
    tb(s, label, Inches(10.35), py + Pt(8),
       Inches(2.5), Inches(0.42), size=13, color=SILVER)

rule(s, Inches(8.6), Inches(5.98), Inches(4.3), LIME)

# Quote — labeled as persona narrative, not a real testimonial
tb(s,
   "Persona narrative:\n\"She asked to draw instead\nof the tablet. For the first time.\"",
   Inches(8.6), Inches(6.14),
   Inches(4.5), Inches(1.1),
   size=14, bold=True, color=WHITE, italic=True)
tb(s, "— Maya (composite persona)",
   Inches(8.6), Inches(7.0), Inches(4.3), Inches(0.28),
   size=11, color=LIME)

footer(s); slide_num(s, 7)


# ════════════════════════════════════════════════
# SLIDE 8 — HOW IT WORKS (SYSTEM)
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, WHITE)
rect(s, 0, 0, Inches(0.18), H, GREEN)

chapter_tag(s, "HOW MOTIONMIND WORKS", GREEN)

tb(s, "Three layers. One complete system.",
   Inches(0.38), Inches(0.68),
   W - Inches(0.76), Inches(0.68),
   size=36, bold=True, color=CHARCOAL)
rule(s, Inches(0.38), Inches(1.42), W - Inches(0.76), GREEN)

# 3 layer cards
layers = [
    (GREEN,  "⌚  WEARABLE BAND",
     "$49 · Wrist sensor",
     ["Handgrip force sensor",
      "Surface EMG (muscle activity)",
      "3-axis accelerometer + gyroscope",
      "Skin conductance (arousal)",
      "→  Captures what camera CAN'T"]),
    (TEAL,   "📷  CAMERA SYSTEM",
     "No extra hardware needed",
     ["Google MediaPipe — 21-point hand skeleton",
      "Full body pose landmarks",
      "Gesture quality scoring",
      "Visual-motor reaction timing",
      "→  Works on any tablet/phone"]),
    (MID,    "🤖  AI PLATFORM",
     "Cloud + on-device",
     ["Fuses band + camera in real time",
      "Scores 7/8 developmental gaps",
      "Generates activity prescription",
      "Tracks progress week-over-week",
      "→  Parent report + clinician PDF"]),
]

cw3 = Inches(4.1)
for i, (col, title, sub, items) in enumerate(layers):
    cx3 = Inches(0.38) + i * (cw3 + Inches(0.12))
    rect(s, cx3, Inches(1.62), cw3, Inches(0.52), col)
    tb(s, title, cx3 + Inches(0.14), Inches(1.68),
       cw3 - Inches(0.28), Inches(0.42), size=13, bold=True, color=WHITE)
    rr(s, cx3, Inches(2.14), cw3, Inches(4.88),
       OFFWHITE, lc=col, lw=1)
    tb(s, sub, cx3 + Inches(0.16), Inches(2.22),
       cw3 - Inches(0.32), Inches(0.35),
       size=11, color=col, italic=True)
    rule(s, cx3 + Inches(0.16), Inches(2.6), cw3 - Inches(0.32), col, h_pt=1)
    for j, item in enumerate(items):
        jy3 = Inches(2.75) + j * Inches(0.72)
        is_last = item.startswith("→")
        dot_col = col
        if not is_last:
            # bullet dot
            pass
        rect(s, cx3 + Inches(0.16), jy3 + Inches(0.16),
             Pt(3), Pt(3), col)
        tb(s, item, cx3 + Inches(0.3), jy3,
           cw3 - Inches(0.46), Inches(0.6),
           size=12 if not is_last else 12,
           bold=is_last, color=CHARCOAL if not is_last else col)

# Bottom: 1 sentence
rr(s, Inches(0.38), Inches(7.12), W - Inches(0.76), Inches(0.28),
   RGBColor(0xE8, 0xF5, 0xF1), lc=GREEN, lw=1)
tb(s,
   "Zero clinical expertise required from parents.  "
   "COPPA 2025 compliant.  FDA General Wellness (Jan 2026).",
   Inches(0.58), Inches(7.16), W - Inches(1.15), Inches(0.22),
   size=11, color=GREEN)

footer(s); slide_num(s, 8)


# ════════════════════════════════════════════════
# SLIDE 9 — THE NUMBERS
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, CHARCOAL)
rect(s, 0, 0, Inches(0.18), H, GREEN)

chapter_tag(s, "THE NUMBERS", GREEN)

tb(s, "8M kids. Billions of screen hours.\nZero tools designed for their bodies.",
   Inches(0.38), Inches(0.72),
   W - Inches(0.76), Inches(1.1),
   size=38, bold=True, color=WHITE)

rule(s, Inches(0.38), Inches(1.68), W - Inches(0.76), GREEN)

# 6 stat cards — all figures sourced from CIM206_Biodesign_Deck(3).pptx
stats9 = [
    ("8M+",    "US children 0–11\nshowing symptoms\n(CDC / Boyle et al.)",              GREEN),
    ("82%",    "of adolescents don't\nmeet movement guidelines\n(WHO, Lancet 2019)",      ORANGE),
    ("6 hrs",  "average daily\nscreen time for children\n(source deck)",                  SILVER),
    ("$103B",  "child rehab + digital health\nmarket by 2034, 7% CAGR\n(source deck)",   TEAL),
    ("7–12×",  "ROI on early intervention\n(Heckman, heckmanequation.org)",              LIME),
    ("7/8",    "developmental gaps\nMotionMind closes\n(product claim)",                  GREEN),
]

sw4 = Inches(4.0)
for i, (val, label, col) in enumerate(stats9):
    ci2 = i % 3
    ri2 = i // 3
    sx4 = Inches(0.38) + ci2 * (sw4 + Inches(0.34))
    sy4 = Inches(2.0) + ri2 * Inches(2.45)
    rect(s, sx4, sy4, sw4, Inches(2.1), DARK, lc=col, lw=1)
    rect(s, sx4, sy4, sw4, Pt(3), col)
    tb(s, val, sx4 + Inches(0.2), sy4 + Inches(0.12),
       sw4 - Inches(0.4), Inches(0.95),
       size=56, bold=True, color=col)
    tb(s, label, sx4 + Inches(0.2), sy4 + Inches(1.1),
       sw4 - Inches(0.4), Inches(0.82),
       size=14, color=SILVER)

footer(s); slide_num(s, 9)


# ════════════════════════════════════════════════
# SLIDE 10 — CLOSING / CALL TO ACTION
# ════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK)

# Split: left dark, right illustration
rect(s, 0, 0, Inches(6.5), H, CHARCOAL)
rect(s, 0, 0, Inches(0.18), H, GREEN)
img(s, "persona_05_transformation.png",
    Inches(6.5), 0, Inches(6.83), H)
# overlay on right
rect(s, Inches(6.5), H - Inches(0.3), Inches(6.83), Inches(0.3), GREEN)

chapter_tag(s, "THE OPPORTUNITY", GREEN)

tb(s, "The screen isn't\nleaving. Let's fix\nwhat it does.",
   Inches(0.38), Inches(0.72),
   Inches(5.9), Inches(1.9),
   size=38, bold=True, color=WHITE)

rule(s, Inches(0.38), Inches(2.72), Inches(5.6), GREEN)

tb(s,
   "iPads and tablets were designed for adults.\n"
   "MotionMind is the first system built around\n"
   "how a child's body actually develops —\n"
   "turning every screen session into a chance\n"
   "to grow, not just consume.",
   Inches(0.38), Inches(2.9),
   Inches(5.8), Inches(1.8),
   size=14, color=SILVER)

rule(s, Inches(0.38), Inches(4.62), Inches(5.6), GREEN)

# Disclosure footnote
tb(s, "Lena & Maya are composite personas. All statistics sourced from CIM206_Biodesign_Deck(3).pptx.",
   Inches(0.38), Inches(4.68), Inches(5.8), Inches(0.28),
   size=9, italic=True, color=RGBColor(0x60, 0x90, 0x78))

# 3 mini CTAs
ctas = [
    (GREEN,  "Seed Round", "$750K–$1.2M  ·  Band v1 + App launch"),
    (TEAL,   "Pilot Sites", "3–5 OT practices + schools  ·  Q3 2026"),
    (LIME,   "Advisors",   "Pediatric OT  ·  FDA counsel  ·  HW engineer"),
]
for i, (col, title, sub) in enumerate(ctas):
    cy4 = Inches(4.82) + i * Inches(0.68)
    rect(s, Inches(0.38), cy4, Pt(4), Inches(0.52), col)
    tb(s, title, Inches(0.62), cy4 + Inches(0.04),
       Inches(1.5), Inches(0.42), size=13, bold=True, color=col)
    tb(s, sub, Inches(2.15), cy4 + Inches(0.06),
       Inches(4.1), Inches(0.38), size=12, color=SILVER)

tb(s, "MotionMind  ·  Stanford CIM206  ·  March 2026\ncontact@motionmind.com",
   Inches(0.38), Inches(6.78), Inches(5.8), Inches(0.55),
   size=11, color=RGBColor(0x60, 0x90, 0x78))

footer(s); slide_num(s, 10)


# ─────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────
out = "MotionMind_Persona_Story.pptx"
prs.save(out)
print(f"✅  Saved: {out}  ({len(prs.slides)} slides)")
