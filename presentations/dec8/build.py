"""Dec 8 final presentation (draft): writes the slides into a deck folder from the v9 results and data files.
Usage: build.py <deck root> <first page number>. Image URLs come from blobs.json. Every number is read from a file.
Audience: people who do not know the topic. No presenter labels (to be decided by the team)."""
import json, os, sys

ROOT, FIRST = sys.argv[1], int(sys.argv[2])
SL = os.path.join(ROOT, "project/slides")
HERE = os.path.dirname(os.path.abspath(__file__))
E = os.path.join(HERE, "../../hopenhayn_project/eps_model/")
R = json.load(open(E + "results_v9.json"))
CFG = json.load(open(E + "targets_v9.json"))
H = json.load(open(os.path.join(HERE, "../../bunching/cap_use_hist.json")))
PE = json.load(open(os.path.join(HERE, "../../bunching/premium_evidence.json")))
SB = json.load(open(E + "baseline/survey_binding.json"))
ML = json.load(open(os.path.join(HERE, "mlfs_2026h1.json")))
RV = json.load(open(E + "v8_review.json"))
BLOB = json.load(open(os.path.join(HERE, "blobs.json")))
P, C = R["params"], R["changes"]
B24, B19 = R["moments_2024"], R["moments_2019"]
RUNS = R["runs"]

ORDER = ["dec8-cover", "dec8-answer",
         "dec8-shortage", "dec8-eps", "dec8-caps", "dec8-question", "dec8-approach",
         "dec8-data", "dec8-fact-users", "dec8-fact-capuse", "dec8-fact-hiring", "dec8-fact-wages",
         "dec8-model-map", "dec8-model-prod", "dec8-model-premium", "dec8-model-rules", "dec8-model-plant", "dec8-model-eq", "dec8-experiments",
         "dec8-params", "dec8-fit", "dec8-valid-hist", "dec8-valid-size", "dec8-valid-who",
         "dec8-res-equal", "dec8-res-why", "dec8-res-tilt", "dec8-res-price", "dec8-res-mech", "dec8-res-quota", "dec8-res-summary", "dec8-robust",
         "dec8-learn", "dec8-limits", "dec8-next", "dec8-refs"]
TOTAL = FIRST - 1 + len(ORDER)
PG = {k: FIRST + i for i, k in enumerate(ORDER)}
SERIF, SANS = "'Source Serif 4', Georgia, serif", "'IBM Plex Sans', Arial, sans-serif"
NAVY, INK, BODY, MUTED, RUST, STEEL = "#14213d", "#1f2a3c", "#3d4756", "#5f6876", "#a8432c", "#2f5d8a"
LOGO = "/_blob/921ccfeb3c9f6d9c3ed1cc4a5be8bdd4"
EQS = ["(1) y = s·(h^ρ + λₜ ℓ^ρ)^(α/ρ), ℓ = k + m", "(2) cost of k = w·(1 + ψ(1 + h)^−ξ); of m = w", "(3) Eligible (share e): m ≤ q(h + k), h + k &lt; 300",
       "(4) Price: m at w + p; equal limit: m ≤ L", "(5) Exit if β(1−δ)E[V(s′)] &lt; 0; Σν V = cₑ", "(6) Σμ(h + k) = N, Σμ m = M"]


def pct(x, d=0, sign=False):
    v = round(100 * x, d) + 0.0
    if v == 0:
        return f"{0:.{d}f}%"
    return f"{v:{'+' if sign else ''}.{d}f}%".replace("-", "−")


def page(i, dark=False):
    return (f'<p style="position:absolute; right:128px; bottom:40px; width:160px; font-family:{SANS}; font-size:24px; '
            f'text-align:right; color:{"#c9d1de" if dark else "#8a94a6"}">{PG[i]}/{TOTAL}</p>')


def logo():
    return f'<img src="{LOGO}" alt="Logo" style="position:absolute; right:8px; bottom:952.01px; width:112.01px; height:114.78px">'


def foot(t):
    return f'<p style="position:absolute; bottom:40px; left:128px; width:1440px; font-family:{SANS}; font-size:22px; color:{MUTED}">{t}</p>'


def h2(t):
    return f'<h2 style="font-family:{SERIF}; font-size:50px; font-weight:600; line-height:1.15; color:{NAVY}">{t}</h2>'


def h3(t):
    return f'<h3 style="font-family:{SERIF}; font-size:32px; font-weight:600; color:{NAVY}">{t}</h3>'


def kicker(t):
    return f'<p style="font-family:{SANS}; font-size:22px; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; color:{RUST}">{t}</p>'


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


def box(t, size=25):
    return (f'<p style="padding:20px 28px; font-family:{SANS}; font-size:{size}px; line-height:1.4; color:{INK}; '
            f'background:#e8eef6; border-left:6px solid {STEEL}; border-radius:12px">{t}</p>')


def card(big, small, hi=False):
    st = f"background:#fbefea; border:3px solid {RUST}" if hi else "background:#f4f7fb; border:1px solid #d8dee8"
    return (f'<div style="display:flex; flex-direction:column; gap:8px; padding:24px 28px; {st}; border-radius:12px">'
            f'<p style="font-family:{SERIF}; font-size:58px; font-weight:600; line-height:1.1; color:{RUST if hi else NAVY}">{big}</p>'
            f'<p style="font-family:{SANS}; font-size:25px; line-height:1.3; color:{BODY}">{small}</p></div>')


def cards(items):
    return f'<div style="display:grid; gap:24px; grid-template-columns:{" ".join(["1fr"] * len(items))}">{"".join(items)}</div>'


def row(*parts):
    return f'<div style="display:flex; flex-direction:row; gap:32px">{"".join(parts)}</div>'


def col(html, flex=1):
    return f'<div style="display:flex; flex-direction:column; gap:20px; flex:{flex}">{html}</div>'


def fig(name, w, h, alt):
    return f'<img src="{BLOB[name]}" alt="{alt}" style="width:{w}px; height:{h}px; object-fit:contain">'


def bullets(items, size=26):
    return f'<ul style="font-family:{SANS}; font-size:{size}px; line-height:1.4; color:{BODY}">{"".join(f"<li>{i}</li>" for i in items)}</ul>'


def eqbox(e, size=30):
    return f'<p style="font-family:{SERIF}; font-size:{size}px; line-height:1.35; color:{NAVY}; padding:14px 24px; background:#f4f7fb; border-radius:12px">{e}</p>'


