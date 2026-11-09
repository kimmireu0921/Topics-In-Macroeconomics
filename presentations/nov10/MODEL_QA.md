# Questions on the model, answered from the code and results

Benjamin's questions before Nov 10, answered from the model code (`hopenhayn_project/eps_model/`) and
its saved results, not from the slides. Code and result files are named in each answer so anyone can check them.
All numbers use the calibrated parameters (`v6_best.json`), the 2024 caps and the 24 × 11 calibration
grid, unless a finer grid is stated.

## 1. Baseline model

**Does the current-rule model have a permit price?**
No. Under the current rule permits are free. An EPS worker costs the wage `w` (`phi = 1`), plus the fixed
cost `c_m` = 0.383 once a plant uses any EPS. The quota is shared by quantity: every eligible plant
may use the same share θ = 0.212 of its cap. The permit price `p` appears only in the counterfactual.
(`eps_model.py`, `_plan`: `wm = phi * w` under `"current"`, `wm = phi * w + x` under `"neutral"`.)

**Is the cap computed from h or from h + k?**
From core Koreans `h` only: `m ≤ θ · q(h)`, and eligibility is `1 ≤ h < 300`. The law counts all
insured Korean workers, `h + k`. The code docstring calls `q(h)` an approximation of `q(h + k)`.

**Is the national quota fixed in both scenarios?**
Yes. `M` = 0.058 (EPS workers = 5.5% of all workers, with Korean labor `N` = 1) in the current rule, the
price experiment and the free equal-limit experiment. θ, `p` or the equal limit adjusts until
EPS use equals `M`. Two exceptions: the "free, no limit" column on slide 50 is not an equilibrium
(demand would be 8.5 times the quota), and the ±50% quota runs are used only for the kill line.

## 2. Slide 49: large plants

**Why does the Korean manual premium fall with plant size?**
It is an assumption, not something we measured. The reason given in the code is that small plants
struggle to find Korean manual workers ("no applicants": 53% of Lee, Peri and Yang's firms; 82.6% of
KBIZ 2025 firms say they hire EPS because they cannot find Koreans). Those surveys support a recruiting
problem. They do not tell us how it changes with size. ψ (0.915) and ξ (0.231) are calibrated to the 8
targets, mainly through who uses EPS and how large users are. This is the assumption slide 51 tests.

**Is p = 0.34 solved inside the model? How?**
Yes. `solve("neutral")` starts at `p` = 0. If EPS demand exceeds `M`, it widens a bracket (×4 each
time) and finds the root of *EPS demand(p) − M* with Brent's method. At every trial `p` it re-solves
the whole equilibrium: plant choices, the wage from free entry, and the number of entrants from
Korean labor. Result: `p` = 0.344 at a wage of 0.816, so a permit costs about 42% of the wage.
(`eps_model_v5.py`, `solve`.)

**Why do the saving and the price cross at about 28 core Koreans?**
One EPS worker saves the premium, `w · ψ(1 + h)^−ξ`. It costs `p`. Setting them equal gives
`h = (p / (w ψ))^(−1/ξ) − 1 = (0.344 / (0.816 × 0.915))^(−1/0.231) − 1 = 27.6`.
The cutoff ignores `c_m`, so a plant also needs the total saving to cover 0.383. In the price
experiment, plants below about 28 core Koreans use EPS for all their manual work. Plants above it use
none.

**Why does the top-1% plant lose all its EPS workers but grow from 317 to 328?**
Losing its EPS workers: with 150 core Koreans, a permit saves 0.287 × `w` = 0.23, less than `p` = 0.34.
(The "11" is 10.6 rounded.)

