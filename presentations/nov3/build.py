"""Writes the Nov 3 slides into the deck folder from the results files, so the numbers
can be refreshed when the calibration finishes. Usage: build.py <deck root> <prelim 0|1>."""
import json, math, os, re, sys
import numpy as np, pandas as pd

ROOT, PRELIM = sys.argv[1], sys.argv[2] == "1"
SL = os.path.join(ROOT, "project/slides")
EM = "/Users/mimi/Desktop/동규 컴퓨터 공유 폴더/2026-2/Topics in Macroeconomics/hopenhayn_project/eps_model/"
R6, R5 = json.load(open(EM + "v6_results.json")), json.load(open(EM + "v5_results.json"))
HAS_FINE = os.path.exists(EM + "v6_results_fine.json")
FINE = json.load(open(EM + ("v6_results_fine.json" if HAS_FINE else "v6_results.json")))
EX = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fine_extra.json")))
SV = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "survey.json")))
df = pd.read_stata(os.path.expanduser("~/EPS_data/eps.dta"), convert_categoricals=False)

ORDER_NEW = ["nov3-cover", "nov3-feedback", "nov3-caps", "nov3-survey", "nov3-capuse",
             "nov3-databunch", "nov3-modelbunch", "nov3-targets", "nov3-results", "nov3-outreach", "nov3-assume", "nov3-next"]
FIRST, TOTAL = 27, 26 + len(ORDER_NEW)
PG = {k: FIRST + i for i, k in enumerate(ORDER_NEW)}
SERIF, SANS = "'Source Serif 4', Georgia, serif", "'IBM Plex Sans', Arial, sans-serif"
NAVY, INK, BODY, MUTED, RUST, STEEL = "#14213d", "#1f2a3c", "#3d4756", "#5f6876", "#a8432c", "#2f5d8a"
BLUE, ORANGE = "#2a78d6", "#eb6834"
LOGO = "/_blob/921ccfeb3c9f6d9c3ed1cc4a5be8bdd4"
PRESENTERS = {"nov3-cover": "Julian", "nov3-feedback": "Julian", "nov3-caps": "Julian", "nov3-survey": "Mimi", "nov3-capuse": "Mimi",
              "nov3-databunch": "Mimi", "nov3-modelbunch": "Sara", "nov3-targets": "Sara", "nov3-results": "Sara",
              "nov3-outreach": "Donny", "nov3-assume": "Donny", "nov3-next": "Donny"}
PRESENTER = "[name]"
TAG = " Preliminary: calibration still running." if PRELIM else ""


def pct(x, d=1, sign=False):
    return f"{100 * x:{'+' if sign else ''}.{d}f}%".replace("-", "−")


def page(id_, dark=False):
    return (f'<p style="position:absolute; right:128px; bottom:40px; width:160px; font-family:{SANS}; font-size:24px; '
            f'text-align:right; color:{"#c9d1de" if dark else "#8a94a6"}">{PG[id_]}/{TOTAL}</p>')


def logo():
    return f'<img src="{LOGO}" alt="Logo" style="position:absolute; right:8px; bottom:952.01px; width:112.01px; height:114.78px">'


def presenter(dark=False):
    return (f'<p style="position:absolute; top:64px; right:128px; width:480px; font-family:{SANS}; font-size:24px; font-weight:600; '
            f'text-align:right; color:{"#c9d1de" if dark else MUTED}">Presenter: {PRESENTER}</p>')


def foot(text):
    return (f'<p style="position:absolute; bottom:40px; left:128px; width:1440px; font-family:{SANS}; font-size:24px; '
            f'color:{MUTED}">{text}</p>')


def h2(text, size=52):
    return f'<h2 style="font-family:{SERIF}; font-size:{size}px; font-weight:600; line-height:1.15; color:{NAVY}">{text}</h2>'


EQS = ["(1) y = s·(h^ρ + λₜ ℓ^ρ)^(α/ρ), ℓ = k + m", "(2) cost of k = w·(1 + ψ(1 + h)^−ξ)", "(3) Current rule: m ≤ θ·q(h), cost ≈ w",
       "(4) No size rule: cost of m = w + p", "(5) Exit if β(1−δ)E[V(s′)] &lt; 0; Σν V = cₑ", "(6) Σμ(h + k) = N, Σμ m = M"]


def eqs(on):
    cells = "".join(
        f'<p style="font-family:{SERIF}; font-size:24px; font-weight:{600 if i + 1 in on else 400}; line-height:1.4; '
        f'color:{NAVY if i + 1 in on else "#a3acba"}">{e}</p>' for i, e in enumerate(EQS))
    return (f'<div style="position:absolute; top:880px; left:128px; width:1664px; height:108px; display:grid; '
            f'grid-template-columns:1fr 1fr 1fr; padding:12px 24px; background:#f4f7fb; border-top:2px solid #d8dee8">{cells}</div>')


