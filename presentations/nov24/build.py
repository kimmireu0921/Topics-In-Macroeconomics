"""Writes the Nov 24 slides into the deck folder from the v8 results.
Usage: build.py <deck root>. Image URLs come from blobs.json (uploaded fig_*.png)."""
import json, os, sys

import numpy as np

ROOT = sys.argv[1]
SL = os.path.join(ROOT, "project/slides")
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, "../../hopenhayn_project/eps_model/")
R = json.load(open(E + "v8_results.json"))
HIST = json.load(open(os.path.join(HERE, "../../bunching/cap_use_hist.json")))
SB = json.load(open(E + "baseline/survey_binding.json"))
BLOB = json.load(open(os.path.join(HERE, "blobs.json")))
P, FIT, T, X = R["params"], R["fit"], R["targets"], R["experiments"]
CH = R["change_vs_current"]
CUR, PRICE, EQ, NONE = X["current rule"], X["price"], X["equal limit"], X["no EPS"]
PRESENTERS = json.load(open(os.path.join(HERE, "presenters.json")))   # {"part name": "presenter"}

PARTS = [("feedback", ["nov24-cover", "nov24-feedback", "nov24-test"]),
         ("model", ["nov24-env", "nov24-tech", "nov24-rules", "nov24-plant", "nov24-eq"]),
         ("calibration", ["nov24-params", "nov24-fit", "nov24-checks", "nov24-who"]),
         ("results", ["nov24-results", "nov24-plans", "nov24-assume", "nov24-next"])]
ORDER = [s for _, ss in PARTS for s in ss]
FIRST = 63
TOTAL = FIRST - 1 + len(ORDER)
PG = {k: FIRST + i for i, k in enumerate(ORDER)}
PRESENTER = {s: PRESENTERS.get(n) for n, ss in PARTS for s in ss}
SERIF, SANS = "'Source Serif 4', Georgia, serif", "'IBM Plex Sans', Arial, sans-serif"
NAVY, INK, BODY, MUTED, RUST, STEEL = "#14213d", "#1f2a3c", "#3d4756", "#5f6876", "#a8432c", "#2f5d8a"
LOGO = "/_blob/921ccfeb3c9f6d9c3ed1cc4a5be8bdd4"
EQS = ["(1) y = s·(h^ρ + λₜ ℓ^ρ)^(α/ρ), ℓ = k + m", "(2) cost of k = w·(1 + ψ(1 + h)^−ξ); of m = w", "(3) Eligible (prob. e): m ≤ q(h + k), h + k &lt; 300",
       "(4) Price: m at w + p, no cap", "(5) Exit if β(1−δ)E[V(s′)] &lt; 0; Σν V = cₑ", "(6) Σμ(h + k) = N, Σμ m = M"]


def pct(x, d=0, sign=False):
    return f"{100 * x:{'+' if sign else ''}.{d}f}%".replace("-", "−")


def num(x, d=0, sign=False):
    return f"{x:{'+' if sign else ''},.{d}f}".replace("-", "−")


def page(id_, dark=False):
    return (f'<p style="position:absolute; right:128px; bottom:40px; width:160px; font-family:{SANS}; font-size:24px; '
            f'text-align:right; color:{"#c9d1de" if dark else "#8a94a6"}">{PG[id_]}/{TOTAL}</p>')


def logo():
    return f'<img src="{LOGO}" alt="Logo" style="position:absolute; right:8px; bottom:952.01px; width:112.01px; height:114.78px">'


def presenter(id_, dark=False):
    if not PRESENTER.get(id_):
        return ""
    return (f'<p style="position:absolute; top:64px; right:128px; width:480px; font-family:{SANS}; font-size:24px; font-weight:600; '
            f'text-align:right; color:{"#c9d1de" if dark else MUTED}">Presenter: {PRESENTER[id_]}</p>')


def foot(text):
    return f'<p style="position:absolute; bottom:40px; left:128px; width:1440px; font-family:{SANS}; font-size:24px; color:{MUTED}">{text}</p>'


def h2(text):
    return f'<h2 style="font-family:{SERIF}; font-size:52px; font-weight:600; line-height:1.15; color:{NAVY}">{text}</h2>'


def h3(text):
    return f'<h3 style="font-family:{SERIF}; font-size:34px; font-weight:600; color:{NAVY}">{text}</h3>'


def eqs(on):
    cells = "".join(f'<p style="font-family:{SERIF}; font-size:24px; font-weight:{600 if i + 1 in on else 400}; line-height:1.4; '
                    f'color:{NAVY if i + 1 in on else "#a3acba"}">{e}</p>' for i, e in enumerate(EQS))
    return (f'<div style="position:absolute; top:880px; left:128px; width:1664px; height:108px; display:grid; '
            f'grid-template-columns:1fr 1fr 1fr; padding:12px 24px; background:#f4f7fb; border-top:2px solid #d8dee8">{cells}</div>')


