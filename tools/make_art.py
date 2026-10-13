"""Draws all Boulder Dash sprites as 32x32 pixel art. Output: <out>/<sprite>/<n>.png"""
import math, os, random, sys
from PIL import Image, ImageDraw

OUT = sys.argv[1]
S = 32
T = (0, 0, 0, 0)

def new():
    return Image.new("RGBA", (S, S), T)

def save(name, frames):
    d = os.path.join(OUT, name)
    os.makedirs(d, exist_ok=True)
    for i, f in enumerate(frames):
        f.save(os.path.join(d, f"{i}.png"))

def px(img, x, y, c):
    if 0 <= x < S and 0 <= y < S:
        img.putpixel((x, y), c)

# ---------- Wall (bricks) ----------
def wall():
    img = Image.new("RGBA", (S, S), (70, 40, 30, 255))  # mortar
    d = ImageDraw.Draw(img)
    rnd = random.Random(1)
    for row in range(4):
        y0 = row * 8
        off = 0 if row % 2 == 0 else -8
        for col in range(-1, 3):
            x0 = off + col * 16
            base = rnd.choice([(178, 74, 52), (165, 66, 46), (190, 84, 58)])
            d.rectangle([x0 + 1, y0 + 1, x0 + 14, y0 + 6], fill=base + (255,))
            d.line([x0 + 1, y0 + 1, x0 + 14, y0 + 1], fill=(222, 120, 90, 255))
            d.line([x0 + 1, y0 + 6, x0 + 14, y0 + 6], fill=(120, 46, 34, 255))
    return img

# ---------- Dirt ----------
def dirt():
    img = Image.new("RGBA", (S, S), (122, 78, 42, 255))
    rnd = random.Random(7)
    cols = [(98, 60, 30), (140, 92, 52), (110, 70, 36), (156, 106, 62)]
    for _ in range(90):
        x, y = rnd.randrange(S), rnd.randrange(S)
        c = rnd.choice(cols) + (255,)
        px(img, x, y, c)
        if rnd.random() < 0.4:
            px(img, x + 1, y, c)
    for _ in range(6):  # pebbles
        x, y = rnd.randrange(2, S - 3), rnd.randrange(2, S - 3)
        px(img, x, y, (170, 150, 120, 255)); px(img, x + 1, y, (150, 130, 100, 255))
        px(img, x, y + 1, (100, 85, 65, 255)); px(img, x + 1, y + 1, (90, 70, 50, 255))
    return img

# ---------- Shaded round shape helper ----------
def shaded_blob(img, cx, cy, r, light, mid, dark, outline, squash=1.0):
    for y in range(S):
        for x in range(S):
            dx, dy = (x + 0.5 - cx), (y + 0.5 - cy) / squash
            dist = math.hypot(dx, dy)
            if dist <= r:
                # light from top-left
                l = (-dx - dy) / (r * 1.4)
                if dist > r - 1.2:
                    c = outline
                elif l > 0.35:
                    c = light
                elif l > -0.25:
                    c = mid
                else:
                    c = dark
                img.putpixel((x, y), c + (255,))

# ---------- Boulder ----------
def boulder():
    img = new()
    shaded_blob(img, 16, 17, 14.5, (176, 170, 160), (130, 124, 116), (88, 82, 76), (40, 36, 34), squash=0.95)
    rnd = random.Random(3)
    for _ in range(10):  # cracks / spots
        x, y = rnd.randrange(8, 24), rnd.randrange(9, 26)
        if img.getpixel((x, y))[3]:
            px(img, x, y, (80, 74, 70, 255))
    for (x, y) in [(10, 9), (11, 9), (9, 10), (10, 10)]:  # highlight
        px(img, x, y, (225, 220, 210, 255))
    return img

# ---------- Diamond (8 frames: sparkle rotates) ----------
def diamond_base():
    img = new()
    d = ImageDraw.Draw(img)
    top, mid, bot = 5, 12, 28
    # facets
    d.polygon([(4, mid), (10, top), (22, top), (28, mid)], fill=(120, 230, 255, 255))
    d.polygon([(4, mid), (16, bot), (16, mid)], fill=(40, 150, 230, 255))
    d.polygon([(16, mid), (16, bot), (28, mid)], fill=(20, 100, 190, 255))
    d.polygon([(10, top), (16, mid), (22, top)], fill=(200, 250, 255, 255))
    d.line([(4, mid), (28, mid)], fill=(230, 255, 255, 255))
    d.line([(4, mid), (10, top), (22, top), (28, mid), (16, bot), (4, mid)], fill=(10, 60, 130, 255))
    return img

