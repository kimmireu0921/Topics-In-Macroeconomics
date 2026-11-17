"""Writes the Nov 10 slides (presented Nov 17) into the deck folder from the baseline results.
Usage: build.py <deck root>. Image URLs come from blobs.json (uploaded fig_*.png)."""
import json, os, sys
import numpy as np

ROOT = sys.argv[1]
SL = os.path.join(ROOT, "project/slides")
HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.join(HERE, "../../hopenhayn_project/eps_model/baseline/")
D, S = json.load(open(B + "diagnostics.json")), json.load(open(B + "survey_binding.json"))
FF, PR, G = json.load(open(B + "free_flat.json")), json.load(open(B + "premium_slope.json")), json.load(open(B + "bumpy_line.json"))
BLOB = json.load(open(os.path.join(HERE, "blobs.json")))
R = D["runs"]
C24, C19, NR = R["current_2024"], R["current_2019"], R["no_rule"]
REG = {x["name"]: x for x in FF if not x["grid"]}
FIN = {x["name"]: x for x in FF if x["grid"]}
QUOTA50, QUOTA50F = 0.0372, 0.0365                 # v6_quota_check.json, net output at +50% quota
FIT = json.load(open(B + "../v6_results.json"))["fit"]  # calibration fit, 2019 caps
TOP = json.load(open(B + "top_plant.json"))              # top_plant.py: the top 1% plant at each wage
WHY = json.load(open(B + "../v6_why_no_rule.json"))      # v6_why_no_rule.py: costs by source

PARTS = [("Sara", ["nov10-cover", "nov10-model1", "nov10-model2", "nov10-data", "nov10-targets", "nov10-answers"]),
         ("Mimi", ["nov10-who", "nov10-size", "nov10-shares", "nov10-policy", "nov10-scale"]),
         ("Julian", ["nov10-binding", "nov10-capuse", "nov10-wants", "nov10-quota"]),
         ("Benjamin", ["nov10-margin", "nov10-top", "nov10-split", "nov10-split2", "nov10-costs", "nov10-premium", "nov10-bumpy", "nov10-bunch"]),
         ("Mimi", ["nov10-next"])]
ORDER = [s for _, ss in PARTS for s in ss]
FIRST, TOTAL = 39, 38 + len(ORDER)
PG = {k: FIRST + i for i, k in enumerate(ORDER)}
SERIF, SANS = "'Source Serif 4', Georgia, serif", "'IBM Plex Sans', Arial, sans-serif"
NAVY, INK, BODY, MUTED, RUST, STEEL = "#14213d", "#1f2a3c", "#3d4756", "#5f6876", "#a8432c", "#2f5d8a"
LOGO = "/_blob/921ccfeb3c9f6d9c3ed1cc4a5be8bdd4"
PRESENTER = {s: n for n, ss in PARTS for s in ss}         # Nov 17: Donny away, his part goes to Mimi
HANDOVER = {"nov10-answers": "Mimi will now show who uses EPS in the model, and the policy functions.", "nov10-scale": "Julian will now show whether the cap binds, in the survey and in the model.", "nov10-quota": "Benjamin will now explain why large plants barely grow, and the checks we ran.", "nov10-bunch": "Mimi will sum up and ask our questions."}
EQS = ["(1) y = s·(h^ρ + λₜ ℓ^ρ)^(α/ρ), ℓ = k + m", "(2) cost of k = w·(1 + ψ(1 + h)^−ξ)", "(3) Current rule: m ≤ θ·q(h), cost ≈ w",
       "(4) No size rule: cost of m = w + p", "(5) Exit if β(1−δ)E[V(s′)] &lt; 0; Σν V = cₑ", "(6) Σμ(h + k) = N, Σμ m = M"]


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
    return (f'<p style="position:absolute; top:64px; right:128px; width:480px; font-family:{SANS}; font-size:24px; font-weight:600; '
            f'text-align:right; color:{"#c9d1de" if dark else MUTED}">Presenter: {PRESENTER[id_]}</p>')


def foot(text):
    return f'<p style="position:absolute; bottom:40px; left:128px; width:1440px; font-family:{SANS}; font-size:24px; color:{MUTED}">{text}</p>'


def h2(text):
    return f'<h2 style="font-family:{SERIF}; font-size:52px; font-weight:600; line-height:1.15; color:{NAVY}">{text}</h2>'


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


def cards(items):
    return f'<div style="display:grid; gap:24px; grid-template-columns:{" ".join(["1fr"] * len(items))}">{"".join(items)}</div>'


def row(*parts):
    return f'<div style="display:flex; flex-direction:row; gap:32px">{"".join(parts)}</div>'


def col(html, flex):
    return f'<div style="display:flex; flex-direction:column; gap:24px; flex:{flex}">{html}</div>'


def fig(name, w, h, alt):
    return f'<img src="{BLOB[name]}" alt="{alt}" style="width:{w}px; height:{h}px; object-fit:contain">'


def bullets(items):
    return f'<ul style="font-family:{SANS}; font-size:26px; line-height:1.4; color:{BODY}">{"".join(f"<li>{i}</li>" for i in items)}</ul>'


def notes(blocks):
    text = "<br><br>".join(f"[{a}]<br>{b}" for a, b in blocks)
    assert len(text) <= 4000, len(text)
    return f"<aside>{text}</aside>"


def write(id_, body, blocks, on=(), band=True):
    if id_ in HANDOVER:
        blocks = blocks + [("Hand over", f'"{HANDOVER[id_]}"')]
    html = (f'<section id="{id_}" data-transition="fade" style="display:flex; flex-direction:column; gap:28px; padding:128px 128px {220 if band else 160}px; background:#ffffff">\n'
            f'{body}{eqs(on) if band else ""}{presenter(id_)}{page(id_)}{logo()}{notes(blocks)}\n</section>\n')
    open(os.path.join(SL, id_ + ".html"), "w").write(html)


# ------------------------------------------------------------------ numbers
who, b24, b19 = C24["who_uses"], C24["binding"], C19["binding"]
sg = np.array(C24["s_grid"])
pc = C24["pct"]["manual"]
act, fre = C24["policy"]["manual"]["actual"], C24["policy"]["manual"]["free"]


def plan(p, q):
    i = int(np.searchsorted(sg, pc[q]))
    h, k, m = p["h"][i], p["k"][i], p["m"][i]
    return h, k, m, h + k + m


T = C24["size_table"]
CU = S["by_cap_use"]                               # survey: cap use against wanting more workers
PREM = lambda h: 1 + D["params"]["psi"] * (1 + h) ** -D["params"]["xi"]   # Korean manual cost / w, equation (2)
ratios = [T[b]["free_size_manual"] / T[b]["size_manual"] for b in T]
SALL = S["all"]
wanted_ratio = SALL["wanted"] / SALL["eps"]
T19 = C19["size_table"]
ubt = C19["users_by_total"]
sbt = S["by_total_workers"]
cut = (NR["x"] / (NR["w"] * D["params"]["psi"])) ** (-1 / D["params"]["xi"]) - 1
net = lambda d, n: d[n]["net_Y"] / d["current"]["net_Y"] - 1
gross = lambda d, n: 100 * d[n]["Y"] / d["current"]["Y"]
costs = lambda d, n: 100 * (d[n]["Y"] - d[n]["net_Y"]) / d["current"]["Y"]
small = lambda d, n: d[n]["size"]["0-5"]["share_eps"]
PT = lambda n: REG[n]["policy"]["total"][2]