The growth has **nothing to do with EPS. It comes from the lower wage.** We solved the same plant
(the 99th-percentile productivity among manual-intensive plants under today's rule) at both wages:

| Plan for the same plant | Wage | Core h | Korean manual k | EPS m | Total |
|---|---|---|---|---|---|
| Current rule | 0.830 (today) | 150 | 156 | 10.6 | 317 |
| Price | 0.816 (price economy) | 150 | 178 | 0 | 328 |
| Price | 0.830 (today) | 141 | 167 | 0 | 308 |
| No EPS at all | 0.830 (today) | 141 | 167 | 0 | 308 |
| No EPS at all | 0.816 (price economy) | 150 | 178 | 0 | 328 |

At either wage, the price plan is identical to having no EPS at all. With a price the wage falls 1.7%
(free entry: fewer manual-intensive plants survive, so the entry condition settles at a lower `w`), and
every plant hires a little more.

There is a second effect. Under today's rule the plant sits just past the 150-worker step
(h = 150.00015), where its cap jumps from 40 to 50. Without the rule, at the same wage, it would choose
141. So the size rule makes this plant *larger*, by about one grid step: it bunches at the cap step.

Caveat: 141 to 150 is one point on the `h` grid (points are about 3.6% apart), so differences of this
size are close to the grid's resolution. **Suggested wording for slide 49:** "the top-1% plant drops its
EPS workers and stays about the same size; the small rise comes from the lower wage, not from EPS."

**Does the explanation hold if the cap is corrected to q(h + k)?**
Mostly yes, though this has not been run. The price experiment has no cap at all, so `p` = 0.344, the
28-worker cutoff and the price-economy outcomes do not change. What changes is the comparison point,
today's rule:
- The top-1% plant has h + k = 306 Koreans. Under the law it would be **over 300 and ineligible**,
  so it would have no EPS workers today either. "Loses 11 EPS workers" would become "had none."
- Plants with many Korean manual workers would get larger caps. θ would fall to keep total use at `M`,
  moving permits toward those plants.
- The levels (+0.33%, −0.9%) would change, and the model would need recalibrating, because the
  targets were matched with `q(h)`.

Running it needs `m ≤ θ · q(h + ℓ − m)` solved at each grid point. It can be done, but it is a new run.

## 3. Slide 50: policy comparisons

**What changes between the three?**

| | Current rule | Price | Free, equal limit |
|---|---|---|---|
| Limit per plant | `m ≤ θ · q(h)`, θ = 0.212 | none | `m ≤ L`, L = 3.86 workers for every plant |
| Who may use EPS | 1 ≤ h < 300 | h ≥ 1 | h ≥ 1 (a version keeping 1 ≤ h < 300 gives almost the same result) |
| Cost of an EPS worker | `w` (+ `c_m`) | `w + p` (+ `c_m`) | `w` (+ `c_m`) |
| What clears `M` | θ | `p` = 0.344 | `L` |

Everything else (parameters, `N`, `M`, the grid) is the same. Code: `v6_free_flat.py`, class `Flat`.

**Why does gross output fall 0.9% with a price but rise 1.0% with an equal limit?**
- *Price:* small manual-intensive plants now pay 42% more per EPS worker, and plants above about 28 core
  Koreans stop using EPS. Fewer manual-intensive plants survive (mass 0.0141 to 0.0105). The share of
  plants using EPS falls from 10.7% to 6.2%. Their output falls from 0.550 to 0.515, while light plants
  gain only from 0.774 to 0.797 using the freed Korean workers. Net effect: −0.9%.
- *Equal limit:* permits stay free, so EPS is just as cheap, and they are spread thinly to many plants.
  62% of EPS workers go to plants with 0–5 Koreans. More manual-intensive plants survive (share 10.8% to
  11.6%), the number of plants rises 2.3%, and gross output rises 1.0%.

**Why does net output rise when gross output falls?**
Net output = gross output − real resource costs (see the next answer). With a price, costs fall by more
than output does:

| Per 100 of today's gross output | Current | Price | Change |
|---|---|---|---|
| Gross output | 100.0 | 99.1 | −0.9 |
| Korean manual premium | 2.49 | 2.36 | −0.13 |
| EPS fixed cost `c_m` | 0.40 | 0.23 | −0.17 |
| Fixed operating costs `c_f` | 6.37 | 5.70 | −0.67 |
| Entry costs | 11.77 | 11.57 | −0.19 |
| **Net output** | **79.0** | **79.2** | **+0.26 points = +0.33%** |

Most of the saving is fixed operating costs: manual-intensive plants fall by about a quarter (mass
0.0141 to 0.0105), and each costs 2.68 a year to run, against 0.40 for a light plant. So the net gain comes mostly from
**today's rule keeping more manual-intensive plants alive**, each with a high fixed cost. That is closer
to Prof. Hur's original question than slide 50 currently says.

**What is in the costs of 21.0, 19.9 and 21.9?**
Per 100 of today's gross output: (gross − net) / today's gross.
- Included: the Korean manual premium above the wage, `w ψ(1+h)^−ξ · k`; the EPS fixed cost `c_m`
  per user; fixed operating costs `c_f` per plant; entry costs `c_e` × entrants. (`summarize`:
  `net_Y = Σμ(y − rc) − Σ c_f − c_e · Me`, where `rc` = premium × k + `c_m`.)
- Not included: wages (Korean labor is a fixed endowment, so wages are not a resource cost), and permit
  payments `p · m` = 0.020. Those are a transfer to whoever sells the permits.

**Which grid gives which number?**

| | 24 × 11 (calibration grid) | 48 × 21 (finer; last week's chart) |
|---|---|---|
| Price, net output | +0.33% | +0.37% |
| Free equal limit, net output | +0.19% | +0.09% |

"24 × 11" means 24 permanent-productivity points × 11 persistent-shock points; both use 320 size points.

## 4. Slide 51: robustness

**What changes and what stays fixed?**
Only the premium curve changes: its slope ξ and its level ψ. In five runs ψ moves so that the premium at
10 core Koreans stays as calibrated. The sixth uses version 5's pair (ψ 1.599, ξ 0.101). Rows: ξ = 0.231
(ours), 0.15, 0.10, 0.05, 0.35, and version 5. The other 11 parameters, `α`, `β`, `N`, `M` and the grid
stay fixed. For each pair, both the current rule and the price experiment are fully re-solved: `w`, θ or
`p`, and the number of plants. (`v6_free_flat.py`, `premium_run`.)

**Are the six recalibrated?**
No. Five of them are not recalibrated and do not fit the 8 targets. The sixth is our calibration itself.
So the table shows direction only, not levels.

**Why do the gross and net directions hold while large-plant EPS changes?**
The premium decides where the cutoff lies (25 to 419 core Koreans across the rows), and so whether large
plants keep EPS. It does not decide whether they grow. Because `ℓ = k + m`, an EPS worker replaces a
Korean manual worker one for one. A large plant already hires Koreans, so its next manual worker costs
the Korean rate whatever its EPS count. Extra permits only lower its costs on workers it already has.
In version 5's row the top plant goes from 10 to 69 EPS workers but from 203 to 200 workers in total.
Gross output falls in every row (−0.7% to −2.2%) because small manual-intensive plants lose cheap
permits and some close; net output rises (+0.33% to +0.77%) because fixed costs fall. Both run through
small plants, not large ones.

## 5. Slide 52: numerical accuracy

**What caused the bumps?**
The productivity grid. On last week's 48 × 21 grid, productivity moves in steps of about 5% (log step
0.051). Plant size rises about 3.2 times as fast as productivity (1 / (1 − α) with α = 0.69), so a step
moves plant size by about 16%. That is wider than the 8% histogram bins, so some bins are empty and
others double up. Finer productivity grids smooth the no-rule line (roughness 0.68 to 0.48), and a finer
size grid smooths it further (0.22).

**How do we know the remaining bunching is the policy, not numerical error?**
1. The step ratio (density just past a cap step ÷ just before it) stays at 1.5–2.1 under today's rule on
   every grid, from 24 × 11 to 96 × 41 with 1,280 size points. Without the rule it stays at 0.65–0.98 on
   the same grids. Grid error would not line up exactly with the cap steps, and it would show up in both
   lines.
2. Roughness of the current-rule line levels off near 0.6 on fine grids, while the no-rule line keeps
   falling to 0.2. The jumps that remain are at the steps.
3. The mechanism is visible directly: the top-1% plant sits at h = 150.00015, just past the 150 step
   (section 2).

Caveat: the finer-grid runs hold prices at the 48 × 21 solution, so they check the shape of the
distribution, not the +0.33%.

## 6. Prof. Hur's main concern

**Are plants limited by the cap, the quota, or something else?**
- *In the model:* the quota, through θ. 82% of users are at θ × cap, 98% would hire more, and **none
  reach the legal cap**. The legal cap decides only how the quota is shared. This is an assumption: the
  quota is assumed to bind.
- *In the survey (2019, 772 EPS users):* the cap binds for a minority. 17.6% are at or above the 2019
  cap. Average use is 62% of the cap, and 42% are below half. Only 44% would hire more with no limit. Firms
  far below their cap want more almost as often (41%) as firms at the cap (50%), so for most firms
  something other than the cap limits them. That could be the quota and the points ranking, the 3–6
  new permits per round, or simply demand. With the 2024 caps on the same firms, only about 1% would go
  past the cap.
- *Quota:* a December 2024 projection put E-9 arrivals near 80,000 against a 165,000 quota, so it may
  not bind every year. Low-scoring firms were still waitlisted in 2026.
- We can't tell these apart yet. The Ministry disclosure request asks for exactly this.

**Which conclusions come from the data, and which from assumptions?**

From data (targeted or checked):
- Plant sizes, exit rate, share of plants with 50+ workers (census).
- 36.9% average EPS share and 20.8 workers at EPS plants (Lee, Peri and Yang): model 37.2% and 21.4.
- Extra closures after the 2020–21 stop, slope 0.152: model 0.150 (0.05 on the finer grid).
- The pattern of EPS use by size matches, but the model has too many very small users, and EPS shares
  are too low from 20 workers up (18% against 26% at 20–49).
- Survey cap use and wanting more: used as checks, and they contradict the model.

From assumptions (the model produces them):
- The premium curve, which decides who uses EPS and the 28-worker cutoff.
- Perfect substitutes, which is why large plants don't grow.
- The 10.8% manual-intensive share, which decides the 10.7% of plants using EPS. It is calibrated, not
  measured.
- A binding quota, shared in proportion to the cap with one θ.
- Every policy result: −0.9% gross, +0.33% net, equal limit +1.0% / +0.19%.

**The main limitations to say openly**
1. **The net gain is small and sits at our own kill line** (0.09–0.10 of a 50% larger quota). It moves
   with the grid (+0.33% to +0.37%; equal limit +0.19% to +0.09%).
2. **The net gain depends on how costs are counted.** It treats the Korean premium as a real cost, and
   it mostly comes from saving the fixed costs of manual-intensive plants that close.
3. **The premium curve is not measured**, and the robustness rows are not recalibrated.
4. **Perfect substitutes** decides the large-plant result. Employers rate EPS workers at 74–96% of a
   Korean worker, and that is not in the model.
5. **The cap uses h, not h + k.** The largest plants would be ineligible under the law.
6. **One θ and a binding quota contradict the survey.** In the model 98% of users want more; in the
   survey 44% do.
7. **Two targets have no recorded source:** EPS workers as 5.5% of all workers, and 10% of plants using
   EPS.
8. **The closure slope matches only on the calibration grid** (0.15 against 0.05 on the finer grid), and
   σ of productivity shocks sits at its lower bound.
9. **Only steady states are compared.** There is no transition, Korean labor supply is fixed, EPS workers
   are paid the Korean wage, and permit revenue is not given back to anyone.