def table(rows, widths, size=24, hi=()):
    head = "".join(f'<th style="width:{w}%">{c}</th>' for c, w in zip(rows[0], widths))
    out = [f"<tr>{head}</tr>"]
    for i, r in enumerate(rows[1:]):
        bg = ' style="background:#fbefea"' if i in hi else (' style="background:#f4f7fb"' if i % 2 else "")
        out.append(f"<tr{bg}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>")
    return f'<table style="font-family:{SANS}; font-size:{size}px; color:{INK}">{"".join(out)}</table>'


def box(text, flex=None, size=26):
    fx = f"flex:{flex}; " if flex else ""
    return (f'<p style="{fx}padding:20px 28px; font-family:{SANS}; font-size:{size}px; line-height:1.4; color:{INK}; '
            f'background:#e8eef6; border-left:6px solid {STEEL}; border-radius:12px">{text}</p>')


def card(big, small, hi=False):
    st = f"background:#fbefea; border:3px solid {RUST}" if hi else "background:#f4f7fb; border:1px solid #d8dee8"
    return (f'<div style="display:flex; flex-direction:column; gap:8px; padding:24px 28px; {st}; border-radius:12px">'
            f'<p style="font-family:{SERIF}; font-size:60px; font-weight:600; line-height:1.1; color:{RUST if hi else NAVY}">{big}</p>'
            f'<p style="font-family:{SANS}; font-size:25px; line-height:1.3; color:{BODY}">{small}</p></div>')


def cards(items):
    return f'<div style="display:grid; gap:24px; grid-template-columns:{" ".join(["1fr"] * len(items))}">{"".join(items)}</div>'


def row(*parts):
    return f'<div style="display:flex; flex-direction:row; gap:32px">{"".join(parts)}</div>'


def col(html, flex):
    return f'<div style="display:flex; flex-direction:column; gap:20px; flex:{flex}">{html}</div>'


def fig(name, w, h, alt):
    return f'<img src="{BLOB[name]}" alt="{alt}" style="width:{w}px; height:{h}px; object-fit:contain">'


def bullets(items, size=26):
    return f'<ul style="font-family:{SANS}; font-size:{size}px; line-height:1.4; color:{BODY}">{"".join(f"<li>{i}</li>" for i in items)}</ul>'


def eqbox(e, size=30):
    return f'<p style="font-family:{SERIF}; font-size:{size}px; line-height:1.35; color:{NAVY}; padding:16px 24px; background:#f4f7fb; border-radius:12px">{e}</p>'


def notes(blocks):
    text = "<br><br>".join(f"[{a}]<br>{b}" for a, b in blocks)
    assert len(text) <= 4000, len(text)
    return f"<aside>{text}</aside>"


def write(id_, body, blocks, on=(), band=True):
    html = (f'<section id="{id_}" data-transition="fade" style="display:flex; flex-direction:column; gap:26px; padding:128px 128px {220 if band else 150}px; background:#ffffff">\n'
            f'{body}{eqs(on) if band else ""}{presenter(id_)}{page(id_)}{logo()}{notes(blocks)}\n</section>\n')
    open(os.path.join(SL, id_ + ".html"), "w").write(html)


# ------------------------------------------------------------------ numbers
PREM = lambda h: 1 + P["psi"] * (1 + h) ** -P["xi"]
e24, e19 = R["e_2024"], R["e_2019"]
G = CUR["groups"]
H = HIST                                                   # survey cap-use histogram
use_model = R["lpy"]["use_of_cap"]
at_cap_model = R["lpy"]["at_cap"]
use_hist = R["lpy"]["use_hist"]
over_model = use_hist[-1]
chg = lambda n, k="net_Y": CH[n][k]
PL = R["plans"]
CAP24 = [["Korean workers h + k", "1–10", "11–50", "51–100", "101–150", "151–200", "201–299", "300+"],
         ["2024 legal cap q", "n + 10", "min(30, 2n)", "35", "40", "50", "60", "not eligible"]]
CAP19 = [["Korean workers h + k", "1–5", "6–10", "11–30", "31–50", "51–100", "101–150", "151–200", "201–299"],
         ["2019 legal cap q", "5", "7", "10", "12", "15", "20", "25", "30"]]

