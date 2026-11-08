"""Writes the Nov 10 slides into the deck folder from the baseline results.
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

ORDER = ["nov10-cover", "nov10-refresh", "nov10-answers", "nov10-who", "nov10-size", "nov10-policy", "nov10-scale", "nov10-binding", "nov10-wants",
         "nov10-quota", "nov10-margin", "nov10-split", "nov10-premium", "nov10-bumpy", "nov10-next"]
FIRST, TOTAL = 39, 38 + len(ORDER)
PG = {k: FIRST + i for i, k in enumerate(ORDER)}
SERIF, SANS = "'Source Serif 4', Georgia, serif", "'IBM Plex Sans', Arial, sans-serif"
NAVY, INK, BODY, MUTED, RUST, STEEL = "#14213d", "#1f2a3c", "#3d4756", "#5f6876", "#a8432c", "#2f5d8a"
LOGO = "/_blob/921ccfeb3c9f6d9c3ed1cc4a5be8bdd4"
PRESENTER = {s: n for n, ss in [("Sara", ["nov10-cover", "nov10-refresh", "nov10-answers"]), ("Donny", ["nov10-who", "nov10-size", "nov10-policy", "nov10-scale"]), ("Julian", ["nov10-binding", "nov10-wants", "nov10-quota"]), ("Benjamin", ["nov10-margin", "nov10-split", "nov10-premium", "nov10-bumpy"]), ("Mimi", ["nov10-next"])] for s in ss}
HANDOVER = { "nov10-answers": "Donny will now show who uses EPS in the model, and the policy functions.", "nov10-scale": "Julian will now show whether the cap binds, in the survey and in the model.", "nov10-quota": "Benjamin will now explain why large plants barely grow, and the checks we ran.", "nov10-bumpy": "Mimi will sum up and ask our questions." }
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
<p style="position:absolute; top:376px; left:128px; width:1664px; font-family:{SANS}; font-size:36px; line-height:1.4; color:#c9d1de">November 10, 2026 · Who uses EPS, who is held back, and what removing the size rule really does</p>
<h2 style="position:absolute; top:490px; left:128px; width:1664px; font-family:{SERIF}; font-size:52px; color:#f7f5f0"><b>Research Topic: Does tying EPS workers to plant size keep weak plants alive, and how much would output change if the same quota ignored plant size?</b></h2>
<p style="position:absolute; bottom:96px; left:128px; width:1664px; font-family:{SANS}; font-size:26px; line-height:1.5; color:#c9d1de">Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo<br>ISA6327 Topics in Macroeconomics · Prof. Sewon Hur · November 10, 2026</p>
{presenter("nov10-cover", True)}{page("nov10-cover", True)}{logo()}{notes([("Title", '"Good afternoon. Last week you asked us to understand the baseline model before running more experiments. So today nothing in the model has changed. We\'ll show how it behaves."'),
 ("Plan", '"We start with a short refresher, then cover who uses EPS, whether the limit binds, and why removing the size rule does not make large plants grow. We also ran the checks you asked for."')])}
</section>
''')

# ------------------------------------------------------------------ refresher
rows = [["Equation", "In words"],
        ["(1) y = s·(h^ρ + λₜ ℓ^ρ)^(α/ρ), ℓ = k + m", "Core Koreans h and manual work ℓ make output; λₜ differs by plant type"],
        ["(2) cost of k = w·(1 + ψ(1 + h)^−ξ)", "Korean manual workers cost a premium, smaller at larger plants"],
        ["(3) m ≤ θ·q(h), cost ≈ w", "Current rule: EPS workers m are limited by a share θ of the legal cap q(h)"],
        ["(4) cost of m = w + p", "No size rule: same quota, shared by a permit price p"],
        ["(5) Exit if β(1−δ)E[V(s′)] &lt; 0; Σν V = cₑ", "Plants exit when the future is not worth it; free entry sets the wage w"],
        ["(6) Σμ(h + k) = N, Σμ m = M", "Korean labor N and the quota M are fixed, and both markets clear"]]
write("nov10-refresh", f"""{h2("Refresher: the question, the model and the data")}
{row(col(f'''<h3 style="font-family:{SERIF}; font-size:36px; font-weight:600; color:{NAVY}">The question</h3>
<p style="font-family:{SANS}; font-size:26px; line-height:1.4; color:{BODY}">EPS ties each plant's foreign workers to its Korean workers. Does that keep weak plants alive, and how much would output change if the same quota ignored size?</p>
<h3 style="font-family:{SERIF}; font-size:36px; font-weight:600; color:{NAVY}">The data</h3>
<p style="font-family:{SANS}; font-size:26px; line-height:1.4; color:{BODY}">MDIS census: plant sizes. KDI–World Bank EPS survey: 772 manufacturers, EPS users only. Lee, Peri and Yang: closures after the 2020–21 stop. Ministry records: requested.</p>''', 2),
     col(f'<h3 style="font-family:{SERIF}; font-size:36px; font-weight:600; color:{NAVY}">The model</h3>' + table(rows, [46, 54]), 3))}
{foot("A Hopenhayn (1992) model with two plant types: light and manual-intensive. Calibrated to 8 targets; unchanged since Nov 3.")}""",
      [("Question", '"A quick reminder. Korea\'s Employment Permit System, EPS, limits each plant\'s foreign workers according to its number of Korean workers. We ask whether that keeps weak plants alive, and how much output would change if the same quota ignored size."'),
       ("Model", '"It\'s a Hopenhayn model. A plant has productivity s and hires core Koreans h and manual workers. Manual work can be done by Koreans, k, or EPS workers, m. Korean manual workers cost a premium that is smaller at larger plants. Under the current rule, a plant can have up to a share theta of its legal cap. In the no-size-rule experiment, plants pay a price p instead."'),
       ("Data", '"The census gives plant sizes, the survey covers firms that use EPS, and Lee, Peri and Yang give closures after the 2020–21 stop in new arrivals. We\'ve asked the Ministry for the rest."'),
       ("If asked: how many parameters", '"13 parameters and 8 targets, so it is not exactly identified target by target. Some come from the structure and the search over them."')], band=False)

# ------------------------------------------------------------------ answers
rows = [["What you asked", "Short answer", "Slides"],
        ["Who uses EPS? Is the 10.7% assumed?", f"Manual-intensive plants, {pct(who['users_manual'] / who['manual'])} of them. The {pct(who['users'], 1)} follows mostly from their share, which we calibrate", f"{PG['nov10-who']}"],
        ["Do users match the data? What is the EPS share?", "Same pattern by size, but too many very small users. Three EPS shares, defined", f"{PG['nov10-size']}"],
        ["Which plants are at their optimal scale?", f"Light plants, {pct(who['light'])} of plants. {pct(b24['users_want_more'])} of EPS users are below it, held back by the quota", f"{PG['nov10-policy']}–{PG['nov10-scale']}"],
        ["Is the cap binding?", f"{pct(SALL['at_or_above'])} at or above the 2019 cap, about {pct(SALL['want_past_2024'])} past the 2024 cap. Firms far below the cap want more almost as often", f"{PG['nov10-binding']}–{PG['nov10-quota']}"],
        ["Why does gross output fall, and why do users get smaller?", "Large plants' next worker is Korean, so a permit only saves money; with a price they stop using EPS", f"{PG['nov10-margin']}–{PG['nov10-premium']}"],
        ["Is the bumpy line an error?", "Yes, mostly. It is smooth on finer grids, and the bunching result does not change", f"{PG['nov10-bumpy']}"]]
write("nov10-answers", f"""{h2("Your questions from last week, and the short answers")}
{table(rows, [32, 58, 10])}
{foot(f"Correction: 36.9% is the average EPS share across EPS firms, not the share in the economy. Slide {PG['nov10-size']} defines all three.")}""",
      [("Title", '"Here is what you asked last week, with our short answers. The next slides show each one."'),
       ("Correction", '"First, some corrections to what we told you. The EPS share of 36.9 percent is the average, across firms using EPS, of EPS workers divided by that firm\'s workers. It is not the share in the economy, which is 5.5 percent, or the share of firms using EPS, which is about 10 percent. Slide ' + str(PG["nov10-size"]) + ' shows all three, in the model and the data."'),
       ("Correction on the cap", '"We also said firms can go above the cap by request, by 3 to 6 workers. We have no source for that. In Dong, Lee and Yang, 3 to 6 is the maximum number of new permits. We\'ve asked the Ministry for the rule."'),
       ("Correction on the survey", '"On slides 31 and 37 we said every user wants more. In the model that is 98 percent."')],
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
{box(f"<b>So {pct(who['users'], 1)} of plants use EPS mostly because we calibrate {pct(who['manual'], 1)} to be manual-intensive.</b> The cap does not decide this. We have not measured that share directly, so we've asked the Ministry for plants by share of manual workers.")}
{foot("Model, 2024 caps. Only about 0.1% of plants are manual-intensive and ineligible, because they have 300+ core Koreans.")}""",
      [("Title", '"You asked why only about 10 percent of plants use EPS. The answer is the two plant types."'),
       ("Table", f'"{pct(who["light"])} of plants are light: they have almost no use for manual work, so they hire no manual workers and none uses EPS. The other {pct(who["manual"])} are manual-intensive, and {pct(who["users_manual"] / who["manual"])} of those use EPS."'),
       ("Why box", '"An EPS worker costs less than a Korean manual worker because it saves the premium. A plant uses EPS if that saving beats the fixed cost. Light plants would not use EPS even if it were free."'),
       ("Bottom box", '"So the 10 percent mostly comes from a number we calibrate, not from the cap. That is a weakness: nothing measures that share directly. It is in our Ministry request."'),
       ("If asked: is 89 percent with no manual workers realistic", '"Probably not literally. It is a two-type simplification. Real plants have some manual work. We need the data to say how far off it is."'),
       ("If asked: why hire EPS workers if they cost the same and are less productive", f'"Because Korean manual workers only come at a higher price, and the premium in equation 2 is that price. A Korean manual worker costs about {PREM(7):.1f} times the wage at a plant with 7 core Koreans and {PREM(150):.1f} times at 150. Employers rate EPS workers at 74 to 96 percent of a Korean worker. Even at 74 percent, an EPS worker costs about {1 / 0.74:.2f} times the wage per unit of work: still cheaper at small plants, but not at large ones. So lower productivity would make large plants want EPS even less, which supports our result."')],
      on=(1, 2))