def notes(blocks):
    text = "<br><br>".join(f"[{a}]<br>{b}" for a, b in blocks)
    assert len(text) <= 4000, len(text)
    return f"<aside>{text}</aside>"


def write(i, body, blocks, on=None):
    band = on is not None
    html = (f'<section id="{i}" data-transition="fade" style="display:flex; flex-direction:column; gap:24px; padding:120px 128px {220 if band else 140}px; background:#ffffff">\n'
            f'{body}{eqs(on) if band else ""}{page(i)}{logo()}{notes(blocks)}\n</section>\n')
    open(os.path.join(SL, i + ".html"), "w").write(html)


def get(d, key):
    for part in key.split("."):
        d = d[part]
    return d


# ------------------------------------------------------------------ numbers
e24, e19 = R["e_2024"], R["e_2019"]
price, eq24, eq19, noeps = C["price_vs_2024"], C["equal_vs_2024"], C["equal_vs_2019"], C["no_eps_vs_2024"]
q125 = C["quota"]["1.25"]
pr_run = RUNS["price"]
p_price, w_price = pr_run["x"], pr_run["w"]
L24 = RUNS["equal_2024"]["x"]
PREM = lambda h: 1 + P["psi"] * (1 + h) ** -P["xi"]
manual_ratio = P["lamB"] ** (1 / (1 - P["rho"]))
hist = RUNS["hist_2019"]
plans = RUNS["plans"]
byh_t, byh_p = RUNS["today_2024"]["by_h"], RUNS["price"]["by_h"]
G = B24["groups"]
CAP24 = [["Korean workers", "1–10", "11–50", "51–100", "101–150", "151–200", "201–299", "300+"],
         ["2024 cap", "n + 10", "min(30, 2n)", "35", "40", "50", "60", "not eligible"]]
CAP19 = [["Korean workers", "1–5", "6–10", "11–30", "31–50", "51–100", "101–150", "151–200", "201–299"],
         ["2019 cap", "5", "7", "10", "12", "15", "20", "25", "30"]]
surv_tot = SB["by_total_workers"]
pe = PE["by_korean_workers"]

# ------------------------------------------------------------------ 1. cover
open(os.path.join(SL, "dec8-cover.html"), "w").write(f'''<section id="dec8-cover" data-transition="fade" style="background:{NAVY}">
<h1 style="position:absolute; top:150px; left:128px; width:1664px; font-family:{SERIF}; font-size:84px; font-weight:600; line-height:1.1; color:#f7f5f0">Who should get Korea's<br>guest workers?</h1>
<p style="position:absolute; top:370px; left:128px; width:1664px; font-family:{SANS}; font-size:36px; line-height:1.4; color:#c9d1de">Plant size, access and output under the Employment Permit System</p>
<h2 style="position:absolute; top:480px; left:128px; width:1664px; font-family:{SERIF}; font-size:46px; color:#f7f5f0"><b>Research question: Does tying EPS workers to plant size distort which plants operate and grow, and how much would output change if the same quota were allocated differently?</b></h2>
<p style="position:absolute; bottom:96px; left:128px; width:1664px; font-family:{SANS}; font-size:26px; line-height:1.5; color:#c9d1de">Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo<br>ISA6327 Topics in Macroeconomics · Prof. Sewon Hur · December 8, 2026</p>
{page("dec8-cover", True)}{logo()}{notes([("Title", '"Good afternoon. Korea brings in low-skilled foreign workers through the Employment Permit System. Our project asks a simple question: who should get those workers? In particular, does tying them to plant size, as the law does, cost the economy output?"')])}
</section>
''')

# ------------------------------------------------------------------ 2. the answer first
write("dec8-answer", f"""{kicker("Our answer, in one slide")}{h2("The size rule barely matters; access and the quota do")}
{cards([card(pct(eq24['net_Y'], 2), "change in net output if every eligible plant got the <b>same cap</b>, with no link to size"),
        card(pct(price['net_Y'], 2, True), "if the same quota went to <b>any plant willing to pay a permit price</b>", True),
        card(pct(q125['net_Y'], 1, True), "if the quota were <b>25% larger</b> under today's rules")])}
{box("Why: in our model the legal caps rarely bind. What holds plants back is whether they get permits at all, and how many permits exist. The price gain depends on how costly it is for small plants to hire Korean manual workers.")}
{foot("Model of Korean manufacturing calibrated to 2024 data; same total EPS workers in the first two experiments. Draft: numbers update with the Ministry data.")}""",
      [("Why start here", '"We start with the answer so you can follow the logic. Three numbers."'),
       ("Cards", f'"If we remove the link between plant size and the EPS cap, output does not change. If we let any plant buy permits at a price, output rises by about {pct(price["net_Y"], 1)}. And if Korea simply had 25 percent more EPS workers, output would rise by about {pct(q125["net_Y"], 1)}."'),
       ("Box", '"The rest of the talk explains why: the caps rarely bind, so the real constraints are access and the size of the quota."')])

# ------------------------------------------------------------------ 3. background: shortage
write("dec8-shortage", f"""{kicker("Background")}{h2("Korean manufacturers, especially small ones, cannot find manual workers")}
{fig("fig_hiring.png", 1664, 540, "Hiring difficulty by size: survey and Ministry establishment survey")}
{box(f"Among EPS firms that tried to hire Koreans, {pct(PE['share_with_difficulty'])} had difficulty, and {pct(PE['reason_no_applicants'])} of those said the main reason was <b>no applicants</b>; only {pct(PE['reason_labor_cost'])} said labour costs.", 24)}
{foot("Left: KDI–World Bank EPS survey 2019 (772 manufacturers), Q4 and Q6. Right: 고용노동부, 직종별사업체노동력조사 2026 상반기, table 1-1, manufacturing.")}""",
      [("Left", f'"Our firm survey asks how many Korean production and simple-labour workers each firm planned to hire last year, and how many it actually hired. The smallest firms left {pct(pe["1-5"]["unfilled_manual_aggregate"])} of those jobs unfilled; firms with more than 50 Korean workers only {pct(pe["51-plus"]["unfilled_manual_aggregate"])}."'),
       ("Right", '"Official data for all manufacturing plants say the same: the share of jobs plants need but cannot fill falls from 4 percent at the smallest plants to 2 percent at plants with 100 to 299 workers."'),
       ("Box", '"And the reason is not pay: firms say there are simply no applicants."')])