# ------------------------------------------------------------------ cover
open(os.path.join(SL, "nov24-cover.html"), "w").write(f'''<section id="nov24-cover" data-transition="fade" style="background:{NAVY}">
<h1 style="position:absolute; top:150px; left:128px; width:1664px; font-family:{SERIF}; font-size:88px; font-weight:600; line-height:1.1; color:#f7f5f0">EPS project: the model,<br>written up in full</h1>
<p style="position:absolute; top:376px; left:128px; width:1664px; font-family:{SANS}; font-size:36px; line-height:1.4; color:#c9d1de">November 24, 2026 · Random eligibility, the full legal cap, and what the data say</p>
<h2 style="position:absolute; top:490px; left:128px; width:1664px; font-family:{SERIF}; font-size:52px; color:#f7f5f0"><b>Research Topic: Does tying EPS workers to plant size keep weak plants alive, and how much would output change if the same quota ignored plant size?</b></h2>
<p style="position:absolute; bottom:96px; left:128px; width:1664px; font-family:{SANS}; font-size:26px; line-height:1.5; color:#c9d1de">Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo<br>ISA6327 Topics in Macroeconomics · Prof. Sewon Hur · November 24, 2026</p>
{presenter("nov24-cover", True)}{page("nov24-cover", True)}{logo()}{notes([("Title", '"Good afternoon. Last week you asked us to test our 21 percent rule against the data, and to send you a complete write-up of the model. Today we do both."'),
 ("Plan", '"First the test and what it told us. Then the full model, one slide per part. Then the calibration, the checks, and one main result."')])}
</section>
''')

# ------------------------------------------------------------------ feedback
rows = [["Your comment (Nov 17)", "What we did", "Slide"],
        ["Justify the 21% rule with a histogram of cap use", f"Done with the survey. Firms are spread from 10% to over 100%, median {pct(H['median'])}: the rule is not supported, so we dropped it", f"{PG['nov24-test']}"],
        ["Randomly assign which firms are EPS-eligible; eligible firms hire up to their legal cap", f"Done. A share e of new plants is eligible; e adjusts so the quota is used ({pct(e24)} of entrants)", f"{PG['nov24-rules']}"],
        ["The legal cap and eligibility count all Korean workers", "Done: cap q(h + k) and h + k &lt; 300, as in the law", f"{PG['nov24-rules']}"],
        ["The 2024 “would go past the cap” line is too much of a stretch", "Dropped", "—"],
        ["The comparison with a 50% larger quota is not informative", "Dropped. We report the change in output only", f"{PG['nov24-results']}"],
        ["Perfect substitutes: corner solutions", "Kept, to change one thing at a time. With the full cap the model still matches cap use (next slides)", f"{PG['nov24-assume']}"],
        ["Send a complete write-up of the model", "Slides 66–70, and the targets and sources", f"{PG['nov24-env']}–{PG['nov24-fit']}"]]
write("nov24-feedback", f"""{h2("Your feedback last week, and what we changed")}
{table(rows, [36, 54, 10], 22)}
{foot("All results today come from the new model (v8), recalibrated to sourced targets.")}""",
      [("Title", '"Here is each comment from last week and what we did. The main change: the 21 percent rule is gone. Instead, plants are randomly eligible for EPS, and eligible plants can hire up to their full legal cap, counted on all Korean workers as in the law."'),
       ("Perfect substitutes", '"We kept perfect substitutes for now, so that we change one thing at a time. With the full cap, the model already matches how much of their cap firms use. We come back to it at the end."')], band=False)

# ------------------------------------------------------------------ the test
write("nov24-test", f"""{h2("The test you asked for: how much of its legal cap does each EPS firm use?")}
{fig("fig_capuse.png", 1664, 582, "Share of the 2019 legal cap used by EPS firms, survey against the new model")}
{row(box(f"<b>Survey:</b> median {pct(H['median'])} of the cap, {pct(H['at_or_below_theta_0_21'])} at or below 21%, {pct(H['at_or_above_cap'])} at or above the cap. The 21% rule does not fit, so we dropped it.", 1, 24),
     box(f"<b>New model:</b> eligible plants may use their full cap. They use {pct(use_model)} of it on average (survey {pct(H['mean'])}, our target); {pct(at_cap_model)} are at the cap (survey {pct(H['at_or_above_cap'])}).", 1, 24))}
{foot("772 survey firms, 2019 caps from listed Korean workers (Lee, Peri and Yang, Table 4). Spikes at 20, 40, 60, 80%: firms with a cap of 5.")}""",
      [("Title", '"You asked for a histogram: among firms with at least one EPS worker, the share of their legal cap they use. Orange is the survey, 772 firms in 2019."'),
       ("Survey", f'"Firms are spread out. The median firm uses {pct(H["median"])} of its cap. Only {pct(H["at_or_below_theta_0_21"])} are at or below 21 percent, and {pct(H["at_or_above_cap"])} are at or above the cap. So the data do not support our old rule, which put every plant at 21 percent. The dashed line shows where it was."'),
       ("Model", f'"Blue is the new model. Eligible plants may use their whole cap. Small plants whose manual work is below their cap use less, so the model spreads out too: {pct(use_model)} on average and {pct(at_cap_model)} at the cap. The average is a target; the shape is not."'),
       ("If asked: the spikes", '"Many survey firms have a cap of 5. One, two, three or four workers is 20, 40, 60 or 80 percent."'),
       ("If asked: over 100 percent", f'"{pct(H["bins"]["above 100%"])} of survey firms are above their cap. The model cannot produce that. They may have been counted on a different date, or have extra permits; we asked the Ministry."')],
      band=False)

