"""Figures for the proposal. Writes fig_caps.svg and fig_alloc.svg.

Figure 1: maximum foreign-worker share by plant size under the 2019 and 2024 EPS cap
schedules (manufacturing).

Share = cap / (Korean workers + cap). Caps by number of Korean insured workers:
  2024 (eps.go.kr): 1-10: Koreans+10; 11-50: 30 (at most 2x Koreans); 51-100: 35;
                    101-150: 40; 151-200: 50; 201-300: 60
  2019 (Lee, Peri and Yang 2026, Table 4): 1-5: 5; 6-10: 7; 11-30: 10; 31-50: 12;
                    51-100: 15; 101-150: 20; 151-200: 25; 201-300: 30
Colors: categorical slots 1-2 of the dataviz reference palette (validated);
2019 is also dashed so the series stay distinct in grayscale print.

Figure 2: share of all EPS workers by Korean workers at the plant, current rule vs.
same quota without the size rule, from the recalibrated model. Data come from
hopenhayn_project/eps_model/eps_by_size.py (eps_by_size.json). The current rule keeps
blue (it is the 2024-cap series of Figure 1); the size-neutral allocation takes slot 3
(aqua), validated all-pairs with slot 1.
"""
import json
import math

def cap24(n):
    if n <= 10: return n + 10
    if n <= 50: return min(30, 2 * n)
    return 35 if n <= 100 else 40 if n <= 150 else 50 if n <= 200 else 60

def cap19(n):
    for hi, q in [(5, 5), (10, 7), (30, 10), (50, 12), (100, 15), (150, 20), (200, 25)]:
        if n <= hi: return q
    return 30

W, H = 640, 225
L, R, T, B = 58, 108, 16, 44          # plot margins
pw, ph = W - L - R, H - T - B
xs = lambda n: L + pw * math.log(n) / math.log(300)
ys = lambda v: T + ph * (1 - v)
ns = range(1, 301)

def path(cap):
    pts = [(xs(n), ys(cap(n) / (n + cap(n)))) for n in ns]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)

INK, MUTED, GRID = "#1f1f1e", "#5f5e58", "#e3e2dc"
BLUE, ORANGE = "#2a78d6", "#eb6834"
F = 'font-family="Times New Roman, Times, serif"'
out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">',
       f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