def table(rows, widths, size=24, band=True, hi=()):
    head = "".join(f'<th style="width:{w}%">{c}</th>' for c, w in zip(rows[0], widths))
    out = [f"<tr>{head}</tr>"]
    for i, r in enumerate(rows[1:]):
        bg = ' style="background:#fbefea"' if i in hi else (' style="background:#f4f7fb"' if band and i % 2 else "")
        out.append(f"<tr{bg}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return f'<table style="font-family:{SANS}; font-size:{size}px; color:{BODY}">{"".join(out)}</table>'


def box(text, flex=None, size=26):
    fx = f"flex:{flex}; " if flex else ""
    return (f'<p style="{fx}padding:20px 28px; font-family:{SANS}; font-size:{size}px; line-height:1.4; color:{INK}; '
            f'background:#e8eef6; border-left:6px solid {STEEL}; border-radius:12px">{text}</p>')


def card(big, small, hi=False):
    st = f"background:#fbefea; border:3px solid {RUST}" if hi else "background:#f4f7fb; border:1px solid #d8dee8"
    return (f'<div style="display:flex; flex-direction:column; gap:8px; padding:24px 28px; {st}; border-radius:12px">'
            f'<p style="font-family:{SERIF}; font-size:64px; font-weight:600; line-height:1.1; color:{RUST if hi else NAVY}">{big}</p>'
            f'<p style="font-family:{SANS}; font-size:26px; line-height:1.3; color:{BODY}">{small}</p></div>')


def label(x, y, w, text, align="left", color=MUTED, size=24, weight=400):
    return (f'<p style="position:absolute; left:{x:.0f}px; top:{y:.0f}px; width:{w:.0f}px; font-family:{SANS}; font-size:{size}px; '
            f'font-weight:{weight}; line-height:1.2; text-align:{align}; color:{color}">{text}</p>')


def legend(x, y, items):
    out = []
    for name, col, dash in items:
        pat = f'<svg aria-label="{name} key" width="48" height="8" viewBox="0 0 48 8" style="position:absolute; left:{x}px; top:{y + 12}px; width:48px; height:8px"><line x1="0" y1="4" x2="48" y2="4" stroke="{col}" stroke-width="4"{" stroke-dasharray=\"10 7\"" if dash else ""}/></svg>'
        w = int(len(name) * 14.5) + 16
        out += [pat, label(x + 58, y, w, name, color=INK)]
        x += 58 + w + 24
    return "".join(out)


def section(id_, body, notes, style=None):
    style = style or "display:flex; flex-direction:column; gap:28px; padding:128px 128px 160px; background:#ffffff"
    return f'<section id="{id_}" data-transition="fade" style="{style}">\n{body}\n<aside>{notes}</aside>\n</section>\n'


PAGE_EDITED = {"nov3-cover", "nov3-feedback"}                # edited by hand on the deck page; keep the live versions


def write(id_, html):
    if id_ in PAGE_EDITED:
        return
    assert html.count("Presenter: [name]") == 1
    html = html.replace("Presenter: [name]", "Presenter: " + PRESENTERS[id_])
    assert len(re.findall("<svg", html)) < 12
    open(os.path.join(SL, id_ + ".html"), "w").write(html)


SECT_EQ = "display:flex; flex-direction:column; gap:28px; padding:128px 128px 220px; background:#ffffff"
res = R6["net_Y_change_vs_current"]
res5 = R5["net_Y_change_vs_current"]
gain, up, down, noeps = (res[k] for k in ("size-neutral, same quota (by price)", "current rule, quota +50%", "current rule, quota -50%", "no EPS"))
gain5, up5, down5, noeps5 = (res5[k] for k in ("size-neutral, same quota (by price)", "current rule, quota +50%", "current rule, quota -50%", "no EPS"))
ratio = gain / up
fit, lp = R6["fit"], R6["lpy"]
above_line = ratio >= 0.10
fine_gain = FINE["net_Y_change_neutral"]
fine_ratio = fine_gain / EX["up_change"]
below = ratio < 0.10 and fine_ratio < 0.10
line_word = "below" if below else "at"
fine_slope = FINE["fit"]["slope_lpy"]

# ------------------------------------------------------------------ 27 cover
RQ = ("<b>Research question.</b> Korea's Employment Permit System (EPS) ties a manufacturing plant's access to foreign workers to its size. "
      "Does this size-dependent allocation keep low-productivity plants in business and lower aggregate productivity, and how much would "
      "output change if the same national quota were allocated without regard to plant size?")
write("nov3-cover", section("nov3-cover", f"""
<h1 style="position:absolute; top:150px; left:128px; width:1664px; font-family:{SERIF}; font-size:88px; font-weight:600; line-height:1.1; color:#f7f5f0">EPS project update:<br>what changed since your feedback</h1>
<p style="position:absolute; top:376px; left:128px; width:1664px; font-family:{SANS}; font-size:36px; line-height:1.4; color:#c9d1de">November 3, 2026 · The cap schedule, bunching, new survey data, corrected targets and results</p>
<p style="position:absolute; top:490px; left:128px; width:1664px; font-family:{SERIF}; font-size:38px; line-height:1.4; color:#f7f5f0">{RQ}</p>
<p style="position:absolute; bottom:96px; left:128px; width:1664px; font-family:{SANS}; font-size:26px; line-height:1.5; color:#c9d1de">Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo<br>ISA6327 Topics in Macroeconomics · Prof. Sewon Hur · November 3, 2026</p>
{presenter(True)}{page("nov3-cover", True)}{logo()}""",
f"""▶ TITLE. Good afternoon. Today we report what we did with your feedback from October 27 and your comments on the proposal. ▶ RESEARCH QUESTION. Our question has not changed. ▶ SUBTITLE. We will cover five things: the cap schedule you questioned, bunching in the model and in the data, a firm-level survey we found, three calibration targets we corrected, and what that does to our result. We finish with the assumptions we are making, and why we still want to contact the survey's authors and the Ministry, which we want to check with you first.""",
"background:#14213d"))

# ------------------------------------------------------------------ 28 feedback
gp = pct(gain, 2, True) if PRELIM else pct(gain, 2, True)
rows = [["What you asked", "What we did", "Status"],
        ["See bunching, at least in the model", f"Size grid now contains every cap step (slide {PG['nov3-modelbunch']}); compared with the data on slide {PG['nov3-databunch']}", "Done"],
        ["A fatter tail for large plants", f"Productivity s = x·z, with x drawn from Pareto(1, γ); plants with 50+ workers now {pct(fit['share_50plus'], 1)} vs. 2.1% in the data", "Done"],
        ["0.4% looks small", f"Bunching raised it to {pct(gain5, 1, True)}; three corrected targets bring it to {gp} (slides {PG['nov3-targets']}–{PG['nov3-results']})", "Open"],
        ["Cap numbers and Figure 1 do not add up", f"Re-checked at eps.go.kr: our sentence left out a limit; figure redrawn (slide {PG['nov3-caps']})", "Done"],
        ["Look at the data; lean toward what is meaningful", f"Found firm-level EPS data for 772 manufacturers (slides {PG['nov3-survey']}–{PG['nov3-databunch']})", "Done"],
        ["H-1B frictions may depend on firm size", "Agreed: visa paperwork weighs more on small firms; our fixed cost of using EPS plays this role", "Noted"],
        ["Did you account for population?", "Korean labor N is fixed; quota experiments add or remove EPS workers; no growth rate yet", "Next"],
        ["State every assumption", f"Listed and checked against the survey (slide {PG['nov3-assume']})", "Done"]]
write("nov3-feedback", section("nov3-feedback", f"""
{h2("Your feedback: what you asked, and what we did")}
{table(rows, [31, 59, 10], 24)}
{foot(f"Your written summary mentioned about −0.5% from removing EPS; our Oct 27 slide showed −7.5% (now {pct(noeps, 1)}).")}
{presenter()}{page("nov3-feedback")}{logo()}""",
f"""▶ TITLE. Here is everything you raised, and where it stands. ▶ ROW 1. You said we should at least see bunching in the model. Now we do; slide {PG['nov3-modelbunch']}. ▶ ROW 2. You suggested a fatter tail. Productivity now has a permanent part drawn from a Pareto distribution, as in your model. ▶ ROW 3. You said 0.4 percent looked small. Bunching and the tail raised it to about 1 percent, but when we corrected three targets it came back down. This one is still open. ▶ ROW 4. Your comment on the cap numbers was right to flag a problem; our sentence was incomplete. ▶ ROW 5. You told us to look at the data. We found firm-level data on EPS workers. ▶ ROW 6. Your H-1B point: agreed. Paperwork is a bigger burden for small firms, and our fixed cost of using EPS captures that. ▶ ROW 7. Population. Korean labor is fixed, and the quota experiments only add or remove EPS workers. Only the ratio of the quota to Korean labor matters. There is no population growth rate yet; it is on our list. ▶ ROW 8. The full list of assumptions is on slide {PG['nov3-assume']}.
IF ASKED about wages: the Korean wage is solved in general equilibrium, pinned by free entry."""))

# ------------------------------------------------------------------ 29 caps
def cap24(n): return n + 10 if n <= 10 else min(30, 2 * n) if n <= 50 else 35 if n <= 100 else 40 if n <= 150 else 50 if n <= 200 else 60
def cap19(n):
    for hi, q in [(5, 5), (10, 7), (30, 10), (50, 12), (100, 15), (150, 20), (200, 25)]:
        if n <= hi: return q
    return 30

def cap_panel(x0, fn, ymax, yticks, fmt, name):
    W, H, L, B, T = 470, 340, 74, 4, 8
    X = lambda n: L + (W - L - 8) * math.log(n) / math.log(300)
    Y = lambda v: T + (H - T - B) * (1 - v / ymax)
    p = lambda cap: "M" + " L".join(f"{X(n):.1f},{Y(fn(n, cap(n))):.1f}" for n in range(1, 301))
    s = [f'<svg aria-label="{name}: 2024 and 2019 schedules by Korean workers" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:{x0}px; top:292px; width:{W}px; height:{H}px">']
    for v in yticks:
        s.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W - 4}" y2="{Y(v):.1f}" stroke="#d8dee8" stroke-width="1.5"/>')
    s.append(f'<path d="{p(cap19)}" fill="none" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="10 7"/>')
    s.append(f'<path d="{p(cap24)}" fill="none" stroke="{BLUE}" stroke-width="4"/></svg>')
    out = ["".join(s)]
    for v in yticks:
        out.append(label(x0 - 6, 292 + Y(v) - 14, 72, fmt(v), "right"))
    for n in (1, 3, 10, 30, 100, 300):
        out.append(label(x0 + X(n) - 30, 636, 60, str(n), "center"))
    return "".join(out)

