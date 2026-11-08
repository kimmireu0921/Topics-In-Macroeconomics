"""Writes the team's equation sheet for slide 40 (equation_sheet.html) and prints it to
"Equation sheet.pdf" with headless Chrome. Numbers are read from the v6 results, so the
sheet matches the model that produced the slides.

  /opt/anaconda3/bin/python3 equation_sheet.py
"""
import json
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "../../hopenhayn_project/eps_model/v6_results.json")))
P, FIT, T = R["params"], R["fit"], R["targets"]
CUR, PRICE = R["experiments"]["current rule"], R["experiments"]["size-neutral, same quota (by price)"]
w0, th, wp, pp = CUR["w"], CUR["x"], PRICE["w"], PRICE["x"]
psi, xi = P["psi"], P["xi"]
prem = lambda h: psi * (1 + h) ** -xi
h_cross = (pp / (wp * psi)) ** (-1 / xi) - 1
light, manual = CUR["type_share"]


def v(sym, g, sub=""):
    """A symbol chip in its group's colour."""
    s = f"<sub>{sub}</sub>" if sub else ""
    return f'<span class="v {g}">{sym}{s}</span>'


y, s, x, z = v("y", "out"), v("s", "out"), v("x", "out"), v("z", "out")
h = v("h", "core")
k, ps, xi_ = v("k", "kor"), v("ψ", "kor"), v("ξ", "kor")
m, tht, q = v("m", "eps"), v("θ", "eps"), v("q", "eps")
ell = v("ℓ", "man")
W = v("w", "wage")
p = v("p", "price")
lam = v("λ", "lam", "t")
rho, al = v("ρ", "shape"), v("α", "shape")
be, de, V, nu, mu = (v(c, "dyn") for c in ("β", "δ", "V", "ν", "μ"))
cm, cf, ce = v("c", "fix", "m"), v("c", "fix", "f,t"), v("c", "fix", "e")
N, M = v("N", "core"), v("M", "eps")
pct = lambda a, d=0: f"{100 * a:.{d}f}%"


def symbols(rows):
    return '<table class="sym">' + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows) + "</table>"


def say(t):
    return f'<div class="say"><b>Say it:</b> “{t}”</div>'


def card(n, title, body, cls=""):
    badge = f'<span class="n">{n}</span>' if n else ""
    return f'<section class="card {cls}"><h2>{badge}{title}</h2>{body}</section>'


# ---- the permit chart (price experiment): value of a permit vs its price -----------
X = lambda hh: 50 + hh / 150 * 420
Y = lambda val: 180 - val / 0.8 * 165
hs = np.concatenate([np.linspace(0, 10, 21), np.linspace(11, 150, 60)])
path = "M" + " L".join(f"{X(a):.1f},{Y(wp * prem(a)):.1f}" for a in hs)
grid = "".join(f'<line x1="50" x2="470" y1="{Y(t):.1f}" y2="{Y(t):.1f}" class="gl"/>'
               f'<text x="44" y="{Y(t) + 4:.1f}" class="tk" text-anchor="end">{t:.1f}</text>' for t in (0, .2, .4, .6))
ticks = "".join(f'<text x="{X(t):.1f}" y="196" class="tk" text-anchor="middle">{t}</text>' for t in (0, 50, 100, 150))
chart = f"""<svg viewBox="0 0 480 222" class="chart" role="img" aria-label="Value of a permit falls with core Korean workers and crosses the permit price at about {h_cross:.0f}">
{grid}{ticks}
<line x1="50" x2="470" y1="{Y(pp):.1f}" y2="{Y(pp):.1f}" class="pl"/>
<path d="{path}" class="cv"/>
<line x1="{X(h_cross):.1f}" x2="{X(h_cross):.1f}" y1="{Y(pp):.1f}" y2="180" class="dl"/>
<circle cx="{X(h_cross):.1f}" cy="{Y(pp):.1f}" r="4.5" class="dot"/>
<text x="64" y="{Y(prem(3) * wp) - 6:.1f}" class="lb">Saving from one permit = w × premium</text>
<text x="466" y="{Y(pp) - 7:.1f}" class="lb" text-anchor="end">Permit price p = {pp:.2f}</text>
<text x="{X(h_cross) + 6:.1f}" y="174" class="lb">h ≈ {h_cross:.0f}</text>
<text x="260" y="214" class="tk" text-anchor="middle">core Korean workers h</text>
</svg>"""