def diamond():
    frames = []
    for i in range(8):
        img = diamond_base()
        # moving sparkle
        sx, sy = [(9, 9), (12, 7), (16, 6), (20, 7), (23, 9), (20, 15), (16, 20), (12, 15)][i]
        for dx, dy in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
            px(img, sx + dx, sy + dy, (255, 255, 255, 255))
        if i % 2 == 0:
            for dx, dy in [(2, 0), (-2, 0), (0, 2), (0, -2)]:
                px(img, sx + dx, sy + dy, (255, 255, 255, 200))
        frames.append(img)
    return frames

# ---------- Player (Rockford-like miner) ----------
SKIN = (240, 190, 140, 255)
HELMET = (240, 200, 40, 255)
HELMET_D = (180, 140, 20, 255)
SHIRT = (60, 120, 220, 255)
SHIRT_D = (40, 80, 160, 255)
PANTS = (90, 60, 40, 255)
BOOT = (40, 30, 25, 255)
EYE = (20, 20, 20, 255)
LAMP = (255, 255, 200, 255)

def player_frame(facing, step, blink=False, tap=False):
    """facing: 0 front, -1 left, 1 right; step 0..3 for walk cycle"""
    img = new()
    d = ImageDraw.Draw(img)
    bob = 1 if step in (1, 3) else 0
    y0 = 2 + bob
    # helmet
    d.rectangle([10, y0, 21, y0 + 4], fill=HELMET)
    d.rectangle([8, y0 + 4, 23, y0 + 5], fill=HELMET_D)
    lamp_x = 15 if facing == 0 else (11 if facing < 0 else 19)
    d.rectangle([lamp_x, y0 + 1, lamp_x + 1, y0 + 2], fill=LAMP)
    # head
    d.rectangle([10, y0 + 6, 21, y0 + 12], fill=SKIN)
    if facing == 0:
        if not blink:
            d.rectangle([12, y0 + 8, 13, y0 + 9], fill=EYE)
            d.rectangle([18, y0 + 8, 19, y0 + 9], fill=EYE)
        else:
            d.line([12, y0 + 9, 13, y0 + 9], fill=EYE)
            d.line([18, y0 + 9, 19, y0 + 9], fill=EYE)
        d.line([14, y0 + 11, 17, y0 + 11], fill=(170, 80, 60, 255))
    else:
        ex = 11 if facing < 0 else 19
        d.rectangle([ex, y0 + 8, ex + 1, y0 + 9], fill=EYE)
        mx = 10 if facing < 0 else 19
        d.line([mx, y0 + 11, mx + 2, y0 + 11], fill=(170, 80, 60, 255))
    # body
    d.rectangle([9, y0 + 13, 22, y0 + 20], fill=SHIRT)
    d.line([9, y0 + 20, 22, y0 + 20], fill=SHIRT_D)
    # arms
    swing = [0, 2, 0, -2][step] if facing != 0 else 0
    d.rectangle([6, y0 + 13 + max(0, swing), 8, y0 + 18 + max(0, swing)], fill=SHIRT_D)
    d.rectangle([23, y0 + 13 + max(0, -swing), 25, y0 + 18 + max(0, -swing)], fill=SHIRT_D)
    d.rectangle([6, y0 + 19 + max(0, swing), 8, y0 + 20 + max(0, swing)], fill=SKIN)
    d.rectangle([23, y0 + 19 + max(0, -swing), 25, y0 + 20 + max(0, -swing)], fill=SKIN)
    # legs
    ly = y0 + 21
    if facing == 0:
        left_up = 2 if tap else 0
        d.rectangle([10, ly, 14, 27 - left_up], fill=PANTS)
        d.rectangle([17, ly, 21, 27], fill=PANTS)
        d.rectangle([9, 28 - left_up, 14, 29 - left_up], fill=BOOT)
        d.rectangle([17, 28, 22, 29], fill=BOOT)
    else:
        spread = [0, 3, 0, 3][step]
        flip = step >= 2
        a = 12 - (spread if not flip else 0)
        b = 17 + (spread if flip else 0)
        a2 = 12 + (spread if flip else 0)
        b2 = 17 - (spread if not flip else 0)
        # back leg
        d.rectangle([min(a, a2), ly, min(a, a2) + 3, 27], fill=PANTS)
        d.rectangle([max(b, b2) - 1, ly, max(b, b2) + 2, 27], fill=PANTS)
        toe = -2 if facing < 0 else 2
        d.rectangle([min(a, a2) + min(0, toe), 28, min(a, a2) + 3 + max(0, toe), 29], fill=BOOT)
        d.rectangle([max(b, b2) - 1 + min(0, toe), 28, max(b, b2) + 2 + max(0, toe), 29], fill=BOOT)
    return img

def player_idle():
    return [player_frame(0, 0), player_frame(0, 0, blink=True),
            player_frame(0, 0), player_frame(0, 0, tap=True)]