chart = (cap_panel(128, lambda n, q: q, 70, (0, 20, 40, 60), lambda v: f"{v}", "Foreign-worker cap") +
         cap_panel(628, lambda n, q: q / (q + n), 1.0, (0, .25, .5, .75, 1), lambda v: f"{100 * v:.0f}%", "Maximum foreign share"))
rows = [["Korean workers", "2024 cap", "Max share", "2019 cap", "Max share"]]
for n in (3, 10, 11, 15, 50, 250):
    a, b = cap24(n), cap19(n)
    rows.append([n, a, f"{100 * a / (a + n):.0f}%", b, f"{100 * b / (b + n):.0f}%"])
write("nov3-caps", section("nov3-caps", f"""
{h2("Cap schedule: re-checked at the source and redrawn")}
{legend(128, 212, [("2024 caps", BLUE, False), ("2019 caps", ORANGE, True)])}
{label(128, 252, 470, "Cap, in foreign workers", color=NAVY, size=26, weight=600)}
{label(628, 252, 470, "Maximum foreign share of workers", color=NAVY, size=26, weight=600)}
{chart}
{label(128, 668, 970, "Korean insured workers at the plant (log scale)", "center")}
<div style="position:absolute; left:1136px; top:212px; width:656px">{table(rows, [28, 17, 19, 17, 19], 24)}</div>
<p style="position:absolute; left:128px; top:716px; width:1664px; padding:18px 28px; font-family:{SANS}; font-size:26px; line-height:1.4; color:{INK}; background:#e8eef6; border-left:6px solid {STEEL}; border-radius:12px"><b>The rule:</b> Koreans + 10 for 1–10 Korean workers; 30 for 11–50, <b>but at most twice the Korean workers</b>, the limit our sentence left out; 35, 40, 50 and 60 up to 300.<br>So 10 Koreans may hire 20 (67%, not 50%); 11 may hire 22 (67%, not 75%); 30 is first reached at 15. The 81% is the share at 3 Koreans: 13 ÷ 16.</p>
{foot("Sources: eps.go.kr, 2024 schedule; Lee, Peri and Yang (2026, Table 4) for 2019. Share = cap ÷ (Korean workers + cap).")}
{presenter()}{page("nov3-caps")}{logo()}""",
f"""▶ TITLE. You asked us to re-check the schedule and redraw the figure. We checked it against the EPS site. ▶ BLUE BOX, FIRST LINE. The schedule is Koreans plus 10 for plants with 1 to 10 Korean workers. For 11 to 50 it is 30, but never more than twice the number of Korean workers. Our proposal sentence left out that limit, and that is why the numbers looked wrong to you. ▶ LEFT CHART. The cap in workers: you can see 20 at 10 Koreans, then 22 at 11, reaching 30 at 15. ▶ RIGHT CHART. The share: the blue line is flat at 67 percent between 10 and 15, then falls. The figure in the proposal plotted this correctly; the sentence was the problem. ▶ TABLE. At 10 Koreans the cap is 20, so 67 percent, not 50. At 11 it is 22, so still 67 percent. The 81 percent we quoted is at 3 Korean workers, 13 out of 16. ▶ IF ASKED. Root industries may hire 20 percent above the cap, which the model ignores; it is on our assumptions list. The page does not state outright that the cap limits the stock, but it is labelled total allowed workers, and Dong, Lee and Yang's table separates it from a limit on new permits.""", ))

# ------------------------------------------------------------------ 30 model bunching
def stairs(ex):
    b = ex["bunching"]
    e, h = np.array(b["hist_edges"]), np.array(b["hist"])
    return e, h / np.diff(e)