cap_rows = [("1–10", "h + 10"), ("11–50", "min(30, 2h)"), ("51–100", "35"), ("101–150", "40"),
            ("151–200", "50"), ("201–299", "60"), ("300 or more", "not eligible")]
cap_tbl = ('<table class="grid"><tr><th>Core Koreans h</th><th>Cap q(h), 2024</th></tr>'
           + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in cap_rows) + "</table>")

prem_tbl = ('<table class="grid"><tr><th>h</th>' + "".join(f"<td>{a}</td>" for a in (0, 7, 28, 150)) + "</tr>"
            "<tr><th>Cost of k ÷ w</th>" + "".join(f"<td>{1 + prem(a):.2f}</td>" for a in (0, 7, 28, 150)) + "</tr></table>")

# ---- sections ------------------------------------------------------------------------
key = [((y, s), "Output and plant productivity"), ((h,), "Core Korean workers"),
       ((k, ps, xi_), "Korean manual workers and their premium"), ((m, tht, q), "EPS workers and the rule that limits them"),
       ((ell,), "Manual work in total: ℓ = k + m, any mix"), ((W,), "Wage of a Korean worker"),
       ((p,), "Permit price (no-size-rule experiment)"), ((v("λ", "lam"),), "Weight on manual work, by plant type"),
       ((rho, al), "Shape of the production function"), ((be, de, V, nu, mu), "Entry, exit and counting plants"),
       ((v("c", "fix"),), "Fixed costs: of running a plant, using EPS, entering")]
key_html = '<div class="key">' + "".join(f'<div><div class="chips">{"".join(a)}</div><div>{b}</div></div>' for a, b in key) + "</div>"

big = card("", "The model in one paragraph", f"""<p>The economy has many manufacturing plants. Each plant has a productivity {s}
and a type: <b>light</b> (manual work barely matters) or <b>manual-intensive</b> (casting, plastics, textiles).
Every year a plant hires workers to make as much profit as it can (equations 1–4), then decides whether to stay
or close (5). New plants enter until entering is no longer worth it (5). Two national totals are fixed: Korean
workers {N} and the EPS quota {M} (6). We solve for the long run, where all of this is steady, once under
today's rule (3) and once with a permit price (4), and compare output.</p>""", "lead")

c1 = card(1, "Production: what a plant makes", f"""
<div class="eq">{y} = {s} · ( {h}<sup>{rho}</sup> + {lam} {ell}<sup>{rho}</sup> )<sup>{al}/{rho}</sup>
<span class="where">where</span> {ell} = {k} + {m}</div>
{say("A plant's output is its productivity times a mix of core Korean workers and manual work. Manual work matters much more for some plants, and it can be done by a Korean worker or an EPS worker.")}
<h3>How it builds up</h3>
<div class="steps">
<div><b>Step 1 · Productivity</b><div class="mini">{s} = {x} · {z}</div>
<p>{x} is drawn when the plant is born and never changes: most plants get a low {x}, a few get a very high one
(a Pareto draw). {z} changes from year to year, but slowly.</p></div>
<div><b>Step 2 · Two kinds of work</b><div class="mini">{h}<sup>{rho}</sup> + {lam} {ell}<sup>{rho}</sup></div>
<p>Core work {h} is done only by Koreans. Manual work {ell} gets weight {lam}: {P['lamA']:.3f} for light plants,
{P['lamB']:.2f} for manual-intensive plants.</p></div>
<div><b>Step 3 · Who does manual work</b><div class="mini">{ell} = {k} + {m}</div>
<p>A Korean manual worker {k} or an EPS worker {m}. They are <b>perfect substitutes</b>: one EPS worker does exactly
the work of one Korean manual worker, no more.</p></div>
<div><b>Step 4 · Shape</b><div class="mini">( … )<sup>{al}/{rho}</sup></div>
<p>{rho} = {P['rho']:.3f}: core and manual work are fairly easy to swap. {al} = 0.69 is below 1, so each extra
worker adds a bit less (decreasing returns). That is what stops a plant from growing forever.</p></div>
</div>
<p class="later"><b>Where it shows up later.</b> With λ this small, light plants hire almost no manual workers, so
EPS has nothing to save them and no light plant uses it (slide 42). {pct(light, 0)} of plants are light because
{pct(1 - P['shB'], 0)} of new plants are light and manual-intensive plants close more often (their fixed cost is
higher). Perfect substitutes are why, at a large plant, an extra permit replaces a Korean worker instead of making
the plant bigger (slides 49 and 51).</p>""", "wide")