def gk(reg, nx, nz, nh=None, nl=None):
    return next(g for g in G if g["reg"] == reg and g["grid"]["nx"] == nx and g["grid"]["nz"] == nz and g["grid"].get("nh") == nh and g["grid"].get("nl") == nl)


def step_range(g):
    v = list(g["step_ratio"].values())
    return f"{min(v):.1f}–{max(v):.1f}"


# ------------------------------------------------------------------ cover
open(os.path.join(SL, "nov10-cover.html"), "w").write(f'''<section id="nov10-cover" data-transition="fade" style="background:{NAVY}">
<h1 style="position:absolute; top:150px; left:128px; width:1664px; font-family:{SERIF}; font-size:88px; font-weight:600; line-height:1.1; color:#f7f5f0">EPS project update:<br>understanding the baseline</h1>
<p style="position:absolute; top:376px; left:128px; width:1664px; font-family:{SANS}; font-size:36px; line-height:1.4; color:#c9d1de">November 17, 2026 · Who uses EPS, who is held back, and what removing the size rule really does</p>
<h2 style="position:absolute; top:490px; left:128px; width:1664px; font-family:{SERIF}; font-size:52px; color:#f7f5f0"><b>Research Topic: Does tying EPS workers to plant size keep weak plants alive, and how much would output change if the same quota ignored plant size?</b></h2>
<p style="position:absolute; bottom:96px; left:128px; width:1664px; font-family:{SANS}; font-size:26px; line-height:1.5; color:#c9d1de">Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo<br>ISA6327 Topics in Macroeconomics · Prof. Sewon Hur · November 17, 2026</p>
{presenter("nov10-cover", True)}{page("nov10-cover", True)}{logo()}{notes([("Title", '"Good afternoon. Last time you asked us to understand the baseline model before running more experiments. The model has not changed since then. Today we show how it behaves."'),
 ("Plan", '"First a short refresher on the model and our data, including a check of where every target comes from. Then who uses EPS, whether the limit binds, why removing the size rule does not make large plants grow, and the checks you asked for."')])}
</section>
''')

# ------------------------------------------------------------------ model, part 1
def eqbox(e):
    return f'<p style="font-family:{SERIF}; font-size:34px; line-height:1.3; color:{NAVY}; padding:18px 24px; background:#f4f7fb; border-radius:12px">{e}</p>'


prem_rows = [["Core Koreans h", "0", "7", "28", "150"], ["Cost of a Korean manual worker ÷ w"] + [f"{PREM(h):.2f}" for h in (0, 7, 28, 150)]]
write("nov10-model1", f"""{h2("The model (1/2): what a plant makes, and what its workers cost")}
{row(col(eqbox("(1) y = s·(h<sup>ρ</sup> + λ<sub>t</sub> ℓ<sup>ρ</sup>)<sup>α/ρ</sup>, &nbsp;ℓ = k + m") + bullets([
    "s: the plant's productivity",
    "h: core Korean workers. ℓ: manual work, done by Korean manual workers k or EPS workers m, one for one",
    f"λ<sub>t</sub>: weight on manual work, {D['params']['lamA']:.3f} for light plants and {D['params']['lamB']:.2f} for manual-intensive plants",
    "α = 0.69 &lt; 1: each extra worker adds a little less"]), 1),
     col(eqbox("(2) cost of k = w·(1 + ψ(1 + h)<sup>−ξ</sup>)") + bullets([
    "Korean manual workers are hard to find at small plants (“no applicants”), so they cost more than the wage w",
    "An EPS worker costs w, so each one saves this premium"]) + table(prem_rows, [40, 15, 15, 15, 15], 24), 1))}
{foot(f"Hopenhayn (1992) with two plant types. 13 parameters calibrated to 8 targets; unchanged since Nov 3. Slide {PG['nov10-targets']} lists the targets.")}""",
      [("Equation 1", '"A plant has productivity s. It needs core Korean workers h and manual work. Manual work can be done by a Korean manual worker or an EPS worker, one for one. Light plants put almost no weight on manual work; manual-intensive plants put a lot."'),
       ("Equation 2", f'"Korean manual workers cost more than the wage, most of all at small plants. At a plant with no core Koreans the cost is {PREM(0):.2f} times the wage; at 150 it is {PREM(150):.2f}. An EPS worker costs the wage, so it saves that premium."'),
       ("If asked: how many parameters", '"13 parameters and 8 targets, so it is not exactly identified target by target."')], band=False)

# ------------------------------------------------------------------ model, part 2
rows = [["Equation", "In words", "Value"],
        ["(3) m ≤ θ·q(h) if 1 ≤ h &lt; 300; cost of m = w", "Today: EPS workers up to a share θ of the legal cap q. θ is the same for every plant and adjusts so the quota is used", f"θ = {C24['x']:.2f}"],
        ["(4) cost of m = w + p, any plant with h ≥ 1", "Experiment: no cap. Every plant pays the same permit price p, which adjusts so the same quota is used", f"p = {REG['price']['price']:.2f}"],
        ["(5) Exit if β(1−δ)E[V(s′)] &lt; 0; Σν V = c<sub>e</sub>", "Plants close when the future is not worth it. New plants enter until entering is worth its cost, which sets the wage w", f"w = {REG['current']['w']:.2f}"],
        ["(6) Σμ(h + k) = N, Σμ m = M", "Korean labor N and the EPS quota M are fixed, and both are fully used", "M: 5.5% of workers"]]
write("nov10-model2", f"""{h2("The model (2/2): the size rule, the experiment, entry and exit")}
{table(rows, [34, 50, 16], 24)}
{box("<b>A simplification we will fix:</b> the model's cap and eligibility count core Koreans h only. The law counts all insured Korean workers, h + k.")}
{foot("θ, p and w are solved in equilibrium. Values: v6 calibration, 2024 caps.")}""",
      [("Rule and experiment", '"Today a plant can have EPS workers up to a share theta of its legal cap, and theta is the same for every plant. In our experiment the cap is gone and every plant pays the same permit price p. Theta or p adjusts so the quota is used."'),
       ("Entry and exit", '"Plants close when the future is not worth it, and new plants enter until entry is worth its cost. That pins down the wage. Korean labor and the quota are fixed."'),
       ("Box", '"One simplification: our cap counts core Koreans only, while the law counts all Korean workers. We will change that for next time."')], band=False)

# ------------------------------------------------------------------ data
rows = [["Source", "Sample", "Construction rules", "Gives us"],
        ["MDIS business census (전국사업체조사), 2024", "All 509,467 manufacturing plants (KSIC C)", "Workers = all workers at the plant. 13% of headcounts are masked by size band; we give each the band's average", "Plant size targets"],
        ["KDI–World Bank EPS survey, 2019", "772 manufacturers that use EPS", "Cap from Korean workers in Feb 2019 (Ministry list). Wants more = extra workers wanted with no limit (Q9) &gt; 0", "Cap use, wanting more, users by size"],
        ["Lee, Peri and Yang (2026)", "761 EPS firms, Jan 2020–Jan 2021", "As published, Tables 3 and 6", "EPS share and size at EPS firms; closures"],
        ["Ministry of Employment and Labor (e-나라지표), end of 2024", "E-9 workers and workplaces in manufacturing", "Workplaces = E-9 only + E-9 and H-2", "EPS share of workers, plants using EPS"],
        ["Statistics Korea, business demography, 2024", "Manufacturing enterprises", "Exit rate = enterprises that stopped ÷ active", "Exit rate"]]