# ------------------------------------------------------------------ model 1: environment
write("nov24-env", f"""{h2("The model (1/5): plants, timing and what is fixed")}
{row(col(h3("Plants") + bullets([
    "Hopenhayn (1992): many plants, one good, discrete years, a stationary equilibrium",
    f"At entry a plant draws, once and for all: its <b>type</b> (light, or manual-intensive with probability {P['shB']:.2f}), a permanent productivity x from a Pareto tail (γ = {P['gamma']:.2f}), and whether it is <b>EPS-eligible</b> (probability e)",
    f"Productivity s = x·z; z follows an AR(1) in logs (persistence 0.90, s.d. {P['sigma_s']:.3f})"], 25), 1),
     col(h3("Each year") + bullets([
    "1. Plants hire and produce, given s",
    f"2. Each plant exits with probability δ = {P['delta']:.3f}, or chooses to close if staying is not worth it",
    f"3. New plants enter until entering is worth its cost c<sub>e</sub> = {P['ce']:.1f}"], 25)
    + h3("Fixed in the economy") + bullets([
    "Korean workers N = 1 (all hired at the wage w)",
    "The EPS quota M: 5.29% of manufacturing workers"], 25), 1))}
{foot("Stationary equilibrium: we compare steady states, not transitions. Light plants stand for the rest of manufacturing.")}""",
      [("Plants", '"This is a Hopenhayn model. When a plant enters it draws three things that never change: its type, light or manual-intensive; a permanent productivity level from a Pareto tail; and whether it is eligible for EPS. On top, productivity moves each year with a small shock."'),
       ("Timing", '"Each year plants hire and produce. Then some exit by chance, and others close if the future is not worth it. New plants enter until entry is worth its cost; that pins down the wage."'),
       ("Fixed", '"Korean labour and the EPS quota are fixed. We compare steady states."'),
       ("If asked: one sector?", '"Light plants put almost no weight on manual work and never use EPS, so they act as the rest of the economy. The EPS question is about the manual-intensive plants."')],
      on=(5, 6))

# ------------------------------------------------------------------ model 2: technology and costs
prem_rows = [["Core Koreans h", "0", "7", "28", "150"], ["Cost of a Korean manual worker ÷ w"] + [f"{PREM(h):.2f}" for h in (0, 7, 28, 150)]]
write("nov24-tech", f"""{h2("The model (2/5): output and labour costs")}
{row(col(eqbox("(1) y = s·(h<sup>ρ</sup> + λ<sub>t</sub> ℓ<sup>ρ</sup>)<sup>α/ρ</sup>, &nbsp;ℓ = k + m") + bullets([
    "h: core Korean workers. ℓ: manual work, done by Korean manual workers k or EPS workers m, one for one",
    f"λ<sub>t</sub>: weight on manual work, {P['lamA']:.3f} (light) and {P['lamB']:.2f} (manual-intensive). ρ = {P['rho']:.2f}",
    "α = 0.69 &lt; 1: each extra worker adds a little less"], 25), 1),
     col(eqbox("(2) cost of k = w·(1 + ψ(1 + h)<sup>−ξ</sup>); &nbsp;cost of m = w") + bullets([
    f"Korean manual workers are hard to find at small plants, so they cost more than w (ψ = {P['psi']:.2f}, ξ = {P['xi']:.2f})",
    f"An EPS worker costs w; using any costs a fixed c<sub>m</sub> = {P['cm']:.2f} a year",
    f"Every plant pays a fixed cost to operate: {P['cfA']:.2f} (light), {P['cfB']:.2f} (manual-intensive)"], 25)
    + table(prem_rows, [40, 15, 15, 15, 15], 24), 1))}
{foot("Net output = output − the Korean premium paid − EPS and operating fixed costs − entry costs. All costs in units of the good.")}""",
      [("Equation 1", '"A plant combines core Korean workers with manual work. Manual work can be done by a Korean manual worker or an EPS worker, one for one. Manual-intensive plants put much more weight on manual work."'),
       ("Equation 2", f'"Korean manual workers cost more than the wage, most of all at small plants: {PREM(0):.2f} times the wage with no core Koreans, {PREM(150):.2f} at 150. An EPS worker costs the wage, plus a fixed cost of using EPS at all."'),
       ("Footer", '"We measure welfare as net output: output minus the premium, the fixed costs and entry costs."')],
      on=(1, 2))