c2 = card(2, "Cost of a Korean manual worker", f"""
<div class="eq">cost of {k} = {W} · ( 1 + {ps} (1 + {h})<sup>−{xi_}</sup> )</div>
{say("A Korean manual worker costs the wage plus a premium. The premium is large at small plants, which struggle to find Koreans for manual jobs, and shrinks slowly as the plant grows.")}
{symbols([(W, "Wage of a Korean worker. Core workers cost exactly w."),
          (ps, f"Premium at a plant with no core Koreans: {psi:.3f}, so a manual Korean costs about 1.9 times the wage there"),
          (xi_, f"How fast the premium shrinks as h grows: {xi:.3f}, which is slow"),
          (h, "Core Korean workers at the plant")])}
{prem_tbl}
<p class="note">In the model the premium is a real cost (time and money spent finding and keeping workers), not extra
pay. Whether it should count that way is an open question in the project log.</p>""")

c3 = card(3, "Current rule: EPS limited by size", f"""
<div class="eq"><span class="nw">{m} ≤ {tht} · {q}({h}),</span> <span class="nw sm2">for 1 ≤ {h} &lt; 300</span><br><span class="nw">cost of {m} = {W}</span></div>
{say("Under today's rule a plant can hire EPS workers up to a share theta of its legal cap, and the cap depends on its Korean workers. An EPS worker costs just the wage, so each one saves the premium.")}
{symbols([(m, "EPS workers the plant hires"),
          (v("q(h)", "eps"), "Legal cap, from the 2024 table below"),
          (tht, f"The share of the cap every plant can actually get, {th:.2f}. It is the same for every plant and adjusts until total EPS use equals the quota M"),
          (W, "An EPS worker costs the wage, with no premium. Using EPS at all also costs a fixed c<sub>m</sub>")])}
{cap_tbl}
<p class="note"><b>h, not h + k.</b> The law counts all insured Korean workers, h + k. The model counts only core
Koreans h, a simplification: hiring Korean manual workers does not raise a plant's cap. Example: a plant with
h = 20 has cap 30 and may hire up to {th:.2f} × 30 ≈ {th * 30:.1f} EPS workers.</p>
<div class="hl"><b>Why plants want EPS: compare equations 2 and 3</b>
<div class="eq sm"><span class="nw">saving per EPS worker = {W} × {ps}(1 + {h})<sup>−{xi_}</sup></span></div>
<p>That is the premium from equation 2. A plant uses EPS if the saving on all its EPS workers is larger than the
fixed cost {cm} (slide 42).</p></div>""")