cur, neu = FINE["experiments"]["current rule"], FINE["experiments"]["size-neutral, same quota (by price)"]
W, H, L = 1040, 510, 84
xmin, xmax, ymin, ymax = 20, 400, 1e-6, 3e-3
X = lambda v: L + (W - L - 8) * (v - xmin) / (xmax - xmin)
Y = lambda v: 8 + (H - 12) * (1 - (math.log10(max(v, ymin)) - math.log10(ymin)) / (math.log10(ymax) - math.log10(ymin)))
def spath(ex):
    e, d = stairs(ex)
    pts, first = [], True
    for a, b, v in zip(e[:-1], e[1:], d):
        if a < xmin or a >= 380: continue
        pts += [(X(a), Y(v)), (X(b), Y(v))]
    return "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
svg = [f'<svg aria-label="Plant density by Korean core workers: current rule against no size rule" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:128px; top:252px; width:{W}px; height:{H}px">']
for v in (1e-3, 1e-4, 1e-5, 1e-6):
    svg.append(f'<line x1="{L}" y1="{Y(v):.1f}" x2="{W - 4}" y2="{Y(v):.1f}" stroke="#d8dee8" stroke-width="1.5"/>')
for t in (50, 100, 150, 200, 300):
    svg.append(f'<line x1="{X(t):.1f}" y1="8" x2="{X(t):.1f}" y2="{H - 4}" stroke="{MUTED}" stroke-width="1.5" stroke-dasharray="6 6"/>')
svg.append(f'<path d="{spath(neu)}" fill="none" stroke="{ORANGE}" stroke-width="4" stroke-dasharray="10 7"/>')
svg.append(f'<path d="{spath(cur)}" fill="none" stroke="{BLUE}" stroke-width="4"/></svg>')
ticks = "".join(label(128 - 4, 252 + Y(v) - 14, 80, s, "right") for v, s in ((1e-3, "10⁻³"), (1e-4, "10⁻⁴"), (1e-5, "10⁻⁵"), (1e-6, "10⁻⁶")))
ticks += "".join(label(128 + X(t) - 30, 766, 60, str(t), "center") for t in (20, 50, 100, 150, 200, 300, 400))
steps = cur["bunching"]["steps"]
ratios = {t: steps[str(t)]["density_above"] / max(steps[str(t)]["density_below"], 1e-12) for t in (50, 100, 150, 200, 300)}
rneu = {t: neu["bunching"]["steps"][str(t)]["density_above"] / max(neu["bunching"]["steps"][str(t)]["density_below"], 1e-12) for t in (50, 100, 150, 200, 300)}
MODEL_TITLE = "Model bunching: plants pile up at the cap steps"
rows = [["Cap step", "Current rule", "No size rule"]] + [[("Under 300" if t == 300 else t), f"{ratios[t]:.2f}", f"{rneu[t]:.2f}"] for t in (50, 100, 150, 200, 300)]
write("nov3-modelbunch", section("nov3-modelbunch", f"""
{h2(MODEL_TITLE)}
{legend(128, 208, [("Current rule (2024 caps)", BLUE, False), ("Same quota, no size rule", ORANGE, True)])}
{"".join(svg)}{ticks}
{label(128, 800, 1040, "Korean core workers at the plant, h. Vertical axis: share of plants per worker (log scale). Dashed lines: cap steps.", "left")}
<div style="position:absolute; left:1200px; top:208px; width:592px; display:flex; flex-direction:column; gap:20px">
<p style="font-family:{SANS}; font-size:26px; line-height:1.35; color:{BODY}">Density just past each step ÷ density just below it. A value of 1 means no bunching.</p>
{table(rows, [36, 32, 32], 24)}
<p style="padding:18px 24px; font-family:{SANS}; font-size:26px; line-height:1.35; color:{INK}; background:#e8eef6; border-left:6px solid {STEEL}; border-radius:12px"><b>What changed:</b> a Pareto tail, so plants reach these sizes, and a size grid with every cap step. Version 4 had neither.</p>
</div>
{foot(("Model solved on a finer productivity grid (48 × 21)." if HAS_FINE else "Calibration grid (24 × 11); single productivity levels can land on a step by chance.") + TAG)}
{eqs({1, 3})}
{presenter()}{page("nov3-modelbunch")}{logo()}""",
f"""▶ TITLE. You told us that with a size-based cap, profit-maximizing plants should bunch, and that if the model does not show it, the model is wrong. Version 4 showed none. ▶ BLUE BOX. We fixed two things. The Pareto tail, so that plants reach sizes of 100 or 200, and a size grid containing every cap step, so a plant can locate exactly where the rule rewards it. ▶ CHART. Blue is the current rule; the dashed orange line is the same quota with no size rule. ▶ TABLE. This is density just past each step divided by density just below it. 1 means no bunching. Under the current rule it sits above 1 at most steps, and removing the rule brings it to about 1. Just under 300 the ratio is below 1 because plants stop before losing eligibility. ▶ EQUATION (3). The bunching comes from this line: the cap q(h) jumps at each step. ▶ CAVEAT. The model applies the cap to core Korean workers h, while the law counts all insured Koreans. That is on our assumptions list.{" These are preliminary numbers." if PRELIM else ""}""", SECT_EQ))

# ------------------------------------------------------------------ 31 survey
rows = [["", "EPS survey (KDI with the World Bank)"],
        ["When", "August–October 2019; a second wave in January 2021 is not in the public file"],
        ["Sample", "1,000 of 51,619 EPS firms, 144 strata by region, industry and size; 772 in manufacturing"],
        ["Per firm", "Korean workers, EPS workers, wages, tasks, dorm and meal costs, extra EPS workers wanted"],
        ["Access", "Replication file published with Dong, Lee and Yang (2024, <i>Oxford Economic Papers</i>)"],
        ["Limits", "EPS users only; 2019 caps; 27.6% response; closures not in the file"]]
cards = "".join(card(a, b) for a, b in [(f"{SV['total']:.1f}", "workers per firm"), (f"{SV['korean']:.1f}", "Korean workers"), (f"{SV['eps']:.1f}", "EPS workers"), (f"{100 * SV['share']:.0f}%", "average EPS share")])
write("nov3-survey", section("nov3-survey", f"""
{h2("New data: EPS and Korean workers at each surveyed firm")}
<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:24px">{cards}</div>
{table(rows, [12, 88], 26)}
{box("Until now we used only published tables from this survey. It is the data you told us to look for, but a sample of users, not all plants.")}
{foot("Dong, Lee and Yang (2024), <i>Oxford Economic Papers</i> 76(2); Lee, Peri and Yang (2026) use the same survey. Aggregates only.")}
{presenter()}{page("nov3-survey")}{logo()}""",
f"""▶ TITLE. You asked us to look for meaningful data. We found a firm-level survey of EPS employers. ▶ CARDS. The average firm has about 20 workers, 15 and a half Korean and 5 EPS. The average EPS share is 38 percent. ▶ TABLE. KDI ran it with the World Bank in 2019. It sampled 1,000 of about 51,600 EPS firms, 772 in manufacturing. The data are published as the replication file of Dong, Lee and Yang, 2024. Lee, Peri and Yang use the same survey in the paper we calibrate to. ▶ TABLE, LIMITS. It covers EPS users only, under the 2019 caps, with a 27.6 percent response rate. The public file does not include the 2021 wave, so no closures. ▶ BLUE BOX. So this is real firm-level data, but not all plants. The next two slides show what it says about caps and bunching."""))