write("nov10-data", f"""{h2("Our data: what each source covers, and how we used it")}
{table(rows, [24, 22, 36, 18], 22)}
{foot("Survey and census files stay outside our repository; the scripts that build every number are in it.")}""",
      [("Title", '"Before the results, here is every data source, the sample, and the rules we used to build each number."'),
       ("Rows", '"The census gives plant sizes. Some headcounts are hidden in size bands, so we give each hidden plant the average of its band. The survey covers only firms that use EPS, in 2019. Lee, Peri and Yang give the closure evidence. The Ministry and Statistics Korea give the EPS totals and the exit rate."'),
       ("If asked: why 2024", '"It is the latest year in the census, and it matches the 2024 caps in the model."')], on=())

# ------------------------------------------------------------------ targets
rows = [["Target", "Used so far", "Sourced value", "Source"],
        ["EPS workers ÷ manufacturing workers (sets the quota)", "5.5%", "5.29%", "219,507 E-9 workers ÷ 4.15 million census workers, 2024"],
        ["Plants that use EPS", "10%", "8.0%", "40,766 workplaces ÷ 509,467 plants, 2024"],
        ["Exit rate", "8% (assumed)", "6.6%", "Business demography, manufacturing, 2024"],
        ["Average plant size", "7.5", "8.14", "Census 2024, counting masked and 1,000+ plants"],
        ["Plants with 1–4 workers", "70%", "71.3%", "Census 2024"],
        ["EPS share at EPS firms, their size, closure slope", "36.9%, 20.8, 0.152", "Same", "Lee, Peri and Yang, Tables 3 and 6"]]
write("nov10-targets", f"""{h2("Checking our targets: two had no source, so we replaced them")}
{table(rows, [32, 16, 14, 38], 22, hi=(0, 1, 2))}
{box(f"<b>Today's results still use the old targets.</b> Against the sourced values, the model has too many EPS users ({pct(FIT['users'], 1)} vs 8.0%) and too much exit ({pct(FIT['exit_rate'], 1)} vs 6.6%). We are recalibrating and will show the results on Nov 24.")}
{foot("Check: manufacturing has 81% of all E-9 workers (219,507 of 271,925), in line with published figures of about 80%.")}""",
      [("Title", '"We traced every calibration target to its source. Two had none: the EPS share of workers and the share of plants using EPS were rough figures from our first model. The exit rate was an assumption."'),
       ("Table", '"Here are the sourced values. The EPS share of workers barely changes. The share of plants using EPS falls from 10 to 8 percent, and the exit rate from 8 to 6.6 percent. Average size rises to 8.1 once we count the plants the census masks and the largest plants."'),
       ("Box", '"Today\'s results use the old targets. The model has too many EPS users and too much exit against the new values, so we are recalibrating. We will bring the new results next week."'),
       ("If asked: are workplaces and plants the same", '"Not exactly. The Ministry counts workplaces and the census counts establishments. They are close, but the 8 percent may be off slightly."')], on=(6,))

# ------------------------------------------------------------------ answers
rows = [["What you asked", "Short answer", "Slides"],
        ["Who uses EPS? Is the 10.7% assumed?", f"Manual-intensive plants, {pct(who['users_manual'] / who['manual'])} of them. The {pct(who['users'], 1)} follows mostly from their share, which we calibrate", f"{PG['nov10-who']}"],
        ["Do users match the data? What is the EPS share?", "Same pattern by size, but too many very small users. Three EPS shares, defined", f"{PG['nov10-size']}–{PG['nov10-shares']}"],
        ["Which plants are at their optimal scale?", f"Light plants, {pct(who['light'])} of plants. {pct(b24['users_want_more'])} of EPS users are below it, held back by the quota", f"{PG['nov10-policy']}–{PG['nov10-scale']}"],
        ["Is the cap binding?", f"{pct(SALL['at_or_above'])} at or above the 2019 cap, about {pct(SALL['want_past_2024'])} past the 2024 cap. Firms far below the cap want more almost as often", f"{PG['nov10-binding']}–{PG['nov10-quota']}"],
        ["Why does gross output fall, and why do users get smaller?", "Large plants' next worker is Korean, so a permit only saves money; with a price they stop using EPS", f"{PG['nov10-margin']}–{PG['nov10-premium']}"],
        ["Is the bumpy line an error?", "Yes, mostly. It is smooth on finer grids, and the bunching result does not change", f"{PG['nov10-bumpy']}–{PG['nov10-bunch']}"]]
write("nov10-answers", f"""{h2("Your questions from last time, and the short answers")}
{table(rows, [32, 58, 10])}
{foot(f"Correction: 36.9% is the average EPS share across EPS firms, not the share in the economy. Slide {PG['nov10-shares']} defines all three.")}""",
      [("Title", '"Here is what you asked, with our short answers. The next slides show each one."'),
       ("Correction", f'"First, a correction. The EPS share of 36.9 percent is the average, across firms using EPS, of EPS workers divided by that firm\'s workers. It is not the share in the economy. Slide {PG["nov10-shares"]} shows all three meanings."'),
       ("Correction on the cap", '"We also said firms can go above the cap by request, by 3 to 6 workers. We have no source for that. In Dong, Lee and Yang, 3 to 6 is the maximum number of new permits. We\'ve asked the Ministry for the rule."'),
       ("Correction on the survey", f'"Earlier we said every user wants more. In the model that is {pct(b24["users_want_more"])}. In the survey it is {pct(SALL["want_more"])}."')],
      on=(3,))

# ------------------------------------------------------------------ who uses
mlam, llam = D["params"]["lamB"], D["params"]["lamA"]
rows = [["", "Light plants", "Manual-intensive plants"],
        ["Share of plants", pct(who["light"], 1), pct(who["manual"], 1)],
        ["Weight on manual work, λ", f"{llam:.3f}", f"{mlam:.2f}"],
        ["Manual workers per plant", num(who["light_manual_workers"]), num(who["manual_manual_workers"], 1)],
        ["Core Koreans per plant", num(who["light_core"], 1), num(who["manual_core"], 1)],
        ["Use EPS", pct(who["users_light"] / who["light"]), pct(who["users_manual"] / who["manual"])]]
write("nov10-who", f"""{h2("Who uses EPS: manual-intensive plants, and no light plants")}
{row(col(table(rows, [46, 24, 30], 26), 3), box(f"<b>Why:</b> an EPS worker saves the premium in equation (2), and using EPS has a fixed cost c<sub>m</sub>. Light plants have no manual work to save on. Even with free permits and no fixed cost, only {pct(who['light_gain_with_zero_cm'], 2)} would use EPS.", 2))}
{box(f"<b>So {pct(who['users'], 1)} of plants use EPS mostly because we calibrate {pct(who['manual'], 1)} to be manual-intensive.</b> The cap does not decide this. In the data, 8.0% of manufacturing plants employ EPS workers (2024).")}
{foot("Model, 2024 caps. Only about 0.1% of plants are manual-intensive and ineligible, because they have 300+ core Koreans.")}""",
      [("Title", '"You asked why only about 10 percent of plants use EPS. The answer is the two plant types."'),
       ("Table", f'"{pct(who["light"])} of plants are light: they have almost no use for manual work, so they hire no manual workers and none uses EPS. The other {pct(who["manual"])} are manual-intensive, and {pct(who["users_manual"] / who["manual"])} of those use EPS."'),
       ("Why box", '"An EPS worker costs less than a Korean manual worker because it saves the premium. A plant uses EPS if that saving beats the fixed cost. Light plants would not use EPS even if it were free."'),
       ("Bottom box", '"So the 10 percent mostly comes from a number we calibrate, not from the cap. The sourced value is 8 percent of plants, so the model has slightly too many users; the recalibration fixes that."'),
       ("If asked: is 89 percent with no manual workers realistic", '"Probably not literally. It is a two-type simplification. Real plants have some manual work. We need the data to say how far off it is."'),
       ("If asked: why hire EPS workers if they cost the same and are less productive", f'"Because Korean manual workers only come at a higher price, and the premium in equation 2 is that price. A Korean manual worker costs about {PREM(7):.1f} times the wage at a plant with 7 core Koreans and {PREM(150):.1f} times at 150. Employers rate EPS workers at 74 to 96 percent of a Korean worker. Even at 74 percent, an EPS worker costs about {1 / 0.74:.2f} times the wage per unit of work: still cheaper at small plants, but not at large ones. So lower productivity would make large plants want EPS even less, which supports our result."')],
      on=(1, 2))