for v in (0, .25, .5, .75, 1):
    y = ys(v)
    out.append(f'<line x1="{L}" y1="{y:.1f}" x2="{L+pw}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
    out.append(f'<text x="{L-8}" y="{y+4:.1f}" text-anchor="end" font-size="13" fill="{MUTED}" {F}>{int(v*100)}%</text>')
for n in (1, 3, 10, 30, 100, 300):
    x = xs(n)
    out.append(f'<line x1="{x:.1f}" y1="{T+ph}" x2="{x:.1f}" y2="{T+ph+5}" stroke="{MUTED}" stroke-width="1"/>')
    out.append(f'<text x="{x:.1f}" y="{T+ph+20}" text-anchor="middle" font-size="13" fill="{MUTED}" {F}>{n}</text>')
out.append(f'<text x="{L+pw/2:.1f}" y="{H-6}" text-anchor="middle" font-size="13" fill="{INK}" {F}>Korean insured workers at the plant (log scale)</text>')
out.append(f'<text x="14" y="{T+ph/2:.1f}" text-anchor="middle" font-size="13" fill="{INK}" {F} transform="rotate(-90 14 {T+ph/2:.1f})">Max. foreign share</text>')
out.append(f'<path d="{path(cap19)}" fill="none" stroke="{ORANGE}" stroke-width="2" stroke-dasharray="6 4"/>')
out.append(f'<path d="{path(cap24)}" fill="none" stroke="{BLUE}" stroke-width="2"/>')
# selective markers and labels at 3 and 250 Korean workers
for n, cap, col, dx, dy in [(3, cap24, BLUE, 6, -10), (3, cap19, ORANGE, -34, 20), (250, cap24, BLUE, 6, -10), (250, cap19, ORANGE, -34, 20)]:
    v = cap(n) / (n + cap(n)); x, y = xs(n), ys(v)
    out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="{col}" stroke="#ffffff" stroke-width="2"/>')
    out.append(f'<text x="{x+dx:.1f}" y="{y+dy:.1f}" font-size="13" fill="{INK}" {F}>{int(v*100+0.5)}%</text>')
# direct labels at the right end
for cap, col, lab, dash in [(cap24, BLUE, "2024 caps", ""), (cap19, ORANGE, "2019 caps", ' stroke-dasharray="6 4"')]:
    y = ys(cap(300) / (300 + cap(300)))
    out.append(f'<line x1="{L+pw+6}" y1="{y:.1f}" x2="{L+pw+26}" y2="{y:.1f}" stroke="{col}" stroke-width="2"{dash}/>')
    out.append(f'<text x="{L+pw+30}" y="{y+4:.1f}" font-size="13" fill="{INK}" {F}>{lab}</text>')
out.append('</svg>')
open("fig_caps.svg", "w").write("\n".join(out))
print("wrote fig_caps.svg")

# ---- Figure 2 -------------------------------------------------------------------
AQUA = "#1baf7a"
d = json.load(open("../hopenhayn_project/eps_model/eps_by_size.json"))
W2, H2 = 640, 180
L2, R2, T2, B2 = 58, 16, 30, 40
pw2, ph2 = W2 - L2 - R2, H2 - T2 - B2
TOP = 0.5
y2 = lambda v: T2 + ph2 * (1 - v / TOP)
bw, gap = 54, 2                               # bar width, surface gap between paired bars
gw = pw2 / len(d["bins"])

def bar(x, v, col):
    """Bar anchored to the baseline with a 4px rounded top."""
    yb, yt, r = y2(0), y2(v), 4
    if yb - yt < r:
        return f'<rect x="{x:.1f}" y="{yt:.1f}" width="{bw}" height="{yb-yt:.1f}" fill="{col}"/>'
    return (f'<path d="M{x:.1f},{yb:.1f} V{yt+r:.1f} Q{x:.1f},{yt:.1f} {x+r:.1f},{yt:.1f} '
            f'H{x+bw-r:.1f} Q{x+bw:.1f},{yt:.1f} {x+bw:.1f},{yt+r:.1f} V{yb:.1f} Z" fill="{col}"/>')

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2} {H2}" width="{W2}" height="{H2}">',
       f'<rect width="{W2}" height="{H2}" fill="#ffffff"/>']
for v in (0, .25, .5):
    y = y2(v)
    out.append(f'<line x1="{L2}" y1="{y:.1f}" x2="{L2+pw2}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
    out.append(f'<text x="{L2-8}" y="{y+4:.1f}" text-anchor="end" font-size="13" fill="{MUTED}" {F}>{int(v*100)}%</text>')
for i, lab in enumerate(d["bins"]):
    cx = L2 + gw * (i + .5)
    for j, (key, col) in enumerate([("current", BLUE), ("neutral", AQUA)]):
        v = d[key]["share"][i]
        x = cx - bw - gap / 2 if j == 0 else cx + gap / 2
        out.append(bar(x, v, col))
        out.append(f'<text x="{x+bw/2:.1f}" y="{y2(v)-5:.1f}" text-anchor="middle" font-size="13" fill="{INK}" {F}>{int(v*100+0.5)}%</text>')
    out.append(f'<text x="{cx:.1f}" y="{T2+ph2+18}" text-anchor="middle" font-size="13" fill="{MUTED}" {F}>{lab}</text>')
out.append(f'<text x="{L2+pw2/2:.1f}" y="{H2-6}" text-anchor="middle" font-size="13" fill="{INK}" {F}>Korean workers at the plant</text>')
out.append(f'<text x="14" y="{T2+ph2/2:.1f}" text-anchor="middle" font-size="13" fill="{INK}" {F} transform="rotate(-90 14 {T2+ph2/2:.1f})">Share of EPS workers</text>')
lx = L2 + 4
for col, lab in [(BLUE, "Current rule (2024 caps)"), (AQUA, "Same quota, no size rule")]:
    out.append(f'<rect x="{lx}" y="6" width="12" height="12" rx="2" fill="{col}"/>')
    out.append(f'<text x="{lx+18}" y="16.5" font-size="13" fill="{INK}" {F}>{lab}</text>')
    lx += 200
out.append('</svg>')
open("fig_alloc.svg", "w").write("\n".join(out))
print("wrote fig_alloc.svg")