# ------------------------------------------------------------------ 4. EPS
write("dec8-eps", f"""{kicker("Background")}{h2("The Employment Permit System (EPS) fills that gap with foreign workers")}
{row(col(bullets([
    "Since 2004, Korea admits low-skilled foreign workers on <b>E-9 visas</b> for fixed-term contracts",
    f"Manufacturing employs most of them: <b>219,507</b> E-9 workers at the end of 2024, <b>{pct(CFG['quota']['eps_share_of_workers'], 1)}</b> of manufacturing workers",
    "Workers cannot choose their employer; the government matches them to firms",
    "The government sets a yearly <b>quota</b>; firms apply, are ranked by points, and many wait"], 26)),
     col(bullets([
    "A firm may hire E-9 workers only if it is <b>eligible</b> (fewer than 300 workers, or small capital)",
    "Even then, it may hire only up to a <b>legal cap</b> that depends on its number of insured Korean workers",
    f"{pct(CFG['targets'][4]['value'])} of manufacturing plants employ E-9 workers"], 26)))}
{foot("Sources: e-나라지표 1501 (고용노동부/한국고용정보원), tables 150106–150107, end of 2024; MDIS business census 2024; eps.go.kr.")}""",
      [("Left", '"EPS is Korea\'s main channel for low-skilled foreign workers. Most work in manufacturing, about 5 percent of all manufacturing workers. They cannot change employers freely: the government matches them. Each year there is a quota, and firms compete for it through a points system."'),
       ("Right", '"Firms face two limits: they must be eligible, and they may hire only up to a legal cap that grows with their number of Korean workers. That second rule is what our project is about."')])

# ------------------------------------------------------------------ 5. caps
write("dec8-caps", f"""{kicker("The rule we study")}{h2("The legal cap rises with plant size, but much more slowly than the plant")}
{table(CAP24, [20, 11, 14, 11, 11, 11, 11, 11], 24)}
{table(CAP19, [20, 10, 10, 10, 10, 10, 10, 10, 10], 24)}
{box("A plant with 5 Korean workers may hire up to 15 EPS workers (3 for every Korean worker); a plant with 200 may hire only 50 (1 for every 4). <b>The rule favours small plants.</b> If small plants are less productive, tying permits to size could keep weak plants alive and hold strong plants back.", 24)}
{foot("Manufacturing caps by insured Korean workers n: eps.go.kr (2024); Lee, Peri and Yang (2026), Table 4 (2019).")}""",
      [("Tables", '"These are the legal caps. In 2024 a plant with 1 to 10 Korean workers may hire its number of Koreans plus 10; above that the cap grows in steps, up to 60. The 2019 caps, which our survey firms faced, were much lower."'),
       ("Box", '"Look at the ratio: small plants may hire three EPS workers per Korean worker, large ones one per four. Economists usually worry about rules like this: size-dependent policies can keep unproductive small firms alive. That is the worry we test."')])

# ------------------------------------------------------------------ 6. question and literature
write("dec8-question", f"""{kicker("Research question")}{h2("Does the size rule cost output, and would another allocation do better?")}
{row(col(h3("What we ask") + bullets([
    "Does tying EPS workers to plant size distort which plants operate and how large they grow?",
    "With the <b>same number</b> of EPS workers, how much would output change if they were allocated differently?",
    "How does that compare with simply having more EPS workers?"], 25)),
     col(h3("What is known") + bullets([
    "Size-dependent rules can lower output by distorting firm size: Guner, Ventura and Xu (2008); Garicano, Lelarge and Van Reenen (2016)",
    "EPS firms more exposed to the 2020–21 stop in inflows closed more often: Lee, Peri and Yang (2026)",
    "<b>Missing:</b> a model of the whole manufacturing sector to ask what a different allocation would do"], 25)))}""",
      [("Left", '"Three questions: does the size rule distort plants, how much would a different allocation of the same workers change output, and how does that compare with more workers?"'),
       ("Right", '"The literature tells us size-dependent rules can be costly, and that EPS matters for whether firms survive. What is missing is a model that can run the counterfactual: same workers, different rule. That is our contribution."')])

# ------------------------------------------------------------------ 7. approach
write("dec8-approach", f"""{kicker("Approach")}{h2("Four steps: facts, a model, calibration, experiments")}
{table([["Step", "What we do", "Slides"],
        ["1. Facts", "Document who uses EPS, how much of their cap they use, and how hard it is to hire Koreans", f"{PG['dec8-data']}–{PG['dec8-fact-wages']}"],
        ["2. Model", "Build a model of manufacturing plants that enter, hire, grow and exit, with the EPS rules", f"{PG['dec8-model-map']}–{PG['dec8-experiments']}"],
        ["3. Calibration", "Choose parameters so the model matches Korean data, then check it on data it was not fitted to", f"{PG['dec8-params']}–{PG['dec8-valid-who']}"],
        ["4. Experiments", "Keep the same EPS workers, change the rule; compare output and welfare", f"{PG['dec8-res-equal']}–{PG['dec8-robust']}"]], [16, 70, 14], 25)}""",
      [("Table", '"We proceed in four steps. First, facts from the data. Second, a model built to match those facts. Third, we calibrate it to Korea and check it against things it was not fitted to. Fourth, we change the rule and compare."')])

# ------------------------------------------------------------------ 8. data
write("dec8-data", f"""{kicker("Facts")}{h2("Our data")}
{table([["Source", "What it covers", "What we use it for"],
        ["MDIS business census 2024", "All 509,467 manufacturing plants", "Plant sizes"],
        ["KDI–World Bank EPS survey 2019", "772 manufacturers that use EPS (Dong, Lee and Yang 2024)", "Cap use, EPS share by size, hiring difficulty, wages, costs"],
        ["Lee, Peri and Yang (2026)", "761 EPS firms, 2020–21", "EPS share and size of EPS firms; closures"],
        ["Ministry of Employment and Labor (e-나라지표)", "E-9 workers and workplaces, 2024", "Size of the EPS workforce; plants using EPS"],
        ["Statistics Korea, business demography", "Manufacturing enterprises, 2024", "Exit rate"],
        ["Ministry establishment survey (직종별사업체노동력조사)", "All establishments, 2026 H1", "Labour shortages by plant size"],
        ["Ministry disclosure request (pending)", "EPS workplaces by size, caps, applications, exits", "Updates targets and checks"]], [32, 34, 34], 22)}
{foot("Survey and census microdata stay outside our repository; the scripts that build every number are in it.")}""",
      [("Table", '"We combine the census for plant sizes, a firm-level EPS survey, the closure evidence from Lee, Peri and Yang, official EPS statistics and exit rates, and an official establishment survey on labour shortages. We have also requested Ministry data by plant size, which will update the targets."')])