# ------------------------------------------------------------------ users by size
keys = [("0-10", "Under 10"), ("10-20", "10–19"), ("20-50", "20–49"), ("50-100", "50–99"), ("100-200", "100–199"), ("200-300", "200–299")]
rows = [["Total workers", "Share of EPS firms: model", "Survey", "EPS share at those firms: model", "Survey"]]
for k, lab in keys:
    rows.append([lab, pct(ubt[k]["share_of_users"]), pct(sbt[k]["share_of_firms"]), pct(ubt[k]["eps_share"]), pct(sbt[k]["eps_share"])])
write("nov10-size", f"""{h2("Do model users match the data? The shape, but not the small end")}
{row(col(table(rows, [18, 24, 12, 32, 14], 24), 3), box(f"<b>Fits:</b> the EPS share falls with size in both, from about half at the smallest firms to about 5%. We only targeted the average.<br><br><b>Misses:</b> too many EPS firms under 10 workers ({pct(ubt['0-10']['share_of_users'])} vs {pct(sbt['0-10']['share_of_firms'])}), too few at 20–49 ({pct(ubt['20-50']['share_of_users'])} vs {pct(sbt['20-50']['share_of_firms'])}), and EPS shares too low from 20 workers up.", 2))}
{foot("2019 caps, firms under 300 workers. Survey: 772 EPS firms, 2019. Model: plants that use EPS.")}""",
      [("Title", '"You asked us to check that the model\'s EPS users look like the data\'s. Here they are by total workers, under the 2019 caps, when the survey was done."'),
       ("Right columns", '"The EPS share falls with size in both, from about half at the smallest firms to about 5 percent. We only targeted the average, so this shape is a check."'),
       ("Left columns", f'"The miss is in where users are: {pct(ubt["0-10"]["share_of_users"])} of the model\'s EPS firms are under 10 workers, against {pct(sbt["0-10"]["share_of_firms"])} in the survey, and too few are at 20 to 49. From 20 workers up, the model\'s EPS shares are also lower, for example {pct(ubt["20-50"]["eps_share"])} against {pct(sbt["20-50"]["eps_share"])} at 20 to 49."'),
       ("If asked: why the miss", '"We don\'t know yet. One theta for every plant may be the reason, but we haven\'t tested it."')],
      on=(3,))

# ------------------------------------------------------------------ three EPS shares
e9_share, plants_eps, size_eps, size_all = 0.0529, 0.080, 20.78, 8.14
at_eps = plants_eps * size_eps / size_all
write("nov10-shares", f"""{h2("Three different “EPS shares”, in the data and in the model")}
{table([["What “EPS share” means", "Data", "Source", "Model"],
        ["Average, across EPS firms, of EPS workers ÷ that firm's workers", "36.9%", "Lee, Peri and Yang, Table 3", pct(FIT["eps_share_users"], 1)],
        ["EPS workers ÷ all manufacturing workers", "5.3% (we used 5.5%)", "Ministry and census, 2024", pct(C24["summary"]["eps_share"], 1)],
        ["Share of plants that use EPS", "8.0% (we used 10%)", "Ministry and census, 2024", pct(who["users"], 1)]], [44, 18, 24, 14], 24)}
{box(f"<b>Check that they fit together:</b> 8% of plants use EPS, and they have about {size_eps:.0f} workers against {size_all:.0f} for the average plant, so they employ about {pct(at_eps)} of all workers. EPS workers are 5.3% of all workers, so about {pct(e9_share / at_eps)} of the workers at EPS plants. That is below the 37% average because large EPS firms have lower EPS shares.")}
{foot("The 37% average counts each firm once; the 26% share weights firms by their workers.")}""",
      [("Title", '"You asked us to define the EPS share. There are three, and they measure different things."'),
       ("Table", f'"The first, 36.9 percent, is the average across EPS firms of each firm\'s EPS share. The second, about 5 percent, is EPS workers in all manufacturing. It sets the quota. The third, 8 percent, is the share of plants that use EPS. The model has {pct(who["users"], 1)}, because it was calibrated to the old 10 percent."'),
       ("Box", '"They are consistent. EPS plants are about two and a half times the average size, so they hold about a fifth of all workers. A quarter of those workers are EPS workers, which gives about 5 percent of all workers."')],
      on=(3, 6))

# ------------------------------------------------------------------ policy functions
a50, f50, a90, f90, a99, f99 = plan(act, "50"), plan(fre, "50"), plan(act, "90"), plan(fre, "90"), plan(act, "99"), plan(fre, "99")
write("nov10-policy", f"""{h2("Policy functions for manual-intensive plants")}
{fig("fig_policy.png", 1664, 490, "Policy functions by productivity: EPS workers, Korean manual workers and all workers")}
{box(f"<b>Small plants use only EPS for manual work, and large plants mix.</b> The top 1% plant has {a99[2]:.0f} EPS and {a99[1]:.0f} Korean manual workers. With no limit it would have {f99[2]:.0f} EPS, none Korean, and grow from {a99[3]:.0f} to {f99[3]:.0f} workers.")}
{foot("Model, 2024 caps. p50, p90, p99: percentiles of productivity among manual-intensive plants. Blue line at today's prices.")}""",
      [("Title", '"These are the policy functions you asked for. Each panel has productivity on the horizontal axis, for manual-intensive plants. Blue is the current rule. Orange is what the plant would choose with no limit and free permits."'),
       ("Left panel", f'"EPS workers are held low by the limit under the current rule. The median plant has {a50[2]:.0f}, and the top 1 percent plant has {a99[2]:.0f}. With no limit they would want {f50[2]:.0f} and {f99[2]:.0f}."'),
       ("Middle panel", f'"This is the key panel. The median plant hires no Korean manual workers. A top 1 percent plant hires {a99[1]:.0f}. So for large plants, the next manual worker is Korean. With no limit, all of them switch to EPS."'),
       ("Right panel", f'"Total workers. With no limit, the top 1 percent plant grows from {a99[3]:.0f} to {f99[3]:.0f}, and the median from {a50[3]:.0f} to {f50[3]:.0f}. Keep in mind the orange line is not an equilibrium, as the next slide shows."'),
       ("If asked: why EPS falls to zero at the right", '"Past 300 core Koreans a plant is not eligible under the current rule."'),
       ("If asked: why the steps", '"Productivity is on a grid, and the plan changes in steps. The caps also create jumps. Slide ' + str(PG["nov10-bumpy"]) + ' checks the grid."')],
      on=(1, 2, 3))