# ------------------------------------------------------------------ 32 cap use
def cap(n): return np.select([n <= 5, n <= 10, n <= 30, n <= 50, n <= 100, n <= 150, n <= 200], [5, 7, 10, 12, 15, 20, 25], 30)
kl, mm, q9 = df.korean.astype(float), df.q13_1a.astype(float), df.q9.astype(float)
use = mm / cap(kl)
rows = [["Korean workers", "Firms", "EPS workers", "2019 cap", "Share of cap used", "Want more"]]
for a, b, c in [(0, 5, "5"), (5, 10, "7"), (10, 30, "10"), (30, 50, "12"), (50, 100, "15"), (100, 300, "20–30")]:
    s = ((kl > a) | (a == 0)) & (kl <= b)
    rows.append([f"{a + 1 if a else 0}–{b}", int(s.sum()), f"{mm[s].mean():.1f}", c, f"{100 * use[s].mean():.0f}%", f"{100 * (q9[s] > 0).mean():.0f}%"])
cards = "".join(card(a, b, h) for a, b, h in [(f"{100 * SV['use_mean']:.0f}%", "average share of cap used", True), (f"{100 * SV['below_half']:.0f}%", "use less than half", False), (f"{100 * SV['at_or_above']:.0f}%", "at or above their cap", False), (f"{100 * SV['want_more']:.0f}%", "would hire more with no limit", False)])
write("nov3-capuse", section("nov3-capuse", f"""
{h2("Cap use: firms use about 60% of their cap, at nearly every size")}
<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:24px">{cards}</div>
<div style="display:flex; flex-direction:row; gap:32px">
<div style="display:flex; flex-direction:column; flex:3">{table(rows, [22, 12, 17, 13, 21, 15], 24)}</div>
{box(f"Equation (3) is about right on average: the model gives {100 * lp['use_of_cap']:.0f}%, flat by construction. But it gives every plant nearly the same share, and every user wants more. In the data, {100 * (1 - SV['want_more']):.0f}% do not.", 2, 24)}
</div>
{eqs({3})}
{foot("EPS survey, 772 manufacturers; Korean workers from the EPS firm list, Feb 2019. 2019 caps." + TAG)}
{presenter()}{page("nov3-capuse")}{logo()}""",
f"""▶ TITLE. This is the number we were missing: how close firms are to their caps. ▶ FIRST CARD. Firms use 62 percent of their cap on average. ▶ TABLE. And it is nearly the same at every size, around 60 percent, which supports the way equation (3) treats rationing on average. The bottom row has only 16 firms. ▶ CARDS 2 AND 3. But firms differ a lot: 42 percent use less than half, and 18 percent are at or above the cap. Some sectors and regions were allowed extra. ▶ LAST CARD AND LAST COLUMN. The survey asks how many more workers the firm would hire with no limit. 44 percent would hire more. So more than half would not. ▶ BLUE BOX. In the model every user is constrained and wants more, so this is the assumption we most need to fix. ▶ IF ASKED: why are firms below the cap but still wanting more? Dong, Lee and Yang describe a points ranking with a cut-off, and a limit of 3 to 6 new permits per round. Our model has neither. Source: the EPS survey, with Korean workers from the EPS firm list of February 2019.""", SECT_EQ))

# ------------------------------------------------------------------ 33 data bunching
lc, sc = SV["list_counts"], SV["survey_counts"]
ms = [100 * v for v in EX["by_korean"]]
ls_, ss_ = [100 * v / SV["n"] for v in lc], [100 * v / SV["n"] for v in sc]
W, H, L = 1040, 470, 60
ym = 40
bw = (W - L - 8) / 20
Yb = lambda v: 8 + (H - 12) * (1 - v / ym)
svg = [f'<svg aria-label="Share of EPS firms by Korean workers, 1 to 20: firm list, survey answer and model" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="position:absolute; left:128px; top:272px; width:{W}px; height:{H}px">']
for v in (0, 10, 20, 30, 40):
    svg.append(f'<line x1="{L}" y1="{Yb(v):.1f}" x2="{W - 4}" y2="{Yb(v):.1f}" stroke="#d8dee8" stroke-width="1.5"/>')
for i_ in range(20):
    x = L + i_ * bw
    svg.append(f'<rect x="{x + 3:.1f}" y="{Yb(ls_[i_]):.1f}" width="{bw / 2 - 4:.1f}" height="{Yb(0) - Yb(ls_[i_]):.1f}" rx="2" fill="{BLUE}"/>')
    svg.append(f'<rect x="{x + bw / 2 + 1:.1f}" y="{Yb(ss_[i_]):.1f}" width="{bw / 2 - 4:.1f}" height="{Yb(0) - Yb(ss_[i_]):.1f}" rx="2" fill="{ORANGE}"/>')
for t_ in (5, 10):
    x = L + t_ * bw
    svg.append(f'<line x1="{x:.1f}" y1="8" x2="{x:.1f}" y2="{H - 4}" stroke="{MUTED}" stroke-width="2" stroke-dasharray="6 6"/>')