# ------------------------------------------------------------------ 9. fact: users
st = surv_tot
write("dec8-fact-users", f"""{kicker("Fact 1")}{h2("Few plants use EPS, mostly small ones, and they rely on it heavily")}
{cards([card(pct(CFG['targets'][4]['value']), "of manufacturing plants employ E-9 workers"),
        card(pct(st['0-10']['share_of_firms']), "of EPS firms have fewer than 10 workers"),
        card(f"{pct(st['0-10']['eps_share'])} → {pct(st['200-300']['eps_share'])}", "EPS share of workers, from firms under 10 to firms of 200–299")])}
{box("EPS matters most at the small end of manufacturing: small EPS firms rely on foreign workers for about half their workforce.", 25)}
{foot("40,766 workplaces with E-9 workers / 509,467 census plants (2024); KDI–World Bank EPS survey 2019 (total workers = Korean + EPS).")}""",
      [("Cards", '"Only 8 percent of manufacturing plants use EPS. Those that do are mostly small: four in ten have fewer than 10 workers. And small EPS firms rely heavily on it: about half their workers are EPS workers, against 6 percent at firms of 200 to 299."')])

# ------------------------------------------------------------------ 10. fact: cap use
write("dec8-fact-capuse", f"""{kicker("Fact 2")}{h2("Most EPS firms are below their legal cap, yet many want more workers")}
{cards([card(pct(H['median']), "of its legal cap: what the median EPS firm uses"),
        card(pct(H['at_or_above_cap']), "of EPS firms are at or above their cap"),
        card(pct(SB['all']['want_more']), "of EPS firms would hire more EPS workers if they could", True)])}
{box("If the cap held firms back, firms at the cap would want more and firms below it would not. Instead, firms far below their cap want more almost as often: " + f"{pct(SB['by_cap_use']['under_half']['want_more'])} of firms below half their cap, against {pct(SB['by_cap_use']['at_or_above']['want_more'])} of firms at or above it. <b>Something other than the cap limits most firms: access to permits.</b>", 24)}
{foot("KDI–World Bank EPS survey 2019, 772 firms; caps from listed Korean workers (2019 schedule). Wanting more: Q9.")}""",
      [("Cards", '"The median EPS firm uses only 60 percent of its legal cap. Only 18 percent are at or above it. Yet 44 percent say they would hire more EPS workers if they could."'),
       ("Box", '"If the cap were the problem, firms at the cap would be the ones wanting more. But firms far below the cap want more almost as often. So the binding limit is not the cap; it is getting permits at all. Keep this fact in mind: it is the heart of our results."')])

# ------------------------------------------------------------------ 11. fact: hiring
write("dec8-fact-hiring", f"""{kicker("Fact 3")}{h2("The smaller the plant, the harder it is to hire Korean manual workers")}
{table([["Korean workers at the firm", "1–5", "6–10", "11–30", "31–50", "51+"],
        ["Planned Korean manual hires left unfilled"] + [pct(pe[k]["unfilled_manual_aggregate"]) for k in ("1-5", "6-10", "11-30", "31-50", "51-plus")],
        ["Planned Korean core hires left unfilled"] + [pct(pe[k]["unfilled_core_aggregate"]) for k in ("1-5", "6-10", "11-30", "31-50", "51-plus")]], [34, 13, 13, 13, 13, 14], 26)}
{box("Manual jobs are much harder to fill than core jobs (managers, office staff), and much harder at small plants. This is the main reason a foreign worker is worth more to a small plant than to a large one.", 25)}
{foot("KDI–World Bank EPS survey 2019, Q4: Korean workers planned vs hired last year; manual = production + elementary jobs, core = managers, professionals, clerical.")}""",
      [("Table", '"Our survey splits planned hiring by occupation. Small firms leave more than half their planned Korean manual hires unfilled; large firms about a tenth. Core jobs are much easier to fill at every size."'),
       ("Box", '"So an EPS worker is worth most to a small plant: it fills a job that would otherwise stay empty. This difficulty is a key ingredient of our model."')])

# ------------------------------------------------------------------ 12. fact: wages
write("dec8-fact-wages", f"""{kicker("Fact 4")}{h2("Small plants do not pay Koreans more; the difficulty shows up as empty jobs")}
{table([["Korean workers at the firm", "1–5", "6–10", "11–30", "31–50", "51+"],
        ["Korean monthly wage ÷ EPS monthly wage (median)"] + [f"{pe[k]['wage_ratio_korean_to_eps_median']:.2f}" for k in ("1-5", "6-10", "11-30", "31-50", "51-plus")]], [40, 12, 12, 12, 12, 12], 26)}
{box("If small plants paid Koreans a premium, the ratio would be higher at small plants. It is flat. So the extra cost of a Korean manual worker at a small plant is not higher pay but <b>unfilled positions, recruiting effort and lost output</b>. We model it as a real cost.", 25)}
{foot("KDI–World Bank EPS survey 2019, Q13: average monthly wage of Korean and EPS workers at each firm.")}""",
      [("Table", '"Korean workers earn about 12 percent more than EPS workers, and that gap is the same at every firm size."'),
       ("Box", '"This matters for how we model the difficulty. It is not that small plants pay more; it is that jobs stay empty. So in the model it is a real cost to the plant, not a transfer to the worker. We come back to this assumption at the end."')])

# ------------------------------------------------------------------ 13. model map
step = lambda t, d: (f'<div style="flex:1; padding:20px 24px; background:#f4f7fb; border:1px solid #d8dee8; border-radius:12px">'
                     f'<p style="font-family:{SERIF}; font-size:28px; font-weight:600; color:{NAVY}">{t}</p>'
                     f'<p style="font-family:{SANS}; font-size:22px; line-height:1.35; color:{BODY}">{d}</p></div>')