# ------------------------------------------------------------------ scale
write("nov10-scale", f"""{h2("Who is held back: almost every user, by the quota, not the cap")}
{cards([card(pct(b24['users_want_more']), "of EPS users would hire more: below their optimal scale"), card(pct(b24['users_at_limit']), "are at their limit, θ × cap (2024 caps)"), card(pct(b24['users_at_legal_cap']), "reach the legal cap itself", True)])}
{box(f"<b>In the model the quota does the limiting; the legal cap only decides how it is shared.</b> With no limit and free permits, manual-intensive plants would be {min(ratios):.1f} to {max(ratios):.1f} times larger, but total demand would be {b24['ratio_free_to_quota']:.1f} times the quota, so that cannot happen at the same quota.")}
{foot("Model, 2024 caps. Optimal scale: the size a plant would choose with no limit at today's prices. Light plants are already there.")}""",
      [("Title", '"You asked who is constrained, and where they would be without the limit."'),
       ("Cards", f'"Optimal scale is the size a plant would choose with no limit. Light plants are already there. {pct(b24["users_want_more"])} of EPS users would hire more, and {pct(b24["users_at_limit"])} are at their limit. But the limit is theta times the cap, with theta {C24["x"]:.2f}, so no plant reaches the legal cap itself."'),
       ("Box", f'"So the quota does the limiting. Without any limit plants would be {min(ratios):.1f} to {max(ratios):.1f} times larger, but they would want {b24["ratio_free_to_quota"]:.1f} times the quota."'),
       ("If asked: 82 versus 98 percent", f'"The others sit just below their limit but would still hire more. Under the 2019 caps, {pct(b19["users_at_limit"])} are at the limit."'),
       ("If asked: is theta realistic", '"Theta is a simple stand-in for rationing: every plant gets the same share of its cap. Real rationing uses a score and a cut-off."')],
      on=(3, 6))

# ------------------------------------------------------------------ binding
write("nov10-binding", f"""{h2("Is the cap binding? Yes for 2019 caps, barely for 2024 caps")}
{fig("fig_binding.png", 1664, 470, "Share of survey firms at or above the cap and past it under 2019 and 2024 caps, by Korean workers")}
{box(f"<b>2019 caps: {pct(SALL['at_or_above'])} of firms are at or above the cap, and {pct(SALL['want_past_2019'])} would go past it with no limit. With the 2024 caps, about {pct(SALL['want_past_2024'])} would.</b>")}
{foot("EPS survey, 772 firms, 2019. “Would go past” = EPS workers + extra wanted with no limit &gt; cap.")}""",
      [("Title", '"You asked how many firms are at or near the cap, by size, under the 2019 and 2024 caps."'),
       ("Blue bars", f'"Blue is firms at or above the 2019 cap, {pct(SALL["at_or_above"])} overall. As you said, that is not small."'),
       ("Orange bars", f'"Orange adds what they say they would hire with no limit: {pct(SALL["want_past_2019"])} would go past the 2019 cap, at every size."'),
       ("Green bars", f'"Green applies the 2024 caps, which are much higher, to the same firms and answers. Then about {pct(SALL["want_past_2024"])} would go past. So after 2024 the legal cap may barely bind."'),
       ("If asked: how firms are above the cap", '"We can\'t fully explain it. Root industries may hire 20 percent more, and the public file doesn\'t show which firms those are. We\'ve asked the Ministry."')],
      on=(3,))

# ------------------------------------------------------------------ cap use
rows = [["Use of the 2019 cap", "Share of firms", "Would hire more with no limit"]]
for k, lab in [("under_half", "Under half"), ("half_to_cap", "Half to the cap"), ("at_or_above", "At or above the cap")]:
    rows.append([lab, pct(CU[k]["share_of_firms"]), pct(CU[k]["want_more"])])
write("nov10-capuse", f"""{h2("Firms far below the cap still want more: something else limits them")}
{row(col(cards([card(pct(SALL['cap_2019_use']), "of the cap is used, on average"), card(pct(SALL['want_more']), "of firms would hire more with no limit")]) + table(rows, [40, 25, 35], 26), 3),
     box("<b>If the cap held firms back,</b> firms far below it would not want more workers. They want more almost as often as firms at the cap. So most firms are limited by something else: the national quota, the points ranking, the 3–6 new permits per round, or their own demand. The survey cannot separate these; the Ministry records we requested can.", 2))}
{foot("EPS survey, 772 firms, 2019. Cap from Korean workers in Feb 2019; would hire more = Q9 &gt; 0.")}""",
      [("Title", f'"You also asked whether the caps bind at all, since firms use only {pct(SALL["cap_2019_use"])} of their cap on average."'),
       ("Table", f'"{pct(CU["under_half"]["share_of_firms"])} of firms use less than half their cap. If the cap were what limits firms, those firms should not want more. But {pct(CU["under_half"]["want_more"])} of them do, almost as many as at the cap, {pct(CU["at_or_above"]["want_more"])}."'),
       ("Box", f'"So for most firms something else limits them. That matches the model, where the quota limits plants, not the cap. And {pct(1 - SALL["want_more"])} of firms want no more workers at all."'),
       ("Why it matters", '"You said that if no one is constrained there is no paper. Under the 2019 caps there clearly is a constraint. Under the 2024 caps we need newer data."')],
      on=(3, 6))

# ------------------------------------------------------------------ wants
s101 = S["bins"]["101-300"]
write("nov10-wants", f"""{h2("How much do plants want? Far more in the model than the survey")}
{fig("fig_wants.png", 1664, 450, "EPS workers each plant has and wants, in the model and the survey, by Korean workers")}
{box(f"<b>With no limit, model demand is {C19['binding']['ratio_free_to_quota']:.1f} times what plants have; survey firms want {wanted_ratio:.2f} times.</b> At 101–300 Korean workers, the model wants {T19['101-300']['free_m']:.0f} and the survey {s101['wanted']:.0f}. Stated wants may be too low, but this gap suggests the model's EPS workers are too attractive.")}
{foot("2019 caps in both. Survey wants: EPS workers + extra wanted with no limit (Q9), so they may reflect current conditions.")}""",
      [("Title", '"Here is the same comparison in levels: what plants have and what they want. Log scale, 2019 caps in both."'),
       ("Left panel", f'"In the model, wanted EPS workers rise steeply with size, to about {T19["101-300"]["free_m"]:.0f} per plant at 101 to 300 Korean workers."'),
       ("Right panel", f'"In the survey, they barely rise: about {s101["wanted"]:.0f}. What plants have now is similar at small sizes, and lower in the model at large ones."'),
       ("Takeaway", '"You warned us not to get too worked up when the survey contradicts an assumption, and stated wants could be low. But this is a large gap. In the model, an EPS worker is a perfect substitute for a Korean worker at a lower cost, so large plants would replace all their Korean manual workers. Firms don\'t say that. So the model\'s demand is probably too high."'),
       ("If asked: what would fix it", '"We haven\'t tried. Productivity differences or EPS workers being imperfect substitutes could lower it, but you advised us to keep the model simple, so we want to discuss it first."')],
      on=(1, 2, 3))

# ------------------------------------------------------------------ quota
rows = [["Year", "E-9 quota, all sectors", "E-9 actually issued"],
        ["2023", "120,000", "Not in our sources"], ["2024", "165,000", "About 80,000 (a Dec 2024 projection)"],
        ["2025", "130,000", "Not in our sources"], ["2026", "80,000", "Not in our sources"]]
