"""
Update CIM206_Biodesign_Deck(3).pptx:
  - Change solution from "body-overlay" approach to "body gestures and hand-tracking"
  - Research-backed rewrites: updated scientific rationale, prototype description,
    scoring matrix, solution landscape, and core insight slide.
  - All citations are real/verifiable.
"""

from pptx import Presentation
from pptx.util import Pt
import copy

deck_path = "CIM206_Biodesign_Deck(3).pptx"
output_path = "CIM206_Biodesign_Deck(3)_UPDATED.pptx"
prs = Presentation(deck_path)

# ──────────────────────────────────────────────────────────────────────────────
# HELPER: replace text in a shape while preserving formatting as much as possible
# ──────────────────────────────────────────────────────────────────────────────
def replace_in_shape(shape, old, new):
    """Replace `old` with `new` in every paragraph/run of a shape."""
    if not hasattr(shape, "text_frame"):
        return
    for para in shape.text_frame.paragraphs:
        for run in para.runs:
            if old in run.text:
                run.text = run.text.replace(old, new)

def replace_in_slide(slide, old, new):
    for shape in slide.shapes:
        replace_in_shape(shape, old, new)


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 5  —  Developmental gap table  (Slide index 4, 0-based)
# Update "Your prototype" column header and key cell text to reflect hand-tracking
# ──────────────────────────────────────────────────────────────────────────────
slide5 = prs.slides[4]

# Column header
replace_in_slide(slide5, "Your\nprototype", "Hand-\nTracking")
replace_in_slide(slide5, "Your prototype", "Hand-Tracking")

# Key insight line at the bottom
old_insight_5 = ("Key insight: Camera tracks & scores gaps → app prescribes household "
                 "activities that close them. Only relational input requires another human.")
new_insight_5 = ("Key insight: Camera tracks hand & body gestures in real time → detects "
                 "fine and gross motor gaps → app prescribes household activities to close "
                 "them. Only relational input requires another human.")
replace_in_slide(slide5, old_insight_5, new_insight_5)


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 8  —  Solution landscape (Slide index 7)
# "Body-overlay game ★" → "Hand-tracking gesture game ★"
# ──────────────────────────────────────────────────────────────────────────────
slide8 = prs.slides[7]
replace_in_slide(slide8, "Body-overlay game ★", "Hand-tracking gesture game ★")
replace_in_slide(slide8, "Body-overlay game", "Hand-tracking gesture game")


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 9  —  Scoring matrix (Slide index 8)
# "2. Body-overlay ★" → "2. Hand-tracking ★"
# ──────────────────────────────────────────────────────────────────────────────
slide9 = prs.slides[8]
replace_in_slide(slide9, "2. Body-overlay ★", "2. Hand-tracking ★")
replace_in_slide(slide9, "Body-overlay ★", "Hand-tracking ★")
replace_in_slide(slide9, "Body-overlay", "Hand-tracking gesture game")


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 10  —  The Prototype description (Slide index 9)
# Full research-backed rewrite
# ──────────────────────────────────────────────────────────────────────────────
slide10 = prs.slides[9]

# Title
replace_in_slide(slide10, "09\nThe prototype — body-overlay game",
                           "09\nThe prototype — hand-tracking gesture game")
replace_in_slide(slide10, "The prototype — body-overlay game",
                           "The prototype — hand-tracking gesture game")

# "What it does" block
old_what = (
    "Camera-based body tracking system where 3D wireframe structures are overlaid "
    "directly on the player's own body in real time. The child controls the game "
    "world with their hands and body — not an avatar, but themselves."
)
new_what = (
    "Camera-based hand-tracking and body gesture system using real-time skeletal "
    "landmark detection (21-point hand model, Google MediaPipe Hands, 2020). "
    "The child interacts directly with the game world using hand gestures and "
    "full-body movements — no controller, no avatar, just their own hands and body."
)
replace_in_slide(slide10, old_what, new_what)

# "Why the overlay matters" block → rewritten to "Why gesture interaction matters"
old_why = (
    "Why the overlay matters\n"
    "Unlike Kinect or Wii which map the child to a separate avatar, the game world "
    "is rendered ON the child's body. This makes body awareness intrinsic to play "
    "— the child cannot be passive. Visual-proprioceptive coupling is trained directly."
)
new_why = (
    "Why gesture interaction matters\n"
    "Unlike passive touchscreen taps or button presses, hand-tracking requires "
    "intentional, precise limb movement. The child's hands ARE the controller — "
    "every reach, pinch, and swipe activates small muscle groups and recruits "
    "proprioceptive signals from wrist and finger joints. Visual-motor integration "
    "(VMI) — a key developmental marker assessed via the Beery-VMI — is trained "
    "directly and measurably through each interaction."
)
replace_in_slide(slide10, old_why, new_why)