c4 = card(4, "No-size-rule experiment: a price instead", f"""
<div class="c4in"><div>
<div class="eq"><span class="nw">cost of {m} = {W} + {p},</span> <span class="nw sm2">no cap, any plant with {h} ≥ 1</span></div>
{say("In the experiment the size cap disappears. Every plant pays the same permit price p, and p moves until the same quota is used up.")}
{symbols([(p, f"Price of one permit, the same for every plant: {pp:.2f}, about {pp / wp:.0%} of the wage. The money goes to whoever sells the permits, not to the plant")])}
{chart}</div><div>
<p class="note">Saving per permit is now w × premium − p. Left of the dot the premium saved is bigger than the price, so
the plant uses EPS (if the total also covers {cm}). Right of it a Korean manual worker is cheaper, so plants with more
than about {h_cross:.0f} core Koreans drop EPS. That is why EPS users get smaller on average, from
{CUR['users_size']:.1f} to {PRICE['users_size']:.1f} workers (slide 49).</p>
<table class="grid cmp"><tr><th></th><th>Current rule (3)</th><th>Experiment (4)</th></tr>
<tr><th>What limits EPS</th><td>A cap that depends on h</td><td>A price, no link to size</td></tr>
<tr><th>Who may use EPS</th><td>1 ≤ h &lt; 300</td><td>h ≥ 1</td></tr>
<tr><th>Cost of an EPS worker</th><td>{W} (plus {cm} once)</td><td>{W} + {p} (plus {cm} once)</td></tr>
<tr><th>What adjusts to fit M</th><td>{tht} = {th:.2f}</td><td>{p} = {pp:.2f}</td></tr>
<tr><th>Money for permits</th><td>None: permits are free</td><td>p per permit, paid to the permit seller</td></tr></table>
<p class="note"><b>Careful:</b> the experiment changes two things at once: it removes the size link and it charges for
permits. Slide 50 separates them.</p></div></div>""", "wide")

c5 = card("★", "Profit: equations 1–4 together", f"""
<div class="eq">π = {y} − {W}·{h} − (cost of {k})·{k} − (cost of {m})·{m} − {cm}·1[{m} &gt; 0] − {cf}</div>
{say("Profit is output minus what the plant pays: core Koreans, Korean manual workers with their premium, EPS workers, a fixed cost if it uses EPS at all, and a fixed cost of running the plant.")}
{symbols([(v("c", "fix", "m"), f"Fixed cost of using any EPS workers: {P['cm']:.3f} (recruiting, paperwork)"),
          (cf, f"Fixed cost of running the plant each year: {P['cfA']:.2f} light, {P['cfB']:.2f} manual-intensive"),
          ("1[m &gt; 0]", "Equals 1 if the plant uses EPS, 0 if not")])}
<p class="note">Each year the plant picks h, k and m to make π as large as possible, given w and the rule (3) or the
price (4). This is the “policy function” slides 44–45 show.</p>""", "wide")

c6 = card(5, "Plants exit and enter", f"""
<div class="eq"><span class="nw">{V}({s}) = π({s}) + max{{ 0, {be}(1 − {de}) E[{V}({s}′)] }}</span><br><span class="nw">Exit if {be}(1 − {de}) E[{V}({s}′)] &lt; 0</span><br><span class="nw">Entry: Σ {nu} {V} = {ce}</span></div>
{say("A plant's value is this year's profit plus the better of closing, worth zero, or staying. A plant closes when its future is not worth it. New plants keep entering until the value of entering equals the entry cost, and that pins down the wage.")}
{symbols([(V, "Value of a plant. E[…] is its expected value next year, given today's s"),
          (v("s′", "out"), "Next year's productivity"),
          (be, "Discount factor, 0.96: how much next year counts"),
          (de, f"Chance a plant is closed by an outside shock anyway: {P['delta']:.3f} a year"),
          (nu, f"Where new plants start: x from a Pareto draw with tail {P['gamma']:.2f}, z from its usual range. {pct(P['shB'], 1)} of new plants are manual-intensive"),
          (ce, f"Cost of entering, {P['ce']:.1f}. The entrant pays it before it knows its type or productivity")])}
<p class="note"><b>Why entry sets w.</b> If w were lower, plants would earn more, entering would be worth more than
{ce}, and more plants would come in. Only one wage makes entering exactly worth {ce}: {w0:.3f} under today's rule,
{wp:.3f} in the experiment. In the code a small random shock also enters the close-or-stay choice, so closing is a
probability that rises smoothly as the value falls; this only smooths the decision.</p>""")