arrow = f'<p style="font-family:{SANS}; font-size:44px; color:{STEEL}; align-self:center">→</p>'
write("dec8-model-map", f"""{kicker("Model")}{h2("The model in one picture")}
<div style="display:flex; flex-direction:row; gap:12px">{step("1. Entry", "A new plant draws its type (light or manual-intensive), its productivity, and whether it is EPS-eligible")}{arrow}{step("2. Hiring", "It hires core Korean workers, and does manual work with Korean or EPS workers, within the EPS rules")}{arrow}{step("3. Production", "It produces and pays wages, the extra cost of Korean manual workers, and fixed costs")}{arrow}{step("4. Exit", "It stays if the future is worth it; otherwise it closes and new plants enter")}</div>
{box("<b>Markets close the model:</b> the Korean wage adjusts so all Korean workers are employed; the share of eligible plants adjusts so the EPS quota is used. We compare long-run (steady-state) economies.", 25)}
{foot("Hopenhayn (1992) model of plant dynamics, extended with two plant types, a Pareto productivity tail and the EPS rules.")}""",
      [("Steps", '"Here is the model in four steps. A new plant learns its type, its productivity and whether it may use EPS. It hires workers within the rules, produces, pays its costs, and decides whether to stay. Plants that close are replaced by new ones."'),
       ("Box", '"Two prices close the model: the wage, which clears the Korean labour market, and the share of eligible plants, which makes sure the EPS quota is exactly used. We compare long-run economies, before and after a policy change."')], on=())

# ------------------------------------------------------------------ 14. production
write("dec8-model-prod", f"""{kicker("Model")}{h2("What a plant produces, and with whom")}
{eqbox("y = s·(h<sup>ρ</sup> + λ<sub>t</sub> ℓ<sup>ρ</sup>)<sup>α/ρ</sup>, &nbsp;ℓ = k + m", 32)}
{bullets([
    "<b>s</b>: productivity, a permanent part (Pareto tail) times a part that moves each year",
    "<b>h</b>: core Korean workers (managers, office, skilled staff)",
    "<b>ℓ</b>: manual work, done by Korean manual workers <b>k</b> or EPS workers <b>m</b>, one for one",
    f"<b>λ</b>: weight on manual work: {P['lamA']:.3f} for light plants, {P['lamB']:.2f} for manual-intensive plants",
    f"<b>α = {P.get('alpha', 0.6916):.2f}</b> &lt; 1: each extra worker adds a little less"], 26)}
{foot("Two plant types drawn at entry: light (most plants; little manual work) and manual-intensive (the plants that can use EPS).")}""",
      [("Equation", '"A plant combines core Korean workers with manual work. Manual work can be done by a Korean or an EPS worker, one for one. Light plants barely need manual work; manual-intensive plants need a lot. Productivity differs across plants, with a few very productive ones."')], on=(1,))

# ------------------------------------------------------------------ 15. premium
write("dec8-model-premium", f"""{kicker("Model")}{h2("Korean manual workers cost more at small plants")}
{eqbox("cost of a Korean manual worker = w·(1 + ψ(1 + h)<sup>−ξ</sup>); &nbsp;cost of an EPS worker = w, plus a fixed c<sub>m</sub>", 30)}
{table([["Core Korean workers h", "0", "7", "28", "150"], ["Cost of a Korean manual worker ÷ wage"] + [f"{PREM(x):.2f}" for x in (0, 7, 28, 150)]], [44, 14, 14, 14, 14], 26)}
{bullets(["The extra cost captures Fact 3: small plants cannot fill manual jobs with Koreans",
          "It is a <b>real cost</b> (empty jobs, recruiting), not pay (Fact 4)",
          f"Calibrated: ψ = {P['psi']:.2f}, ξ = {P['xi']:.2f}. An EPS worker saves this extra cost, so EPS is worth most to small plants"], 25)}""",
      [("Equation", '"Hiring a Korean manual worker costs a plant more than the wage, and the smaller the plant the more it costs. At a plant with no core staff it is 2.7 times the wage; at a plant with 150 core workers about 1.1."'),
       ("Why", '"This is how the model captures the facts: small plants struggle to fill manual jobs, and the cost is empty jobs, not higher pay. An EPS worker costs the wage, so it saves exactly this extra cost."')], on=(2,))

# ------------------------------------------------------------------ 16. rules
write("dec8-model-rules", f"""{kicker("Model")}{h2("The EPS rules in the model")}
{eqbox("If eligible: &nbsp;m ≤ q(h + k), &nbsp;only if h ≥ 1 and h + k &lt; 300. &nbsp;If not eligible: m = 0", 30)}
{bullets([
    f"<b>Who is eligible:</b> a random share e of new plants, regardless of type or productivity. It stands in for the points ranking and waiting lists (Fact 2: access, not the cap, limits most firms)",
    f"<b>The share adjusts</b> until total EPS use equals the quota: e = {pct(e24)} of entrants under the 2024 caps, {pct(e19)} under 2019",
    "<b>The cap</b> q follows the law: 2024 or 2019 schedule, counted on all Korean workers h + k"], 26)}
{foot("2024 caps for today's economy; 2019 caps when we compare with the 2019 survey and the 2020–21 shock.")}""",
      [("Equation", '"An eligible plant may hire EPS workers up to its legal cap, counted on all its Korean workers, as the law does. A plant that is not eligible hires none."'),
       ("Eligibility", f'"Who is eligible is random: about {pct(e24)} of new plants. That captures the fact that access, not the cap, is what limits firms. The share is not chosen by us: it adjusts until the quota is used."')], on=(3, 6))

# ------------------------------------------------------------------ 17. plant problem
write("dec8-model-plant", f"""{kicker("Model")}{h2("Each plant's decisions")}
{eqbox("Each year: &nbsp;π(s) = max<sub>h, ℓ, m</sub> &nbsp;output − wages − extra cost of Korean manual workers − EPS fixed cost − operating cost", 27)}
{eqbox("Value: &nbsp;V(s) = π(s) + value of staying; &nbsp;stay if β(1 − δ)·E[V(s′)] is worth more than closing", 27)}
{eqbox("Entry: &nbsp;new plants enter until the expected value of entering equals the entry cost c<sub>e</sub>", 27)}
{bullets(["Because an EPS worker is cheaper than a Korean manual worker, an eligible plant fills its manual work with EPS workers, up to its cap",
          "Productivity changes each year; unlucky plants close, and new plants replace them"], 24)}""",
      [("Equations", '"Each year a plant chooses its workers to maximise profit. It looks ahead: it stays open if the future is worth it, otherwise it closes. New plants keep entering until entering is just worth its cost; that pins down the wage."')], on=(5,))

