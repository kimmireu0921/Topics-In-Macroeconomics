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
XT = json.load(open(E + "v8_extra.json"))
CUR, PRICE, EQ, NONE = X["current rule"], X["price"], X["equal limit"], X["no EPS"]

PARTS = [("Mimi", ["nov24-cover", "nov24-feedback", "nov24-test"]),            # Nov 23: concise version, 12 slides;
         ("Benjamin", ["nov24-change", "nov24-env", "nov24-plant"]),                          # Donny takes the results (hardest)
         ("Julian", ["nov24-eq", "nov24-fit"]),
         ("Sara", ["nov24-who", "nov24-checks"]),
         ("Donny", ["nov24-results", "nov24-plans", "nov24-next"])]
ORDER = [s for _, ss in PARTS for s in ss]
FIRST = 63
TOTAL = FIRST - 1 + len(ORDER)
PG = {k: FIRST + i for i, k in enumerate(ORDER)}
PRESENTER = {s: n for n, ss in PARTS for s in ss}
SERIF, SANS = "'Source Serif 4', Georgia, serif", "'IBM Plex Sans', Arial, sans-serif"
NAVY, INK, BODY, MUTED, RUST, STEEL = "#14213d", "#1f2a3c", "#3d4756", "#5f6876", "#a8432c", "#2f5d8a"
LOGO = "/_blob/921ccfeb3c9f6d9c3ed1cc4a5be8bdd4"
EQS = ["(1) y = s·(h^ρ + λₜ ℓ^ρ)^(α/ρ), ℓ = k + m", "(2) cost of k = w·(1 + ψ(1 + h)^−ξ); of m = w", "(3) Eligible (prob. e): m ≤ q(h + k), h + k &lt; 300",
       "(4) Price: m at w + p, no cap", "(5) Exit if β(1−δ)E[V(s′)] &lt; 0; Σν V = cₑ", "(6) Σμ(h + k) = N, Σμ m = M"]