c7 = card(6, "Markets clear: the totals are fixed", f"""
<div class="eq"><span class="nw">Σ {mu} ({h} + {k}) = {N}</span><br><span class="nw">Σ {mu} {m} = {M}</span></div>
{say("Add up every plant. All the Korean workers they use equal the fixed supply N, and all the EPS workers they use equal the quota M.")}
{symbols([(mu, "How many plants there are of each type and productivity. Size follows from productivity. Σ adds over all of them"),
          (N, "Korean workers, core plus manual, set to 1"),
          (M, "EPS quota, set so EPS workers are 5.5% of all workers: M ≈ 0.058 (source of 5.5% being checked)")])}
<p class="note">The wage is already fixed by entry (5), so Korean labor is matched to {N} by the <b>number of new
plants</b>: more entrants, more plants, more Koreans hired. The quota is matched to {M} by {tht} (today) or {p}
(experiment).</p>""")

c8 = card("★", "How the six fit together", f"""<ol class="flow">
<li><b>Guess</b> {tht} (or {p}).</li>
<li><b>Each plant</b> picks h, k, m to maximize profit (1–4) and decides to stay or close (5).</li>
<li><b>Wage.</b> Find the w at which entering is worth exactly {ce} (5).</li>
<li><b>Number of plants.</b> Scale entry until Korean workers add up to {N} (6).</li>
<li><b>Quota.</b> If plants use more EPS workers than {M}, lower {tht} (or raise {p}); if fewer, the other way. Repeat from 2.</li>
<li><b>Compare</b> plant sizes and output under today's rule and under the permit price.</li></ol>""", "dark")

params = [("Set by us", [("α", "0.69", "returns to scale"), ("β", "0.96", "discount factor"),
                         ("persistence of z", "0.90", "how slowly z changes"), ("N, M", "1, 0.058", "labor and quota")]),
          ("Calibrated (13 numbers to fit 8 targets)",
           [("ρ", f"{P['rho']:.3f}", "core vs manual"), ("λ light, manual", f"{P['lamA']:.3f}, {P['lamB']:.2f}", "weight on manual work"),
            ("c<sub>f</sub> light, manual", f"{P['cfA']:.2f}, {P['cfB']:.2f}", "fixed cost of running"),
            ("manual share at entry", f"{P['shB']:.3f}", ""), ("ψ, ξ", f"{psi:.3f}, {xi:.3f}", "Korean premium"),
            ("c<sub>m</sub>", f"{P['cm']:.3f}", "fixed cost of EPS"), ("σ of z", f"{P['sigma_s']:.3f}", "size of z shocks"),
            ("γ", f"{P['gamma']:.2f}", "Pareto tail of x"), ("c<sub>e</sub>", f"{P['ce']:.1f}", "entry cost"),
            ("δ", f"{P['delta']:.3f}", "outside exit shock")]),
          ("Solved in equilibrium", [("w", f"{w0:.3f} / {wp:.3f}", "today / experiment"), ("θ", f"{th:.3f}", "today"),
                                    ("p", f"{pp:.3f}", "experiment")])]
ptab = "".join(f'<tr class="grp"><th colspan="3">{g}</th></tr>' + "".join(f"<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>" for a, b, c in rows)
               for g, rows in params)
tg = [("Average plant size (workers)", "avg_size", lambda a: f"{a:.1f}"), ("Plants under 5 workers", "share_small", pct),
      ("Exit rate", "exit_rate", lambda a: pct(a, 1)), ("Plants using EPS", "users", lambda a: pct(a, 1)),
      ("Average EPS share at EPS plants", "eps_share_users", lambda a: pct(a, 1)),
      ("Average size of EPS plants", "users_size", lambda a: f"{a:.1f}"),
      ("Extra closures per unit of exposure, 2020–21", "slope_lpy", lambda a: f"{a:.3f}"),
      ("Plants with 50+ workers", "share_50plus", lambda a: pct(a, 1))]
ttab = "".join(f"<tr><td>{a}</td><td>{f(T[b])}</td><td>{f(FIT[b])}</td></tr>" for a, b, f in tg)
c9 = card("", "The numbers behind the symbols", f"""<div class="two">
<table class="grid par"><tr><th>Symbol</th><th>Value</th><th>Meaning</th></tr>{ptab}</table>
<table class="grid par"><tr><th>Target</th><th>Data</th><th>Model</th></tr>{ttab}</table></div>
<p class="note">Targets use the 2024 caps, except EPS share, EPS plant size and closures, which use the 2019 caps their
survey firms faced. The 10% and 5.5% targets have no recorded source yet.</p>""", "wide")