# ------------------------------------------------------------------ 18. equilibrium
write("dec8-model-eq", f"""{kicker("Model")}{h2("Equilibrium: what adjusts and what is fixed")}
{table([["", "Fixed", "Adjusts"],
        ["Korean workers", "Total N", "The wage w, so all are employed"],
        ["EPS workers", f"The quota M ({pct(CFG['quota']['eps_share_of_workers'], 1)} of workers)", "The eligible share e (or the price p, or the limit L)"],
        ["Plants", "Entry cost, fixed costs", "How many enter, grow, and close"]], [24, 38, 38], 26)}
{box("We compare two long-run economies: today's rules and an alternative, with the same Korean workers and the same EPS quota. The difference in output is the cost (or gain) of the rule.", 25)}""",
      [("Table", '"Korean labour and the EPS quota are fixed. The wage, the eligible share, and the number and size of plants adjust. Every experiment keeps the same workers, so any difference in output comes from how they are allocated."')], on=(6,))

# ------------------------------------------------------------------ 19. experiments
write("dec8-experiments", f"""{kicker("Experiments")}{h2("Four ways to allocate EPS workers")}
{table([["", "Who may hire EPS", "How many", "What clears the quota"],
        ["<b>Today</b>", "Eligible plants (random share e)", "Up to the legal cap q(h + k)", "e"],
        ["<b>Equal limit</b>", "The same eligible plants", "Up to the same limit L for all", "L"],
        ["<b>Cap tilt</b>", "The same eligible plants", "Up to A·(Korean workers)<sup>S</sup>, for many tilts S", "A"],
        ["<b>Permit price</b>", "Any plant", "Any number, paying p per worker", "p"],
        ["<b>Larger or smaller quota</b>", "Eligible plants", "Up to the legal cap", "e"]], [22, 28, 30, 20], 24)}
{box("The equal limit and the tilt change only the link to size; the price changes who has access; the quota changes how many workers there are.", 25)}""",
      [("Table", '"We run four kinds of experiments. The equal limit and the tilt keep the same eligible plants and change only how the cap depends on size: this is the direct test of our question. The price lets any plant buy permits, which changes access. And we vary the size of the quota for comparison."')], on=(3, 4))

# ------------------------------------------------------------------ 20. parameters
ext = CFG["external"]
rows = [["Parameter", "Value", "How it is set"]]
EXT_LAB = dict(alpha=("α (returns to scale)", "Earlier Hopenhayn calibration to the Korean plant-size distribution"),
               rho_s=("ρ<sub>s</sub> (productivity persistence)", "Earlier Hopenhayn calibration to the Korean plant-size distribution"),
               beta=("β (discount factor)", "Standard annual value"), sig_e=("σ<sub>ε</sub>", "Smoothing of exit choices only"))
rows += [[EXT_LAB.get(k, (k, ""))[0], f"{v['value']}", EXT_LAB.get(k, ("", v["source"]))[1]] for k, v in ext.items()]
rows += [["ρ, λ, ψ, ξ, c<sub>m</sub>, c<sub>f</sub>, π<sub>B</sub>, σ<sub>s</sub>, γ, c<sub>e</sub>, δ", "13 values", "Chosen together to match the 8 targets (next slide)"]]
write("dec8-params", f"""{kicker("Calibration")}{h2("Parameters: set from outside, or chosen to match the data")}
{table(rows, [26, 14, 60], 23)}
{box("Draft: we are moving five of the chosen parameters to values set from data or the literature, so that parameters equal targets (for example ξ from the hiring-shortfall gradient, δ from the exit rate of the largest plants).", 23)}""",
      [("Table", '"Some parameters are set from outside; the rest are chosen together so the model matches Korean data."'),
       ("Box", '"We are reducing the number of freely chosen parameters, so that each one is pinned down by a target or a source."')])

# ------------------------------------------------------------------ 21. fit
lab = dict(avg_size=("Average plant size", 2), share_small=("Plants with 1–4 workers", "p"), share_50plus=("Plants with 50+ workers", "p"),
           exit_rate=("Exit rate", "p"), users=("Plants using EPS", "p"), eps_share_users=("EPS share at EPS firms", "p"),
           users_size=("Workers at EPS firms", 1), use_of_cap=("Share of the cap used", "p"))
SRC_LAB = dict(avg_size="MDIS business census 2024", share_small="MDIS business census 2024", share_50plus="MDIS business census 2024",
               exit_rate="Statistics Korea business demography", users="e-나라지표 1501 ÷ census plants", eps_share_users="Lee, Peri and Yang (2026)",
               users_size="Lee, Peri and Yang (2026)", use_of_cap="KDI–World Bank EPS survey 2019")
fmt = lambda v, d: pct(v, 1) if d == "p" else f"{v:.{d}f}"
rows = [["Target", "Data", "Model", "Source"]]
for t in CFG["targets"]:
    if t["name"] in lab and t["weight"] > 0:
        mv = get(B24 if t["caps"] == 2024 else B19, t["moment"])
        rows.append([lab[t["name"]][0], fmt(t["value"], lab[t["name"]][1]), fmt(mv, lab[t["name"]][1]), SRC_LAB.get(t["name"], t["source"].split(",")[0])])
write("dec8-fit", f"""{kicker("Calibration")}{h2("The model matches Korean manufacturing")}
{table(rows, [30, 12, 12, 46], 22)}
{foot("Plant-size and EPS-use targets under the 2024 caps; survey and Lee–Peri–Yang targets under the 2019 caps those firms faced.")}""",
      [("Table", '"Eight targets: plant sizes and exit from the census and Statistics Korea, how many plants use EPS from the Ministry, and how EPS firms look and how much of their cap they use from the survey and Lee, Peri and Yang. The model matches all of them closely."')])

# ------------------------------------------------------------------ 22-24 validation
write("dec8-valid-hist", f"""{kicker("Validation")}{h2("Check 1: how much of its cap each EPS firm uses")}
{fig("fig_capuse.png", 1664, 560, "Share of the 2019 legal cap used, survey against the model")}
{box(f"<b>Same average</b> ({pct(H['mean'])}, targeted) and a close median ({pct(hist['median'])} vs {pct(H['median'])}). The model is more concentrated: no plants below 30% or above 100% of their cap.", 24)}""",
      [("Chart", '"Orange is the survey, blue the model, both under the 2019 caps. The model matches the average, which we target, and the median. It misses the tails: in the data some firms use very little of their cap, and some are above it."')])
write("dec8-valid-size", f"""{kicker("Validation")}{h2("Check 2: which plants use EPS, and how much")}
{fig("fig_size.png", 1664, 562, "EPS firms by total workers, model against the survey, 2019 caps")}
{foot("Not targeted: only the averages are. The model's EPS share is flat among small plants because their manual share is the same at every size.")}""",
      [("Left", '"Where EPS firms are by size: the model is close to the survey."'),
       ("Right", '"Their EPS share falls with size in both. The model is too flat among the smallest firms, because in the model every manual-intensive plant has the same manual share at any size."')])