# ------------------------------------------------------------------ model 3: EPS rules
write("nov24-rules", f"""{h2("The model (3/5): today's EPS rules")}
{eqbox("(3) If eligible: &nbsp;m ≤ q(h + k), &nbsp;only if h ≥ 1 and h + k &lt; 300. &nbsp;If not eligible: m = 0", 30)}
{table(CAP24, [22, 11, 13, 11, 11, 11, 11, 10], 22)}
{table(CAP19, [22, 9, 9, 10, 10, 10, 10, 10, 10], 22)}
{row(box(f"<b>Who is eligible:</b> a share e of new plants, by chance, regardless of type or productivity. It stands for the points ranking and waiting lists: demand exceeds the quota, and which firm gets workers is partly luck.", 1, 24),
     box(f"<b>The quota sets e:</b> e adjusts so total EPS use equals M. Under the 2024 caps e = {pct(e24)}; under the 2019 caps e = {pct(e19)}. Eligible plants keep the saving (no fee).", 1, 24))}
{foot("Caps: eps.go.kr (2024, manufacturing) and Lee, Peri and Yang (2026), Table 4 (2019). The law counts insured Korean workers, h + k.")}""",
      [("Equation", '"Today\'s rule in the model: an eligible plant may hire EPS workers up to its legal cap, which depends on all its Korean workers, core and manual, as in the law. Plants with 300 or more Korean workers are not eligible. A plant that is not eligible hires none."'),
       ("Tables", '"These are the two cap schedules. We use 2024 for today\'s economy and 2019 for the survey and the 2020 shock, because those firms faced the 2019 caps."'),
       ("Boxes", f'"Who is eligible is random: a share e of new plants. That stands in for the points system and waiting lists. e is not a parameter; it adjusts so the quota is used, like the 21 percent did before. It comes out at {pct(e24)} of new plants."'),
       ("If asked: why random", '"Your suggestion, and the data: firms far below their cap still want more, so access, not the cap, limits most of them. A random draw is the simplest way to ration access."')],
      on=(3,), band=False)

# ------------------------------------------------------------------ model 4: the plant's problem
write("nov24-plant", f"""{h2("The model (4/5): the plant's problem")}
{eqbox("π<sub>t,e</sub>(s) = max<sub>h, ℓ, m</sub> &nbsp;s·f<sub>t</sub>(h, ℓ) − w·h − w(1 + ψ(1 + h)<sup>−ξ</sup>)·(ℓ − m) − w·m − c<sub>m</sub>·1[m &gt; 0] − c<sub>f,t</sub> &nbsp;&nbsp;subject to (3)", 28)}
{eqbox("V<sub>t,e</sub>(s) = π<sub>t,e</sub>(s) + σ<sub>ε</sub>·log(1 + exp(β(1 − δ)·E[V<sub>t,e</sub>(s′) | s] / σ<sub>ε</sub>))", 28)}
{eqbox("Free entry: &nbsp;Σ<sub>t</sub> Pr(t)·[ e·∫V<sub>t,1</sub> dν + (1 − e)·∫V<sub>t,0</sub> dν ] = c<sub>e</sub>", 28)}
{bullets([
    "Static: each year the plant picks core workers, manual work and how much of it EPS workers do. Since an EPS worker costs less, an eligible plant that uses EPS fills its manual work with them up to the cap",
    "Dynamic: staying is worth the expected future value; a taste shock (σ<sub>ε</sub> = 0.1) smooths the exit choice. Exit probability: 1 − (1 − δ)·Pr(stay)",
    "Entry: new plants draw (t, x, z, eligibility) from ν and enter until the expected value equals c<sub>e</sub>"], 24)}
{foot("β = 0.96. ν: entrants' draws (type, Pareto x, z from its stationary distribution, eligibility).")}""",
      [("Static", '"Each year the plant chooses core workers, manual work, and how much of the manual work EPS workers do. An EPS worker is cheaper than a Korean manual worker, so an eligible plant that uses EPS uses as many as its cap allows, unless its manual work is smaller than the cap."'),
       ("Dynamic", '"The value of a plant is today\'s profit plus the option to stay. The taste shock just makes exit smooth."'),
       ("Entry", '"New plants enter until the expected value of entering equals the entry cost. The expectation is over type, productivity and eligibility."')],
      on=(5,), band=False)

# ------------------------------------------------------------------ model 5: equilibrium and experiments
rows = [["", "Today (baseline)", "Price (experiment)", "Equal limit (check)"],
        ["Who may hire EPS", "Eligible plants (share e)", "Every plant with h ≥ 1", "The same eligible plants"],
        ["How many", "Up to q(h + k)", "Any number", "Up to L, the same for all"],
        ["Cost of an EPS worker", "w", "w + p", "w"],
        ["What clears the quota", "e", "p", "L"]]