pts = [(L + i_ * bw + bw / 2, Yb(ms[i_])) for i_ in range(20)]
svg.append('<path d="M' + " L".join(f"{a:.1f},{b:.1f}" for a, b in pts) + f'" fill="none" stroke="{NAVY}" stroke-width="3"/>')
svg += [f'<circle cx="{a:.1f}" cy="{b:.1f}" r="6" fill="{NAVY}" stroke="#ffffff" stroke-width="2"/>' for a, b in pts]
svg.append("</svg>")
ticks = "".join(label(128 + 4, 272 + Yb(v) - 14, 52, f"{v}%", "right") for v in (0, 10, 20, 30, 40))
ticks += "".join(label(128 + L + (k - 1) * bw + bw / 2 - 24, 746, 48, str(k), "center") for k in (1, 3, 5, 6, 8, 10, 11, 13, 15, 17, 20))
ticks += label(128 + L + 5 * bw - 150, 280, 146, "cap 5 → 7", "right", INK) + label(128 + L + 10 * bw + 8, 280, 180, "cap 7 → 10", color=INK)
rows = [["Korean workers", "List", "Survey", "Model"]] + [[("<b>6</b>" if n == 6 else n), f"{ls_[n - 1]:.1f}%", f"{ss_[n - 1]:.1f}%", f"{ms[n - 1]:.1f}%"] for n in (5, 6, 7, 11)]
write("nov3-databunch", section("nov3-databunch", f"""
{h2("Bunching: the data show a small spike; the model piles up far more")}
{legend(128, 212, [("EPS firm list, Feb 2019", BLUE, False), ("Survey answer, Aug 2019", ORANGE, False), ("Model", NAVY, False)])}
{"".join(svg)}{ticks}
{label(128, 784, 1040, "Korean workers at the firm. Vertical axis: share of EPS firms (2019 caps). Model: a plant just past a step counts in the next whole number.", "left")}
<div style="position:absolute; left:1200px; top:212px; width:592px; display:flex; flex-direction:column; gap:16px">
{table(rows, [40, 20, 20, 20], 24)}
<ul style="font-family:{SANS}; font-size:24px; line-height:1.35; color:{BODY}">
<li><b>Data:</b> counts dip at 5, a round number, then jump at 6: 1.4–1.6 times a smooth trend (z = 2.1–2.9)</li>
<li><b>Against:</b> no clear spike past 10, 30 or 50, and 14 and 15 reach similar z</li>
<li><b>Model:</b> {ms[5]:.0f}% of EPS users sit just past 5, with none at 4–5 or 7–10: no frictions, and all get the same share of the cap</li>
<li><b>Limits:</b> users only; too few firms past 50</li>
</ul>
</div>
{foot("EPS survey, 772 manufacturers. Trend: Poisson regression on a polynomial in log workers. Model on the finer grid.")}
{presenter()}{page("nov3-databunch")}{logo()}""", "x"))

# ------------------------------------------------------------------ 34 targets
v5p = {k: R5["params"][k] for k in R5["params"]}
V5 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "v5_newmeasures.json")))
rows = [["Moment", "Data", "Version 5", "Corrected"],
        ["Plants with 1–4 workers", "0.70", f"{V5['share_small']:.2f}", f"{fit['share_small']:.2f}"],
        ["Annual exit rate (assumed)", "8%", pct(V5['exit_rate'], 1), pct(fit['exit_rate'], 1)],
        ["Plants using EPS", "10%", pct(V5['users'], 1), pct(fit['users'], 1)],
        ["Average plant size", "7.5", f"{V5['avg_size']:.1f}", f"{fit['avg_size']:.1f}"],
        ["Plants with 50+ workers", "2.1%", pct(V5['share_50plus'], 1), pct(fit['share_50plus'], 1)],
        ["<b>EPS share, average across firms</b>", "<b>36.9%</b>", pct(V5['eps_share_users'], 1), f"<b>{pct(fit['eps_share_users'], 1)}</b>"],
        ["<b>Workers per EPS firm</b>", "<b>20.8</b>", f"{V5['users_size']:.1f}", f"<b>{fit['users_size']:.1f}</b>"],
        ["<b>Closure slope, size controls</b>", "<b>0.15</b>", f"{V5['slope_lpy']:.2f}", f"<b>{fit['slope_lpy']:.2f}</b> (finer grid: {fine_slope:.2f})"]]
write("nov3-targets", section("nov3-targets", f"""
{h2("Calibration: three targets corrected to match how the data measure them")}
<div style="display:flex; flex-direction:row; gap:32px">
<div style="display:flex; flex-direction:column; flex:3">{table(rows, [46, 11, 15, 28], 24, hi=(5, 6, 7))}</div>
<div style="display:flex; flex-direction:column; gap:12px; flex:2; padding:24px 28px; background:#f4f7fb; border:1px solid #d8dee8; border-radius:16px">
<h3 style="font-family:{SANS}; font-size:28px; font-weight:600; color:{NAVY}">What we had wrong</h3>
<ul style="font-family:{SANS}; font-size:24px; line-height:1.35; color:{BODY}">
<li><b>EPS share:</b> their 36.9% is a simple average across firms; we used an employment-weighted share</li>
<li><b>Firm size:</b> their 20.8 is total workers; our 13 had no clear source</li>
<li><b>Closure slope:</b> every estimate of theirs controls for firm size; ours did not</li>
</ul>
<p style="font-family:{SANS}; font-size:24px; line-height:1.35; color:{RUST}"><b>Still open:</b> the closure slope matches only on the calibration grid</p>
</div>
</div>
{foot("Version 5 column: old parameters, measured the corrected way. Sources: census; Lee, Peri and Yang (2026)." + TAG)}
{eqs({1, 2, 3, 5, 6})}
{presenter()}{page("nov3-targets")}{logo()}""",
f"""▶ TITLE. When we read the survey and the papers closely, we found that three of our targets did not match how the data measure them. These were our mistakes. ▶ RIGHT BOX, FIRST BULLET. EPS share. Their 36.9 percent is a simple average across firms. We were comparing it with an employment-weighted share. ▶ SECOND BULLET. Firm size. Their average is 20.8 total workers. We were targeting 13, which has no clear source. ▶ THIRD BULLET. Closure slope. Every one of their estimates controls for firm size, and ours did not. We now take the average of their size-bin and cubic specifications, about 0.15. ▶ TABLE. Version 5 column shows the old parameters measured the corrected way; it overshot the EPS share and the slope, and undershot firm size. The corrected calibration fits these three closely. ▶ TABLE, TOP ROWS. Plants with 50 or more workers are still low, {pct(fit['share_50plus'], 1)} against 2.1 percent, and small plants a little high. ▶ IF ASKED. The substitution parameter rho and premium decline xi were at the edge of their ranges in version 5, and are no longer.{" These numbers are preliminary; the search is still running." if PRELIM else ""}""", SECT_EQ))

# ------------------------------------------------------------------ 35 results
cards = "".join(card(a, b, h) for a, b, h in [
    (pct(noeps, 1, True), f"No EPS at all<br>(version 5: {pct(noeps5, 1, True)})", False),
    (pct(gain, 2, True), f"<b>Same quota, no size rule</b><br>(version 5: {pct(gain5, 2, True)})", True),
    (pct(up, 1, True), f"Quota +50%<br>(version 5: {pct(up5, 1, True)})", False),
    (pct(down, 1, True), f"Quota −50%<br>(version 5: {pct(down5, 1, True)})", False)])