c10 = card("", "Easy to mix up", f"""<ul class="mix">
<li><b>{ell} is not half Korean, half EPS.</b> It is any mix: k + m. The plant chooses the split.</li>
<li><b>The cap counts h only</b> in the model; the law counts h + k. The 2024 survey data do not separate core and manual Koreans.</li>
<li><b>{tht} is one number for every plant.</b> It is not a plant's own choice; it is how the quota gets shared.</li>
<li><b>“EPS share” has three meanings:</b> {pct(T['eps_share_users'], 1)} is the average across EPS plants;
5.5% is EPS workers in all workers; about 10% is the share of plants using EPS (slide 43).</li>
<li><b>Light plants never use EPS</b> in the model: they hire almost no manual workers, and they are already at their best size. Manual-intensive plants are the users.</li>
<li><b>The permit chart is the experiment only.</b> Under today's rule there is no price, only the cap.</li></ul>""", "wide")

CSS = """
@page { size: A4; margin: 12mm 11mm; }
:root { --ink:#17233d; --body:#3b4558; --mute:#6b7487; --line:#dfe3ea; --bg:#f4f5f8; }
* { box-sizing: border-box; }
body { margin:0; background:var(--bg); color:var(--body); font: 9.6pt/1.42 "Helvetica Neue", Helvetica, Arial, sans-serif;
  -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.top { font-size:8pt; letter-spacing:.08em; text-transform:uppercase; color:var(--mute); font-weight:600; }
h1 { font: 600 24pt/1.15 "STIX Two Text", Georgia, serif; color:var(--ink); margin:4px 0 6px; }
.intro { margin:0 0 10px; max-width:150mm; }
.row { display:flex; gap:9px; align-items:stretch; margin-bottom:9px; break-inside:avoid; }
.row > .card { flex:1 1 0; margin-bottom:0; }
.card { background:#fff; border:1px solid var(--line); border-radius:9px; padding:10px 12px; break-inside:avoid; margin-bottom:9px; }
.nw { white-space:nowrap; }
.c4in { display:grid; grid-template-columns:1fr 1fr; gap:12px; align-items:start; }
.lead { background:#eef2f9; }
.card h2 { font: 600 13.5pt/1.2 "STIX Two Text", Georgia, serif; color:var(--ink); margin:0 0 7px; display:flex; align-items:center; gap:7px; }
.n { display:inline-grid; place-items:center; width:19px; height:19px; border-radius:50%; background:var(--ink); color:#fff;
  font:600 9pt "Helvetica Neue", sans-serif; flex:none; }
h3 { font-size:9pt; margin:8px 0 4px; color:var(--ink); }
p { margin:4px 0; }
.eq { font: 14pt/1.9 "STIX Two Text", Georgia, serif; color:var(--ink); margin:2px 0 6px; }
.eq.sm, .row .eq.sm { font-size:11pt; }
.row .eq, .c4in .eq { font-size:12.5pt; }
.sm2 { font-size:10pt; font-style:italic; color:var(--mute); margin-left:4px; }
.eq sup { font-size:68%; vertical-align: 0.55em; }
.eq sup .v { padding:0 2px; }
.where { font-style:italic; margin:0 6px 0 14px; font-size:11pt; color:var(--mute); }
.v { display:inline-block; font-family:"STIX Two Text", Georgia, serif; font-style:italic; border:1px solid; border-radius:4px;
  padding:0 3px; line-height:1.25; margin:0 1px; }
.v sub { font-size:65%; font-style:italic; }
.out { background:#eaf1fc; border-color:#9bb8e6; color:#21457e; }
.core { background:#1d2a44; border-color:#1d2a44; color:#fff; }
.kor { background:#fdf0e4; border-color:#eab48a; color:#8a4410; }
.eps { background:#e4f6f3; border-color:#7cc8bb; color:#0f5e52; }
.man { background:#fbf4dc; border-color:#d9bf6a; color:#6b5410; }
.wage { background:#e9f6e6; border-color:#94c98a; color:#2a6020; }
.price { background:#fceaf1; border-color:#e59bb8; color:#8a1f4a; }
.lam { background:#f1ebfb; border-color:#b49ae0; color:#4f2e8c; }
.shape { background:#f6f7f9; border:1px dashed #9aa3b3; color:#4a5468; }
.dyn { background:#fff7d6; border-color:#e0c560; color:#6d5600; }
.fix { background:#eef0f3; border-color:#a9b1bf; color:#3b4558; }
.say { background:#f2f4f8; border-left:3px solid var(--ink); padding:5px 8px; margin:4px 0 6px; font-size:9pt; }
.steps { display:grid; grid-template-columns:repeat(4,1fr); gap:6px; }
.steps > div { border:1px solid var(--line); border-radius:7px; padding:6px 7px; font-size:8.6pt; }
.steps b { font-size:7.8pt; text-transform:uppercase; letter-spacing:.05em; color:var(--ink); }
.mini { font: 12pt/1.9 "STIX Two Text", Georgia, serif; margin:2px 0; }
.mini sup { font-size:68%; }
.later, .note { font-size:8.6pt; color:var(--body); }
table { border-collapse:collapse; }
.sym { width:100%; margin:3px 0; font-size:8.6pt; }
.sym td { padding:2px 4px; vertical-align:top; }
.sym td:first-child { width:52px; white-space:nowrap; }
.grid { font-size:8.4pt; margin:5px 0; }
.grid th, .grid td { border-bottom:1px solid var(--line); padding:2px 7px; text-align:left; }
.grid th { color:var(--ink); }
.cmp { width:100%; }
.hl { border:1px solid #eab48a; background:#fff8f1; border-radius:7px; padding:6px 8px; margin-top:6px; font-size:8.6pt; }
.chart { width:100%; height:auto; margin:4px 0 0; }
.chart .gl { stroke:#e6e9ef; stroke-width:1; }
.chart .tk { font:9px "Helvetica Neue", sans-serif; fill:#6b7487; }
.chart .lb { font:10px "Helvetica Neue", sans-serif; fill:#3b4558; }
.chart .cv { fill:none; stroke:#c0581f; stroke-width:2; }
.chart .pl { stroke:#c2185b; stroke-width:1.5; stroke-dasharray:5 4; }
.chart .dl { stroke:#6b7487; stroke-width:1; stroke-dasharray:2 3; }
.chart .dot { fill:#17233d; stroke:#fff; stroke-width:2; }
.key { display:grid; grid-template-columns:repeat(4,1fr); gap:6px 10px; font-size:8.2pt; }
.chips { margin-bottom:1px; }
.dark { background:var(--ink); color:#e6e9f0; border-color:var(--ink); }
.dark h2 { color:#fff; } .dark .n { background:#fff; color:var(--ink); }
.flow { margin:0; padding-left:18px; } .flow li { margin:3px 0; }
.two { display:grid; grid-template-columns:1.25fr 1fr; gap:12px; align-items:start; }
.par { width:100%; } .par tr.grp th { background:#f2f4f8; font-size:8pt; text-transform:uppercase; letter-spacing:.04em; }
.mix { margin:0; padding-left:16px; } .mix li { margin:2px 0; }
.pb { break-before: page; }
"""

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Equation sheet</title><style>{CSS}</style></head><body>
<div class="top">EPS project · Nov 10 update · slide 40</div>
<h1>The model, one equation at a time</h1>
<p class="intro">Each symbol keeps one colour in every equation, so you can follow it as the model is built up. Numbers
are from the calibrated model (v6) used on the slides.</p>
<section class="card">{key_html}</section>
{big}{c1}
<div class="row pb">{c2}{c3}</div>
{c4}
{c5}
<div class="row">{c6}{c7}</div>
<div class="row">{c8}{c10}</div>
{c9}
</body></html>"""

out = os.path.join(HERE, "equation_sheet.html")
open(out, "w", encoding="utf-8").write(html)
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
pdf = os.path.join(HERE, "Equation sheet.pdf")
subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={pdf}", "file://" + out],
               check=True, capture_output=True)
print("wrote", out, "and", pdf)