write("nov10-quota", f"""{h2("The real limit, cap or quota? The model assumes the quota")}
{row(col(table(rows, [14, 36, 50], 26), 3), box("<b>Evidence is mixed.</b> The 2024 quota may have been only half used, which would mean it did not bind. But in 2026, low-scoring firms were still put on a waiting list (대기번호), so permits can still be scarce.", 2))}
{box("<b>Our disclosure request to the Ministry</b> asks, by plant size and round: firms applying, workers requested, workers allocated, firms waitlisted, permits issued and arrivals, plus caps and actual E-9 workers. That separates the cap from the quota and covers plants that don't use EPS.")}
{foot("Sources: 이투데이 Dec 2024, 파이낸셜뉴스 Dec 2025 (quotas); 고용노동부 서울북부지청 notice, Sept 2026 (waiting list).")}""",
      [("Title", '"In the model the quota always binds. Theta adjusts until total EPS demand equals the quota. We looked into whether that is true."'),
       ("Table", '"These are the announced E-9 quotas. A December 2024 report projected about 80,000 for 2024, half of the 165,000 quota. That is a projection, across all sectors, and we don\'t yet have the final number."'),
       ("Right box", '"At the same time, the Ministry\'s 2026 notice says firms with low scores get a waiting number. So the quota may bind in some rounds and sectors but not others. We can\'t tell yet."'),
       ("Bottom box", '"As you advised, we used the formal disclosure process with the Ministry. Those tables would show whether the cap or the quota does the limiting, and at what size. The law gives them 10 days, extendable by 10."'),
       ("If asked: what if the quota does not bind", '"Then theta would be 1 and only the legal cap would limit plants, and that would change our experiment. With the 2024 caps few firms reach the cap. That is why this is on our list of questions for you."')],
      on=(3, 6))

# ------------------------------------------------------------------ margin
PRODTABLE = '<div style="display:flex; flex-direction:column; gap:8px"><p style="font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; font-weight:600; color:#1f2a3c">If an EPS worker does only 74% of a Korean worker\'s work, the same work costs w ÷ 0.74 ≈ 1.35·w:</p><table style="border-collapse:collapse; width:100%"><tr><th style="padding:8px 12px; border-bottom:2px solid #14213d; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; font-weight:600; color:#14213d; text-align:left">Core Koreans</th><th style="padding:8px 12px; border-bottom:2px solid #14213d; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; font-weight:600; color:#14213d; text-align:left; text-align:right">Korean manual</th><th style="padding:8px 12px; border-bottom:2px solid #14213d; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; font-weight:600; color:#14213d; text-align:left; text-align:right">EPS</th><th style="padding:8px 12px; border-bottom:2px solid #14213d; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; font-weight:600; color:#14213d; text-align:left">Cheaper</th></tr><tr><td style="padding:8px 12px; border-bottom:1px solid #d8dee8; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; color:#3d4756">7 (small plant)</td><td style="padding:8px 12px; border-bottom:1px solid #d8dee8; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; color:#3d4756; text-align:right">1.57·w</td><td style="padding:8px 12px; border-bottom:1px solid #d8dee8; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; color:#3d4756; text-align:right">1.35·w</td><td style="padding:8px 12px; border-bottom:1px solid #d8dee8; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; color:#3d4756; font-weight:600; color:#14213d">EPS</td></tr><tr><td style="padding:8px 12px; border-bottom:1px solid #d8dee8; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; color:#3d4756">150 (large plant)</td><td style="padding:8px 12px; border-bottom:1px solid #d8dee8; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; color:#3d4756; text-align:right">1.29·w</td><td style="padding:8px 12px; border-bottom:1px solid #d8dee8; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; color:#3d4756; text-align:right">1.35·w</td><td style="padding:8px 12px; border-bottom:1px solid #d8dee8; font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:22px; color:#3d4756; font-weight:600; color:#14213d">Korean</td></tr></table><p style="font-family:\'IBM Plex Sans\', Arial, sans-serif; font-size:20px; color:#5f6876">Employers rate EPS workers at 74–96% of a Korean worker, rising with experience (EPS survey, 2019).</p></div>'   # 74% productivity: cost of the same work, small vs large plant
write("nov10-margin", f"""{h2("Why large plants barely grow: their next worker is Korean")}
{row(col(fig("fig_permit.png", 960, 520, "Value of one permit by core Korean workers against the permit price"), 3),
     col(box(f"<b>1. With a limit,</b> a large plant fills its EPS permits and hires the rest as Koreans. Its next worker still costs w·(1 + premium), so the limit only saves money.", None, 26) +
         box(f"<b>2. With a price,</b> EPS costs w + p. Past about {cut:.0f} core Koreans a permit saves less than p, so plants stop using EPS.", None, 26) + PRODTABLE, 2))}
{foot("Saving from one permit = w × premium from (2). It falls with core Koreans and crosses p where w·ψ(1 + h)<sup>−ξ</sup> = p.")}""",
      [("Title", '"You expected large, productive plants to be held back, so removing the rule should make them grow. Here is why that does not happen in our model."'),
       ("Point 1", '"Large plants already hire Korean manual workers. Once their EPS permits are used, the next worker is Korean. So the limit doesn\'t change what the next worker costs; it only saves money on workers the plant would hire anyway."'),
       ("Chart", f'"The line is what one permit saves: the wage times the premium. It falls with core Koreans, because we assume recruiting is easier at large plants. The dashed line is the permit price. They cross at about {cut:.0f} core Koreans."'),
       ("Point 2", '"Past that point a permit is not worth its price, so large plants drop EPS. Only a middle band of plants uses it."'),
       ("Table", f'"What if EPS workers are less productive? Employers rate them at 74 to 96 percent of a Korean worker. At 74 percent, the same amount of work costs about {1 / 0.74:.2f} times the wage. That is still cheaper than a Korean manual worker at a small plant, {PREM(7):.2f}, but dearer than one at a large plant, {PREM(150):.2f}. So lower productivity would make large plants want EPS even less, which supports this result."')],
      on=(2, 3, 4))

# ------------------------------------------------------------------ top plant
TR = {r["label"]: r for r in TOP["rows"]}
rows = [["Plan for the top 1% plant", "Wage", "Core Koreans h", "Korean manual k", "EPS m", "Total"]]
for lab, key in [("Today's rule", "current rule, today's wage"), ("Price", "price, price-economy wage"),
                 ("Price, at today's wage", "price, today's wage"), ("No EPS at all, at today's wage", "no EPS, today's wage")]:
    r = TR[key]
    rows.append([lab, f"{r['w']:.3f}", num(r["h"]), num(r["k"]), num(r["m"]), num(r["total"])])
tc, tp = TR["current rule, today's wage"], TR["price, price-economy wage"]
wfall = 1 - tp["w"] / tc["w"]
write("nov10-top", f"""{h2("The top 1% plant drops EPS and barely changes size")}
{table(rows, [34, 12, 16, 16, 10, 12], 26, hi=(1,))}
{box(f"<b>At the same wage, the price plan is the same as having no EPS at all.</b> The plant grows from {tc['total']:.0f} to {tp['total']:.0f} workers only because the wage is {pct(wfall, 1)} lower with a price. Under today's rule it sits just past the 150-worker step, where its cap rises from 40 to 50, so the rule makes it slightly larger. EPS users get smaller on average ({REG['current']['users_size']:.1f} to {REG['price']['users_size']:.1f} workers) because large plants leave EPS.")}
{foot("Model, 2024 caps. Every row is the same plant: 99th percentile of manual-intensive productivity.")}""",
      [("Title", '"Here is the top 1 percent plant in detail."'),
       ("Rows 1 and 2", f'"Today it has {tc["m"]:.0f} EPS workers. With a price it has none and hires more Korean manual workers instead. It goes from {tc["total"]:.0f} to {tp["total"]:.0f} workers."'),
       ("Rows 3 and 4", '"Why does it grow at all? At today\'s wage its price plan is exactly its plan with no EPS. So EPS plays no part. The growth comes from the wage, which is lower with a price because fewer manual-intensive plants survive."'),
       ("Box", '"Under today\'s rule the plant sits just past the 150 cap step to get the larger cap. That is the size rule making it a little bigger: bunching."'),
       ("If asked: how precise are these sizes", '"Sizes sit on a grid with steps of a few percent, so 308 against 317 is about one grid step."')],
      on=(1, 3, 4))