def player_walk(facing):
    return [player_frame(facing, s) for s in range(4)]

# ---------- Firefly (spinning square with glow) ----------
def firefly():
    frames = []
    for i in range(4):
        img = new()
        ang = i * math.pi / 8
        # glow
        for y in range(S):
            for x in range(S):
                dist = math.hypot(x + 0.5 - 16, y + 0.5 - 16)
                if dist < 15:
                    a = int(90 * (1 - dist / 15))
                    img.putpixel((x, y), (255, 140, 30, a))
        def square(r, col):
            pts = [(16 + r * math.cos(ang + k * math.pi / 2), 16 + r * math.sin(ang + k * math.pi / 2)) for k in range(4)]
            ImageDraw.Draw(img).polygon(pts, fill=col)
        square(12, (255, 120, 20, 255))
        square(8, (255, 220, 60, 255))
        square(4, (255, 255, 220, 255))
        frames.append(img)
    return frames

# ---------- Exit ----------
def exit_door(open_frame=None):
    img = Image.new("RGBA", (S, S), (80, 84, 96, 255))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, 31, 31], outline=(40, 42, 50, 255))
    d.rectangle([1, 1, 30, 1], fill=(140, 146, 160, 255))
    d.rectangle([1, 1, 1, 30], fill=(140, 146, 160, 255))
    if open_frame is None:
        # closed steel door with rivets
        d.rectangle([5, 5, 26, 31], fill=(110, 116, 130, 255), outline=(50, 52, 60, 255))
        d.line([16, 5, 16, 31], fill=(50, 52, 60, 255))
        for (x, y) in [(8, 8), (23, 8), (8, 20), (23, 20)]:
            d.rectangle([x, y, x + 1, y + 1], fill=(170, 176, 190, 255))
        d.rectangle([13, 17, 14, 19], fill=(40, 40, 40, 255))
        d.rectangle([18, 17, 19, 19], fill=(40, 40, 40, 255))
    else:
        light = [(255, 255, 160, 255), (120, 255, 120, 255)][open_frame]
        d.rectangle([5, 5, 26, 31], fill=(10, 10, 20, 255), outline=light)
        d.rectangle([6, 6, 25, 31], outline=light)
        # arrow pointing in
        c = light
        d.polygon([(16, 10), (22, 17), (18, 17), (18, 25), (14, 25), (14, 17), (10, 17)], fill=c)
    return img

# ---------- Explosion (6 frames) ----------
def explosion():
    frames = []
    rnd = random.Random(11)
    for i in range(6):
        img = new()
        r = [6, 10, 14, 15, 15, 13][i]
        fade = [255, 255, 255, 220, 160, 90][i]
        for y in range(S):
            for x in range(S):
                dist = math.hypot(x + 0.5 - 16, y + 0.5 - 16) + rnd.uniform(-2.5, 2.5)
                if dist < r:
                    t = dist / r
                    if i >= 4:
                        col = (120, 110, 100) if t < 0.7 else (80, 70, 60)  # smoke
                    elif t < 0.35:
                        col = (255, 255, 220)
                    elif t < 0.65:
                        col = (255, 210, 60)
                    elif t < 0.85:
                        col = (240, 110, 20)
                    else:
                        col = (170, 40, 20)
                    img.putpixel((x, y), col + (fade,))
        frames.append(img)
    return frames

save("s_Wall", [wall()])
save("s_Dirt", [dirt()])
save("s_Boulder", [boulder()])
save("s_Diamond", diamond())
save("s_PlayerIdle", player_idle())
save("s_PlayerLeft", player_walk(-1))
save("s_PlayerRight", player_walk(1))
save("s_Firefly", firefly())
save("s_ExitClosed", [exit_door()])
save("s_ExitOpen", [exit_door(0), exit_door(1)])
save("s_Explosion", explosion())

# preview sheet
names = ["s_Wall", "s_Dirt", "s_Boulder", "s_Diamond", "s_PlayerIdle", "s_PlayerLeft", "s_PlayerRight",
         "s_Firefly", "s_ExitClosed", "s_ExitOpen", "s_Explosion"]
sheet = Image.new("RGBA", (8 * 36 + 4, len(names) * 36 + 4), (20, 20, 28, 255))
for r, n in enumerate(names):
    files = sorted(os.listdir(os.path.join(OUT, n)), key=lambda f: int(f.split(".")[0]))
    for c, f in enumerate(files):
        im = Image.open(os.path.join(OUT, n, f))
        sheet.alpha_composite(im, (4 + c * 36, 4 + r * 36))
sheet.resize((sheet.width * 3, sheet.height * 3), Image.NEAREST).save(os.path.join(OUT, "preview.png"))