# ------------------------------------------------------------------ users by size
keys = [("0-10", "Under 10"), ("10-20", "10–19"), ("20-50", "20–49"), ("50-100", "50–99"), ("100-200", "100–199"), ("200-300", "200–299")]
rows = [["Total workers", "Share of EPS firms: model", "Survey", "EPS share at those firms: model", "Survey"]]
for k, lab in keys:
    rows.append([lab, pct(ubt[k]["share_of_users"]), pct(sbt[k]["share_of_firms"]), pct(ubt[k]["eps_share"]), pct(sbt[k]["eps_share"])])
write("nov10-size", f"""{h2("Do model users match the data? The shape, but not the small end")}
{row(col(table(rows, [18, 24, 12, 32, 14], 24), 3), box(f"<b>Fits:</b> the EPS share falls with size in both, from about half at the smallest firms to about 5%. We only targeted the average.<br><br><b>Misses:</b> too many EPS firms under 10 workers ({pct(ubt['0-10']['share_of_users'])} vs {pct(sbt['0-10']['share_of_firms'])}), too few at 20–49 ({pct(ubt['20-50']['share_of_users'])} vs {pct(sbt['20-50']['share_of_firms'])}).", 2))}
{table([["What “EPS share” means", "Data", "Model"],
        ["Average, across EPS firms, of EPS workers ÷ that firm's workers", "36.9%", pct(FIT["eps_share_users"], 1)],
        ["EPS workers ÷ all manufacturing workers", "5.5%", pct(C24["summary"]["eps_share"], 1)],
        ["Share of plants that use EPS", "About 10%", pct(who["users"], 1)]], [62, 19, 19])}
{foot("2019 caps, firms under 300 workers. 36.9%: Lee, Peri and Yang, Table 3. 5.5% and 10%: our targets, sources being checked.")}""",
      [("Title", '"You asked us to check that the model\'s EPS users look like the data\'s. Here they are by total workers, under the 2019 caps, which is when the survey was done."'),
       ("Right columns", '"The EPS share falls with size in both, from about half at the smallest firms to around 5 percent at the largest. We only targeted the average, so this shape is a check."'),
       ("Left columns", f'"The miss is in where users are. The model has {pct(ubt["0-10"]["share_of_users"])} of EPS firms under 10 workers, against {pct(sbt["0-10"]["share_of_firms"])} in the survey, and too few at 20 to 49."'),
       ("If asked: why the miss", '"We don\'t know yet. The model\'s plant sizes under 10 come from a target for the share of very small plants. The survey covers EPS users only, so we can\'t test this on non-users."'),
       ("Bottom table", f'"You asked us to define the EPS share. There are three. First, the average across EPS firms of each firm\'s EPS workers divided by its workers: 36.9 percent in Lee, Peri and Yang, {pct(FIT["eps_share_users"], 1)} in the model, measured the same way. Second, EPS workers as a share of all manufacturing workers: 5.5 percent, which sets the quota in the model. Third, the share of plants that use EPS: about 10 percent, and {pct(who["users"], 1)} in the model."'),
       ("If asked: where do 5.5 and 10 percent come from", '"They are our calibration targets. We are still checking their sources and will confirm them."')],
      on=(3,))

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
labs = ["0-5", "6-10", "11-30", "31-50", "51-100", "101-300", "300+"]
rows = [["Korean workers", "Workers now", "With no limit", "Times larger", "EPS now", "EPS wanted"]]
for b in labs:
    r = T[b]
    rows.append([b.replace("-", "–"), num(r["size_manual"]), num(r["free_size_manual"]), f"{r['free_size_manual'] / r['size_manual']:.1f}", num(r["m_manual"]), num(r["free_m"])])