write("nov24-eq", f"""{h2("The model (5/5): equilibrium, and the two experiments")}
{eqbox("Equilibrium: w, the quota variable (e, p or L), entry M<sub>e</sub> and the distribution μ such that plants optimize, free entry holds, Σμ(h + k) = N and Σμ m = M", 27)}
{table(rows, [25, 25, 25, 25], 24)}
{box("<b>Question:</b> with the same quota, does output rise if EPS workers go to the plants that value them most (a price), instead of to plants that are lucky and small enough (today)? The equal limit keeps who is eligible and only removes the link to size.", size=25)}
{foot("Permit revenue p·M goes back to households, so it is not lost. We hold N and M fixed and compare steady states.")}""",
      [("Equilibrium", '"An equilibrium is a wage, the variable that clears the quota, an entry mass and a distribution of plants, such that plants optimize, entry is free, and both Korean labour and the quota are fully used."'),
       ("Table", '"Today, eligible plants hire up to their cap, and the eligible share clears the quota. In the price experiment any plant can buy permits at a price p that clears the same quota. In the equal-limit check, the same lucky plants are eligible, but each gets the same limit L, so only the link to size is removed."'),
       ("Box", '"So the question is: with the same quota, does output rise if workers go to the plants that value them most?"')],
      on=(4, 6), band=False)

# ------------------------------------------------------------------ calibration: parameters
prow = lambda name, sym, v, d, how: [name, sym, f"{v:.{d}f}", how]
rows = [["Parameter", "Symbol", "Value", "Pinned down mainly by"],
        prow("Returns to scale", "α", 0.6916, 2, "Set (earlier Hopenhayn calibration)"),
        prow("Productivity persistence", "ρ<sub>s</sub>", 0.8975, 2, "Set"),
        prow("Discount factor; exit taste shock", "β; σ<sub>ε</sub>", 0.96, 2, "Set; σ<sub>ε</sub> = 0.1 (smoothing)"),
        prow("Productivity shock s.d.; Pareto tail", "σ<sub>s</sub>; γ", P["sigma_s"], 3, f"Exit rate; plants with 50+ workers (γ = {P['gamma']:.2f})"),
        prow("Exogenous exit; entry cost", "δ; c<sub>e</sub>", P["delta"], 3, f"Exit rate; average size (c<sub>e</sub> = {P['ce']:.1f})"),
        prow("Manual-intensive share of entrants", "Pr(B)", P["shB"], 2, "Plants using EPS"),
        prow("Weight on manual work, B; A", "λ<sub>B</sub>; λ<sub>A</sub>", P["lamB"], 2, f"EPS share and size of EPS firms (λ<sub>A</sub> = {P['lamA']:.3f})"),
        prow("Fixed operating cost, B; A", "c<sub>f,B</sub>; c<sub>f,A</sub>", P["cfB"], 2, f"Size of EPS firms; plants with 1–4 workers (c<sub>f,A</sub> = {P['cfA']:.2f})"),
        prow("Korean manual premium; its decline", "ψ; ξ", P["psi"], 2, f"Cap use; EPS share by size (ξ = {P['xi']:.2f})"),
        prow("Fixed cost of using EPS", "c<sub>m</sub>", P["cm"], 2, "Plants using EPS"),
        prow("Curvature between core and manual", "ρ", P["rho"], 2, "Size of EPS firms")]
write("nov24-params", f"""{h2("Calibration: 4 parameters set, 13 chosen to fit 8 targets")}
{table(rows, [34, 16, 10, 40], 22)}
{foot("“Pinned down mainly by” is a guide: all 13 move together to minimize the sum of squared % gaps to the targets (next slide).")}""",
      [("Title", '"Four parameters are set from earlier work. Thirteen are chosen together so the model fits eight targets as closely as possible."'),
       ("How to read", '"The last column says which target mostly moves each parameter. For example, the manual-intensive share of entrants mostly sets how many plants use EPS."'),
       ("If asked: 13 for 8", '"It is not exactly identified one by one; we minimize the sum of squared percentage gaps."')], band=False)

# ------------------------------------------------------------------ calibration: fit
lab = dict(avg_size=("Average plant size (workers)", "MDIS census 2024, all 509,467 plants", 2),
           share_small=("Plants with 1–4 workers", "MDIS census 2024", "p"),
           share_50plus=("Plants with 50+ workers", "MDIS census 2024", "p"),
           exit_rate=("Exit rate", "Statistics Korea, business demography 2024", "p"),
           users=("Plants that use EPS", "Ministry (e-나라지표), 40,766 workplaces, 2024", "p"),
           eps_share_users=("EPS share at EPS firms (average)", "Lee, Peri and Yang, Table 3", "p"),
           users_size=("Workers at EPS firms (average)", "Lee, Peri and Yang, Table 3", 1),
           use_of_cap=("Share of the 2019 cap used (average)", "KDI–World Bank survey 2019 (new)", "p"))
