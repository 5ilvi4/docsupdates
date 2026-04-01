"""
MotionMind — Investor + Demo Product Deck
Builds a fully designed PowerPoint presentation from scratch.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
import pptx.oxml.ns as nsmap
from lxml import etree
import copy, math

# ─────────────────────────────────────────────────
# BRAND COLORS
# ─────────────────────────────────────────────────
NAVY       = RGBColor(0x0D, 0x1B, 0x2A)   # deep navy
INDIGO     = RGBColor(0x1B, 0x3A, 0x6B)   # indigo
ELECTRIC   = RGBColor(0x00, 0xB4, 0xD8)   # electric cyan
MINT       = RGBColor(0x06, 0xD6, 0xA0)   # mint green
CORAL      = RGBColor(0xFF, 0x6B, 0x6B)   # coral accent
GOLD       = RGBColor(0xFF, 0xC3, 0x00)   # gold
WHITE      = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF0, 0xF4, 0xF8)
MID_GRAY   = RGBColor(0x8D, 0x99, 0xAE)
DARK_GRAY  = RGBColor(0x2B, 0x2D, 0x42)

# Slide dimensions — widescreen 16:9
W = Inches(13.33)
H = Inches(7.5)

prs = Presentation()
prs.slide_width  = W
prs.slide_height = H

BLANK_LAYOUT = prs.slide_layouts[6]  # completely blank

# ─────────────────────────────────────────────────
# LOW-LEVEL HELPERS
# ─────────────────────────────────────────────────

def rgb_hex(r, g, b):
    return RGBColor(r, g, b)

def add_rect(slide, x, y, w, h, fill_color, alpha=None):
    shape = slide.shapes.add_shape(1, x, y, w, h)  # MSO_SHAPE_TYPE.RECTANGLE
    shape.line.fill.background()
    shape.line.width = 0
    fill = shape.fill
    fill.solid()
    fill.fore_color.rgb = fill_color
    return shape

def add_textbox(slide, text, x, y, w, h,
                font_size=16, bold=False, color=WHITE,
                align=PP_ALIGN.LEFT, italic=False,
                font_name="Calibri", word_wrap=True):
    txBox = slide.shapes.add_textbox(x, y, w, h)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font_name
    return txBox

def add_multiline_textbox(slide, lines, x, y, w, h,
                           font_size=14, bold_first=False,
                           color=WHITE, align=PP_ALIGN.LEFT,
                           font_name="Calibri", spacing_pt=6):
    txBox = slide.shapes.add_textbox(x, y, w, h)
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.alignment = align
        p.space_before = Pt(spacing_pt if i > 0 else 0)
        run = p.add_run()
        run.text = line
        run.font.size = Pt(font_size)
        run.font.bold = (bold_first and i == 0)
        run.font.color.rgb = color
        run.font.name = font_name
    return txBox

def add_pill(slide, text, x, y, w, h, bg_color, text_color=WHITE, font_size=13):
    """Rounded pill badge."""
    shape = slide.shapes.add_shape(
        5,  # ROUNDED_RECTANGLE
        x, y, w, h
    )
    shape.line.fill.background()
    shape.line.width = 0
    shape.fill.solid()
    shape.fill.fore_color.rgb = bg_color
    tf = shape.text_frame
    tf.word_wrap = False
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = True
    run.font.color.rgb = text_color
    run.font.name = "Calibri"
    return shape

def add_divider(slide, x, y, w, color=ELECTRIC, thickness=2):
    shape = slide.shapes.add_shape(1, x, y, w, Pt(thickness))
    shape.line.fill.background()
    shape.line.width = 0
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    return shape

def slide_bg(slide, color=NAVY):
    add_rect(slide, 0, 0, W, H, color)

def add_slide_number(slide, num, total=12):
    add_textbox(slide, f"{num} / {total}",
                W - Inches(1.2), H - Inches(0.4),
                Inches(1.1), Inches(0.35),
                font_size=10, color=MID_GRAY, align=PP_ALIGN.RIGHT)

def header_bar(slide, title, subtitle=None, num=None, total=12):
    """Dark top bar with title."""
    add_rect(slide, 0, 0, W, Inches(1.15), INDIGO)
    add_textbox(slide, title,
                Inches(0.45), Inches(0.18),
                Inches(9), Inches(0.65),
                font_size=26, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    if subtitle:
        add_textbox(slide, subtitle,
                    Inches(0.45), Inches(0.78),
                    Inches(9), Inches(0.35),
                    font_size=13, color=ELECTRIC, align=PP_ALIGN.LEFT)
    if num:
        add_textbox(slide, f"{num}",
                    W - Inches(1.1), Inches(0.28),
                    Inches(0.9), Inches(0.55),
                    font_size=32, bold=True, color=ELECTRIC, align=PP_ALIGN.RIGHT)
    add_divider(slide, Inches(0.45), Inches(1.12), W - Inches(0.9))

def stat_card(slide, big_text, label, x, y, w=Inches(2.8), h=Inches(1.6),
              bg=INDIGO, accent=ELECTRIC):
    add_rect(slide, x, y, w, h, bg)
    add_textbox(slide, big_text,
                x + Inches(0.15), y + Inches(0.12),
                w - Inches(0.3), Inches(0.85),
                font_size=34, bold=True, color=accent, align=PP_ALIGN.CENTER)
    add_textbox(slide, label,
                x + Inches(0.15), y + Inches(0.9),
                w - Inches(0.3), Inches(0.6),
                font_size=11, color=WHITE, align=PP_ALIGN.CENTER)

def feature_card(slide, icon, title, body, x, y,
                 w=Inches(3.9), h=Inches(2.1),
                 bg=INDIGO, accent=ELECTRIC):
    add_rect(slide, x, y, w, h, bg)
    add_textbox(slide, icon,
                x + Inches(0.18), y + Inches(0.14),
                Inches(0.55), Inches(0.55),
                font_size=22, color=accent, align=PP_ALIGN.LEFT)
    add_textbox(slide, title,
                x + Inches(0.75), y + Inches(0.17),
                w - Inches(0.9), Inches(0.45),
                font_size=15, bold=True, color=WHITE, align=PP_ALIGN.LEFT)
    add_textbox(slide, body,
                x + Inches(0.18), y + Inches(0.68),
                w - Inches(0.36), h - Inches(0.78),
                font_size=12, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

def check_list(slide, items, x, y, w, font_size=13, color=WHITE, bullet="✓", accent=MINT):
    txBox = slide.shapes.add_textbox(x, y, w, Inches(len(items) * 0.38))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(5)
        # bullet run
        r1 = p.add_run()
        r1.text = bullet + "  "
        r1.font.size = Pt(font_size)
        r1.font.bold = True
        r1.font.color.rgb = accent
        r1.font.name = "Calibri"
        # text run
        r2 = p.add_run()
        r2.text = item
        r2.font.size = Pt(font_size)
        r2.font.color.rgb = color
        r2.font.name = "Calibri"

def step_pill(slide, num, text, x, y, w=Inches(2.5), h=Inches(0.85)):
    add_rect(slide, x, y, Inches(0.55), h, ELECTRIC)
    add_textbox(slide, str(num),
                x, y, Inches(0.55), h,
                font_size=20, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_rect(slide, x + Inches(0.55), y, w - Inches(0.55), h, INDIGO)
    add_textbox(slide, text,
                x + Inches(0.62), y + Inches(0.08),
                w - Inches(0.72), h - Inches(0.12),
                font_size=12, color=WHITE, align=PP_ALIGN.LEFT)

def arrow_right(slide, x, y):
    """Small → arrow between steps."""
    add_textbox(slide, "→",
                x, y, Inches(0.4), Inches(0.5),
                font_size=20, bold=True, color=ELECTRIC, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 1 — COVER
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)

# Left gradient accent block
add_rect(s, 0, 0, Inches(0.35), H, ELECTRIC)

# Big product name
add_textbox(s, "MotionMind",
            Inches(0.7), Inches(1.1),
            Inches(8), Inches(1.5),
            font_size=72, bold=True, color=WHITE, align=PP_ALIGN.LEFT)

# Tagline
add_textbox(s, "Your child's hands are the controller.",
            Inches(0.7), Inches(2.55),
            Inches(9), Inches(0.7),
            font_size=28, bold=False, color=ELECTRIC, align=PP_ALIGN.LEFT)

add_divider(s, Inches(0.7), Inches(3.38), Inches(5.5), MINT, thickness=3)

add_textbox(s,
    "A camera-based hand-tracking and body gesture game that detects\n"
    "developmental gaps in children ages 3–11 — and tells parents\n"
    "exactly what to do about them.",
    Inches(0.7), Inches(3.6),
    Inches(8.2), Inches(1.4),
    font_size=17, color=LIGHT_GRAY, align=PP_ALIGN.LEFT)

# Badges row
for i, (label, bg) in enumerate([
    ("🎮  Gesture-First", INDIGO),
    ("📷  Camera-Only", INDIGO),
    ("🧠  Science-Backed", INDIGO),
    ("🏥  Clinician-Ready", INDIGO),
]):
    add_pill(s, label,
             Inches(0.7) + i * Inches(2.35),
             Inches(5.25),
             Inches(2.2), Inches(0.52),
             bg_color=bg, font_size=12)

# Bottom right visual placeholder — hand skeleton illustration text
add_rect(s, Inches(9.6), Inches(0.6), Inches(3.4), Inches(6.5), INDIGO)
add_textbox(s, "🤚",
            Inches(9.9), Inches(1.8),
            Inches(2.8), Inches(2.0),
            font_size=110, color=ELECTRIC, align=PP_ALIGN.CENTER)
add_textbox(s, "21-point hand skeleton\nGoogle MediaPipe Hands",
            Inches(9.9), Inches(4.2),
            Inches(2.8), Inches(0.9),
            font_size=12, color=MID_GRAY, align=PP_ALIGN.CENTER)
add_textbox(s, "Real-time · <10ms · Camera-only",
            Inches(9.9), Inches(5.2),
            Inches(2.8), Inches(0.5),
            font_size=11, color=ELECTRIC, align=PP_ALIGN.CENTER)

add_textbox(s, "Investor & Demo Deck  ·  March 2026  ·  Stanford CIM206",
            Inches(0.7), H - Inches(0.5),
            Inches(8), Inches(0.4),
            font_size=11, color=MID_GRAY, align=PP_ALIGN.LEFT)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 2 — THE PROBLEM
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "The Problem", "Screens are permanent. The problem is what the child's body is NOT getting.", num="01")

# Big quote / hook
add_rect(s, Inches(0.45), Inches(1.35), Inches(12.43), Inches(1.05), INDIGO)
add_textbox(s,
    "6 hours/day on screens · Only 18% of children meet movement guidelines · Screen → dopamine → meltdown → deeper dependency",
    Inches(0.6), Inches(1.42),
    Inches(12.2), Inches(0.85),
    font_size=14, bold=True, color=ELECTRIC, align=PP_ALIGN.CENTER)

# 5 problem cards
problems = [
    ("🎯", "Digital Addiction",      "54% of parents say their child is addicted.\nDopamine loop reinforces itself."),
    ("😴", "Sleep Disruption",       "Blue light + arousal suppress melatonin.\nChild loses avg 1hr sleep/night."),
    ("💰", "Screen as Currency",     "55% use screen as reward.\nIncreases dependency 1.4–1.7×."),
    ("🤝", "Social-Emotional Gap",   "Social skill formation requires face-to-face.\nScreens cannot provide this."),
    ("🏃", "Physical Body Gaps",     "Only 18% of kids meet movement guidelines.\nMotor development silently falls behind."),
]

card_w = Inches(2.35)
card_h = Inches(3.45)
for i, (icon, title, body) in enumerate(problems):
    cx = Inches(0.45) + i * (card_w + Inches(0.18))
    cy = Inches(2.6)
    add_rect(s, cx, cy, card_w, card_h, INDIGO)
    add_textbox(s, icon, cx + Inches(0.15), cy + Inches(0.15),
                Inches(0.6), Inches(0.6), font_size=26, color=ELECTRIC)
    add_textbox(s, title, cx + Inches(0.15), cy + Inches(0.75),
                card_w - Inches(0.3), Inches(0.5),
                font_size=14, bold=True, color=WHITE)
    add_textbox(s, body, cx + Inches(0.15), cy + Inches(1.3),
                card_w - Inches(0.3), Inches(2.0),
                font_size=11.5, color=LIGHT_GRAY)

add_textbox(s,
    "The reinforcing trap:  Screen → dopamine → meltdown → screen to manage → screen becomes currency → relationship erodes → deeper dependency",
    Inches(0.45), Inches(6.25),
    Inches(12.43), Inches(0.55),
    font_size=11, color=CORAL, italic=True, align=PP_ALIGN.CENTER)
add_slide_number(s, 2)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 3 — MARKET OPPORTUNITY
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "Market Opportunity", "A $103B market — and the white space is wide open.", num="02")

# 4 big stat cards
stats = [
    ("$56B→$103B", "Child rehab market by 2034\n7% CAGR"),
    ("$9B+",       "Early intervention (US annual)\nIDEA federal mandate"),
    ("8M+",        "US children 0–11 showing\ndevelopmental symptoms"),
    ("7–12×",      "ROI on early intervention\n(Heckman Equation)"),
]
for i, (big, label) in enumerate(stats):
    stat_card(s, big, label,
              Inches(0.45) + i * Inches(3.1),
              Inches(1.45),
              w=Inches(2.9), h=Inches(1.8))

# White space box
add_rect(s, Inches(0.45), Inches(3.55), Inches(12.43), Inches(1.3), RGBColor(0x06, 0x1A, 0x38))
add_textbox(s, "⬜  The White Space",
            Inches(0.65), Inches(3.65),
            Inches(5), Inches(0.45),
            font_size=15, bold=True, color=ELECTRIC)
add_textbox(s,
    "Between screen management tools (Bark, Apple Screen Time) and clinical treatment — nobody serves the "
    "family that sees something is wrong but hasn't entered the clinical pathway yet. That is MotionMind's addressable market.",
    Inches(0.65), Inches(4.1),
    Inches(12.0), Inches(0.65),
    font_size=12.5, color=LIGHT_GRAY)

# Comp market rows
comps = [
    ("Kids apps",              "$2.2B → $16B",   "28% CAGR"),
    ("Parenting apps",         "$1.9B → $6B",    "by 2035"),
    ("Parental control sw",    "$1.7B → $4.2B",  "by 2035"),
    ("Untreated adversity",    "$14.1T",          "lifetime economic toll"),
]
for i, (label, val, note) in enumerate(comps):
    row_y = Inches(5.1) + i * Inches(0.42)
    add_rect(s, Inches(0.45), row_y, Inches(12.43), Inches(0.38),
             INDIGO if i % 2 == 0 else RGBColor(0x12, 0x2A, 0x52))
    add_textbox(s, label, Inches(0.6),  row_y + Inches(0.04), Inches(4.5), Inches(0.34),
                font_size=12, color=WHITE)
    add_textbox(s, val,   Inches(5.5),  row_y + Inches(0.04), Inches(3.5), Inches(0.34),
                font_size=13, bold=True, color=GOLD)
    add_textbox(s, note,  Inches(9.3),  row_y + Inches(0.04), Inches(3.2), Inches(0.34),
                font_size=11, color=MID_GRAY)
add_slide_number(s, 3)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 4 — THE SOLUTION
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "The Solution — MotionMind", "Hand-tracking gesture game + gap-specific activity prescription.", num="03")

# Left: product description
add_rect(s, Inches(0.45), Inches(1.35), Inches(7.0), Inches(5.7), INDIGO)

add_textbox(s, "What it is",
            Inches(0.65), Inches(1.5),
            Inches(6.5), Inches(0.45),
            font_size=16, bold=True, color=ELECTRIC)
add_textbox(s,
    "A camera-based app that uses real-time hand-tracking and body "
    "gesture recognition (Google MediaPipe Hands, 21-point skeleton) to "
    "deliver a game children actually want to play — while simultaneously "
    "detecting and scoring developmental gaps.",
    Inches(0.65), Inches(1.95),
    Inches(6.5), Inches(1.2),
    font_size=13, color=LIGHT_GRAY)

add_textbox(s, "How it works",
            Inches(0.65), Inches(3.2),
            Inches(6.5), Inches(0.4),
            font_size=15, bold=True, color=MINT)

steps = [
    ("1", "Child plays gesture game — no controller, no avatar"),
    ("2", "Camera tracks hand & body movements in real time"),
    ("3", "App detects 7/8 developmental gaps automatically"),
    ("4", "Parent gets plain-language weekly body report card"),
    ("5", "App prescribes household activities to close each gap"),
]
for i, (n, txt) in enumerate(steps):
    sy = Inches(3.7) + i * Inches(0.44)
    add_rect(s, Inches(0.65), sy, Inches(0.38), Inches(0.36), ELECTRIC)
    add_textbox(s, n, Inches(0.65), sy, Inches(0.38), Inches(0.36),
                font_size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_textbox(s, txt, Inches(1.1), sy + Inches(0.02),
                Inches(6.1), Inches(0.36), font_size=12, color=WHITE)

# Right: the "no hardware" badge + gap table
add_rect(s, Inches(7.65), Inches(1.35), Inches(5.23), Inches(5.7), RGBColor(0x06, 0x1A, 0x38))

add_textbox(s, "📱  Works on any tablet or phone",
            Inches(7.85), Inches(1.5),
            Inches(4.8), Inches(0.45),
            font_size=14, bold=True, color=GOLD)
add_textbox(s, "No special hardware. Just a front camera.",
            Inches(7.85), Inches(1.95),
            Inches(4.8), Inches(0.35),
            font_size=12, color=MID_GRAY)

add_divider(s, Inches(7.85), Inches(2.4), Inches(4.8), ELECTRIC)

add_textbox(s, "Gaps detected by MotionMind",
            Inches(7.85), Inches(2.55),
            Inches(4.8), Inches(0.38),
            font_size=13, bold=True, color=WHITE)

gaps = [
    ("Body schema + spatial cognition",     MINT),
    ("Visual-motor integration (VMI)",      MINT),
    ("Gross motor activation",              MINT),
    ("Vestibular (full-body movement)",     MINT),
    ("Fine motor precision",                ELECTRIC),
    ("Proprioceptive load",                 ELECTRIC),
    ("Tactile discrimination",              CORAL),
]
for i, (gap, col) in enumerate(gaps):
    gy = Inches(3.05) + i * Inches(0.42)
    add_rect(s, Inches(7.85), gy + Inches(0.08), Inches(0.22), Inches(0.22), col)
    add_textbox(s, gap,
                Inches(8.15), gy,
                Inches(4.5), Inches(0.38),
                font_size=12, color=WHITE)

add_textbox(s, "● Camera detects  ● Prescribes  ● Tracks progress",
            Inches(7.85), Inches(6.1),
            Inches(4.8), Inches(0.35),
            font_size=11, color=ELECTRIC, italic=True)
add_slide_number(s, 4)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 5 — PRODUCT DEMO FLOW
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "Product Demo — User Journey", "From first launch to developmental insight in under 5 minutes.", num="04")

# 5-step demo flow with connectors
demo_steps = [
    ("🚀", "Launch",        "Parent opens app.\nChild profile created.\n3-min OT onboarding."),
    ("🎮", "Play",          "Child plays gesture game.\nHands & body tracked live.\nNo controller needed."),
    ("📷", "Detect",        "Camera scores gesture quality,\nmotion range, hand precision\n& body schema in real time."),
    ("📊", "Report",        "Weekly body report card.\nPlain language for parents.\n'Balance: Level 2 → Level 3'"),
    ("🏠", "Prescribe",     "App prescribes gap-closing\nhousehold activities.\nZero extra effort needed."),
]

step_w = Inches(2.25)
step_h = Inches(4.2)
gap_x  = Inches(0.32)

for i, (icon, title, body) in enumerate(demo_steps):
    cx = Inches(0.45) + i * (step_w + gap_x)
    cy = Inches(1.45)
    # step block
    add_rect(s, cx, cy, step_w, step_h, INDIGO)
    # top accent stripe
    add_rect(s, cx, cy, step_w, Inches(0.08), ELECTRIC)
    # step number
    add_rect(s, cx, cy + Inches(0.15), Inches(0.52), Inches(0.46), ELECTRIC)
    add_textbox(s, str(i+1),
                cx, cy + Inches(0.15), Inches(0.52), Inches(0.46),
                font_size=18, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    # icon
    add_textbox(s, icon,
                cx + Inches(0.6), cy + Inches(0.15),
                Inches(1.0), Inches(0.55),
                font_size=28, color=GOLD)
    # title
    add_textbox(s, title,
                cx + Inches(0.15), cy + Inches(0.82),
                step_w - Inches(0.3), Inches(0.48),
                font_size=16, bold=True, color=WHITE)
    # body
    add_textbox(s, body,
                cx + Inches(0.15), cy + Inches(1.38),
                step_w - Inches(0.3), Inches(2.55),
                font_size=12, color=LIGHT_GRAY)
    # arrow between steps
    if i < 4:
        arr_x = cx + step_w + Inches(0.04)
        add_textbox(s, "▶",
                    arr_x, cy + Inches(1.8),
                    Inches(0.28), Inches(0.45),
                    font_size=16, bold=True, color=ELECTRIC, align=PP_ALIGN.CENTER)

# Bottom demo CTA
add_rect(s, Inches(0.45), Inches(5.85), Inches(12.43), Inches(0.9), RGBColor(0x06, 0x1A, 0x38))
add_textbox(s,
    "Demo available:  Open app → point camera at child's hands → watch real-time skeleton overlay + gap scoring populate live.",
    Inches(0.65), Inches(5.97),
    Inches(12.0), Inches(0.65),
    font_size=13, bold=True, color=ELECTRIC, align=PP_ALIGN.CENTER)
add_slide_number(s, 5)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 6 — SCIENCE & EVIDENCE
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "Science & Evidence", "Every claim is sourced. Every mechanism is validated.", num="05")

evidence = [
    ("🧬", "Visual-Motor Integration\n(VMI)",
     "VMI deficits are among the earliest predictors of fine motor delay & academic readiness.\nBeery & Beery, 2010 — Beery VMI (6th ed.), standard OT assessment tool."),
    ("👁️", "Visual-Proprioceptive\nCoupling in Children 4–8",
     "Children ages 4–8 rely heavily on visual cues for spatial and motor tasks — different from adults.\nPLOS One, 2020 — well-established developmental neuroscience."),
    ("📐", "Embodied Learning\nMeta-Analysis",
     "Technology-based embodied learning produces significant motor & cognitive gains.\nSMD = 0.41, p<.01 across 44 studies (2025 meta-analysis)."),
    ("🤚", "Gesture-Based Interaction\nvs. Passive Touch",
     "Gesture-based game interfaces show significant gains in fine motor coordination vs. passive touchscreen.\nRamstrand et al., 2023."),
    ("🧠", "Heckman Equation —\nEarly Intervention ROI",
     "7–12× return on investment for early developmental intervention.\nHeckman, Nobel Prize in Economics — federal policy basis for IDEA funding."),
    ("📋", "COPPA 2025 + FDA\nGeneral Wellness",
     "FDA Jan 2026: camera-based wellness sensing + activity prescription = General Wellness, not SaMD.\nCOPPA 2025 amendments cover biometric data — MotionMind architecture is compliant."),
]

cols = 3
rows = 2
card_w = Inches(4.0)
card_h = Inches(2.2)
start_x = Inches(0.45)
start_y = Inches(1.45)
gap_x2  = Inches(0.2)
gap_y2  = Inches(0.2)

for idx, (icon, title, body) in enumerate(evidence):
    col = idx % cols
    row = idx // cols
    cx = start_x + col * (card_w + gap_x2)
    cy = start_y + row * (card_h + gap_y2)
    add_rect(s, cx, cy, card_w, card_h, INDIGO)
    add_rect(s, cx, cy, Inches(0.07), card_h, ELECTRIC)
    add_textbox(s, icon,
                cx + Inches(0.2), cy + Inches(0.12),
                Inches(0.6), Inches(0.6), font_size=22, color=ELECTRIC)
    add_textbox(s, title,
                cx + Inches(0.85), cy + Inches(0.12),
                card_w - Inches(1.05), Inches(0.7),
                font_size=13, bold=True, color=WHITE)
    add_textbox(s, body,
                cx + Inches(0.2), cy + Inches(0.85),
                card_w - Inches(0.4), Inches(1.25),
                font_size=11, color=LIGHT_GRAY)
add_slide_number(s, 6)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 7 — COMPETITIVE LANDSCAPE
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "Competitive Landscape", "MotionMind is the only product that detects AND prescribes.", num="06")

# Header row
headers = ["Product", "Gesture / Hand-Track", "Detects Gaps", "Prescribes Activities", "COPPA", "No Hardware"]
col_widths = [Inches(2.5), Inches(1.9), Inches(1.8), Inches(2.5), Inches(1.3), Inches(1.9)]
col_starts = []
cx = Inches(0.45)
for w in col_widths:
    col_starts.append(cx)
    cx += w

row0_y = Inches(1.45)
add_rect(s, Inches(0.45), row0_y, sum(col_widths), Inches(0.48), ELECTRIC)
for j, (h, cs, cw) in enumerate(zip(headers, col_starts, col_widths)):
    add_textbox(s, h, cs + Inches(0.08), row0_y + Inches(0.06),
                cw - Inches(0.1), Inches(0.36),
                font_size=12, bold=True, color=NAVY, align=PP_ALIGN.CENTER)

# Data rows
comps2 = [
    #  name               gesture  detect  prescribe  coppa   nohw
    ("MotionMind ★",       "✅ Full", "✅ 7/8",  "✅ Auto",    "✅", "✅"),
    ("Nex Playground",     "✅ Body", "❌",       "❌",         "⚠️", "❌"),
    ("Osmo",               "⚠️ Touch","❌",      "⚠️ Manual",  "✅", "❌"),
    ("GoNoodle",           "❌",      "❌",       "❌",         "✅", "✅"),
    ("Apple Screen Time",  "❌",      "❌",       "❌",         "✅", "✅"),
    ("Kinect / Xbox",      "✅ Body", "❌",       "❌",         "⚠️", "❌"),
    ("Pediatric OT",       "⚠️ Manual","✅",     "✅ Manual",  "✅", "N/A"),
]

for i, row_data in enumerate(comps2):
    ry = Inches(1.93) + i * Inches(0.57)
    bg = RGBColor(0x1B, 0x3A, 0x6B) if i == 0 else (INDIGO if i % 2 == 0 else RGBColor(0x12, 0x2A, 0x52))
    add_rect(s, Inches(0.45), ry, sum(col_widths), Inches(0.54), bg)
    if i == 0:
        add_rect(s, Inches(0.45), ry, Inches(0.06), Inches(0.54), MINT)
    for j, (cell, cs, cw) in enumerate(zip(row_data, col_starts, col_widths)):
        fc = GOLD if (i == 0) else (WHITE if j == 0 else LIGHT_GRAY)
        add_textbox(s, cell, cs + Inches(0.08), ry + Inches(0.08),
                    cw - Inches(0.1), Inches(0.38),
                    font_size=12 if j > 0 else 13,
                    bold=(i == 0),
                    color=fc,
                    align=PP_ALIGN.CENTER if j > 0 else PP_ALIGN.LEFT)

add_textbox(s,
    "★ MotionMind is the only solution that combines real-time gesture tracking, automatic developmental gap detection, "
    "and zero-effort activity prescription — on hardware families already own.",
    Inches(0.45), Inches(6.6),
    Inches(12.43), Inches(0.6),
    font_size=12, color=MINT, italic=True, align=PP_ALIGN.CENTER)
add_slide_number(s, 7)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 8 — PRODUCT FEATURES (PARENT / CHILD / CLINICIAN)
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "Product Features", "Built for three users — parent, child, and clinician.", num="07")

cols_data = [
    {
        "title": "👨‍👩‍👧  For Parents",
        "color": ELECTRIC,
        "items": [
            "Weekly plain-language body report card",
            "Session motion heat map",
            "Push notification of specific gains",
            "Meltdown frequency tracker",
            "Share-with-pediatrician PDF report",
            "OT referral directory (zip code)",
            "HSA/FSA eligible · Free core tier",
        ]
    },
    {
        "title": "🧒  For Children",
        "color": MINT,
        "items": [
            "Story world with ongoing narrative",
            "Collectible objects unlock game levels",
            "Child-chosen daily quest",
            "Sibling co-play mode",
            "2-player gesture co-op",
            "Skill level: 'Balance LEVEL 3'",
            "Adaptive difficulty as body improves",
        ]
    },
    {
        "title": "🩺  For Clinicians",
        "color": GOLD,
        "items": [
            "PDF formatted for 15-min well-child visit",
            "SMART on FHIR patient portal (v1.5)",
            "HL7 FHIR Observation (v2 / Epic/Cerner)",
            "Anonymized outcome data dashboard",
            "AAP Bright Futures alignment",
            "IDEA codes (ages 0–3) — federal pathway",
            "De Novo path → Medicaid/CHIP (APDTA)",
        ]
    },
]

col_w = Inches(3.95)
for i, col in enumerate(cols_data):
    cx = Inches(0.45) + i * (col_w + Inches(0.25))
    cy = Inches(1.45)
    add_rect(s, cx, cy, col_w, Inches(5.7), INDIGO)
    add_rect(s, cx, cy, col_w, Inches(0.55), RGBColor(0x06, 0x1A, 0x38))
    add_textbox(s, col["title"],
                cx + Inches(0.15), cy + Inches(0.07),
                col_w - Inches(0.3), Inches(0.42),
                font_size=15, bold=True, color=col["color"])
    check_list(s, col["items"],
               cx + Inches(0.15), cy + Inches(0.72),
               col_w - Inches(0.3),
               font_size=12, color=WHITE, bullet="→", accent=col["color"])
add_slide_number(s, 8)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 9 — REGULATORY & COMPLIANCE
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "Regulatory & Compliance", "Launch-ready today. Clear path to reimbursement.", num="08")

# Left — Green (no FDA needed)
add_rect(s, Inches(0.45), Inches(1.45), Inches(5.8), Inches(5.6), RGBColor(0x03, 0x20, 0x12))
add_rect(s, Inches(0.45), Inches(1.45), Inches(5.8), Inches(0.5), MINT)
add_textbox(s, "✅  FDA NOT NEEDED — Launch Now",
            Inches(0.65), Inches(1.52),
            Inches(5.5), Inches(0.38),
            font_size=14, bold=True, color=NAVY)

green_items = [
    "Camera tracks movement → wellness summaries",
    "Activity prescription from camera data",
    "Gap report: 'balance tracking is developing'",
    "Prompt: 'consider seeing an OT'",
    "All covered under FDA General Wellness\nGuidance, January 6 2026",
]
check_list(s, green_items,
           Inches(0.65), Inches(2.1),
           Inches(5.4), font_size=12.5, color=WHITE, bullet="✓", accent=MINT)

# Right — Red (FDA needed if)
add_rect(s, Inches(6.55), Inches(1.45), Inches(6.33), Inches(5.6), RGBColor(0x20, 0x06, 0x06))
add_rect(s, Inches(6.55), Inches(1.45), Inches(6.33), Inches(0.5), CORAL)
add_textbox(s, "⚠️  FDA NEEDED — Do NOT Cross",
            Inches(6.75), Inches(1.52),
            Inches(6.0), Inches(0.38),
            font_size=14, bold=True, color=WHITE)

red_items = [
    "Claim to diagnose a condition (SaMD — needs clearance)",
    "Claim to treat a disorder (De Novo or 510(k))",
    "Replace clinician judgment without review",
    "Claim insurance reimbursement before clearance",
]
check_list(s, red_items,
           Inches(6.75), Inches(2.1),
           Inches(6.0), font_size=12.5, color=WHITE, bullet="✗", accent=CORAL)

# COPPA box
add_rect(s, Inches(6.55), Inches(4.3), Inches(6.33), Inches(2.75), RGBColor(0x1A, 0x1A, 0x0A))
add_textbox(s, "🔒  COPPA 2025 — Compliance Deadline April 22 2026",
            Inches(6.75), Inches(4.42),
            Inches(6.0), Inches(0.45),
            font_size=13, bold=True, color=GOLD)
coppa_items = [
    "Parent account only — child never registers",
    "Verifiable parental consent before camera activates",
    "No third-party analytics or ad SDKs",
    "Camera/hand tracking = biometric data under 2025 amendments",
    "$53,088 per violation — architecture built before testing",
]
check_list(s, coppa_items,
           Inches(6.75), Inches(4.95),
           Inches(6.0), font_size=11.5, color=WHITE, bullet="•", accent=GOLD)
add_slide_number(s, 9)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 10 — GO-TO-MARKET
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "Go-to-Market Strategy", "Three parallel tracks — consumer, clinical, institutional.", num="09")

tracks = [
    {
        "num": "1",
        "title": "B2C — Direct to Families",
        "color": ELECTRIC,
        "items": [
            "Free core tier (app store — iOS + Android)",
            "Premium subscription: activity prescription library",
            "HSA/FSA eligible from launch",
            "Target: parents of children ages 3–7 in meltdown loop",
            "CAC channel: parenting blogs, pediatrician waiting rooms",
        ]
    },
    {
        "num": "2",
        "title": "B2B — Schools & Libraries",
        "color": MINT,
        "items": [
            "Site licensing for school districts",
            "Library lending program (B2B route to low-income families)",
            "IDEA early intervention codes (ages 0–3) — federally funded",
            "OT community session as evidence generation site",
            "Target: Title I schools, early intervention programs",
        ]
    },
    {
        "num": "3",
        "title": "Clinical — Pediatrician + OT",
        "color": GOLD,
        "items": [
            "PDF report fits 15-min well-child visit (now)",
            "SMART on FHIR integration (v1.5)",
            "AAP Section on Developmental Pediatrics pathway",
            "De Novo clearance → Medicaid/CHIP (APDTA)",
            "Target: 130,000+ US pediatricians + OT practices",
        ]
    },
]

track_w = Inches(3.95)
for i, track in enumerate(tracks):
    cx = Inches(0.45) + i * (track_w + Inches(0.27))
    cy = Inches(1.45)
    add_rect(s, cx, cy, track_w, Inches(5.6), INDIGO)
    add_rect(s, cx, cy, Inches(0.55), Inches(5.6), track["color"])
    add_textbox(s, track["num"],
                cx, cy + Inches(0.2),
                Inches(0.55), Inches(0.55),
                font_size=22, bold=True, color=NAVY, align=PP_ALIGN.CENTER)
    add_textbox(s, track["title"],
                cx + Inches(0.68), cy + Inches(0.15),
                track_w - Inches(0.85), Inches(0.55),
                font_size=14, bold=True, color=track["color"])
    check_list(s, track["items"],
               cx + Inches(0.68), cy + Inches(0.85),
               track_w - Inches(0.85),
               font_size=12, color=WHITE, bullet="→", accent=track["color"])
add_slide_number(s, 10)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 11 — TRACTION & ROADMAP
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
header_bar(s, "Traction & Roadmap", "From need validation to market — a clear critical path.", num="10")

# Market proof boxes
proof = [
    ("Nex Playground", "#2 US hardware Nov 2025", "Market proof: parents pay for active screens"),
    ("Osmo",           "$100M+ acquisition",       "Physical-digital hybrid — validated commercial category"),
    ("Heckman Eq.",    "7–12× ROI",                "Early intervention — payer economic case"),
]
for i, (name, val, note) in enumerate(proof):
    bx = Inches(0.45) + i * Inches(4.15)
    add_rect(s, bx, Inches(1.45), Inches(3.9), Inches(1.35), INDIGO)
    add_textbox(s, name, bx + Inches(0.15), Inches(1.55),
                Inches(3.6), Inches(0.38), font_size=13, bold=True, color=ELECTRIC)
    add_textbox(s, val,  bx + Inches(0.15), Inches(1.93),
                Inches(3.6), Inches(0.38), font_size=18, bold=True, color=GOLD)
    add_textbox(s, note, bx + Inches(0.15), Inches(2.32),
                Inches(3.6), Inches(0.35), font_size=11, color=MID_GRAY)

# Roadmap
add_textbox(s, "Development Roadmap",
            Inches(0.45), Inches(3.05),
            Inches(8), Inches(0.45),
            font_size=16, bold=True, color=WHITE)

roadmap = [
    ("Now",          ELECTRIC, ["Field validation (parent interviews)", "COPPA architecture", "Prototype gesture mechanic", "OT session shadow"]),
    ("Q3 2026",      MINT,     ["MVP with hand-tracking + gap detection", "Free tier app store launch", "OT community session pilot (evidence gen)", "PDF report for pediatricians"]),
    ("Q4 2026",      GOLD,     ["Premium subscription launch", "HSA/FSA filing", "SMART on FHIR (v1.5)", "School/library B2B pilots"]),
    ("2027–2028",    CORAL,    ["AAP pilot data publication", "De Novo FDA filing", "Epic/Cerner FHIR integration", "Medicaid/CHIP coverage pathway"]),
]

for i, (period, color, items) in enumerate(roadmap):
    rx = Inches(0.45) + i * Inches(3.15)
    ry = Inches(3.6)
    add_rect(s, rx, ry, Inches(3.0), Inches(0.42), color)
    add_textbox(s, period, rx + Inches(0.1), ry + Inches(0.05),
                Inches(2.8), Inches(0.35), font_size=13, bold=True, color=NAVY)
    add_rect(s, rx, ry + Inches(0.42), Inches(3.0), Inches(2.9), INDIGO)
    for j, item in enumerate(items):
        add_textbox(s, "• " + item,
                    rx + Inches(0.12), ry + Inches(0.55) + j * Inches(0.62),
                    Inches(2.76), Inches(0.58),
                    font_size=11, color=WHITE)
add_slide_number(s, 11)


# ═══════════════════════════════════════════════════════════════════
# SLIDE 12 — THE ASK / CLOSING
# ═══════════════════════════════════════════════════════════════════
s = prs.slides.add_slide(BLANK_LAYOUT)
slide_bg(s, NAVY)
add_rect(s, 0, 0, Inches(0.35), H, MINT)

add_textbox(s, "The Ask",
            Inches(0.7), Inches(0.6),
            Inches(10), Inches(1.0),
            font_size=52, bold=True, color=WHITE)

add_divider(s, Inches(0.7), Inches(1.65), Inches(5.5), MINT, thickness=3)

# Core insight
add_rect(s, Inches(0.7), Inches(1.9), Inches(12.28), Inches(1.3), INDIGO)
add_textbox(s,
    "MotionMind is the only solution that detects 7/8 developmental gaps AND tells parents exactly what "
    "to do — at zero parent effort, without removing screens, using household objects. "
    "Nothing on the market combines real-time hand-tracking, gesture-based gameplay, "
    "and gap-specific activity prescription for children ages 0–11.",
    Inches(0.9), Inches(2.0),
    Inches(11.9), Inches(1.1),
    font_size=13.5, color=LIGHT_GRAY, italic=False)

# 3 ask cards
asks = [
    ("🤝", "Advisors & Pilots",
     "Pediatric OT advisors to validate gap assessment methodology.\n"
     "1–2 pilot clinics for well-child visit PDF integration."),
    ("💰", "Seed Funding",
     "Pre-seed round to fund:\n"
     "MVP build · COPPA architecture · OT evidence generation · HSA/FSA filing.\n"
     "Target: $750K–$1.2M."),
    ("🏥", "Clinical Partnerships",
     "Children's hospital research partner for AAP pilot data.\n"
     "OT community session network (70+ sites via Pathways.org)."),
]

for i, (icon, title, body) in enumerate(asks):
    ax = Inches(0.7) + i * Inches(4.1)
    ay = Inches(3.45)
    add_rect(s, ax, ay, Inches(3.85), Inches(2.6), INDIGO)
    add_rect(s, ax, ay, Inches(3.85), Inches(0.08), ELECTRIC)
    add_textbox(s, icon, ax + Inches(0.18), ay + Inches(0.18),
                Inches(0.55), Inches(0.55), font_size=26, color=ELECTRIC)
    add_textbox(s, title, ax + Inches(0.8), ay + Inches(0.2),
                Inches(2.9), Inches(0.5), font_size=15, bold=True, color=WHITE)
    add_textbox(s, body, ax + Inches(0.18), ay + Inches(0.82),
                Inches(3.5), Inches(1.65), font_size=12, color=LIGHT_GRAY)

# Bottom contact + branding
add_rect(s, Inches(0.7), Inches(6.35), Inches(12.28), Inches(0.75), RGBColor(0x06, 0x1A, 0x38))
add_textbox(s,
    "MotionMind  ·  Stanford CIM206 — Biodesign for Digital Health  ·  March 2026  ·  Contact: [your email]",
    Inches(0.9), Inches(6.48),
    Inches(12.0), Inches(0.45),
    font_size=12, color=MID_GRAY, align=PP_ALIGN.CENTER)

add_slide_number(s, 12)


# ─────────────────────────────────────────────────
# SAVE
# ─────────────────────────────────────────────────
out = "MotionMind_Investor_Demo_Deck.pptx"
prs.save(out)
print(f"✅  Saved: {out}  ({len(prs.slides)} slides)")