write("nov10-scale", f"""{h2("Who is held back: almost every user, by the quota, not the cap")}
{cards([card(pct(b24['users_want_more']), "of users are below their optimal scale"), card(pct(b24['users_at_limit']), "are at θ × cap (2024 caps)"), card(pct(b24['users_at_legal_cap']), "reach the legal cap", True), card(f"{b24['ratio_free_to_quota']:.1f}×", "the quota: demand with no limit")])}
{table(rows, [22, 16, 18, 16, 14, 14])}
{foot("Manual-intensive plants; light plants are already at optimal scale. No limit = free permits, not an equilibrium.")}""",
      [("Title", '"You asked who is constrained, and where they would be without the limit."'),
       ("Cards", f'"Optimal scale means the size a plant would choose with no limit, at today\'s prices. Light plants, {pct(who["light"])} of all plants, are already there. {pct(b24["users_want_more"])} of EPS users would hire more, so they are below it, and {pct(b24["users_at_limit"])} are at their limit. But that limit is theta times the cap, and theta is {C24["x"]:.2f}. No plant reaches the legal cap. In the model, the quota does the limiting, and the legal cap decides how it is shared."'),
       ("Table", f'"With no limit, plants would be {min(ratios):.1f} to {max(ratios):.1f} times larger. But total demand would be {b24["ratio_free_to_quota"]:.1f} times the quota, so this can\'t happen at the same quota. It is a measure of how much plants want EPS workers."'),
       ("If asked: 82 percent versus 98 percent", f'"The others sit just below their limit but would still hire more. Part of this may be the grid for manual workers, and we haven\'t checked. Under the 2019 caps, {pct(b19["users_at_limit"])} are at the limit."'),
       ("If asked: who else is below optimal scale", f'"The {pct(who["non_manual_ineligible"], 1)} of plants that are manual-intensive but have 300 or more core Koreans, so they are not eligible for EPS."'),
       ("If asked: is theta realistic", '"Theta is a simple stand-in for rationing. It gives every plant the same share of its cap. Real rationing uses a score and a cut-off, and we kept the model simple as you advised."')],
      on=(3, 6))