fmt = lambda v, d: pct(v, 1) if d == "p" else f"{v:.{d}f}"
rows = [["Target", "Data", "Model", "Source"]] + [[lab[k][0], fmt(T[k], lab[k][2]), fmt(FIT[k], lab[k][2]), lab[k][1]] for k in lab]
rows.append(["Quota M: EPS ÷ manufacturing workers", "5.29%", "5.29%", "Ministry and census 2024 (holds by construction)"])
slope = R["checks"]["slope_lpy"]
write("nov24-fit", f"""{h2("Calibration: targets, sources and fit")}
{table(rows, [34, 11, 11, 44], 22)}
{box(f"<b>Not targeted any more: the closure slope</b> (Lee, Peri and Yang: 0.152; model {slope:.3f}). Eligible plants keep their permits, so EPS users are rarely close to closing, and a two-year cut barely moves them. It was fragile before too (0.15 to 0.05 on a finer grid).", size=23)}
{foot("Census and survey files stay outside our repository; the scripts that build every number are in it. Sources: TARGETS.md.")}""",
      [("Table", '"These are the eight targets, the data, the model, and the source of each. One is new: the average share of its cap an EPS firm uses, from the survey."'),
       ("Box", f'"One thing we no longer target: how much more often EPS firms close after the 2020 stop. Lee, Peri and Yang find 0.15; our model gives {slope:.2f}. In the new model eligible plants keep their permits, so they are rarely close to closing. This is a gap we state openly."'),
       ("If asked: why did you drop it", '"The best of 256 random parameter draws all gave nearly zero, so keeping it would only pull the other targets off. It was also fragile in the old model."')], band=False)

# ------------------------------------------------------------------ checks: size pattern
write("nov24-checks", f"""{h2("A check we did not target: which EPS firms, and how reliant on EPS")}
{fig("fig_size.png", 1664, 562, "EPS firms by total workers, model against the survey, 2019 caps")}
{foot("Model under the 2019 caps, EPS users only. Survey: 772 firms, total workers = Korean + EPS workers. Targeted: only the averages (36.9% and 20.8 workers).")}""",
      [("Left", '"Where EPS firms are, by total workers: blue is the model, orange the survey."'),
       ("Right", '"The EPS share of workers at those firms, by size. We target only the averages, so the shape is a check."'),
       ("If asked: what fails", '"Read the gaps from the chart: these are untargeted, so we report them as they are."')], band=False)

# ------------------------------------------------------------------ who uses EPS
gname = dict(manual_eligible="Manual-intensive, eligible", manual_not="Manual-intensive, not eligible",
             light_eligible="Light, eligible", light_not="Light, not eligible")
rows = [["Group", "% of plants", "% using EPS", "Workers per plant", "Exit rate"]]
for k in ("manual_eligible", "manual_not", "light_eligible", "light_not"):
    g = G[k]
    rows.append([gname[k], pct(g["plants"], 1), pct(g["user_rate"]), f"{g['size']:.1f}", pct(g["exit"], 1)])
write("nov24-who", f"""{h2("Who uses EPS today, in the new model")}
{table(rows, [34, 16, 16, 18, 16], 26, hi=(0,))}
{box(f"<b>Users are the eligible manual-intensive plants.</b> Light plants put almost no weight on manual work, so EPS is not worth its fixed cost. Manual-intensive plants that are not eligible pay the Korean premium instead. {pct(CUR['users'], 1)} of plants use EPS (data 8.0%).", size=25)}
{foot("2024 caps. Shares of all plants in the stationary distribution; eligibility is drawn at entry.")}""",
      [("Table", '"The highlighted row is who uses EPS: manual-intensive plants that drew eligibility. Light plants never use it. Manual-intensive plants without eligibility do their manual work with Korean workers at a premium."'),
       ("Exit", '"Compare exit rates: eligible manual plants survive more easily, because the permits save them money every year."')], band=False)

# ------------------------------------------------------------------ results
def rrow(name, key):
    d, c = X[key], CH[key]
    return [name, pct(c["net_Y"], 2, True), pct(c["Y"], 2, True), pct(c["firms"], 1, True), pct(c["w"], 2, True), pct(d["users"], 1)]


rows = [["", "Net output", "Gross output", "Plants", "Wage", "Plants using EPS"],
        ["Today (random eligibility + cap)", "0", "0", "0", "0", pct(CUR["users"], 1)],
        rrow("Price: any plant, permit price p", "price"),
        rrow("Equal limit: same eligible plants", "equal limit"),
        rrow("No EPS at all (for scale)", "no EPS")]
write("nov24-results", f"""{h2("Main result: the same quota, allocated by a price")}
{table(rows, [34, 13, 14, 11, 11, 17], 25, hi=(1,))}
{cards([card(pct(chg('price'), 2, True), f"net output with a permit price of {PRICE['x']:.2f} (≈ {pct(PRICE['x'] / PRICE['w'])} of the wage)", True),
        card(pct(chg('equal limit'), 2, True), f"net output if the same eligible plants each get {EQ['x']:.1f} permits"),
        card(pct(-chg('no EPS'), 2, True), "what EPS adds today, against no EPS at all")])}
{foot("Changes against today, 2024 caps, steady states, same quota M and Korean labour N.")}""",
      [("Table", '"Here is the main result. Each row changes how the same quota is allocated, and we compare steady states."'),
       ("Price", f'"With a permit price, any plant can hire EPS workers if it pays p. Net output changes by {pct(chg("price"), 2, True)}."'),
       ("Equal limit", f'"If we keep the same lucky plants but give each the same limit, net output changes by {pct(chg("equal limit"), 2, True)}. That isolates the link to size."'),
       ("Scale", f'"For scale: EPS as a whole adds {pct(-chg("no EPS"), 2, True)} to net output, against no EPS at all."')], on=(3, 4), band=False)