E6 = R6["experiments"]; c6, n6 = E6["current rule"], E6["size-neutral, same quota (by price)"]
rows = [["Mechanism", "Current rule", "No size rule"],
        ["Plants using EPS", pct(c6["users"], 1), pct(n6["users"], 1)],
        ["Manual-intensive plants", pct(c6["type_share"][1], 1), pct(n6["type_share"][1], 1)],
        ["EPS users’ average size", f"{c6['users_size']:.0f} workers", f"{n6['users_size']:.0f} workers"],
        ["Gross output (current = 100)", "100", f"{100 * n6['Y'] / c6['Y']:.1f}"]]
verdict = (f"Removing the size rule gains {ratio:.3f} of a 50% quota expansion ({fine_ratio:.3f} on a finer grid), {line_word} our kill line of 0.10. "
           f"Robustness and realistic rationing decide it. If it stays below, we refocus on how many workers, not who gets them.")
write("nov3-results", section("nov3-results", f"""
{h2(f"Results: with corrected targets the gain is about {pct(gain, 1, True)}, {line_word} our kill line")}
<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:24px">{cards}</div>
<div style="display:flex; flex-direction:row; gap:32px">
<div style="display:flex; flex-direction:column; flex:3">{table(rows, [44, 28, 28], 26)}</div>
{box(verdict, 2)}
</div>
{foot("Net output = output minus fixed, entry and recruiting costs. Korean labor fixed; quota fixed except ±50%." + TAG)}
{eqs({3, 4, 6})}
{presenter()}{page("nov3-results")}{logo()}""",
f"""▶ TITLE. Here is what the corrections do to our answer. ▶ SECOND CARD. Allocating the same quota without the size rule now raises net output by {pct(gain, 2)}. Version 5, with bunching but the wrong targets, gave {pct(gain5, 2)}. So you were right that bunching can raise the gain, but matching the data properly brings most of it back down. ▶ OTHER CARDS. No EPS at all lowers output by {pct(abs(noeps), 1)}. A 50 percent larger quota raises it by {pct(up, 1)}, and these barely moved. ▶ TABLE. The mechanism is unchanged: without the size rule, fewer and larger plants use EPS, and fewer manual-intensive plants survive. ▶ BLUE BOX. The ratio to a 50 percent quota expansion is {ratio:.3f}. Our kill line, set in the proposal, is one-tenth. We are keeping that line. Robustness and realistic rationing decide it, and if it stays below, the project refocuses on the size of the quota. That would still be a finding: the size rule matters much less than the quota. ▶ IF ASKED: net output is output minus fixed, entry and recruiting costs; Korean labor is fixed, and the quota is fixed except in the plus and minus 50 percent cases.{" These are preliminary numbers; the search is still running." if PRELIM else ""}""", SECT_EQ))

# ------------------------------------------------------------------ 36 outreach
rows = [["What the survey cannot tell us", "Why it matters", "Who holds it", "What we would ask"],
        ["All plants, including non-users, by Korean workers", "A real bunching test needs a comparison group and plants past 50", "MOEL, HRD Korea, KEIS", "Disclosure request for a table of counts, no plant records"],
        ["The 2024 caps", "The current rule is 2024; the survey stops in January 2021", "MOEL, HRD Korea, KEIS", "The same table for 2015–2024"],
        ["Closures by firm in the January 2021 wave", "Our closure target; only published coefficients are available", "Lee and Yang", "Access, or closures by size bin"],
        ["How rationing works in practice", "Firms sit below caps yet want more; the model must explain this", "Lee and Yang", "Is it the points ranking and permit limits?"]]
write("nov3-outreach", section("nov3-outreach", f"""
{h2("Still to request: what the survey cannot tell us, and who holds it")}
{table(rows, [29, 31, 15, 25], 24)}
{box("<b>Why we are raising this with you first:</b> the survey itself is public, so we will not ask for it. Before we write to Prof. Lee and Prof. Yang, or file with the Ministry: is this the right request? And KEIS has a research data system that may need a faculty lead; would that be possible?")}
{foot("We have sent nothing yet. Whether KEIS files identify foreign workers, and who may apply, is not confirmed.")}
{presenter()}{page("nov3-outreach")}{logo()}""",
f"""▶ TITLE. We found the survey ourselves, so a natural question is whether we still need to contact anyone. We think yes, for four things. ▶ ROW 1. The survey covers only EPS users. A real bunching test needs all plants, users and non-users, and enough plants past 50 workers. The Ministry, HRD Korea and KEIS hold those records. They will not release plant-level records, so we would ask for a table of counts. ▶ ROW 2. The survey is from the 2019 caps. The current rule is 2024, so we need that table for recent years too. ▶ ROW 3. Lee, Peri and Yang have a second wave from January 2021 with closures. It is not in the public file, and it is the source of our closure target. Prof. Lee and Prof. Yang are both here at Yonsei. ▶ ROW 4. Firms sit below their caps yet want more, and we want to ask how rationing actually works. ▶ BLUE BOX. We wanted to explain this to you before contacting anyone. Is this the right request? And KEIS has a research data system; we have not confirmed who may apply, or whether it identifies foreign workers, but it may need a faculty lead. Would that be possible?"""))

# ------------------------------------------------------------------ 37 assumptions
rows = [["Assumption in the model", "What the evidence says", "Status"],
        ["EPS workers cost about a Korean wage", f"Survey: wage + dorm and meals = {100 * SV['wage_ratio']:.0f}% of the Korean wage", "Supported"],
        ["The same share θ of the cap for all plants", f"Right on average ({100 * SV['use_mean']:.0f}% at nearly all sizes), but {100 * SV['below_half']:.0f}% use under half", "Too strong"],
        ["Every EPS user wants more workers", f"{100 * (1 - SV['want_more']):.0f}% would not hire more with no limit", "Contradicted"],
        ["EPS and Korean manual workers equally productive", f"Employers: EPS = {SV['prod'][0]:.0f}–{SV['prod'][2]:.0f}% of Korean, rising with experience", "Too strong"],
        ["Cap applies to core Koreans h", "The law counts all insured Koreans (h + k)", "Simplification"],
        ["No points ranking, permit limits or +20% extras", "All three exist; firms exceed the cap in 11% of cases", "Simplification"],
        ["Korean labor N is fixed; no population growth", "Younger cohorts are shrinking; only M/N matters in the model", "Not tested"],
        ["Steady state; output, not welfare; no households", "Fee counted as a transfer; no consumption or remittances", "By design"]]