# ------------------------------------------------------------------ binding
write("nov10-binding", f"""{h2("Is the cap binding? Yes for 2019 caps, barely for 2024 caps")}
{fig("fig_binding.png", 1664, 420, "Share of survey firms at or above the cap and past it under 2019 and 2024 caps, by Korean workers")}
{box(f"<b>2019 caps: {pct(SALL['at_or_above'])} of firms are at or above the cap and {pct(SALL['want_past_2019'])} would go past it. With 2024 caps, {pct(SALL['want_past_2024'])} would.</b> Firms use {pct(SALL['cap_2019_use'])} of their cap on average and {pct(SALL['under_half'])} use under half, yet those below half want more workers almost as often ({pct(CU['under_half']['want_more'])}) as firms at the cap ({pct(CU['at_or_above']['want_more'])}). So for most firms, the cap is not what holds them back.")}
{foot("EPS survey: 772 firms, 2019, users only. “Would go past” = EPS workers + extra wanted with no limit &gt; cap.")}""",
      [("Title", '"You asked how many firms are at or near the cap, by size, under the 2019 and 2024 caps."'),
       ("Blue bars", f'"Blue is firms at or above the 2019 cap, {pct(SALL["at_or_above"])} overall. As you said, that is not small."'),
       ("Orange bars", f'"Orange adds what they say they would hire with no limit: {pct(SALL["want_past_2019"])} would go past the 2019 cap, and that holds at every size."'),
       ("Green bars", f'"Green applies the 2024 caps, which are much higher, to the same firms and answers. Now about {pct(SALL["want_past_2024"])} would go past. So after the 2024 change, the legal cap may barely bind."'),
       ("Box", f'"You also asked whether the caps bind at all, since firms use only {pct(SALL["cap_2019_use"])} of their cap on average and {pct(SALL["under_half"])} use less than half. If the cap were what limits firms, firms far below it should not want more. But {pct(CU["under_half"]["want_more"])} of them do, almost as many as at the cap, {pct(CU["at_or_above"]["want_more"])}. So for most firms something else limits them, like the quota, the points ranking or the limit on new permits per round. That matches the model, where the quota limits plants, not the cap. And {pct(1 - SALL["want_more"])} of firms want no more workers at all: they are at their optimal scale."'),
       ("Why it matters", '"This matters for our question. You said that if no one is constrained there is no paper. Under the 2019 caps there clearly is a constraint. Under the 2024 caps we need newer data. Firms may also have wanted more after 2019, and the quota or the score may still limit them."'),
       ("If asked: then what limits them", '"The survey can\'t tell us. The candidates are the national quota, the points ranking and the 3 to 6 new permits per round. The Ministry tables we requested would separate them."'),
       ("If asked: how firms are above the cap", '"We can\'t fully explain it. Root industries may hire 20 percent more, and the public file doesn\'t show which firms those are. We\'ve asked the Ministry for the rules and the counts."')],
      on=(3,))

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
pa, pn = REG["current"]["policy"], REG["price"]["policy"]
write("nov10-margin", f"""{h2("Why large plants barely grow: their next worker is Korean")}
{row(col(fig("fig_permit.png", 960, 520, "Value of one permit by core Korean workers against the permit price"), 3),
     col(box(f"<b>1. With a limit,</b> a large plant fills its EPS permits and hires the rest as Koreans. The limit only saves money; the next worker still costs w·(1 + premium).", None, 24) +
         box(f"<b>2. With a price,</b> EPS costs w + p. Past about {cut:.0f} core Koreans a permit saves less than p, so plants stop using EPS.", None, 24) +
         box(f"<b>3. So the top 1% plant</b> drops from {pa['m'][2]:.0f} EPS workers to {pn['m'][2]:.0f} and goes from {pa['total'][2]:.0f} to {pn['total'][2]:.0f} workers. EPS users get smaller on average, {REG['current']['users_size']:.1f} to {REG['price']['users_size']:.1f} workers, because large plants stop using EPS.", None, 24), 2))}
{foot("For a plant that still hires Koreans, a permit is worth the same at any productivity; it depends only on core Koreans, through (2).")}""",
      [("Title", '"You expected large, productive plants to be held back, so removing the rule should make them grow. Here is why that does not happen in our model."'),
       ("Point 1", '"Large plants hire Korean manual workers. Once its EPS permits are used, a large plant\'s next worker is Korean. So the limit doesn\'t change what the next worker costs. It only saves money on workers the plant would hire anyway, so it doesn\'t change the plant\'s size much."'),
       ("Chart", f'"The blue line is what one permit is worth: the wage times the premium. It falls with core Koreans, because we assume recruiting is easier at large plants. The orange line is the permit price. They cross at about {cut:.0f} core Koreans."'),
       ("Point 2", f'"Past that point the permit is not worth its price, so large plants drop EPS. Only a middle band of plants uses it."'),
       ("Point 3", f'"A top 1 percent plant goes from {pa["m"][2]:.0f} EPS workers to none and stays about the same size. You noticed that the average EPS user gets smaller, from {REG["current"]["users_size"]:.1f} to {REG["price"]["users_size"]:.1f} workers. That is because large plants leave the group of EPS users, not because they shrink."'),
       ("If asked: so why does gross output fall", f'"With a price, permits move away from small plants, which lose cheap workers and produce less, and large plants swap EPS workers for Koreans instead of growing. So gross output falls to {gross(REG, "price"):.1f}. Costs fall more, from {costs(REG, "current"):.1f} to {costs(REG, "price"):.1f}, so net output rises. In our model the size rule mainly raises costs rather than limiting output, because EPS and Korean manual workers are perfect substitutes."'),
       ("If asked: what if EPS workers are less productive", f'"Employers rate them at 74 to 96 percent of a Korean worker. At 74 percent, EPS work costs about {1 / 0.74:.2f} times the wage per unit, more than a Korean manual worker at a large plant, about {PREM(150):.2f}. So large plants would want EPS even less, and our result would get stronger."'),
       ("If asked: isn\'t the premium the key assumption", f'"Yes, it is, and we don\'t measure it directly. Slide {PG["nov10-premium"]} tests other values."')],
      on=(2, 3, 4))

