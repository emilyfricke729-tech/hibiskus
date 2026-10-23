# Author: @F
# Created: 2026

import tkinter as tk
import math


def lerp_color(c1, c2, t):
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return f"#{r:02x}{g:02x}{b:02x}"


def draw_petal(canvas, cx, cy, length, width, angle_deg, col_base, col_tip, strips=18):
    angle_rad = math.radians(angle_deg - 90)

    def profile(t):
        if t < 0.35:
            return (t / 0.35) * (width / 2)
        else:
            return (1 - t) / 0.65 * (width / 2) * 0.22 + (width / 2) * 0.78 * (1 - (t - 0.35) / 0.65)

    cos_a = math.cos(angle_rad)
    sin_a = math.sin(angle_rad)

    def rot(lx, ly):
        return cx + lx * cos_a - ly * sin_a, cy + lx * sin_a + ly * cos_a

    for i in range(strips):
        t0 = i / strips
        t1 = (i + 1) / strips
        y0 = t0 * length
        y1 = t1 * length
        w0 = profile(t0)
        w1 = profile(t1)

        pts = [rot(x, y) for x, y in [(-w0, y0), (w0, y0), (w1, y1), (-w1, y1)]]
        flat = [c for p in pts for c in p]
        canvas.create_polygon(flat, fill=lerp_color(col_base, col_tip, (t0 + t1) / 2), outline="")

    x0, y0 = rot(0, length * 0.05)
    x1, y1 = rot(0, length * 0.88)
    canvas.create_line(x0, y0, x1, y1, fill="#ffffff", width=1, stipple="gray25")


def draw_stamen(canvas, cx, cy):
    slen = 72
    n = 20
    for i in range(n):
        t0 = i / n
        t1 = (i + 1) / n
        canvas.create_line(cx, cy - t0 * slen, cx, cy - t1 * slen,
                           fill=lerp_color("#cc3300", "#ffcc44", (t0 + t1) / 2),
                           width=5, capstyle=tk.ROUND)

    bx, by = cx, cy - slen - 8
    canvas.create_oval(bx - 9, by - 9, bx + 9, by + 9, fill="#ffd600", outline="#cc8800", width=1)
    canvas.create_oval(bx - 3, by - 5, bx + 2, by - 1, fill="#fffde7", outline="")

    for ox, oy in [(10, 6), (-10, 6), (14, -1), (-14, -1), (0, -13), (6, -12), (-6, -12)]:
        px, py = bx + ox, by + oy
        canvas.create_oval(px - 2.5, py - 2.5, px + 2.5, py + 2.5, fill="#ffee58", outline="")


def main():
    root = tk.Tk()
    root.title("Hibiskus")
    root.configure(bg="#0a0a0a")

    W, H = 520, 520
    canvas = tk.Canvas(root, width=W, height=H, bg="#0a0a0a", highlightthickness=0)
    canvas.pack(padx=20, pady=20)

    cx, cy = W // 2, H // 2

    farben = [
        ("#7a0000", "#ffaa44"),
        ("#8b0000", "#ff9933"),
        ("#6e0000", "#ffb347"),
        ("#800000", "#ff9922"),
        ("#750000", "#ffaa33"),
    ]

    for i, (base, tip) in enumerate(farben):
        draw_petal(canvas, cx, cy, 148, 108, i * 72, base, tip)

    r = 30
    for step in range(20, 0, -1):
        t = (20 - step) / 20
        col = lerp_color("#000000", "#3a0000", t)
        s = r * (step / 20)
        canvas.create_oval(cx - s, cy - s, cx + s, cy + s, fill=col, outline="")
    canvas.create_oval(cx - r - 3, cy - r - 3, cx + r + 3, cy + r + 3, fill="", outline="#7a1000", width=2)

    draw_stamen(canvas, cx, cy)

    root.mainloop()


main()