write("nov3-assume", section("nov3-assume", f"""
{h2("Assumptions: what we are assuming, checked against the survey")}
{table(rows, [40, 46, 14], 24)}
{foot("Also set by us, not estimated: β = 0.96, α = 0.69, ρₛ = 0.90, and a 20% EPS cut with a two-year expected shock for the closure slope.")}
{presenter()}{page("nov3-assume")}{logo()}""",
f"""▶ TITLE. You warned us about assumptions we might not know we were making. Here they are, and for the first time we can check several against data. ▶ ROW 1. EPS workers cost about the same as Koreans. The survey supports this: wage plus dorm and meals is 96 percent of the Korean wage. Our proposal quoted a higher figure, so we will update it. ▶ ROWS 2 AND 3. Rationing. The same share of the cap is right on average but too strong across firms, and many firms do not want more workers. These are the most important ones to fix. ▶ ROW 4. We treat EPS and Korean manual workers as equally productive. Employers rate EPS workers at 74 percent of Koreans in their first year, rising to 96 percent after three to five years. ▶ ROW 5. The cap applies to core Korean workers in the model; the law counts all insured Koreans. ▶ ROW 6. We leave out the points ranking, the limit on new permits and extra allowances. ▶ ROW 7. Korean labor is fixed, with no population growth, the point you raised. ▶ ROW 8. This is a steady-state exercise about output, not welfare. ▶ FOOTER. These parameters we set ourselves. Each of us should be able to defend this list."""))

# ------------------------------------------------------------------ 38 next
SYMS = [("y", "output"), ("s", "productivity, x·z"), ("s′", "next year's productivity"), ("t", "plant type (A light, B manual)"),
        ("h", "Korean core workers"), ("k", "Korean manual workers"), ("m", "EPS workers"), ("ℓ", "manual work, k + m"),
        ("λₜ", "weight on manual work"), ("ρ", "how easily tasks substitute"), ("α", "returns to scale (0.69)"), ("w", "Korean wage"),
        ("ψ, ξ", "size of the premium, its decline"), ("q(h)", "legal EPS cap (0 if ineligible)"), ("θ", "share of the cap granted"), ("p", "permit price (no size rule)"),
        ("β", "discount factor"), ("δ", "exogenous exit rate"), ("V", "value of a plant"), ("ν", "entrants' draw, Pareto tail γ"),
        ("cₑ", "entry cost"), ("μ", "number of plants by state"), ("N", "Korean labor supply"), ("M", "national EPS quota")]
syms = "".join(f'<p style="font-family:{SANS}; font-size:24px; line-height:1.35; color:{BODY}"><b><span style="color:{RUST}">{a}</span></b>  {b}</p>' for a, b in SYMS)
eq_dark = eqs({1, 2, 3, 4, 5, 6})
write("nov3-next", f"""<section id="nov3-next" data-transition="fade" style="display:flex; flex-direction:column; gap:28px; padding:128px 128px 220px; background:#14213d">
<h2 style="font-family:{SERIF}; font-size:56px; font-weight:600; line-height:1.15; color:#f7f5f0">Next steps, and what we would like your feedback on</h2>
<div style="display:flex; flex-direction:row; gap:32px">
<div style="display:flex; flex-direction:column; gap:12px; flex:1; padding:24px 28px; background:#1e2d50; border:1px solid #34446a; border-radius:12px">
<h3 style="font-family:{SANS}; font-size:30px; font-weight:600; color:#f2c4b3">Our next steps</h3>
<ol style="font-family:{SANS}; font-size:26px; line-height:1.35; color:#c9d1de">
<li>Robustness: ρ, shock length, γ, and the closure slope on a finer grid; this decides the kill condition</li>
<li>Rationing from the survey: firms that differ in cap use and demand, which should also soften the pile-up</li>
<li>Add the survey's EPS productivity and costs; population growth if time allows</li>
</ol>
</div>
<div style="display:flex; flex-direction:column; gap:12px; flex:1; padding:24px 28px; background:#1e2d50; border:1px solid #34446a; border-radius:12px">
<h3 style="font-family:{SANS}; font-size:30px; font-weight:600; color:#f2c4b3">Questions for Prof. Hur</h3>
<ol style="font-family:{SANS}; font-size:26px; line-height:1.35; color:#c9d1de">
<li>Can we contact Prof. Lee, Prof. Yang and the Ministry as planned?</li>
<li>How should we model rationing: points, permit limits, or something simpler?</li>
<li>If the gain stays below our line, is refocusing on the quota acceptable?</li>
</ol>
</div>
</div>
<div style="position:absolute; left:128px; top:594px; width:1664px; height:286px; display:flex; flex-direction:column; gap:8px; padding:20px 24px 12px; background:#f4f7fb; border-radius:12px 12px 0 0">
<h3 style="font-family:{SANS}; font-size:26px; font-weight:600; color:{NAVY}">Symbols in equations (1)–(6)</h3>
<div style="display:grid; grid-template-columns:1fr 1fr 1fr 1fr; gap:4px 24px">{syms}</div>
</div>
{presenter(True)}
{eq_dark}
{page("nov3-next", True)}{logo()}
<aside>▶ LEFT, STEP 1. Next we run the robustness checks; they decide the kill condition. ▶ STEP 2. We use the survey to make rationing realistic, with firms that differ in how much of their cap they use and whether they want more. ▶ STEP 3. We add the survey's numbers on EPS productivity and costs, and a population growth rate if time allows. ▶ RIGHT, QUESTION 1. Can we go ahead and contact Prof. Lee, Prof. Yang and the Ministry? ▶ QUESTION 2. How should we model rationing: the actual points system and permit limits, or something simpler? ▶ QUESTION 3. If the gain stays below our line, is refocusing on the quota acceptable? ▶ LIGHT PANEL AT THE BOTTOM. Leave this slide up during questions: every symbol is defined here. CLOSE. Thank you. AI disclosure: literature search, data processing, coding and drafting were assisted by Claude (Anthropic); the team checked the results.</aside>
</section>
""")
print("ratio", round(ratio, 4), "gain", round(gain, 4), "above line", above_line)
print(json.dumps({t: round(v, 2) for t, v in ratios.items()}), json.dumps({t: round(v, 2) for t, v in rneu.items()}))
