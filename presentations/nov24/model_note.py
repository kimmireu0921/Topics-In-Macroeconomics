"""Writes the written model description (model_note.md, then model_note.pdf) from the v8 results.
Run from this folder: python3 model_note.py. Needs pandoc and Google Chrome (for the PDF)."""
import json, os, subprocess

E = "../../hopenhayn_project/eps_model/"
R = json.load(open(E + "v8_results.json"))
XT = json.load(open(E + "v8_extra.json"))
H = json.load(open("../../bunching/cap_use_hist.json"))
CU = json.load(open(E + "baseline/survey_binding.json"))["by_cap_use"]
P, FIT, T = R["params"], R["fit"], R["targets"]
X, CH = R["experiments"], R["change_vs_current"]
C24, C19 = XT["caps2024"], XT["caps2019"]
DECK = "https://claude.ai/artifact/232yGbzBu7EdLqBGKQZ3jE"
REPO = "https://github.com/kimmireu0921/Topics-In-Macroeconomics"


def pc(x, d=1, sign=False):
    v = round(100 * x, d) + 0.0
    if v == 0:
        return f"{0:.{d}f}%"
    return f"{v:{'+' if sign else ''}.{d}f}%".replace("-", "−")


f = lambda v, d=2: f"{v:.{d}f}"
prem0 = 1 + P["psi"]
md = f"""---
title: "Size-Linked Caps and Access to Foreign Workers: Model Description"
subtitle: "Korea's Employment Permit System in a model of plant dynamics"
author: "Sara Ambre Chekroune, Yitang Donny Chen, Mireu Kim, Julian Henry Raymundo, Zachary Benjamin Yoo"
date: "November 18, 2026"
---

* **Slides** (this version: slides 63–78): <{DECK}>
* **Code and data construction:** <{REPO}>. Model `hopenhayn_project/eps_model/eps_model_v8.py`, calibration and experiments `run_v8.py` and `v8_extra.py`, targets and sources `TARGETS.md`. Survey and census microdata are not in the repository; the scripts that build every moment are.

# 1. Overview

Korea's Employment Permit System (EPS) admits low-skilled foreign workers (E-9 visas) under a national quota. A manufacturer may employ them only if it is eligible and only up to a legal cap that rises with its number of insured Korean workers. We ask whether tying permits to plant size distorts which plants operate and how large they are, and how much output would change if the same quota were allocated without regard to size.

The model is a stationary Hopenhayn (1992) economy with two plant types, a Pareto tail in productivity, a scarcity premium on Korean manual workers, and the EPS rules. In this version access is rationed at entry: a random share of entrants is eligible, and an eligible plant may hire foreign workers up to its full legal cap. The eligible share adjusts so that the quota is used.

# 2. Environment

Time is discrete and annual; we study a stationary equilibrium. There is one good. Korean labor $N = 1$ is supplied inelastically at wage $w$. The EPS quota $M$ is fixed so that EPS workers are {pc(219_507 / 4_147_204, 2)} of manufacturing workers, $M/(N+M) = 0.0529$ (219,507 E-9 workers in manufacturing at the end of 2024, Ministry of Employment and Labor, over 4.15 million workers in the 2024 business census).

A plant draws three permanent characteristics at entry, independently of one another:

* a type $t \\in \\{{A, B\\}}$: light ($A$) or manual-intensive ($B$), with $\\Pr(B) = \\pi_B$;
* a permanent productivity level $x \\sim \\text{{Pareto}}(1, \\gamma)$;
* EPS eligibility $\\iota \\in \\{{0, 1\\}}$, with $\\Pr(\\iota = 1) = e$.

Productivity is $s = x z$, where $\\log z' = \\rho_s \\log z + \\sigma_s \\varepsilon'$, $\\varepsilon' \\sim N(0,1)$. Entrants draw $z$ from its stationary distribution; $\\nu$ denotes the entrants' distribution of $s$.

**Timing within a year.** Incumbents and entrants hire and produce. Each plant then exits exogenously with probability $\\delta$; survivors decide whether to stay, subject to a logit taste shock with scale $\\sigma_\\varepsilon$. New plants pay $c_e$ and enter until the expected value of entry equals $c_e$.

# 3. Technology and costs

A plant combines core Korean workers $h$ with manual work $\\ell$:
$$ y = s\\,\\big(h^{{\\rho}} + \\lambda_t\\,\\ell^{{\\rho}}\\big)^{{\\alpha/\\rho}}, \\qquad \\ell = k + m, $$
where manual work is done by Korean manual workers $k$ or EPS workers $m$, one for one, and $\\alpha < 1$.

* A core worker costs $w$.
* A Korean manual worker costs $w\\,\\big(1 + \\psi\\,(1+h)^{{-\\xi}}\\big)$. The premium captures the difficulty of filling manual jobs with Korean workers at small plants (recruiting, unfilled positions, overtime); it falls with $h$.
* An EPS worker costs $w$; using any EPS workers costs a fixed $c_m$ per year.
* Operating costs a fixed $c_{{f,t}}$ per year.

# 4. EPS rules

Today's rule, the baseline, is the following. A plant with $\\iota = 0$ cannot hire EPS workers. A plant with $\\iota = 1$ may hire
$$ 0 \\le m \\le q(h + k) \\quad \\text{{if }} h \\ge 1 \\text{{ and }} h + k < 300, $$
where $q(\\cdot)$ is the legal cap by insured Korean workers $n = h + k$:

| $n$ | 1–10 | 11–50 | 51–100 | 101–150 | 151–200 | 201–299 |
|---|---|---|---|---|---|---|
| $q(n)$, 2024 | $n+10$ | $\\min(30, 2n)$ | 35 | 40 | 50 | 60 |

| $n$ | 1–5 | 6–10 | 11–30 | 31–50 | 51–100 | 101–150 | 151–200 | 201–299 |
|---|---|---|---|---|---|---|---|---|
| $q(n)$, 2019 | 5 | 7 | 10 | 12 | 15 | 20 | 25 | 30 |

Sources: eps.go.kr (2024, manufacturing); Lee, Peri and Yang (2026), Table 4 (2019).

**Rationing.** Demand at the legal caps exceeds the quota, so not every plant can be served. Eligibility is random. It stands in for the points ranking and waiting lists through which permits are allocated. The eligible share $e$ is an equilibrium object: it adjusts so that total EPS employment equals $M$.

# 5. The plant's problem

**Static profit.** For type $t$, eligibility $\\iota$ and productivity $s$:
$$ \\pi_{{t,\\iota}}(s) = \\max_{{h,k,m}}\\; s\\,f_t(h, k+m) - w h - w\\big(1+\\psi(1+h)^{{-\\xi}}\\big)k - w m - c_m\\mathbf{{1}}[m>0] - c_{{f,t}} $$
subject to the rule in Section 4. Because an EPS worker costs less than a Korean manual worker, an eligible plant that uses EPS fills its manual work with EPS workers up to its cap.

**Values and exit.** With $c_{{t,\\iota}}(s) = \\beta(1-\\delta)\\,\\mathbb{{E}}[V_{{t,\\iota}}(s') \\mid s]$,
$$ V_{{t,\\iota}}(s) = \\pi_{{t,\\iota}}(s) + \\sigma_\\varepsilon \\log\\!\\big(1 + e^{{c_{{t,\\iota}}(s)/\\sigma_\\varepsilon}}\\big), \\qquad \\Pr(\\text{{stay}} \\mid s) = \\frac{{1}}{{1 + e^{{-c_{{t,\\iota}}(s)/\\sigma_\\varepsilon}}}}. $$
A plant's exit probability is $1 - (1-\\delta)\\Pr(\\text{{stay}} \\mid s)$.

**Free entry.**
$$ \\sum_t \\Pr(t)\\Big[e\\!\\int V_{{t,1}}\\,d\\nu + (1-e)\\!\\int V_{{t,0}}\\,d\\nu\\Big] = c_e. $$

# 6. Stationary distribution and equilibrium

For each $(t, \\iota)$, the measure of plants satisfies
$$ \\mu_{{t,\\iota}}(s') = M_e \\Pr(t)\\Pr(\\iota)\\,\\nu(s') + (1-\\delta)\\sum_s \\Pr(\\text{{stay}} \\mid s)\\,P(s' \\mid s)\\,\\mu_{{t,\\iota}}(s), $$
where $M_e$ is the mass of entrants and $P$ the transition of $s$.

**Definition.** A stationary equilibrium is $w$, the eligible share $e$, the entry mass $M_e$, policies $(h, k, m)_{{t,\\iota}}(s)$ and measures $\\mu_{{t,\\iota}}$ such that:

1. the policies solve the plant's problem;
2. free entry holds;
3. the Korean labor market clears: $\\sum_{{t,\\iota}}\\int (h+k)\\,d\\mu_{{t,\\iota}} = N$;
4. the quota is used: $\\sum_{{t,\\iota}}\\int m\\,d\\mu_{{t,\\iota}} = M$;
5. $\\mu$ is the stationary measure above.

**Output and welfare.** Gross output is $Y = \\int y\\,d\\mu$. Net output subtracts the resources the economy uses up:
$$ Y^{{net}} = Y - \\int\\big[w\\,\\psi(1+h)^{{-\\xi}}k + c_m\\mathbf{{1}}[m>0]\\big]d\\mu - \\sum_t c_{{f,t}}\\,\\mu_t - c_e M_e . $$
Wages are transfers to households and are not subtracted. The Korean premium is treated as a resource cost; we also report results treating it as pay.

# 7. Allocation experiments

Each experiment holds $N$ and $M$ fixed and compares steady states.

| | Today (baseline) | Price | Equal limit |
|---------|---------|---------|---------|
| Who may hire EPS | eligible plants (share $e$) | any plant with $h \\ge 1$ | the same eligible plants |
| How many | up to $q(h+k)$ | any number | up to $L$, the same for all |
| Cost of an EPS worker | $w$ | $w + p$ | $w$ |
| Variable that clears the quota | $e$ | $p$ | $L$ |

Under the price, permit revenue $pM$ is rebated to households. The equal limit keeps who is eligible and removes only the link to size.

# 8. Computation

Plants choose $(h, \\ell)$ on a grid: 320 log-spaced points for $h$ (plus every cap step) and 201 for $\\ell$. Extra points place $h+k$ just past each cap step, or just below 300, so plants can bunch at the steps. For each grid point, the largest feasible $m$ under the cap is computed once. Productivity uses 24 Pareto nodes for $x$ and 11 Tauchen nodes for $z$. Values are found by value iteration, $w$ by Brent's method on free entry, and $e$ (or $p$, $L$) by Brent's method on the quota condition.

# 9. Calibration

Four parameters are set: $\\alpha = 0.6916$ and $\\rho_s = 0.8975$ (carried over from our first Hopenhayn calibration of Korean manufacturing), $\\beta = 0.96$, and $\\sigma_\\varepsilon = 0.1$, which only smooths exit. The thirteen remaining parameters minimize the sum of squared percentage gaps between eight model moments and their data counterparts.

Census and Ministry moments are computed under the 2024 caps. Moments from the EPS survey and from Lee, Peri and Yang refer to 2019–2020 and are computed in a second equilibrium under the 2019 caps, with the same parameters.

| Parameter | | Value | Parameter | | Value |
|------------|----|-----|------------|----|-----|
| Curvature, core vs manual | $\\rho$ | {f(P['rho'])} | Manual-intensive share of entrants | $\\pi_B$ | {f(P['shB'])} |
| Weight on manual work, A | $\\lambda_A$ | {f(P['lamA'], 3)} | Weight on manual work, B | $\\lambda_B$ | {f(P['lamB'])} |
| Fixed operating cost, A | $c_{{f,A}}$ | {f(P['cfA'])} | Fixed operating cost, B | $c_{{f,B}}$ | {f(P['cfB'])} |
| Korean manual premium | $\\psi$ | {f(P['psi'])} | Decline of the premium with $h$ | $\\xi$ | {f(P['xi'])} |
| Fixed cost of using EPS | $c_m$ | {f(P['cm'])} | Entry cost | $c_e$ | {f(P['ce'], 1)} |
| Productivity shock s.d. | $\\sigma_s$ | {f(P['sigma_s'], 3)} | Pareto tail | $\\gamma$ | {f(P['gamma'])} |
| Exogenous exit | $\\delta$ | {f(P['delta'], 3)} | | | |

The premium is large: at a plant with no core Korean workers, a Korean manual worker costs {prem0:.2f} times the wage.

| Target | Data | Model | Source |
|--------------|-----|-----|-------------------|
| Average plant size (workers) | {T['avg_size']:.2f} | {FIT['avg_size']:.2f} | MDIS business census 2024, all 509,467 manufacturing plants |
| Plants with 1–4 workers | {pc(T['share_small'])} | {pc(FIT['share_small'])} | Same |
| Plants with 50+ workers | {pc(T['share_50plus'])} | {pc(FIT['share_50plus'])} | Same |
| Exit rate | {pc(T['exit_rate'])} | {pc(FIT['exit_rate'])} | Statistics Korea, business demography, manufacturing, 2024 |
| Plants using EPS | {pc(T['users'])} | {pc(FIT['users'])} | Ministry of Employment and Labor: 40,766 workplaces with E-9 workers, end of 2024 |
| EPS share at EPS firms (mean) | {pc(T['eps_share_users'])} | {pc(FIT['eps_share_users'])} | Lee, Peri and Yang (2026), Table 3 |
| Workers at EPS firms (mean) | {T['users_size']:.1f} | {FIT['users_size']:.1f} | Lee, Peri and Yang (2026), Table 3 |
| Share of the 2019 legal cap used (mean) | {pc(T['use_of_cap'])} | {pc(FIT['use_of_cap'])} | KDI–World Bank EPS survey 2019, 772 firms (replication file of Dong, Lee and Yang 2024) |

In equilibrium {pc(R['e_2024'], 0)} of entrants are eligible under the 2024 caps and {pc(R['e_2019'], 0)} under the 2019 caps.

**Cap use.** In the survey (772 manufacturers, fielded in 2019; Dong, Lee and Yang 2024), EPS firms are spread across the whole range of cap use: the median firm uses {pc(H['median'], 0)} of its legal cap, {pc(H['at_or_below_theta_0_21'], 0)} use 21% or less, and {pc(H['at_or_above_cap'], 0)} are at or above the cap. The model matches the mean by construction. It puts {pc(R['lpy']['at_cap'], 0)} of EPS users at the cap, and almost none below 30% of the cap.

**Closure check, not targeted.** Lee, Peri and Yang estimate that EPS firms more exposed to the 2020–21 stop in inflows closed more often (slope 0.152 on statutory exposure $q/(n+q)$, with size controls). In the model we replicate their design: an unexpected two-year 20% cut in each user's EPS workers at fixed prices, then a regression of the extra closure probability on exposure among users. The model slope is {R['checks']['slope_lpy']:.3f}. Eligible plants keep their permits, so users are rarely close to the exit margin. In a random search over parameters, the best draws all gave slopes of 0.07 or less. We report this as a limitation rather than a target.

# 10. Results

| Same quota, change against today | Net output, 2024 caps | Net output, 2019 caps | Gross output, 2024 | Net output if premium is pay, 2024 |
|-------------|-------|-------|-------|-------|
| Equal limit (same eligible plants) | {pc(C24['equal_limit']['net'], 2, True)} | {pc(C19['equal_limit']['net'], 2, True)} | {pc(C24['equal_limit']['gross'], 2, True)} | {pc(C24['equal_limit']['net_premium_as_pay'], 2, True)} |
| Price (any plant) | {pc(C24['price']['net'], 2, True)} | {pc(C19['price']['net'], 2, True)} | {pc(C24['price']['gross'], 2, True)} | {pc(C24['price']['net_premium_as_pay'], 2, True)} |
| No EPS at all | {pc(CH['no EPS']['net_Y'], 2, True)} | — | {pc(CH['no EPS']['Y'], 2, True)} | — |

**The legal caps rarely bind.** {pc(XT['binding_2024']['users_at_cap'], 1)} of EPS users are at their 2024 cap ({pc(XT['binding_2019']['users_at_cap'], 1)} under 2019). Replacing the size-linked cap with an equal limit therefore leaves net output unchanged.

**Access matters more.** Letting any plant buy permits at $p = {X['price']['x']:.2f}$ ({pc(X['price']['x'] / X['price']['w'], 0)} of the wage) raises net output by {pc(C24['price']['net'], 2)}. EPS workers move from plants with 30 or more core Korean workers, which hold {pc(XT['by_h']['today']['30-1e+09'], 0)} of them today and for which the premium is small, to plants with 5–29.

The gain is the Korean premium saved. If the premium is pay rather than a resource cost, the gain is {pc(C24['price']['net_premium_as_pay'], 2, True)}.

# 11. Main assumptions

1. Korean and EPS manual workers are perfect substitutes.
2. Eligibility is random and permanent; actual permits follow a points ranking and last three years.
3. The quota is fully used. A 2024 projection put arrivals near half the quota, while waiting lists were reported in 2026.
4. The Korean premium is a resource cost.
5. Access is all or nothing. The survey's firms above their cap ({pc(H['bins']['above 100%'], 0)}), and firms below half their cap that still want more workers ({pc(CU['under_half']['want_more'], 0)} of them), are not in the model.

# References

Dong, M., Lee, J., and Yang, H.-S. (2024). How does low-skilled immigration affect native wages? Evidence from Employment Permit System in Korea. *Oxford Economic Papers*, 76(2). Survey data from the article's replication file.

Hopenhayn, H. A. (1992). Entry, exit, and firm dynamics in long run equilibrium. *Econometrica*, 60(5), 1127–1150.

Lee, J., Peri, G., and Yang, H.-S. (2026). The effects of a sudden stop in low-skilled immigration: Evidence from Korea's guest worker program. NBER Working Paper 34927.
"""
open("model_note.md", "w").write(md)
css = """body{font-family:'Source Serif 4',Georgia,serif;font-size:11pt;line-height:1.45;max-width:46em;margin:0 auto;color:#1f2a3c}
h1{font-size:14pt;margin-top:1.4em} header h1.title{font-size:19pt;margin-bottom:0.2em} .subtitle{font-size:12.5pt;margin-top:0}
.author,.date{font-size:10.5pt;margin:0.2em 0} table{border-collapse:collapse;margin:0.8em 0;font-size:9.5pt;width:100%}
th,td{border-bottom:1px solid #c9d1de;padding:3px 6px;text-align:left} th{border-bottom:1.5px solid #14213d}
a{color:#2f5d8a;word-break:break-all} @page{size:A4;margin:2.2cm 2cm}"""
open("model_note.css", "w").write(css)
subprocess.run(["pandoc", "model_note.md", "-s", "--mathml", "--css", "model_note.css", "--embed-resources",
                "--metadata", "lang=en", "-o", "model_note.html"], check=True)
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=5000",
                f"--print-to-pdf={os.path.abspath('model_note.pdf')}", "file://" + os.path.abspath("model_note.html")],
               check=True, capture_output=True)
print("written model_note.pdf")