# ------------------------------------------------------------------ split
c, p, f = "current", "price", "flat"
r_p, r_pf = net(REG, p) / QUOTA50, net(FIN, p) / QUOTA50F
r_f, r_ff = net(REG, f) / QUOTA50, net(FIN, f) / QUOTA50F
rows = [["", "Current rule", "Price, no size link", "Free, equal limit (new)", "Free, no limit"],
        ["How permits are shared", f"θ = {C24['x']:.2f} of cap", f"p = {REG[p]['price']:.2f}", f"{REG[f]['limit']:.1f} workers each", "Not an equilibrium"],
        ["Net output (finer grid)", "—", f"{pct(net(REG, p), 2, True)} ({pct(net(FIN, p), 2, True)})", f"{pct(net(REG, f), 2, True)} ({pct(net(FIN, f), 2, True)})", "—"],
        ["Gross output, current = 100", "100", f"{gross(REG, p):.1f}", f"{gross(REG, f):.1f}", "—"],
        ["Costs, in the same units", f"{costs(REG, c):.1f}", f"{costs(REG, p):.1f}", f"{costs(REG, f):.1f}", "—"],
        ["Plants using EPS", pct(REG[c]["users"], 1), pct(REG[p]["users"], 1), pct(REG[f]["users"], 1), "—"],
        ["EPS at plants with 0–5 Koreans", pct(small(REG, c)), pct(small(REG, p)), pct(small(REG, f)), "—"],
        ["Workers at a top 1% plant", f"{PT(c):.0f}", f"{PT(p):.0f}", f"{PT(f):.0f}", f"{f99[3]:.0f}"]]