# ------------------------------------------------------------------ three ways to share
c, p, f = "current", "price", "flat"
r_p, r_pf = net(REG, p) / QUOTA50, net(FIN, p) / QUOTA50F
r_f, r_ff = net(REG, f) / QUOTA50, net(FIN, f) / QUOTA50F
rows = [["", "Today's rule", "Price", "Free, equal limit"],
        ["Limit per plant", f"θ·q(h), θ = {C24['x']:.2f}", "None", f"{REG[f]['limit']:.1f} workers for every plant"],
        ["Who may use EPS", "1 ≤ h &lt; 300", "h ≥ 1", "h ≥ 1"],
        ["Cost of an EPS worker", "w", f"w + p, p = {REG[p]['price']:.2f}", "w"],
        ["What adjusts to use the quota", "θ", "p", "The limit"]]
write("nov10-split", f"""{h2("Three ways to share the same quota")}
{table(rows, [28, 24, 24, 24], 26)}
{box(f"<b>The price version changes two things at once:</b> it removes the size link and it charges for permits. The equal limit removes only the size link; permits stay free. Free permits with no limit are not possible: demand would be {b24['ratio_free_to_quota']:.1f} times the quota.")}
{foot("Same quota, parameters and grid in all three. The equal limit is new; it adds no feature to the model.")}""",
      [("Title", '"Last time\'s experiment changed two things at once. So we split it. Here are the three ways of sharing the same quota that we compare."'),
       ("Table", f'"Today each plant gets a share theta of its cap. With a price, any plant can buy permits at {REG[p]["price"]:.2f}. With an equal limit, permits are free and every plant gets the same {REG[f]["limit"]:.1f} workers."'),
       ("Box", '"The equal limit removes the size link but keeps permits free, so comparing the two tells us what the charge does."')],
      on=(3, 4))

# ------------------------------------------------------------------ results
rows = [["", "Today's rule", "Price", "Free, equal limit"],
        ["Net output, 24 × 11 grid (48 × 21)", "—", f"{pct(net(REG, p), 2, True)} ({pct(net(FIN, p), 2, True)})", f"{pct(net(REG, f), 2, True)} ({pct(net(FIN, f), 2, True)})"],
        ["Gross output, today = 100", "100", f"{gross(REG, p):.1f}", f"{gross(REG, f):.1f}"],
        ["Plants using EPS", pct(REG[c]["users"], 1), pct(REG[p]["users"], 1), pct(REG[f]["users"], 1)],
        ["EPS at plants with 0–5 Koreans", pct(small(REG, c)), pct(small(REG, p)), pct(small(REG, f))],
        ["Workers at a top 1% plant", f"{PT(c):.0f}", f"{PT(p):.0f}", f"{PT(f):.0f}"]]
write("nov10-split2", f"""{h2("A price raises net output; an equal limit raises gross output. Both gains are small")}
{table(rows, [34, 22, 22, 22], 26, hi=(0, 1))}
{box(f"<b>Against our kill line</b> (a tenth of the gain from a 50% larger quota): a price gives {r_p:.2f}–{r_pf:.2f}, at the line; an equal limit gives {r_ff:.2f}–{r_f:.2f}, below it. With an equal limit, {pct(small(REG, f))} of EPS workers go to plants with 0–5 Koreans.")}
{foot("Net output = gross output minus real costs (next slide). 24 × 11: calibration grid; 48 × 21: finer grid.")}""",
      [("Title", '"Here are the results for the three."'),
       ("Net and gross", f'"With a price, gross output falls to {gross(REG, p):.1f} but net output rises {pct(net(REG, p), 2)}. With an equal limit, gross output rises to {gross(REG, f):.1f}, as you expected, but net output rises only {pct(net(REG, f), 2)}, or {pct(net(FIN, f), 2)} on the finer grid."'),
       ("Other rows", f'"With an equal limit more plants use EPS and most permits go to the smallest plants. A top 1 percent plant barely changes size in any version."'),
       ("Box", f'"Both gains are small. A price is at our kill line and an equal limit is below it."')],
      on=(3, 4))

# ------------------------------------------------------------------ costs
W = {x["reg"]: x for x in WHY}
Y0 = W["current"]["Y"]
per = lambda reg, k: 100 * W[reg][k] / Y0
rows = [["Per 100 of today's gross output", "Today's rule", "Price", "Change"]]
for lab, k in [("Gross output", "Y"), ("− Korean manual premium", "recruit_premium"), ("− Fixed cost of using EPS", "eps_fixed"),
               ("− Fixed costs of running plants", "fixed"), ("− Entry costs", "entry"), ("= Net output", "net_Y")]:
    a, b = per("current", k), per("neutral", k)
    rows.append([lab, f"{a:.2f}", f"{b:.2f}", f"{b - a:+.2f}".replace("-", "−")])
ms = [W[r]["types"][1]["plants"] / sum(t["plants"] for t in W[r]["types"]) for r in ("current", "neutral")]
write("nov10-costs", f"""{h2("Where the net gain comes from: fewer costly manual-intensive plants")}
{row(col(table(rows, [40, 20, 20, 20], 26, hi=(3, 5)), 3),
     box(f"<b>With a price, gross output falls {100 - gross(REG, p):.1f} but costs fall more,</b> mostly the fixed costs of manual-intensive plants that close: they are {pct(ms[0], 1)} of plants today and {pct(ms[1], 1)} with a price, and each costs {W['current']['types'][1]['cf']:.2f} a year to run against {W['current']['types'][0]['cf']:.2f} for a light plant. So the size rule does keep some costly plants alive.", 2))}
{foot("Wages and permit payments are transfers, not costs. The premium is counted as a real cost.")}""",
      [("Title", '"So where does the net gain come from? Net output is gross output minus real costs."'),
       ("Table", '"With a price, gross output falls by 0.9. But costs fall by about 1.2, and the biggest part is the fixed costs of running plants."'),
       ("Box", '"Those are manual-intensive plants that close when they must pay for permits. Each is expensive to run. So the size rule does keep some costly plants alive. That is your original question, and the answer is yes, but the effect is small."'),
       ("If asked: what if the premium is just higher pay", '"Then it is a transfer to Korean workers, not a cost, and the gain would be smaller. That is one of the assumptions we want your view on."')],
      on=(5, 6))

# ------------------------------------------------------------------ premium
rows = [["Premium slope ξ", "ψ", "Plants stop using EPS past", "Net output", "Gross output", "Top 1% plant workers", "Top 1% EPS"]]
order = sorted(PR, key=lambda x: (abs(x["psi"] - 1.599) < 1e-6, -x["xi"]))
hi = []
for i, x in enumerate(order):
    tag = " (ours)" if abs(x["xi"] - D["params"]["xi"]) < 1e-9 else (" (version 5)" if abs(x["psi"] - 1.599) < 1e-6 else "")
    if "ours" in tag:
        hi.append(i)
    rows.append([f"{x['xi']:.2f}{tag}", f"{x['psi']:.2f}", f"{x['cutoff']:.0f}", pct(x["net"], 2, True), pct(x["gross"], 1, True),
                 f"{x['current']['total'][2]:.0f} → {x['neutral']['total'][2]:.0f}", f"{x['current']['m'][2]:.0f} → {x['neutral']['m'][2]:.0f}"])
