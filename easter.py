#!/usr/bin/env python3
"""Easter ASCII animation — 80x24 terminal, ANSI stdout for tcpserver/telnet."""

import sys
import time
import math
import random

WIDTH = 80
HEIGHT = 24

# ── ANSI helpers ─────────────────────────────────────────────────────────────

RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR = "\033[2J"

# Color codes: 0=reset, 1=yellow, 2=green, 3=magenta, 4=cyan, 5=red, 7=blue
COLOR_MAP = {
    0: "",
    1: "\033[33m",       # yellow
    2: "\033[32m",       # green
    3: "\033[35m",       # magenta
    4: "\033[36m",       # cyan
    5: "\033[31m",       # red
    7: "\033[34m",       # blue
}

# Frame buffer: list of 24 rows, each a list of (char, color) tuples
_buf = None


def _init_buf():
    global _buf
    _buf = [[(" ", 0)] * WIDTH for _ in range(HEIGHT)]


def _flush_buf():
    """Render the buffer to stdout as ANSI."""
    out = [CLEAR, "\033[H"]  # clear + home
    for row in _buf:
        cur_color = -1
        for ch, col in row:
            if col != cur_color:
                out.append(RESET)
                if col and col in COLOR_MAP:
                    out.append(COLOR_MAP[col])
                cur_color = col
            out.append(ch)
        out.append(RESET + "\r\n")
    sys.stdout.write("".join(out))
    sys.stdout.flush()


def draw_at(row, col, text, color=0):
    """Draw text into the buffer at an absolute position, clipping to 80x24."""
    if row < 0 or row >= HEIGHT:
        return
    if col < 0:
        text = text[-col:]
        col = 0
    if col >= WIDTH:
        return
    text = text[: WIDTH - col]
    for i, ch in enumerate(text):
        _buf[row][col + i] = (ch, color)


def draw_ground():
    for c in range(WIDTH):
        _buf[20][c] = ("~", 2)
    for r in range(21, HEIGHT):
        for c in range(WIDTH):
            _buf[r][c] = (".", 2)


def draw_flowers(offset=0):
    positions = [5, 14, 23, 37, 48, 55, 64, 72]
    petals = ["@", "*", "o", "@", "*", "o", "@", "*"]
    colors = [3, 5, 1, 4, 3, 5, 1, 3]
    for i, x in enumerate(positions):
        px = (x + offset) % WIDTH
        draw_at(19, px, petals[i], colors[i])
        draw_at(20, px, "|", 2)


def pause(ms):
    _flush_buf()
    time.sleep(ms / 1000.0)


# ── ASCII Art ────────────────────────────────────────────────────────────────

EGG = [
    r"       ____       ",
    r"     /`    `\     ",
    r"    / *  ~~  *\   ",
    r"   | ~~    ~~ |   ",
    r"   |  * ~~ *  |   ",
    r"   | ~~    ~~ |   ",
    r"   |  * ~~ *  |   ",
    r"   | ~~    ~~ |   ",
    r"   |  * ~~ *  |   ",
    r"    \ ~~  ~~ /    ",
    r"     \  **  /     ",
    r"      `----'      ",
]

EGG_CRACK1 = [
    r"       ____       ",
    r"     /`    `\     ",
    r"    / *  ~~  *\   ",
    r"   | ~~    ~~ |   ",
    r"   |  * ~~ *  |   ",
    r"---+/~~----~~\+---",
    r"   |  * ~~ *  |   ",
    r"   | ~~    ~~ |   ",
    r"   |  * ~~ *  |   ",
    r"    \ ~~  ~~ /    ",
    r"     \  **  /     ",
    r"      `----'      ",
]

EGG_CRACK2 = [
    r"       ____       ",
    r"     /`    `\     ",
    r"    / *  ~~  *\   ",
    r"   | ~~    ~~ |   ",
    r"  /   * ~~ *   \  ",
    r"-/  ~~      ~~  \-",
    r" \    * ~~ *    /  ",
    r"   | ~~    ~~ |   ",
    r"   |  * ~~ *  |   ",
    r"    \ ~~  ~~ /    ",
    r"     \  **  /     ",
    r"      `----'      ",
]