write("nov10-split", f"""{h2("Splitting the experiment: the size link and the permit charge")}
{table(rows, [32, 16, 19, 20, 13], 24, hi=(1, 2))}
{box(f"<b>Gross output rises with free, equal limits, as you expected, but only by {gross(REG, f) - 100:.1f}%.</b> Permits go to many small plants, so costs rise and the net gain is smaller. Large plants grow only with far more workers. Against a 50% larger quota: {r_p:.2f}–{r_pf:.2f} with a price, {r_ff:.2f}–{r_f:.2f} with an equal limit.")}
{foot("Same quota except the last column; keeping eligibility changes little. Costs: fixed, entry, recruiting, EPS.")}""",
      [("Title", '"Last week\'s no-size-rule experiment changed two things at once: it removed the size link, and it charged for permits. So we split them. This is a new experiment, with no new features in the model."'),
       ("New column", f'"Permits stay free, the quota stays the same, and every plant gets the same limit, {REG[f]["limit"]:.1f} workers. The limit is set so the quota is used."'),
       ("Gross row", f'"With a price, gross output falls to {gross(REG, p):.1f}. With a free, equal limit, it rises to {gross(REG, f):.1f}. So your expectation that gross output rises does hold for this version. But it comes from sharing permits differently, and we can\'t say the charge alone explains it."'),
       ("Other rows", f'"With an equal limit, more plants use EPS, and {pct(small(REG, f))} of EPS workers are at plants with 5 or fewer Koreans. That means more plants survive, and costs rise. So the net gain falls to {pct(net(REG, f), 2, True)}, or {pct(net(FIN, f), 2, True)} on the finer grid."'),
       ("Last row", f'"A top 1 percent plant doesn\'t grow in either version. Only with no limit does it reach {f99[3]:.0f}, and that takes {b24["ratio_free_to_quota"]:.1f} times the quota. At the same quota, more for large plants means less for small ones."'),
       ("Kill line", f'"Our kill line was 0.10 of the gain from a 50 percent larger quota. With a price we are at {r_p:.2f} to {r_pf:.2f}. With an equal limit, {r_ff:.2f} to {r_f:.2f}, below the line."')],
      on=(3, 4))

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
GRIDS = [("24 × 11; 320", (24, 11)), ("48 × 21; 320 (last week)", (48, 21)), ("96 × 41; 320", (96, 41)), ("96 × 41; 1,280", (96, 41, 1280, 200))]
rows = [["Grid: productivity; size points", "Roughness: no rule", "Current rule", "Step ratio: no rule", "Current rule"]]
for lab, g in GRIDS:
    n_, c_ = gk("neutral", *g), gk("current", *g)
    rows.append([lab, f"{n_['roughness']:.2f}", f"{c_['roughness']:.2f}", step_range(n_), step_range(c_)])