def pct(x, d=0, sign=False):
    v = round(100 * x, d) + 0.0                       # no "−0.00%"
    if v == 0:
        return f"{0:.{d}f}%"
    return f"{v:{'+' if sign else ''}.{d}f}%".replace("-", "−")


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
CH19 = json.load(open(E + "v8_capuse_hist.json"))           # model and data, plants with 1+ EPS worker
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
<h1 style="position:absolute; top:150px; left:128px; width:1664px; font-family:{SERIF}; font-size:88px; font-weight:600; line-height:1.1; color:#f7f5f0">EPS project: the new model<br>and what it says</h1>
<p style="position:absolute; top:376px; left:128px; width:1664px; font-family:{SANS}; font-size:36px; line-height:1.4; color:#c9d1de">November 24, 2026 · Random eligibility and the full legal cap</p>
<h2 style="position:absolute; top:490px; left:128px; width:1664px; font-family:{SERIF}; font-size:52px; color:#f7f5f0"><b>Research Topic: Does tying EPS workers to plant size keep weak plants alive, and how much would output change if the same quota ignored plant size?</b></h2>
<p style="position:absolute; bottom:96px; left:128px; width:1664px; font-family:{SANS}; font-size:26px; line-height:1.5; color:#c9d1de">Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo<br>ISA6327 Topics in Macroeconomics · Prof. Sewon Hur · November 24, 2026</p>
{presenter("nov24-cover", True)}{page("nov24-cover", True)}{logo()}{notes([("Title", '"Good afternoon. Today: the histogram you asked for, the new model in brief, and what it says."')])}
</section>
''')

# ------------------------------------------------------------------ feedback
rows = [["Your comment", "What we did"],
        ["Justify the 21% rule with the data", f"Survey histogram: firms are spread out, median {pct(H['median'])} of the cap. Rule dropped"],
        ["Random eligibility, or a two-sector model", f"Random eligibility: {pct(e24)} of new plants; eligible plants hire up to their legal cap"],
        ["The cap counts all Korean workers", "Cap q(h + k) and h + k &lt; 300, as in the law"],
        ["Drop the inferred 2024 line and the larger-quota comparison", "Dropped"],
        ["Send a write-up of the model", "Sent (model note)"]]
write("nov24-feedback", f"""{h2("Your feedback, and what we changed")}
{table(rows, [42, 58], 26)}""",
      [("Table", '"Here is what you asked for and what we did. The main change: the 21 percent rule is gone, replaced by random eligibility, as you suggested."')], band=False)

# ------------------------------------------------------------------ the test
dm, mm = CH19["data"], CH19["model"]
below30 = lambda r: sum(r["share"][:3])
write("nov24-test", f"""{h2("The histogram: EPS workers ÷ legal cap, plants with at least one EPS worker")}
{fig("fig_capuse.png", 1664, 560, "Share of the 2019 legal cap used, survey against the model")}
{box(f"<b>Same average</b> ({pct(dm['mean'])}, targeted). <b>Model is more concentrated:</b> no plants below 30% or above 100% of the cap; the survey has {pct(below30(dm))} and {pct(dm['share'][-1])}.", size=25)}
{foot("2019 survey, 772 firms; 2019 caps (Lee, Peri and Yang, Table 4). Model under the 2019 caps.")}""",
      [("Chart", '"Orange is the survey, blue the model, both under the 2019 caps and only plants with at least one EPS worker. The dashed line is our old 21 percent rule: the data clearly reject it."'),
       ("Box", f'"The model matches the average, which we target. But it is too concentrated: it has no plants below 30 percent of their cap, where the survey has {pct(below30(dm))}, and none above the cap, where the survey has {pct(dm["share"][-1])}."'),
       ("If asked: the spikes", '"Many survey firms have a cap of 5, so one to four workers is 20, 40, 60 or 80 percent."'),
       ("If asked: why none below 30 percent", '"Using EPS has a fixed cost in the model, so a plant that uses EPS hires several workers. We have not tested this yet."')], band=False)

# ------------------------------------------------------------------ what changed
rows = [["", "Before (Nov 17 talk)", "Now"],
        ["Who may hire EPS workers", "Every plant with 1–299 core Korean workers", f"A random {pct(e24)} of new plants (EPS-eligible)"],
        ["How many", "21% of its legal cap (θ = 0.21), the same for every plant", "Up to its full legal cap"],
        ["What the cap counts", "Core Korean workers h only", "All Korean workers h + k, as in the law"],
        ["What makes total EPS use equal the quota", "θ", "The eligible share"],
        ["Targets", "Two had no source (5.5%, 10%)", "All sourced, plus the survey's 62% cap use"],
        ["Main result", "Price +0.33%; equal limit +0.09 to +0.19%", f"Price {pct(XT['caps2024']['price']['net'], 2, True)}; equal limit {pct(XT['caps2024']['equal_limit']['net'], 2, True)}"]]
write("nov24-change", f"""{h2("What changed in the model since last week")}
{table(rows, [28, 36, 36], 24, hi=(0, 1))}
{foot("Unchanged: entry and exit (Hopenhayn), light and manual-intensive plants, the cost of Korean manual workers, and Korean and EPS manual workers as perfect substitutes.")}""",
      [("Title", '"For those who were not here last week: here is exactly what changed. Before, every plant could use EPS, but only 21 percent of its cap. Now a random share of plants is eligible, and eligible plants can use their full legal cap, counted on all Korean workers as the law does."'),
       ("Why", '"The data rejected the 21 percent rule: real firms use 60 percent of their cap on average, not 21. Random eligibility was one of the two fixes the professor suggested."'),
       ("Last row", '"The headline result also changed. Last week, removing the link to size gained up to 0.19 percent. Now it gains nothing, because caps rarely bind once access is rationed. More on that at the end."')], band=False)

# ------------------------------------------------------------------ model 1: plants and EPS rules
write("nov24-env", f"""{h2("The model (1/3): plants and today's EPS rules")}
{bullets([
    "Hopenhayn economy: plants enter, produce, and exit when staying is not worth it. Korean labour and the EPS quota are fixed",
    "At entry each plant draws, for good: its <b>type</b> (light, or manual-intensive), its <b>productivity</b>, and whether it is <b>EPS-eligible</b>",
    f"Eligible plants ({pct(e24)} of entrants, by chance) may hire EPS workers up to the legal cap q(h + k), if h + k &lt; 300; others hire none",
    "The eligible share adjusts until total EPS use equals the quota (5.29% of manufacturing workers). It stands in for the points ranking and waiting lists"], 25)}
{table(CAP24, [22, 11, 13, 11, 11, 11, 11, 10], 22)}
{table(CAP19, [22, 9, 9, 10, 10, 10, 10, 10, 10], 22)}
{foot("2024 caps for today's economy (eps.go.kr); 2019 caps for the survey firms (Lee, Peri and Yang, Table 4). h: core Korean workers; k: Korean manual workers.")}""",
      [("Bullets", f'"Each plant draws three things when it enters: its type, its productivity, and whether it is eligible for EPS. Eligibility is random, {pct(e24)} of new plants, and that share adjusts until the quota is used. Eligible plants can hire up to their legal cap, counted on all Korean workers."'),
       ("Tables", '"These are the legal caps. We use the 2024 schedule for today\'s economy and the 2019 schedule when we compare with the survey, because those firms faced the 2019 caps."'),
       ("If asked: why random", '"The professor suggested it, and it matches the data: demand exceeds the quota, and which firm gets workers is partly luck in the points system."')], band=False)

# ------------------------------------------------------------------ model 2: output, costs and the plant's choice
prem_rows = [["Core Korean workers h", "0", "7", "28", "150"], ["Cost of a Korean manual worker ÷ wage"] + [f"{PREM(h):.2f}" for h in (0, 7, 28, 150)]]
write("nov24-plant", f"""{h2("The model (2/3): output, costs and the plant's choice")}
{row(col(eqbox("y = s·(h<sup>ρ</sup> + λ<sub>t</sub> ℓ<sup>ρ</sup>)<sup>α/ρ</sup>, &nbsp;ℓ = k + m", 28) + bullets(["Output needs core Korean workers h and manual work ℓ", "Manual work is done by Korean manual workers k or EPS workers m, one for one", "Manual-intensive plants put much more weight λ on manual work"], 23)
         + eqbox("V(s) = π(s) + σ<sub>ε</sub>·log(1 + e<sup>β(1−δ)E[V(s′)]/σ<sub>ε</sub></sup>)", 28) + bullets(["A plant stays if the future is worth it; new plants enter until entry pays"], 23), 1),
     col(eqbox("cost of k = w·(1 + ψ(1 + h)<sup>−ξ</sup>); &nbsp;cost of m = w + fixed c<sub>m</sub>", 28) + bullets(["Small plants cannot find Korean manual workers, so each one costs more than the wage", "An EPS worker costs the wage, so it saves that extra cost"], 23)
         + table(prem_rows, [44, 14, 14, 14, 14], 22), 1))}
{foot("In the 2019 survey, the smallest firms fill only 44% of planned Korean manual hires (large firms 89%), while their Korean wages are no higher.")}""",
      [("Left", '"A plant combines core Korean workers with manual work, which can be done by a Korean manual worker or an EPS worker. Plants exit when the future is not worth it, and enter until entry pays."'),
       ("Right", f'"Korean manual workers are hard to find at small plants, so each one costs more than the wage: {PREM(0):.1f} times at a plant with no core Koreans, {PREM(150):.1f} times at 150. An EPS worker costs the wage, so it saves that extra cost."'),
       ("Footer", '"The survey backs this: small firms fill less than half the Korean manual jobs they plan, but they do not pay Koreans more. The extra cost is unfilled jobs."')], band=False)

# ------------------------------------------------------------------ model 3: equilibrium and experiments
rows = [["", "Today", "Price", "Equal limit"],
        ["Who may hire EPS", "Eligible plants", "Any plant", "Same eligible plants"],
        ["How many", "Up to q(h + k)", "Any number", "Up to L, same for all"],
        ["Cost per EPS worker", "w", "w + p", "w"],
        ["Clears the quota", "e", "p", "L"]]
write("nov24-eq", f"""{h2("The model (3/3): equilibrium and the two experiments")}
{table(rows, [28, 24, 24, 24], 26)}
{box("Equilibrium: the wage, the quota variable, entry and the plant distribution are such that Korean labour and the quota are fully used. Same quota in every case.", size=25)}""",
      [("Table", '"We compare today with two ways of allocating the same quota: a permit price open to any plant, and an equal limit for the same eligible plants. The equal limit removes only the link to size."')], band=False)

# ------------------------------------------------------------------ calibration: fit
lab = dict(avg_size=("Average plant size", "Census 2024", 2), share_small=("Plants with 1–4 workers", "Census 2024", "p"),
           share_50plus=("Plants with 50+ workers", "Census 2024", "p"), exit_rate=("Exit rate", "Statistics Korea 2024", "p"),
           users=("Plants using EPS", "Ministry 2024", "p"), eps_share_users=("EPS share at EPS firms", "Lee, Peri and Yang", "p"),
           users_size=("Workers at EPS firms", "Lee, Peri and Yang", 1), use_of_cap=("Share of cap used", "EPS survey 2019", "p"))
fmt = lambda v, d: pct(v, 1) if d == "p" else f"{v:.{d}f}"
rows = [["Target", "Data", "Model", "Source"]] + [[lab[k][0], fmt(T[k], lab[k][2]), fmt(FIT[k], lab[k][2]), lab[k][1]] for k in lab]
slope = R["checks"]["slope_lpy"]
write("nov24-fit", f"""{h2("Calibration: 13 parameters, 8 targets")}
{table(rows, [36, 16, 16, 32], 24)}
{box(f"<b>Not matched:</b> the closure response to the 2020 stop (Lee, Peri and Yang 0.15; model {slope:.2f}). EPS users in the model are far from closing.", size=24)}""",
      [("Table", '"Every target has a source; the model fits all eight closely."'),
       ("Box", '"One thing we do not match: how much more EPS firms closed after the 2020 stop. In our model, plants that use EPS are productive enough that a temporary cut does not push them out. We state this as a limitation."')], band=False)

# ------------------------------------------------------------------ who uses EPS
gname = dict(manual_eligible="Manual-intensive, eligible", manual_not="Manual-intensive, not eligible",
             light_eligible="Light, eligible", light_not="Light, not eligible")
rows = [["Group", "% of plants", "% using EPS", "Workers per plant"]]
for k2 in ("manual_eligible", "manual_not", "light_eligible", "light_not"):
    g = G[k2]
    rows.append([gname[k2], pct(g["plants"], 1), pct(g["user_rate"]), f"{g['size']:.1f}"])
write("nov24-who", f"""{h2(f"Who uses EPS: {pct(CUR['users'], 1)} of plants (data 8.0%)")}
{table(rows, [40, 20, 20, 20], 27, hi=(0,))}
{box("Only eligible manual-intensive plants use EPS. Light plants have little manual work; non-eligible plants cannot.", size=25)}""",
      [("Table", '"This answers your concern that every firm wanted EPS workers. Now only the highlighted group uses them: about 7 percent of plants, against 8 percent in the data."')], band=False)

# ------------------------------------------------------------------ checks: size pattern
write("nov24-checks", f"""{h2("An untargeted check: EPS firms by size")}
{fig("fig_size.png", 1664, 562, "EPS firms by total workers, model against the survey, 2019 caps")}
{foot("2019 caps, EPS users only; survey: 772 firms. Only the averages are targeted.")}""",
      [("Left", '"Where EPS firms are by size: close to the survey."'),
       ("Right", '"Their EPS share falls with size in both, but the model is too flat among the smallest firms."')], band=False)

# ------------------------------------------------------------------ results
C19, C24 = XT["caps2019"], XT["caps2024"]
B24, B19 = XT["binding_2024"], XT["binding_2019"]
rows = [["Same quota, change against today", "Net output, 2024 caps", "Net output, 2019 caps", "Gross output, 2024", "Net if the premium is only pay"],
        ["Equal limit: same eligible plants, no link to size", pct(C24["equal_limit"]["net"], 2, True), pct(C19["equal_limit"]["net"], 2, True), pct(C24["equal_limit"]["gross"], 2, True), pct(C24["equal_limit"]["net_premium_as_pay"], 2, True)],
        ["Price: any plant may buy permits", pct(C24["price"]["net"], 2, True), pct(C19["price"]["net"], 2, True), pct(C24["price"]["gross"], 2, True), pct(C24["price"]["net_premium_as_pay"], 2, True)],
        ["No EPS at all (for scale)", pct(chg("no EPS"), 2, True), "—", pct(chg("no EPS", "Y"), 2, True), "—"]]
write("nov24-results", f"""{h2("Result: the link to size barely matters; access does")}
{table(rows, [34, 16, 16, 15, 19], 25, hi=(1,))}
{box(f"<b>Why size does not matter:</b> caps rarely bind ({pct(B24['users_at_cap'], 1)} of users at the 2024 cap). <b>Why a price helps:</b> permits go to plants that value them most. <b>Caveat:</b> the gain is the Korean premium saved.", size=25)}""",
      [("Table", f'"Same quota, three ways. Removing the link to size changes nothing, under either cap schedule. Letting any plant buy permits raises net output by {pct(C24["price"]["net"], 2, True)}."'),
       ("Box", f'"Size does not matter because caps rarely bind: only {pct(B24["users_at_cap"], 1)} of users are at their 2024 cap. A price helps because permits move to the plants that value them most. But the gain is the premium saved: if the premium is only higher pay, the gain is about zero."'),
       ("If asked: does the size rule keep weak plants alive", '"In this model, no: the caps rarely bind. Whether a plant gets permits at all matters much more."')], band=False)

# ------------------------------------------------------------------ where EPS workers go
BH = XT["by_h"]
hb = [("2-5", "2–4"), ("5-10", "5–9"), ("10-30", "10–29"), ("30-1e+09", "30+")]
rows = [["Core Korean workers h"] + [l for _, l in hb], ["Share of EPS workers, today"] + [pct(BH["today"][k2]) for k2, _ in hb],
        ["Share of EPS workers, price"] + [pct(BH["price"][k2]) for k2, _ in hb]]
def prow2(name, d, i):
    return [name, f"{d['h'][i]:.0f}", f"{d['k'][i]:.0f}", f"{d['m'][i]:.0f}"]


rows2 = [["Eligible manual-intensive plant", "Core h", "Korean manual k", "EPS m"]]
for i2, who2 in ((0, "Median"), (1, "Top 1%")):
    rows2 += [prow2(f"{who2}: today", PL["current"], i2), prow2(f"{who2}: price", PL["price"], i2)]
write("nov24-plans", f"""{h2("Why: with a price, EPS workers move to mid-sized plants")}
{table(rows, [36, 16, 16, 16, 16], 25, hi=(1,))}
{row(col(table(rows2, [40, 18, 24, 18], 22), 1), col(box(f"Large plants (30+ core Koreans) hold {pct(BH['today']['30-1e+09'])} of EPS workers today but save little: Koreans are easy to find there. At a price of {PRICE['x']:.2f} ({pct(PRICE['x'] / PRICE['w'])} of the wage), the median and top plants stop using EPS, and the workers go to plants with 5–29 core Koreans.", size=23), 1))}""",
      [("Top table", f'"Where EPS workers are, by core Korean workers. Today {pct(BH["today"]["30-1e+09"])} are at plants with 30 or more core Koreans. With a price, they all move to plants with 5 to 29, where Korean manual workers are scarcest."'),
       ("Bottom table", '"Two eligible plants, the median and the top 1 percent. Today both use EPS workers. With a price, neither does: for them an EPS worker saves less than the price."'),
       ("If asked: why not the smallest", '"Using EPS has a fixed cost, which the smallest plants cannot cover at that price."')], band=False)

# ------------------------------------------------------------------ assumptions and questions
write("nov24-next", f"""{h2("What we assume, and our questions")}
{row(col(h3("Key assumptions") + bullets([
    "Korean and EPS manual workers are perfect substitutes",
    "Eligibility is random and permanent",
    "The quota is fully used",
    "The Korean premium is a real cost (unfilled jobs), not pay"], 26), 1),
     col(h3("Questions for you") + bullets([
    "<b>Is the model settled?</b> We plan to freeze it and write the paper",
    "Should the paper ask about access (who gets permits) rather than size?",
    "Should eligibility be redrawn over time (permits last 3 years)?"], 26), 1))}""",
      [("Left", '"These four assumptions matter most for the result. The last one matters most: the gain is the premium saved."'),
       ("Right", '"Three questions. Most important: is the model settled, so we can freeze it and write the paper? Second, since caps rarely bind, should the paper be about access rather than size? Third, should eligibility be redrawn over time?"'),
       ("Close", '"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."')], band=False)

print("slides", {k: PG[k] for k in ORDER}, "total", TOTAL)