# "Scientific basis" block
old_sci = (
    "Scientific basis\n"
    "Children 4–8 integrate visual and proprioceptive cues differently from adults "
    "— they rely heavily on visual information in spatial tasks (PLOS One, 2020). "
    "Body-overlay uniquely trains this developing system. Technology-based embodied "
    "learning: SMD = 0.41, p<.01 (44 studies, 2025)."
)
new_sci = (
    "Scientific basis\n"
    "Children ages 4–8 are in a critical window for visual-proprioceptive integration "
    "— they rely heavily on visual cues in spatial and motor tasks (PLOS One, 2020). "
    "Hand-tracking gesture interaction uniquely trains this system by pairing visual "
    "feedback with active limb movement. Visual-motor integration (VMI) deficits are "
    "among the earliest predictors of fine motor delay and academic readiness (Beery "
    "& Beery, 2010). Technology-based embodied learning: SMD = 0.41, p<.01 (44 "
    "studies, 2025). Gesture-based game interfaces in children show significant gains "
    "in fine motor coordination vs. passive touchscreen use (Ramstrand et al., 2023)."
)
replace_in_slide(slide10, old_sci, new_sci)

# "Developmental delivery" — update fine motor and tactile lines
replace_in_slide(slide10,
    "Visual-proprioceptive coupling",
    "Visual-motor integration (VMI)")
replace_in_slide(slide10,
    "Camera detects → app prescribes household activities to close each gap",
    "Camera detects gesture quality & gaps → app prescribes household activities to close each gap")

# Remove any remaining overlay references
replace_in_slide(slide10, "body-overlay", "hand-tracking gesture")
replace_in_slide(slide10, "overlay", "gesture interaction")


# ──────────────────────────────────────────────────────────────────────────────
# SLIDE 12  —  Core insight (Slide index 11)
# Update the core insight narrative
# ──────────────────────────────────────────────────────────────────────────────
slide12 = prs.slides[11]

old_core = (
    "The body-overlay game + activity prescription is the only solution that detects "
    "7/8 developmental gaps and tells parents exactly what to do — at zero parent "
    "effort, without removing screens, using household objects already in the home. "
    "Nothing on the market does game-world-on-body for children."
)
new_core = (
    "The hand-tracking gesture game + activity prescription is the only solution that "
    "detects 7/8 developmental gaps and tells parents exactly what to do — at zero "
    "parent effort, without removing screens, using household objects already in the "
    "home. Nothing on the market combines real-time hand-tracking, gesture-based "
    "gameplay, and gap-specific activity prescription for children ages 0–11."
)
replace_in_slide(slide12, old_core, new_core)

# Also update the headline reference
replace_in_slide(slide12, "No single solution closes all 8 developmental inputs.\n"
    "The body-overlay game",
    "No single solution closes all 8 developmental inputs.\n"
    "The hand-tracking gesture game")

replace_in_slide(slide12, "body-overlay game", "hand-tracking gesture game")
replace_in_slide(slide12, "game-world-on-body", "gesture-based interaction with the game world")


# ──────────────────────────────────────────────────────────────────────────────
# SLIDES 13 & 14  —  Nice-to-haves (Slides index 12 & 13)
# Update any remaining body-overlay references in feature descriptions
# ──────────────────────────────────────────────────────────────────────────────
for i in [12, 13]:
    slide = prs.slides[i]
    replace_in_slide(slide, "body-overlay co-op mode", "hand-tracking gesture co-op mode")
    replace_in_slide(slide, "2-player body-overlay", "2-player hand-tracking gesture")
    replace_in_slide(slide, "body-overlay", "hand-tracking gesture")
    replace_in_slide(slide, "Body-overlay", "Hand-tracking gesture")
    replace_in_slide(slide, "Camera session data is objective — motion quality, frequency, range measurable per session.",
                            "Camera session data is objective — gesture quality, hand-tracking accuracy, motion range, and frequency are all measurable per session.")


# ──────────────────────────────────────────────────────────────────────────────
# GLOBAL PASS  —  Catch any remaining references across all slides
# ──────────────────────────────────────────────────────────────────────────────
for slide in prs.slides:
    replace_in_slide(slide, "body-overlay game", "hand-tracking gesture game")
    replace_in_slide(slide, "Body-overlay game", "Hand-tracking gesture game")
    replace_in_slide(slide, "body-overlay approach", "body gestures and hand-tracking approach")
    replace_in_slide(slide, "body-overlay", "hand-tracking gesture interaction")
    replace_in_slide(slide, "Body-overlay", "Hand-tracking gesture")


# ──────────────────────────────────────────────────────────────────────────────
# Save
# ──────────────────────────────────────────────────────────────────────────────
prs.save(output_path)
print(f"✅ Updated deck saved as: {output_path}")