g1, g3, c3 = gk("neutral", 48, 21), gk("neutral", 96, 41, 1280, 200), gk("current", 96, 41, 1280, 200)
flips = lambda g: int(np.sum(np.sign(np.diff(np.log(g["density"])))[1:] != np.sign(np.diff(np.log(g["density"])))[:-1]))
write("nov10-bumpy", f"""{h2("The bumpy no-rule line was grid error; the bunching result holds")}
{row(col(fig("fig_bumpy.png", 800, 433, "Plant density without the size rule, on last week's grid and on finer grids"), 1),
     col(table(rows, [34, 18, 15, 18, 15], 24) + box(f"<b>You were right.</b> On finer grids the no-rule line turns direction {flips(g3)} times, not {flips(g1)}. The current-rule line stays jagged, as real cap steps should. Step ratios barely move.", None, 24), 1))}
{foot("Finer grids: distributions at the 48 × 21 prices, not re-solved. Roughness: standard deviation of the second difference of log density.")}""",
      [("Title", '"You said the no-size-rule line should be smoother, and to check for approximation error. Last week we blamed the grid, but both lines used the same grid, so that was not a real answer. So we tested it."'),
       ("Chart", '"Blue is last week\'s line. Orange uses a finer grid for productivity and for plant size. It is much smoother."'),
       ("Why", '"On last week\'s grid, productivity moves in steps of about 5 percent. Plant size moves about three times as much, so a step is wider than our 8 percent histogram bins. That makes bumps. So you were right: this was approximation error."'),
       ("Table", f'"Roughness measures how much the line jumps between bins. For the no-rule line it falls from {g1["roughness"]:.2f} to {g3["roughness"]:.2f}. For the current rule it stays around {c3["roughness"]:.1f}, because its jumps are real: they are the cap steps."'),
       ("Last columns", '"The step ratios barely move. Under the current rule plants pile up past each step, at about 1.6 to 2. With no size rule the ratio stays near or below 1. So the bunching result holds on every grid."'),
       ("If asked: does the +0.33 change on this grid", '"We haven\'t solved the full equilibrium on the finest grid. On the 48 by 21 grid it is +0.37 percent. These runs hold prices fixed, so they check the shape of the distribution, not the gain."')],
      on=(1, 3))

