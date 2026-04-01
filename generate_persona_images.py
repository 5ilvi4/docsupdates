"""
Generate persona illustration images for MotionMind story deck.
All images drawn programmatically with Pillow — no external assets needed.
"""

from PIL import Image, ImageDraw, ImageFont
import math, os

W, H = 1200, 700

def save(img, name):
    img.save(name)
    print(f"  ✓  {name}")

def draw_gradient(draw, w, h, top_col, bot_col):
    for y in range(h):
        t = y / h
        r = int(top_col[0] + (bot_col[0] - top_col[0]) * t)
        g = int(top_col[1] + (bot_col[1] - top_col[1]) * t)
        b = int(top_col[2] + (bot_col[2] - top_col[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def rounded_rect(draw, x0, y0, x1, y1, r, fill, outline=None, width=0):
    draw.rounded_rectangle([x0, y0, x1, y1], radius=r, fill=fill,
                            outline=outline, width=width)

def circle(draw, cx, cy, r, fill):
    draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)

def try_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Arial.ttf",
        "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/SFNSDisplay.ttf",
        "/System/Library/Fonts/SFNS.ttf",
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                return ImageFont.truetype(c, size)
            except:
                pass
    return ImageFont.load_default()

# ──────────────────────────────────────────────
# PALETTE
# ──────────────────────────────────────────────
GREEN      = (0, 115, 92)
TEAL       = (0, 168, 138)
LIME       = (108, 194, 74)
CHARCOAL   = (26, 26, 46)
DARK       = (44, 44, 62)
MID        = (74, 74, 106)
SILVER     = (200, 200, 210)
OFFWHITE   = (245, 245, 247)
WHITE      = (255, 255, 255)
ORANGE     = (232, 106, 26)
CREAM      = (255, 248, 235)
SKIN_LIGHT = (255, 213, 170)
SKIN_MID   = (240, 180, 130)
SKIN_DEEP  = (180, 120, 70)
HAIR_DARK  = (60, 30, 10)
HAIR_LIGHT = (180, 120, 60)
RED_SOFT   = (220, 80, 60)
BLUE_SOFT  = (80, 130, 200)
YELLOW_S   = (255, 210, 60)
GRAY_LIGHT = (220, 220, 230)
PINK_SOFT  = (255, 180, 190)
PURPLE_S   = (140, 100, 200)

# ══════════════════════════════════════════════
# IMAGE 1 — LENA PORTRAIT
# Scene: little girl (6) in living room, tired-looking
# Mom on couch watching tablet, dark circles
# ══════════════════════════════════════════════
def draw_lena_portrait():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    # Background — warm living room
    draw_gradient(d, W, H, (255, 245, 225), (235, 220, 195))

    # Floor
    d.rectangle([0, 500, W, H], fill=(200, 175, 140))

    # Window
    d.rectangle([860, 60, 1100, 380], fill=(200, 230, 255))
    d.rectangle([860, 60, 1100, 380], outline=(180, 150, 110), width=8)
    d.line([(980, 60), (980, 380)], fill=(180, 150, 110), width=6)
    d.line([(860, 220), (1100, 220)], fill=(180, 150, 110), width=6)
    # window light ray
    for i in range(6):
        alpha = 30 - i*4
        d.polygon([(980, 220), (980+i*20, 500), (980+(i+1)*20, 500)],
                  fill=(255, 240, 180))

    # Couch
    rounded_rect(d, 100, 400, 750, 560, 18, (180, 120, 90))
    rounded_rect(d, 100, 390, 750, 430, 14, (160, 100, 70))
    rounded_rect(d, 100, 390, 160, 560, 14, (160, 100, 70))
    rounded_rect(d, 690, 390, 750, 560, 14, (160, 100, 70))

    # Rug
    d.ellipse([80, 510, 800, 620], fill=(160, 100, 120))
    d.ellipse([110, 525, 770, 608], fill=(180, 120, 140))

    # ── MOM (right of couch, sitting) ──
    mx = 580
    # body
    rounded_rect(d, mx-40, 330, mx+40, 450, 10, (100, 130, 180))
    # neck
    d.rectangle([mx-12, 310, mx+12, 340], fill=SKIN_MID)
    # head
    d.ellipse([mx-38, 260, mx+38, 340], fill=SKIN_MID)
    # hair — mom bun
    d.ellipse([mx-40, 245, mx+40, 310], fill=HAIR_DARK)
    d.ellipse([mx-10, 235, mx+20, 265], fill=HAIR_DARK)
    # eyes — tired, droopy
    d.arc([mx-22, 285, mx-8, 300], 0, 180, fill=(50, 30, 10), width=2)
    d.arc([mx+8, 285, mx+22, 300], 0, 180, fill=(50, 30, 10), width=2)
    # dark circles
    d.ellipse([mx-24, 298, mx-10, 307], fill=(160, 130, 140))
    d.ellipse([mx+10, 298, mx+24, 307], fill=(160, 130, 140))
    # mouth — slight frown
    d.arc([mx-10, 310, mx+10, 325], 200, 340, fill=(180, 100, 80), width=2)

    # tablet in mom's hands
    rounded_rect(d, mx-50, 370, mx+50, 455, 6, (40, 40, 60))
    rounded_rect(d, mx-44, 376, mx+44, 449, 4, (100, 160, 220))
    # screen glow on mom's face
    d.ellipse([mx-55, 260, mx+55, 360], fill=(220, 235, 255, 30))

    # arms holding tablet
    d.line([(mx-40, 390), (mx-50, 420)], fill=SKIN_MID, width=10)
    d.line([(mx+40, 390), (mx+50, 420)], fill=SKIN_MID, width=10)

    # ── LENA (little girl, left, sitting on floor) ──
    lx = 280
    # legs
    rounded_rect(d, lx-50, 470, lx+50, 560, 8, (255, 160, 80))  # pants
    d.ellipse([lx-55, 460, lx-30, 490], fill=SKIN_LIGHT)  # left foot
    d.ellipse([lx+30, 460, lx+55, 490], fill=SKIN_LIGHT)  # right foot
    # body
    rounded_rect(d, lx-42, 370, lx+42, 480, 10, (220, 100, 120))  # dress
    # arms
    d.line([(lx-42, 400), (lx-80, 450)], fill=SKIN_LIGHT, width=12)
    d.line([(lx+42, 400), (lx+70, 440)], fill=SKIN_LIGHT, width=12)
    # hands with toy
    d.ellipse([lx-90, 445, lx-65, 470], fill=SKIN_LIGHT)
    d.ellipse([lx+60, 432, lx+85, 457], fill=SKIN_LIGHT)
    # small toy in hand
    rounded_rect(d, lx+62, 425, lx+90, 450, 4, YELLOW_S)
    # neck
    d.rectangle([lx-12, 348, lx+12, 378], fill=SKIN_LIGHT)
    # head
    d.ellipse([lx-42, 295, lx+42, 378], fill=SKIN_LIGHT)
    # hair — pigtails
    d.ellipse([lx-44, 278, lx+44, 340], fill=HAIR_LIGHT)
    # pigtail left
    d.ellipse([lx-55, 300, lx-30, 330], fill=HAIR_LIGHT)
    d.line([(lx-50, 328), (lx-62, 370)], fill=HAIR_LIGHT, width=8)
    # pigtail right
    d.ellipse([lx+30, 300, lx+55, 330], fill=HAIR_LIGHT)
    d.line([(lx+50, 328), (lx+62, 370)], fill=HAIR_LIGHT, width=8)
    # hair ties
    circle(d, lx-56, 370, 6, RED_SOFT)
    circle(d, lx+62, 370, 6, RED_SOFT)
    # eyes — Lena curious
    d.ellipse([lx-20, 320, lx-5, 338], fill=WHITE)
    d.ellipse([lx+5, 320, lx+20, 338], fill=WHITE)
    d.ellipse([lx-17, 323, lx-8, 334], fill=(60, 40, 20))
    d.ellipse([lx+8, 323, lx+17, 334], fill=(60, 40, 20))
    # highlights
    circle(d, lx-12, 325, 3, WHITE)
    circle(d, lx+13, 325, 3, WHITE)
    # cheeks
    d.ellipse([lx-32, 340, lx-15, 356], fill=(255, 180, 160, 120))
    d.ellipse([lx+15, 340, lx+32, 356], fill=(255, 180, 160, 120))
    # mouth — slight sad
    d.arc([lx-10, 350, lx+10, 364], 200, 340, fill=(200, 100, 90), width=2)

    # Small tablet on floor — showing cartoons (Lena ignoring toy)
    rounded_rect(d, lx-20, 470, lx+20, 510, 4, (40, 40, 60))
    rounded_rect(d, lx-16, 474, lx+16, 506, 3, (80, 150, 210))

    # caption area
    rounded_rect(d, 0, 590, W, H, 0, (26, 26, 46))
    f_big = try_font(36, bold=True)
    f_sm  = try_font(22)
    d.text((60, 602), "Meet Lena, 6.", font=f_big, fill=WHITE)
    d.text((60, 646), "An average child her age gets ~2.5 hrs/day on screens (Common Sense Media, 2020). Her body is not keeping up.",
           font=f_sm, fill=SILVER)

    save(img, "persona_01_lena_intro.png")

# ══════════════════════════════════════════════
# IMAGE 2 — THE CONCERN
# Scene: Mom at kitchen table, phone out, googling
# Sticky notes around. Worried expression.
# ══════════════════════════════════════════════
def draw_concern():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    draw_gradient(d, W, H, (240, 235, 220), (215, 205, 188))

    # Kitchen table
    d.rectangle([120, 380, 980, 580], fill=(160, 120, 80))
    d.rectangle([120, 360, 980, 395], fill=(180, 140, 95))
    # table legs
    d.rectangle([140, 580, 175, 680], fill=(140, 100, 65))
    d.rectangle([940, 580, 975, 680], fill=(140, 100, 65))

    # coffee mug
    rounded_rect(d, 820, 310, 880, 385, 8, (200, 80, 60))
    rounded_rect(d, 828, 318, 872, 375, 6, (240, 200, 170))
    d.arc([880, 330, 910, 365], -30, 150, fill=(200, 80, 60), width=5)
    # steam
    for i in range(3):
        sx = 840 + i*14
        for j in range(4):
            d.arc([sx-4, 275-j*14, sx+4, 295-j*14], 180, 360, fill=(200, 200, 200), width=2)

    # sticky notes
    stickies = [
        (150, 250, "\"can't hold pencil\nfor long\"", YELLOW_S),
        (320, 220, "\"meltdown when\nwe take tablet\"", PINK_SOFT),
        (500, 240, "\"OT waitlist:\n6 months\"", (180, 220, 180)),
        (680, 215, "\"sensory issues?\nis that a thing?\"", (180, 210, 250)),
    ]
    for sx, sy, txt, col in stickies:
        # slight rotation per note
        note_img = Image.new("RGBA", (160, 120), (0, 0, 0, 0))
        nd = ImageDraw.Draw(note_img)
        rounded_rect(nd, 0, 0, 158, 118, 4, col)
        nf = try_font(19)
        nd.text((12, 16), txt, font=nf, fill=(50, 40, 30))
        # pin dot
        circle(nd, 80, 8, 6, (200, 60, 60))
        img.paste(note_img, (sx, sy), note_img)

    # Phone on table
    rounded_rect(d, 430, 340, 570, 540, 12, (30, 30, 50))
    rounded_rect(d, 440, 350, 560, 530, 8, (245, 245, 255))

    # Search on phone screen
    rounded_rect(d, 448, 358, 552, 380, 6, (230, 230, 240))
    fs = try_font(14)
    d.text((452, 361), "child development delay", font=fs, fill=(60, 60, 80))
    # search results lines
    for i in range(4):
        rounded_rect(d, 448, 390+i*32, 552, 416+i*32, 4, (240, 240, 250))
        d.rectangle([448, 390+i*32, 480, 416+i*32], fill=(200, 220, 240))

    # MOM at table
    mx = 700
    # chair
    rounded_rect(d, mx-60, 420, mx+60, 560, 8, (120, 90, 60))
    d.rectangle([mx-65, 330, mx-55, 425], fill=(120, 90, 60))
    d.rectangle([mx+55, 330, mx+65, 425], fill=(120, 90, 60))
    rounded_rect(d, mx-65, 295, mx+65, 340, 8, (120, 90, 60))
    # body
    rounded_rect(d, mx-45, 340, mx+45, 445, 10, (80, 100, 150))
    # arm on table
    d.line([(mx-45, 390), (mx-120, 400)], fill=SKIN_MID, width=14)
    d.line([(mx+45, 390), (mx+100, 390)], fill=SKIN_MID, width=14)
    # hand resting on chin
    d.ellipse([mx-135, 388, mx-108, 415], fill=SKIN_MID)
    # neck + head
    d.rectangle([mx-14, 318, mx+14, 348], fill=SKIN_MID)
    d.ellipse([mx-42, 268, mx+42, 350], fill=SKIN_MID)
    # hair
    d.ellipse([mx-44, 255, mx+44, 318], fill=HAIR_DARK)
    # furrowed brow
    d.arc([mx-20, 288, mx-4, 302], 220, 320, fill=(60, 40, 20), width=2)
    d.arc([mx+4, 288, mx+20, 302], 220, 320, fill=(60, 40, 20), width=2)
    d.line([(mx-18, 292), (mx-4, 288)], fill=(60, 40, 20), width=2)
    d.line([(mx+4, 288), (mx+18, 292)], fill=(60, 40, 20), width=2)
    # eyes — worried
    d.arc([mx-20, 305, mx-5, 318], 0, 180, fill=(50, 30, 10), width=2)
    d.arc([mx+5, 305, mx+20, 318], 0, 180, fill=(50, 30, 10), width=2)
    # mouth — pursed
    d.line([(mx-8, 333), (mx+8, 333)], fill=(180, 100, 90), width=2)

    # thought bubble
    for i, (bx, by, br) in enumerate([
        (820, 220, 8), (840, 200, 12), (860, 182, 10)]):
        circle(d, bx, by, br, (240, 240, 255))
    rounded_rect(d, 830, 80, 1090, 185, 16, (240, 240, 255))
    ft = try_font(22)
    d.text((848, 96),  "\"She should be\nholding her pencil\nbetter by now...\"",
           font=ft, fill=(60, 60, 100))

    # caption
    rounded_rect(d, 0, 590, W, H, 0, CHARCOAL)
    fb = try_font(34, bold=True)
    fm = try_font(22)
    d.text((60, 600), "Maya, 34. Lena's mom.", font=fb, fill=WHITE)
    d.text((60, 644), "71% of parents worry their child spends too much time on screens. OT waitlist: 6 months. (Pew Research, 2020)",
           font=fm, fill=SILVER)

    save(img, "persona_02_maya_concern.png")

# ══════════════════════════════════════════════
# IMAGE 3 — DISCOVERY / UNBOXING
# Scene: Lena + Maya, MotionMind band on wrist,
# tablet on table, green glow, excited
# ══════════════════════════════════════════════
def draw_discovery():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    draw_gradient(d, W, H, (230, 248, 240), (200, 230, 215))

    # Table
    d.rectangle([80, 430, 1050, 580], fill=(180, 145, 100))
    d.rectangle([80, 410, 1050, 445], fill=(200, 162, 112))

    # Box (unboxed MotionMind)
    # box base
    rounded_rect(d, 700, 300, 960, 445, 8, (240, 240, 245))
    rounded_rect(d, 700, 300, 960, 445, 8, None, outline=GREEN, width=3)
    # box lid open (angled)
    d.polygon([(700, 300), (960, 300), (980, 260), (720, 260)],
              fill=(220, 240, 232))
    d.polygon([(700, 300), (960, 300), (980, 260), (720, 260)],
              outline=GREEN, width=2)
    # brand on box
    fb = try_font(28, bold=True)
    d.text((728, 332), "MotionMind", font=fb, fill=GREEN)
    fs2 = try_font(16)
    d.text((728, 368), "Wearable Development System", font=fs2, fill=MID)
    # green M logo circle
    circle(d, 820, 415, 18, GREEN)
    fb2 = try_font(22, bold=True)
    d.text((813, 404), "M", font=fb2, fill=WHITE)

    # BAND (on table, just taken out)
    # band body
    rounded_rect(d, 750, 455, 910, 510, 20, (30, 30, 50))
    # sensor bump
    rounded_rect(d, 800, 448, 860, 518, 10, (40, 180, 140))
    # green LED glow
    for glow_r in [22, 18, 14, 10]:
        alpha = max(0, 80 - glow_r * 3)
        circle(d, 830, 483, glow_r, (0, 200, 150))
    # small display on band
    rounded_rect(d, 810, 458, 850, 480, 4, (20, 20, 35))
    # blinking dots
    for di in range(3):
        circle(d, 822 + di*10, 469, 3, TEAL)

    # TABLET (left, screen showing game)
    rounded_rect(d, 120, 300, 550, 590, 12, (30, 30, 50))
    rounded_rect(d, 132, 312, 538, 578, 8, (15, 20, 40))
    # game screen — hand outline + landmarks
    d.rectangle([132, 312, 538, 578], fill=(10, 18, 35))
    # hand skeleton drawing
    # palm
    hand_pts_x = [335, 310, 295, 305, 325, 355]
    hand_pts_y = [480, 460, 430, 400, 385, 390]
    # simplified hand
    # wrist
    circle(d, 335, 510, 18, (0, 200, 150))
    # palm lines to fingers
    for fx, fy in [(295, 380), (310, 360), (335, 350), (360, 360), (385, 375)]:
        d.line([(335, 490), (fx, fy)], fill=(0, 200, 150), width=2)
        # knuckle
        circle(d, fx, fy, 6, (0, 200, 150))
        # fingertip
        circle(d, fx, fy-30, 5, LIME)
    # 21 landmark dots scattered on hand area
    lm_positions = [
        (335, 510), (325, 480), (315, 450), (305, 420), (295, 395),
        (310, 475), (298, 440), (290, 408), (283, 380),
        (328, 473), (318, 435), (313, 400), (308, 370),
        (348, 473), (342, 435), (338, 400), (334, 368),
        (368, 476), (362, 438), (358, 404), (354, 372),
    ]
    for lx2, ly2 in lm_positions:
        circle(d, lx2, ly2, 4, TEAL)

    # score bars on screen top
    for bi, (bw2, bcol) in enumerate([
        (90, GREEN), (70, TEAL), (50, LIME), (80, GREEN), (40, TEAL)]):
        bx3 = 140 + bi*78
        d.rectangle([bx3, 318, bx3+bw2, 330], fill=bcol)
        d.rectangle([bx3, 318, bx3+78, 330], outline=(40, 60, 80), width=1)

    # "GREAT!" label on screen
    fg = try_font(32, bold=True)
    d.text((380, 380), "GREAT!", font=fg, fill=YELLOW_S)
    # sparkles
    for sx3, sy3 in [(390, 360), (460, 370), (420, 345), (475, 355), (400, 375)]:
        d.line([(sx3-6, sy3), (sx3+6, sy3)], fill=YELLOW_S, width=2)
        d.line([(sx3, sy3-6), (sx3, sy3+6)], fill=YELLOW_S, width=2)

    # ── LENA (wearing band, playing) ──
    lx3 = 620
    # body — excited posture
    rounded_rect(d, lx3-42, 355, lx3+42, 465, 10, (220, 100, 120))
    # right arm raised
    d.line([(lx3+42, 380), (lx3+120, 300)], fill=SKIN_LIGHT, width=14)
    d.ellipse([lx3+112, 290, lx3+140, 320], fill=SKIN_LIGHT)
    # BAND on wrist (right arm raised)
    rounded_rect(d, lx3+98, 305, lx3+138, 326, 8, (30, 30, 50))
    rounded_rect(d, lx3+108, 302, lx3+128, 329, 6, (40, 180, 140))
    # left arm pointing at screen
    d.line([(lx3-42, 390), (lx3-110, 360)], fill=SKIN_LIGHT, width=14)
    d.ellipse([lx3-128, 348, lx3-98, 378], fill=SKIN_LIGHT)
    # legs
    rounded_rect(d, lx3-42, 455, lx3+0, 580, 8, (255, 160, 80))
    rounded_rect(d, lx3+0,  455, lx3+42, 580, 8, (255, 160, 80))
    # neck + head
    d.rectangle([lx3-12, 330, lx3+12, 360], fill=SKIN_LIGHT)
    d.ellipse([lx3-42, 278, lx3+42, 362], fill=SKIN_LIGHT)
    # hair
    d.ellipse([lx3-44, 262, lx3+44, 325], fill=HAIR_LIGHT)
    d.ellipse([lx3-55, 285, lx3-28, 315], fill=HAIR_LIGHT)
    d.ellipse([lx3+28, 285, lx3+55, 315], fill=HAIR_LIGHT)
    # excited eyes
    d.arc([lx3-20, 305, lx3-4, 322], 200, 340, fill=(50, 30, 10), width=3)
    d.arc([lx3+4, 305, lx3+20, 322], 200, 340, fill=(50, 30, 10), width=3)
    # smile
    d.arc([lx3-14, 330, lx3+14, 348], 20, 160, fill=(200, 80, 70), width=3)
    # cheeks pink
    d.ellipse([lx3-32, 330, lx3-14, 346], fill=(255, 160, 150))
    d.ellipse([lx3+14, 330, lx3+32, 346], fill=(255, 160, 150))

    # ── MAYA (watching, smiling) ──
    mx2 = 860
    # body
    rounded_rect(d, mx2-40, 360, mx2+40, 455, 10, (100, 130, 180))
    d.line([(mx2-40, 395), (mx2-85, 435)], fill=SKIN_MID, width=12)
    d.line([(mx2+40, 395), (mx2+80, 430)], fill=SKIN_MID, width=12)
    d.rectangle([mx2-12, 335, mx2+12, 366], fill=SKIN_MID)
    d.ellipse([mx2-40, 282, mx2+40, 366], fill=SKIN_MID)
    d.ellipse([mx2-42, 268, mx2+42, 328], fill=HAIR_DARK)
    # smile — finally!
    d.arc([mx2-14, 320, mx2+14, 340], 20, 160, fill=(180, 90, 70), width=3)
    d.arc([mx2-18, 295, mx2-4, 312], 0, 180, fill=(50, 30, 10), width=2)
    d.arc([mx2+4, 295, mx2+18, 312], 0, 180, fill=(50, 30, 10), width=2)
    # phone in hand showing app
    rounded_rect(d, mx2+62, 415, mx2+110, 490, 8, (30, 30, 50))
    rounded_rect(d, mx2+68, 421, mx2+104, 484, 5, (80, 200, 160))
    # app UI on phone
    fs3 = try_font(12)
    d.text((mx2+70, 430), "Lena's Report", font=fs3, fill=WHITE)
    for ri in range(3):
        d.rectangle([mx2+70, 448+ri*10, mx2+70+30+ri*8, 456+ri*10],
                    fill=(TEAL if ri == 0 else (LIME if ri == 1 else GREEN)))

    # green aura/glow effect around the band
    for gr in range(5, 0, -1):
        d.ellipse([lx3+100, 288, lx3+146, 334],
                  outline=(0, 200, 150, max(0, 30 * gr // 5)), width=2)

    # caption
    rounded_rect(d, 0, 590, W, H, 0, CHARCOAL)
    fb3 = try_font(34, bold=True)
    fm3 = try_font(22)
    d.text((60, 600), "First session. 8 minutes.", font=fb3, fill=GREEN)
    d.text((60, 644),
           "Camera tracks hand skeleton. Band reads grip. App scores developmental gaps — automatically.",
           font=fm3, fill=SILVER)

    save(img, "persona_03_discovery.png")

# ══════════════════════════════════════════════
# IMAGE 4 — INSIGHT / REPORT
# Close-up: parent dashboard on phone/tablet
# showing developmental gap scorecard
# ══════════════════════════════════════════════
def draw_insight():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    draw_gradient(d, W, H, (245, 250, 248), (225, 238, 230))

    # Main device — tablet showing report
    rounded_rect(d, 180, 50, 820, 620, 18, (25, 25, 42))
    rounded_rect(d, 195, 65, 805, 605, 10, WHITE)

    # App header
    d.rectangle([195, 65, 805, 125], fill=GREEN)
    fh = try_font(28, bold=True)
    d.text((220, 80), "MotionMind", font=fh, fill=WHITE)
    fs4 = try_font(18)
    d.text((220, 112), "Lena's Developmental Profile  ·  Session 3", font=fs4, fill=(180, 230, 210))
    # avatar circle
    circle(d, 772, 95, 24, TEAL)
    fa = try_font(22, bold=True)
    d.text((764, 83), "L", font=fa, fill=WHITE)

    # Section title
    fst = try_font(20, bold=True)
    d.text((210, 140), "BODY DEVELOPMENT GAPS", font=fst, fill=CHARCOAL)
    d.line([(210, 165), (790, 165)], fill=SILVER, width=1)

    # Gap bars
    gaps4 = [
        ("Fine motor precision",     78, GREEN),
        ("Handgrip strength",        52, ORANGE),
        ("Muscle quality",           45, ORANGE),
        ("Gross motor activation",   88, GREEN),
        ("Body schema / spatial",    72, TEAL),
        ("Visual-motor integration", 85, GREEN),
        ("Vestibular",               68, TEAL),
    ]
    bar_x_start = 210
    bar_max_w = 430
    for i, (gap_name, pct, col) in enumerate(gaps4):
        gy = 180 + i * 56
        fl = try_font(17)
        d.text((bar_x_start, gy), gap_name, font=fl, fill=(60, 60, 80))
        # bar background
        rounded_rect(d, bar_x_start, gy+24, bar_x_start+bar_max_w, gy+46, 6,
                     (230, 235, 232))
        # bar fill
        bar_fill_w = int(bar_max_w * pct / 100)
        rounded_rect(d, bar_x_start, gy+24, bar_x_start+bar_fill_w, gy+46, 6, col)
        # pct label
        fp2 = try_font(15, bold=True)
        d.text((bar_x_start + bar_fill_w + 10, gy+26), f"{pct}%", font=fp2, fill=col)
        # status tag
        status = "On Track" if pct >= 70 else "Needs Focus"
        tag_col = (200, 240, 215) if pct >= 70 else (255, 225, 195)
        tag_text_col = (0, 120, 60) if pct >= 70 else (180, 80, 20)
        rounded_rect(d, 680, gy+26, 790, gy+44, 6, tag_col)
        ftt = try_font(13)
        d.text((688, gy+28), status, font=ftt, fill=tag_text_col)

    # Prescription box
    rounded_rect(d, 210, 575, 795, 598, 8, (232, 248, 240))
    d.rectangle([210, 575, 215, 598], fill=GREEN)
    fp3 = try_font(16, bold=True)
    d.text((222, 578),
           "💡  This week: Playdough squeeze games (10 min) · Finger obstacle course · Lego sorting",
           font=fp3, fill=GREEN)

    # right panel — phone showing same app
    rounded_rect(d, 870, 120, 1120, 590, 14, (25, 25, 42))
    rounded_rect(d, 882, 132, 1108, 578, 8, WHITE)
    d.rectangle([882, 132, 1108, 178], fill=GREEN)
    fph = try_font(18, bold=True)
    d.text((900, 142), "MotionMind", font=fph, fill=WHITE)
    fps2 = try_font(13)
    d.text((900, 163), "Weekly summary", font=fps2, fill=(180, 220, 200))

    # pie-ish progress ring
    cx5, cy5, cr5 = 995, 290, 68
    # background ring
    d.arc([cx5-cr5, cy5-cr5, cx5+cr5, cy5+cr5], 0, 360, fill=GRAY_LIGHT, width=14)
    # progress arc ~72%
    d.arc([cx5-cr5, cy5-cr5, cx5+cr5, cy5+cr5], -90, -90+int(360*0.72),
          fill=GREEN, width=14)
    fp4 = try_font(26, bold=True)
    d.text((cx5-20, cy5-16), "72%", font=fp4, fill=CHARCOAL)
    fp5 = try_font(12)
    d.text((cx5-28, cy5+14), "overall", font=fp5, fill=MID)

    # small stat rows
    for si, (label, val2, col2) in enumerate([
        ("Sessions", "3", TEAL),
        ("Streak", "3 days 🔥", ORANGE),
        ("Grip ↑", "+8%", GREEN),
        ("Next Rx", "Today", GREEN),
    ]):
        sy4 = 375 + si * 48
        rounded_rect(d, 890, sy4, 1100, sy4+38, 6, (248, 250, 248))
        fl2 = try_font(14)
        fb4 = try_font(14, bold=True)
        d.text((906, sy4+10), label, font=fl2, fill=MID)
        d.text((1010, sy4+10), val2, font=fb4, fill=col2)

    # caption
    rounded_rect(d, 0, 628, W, H, 0, CHARCOAL)
    fbc = try_font(32, bold=True)
    fmc = try_font(21)
    d.text((60, 636), "Maya opens the report.", font=fbc, fill=WHITE)
    d.text((60, 673),
           "Gap scores. Plain language. A specific activity prescription. No clinical visit needed.",
           font=fmc, fill=SILVER)

    save(img, "persona_04_insight.png")

# ══════════════════════════════════════════════
# IMAGE 5 — TRANSFORMATION
# Scene: 4 weeks later. Lena at table drawing,
# holding pencil correctly. Mom watching, smiling.
# Band on wrist. Green progress glow.
# ══════════════════════════════════════════════
def draw_transformation():
    img = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(img)

    draw_gradient(d, W, H, (240, 252, 244), (215, 238, 222))

    # Bright window
    d.rectangle([780, 30, 1080, 430], fill=(210, 235, 255))
    d.rectangle([780, 30, 1080, 430], outline=(200, 175, 130), width=8)
    d.line([(930, 30), (930, 430)], fill=(200, 175, 130), width=5)
    d.line([(780, 230), (1080, 230)], fill=(200, 175, 130), width=5)
    # sunshine rays from window
    for angle in range(0, 360, 30):
        rx = 930 + 280 * math.cos(math.radians(angle))
        ry = 230 + 200 * math.sin(math.radians(angle))
        d.line([(930, 230), (int(rx), int(ry))],
               fill=(255, 245, 180, 30), width=1)

    # Table
    d.rectangle([80, 400, 900, 540], fill=(170, 135, 90))
    d.rectangle([80, 382, 900, 408], fill=(190, 152, 100))

    # Drawing on table — child's artwork
    d.rectangle([200, 300, 480, 420], fill=WHITE)
    d.rectangle([200, 300, 480, 420], outline=GRAY_LIGHT, width=2)
    # crayon drawing of house + sun
    d.polygon([(280, 345), (340, 300), (400, 345)], fill=RED_SOFT)
    d.rectangle([260, 345, 420, 415], fill=(200, 160, 100))
    d.rectangle([320, 375, 360, 415], fill=(120, 80, 50))
    circle(d, 430, 315, 22, YELLOW_S)
    for sa in range(0, 360, 45):
        lx4 = 430 + 28 * math.cos(math.radians(sa))
        ly4 = 315 + 28 * math.sin(math.radians(sa))
        d.line([(430, 315), (int(lx4), int(ly4))], fill=YELLOW_S, width=2)
    d.arc([330, 380, 390, 410], 0, 180, fill=BLUE_SOFT, width=2)

    # Crayons scattered on table
    for ci2, (col3, cx6) in enumerate([
        (RED_SOFT, 490), (BLUE_SOFT, 520), (YELLOW_S, 550), (GREEN, 580)]):
        d.rectangle([cx6, 395, cx6+12, 438], fill=col3)
        d.polygon([(cx6, 438), (cx6+6, 455), (cx6+12, 438)], fill=col3)

    # ── LENA (drawing, sitting straight, holding pencil) ──
    lx5 = 350
    # chair
    rounded_rect(d, lx5-55, 430, lx5+55, 560, 8, (120, 90, 60))
    # legs
    rounded_rect(d, lx5-40, 510, lx5+0, 600, 8, (200, 140, 60))
    rounded_rect(d, lx5+0, 510, lx5+40, 600, 8, (200, 140, 60))
    d.ellipse([lx5-48, 592, lx5-28, 612], fill=(160, 100, 50))
    d.ellipse([lx5+28, 592, lx5+48, 612], fill=(160, 100, 50))
    # body — upright, proud
    rounded_rect(d, lx5-42, 340, lx5+42, 455, 10, (100, 170, 220))
    # right arm down to table — drawing
    d.line([(lx5+42, 375), (lx5+80, 420)], fill=SKIN_LIGHT, width=13)
    d.ellipse([lx5+72, 412, lx5+98, 438], fill=SKIN_LIGHT)
    # PENCIL in right hand — correct grip
    d.line([(lx5+85, 435), (lx5+100, 410)], fill=YELLOW_S, width=5)
    d.polygon([(lx5+99, 408), (lx5+103, 403), (lx5+107, 408)],
              fill=(230, 150, 50))
    # left arm on table
    d.line([(lx5-42, 390), (lx5-90, 420)], fill=SKIN_LIGHT, width=13)
    d.ellipse([lx5-106, 412, lx5-80, 438], fill=SKIN_LIGHT)
    # neck + head
    d.rectangle([lx5-12, 315, lx5+12, 348], fill=SKIN_LIGHT)
    d.ellipse([lx5-42, 262, lx5+42, 348], fill=SKIN_LIGHT)
    # hair
    d.ellipse([lx5-44, 246, lx5+44, 310], fill=HAIR_LIGHT)
    d.ellipse([lx5-52, 270, lx5-25, 300], fill=HAIR_LIGHT)
    d.ellipse([lx5+25, 270, lx5+52, 300], fill=HAIR_LIGHT)
    circle(d, lx5-52, 310, 6, RED_SOFT)
    circle(d, lx5+52, 310, 6, RED_SOFT)
    # BAND on left wrist
    rounded_rect(d, lx5-106, 420, lx5-72, 438, 8, (30, 30, 50))
    rounded_rect(d, lx5-98, 417, lx5-80, 441, 6, (40, 180, 140))
    # LED active
    circle(d, lx5-89, 429, 4, LIME)
    # eyes — focused, happy
    d.arc([lx5-20, 295, lx5-4, 312], 200, 340, fill=(50, 30, 10), width=3)
    d.arc([lx5+4, 295, lx5+20, 312], 200, 340, fill=(50, 30, 10), width=3)
    # big smile
    d.arc([lx5-15, 322, lx5+15, 342], 20, 160, fill=(200, 80, 70), width=3)
    d.ellipse([lx5-28, 318, lx5-10, 334], fill=(255, 160, 150))
    d.ellipse([lx5+10, 318, lx5+28, 334], fill=(255, 160, 150))

    # ── MAYA (standing, arms crossed, big smile) ──
    mx3 = 680
    # body
    rounded_rect(d, mx3-44, 330, mx3+44, 455, 10, (80, 150, 120))
    # arms crossed
    d.line([(mx3-44, 375), (mx3+44, 400)], fill=SKIN_MID, width=12)
    d.line([(mx3+44, 375), (mx3-44, 400)], fill=SKIN_MID, width=12)
    # legs
    rounded_rect(d, mx3-36, 448, mx3+0, 580, 8, (60, 100, 80))
    rounded_rect(d, mx3+0, 448, mx3+36, 580, 8, (60, 100, 80))
    d.ellipse([mx3-42, 572, mx3-18, 592], fill=(40, 70, 55))
    d.ellipse([mx3+18, 572, mx3+42, 592], fill=(40, 70, 55))
    # neck + head
    d.rectangle([mx3-12, 306, mx3+12, 336], fill=SKIN_MID)
    d.ellipse([mx3-42, 255, mx3+42, 338], fill=SKIN_MID)
    # hair
    d.ellipse([mx3-44, 242, mx3+44, 302], fill=HAIR_DARK)
    # wide smile
    d.arc([mx3-16, 308, mx3+16, 328], 20, 160, fill=(180, 90, 70), width=3)
    d.arc([mx3-18, 278, mx3-4, 295], 0, 180, fill=(50, 30, 10), width=2)
    d.arc([mx3+4, 278, mx3+18, 295], 0, 180, fill=(50, 30, 10), width=2)

    # Progress stat bubble
    rounded_rect(d, 860, 120, 1140, 260, 16, WHITE)
    rounded_rect(d, 860, 120, 1140, 260, 16, None, outline=GREEN, width=2)
    rect_h = try_font(15, bold=True)
    d.text((885, 136), "Lena's Progress — Week 4", font=rect_h, fill=GREEN)
    d.line([(885, 158), (1120, 158)], fill=SILVER, width=1)
    stats5 = [
        ("Grip strength", "+24%", GREEN),
        ("Fine motor",    "+18%", TEAL),
        ("Drawing time",  "12 min", GREEN),
        ("Meltdowns",     "-60%", LIME),
    ]
    for si2, (stat_l, stat_v, stat_c) in enumerate(stats5):
        sx5 = 885 + (si2 % 2) * 128
        sy5 = 168 + (si2 // 2) * 44
        fl3 = try_font(13)
        fb5 = try_font(18, bold=True)
        d.text((sx5, sy5), stat_l, font=fl3, fill=MID)
        d.text((sx5, sy5+18), stat_v, font=fb5, fill=stat_c)

    # Connector arrow from bubble to Maya
    d.line([(860, 190), (mx3+42, 300)], fill=GREEN, width=2)
    circle(d, 860, 190, 5, GREEN)

    # caption
    rounded_rect(d, 0, 615, W, H, 0, CHARCOAL)
    fbc2 = try_font(32, bold=True)
    fmc2 = try_font(21)
    d.text((60, 622), "Weeks later. Lena draws for longer. Her grip is stronger.", font=fbc2, fill=GREEN)
    d.text((60, 661),
           "28% of parents give in to screens to avoid meltdowns weekly (Lurie Children's Hospital, 2025). Maya doesn't anymore.",
           font=fmc2, fill=SILVER)

    save(img, "persona_05_transformation.png")

# ══════════════════════════════════════════════
# RUN ALL
# ══════════════════════════════════════════════
print("Generating persona images...")
draw_lena_portrait()
draw_concern()
draw_discovery()
draw_insight()
draw_transformation()
print("\n✅  All 5 persona images generated.")