rows = [["Group", "% of plants", "% using EPS", "Workers per plant"]]
for k, nm in [("manual_eligible", "Manual-intensive, eligible"), ("manual_not", "Manual-intensive, not eligible"), ("light_eligible", "Light, eligible"), ("light_not", "Light, not eligible")]:
    g = G[k]
    rows.append([nm, pct(g["plants"], 1), pct(g["user_rate"]), f"{g['size']:.1f}"])
write("dec8-valid-who", f"""{kicker("Validation")}{h2(f"Check 3: who uses EPS in the model ({pct(B24['users'], 1)} of plants; data 8.0%)")}
{table(rows, [40, 20, 20, 20], 26, hi=(0,))}
{box("Only eligible manual-intensive plants use EPS. Light plants need little manual work; manual-intensive plants that are not eligible do their manual work with Korean workers at the extra cost.", 24)}""",
      [("Table", '"In the model, only the highlighted group uses EPS. That matches the fact that few plants use EPS, and explains why: many plants do not need it, and of those that do, only some get access."')])

# ------------------------------------------------------------------ 25-32 results
write("dec8-res-equal", f"""{kicker("Result 1")}{h2("Removing the link to size does not change output")}
{table([["Same quota, same eligible plants", "Net output", "Korean households' consumption"],
        [f"Equal limit, 2024 caps (L = {L24:.0f} per plant)", pct(eq24['net_Y'], 3, True), pct(eq24['welfare_korean'], 3, True)],
        [f"Equal limit, 2019 caps (L = {RUNS['equal_2019']['x']:.0f} per plant)", pct(eq19['net_Y'], 3, True), "—"]], [50, 25, 25], 27)}
{box(f"Replacing the size-based caps with one limit for every eligible plant changes net output by less than 0.01%. Only {pct(B24['at_or_above_cap'], 1)} of EPS users are at their 2024 cap ({pct(B19['at_or_above_cap'], 1)} under 2019).", 25)}""",
      [("Table", '"Our first experiment answers the research question directly: keep the same eligible plants and the same quota, but give every plant the same limit instead of a size-based cap. Output does not change."'),
       ("Box", '"The reason is that almost no plant is held back by its cap."')], on=(4,))
write("dec8-res-why", f"""{kicker("Why")}{h2("The caps rarely bind: most plants want fewer EPS workers than they may hire")}
{fig("fig_why_caps.png", 1664, 540, "EPS workers a plant wants against its legal cap")}
{foot(f"A manual-intensive plant with access fills its manual work with EPS workers: about {manual_ratio:.2f} per core Korean worker. Few plants are large enough to reach the cap.")}""",
      [("Chart", f'"The black line is how many EPS workers a manual-intensive plant wants: about {manual_ratio:.2f} per core Korean worker. The blue steps are the 2024 cap. The cap is above the line until a plant has about 63 core Koreans, and very few plants are that large. Under the lower 2019 caps it binds from about 18."')], on=(1, 3))
write("dec8-res-tilt", f"""{kicker("Result 2")}{h2("No tilt of the cap schedule raises output")}
{fig("fig_tilt.png", 1664, 600, "Change in net output against the tilt of the cap schedule")}
{foot("cap = A·(Korean workers)^S; today's 2024 schedule ≈ 9.4·n^0.32. Same eligible plants and quota; A adjusts.")}""",
      [("Chart", '"We then tilt the whole schedule: to the left, small plants get bigger caps; to the right, large plants do. Output stays flat across a wide range and falls only when caps strongly favour large plants and squeeze small ones. No tilt raises output: within our model, today\'s schedule cannot be improved by reshaping it."')], on=(3, 4))
write("dec8-res-price", f"""{kicker("Result 3")}{h2("Opening access with a permit price raises output")}
{table([["Same quota, any plant may buy permits", "Change vs today"],
        [f"Permit price p (clears the quota)", f"{p_price:.2f} ({pct(p_price / w_price)} of the wage)"],
        ["Net output, 2024 baseline", pct(price['net_Y'], 2, True)], ["Net output, 2019 baseline", pct(C['price_vs_2019']['net_Y'], 2, True)],
        ["Gross output", pct(price['Y'], 2, True)], ["Plants", pct(price['firms'], 1, True)],
        ["Korean households' consumption", pct(price['welfare_korean'], 2, True)],
        ["Net output if the extra Korean cost were only pay", pct(C['price_premium_as_pay_vs_2024'], 2, True)]], [60, 40], 25, hi=(1, 5))}""",
      [("Table", f'"Now change access instead of size: any plant may hire EPS workers if it pays a permit price, which settles at about {pct(p_price / w_price)} of the wage. Net output rises by {pct(price["net_Y"], 2)}, and Korean households gain {pct(price["welfare_korean"], 2)}."'),
       ("Caveat", '"The last row is the key caveat: the gain is the extra cost of Korean manual workers that EPS saves. If that cost were only higher pay, the gain would be about zero. Our Facts 3 and 4 support treating it as a real cost."')], on=(4,))
rows = [["Core Korean workers", "2–4", "5–9", "10–29", "30+"],
        ["Share of EPS workers, today"] + [pct(byh_t[k]) for k in ("2-5", "5-10", "10-30", "30-1e+09")],
        ["Share of EPS workers, price"] + [pct(byh_p[k]) for k in ("2-5", "5-10", "10-30", "30-1e+09")]]
pl = lambda lab, i: [lab, f"{plans['today']['m'][i]:.0f} → {plans['price']['m'][i]:.0f}", f"{plans['today']['k'][i]:.0f} → {plans['price']['k'][i]:.0f}"]
write("dec8-res-mech", f"""{kicker("Mechanism")}{h2("With a price, EPS workers move to the plants that need them most")}
{table(rows, [36, 16, 16, 16, 16], 25, hi=(1,))}
{table([["Eligible manual-intensive plant", "EPS workers: today → price", "Korean manual workers: today → price"], pl("Small (10th percentile)", 0), pl("Median", 1), pl("Top 1%", 2)], [40, 30, 30], 24)}
{box("Large plants find Koreans easily, so an EPS worker saves them little; with a price they switch to Korean workers. The workers move to mid-sized plants, where Korean manual workers are scarcest.", 23)}""",
      [("Top table", '"Where EPS workers go. Today about a third are at plants with 30 or more core Koreans, where Korean workers are easy to find. With a price, they move to plants with 5 to 29 core Koreans."'),
       ("Bottom table", '"Individual plants: the top plant gives up its EPS workers and hires Koreans instead; the workers go where they save the most."')], on=(2, 4))