ng, xg = min(x["net"] for x in PR), max(x["net"] for x in PR)
write("nov10-premium", f"""{h2("Does the premium drive the result? The direction holds")}
{table(rows, [22, 8, 18, 13, 13, 16, 10], 24, hi=hi)}
{box(f"<b>In all six, removing the size rule lowers gross output and raises net output ({pct(ng, 2, True)} to {pct(xg, 2, True)}), and large plants barely change size.</b> A higher, flatter premium keeps EPS at large plants, but they swap Korean workers for EPS rather than grow. This is the perfect-substitutes assumption in equation (1).")}
{foot("Not recalibrated: read the direction, not the levels. ψ keeps the premium at 10 core Koreans fixed, except version 5.")}""",
      [("Title", '"The premium is the assumption everything seems to depend on, and we can\'t measure it directly yet. So we varied it, holding everything else at our calibration."'),
       ("Table", '"Each row is a different slope. The flatter the premium, the larger a plant can be and still want EPS. Our value stops at about 28 core Koreans. The last row uses version 5\'s higher, flatter premium: about 400."'),
       ("Key columns", '"But gross output falls in all six rows. And a top 1 percent plant barely changes size, even when it keeps many EPS workers, as in the version 5 row."'),
       ("Why", '"The reason is equation (1). Manual work is k plus m, so EPS and Korean manual workers are perfect substitutes. A large plant replaces Korean workers rather than expanding, because the premium at large plants is small."'),
       ("Honest limit", '"These rows are not recalibrated, so the levels don\'t match the targets. They show direction only. To really test this we would need to measure the premium by size, or relax the perfect-substitutes assumption, and we would like your view on whether that is worth it."')],
      on=(1, 2, 4))

# ------------------------------------------------------------------ bumpy
GRIDS = [("24 × 11; 320", (24, 11)), ("48 × 21; 320 (last time)", (48, 21)), ("96 × 41; 320", (96, 41)), ("96 × 41; 1,280", (96, 41, 1280, 200))]
g1, g3, c3 = gk("neutral", 48, 21), gk("neutral", 96, 41, 1280, 200), gk("current", 96, 41, 1280, 200)
c1 = gk("current", 48, 21)
flips = lambda g: int(np.sum(np.sign(np.diff(np.log(g["density"])))[1:] != np.sign(np.diff(np.log(g["density"])))[:-1]))
write("nov10-bumpy", f"""{h2("The bumpy no-rule line was grid error, as you suspected")}
{row(col(fig("fig_bumpy.png", 1000, 541, "Plant density without the size rule, on last time's grid and on finer grids"), 3),
     box(f"<b>Cause:</b> on last time's grid, productivity moves in steps of about 5%. Plant size moves about 3 times as much, so one step is wider than the 8% histogram bins, and some bins are left empty.<br><br><b>On finer grids</b> the line turns direction {flips(g3)} times instead of {flips(g1)}.", 2))}
{foot("Finer grids: distributions at the 48 × 21 prices, not re-solved.")}""",
      [("Title", '"You said the no-size-rule line should be smoother and to check for approximation error. You were right."'),
       ("Chart", '"Blue is last time\'s line. Orange uses a finer grid for productivity and plant size. It is much smoother."'),
       ("Box", '"Productivity moves in steps of about 5 percent, and plant size moves about three times as much, so a step is wider than our 8 percent bins. That makes the bumps."')],
      on=(1,))

# ------------------------------------------------------------------ bunching holds
rows = [["Grid: productivity; size points", "Roughness: no rule", "Today's rule", "Pile-up past cap steps: no rule", "Today's rule"]]
for lab, g in GRIDS:
    n_, c_ = gk("neutral", *g), gk("current", *g)
    rows.append([lab, f"{n_['roughness']:.2f}", f"{c_['roughness']:.2f}", step_range(n_), step_range(c_)])
write("nov10-bunch", f"""{h2("The bunching at the cap steps is real: it holds on every grid")}
{table(rows, [30, 16, 14, 24, 16], 26)}
{box(f"<b>Under today's rule, plants pile up just past each cap step, at 1.5 to 2 times the density just below, on every grid. With no size rule the ratio stays near or below 1.</b> The no-rule line gets smooth ({g1['roughness']:.2f} to {g3['roughness']:.2f}); today's rule levels off near {c3['roughness']:.1f}, because its jumps are the cap steps.")}
{foot("Pile-up: density just past a cap step ÷ just before. Roughness: s.d. of 2nd difference of log density.")}""",
      [("Title", '"So is the bunching we showed also grid error? No."'),
       ("Last columns", '"The pile-up just past each cap step is 1.5 to 2 times the density just below it under today\'s rule, on every grid. With no size rule it stays near or below 1."'),
       ("Roughness", f'"The no-rule line gets smooth on finer grids, from {g1["roughness"]:.2f} to {g3["roughness"]:.2f}. Today\'s rule levels off near {c3["roughness"]:.1f}, because its jumps are real: they are the cap steps."'),
       ("If asked: does the +0.33 change on this grid", '"These runs hold prices fixed, so they check the shape, not the gain. The +0.33 percent is on the 24 by 11 grid; on 48 by 21 it is +0.37 percent."')],
      on=(3,))

# ------------------------------------------------------------------ next
write("nov10-next", f"""{h2("What we learned, and where we would like your advice")}
{row(col(f'''<h3 style="font-family:{SERIF}; font-size:36px; font-weight:600; color:{NAVY}">What we learned</h3>''' + bullets([f"Who uses EPS is set mostly by the plant-type share, not the cap", "In the model the quota does the limiting; in the survey, something other than the cap limits most firms", "Large plants barely grow without the size rule; the small gain comes from fewer costly plants", f"The gain is small: {pct(net(FIN, f), 2, True)} to {pct(net(FIN, p), 2, True)}, depending on how permits are shared"]), 1),
     col(f'''<h3 style="font-family:{SERIF}; font-size:36px; font-weight:600; color:{NAVY}">Questions for you</h3>''' + bullets(["Should the paper focus on the 2019 caps, the 2024 caps or both?", "Is the gain large enough to continue, or should we refocus on the quota?", "Which comparison is right: a price, an equal limit or something else?", "Should EPS workers be less attractive in the model, for example by adding the survey's dorm and meal costs?"]), 1))}
{box("<b>For Nov 24:</b> recalibrate to the sourced targets, put the cap and eligibility on all Korean workers (h + k), and follow up on the Ministry request.")}
{foot("Results today: v6 calibration, no model changes since Nov 3.")}""",
      [("Left", '"To sum up: who uses EPS comes mostly from the plant-type share. The quota, not the cap, does the limiting in the model, and something other than the cap limits most firms in the survey. Large plants barely grow without the size rule. And the gain is small."'),
       ("Right", '"We have four questions. Should we focus on the 2019 caps, which clearly bind, or the 2024 caps, which may not? Is this gain enough to continue, or should we refocus on the quota? Which comparison is right? And should we make EPS workers less attractive in the model? Firms in the survey want far fewer than the model says, and adding the dorm and meal costs the survey records would be a simple way to do it."'),
       ("Bottom", '"For next week we will recalibrate to the sourced targets, fix the cap to count all Korean workers, and follow up with the Ministry."'),
       ("If asked: does the size rule keep weak plants alive", f'"Slightly. Today\'s rule keeps about {100 * (REG["current"]["firms"] / REG["price"]["firms"] - 1):.1f} percent more plants than a price would, mostly manual-intensive plants that are costly to run."'),
       ("Close", '"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."')],
      on=())
print("slides", {k: PG[k] for k in ORDER}, "total", TOTAL)