EGG_CRACK3 = [
    r"       ____       ",
    r"     /`    `\     ",
    r"    / *  ~~  *\   ",
    r"   | ~~    ~~ |   ",
    r"  /  ` * ~~ * `\  ",
    r" /               \ ",
    r"                   ",
    r"   | ~~    ~~ |   ",
    r"   |  * ~~ *  |   ",
    r"    \ ~~  ~~ /    ",
    r"     \  **  /     ",
    r"      `----'      ",
]

BUNNY_EARS = [
    r"   () ()   ",
    r"   (^ ^)   ",
]

BUNNY_FACE = [
    r"   () ()   ",
    r"   (^ ^)   ",
    "   (>\u00b7<)   ",
    r"    ( )    ",
]

BUNNY_FULL = [
    r"  () ()  ",
    r"  (^ ^)  ",
    "  (>\u00b7<)  ",
    " /|   |\\ ",
    r"  |   |  ",
    r"  d   b  ",
]

BUNNY_HOP1 = [
    r" () ()  ",
    r" (^ ^)  ",
    " (>\u00b7<)  ",
    "/|   |\\ ",
    r" d   b  ",
]

BUNNY_HOP2 = [
    r"  () () ",
    r"  (^ ^) ",
    "  (>\u00b7<) ",
    " /|   |\\",
    r"  d   b ",
]

MINI_EGG1 = [
    r" /\ ",
    r"|~~|",
    r"|**|",
    r" \/ ",
]

MINI_EGG2 = [
    r" /\ ",
    r"|##|",
    r"|@@|",
    r" \/ ",
]

BANNER = [
    r"  _  _                       ___          _           _ ",
    r" | || |__ _ _ __ _ __ _  _  | __|__ _ ___| |_ ___ _ _| |",
    r" | __ / _` | '_ \ '_ \ || | | _|/ _` (_-<  _/ -_) '_|_|",
    r" |_||_\__,_| .__/ .__/\_, | |___\__,_/__/\__\___|_| (_)",
    r"           |_|  |_|   |__/                              ",
]

BANNER_NO = "~ God påske! ~"


# ── Scenes ───────────────────────────────────────────────────────────────────

def scene_egg_appear():
    """Egg fades in line by line."""
    for i in range(len(EGG) + 1):
        _init_buf()
        draw_ground()
        draw_flowers()
        partial = EGG[:i]
        h = len(EGG)
        start_row = 20 - h
        for j, line in enumerate(partial):
            c = (WIDTH - len(line)) // 2
            draw_at(start_row + j, c, line, 1)
        pause(120)
    pause(800)


def scene_egg_crack():
    """Egg cracks open in stages."""
    stages = [EGG, EGG_CRACK1, EGG_CRACK2, EGG_CRACK3]
    for stage in stages:
        _init_buf()
        draw_ground()
        draw_flowers()
        h = len(stage)
        start_row = 20 - h
        for j, line in enumerate(stage):
            c = (WIDTH - len(line)) // 2
            draw_at(start_row + j, c, line, 1)
        pause(500)


def scene_bunny_emerge():
    """Bunny rises from the cracked egg."""
    egg_bottom = [
        r"   | ~~    ~~ |   ",
        r"   |  * ~~ *  |   ",
        r"    \ ~~  ~~ /    ",
        r"     \  **  /     ",
        r"      `----'      ",
    ]
    bunny_stages = [BUNNY_EARS, BUNNY_FACE, BUNNY_FULL]
    for stage in bunny_stages:
        _init_buf()
        draw_ground()
        draw_flowers()
        eb_start = 20 - len(egg_bottom)
        for j, line in enumerate(egg_bottom):
            c = (WIDTH - len(line)) // 2
            draw_at(eb_start + j, c, line, 1)
        bh = len(stage)
        b_start = eb_start - bh
        for j, line in enumerate(stage):
            c = (WIDTH - len(line)) // 2
            draw_at(b_start + j, c, line, 4)
        pause(600)

    for t in range(8):
        _init_buf()
        draw_ground()
        draw_flowers()
        bh = len(BUNNY_FULL)
        b_start = 20 - bh
        for j, line in enumerate(BUNNY_FULL):
            c = (WIDTH - len(line)) // 2
            draw_at(b_start + j, c, line, 4)
        shell_l = r"\_/"
        shell_r = r"/\_"
        sl_x = WIDTH // 2 - 3 - t * 3
        sr_x = WIDTH // 2 + 1 + t * 3
        draw_at(19, sl_x, shell_l, 1)
        draw_at(19, sr_x, shell_r, 1)
        pause(100)

    pause(400)