write("dec8-res-quota", f"""{kicker("Result 4")}{h2("The number of EPS workers matters far more than how caps depend on size")}
{fig("fig_quota.png", 1664, 600, "Change in net output and Korean consumption against the quota size")}
{foot("Same rules; the eligible share adjusts. Korean households' consumption = net output minus EPS workers' wages.")}""",
      [("Chart", '"For comparison, we change the quota. Each 25 percent more EPS workers raises net output by about 1.5 percent. Korean households gain about a quarter of that, because the rest is paid to the EPS workers."')])
write("dec8-res-summary", f"""{kicker("Putting it together")}{h2("Where the gains are: access and quantity, not the size rule")}
{fig("fig_summary.png", 1664, 600, "Gains from each change")}
{foot("For Korean households, a permit price is worth about as much as a 25% larger quota.")}""",
      [("Chart", '"Side by side: reshaping the caps gives nothing; a permit price gives about 0.4 percent; a 25 percent larger quota about 1.5 percent of net output. For Korean households, the price is worth about as much as 25 percent more workers, because it brings no extra wages to pay out."')])
sens = {d["name"]: d for d in RV["sensitivity"]}
write("dec8-robust", f"""{kicker("Robustness")}{h2("How sensitive are the results?")}
{table([["Change", "Price gain (net output)", "Equal limit"],
        ["Baseline", pct(price['net_Y'], 2, True), pct(eq24['net_Y'], 3, True)],
        ["2019 caps instead of 2024", pct(C['price_vs_2019']['net_Y'], 2, True), pct(eq19['net_Y'], 3, True)],
        ["Extra Korean cost treated as pay, not a real cost", pct(C['price_premium_as_pay_vs_2024'], 2, True), "—"],
        ["Smaller extra cost (ψ = 0.92, others fixed)", pct(sens['psi = 0.92 (v6)']['price_net'], 2, True), "—"],
        ["Larger extra cost (ψ × 1.2, others fixed)", pct(sens['psi x1.2']['price_net'], 2, True), "—"]], [52, 24, 24], 24)}
{box("The size result (no effect) holds in every case. The size of the price gain depends on the extra cost of hiring Korean manual workers: it is the one number to read with care.", 24)}""",
      [("Table", '"The finding that the size rule does not matter holds everywhere. The price gain ranges from about 0.1 to 0.5 percent depending on how large the extra cost of Korean manual workers is, and disappears if that cost is only pay."')])

# ------------------------------------------------------------------ 33-36 conclusion
write("dec8-learn", f"""{kicker("Conclusion")}{h2("What we learn")}
{bullets([
    "<b>The size-based cap is not where output is lost.</b> In our model it rarely binds, and no reshaping of it raises output",
    f"<b>Access is.</b> Letting any plant buy permits raises net output by about {pct(price['net_Y'], 1)}: workers move from large plants that can hire Koreans to mid-sized plants that cannot",
    f"<b>Quantity matters most.</b> 25% more EPS workers raise net output by about {pct(q125['net_Y'], 1)}",
    "<b>For policy:</b> debates about EPS should focus on how permits are allocated (points, waiting lists) and on the quota, more than on the size schedule"], 27)}""",
      [("Bullets", '"Three lessons. The size rule, which looked like the obvious distortion, is not where output is lost. Access is: who gets permits matters, and a price would send them where they save the most. And quantity matters most of all. So the policy debate should focus on allocation and the quota."')])
write("dec8-limits", f"""{kicker("Conclusion")}{h2("Limitations")}
{bullets([
    "Korean and EPS manual workers are perfect substitutes; the survey suggests EPS workers are somewhat less productive",
    "Eligibility is random and permanent; real permits follow points and last a few years",
    "The quota is assumed fully used",
    "The extra cost of Korean manual workers drives the price gain; we discipline it with survey and Ministry data, but its size is calibrated",
    f"EPS users rarely close in the model; Lee, Peri and Yang find exposed firms closed more often (slope 0.15; model {B19.get('slope_lpy', 0):.2f})",
    "EPS workers are outside the model: we count their wages but not their wider welfare"], 25)}""",
      [("Bullets", '"We want to be clear about what the model leaves out. The most important for the numbers is the extra cost of hiring Korean manual workers. The most important for interpretation is that the model understates how fragile EPS firms are."')])
write("dec8-next", f"""{kicker("Conclusion")}{h2("Next: checking the model against Ministry data")}
{table([["Ministry table (requested)", "What it will check"],
        ["E-9 workplaces and cap use by size, 2024", "Whether caps bind today (the model says rarely)"],
        ["Applications, allocations and waiting lists", "How rationed access really is (the model: 22% of plants eligible)"],
        ["Exits by E-9 status", "Whether EPS users really close less often"],
        ["Korean hiring before applying, by size", "How costly Korean manual workers are at small plants"]], [45, 55], 25)}""",
      [("Table", '"We have requested Ministry data by plant size. Each table checks one key piece of the model, and our pipeline is ready to use them."')])
write("dec8-refs", f"""{h2("References")}
{bullets([
    "Dong, M., Lee, J. and Yang, H.-S. (2024). How does low-skilled immigration affect native wages? Evidence from Employment Permit System in Korea. <i>Oxford Economic Papers</i> 76(2)",
    "Garicano, L., Lelarge, C. and Van Reenen, J. (2016). Firm size distortions and the productivity distribution: Evidence from France. <i>American Economic Review</i> 106(11)",
    "Guner, N., Ventura, G. and Xu, Y. (2008). Macroeconomic implications of size-dependent policies. <i>Review of Economic Dynamics</i> 11(4)",
    "Hopenhayn, H. A. (1992). Entry, exit, and firm dynamics in long run equilibrium. <i>Econometrica</i> 60(5)",
    "Lee, J., Peri, G. and Yang, H.-S. (2026). The effects of a sudden stop in low-skilled immigration: Evidence from Korea's guest worker program. NBER Working Paper 34927",
    "Data: MDIS business census 2024; KDI–World Bank EPS survey 2019; e-나라지표 1501; Statistics Korea business demography; 고용노동부 직종별사업체노동력조사"], 21)}
{foot("We worked with the AI assistant Claude (Anthropic) for literature search, fact-checking, coding, model runs and drafting, in line with the course AI policy.")}""",
      [("Close", '"Thank you. We are happy to take questions."')])

print("slides", PG, "total", TOTAL)