# ------------------------------------------------------------------ next
write("nov10-next", f"""{h2("What we learned, and where we would like your advice")}
{row(col(f'''<h3 style="font-family:{SERIF}; font-size:36px; font-weight:600; color:{NAVY}">What we learned</h3>''' + bullets([f"The {pct(who['users'], 1)} of users mostly comes from the plant type share", "The quota does the limiting; the legal cap only shares it out", "Large plants barely grow, at any premium slope we tried", f"The gain is small: {pct(net(FIN, f), 2, True)} to {pct(net(FIN, p), 2, True)}, depending on how permits are shared"]), 1),
     col(f'''<h3 style="font-family:{SERIF}; font-size:36px; font-weight:600; color:{NAVY}">Questions for you</h3>''' + bullets(["Should the paper focus on the 2019 caps, the 2024 caps or both?", "Is the gain large enough to continue, or should we refocus on the quota?", "Which comparison is right: a price, an equal limit or something else?", "Is relaxing perfect substitutes worth the added complexity?"]), 1))}
{box("<b>Next:</b> follow up on the Ministry request, and contact Prof. Lee and Prof. Yang about the 2021 survey. Then measure the plant type share and the premium by size where the data allow.")}
{foot("No model changes since Nov 3.")}""",
      [("Left", '"To sum up: the 10 percent of users mostly comes from the plant type share. The quota does the limiting. Large plants barely grow. And the gain is small and depends on how permits are shared."'),
       ("Right", '"We have four questions. First, should the paper focus on the 2019 caps, which clearly bind, or the 2024 caps, which may barely bind? Second, is this gain enough to continue, or should we refocus on the quota, which matters much more? Third, which comparison is the right one? And fourth, you told us not to complicate the model, so is relaxing perfect substitutes worth it?"'),
       ("Bottom", '"Next we follow up on the Ministry request, contact Prof. Lee and Prof. Yang, and measure what we can."'),
       ("If asked: does the size rule keep weak plants alive", f'"Only slightly. The current rule keeps about {100 * (REG["current"]["firms"] / REG["price"]["firms"] - 1):.1f} percent more plants than a price would, and the exit rate is {100 * REG["current"]["exit_rate"]:.2f} against {100 * REG["price"]["exit_rate"]:.2f} percent. An equal limit would keep {100 * (REG["flat"]["firms"] / REG["current"]["firms"] - 1):.1f} percent more plants than today. So the gain comes mainly from lower costs, not from weak plants exiting."'),
       ("Close", '"Thank you. We worked with the AI assistant Claude (Anthropic), used for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy."')],
      on=())
print("slides", {k: PG[k] for k in ORDER}, "total", TOTAL)