def scene_bunny_hop():
    """Bunny hops across the screen left to right."""
    frames = [BUNNY_HOP1, BUNNY_HOP2]
    bh = len(BUNNY_HOP1)
    base_row = 20 - bh

    egg_positions = [10, 28, 45, 62, 75]
    egg_types = [MINI_EGG1, MINI_EGG2, MINI_EGG1, MINI_EGG2, MINI_EGG1]
    egg_colors = [3, 5, 1, 4, 3]

    for x in range(-10, WIDTH + 5, 2):
        _init_buf()
        draw_ground()
        draw_flowers()

        for ei, ex in enumerate(egg_positions):
            egg_art = egg_types[ei]
            er = 20 - len(egg_art)
            for j, line in enumerate(egg_art):
                draw_at(er + j, ex, line, egg_colors[ei])

        frame = frames[(x // 2) % 2]
        bounce = -abs(int(2 * math.sin(x * 0.5)))
        for j, line in enumerate(frame):
            draw_at(base_row + j + bounce, x, line, 4)

        pause(60)


def scene_finale():
    """Happy Easter banner with decorations."""
    confetti_chars = ["*", ".", "o", "+", "~"]
    confetti_colors = [1, 3, 4, 5, 7]

    for t in range(60):
        _init_buf()

        if t < 30:
            count = t * 2
        else:
            count = 60
        rng = random.Random(42)
        for _ in range(count):
            cr = rng.randint(0, 6)
            cc = rng.randint(0, WIDTH - 1)
            ci = rng.randint(0, len(confetti_chars) - 1)
            draw_at(cr, cc, confetti_chars[ci], confetti_colors[ci])

        bh = len(BANNER)
        b_start = 2
        for j, line in enumerate(BANNER):
            c = (WIDTH - len(line)) // 2
            draw_at(b_start + j, c, line, 1)

        # "God påske!" below the English banner
        draw_at(b_start + bh + 1, (WIDTH - len(BANNER_NO)) // 2, BANNER_NO, 5)

        bunny_start = b_start + bh + 3
        for j, line in enumerate(BUNNY_FULL):
            c = (WIDTH - len(line)) // 2
            draw_at(bunny_start + j, c, line, 4)

        egg_l = 15
        egg_r = 60
        for j, line in enumerate(MINI_EGG1):
            draw_at(bunny_start + 1 + j, egg_l, line, 3)
        for j, line in enumerate(MINI_EGG2):
            draw_at(bunny_start + 1 + j, egg_r, line, 5)

        for j, line in enumerate(MINI_EGG2):
            draw_at(bunny_start + 1 + j, egg_l + 8, line, 1)
        for j, line in enumerate(MINI_EGG1):
            draw_at(bunny_start + 1 + j, egg_r - 8, line, 7)

        draw_ground()
        draw_flowers()

        pause(100)

    pause(3000)


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()
    try:
        scene_egg_appear()
        scene_egg_crack()
        scene_bunny_emerge()
        scene_bunny_hop()
        scene_finale()
    except (BrokenPipeError, IOError):
        pass
    finally:
        sys.stdout.write(SHOW_CURSOR + RESET)
        sys.stdout.flush()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.stdout.write(SHOW_CURSOR + RESET)
        sys.stdout.flush()