# ------------------------------------------------------------------ plans of the median and top plants
def prow2(name, d, i):
    return [name, f"{d['h'][i]:.0f}", f"{d['k'][i]:.0f}", f"{d['m'][i]:.0f}", f"{d['total'][i]:.0f}"]


rows = [["Eligible manual-intensive plant", "Core Koreans h", "Korean manual k", "EPS m", "All workers"]]
for i, who in ((0, "Median"), (1, "Top 1%")):
    rows += [prow2(f"{who}: today", PL["current"], i), prow2(f"{who}: price", PL["price"], i), prow2(f"{who}: equal limit", PL["equal"], i)]
write("nov24-plans", f"""{h2("Why: what the median and top plants do in each case")}
{table(rows, [34, 16, 18, 14, 18], 25, hi=(0, 3))}
{box(f"Same productivity in every row: the median and the 99th percentile of eligible manual-intensive plants today. A manual-intensive plant that is not eligible has 0 EPS workers today and the same plan as with a price at a high enough p.", size=24)}
{foot("2024 caps. Plans at each case's own wage and price. Numbers rounded to whole workers.")}""",
      [("Table", '"To see why, here are two plants with the same productivity in every row: the median and the top 1 percent of eligible manual-intensive plants."'),
       ("Read", '"Compare their EPS workers across rows: today they are limited by the cap; with a price they choose where an EPS worker is worth the price."')], band=False)

# ------------------------------------------------------------------ assumptions
rows = [["Assumption", "Why we keep it", "What would change"],
        ["Korean and EPS manual workers are perfect substitutes", "One change at a time; with the full cap the model already matches average cap use", "Imperfect substitutes would remove corners in the price experiment"],
        ["Eligibility is random and permanent", "Your suggestion; the simplest way to ration access", "The points ranking may favour some firms; permits last 3 years"],
        ["The quota is fully used", f"e &lt; 1 clears it; waiting lists in 2026", "A 2024 projection put arrivals near half the quota"],
        ["The Korean premium is a real cost", "Search and pay premia for scarce workers", "If it is only a transfer, the net gain falls"],
        ["Closure slope not targeted", f"Model gives {slope:.2f}; the best of 256 random draws gave at most 0.07", "The model may understate how fragile EPS firms are"]]
write("nov24-assume", f"""{h2("What we assume, and what it could change")}
{table(rows, [32, 36, 32], 23)}
{foot("Survey firms above their cap (11%) and below it but wanting more (41%) are not in the model: access is all-or-nothing here.")}""",
      [("Title", '"Here are the assumptions that matter most for the result, why we keep them, and what each could change."'),
       ("First row", '"We kept perfect substitutes, as you suggested, to change one thing at a time. With the full cap, the model already matches how much of their cap firms use."'),
       ("If asked: the 41 percent", '"Survey firms below their cap that still want more are rationed in a way our model does not have: here, access is all or nothing."')], band=False)

# ------------------------------------------------------------------ next
write("nov24-next", f"""{h2("Where we are, and our questions")}
{row(col(h3("Where we are") + bullets([
    "The 21% rule is gone: random eligibility and the full legal cap on all Korean workers",
    f"The model matches average cap use ({pct(use_model)} vs {pct(H['mean'])}) and the other targets",
    f"With the same quota, a price changes net output by {pct(chg('price'), 2, True)}; an equal limit by {pct(chg('equal limit'), 2, True)}",
    "Ministry data expected around Nov 30: firm counts by size and cap use, 2019 and 2024"], 25), 1),
     col(h3("Questions for you") + bullets([
    "Is this model settled enough to write up the results?",
    "Should eligibility depend on anything (size, industry), or stay random?",
    "Should we add imperfect substitutes now, or leave it as a robustness check?",
    "Is the closure slope something we must match?"], 25), 1))}
{foot("The written model (slides 66–70) and targets (slides 71–72) are what we will send you.")}""",
      [("Left", '"To sum up. We dropped the 21 percent rule, after the test you suggested. Plants are now randomly eligible and can hire up to the full legal cap. The model matches cap use and the other targets, and the price result is on the left."'),
       ("Right", '"Four questions. Is the model settled enough? Should eligibility stay random? Should we add imperfect substitutes now? And must we match the closure slope?"'),
       ("Close", '"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."')], band=False)

print("slides", {k: PG[k] for k in ORDER}, "total", TOTAL)
