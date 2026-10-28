# Project log — ISA6327 Topics in Macroeconomics (Fall 2026)

Team: Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo
Instructor: Prof. Sewon Hur

This log records what we did, what we found, and what each result meant for the
project, day by day. The team worked with the AI assistant Claude (Anthropic),
used for literature search, fact-checking, coding, model runs and drafting, in
line with the course AI policy. All numbers below were produced by the code in
this repository or verified against the cited sources; anything not verified is
marked as such.

**Where things stand (Oct 28):** we are pursuing **Idea 1, Korea's Employment
Permit System (EPS)**. After Prof. Hur's Oct 27 feedback, model version 5 gives
plant productivity a Pareto tail and lets plants bunch at the cap steps, which they
now do. In this version, allocating the same number of guest workers *without* the
size-based rule raises manufacturing net output by about **1.0%**, about a quarter
of what a 50% larger quota would achieve (+4.0%). Version 4, presented on Oct 27,
gave 0.4% because its plants were too small to reach the cap steps. The model's
response to the 2020–21 EPS sudden stop still matches Lee, Peri and Yang's (2026)
estimate. Robustness is the main remaining work. The research proposal (submitted
Oct 23, with the version-4 numbers) is in `proposal/`.

---

## Contents

- [Sep 29 — Finding a question that has not been answered](#sep-29)
- [Oct 8 — Comparing four candidate ideas](#oct-8)
- [Oct 11 — Building the pitch deck](#oct-11)
- [Oct 13 — Presentation script and GitHub setup](#oct-13)
- [Oct 14 — Prof. Hur's feedback: checking the data for bunching](#oct-14)
- [Oct 15 — Building and calibrating the EPS model](#oct-15)
- [Oct 18–19 — Recalibration and the research proposal](#oct-18)
- [Oct 27–28 — Presentation feedback and model version 5](#oct-27)
- [What worked and what didn't](#what-worked)
- [Open questions and next steps](#next-steps)
- [Files and data](#files)

---

<a id="sep-29"></a>
## Sep 29 — Finding a question that has not been answered

**Goal.** The professor said the low bar is recalibrating a lecture model to
another country (the "ladder of feasible projects", Week 2 slide 60). We aimed
for rung 4: add a feature to a lecture model so it answers a question the papers
have not.

**What we did and found.**

| Candidate | Literature check | Verdict |
|---|---|---|
| Demographic decline → falling firm entry in Korea (AHKR model) | Lim (2026, *Economic Modelling*) already does Korea; HNS (2022), Karahan–Pugsley–Şahin (2024), Engbom do the US | Taken |
| Immigration as a policy lever in Carroll–Hur–İmrohoroğlu–Strackman's Korea OLG model | İmrohoroğlu–Kitao–Yamada (2017) did the Japan version; Kim–Han–Hong (2022) did a Korean heterogeneous-agent OLG with immigration | Close to a country swap |
| **EPS guest workers as a size-dependent policy in Hopenhayn/AHKR** | Lee–Peri–Yang (2026, NBER WP 34927) is reduced-form and calls for long-run, firm-dynamics work; Mandelman–Mehra–Shen (2025, *JME*) model H-1B frictions, not size-based | **Open** |

Facts verified for EPS:
- Eligibility: manufacturing plants with fewer than 300 regular workers or capital ≤ ₩8bn (or an SME certificate).
- Caps by number of Korean insured workers, 2024 standard (eps.go.kr): Koreans+10 (1–10), 30 (11–50, at most 2× Koreans), 35, 40, 50, 60 (201–300), 80 (301+). Roughly double the 2019 schedule in Lee–Peri–Yang Table 4.
- Firms hire EPS workers because they cannot find Koreans, not to save costs: 82.6% vs 13.4% (KBIZ 2025 survey); 53% of Lee–Peri–Yang's firms report "no applicants".
- E-9 quota: 52k (2021) → 69k → 120k → 165k (2024).

**What it meant.** EPS became our main candidate. A key modeling lesson: model EPS as
*access* to labor (a quantity limit), not as a cheaper wage.

---

<a id="oct-8"></a>
## Oct 8 — Comparing four candidate ideas

The team had four ideas. We checked each against existing work:

| Idea | Finding | Verdict |
|---|---|---|
| 1. EPS: quantity vs. allocation | No structural model of the EPS rule found | Keep |
| 2. Card-fee tiers for small merchants (0.40% up to ₩300m, 1.00%, 1.15%, 1.45% up to ₩3bn) | No study of bunching or growth at these thresholds found | Keep |
| 3. Who lost purchasing power in Korea's 2026 episode (KOSPI ~+100%, won at a 17-year low, CPI 3.2%, BOK hikes) | Existing redistribution methods (Auclert 2019; open-economy HANK) applied to a new episode; rung 4 only with Korea-specific features (57.3% variable-rate household loans, 14.4m stock owners) | Weaker novelty |
| 4. K-ETS free permits and firm exit | Dardati (2016, *IER*) and Fowlie–Reguant–Ryan (2016, *JPE*) already model permit allocation in firm dynamics | Country swap only |

**What it meant.** Ideas 1 and 2 are the most novel. All four are "calibration"
projects; ideas 3 and 4 add features that published papers already have.

---

<a id="oct-11"></a>
## Oct 11 — Building the pitch deck

The team ranked the ideas 3, 1, 2, with 4 as the country-swap backup. We built a
10-slide pitch deck: <https://claude.ai/artifact/232yGbzBu7EdLqBGKQZ3jE>

- For each idea: question and motivation, then the model for calibration with
  equations in the lecture notation and a parameter → target → source table.
- Equations colour-coded: navy = lecture model (Hopenhayn Week 2, Aiyagari Week 3),
  orange bold = our addition; new parameters marked with an asterisk.
- Contribution and expected outcome (as hypotheses) added for each idea.
- Facts on every slide were checked against sources before being added.

---

<a id="oct-13"></a>
## Oct 13 — Presentation script and GitHub setup

- Wrote a speaker script for the EPS slides (5–6): short on motivation, longer on
  the equations and why each calibration target identifies its parameter
  (e.g. the CES substitution parameter ρ is pinned down by Lee–Peri–Yang's
  closure response). Equations on slide 6 numbered (1)–(6).
- Created this private repository and moved the course code into it. Lecture
  slides and the syllabus are excluded (instructor's materials).

---

<a id="oct-14"></a>
## Oct 14 — Prof. Hur's feedback: checking the data for bunching

**Feedback.** EPS and card fees are the most promising (both have a policy
threshold firms respond to). Check the data, with attention to bunching issues
for the card-fee thresholds.

**Data.** Downloaded MDIS public-use microdata (Statistics Korea):
- 소상공인실태조사 (small-business survey): survey-based 2018–2020, register-sampled 2020–2024. Annual sales (millions of won) are in 2018–2023.
- 전국사업체조사 (business census), 2000–2024, all establishments. No column names; we identified the columns from accounting identities (total workers = male + female).
- Raw files are kept **outside** the repository (on a team member's computer, outside the shared folder) under the MDIS terms of use (no sharing, delete after use, cite the source). Only aggregate numbers appear here.

**Method.** Standard bunching estimator (Kleven–Waseem): count firms in 1-unit
bins, fit a smooth polynomial with dummies for round numbers, and measure excess
firms just below each threshold. Code: `bunching/`. Full tables: `bunching/RESULTS.md`.

**Results.**

| Threshold | Estimate | Reading |
|---|---|---|
| Card fees ₩300m | b = 0.87 (se 3.58) register; 3.74 (se 4.52) survey | No bunching |
| Card fees ₩500m | b = 1.19 (2.06); 0.40 (2.61) | No bunching |
| Card fees ₩1bn | b ≈ 21–27 | Round-number reporting, not policy (same spike at ₩2bn, which has no threshold) |
| 2019 reform at ₩500m (notch shrank from ~2.05% vs 1.3% to 1.4% vs 1.3%) | 2018: −0.20; 2019–20: 0.82 | No change |
| EPS cap steps (10, 30, 50, 100, 150, 200 workers), before vs after EPS (2004) | all ≈ 0 | No bunching, but a weak test |

Problems we hit:
- ₩300m is also retail's double-entry bookkeeping threshold, so retail bunching would be confounded; restaurants are cleaner.
- Sales are self-reported and heavily rounded (38–48% are multiples of ₩10m).
- The EPS cap counts *Korean* insured workers; the census counts all workers, including the EPS workers, which blurs any bunching.

**What it meant.** The card-fee test is clean and finds nothing: the fee tiers
probably barely affect merchant size, which would make for a weak paper. The EPS
null is uninformative. Prof. Hur later clarified that bunching was the concern
for card fees only. We moved forward with **EPS**.

---

<a id="oct-15"></a>
## Oct 15 — Building and calibrating the EPS model

**Question.** Does allocating EPS workers by plant size cost productivity, or
is the effect too small to matter (the project's kill condition)?

### Version 1 — first pass (did not work)

Hopenhayn model with Korean and EPS labor (CES), the 2024 cap, fixed Korean
labor supply and EPS quota, general equilibrium.

- Result: size-neutral allocation changed output by ≈ 0%; quota ±50% by ±3–6%.
- **Why it can't be trusted:** (1) almost no endogenous exit (the exit cutoff sat at the bottom of the productivity grid; 93% of exits exogenous), so the "keeps weak plants alive" channel was switched off; (2) EPS users were large plants using EPS lightly (7–9% EPS share vs 37% in the data).

### Version 2 — endogenous exit (worked)

Re-calibrated the firm side (returns to scale α = 0.69 among others): plant size
7.54 (data 7.5), share with 1–4 workers 0.68 (0.70), exit 8.0% (8%), with most
exits endogenous. (We later found the exit-rate formula was mis-specified; it is
fixed in version 4.)

### Version 3 — task-based production and quantity rationing (partly worked)

- Core work by Koreans; manual work by EPS workers or Korean manual workers, who
  carry a recruiting premium that is largest for small plants ("no applicants").
- Diagnosis: EPS users still sat far above the exit cutoff, because the model let
  them replace EPS workers cheaply.
- Fix that matches the institution: plants pay EPS workers about a Korean wage
  (₩2.93m incl. room and board vs ₩2.6m) and the quota is rationed by
  **quantity** (each plant gets a share θ of its cap, as under the points
  system), so plants keep the value of access.

### Version 4 — two plant types and smooth exit (current version)

- Entrants become a light type or a manual-intensive type (higher fixed costs,
  heavy manual work: casting, plastics, textiles). This lets mid-sized,
  EPS-dependent plants be fragile, as Lee–Peri–Yang find.
- A small logit taste shock in the exit decision makes exit smooth, so the
  optimizer can fit all targets at once. Exit rate now computed from the
  steady-state identity (exits = entrants).
- Calibrated 13 parameters (random search, local search, Nelder–Mead) to plant
  size, share of 1–4 worker plants, exit, EPS users, EPS share among users,
  users' size, and Lee–Peri–Yang's closure response.

*Note: the Oct 15 numbers below are superseded by the Oct 19 recalibration (next section).*

**Fit (best saved calibration, `local_best.json`):**

| Moment | Model | Data |
|---|---|---|
| Share of plants with 1–4 workers | 0.68 | 0.70 |
| Exit rate | 8.7% | 8% |
| Share of plants using EPS | 7.8% | 10% |
| EPS users' average size | 14.5 | 13 |
| Average plant size | 5.7 | 7.5 |
| EPS share among users | 28% | 37% |
| Closure slope, Lee–Peri–Yang design, shock expected 2 years | 0.116 | 0.124–0.177 |
| Closure slope, same, shock expected 5 years | 0.154 | 0.124–0.177 |

**Experiments (net output, relative to the current rule):**

| Experiment | Net output | Notes |
|---|---|---|
| No EPS | −8.3% | |
| **Same quota, allocated without the size rule (by price)** | **+1.0%** | EPS concentrated in fewer plants (3.9% vs 7.8% of plants); manual-intensive plants fall from 8.5% to 5.8% of plants |
| Quota +50% | +3.9% | |
| Quota −50% | −3.9% | |

An earlier, rougher version-4 calibration gave +0.8%, so the sign and size are
stable so far.

**What it meant.**
- The kill condition is **not** triggered: the allocation effect is about 1% of
  manufacturing net output, a quarter of a 50% quota expansion, at no cost in workers.
- The mechanism is the one in our pitch: the size rule spreads EPS workers across
  many small plants and keeps more manual-intensive plants alive.
- A lesson about comparisons: we first measured the closure response over all
  plants with the actual EPS share and got 0.054, which looked like the model
  could not explain Lee–Peri–Yang's closures. Measured their way (EPS users only,
  statutory "imputed" exposure), it is 0.116–0.154, within or just below their
  range. The gap came from our comparison, not from their estimate.

---

<a id="oct-18"></a>
## Oct 18–19 — Recalibration and the research proposal

**Proposal requirements** (handout): 2–3 pages single-spaced excluding references,
PDF, due **Fri Oct 23, 11:59 PM** on LearnUs; groups of up to 4 unless approved by
the instructor (our team has 5, so approval is needed). Required sections: idea and
motivation, literature (3–5+ papers and the gap), contribution, methodology (model
approach preferred), references. We drafted the proposal (`proposal/`), using the
progress-update deck as source material.

**Why recalibrate.** The Oct 15 calibration targeted the closure response measured
over all plants with the actual EPS share, which is not what Lee, Peri and Yang
estimate, and it used the 2024 caps for a shock that happened under the 2019 caps.
Under the 2019 caps, that calibration's closure slope (their design) was only 0.027,
so the earlier statement that the model "reproduces" their closures was not correct.

**What changed.**
- Closure target measured their way: EPS users only, statutory (imputed) exposure, target 0.15.
- The 2020–21 shock and the EPS share among users (measured Jan 2020) are computed
  under the **2019 cap schedule** (Lee–Peri–Yang Table 4); other moments under the 2024 schedule.
- Local search, then Nelder–Mead from the Oct 15 best; loss fell from 0.84 to 0.36.

**Fit (`recal_best.json`):**

| Moment | Model | Data |
|---|---|---|
| Average plant size | 5.9 | 7.5 |
| Share of plants with 1–4 workers | 0.66 | 0.70 |
| Exit rate | 6.3% | 8% |
| Share of plants using EPS | 7.2% | 10% |
| EPS users' average size | 16.1 | 13 |
| EPS share among users (2019 caps) | 29% | 37% |
| Closure slope, their design, 2-year shock | 0.107 | 0.124–0.177 |
| Closure slope, their design, 5-year shock | 0.195 | 0.124–0.177 |

**Experiments (net output vs. the current rule, `eps_results_recal.json`):**

| Experiment | Net output | Notes |
|---|---|---|
| No EPS | −7.5% | |
| **Same quota, no size rule (by price)** | **+0.42%** | EPS users 3.5% of plants (vs 7.2%); manual-intensive plants 5.7% (vs 7.7%) |
| Quota +50% | +3.7% | |
| Quota −50% | −3.8% | |
| 2019 caps instead of 2024, same quota | −0.02% | With a binding quota, the cap schedule hardly matters |

**What it meant.**
- The allocation gain is smaller than first estimated (0.4% vs 1.0%) but rests on a
  calibration that fits the closure evidence better. It is about one-ninth of the
  quota effect, just above the kill threshold we set (one-tenth).
- The model's closure response brackets Lee–Peri–Yang's estimate between a 2-year
  and a 5-year expected shock.
- The magnitude is sensitive to calibration, so robustness is the core of the remaining work.

**Kill condition (adopted in the proposal):** if the allocation gain is not positive
across robustness checks (substitution parameter, expected shock length, cap
schedule), or falls below one-tenth of the gain from a 50% quota expansion, we
refocus on the quantity margin.

**Final proposal (Oct 19, `proposal/proposal.pdf`):** A4, 11pt, single-spaced,
1-inch margins; body on pages 1–3, references on page 4. All 12 references checked
against publisher and RePEc records; Korean sources cited with their original
titles; the statistics agency cited under its current name (Ministry of Data and
Statistics, 국가데이터처). Includes the kill condition above, the course-ladder
framing (we extend Hopenhayn 1992; AHKR was reproduced, not extended), and a link
to this repository. Due Fri Oct 23, 11:59 PM, uploaded to LearnUs by one member.

**Figures and table added (Oct 19):** Figure 1 plots the maximum foreign-worker share
by plant size under the 2019 and 2024 caps; Table 1 lists the counterfactuals;
Figure 2 shows where the EPS workers go in the model. Under the current rule, 20% of
EPS workers are at plants with fewer than 5 Korean workers and 17% at plants with
20 or more; with the same quota and no size rule, these become 0% and 46%, and output
per worker at plants using EPS is 5.5% higher. Figures are built by
`proposal/make_fig.py`; Figure 2's numbers come from `eps_model/eps_by_size.py`.

**A concern raised in the team** (that both final ideas had limited sources and
might not show significant effects): confirmed for card fees (no bunching), not for
EPS. The EPS result is a model counterfactual, so its uncertainty comes from
calibration and robustness rather than statistical significance.

---

<a id="oct-27"></a>
## Oct 27–28 — Presentation feedback and model version 5

**Prof. Hur's feedback on the Oct 27 update**:
- The census bunching test is *inconclusive*, not evidence against bunching: the
  data cannot separate Korean and foreign workers.
- With continuous hiring and a size-based cap, profit-maximizing plants should bunch
  at the cap steps. "If not in the data, you should definitely see it in the model";
  if the model shows none, it is not doing something correctly.
- To get more large plants without changing the average size, use a fatter tail.
  His model draws productivity from a Pareto distribution; ours had no tail parameter.
- The 0.4% looked small to him. If plants bunch, removing the size rule lets them grow
  to their optimal scale, so he expected a bigger result.
- He asked whether the quota experiments change the population (they do: Korean
  labor is fixed and EPS workers are added or removed) and whether the wage is solved
  in general equilibrium (it is: free entry pins the Korean wage). He warned that
  unstated assumptions may have been made by the AI without the team knowing.

**Diagnosis of version 4.** It showed no bunching. The largest plant had about 81
Korean workers, so the steps at 100, 150, 200 and 300 were never reached; near 50 the
size grid was too coarse (41, 49, 51, 58 workers); and with plants getting about a
fifth of their cap, crossing 50 was worth about one EPS worker.

**Version 5** (`eps_model_v5.py`, `run_v5.py`):
- Productivity is s = x·z: x is permanent, drawn at entry from a Pareto distribution
  with tail parameter γ (as in AHKR); z is the version-4 persistent shock. γ replaces ν_top.
- The size grid includes every cap step and a point just past it, and a point just
  under 300, so a plant can locate exactly where the rule rewards it.
- New target: the share of plants with 50 or more workers (2.1%, census 2024).
- Faster solver (dominated grid points pruned; Brent's method), which allowed a
  parallel local search (8 candidates per round) and Nelder–Mead. Nelder–Mead was
  stopped by hand on Oct 28, when improvements had fallen below 0.01.

**Fit (`v5_best.json`, loss 0.150 on 8 targets; version 4: 0.36 on 7):**

| Moment | v5 | v4 | Data |
|---|---|---|---|
| Average plant size | 7.8 | 5.9 | 7.5 |
| Share of plants with 1–4 workers | 0.65 | 0.66 | 0.70 |
| Plants with 50+ workers | 1.6% | 0.5% | 2.1% |
| Exit rate | 9.1% | 6.3% | 8% |
| Share of plants using EPS | 9.6% | 7.2% | 10% |
| EPS users' average size | 15.1 | 16.1 | 13 |
| EPS share among users (2019 caps) | 30% | 29% | 37% |
| Closure slope, their design, 2-year shock | 0.140 | 0.107 | 0.124–0.177 |

Calibrated γ = 4.43. ρ = 0.797 sits at the upper edge of its range (0.8) and ξ = 0.10
at the lower edge; both need a robustness check.

**Bunching in the model (`v5_results_fine.json`, `bunching_v5.png`).** Under the
current rule there are 1.5–1.7 times as many plants just past each cap step (50, 100,
150, 200) as just before it, and plants pile up just under 300 (0.56 times as many
just past it). With the same quota and no size rule the ratios are about 1
(0.79–1.03). This check uses four times as many productivity levels as the
calibration, because with the coarser grid a single productivity level can land on
a step by chance.

**Experiments (net output vs. the current rule, `v5_results.json`):**

| Experiment | v5 | v4 |
|---|---|---|
| No EPS | −8.8% | −7.5% |
| **Same quota, no size rule (by price)** | **+0.99%** (+1.01% with the finer grid) | +0.42% |
| Quota +50% | +4.0% | +3.7% |
| Quota −50% | −4.2% | −3.8% |
| 2019 caps instead of 2024, same quota | −0.13% | −0.02% |

Without the size rule, EPS users fall from 9.6% to 4.2% of plants and their average
size rises from 15 to 25 workers; the Korean wage is 2.6% lower (0.697 → 0.679).

**What it meant.**
- Prof. Hur's prediction holds: once plants can bunch, removing the size rule gives
  a larger gain, more than double version 4's, and about a quarter of a 50% quota
  expansion, well above the kill threshold (one-tenth).
- The histogram he asked for is now a model prediction that the data could test, if
  EPS counts by number of Korean workers become available.
- The proposal (submitted Oct 23) reports the version-4 numbers.

---

<a id="what-worked"></a>
## What worked and what didn't

**Worked**
- Checking every candidate question against the literature before investing in
  it. It ruled out two ideas that looked new but were not (demographics/entry, immigration OLG).
- Verifying policy facts at the source (eps.go.kr, FSC, MDIS) before putting them on slides.
- Diagnosing each failed model version instead of tuning around it. Each fix
  (endogenous exit, quantity rationing, two plant types) came from a specific
  mismatch with the data.
- Matching the empirical design when comparing with a paper (Lee–Peri–Yang's
  sample and exposure measure).
- Keeping licensed microdata outside the shared folder and the repository.

**Didn't work, or cost time**
- Version 1 of the model: missing endogenous exit and the wrong EPS users made the allocation effect look like zero.
- Rationing the quota by a price: it handed the value of EPS access to the "seller", so losing EPS cost plants almost nothing.
- Coarse grids with strict exit decisions: the closure response jumped between 0 and 0.2 and the optimizer stalled. Fixed with a logit exit shock.
- An exit-rate formula error in versions 1–3 (fixed in version 4).
- Comparing our model's closure slope with Lee–Peri–Yang's on a different basis, which briefly led to a wrong conclusion that credit constraints were needed.
- Using today's (2024) caps for the 2020 shock, which overstated the model's closure response (0.116 vs 0.027 under the 2019 caps) until the recalibration fixed it.
- Bunching tests with public data: card-fee sales are self-reported and rounded; the census cannot separate Korean and foreign workers.

---

<a id="next-steps"></a>
## Open questions and next steps

1. ~~Recalibrate with the closure target measured Lee–Peri–Yang's way and the 2019
   caps~~ — done Oct 19.
2. **Remaining fit gaps (version 5):** plants with 50+ workers (1.6% vs 2.1%), EPS
   share among users (30% vs 37%), EPS users' size (15 vs 13). ρ (0.797, bound 0.8)
   and ξ (0.10, bound 0.1) sit at the edge of their ranges.
3. **Robustness (decides the kill condition):** CES parameter ρ, shock length (2 vs 5
   years), cap schedule, the exit taste-shock scale, and the Pareto tail γ.
4. **State the model's assumptions explicitly** (Prof. Hur, Oct 27): no households
   (no consumption, saving or remittances; we measure output, not welfare), fixed
   Korean labor, EPS workers paid a Korean wage, the Korean manual premium as a
   resource cost, the cap on core Koreans h rather than h + k, equal θ for every plant,
   the permit fee as a transfer, steady-state comparisons only.
5. **Data for the bunching test:** EPS workers by number of Korean workers per plant
   (MOEL, HRD Korea and KEIS hold the records; only aggregates are public).
6. **Optional extensions:** a COVID demand shock in the closure experiment; credit
   constraints (links to Song–Storesletten–Zilibotti and our rung 4 code); a
   counterfactual with size-neutral *rationing* (points without the cap) besides allocation by price.
7. **Check with Prof. Hur:** quantity rationing vs. price wedge; whether
   identifying the model from the COVID shock (instead of bunching) is acceptable.
8. Verify the exit-rate target (8%) against KOSIS business demography statistics.

---

<a id="files"></a>
## Files and data

| Path | Contents |
|---|---|
| `hopenhayn_project/eps_model/eps_model.py` | EPS model (version 4) |
| `hopenhayn_project/eps_model/run_eps.py` | Calibration and experiments |
| `proposal/` | Research proposal (Markdown source, CSS, PDF; `make_fig.py` builds Figures 1–2) |
| `hopenhayn_project/eps_model/eps_model_v5.py`, `run_v5.py` | EPS model version 5 (Pareto tail, bunching-ready size grid): calibration, experiments, bunching check |
| `hopenhayn_project/eps_model/v5_best.json` | **Current** calibration (Oct 28, version 5, 13 parameters) |
| `hopenhayn_project/eps_model/v5_results.json`, `v5_results_fine.json` | Version-5 fit, experiments and bunching; the finer-grid check |
| `hopenhayn_project/eps_model/make_bunch_fig.py`, `bunching_v5.png/.svg` | Bunching histogram in the model, current rule vs. no size rule |
| `hopenhayn_project/eps_model/recal_best.json` | Version-4 calibration (Oct 19; numbers in the proposal and the Oct 27 slides) |
| `hopenhayn_project/eps_model/eps_results_recal.json` | Fit and experiment results for the version-4 calibration |
| `hopenhayn_project/eps_model/eps_by_size.py`, `eps_by_size.json` | EPS workers by plant size, current rule vs. no size rule (Figure 2) |
| `hopenhayn_project/eps_model/local_best.json` | Oct 15 calibration (superseded) |
| `hopenhayn_project/eps_model/experiments_localbest.json` | Oct 15 experiment results (superseded) |
| `hopenhayn_project/eps_model/top_draws.json` | Top 20 draws from the version-4 random search |
| `hopenhayn_project/eps_model/NOTES.md` | Model notes and how to rerun |
| `bunching/` | Bunching estimator, census histogram script, `RESULTS.md` |
| `hopenhayn_project/rung1_hopenhayn/`, `ahkr_model/` | Earlier Hopenhayn/AHKR ladder exercises |
| `course_exercises/aiyagari_replication/` | Aiyagari (1994) Table 2 replication (Week 3 exercise; not part of the EPS project) |

Data source: Statistics Korea, MDIS — 소상공인실태조사 (2018–2024) and
전국사업체조사 (2000–2024). Raw files are not in this repository; teammates who
need them should download them with their own MDIS account.

### Where the MDIS data is stored

The raw MDIS files (downloaded Oct 14, 2026, public-use versions) are stored locally
in **`~/MDIS_data`** on the Mac used for the analysis. That folder is outside the
shared course folder and outside git, and only that computer's user account can
open it. The scripts in `bunching/` read the files from there.

| File | Contents |
|---|---|
| `연간자료_조사기반_20261014_62010_데이터.zip` | 소상공인실태조사, survey-based, 2018–2020 (with column names) |
| `연간자료_등록기반_20261014_38507_데이터.zip` | 소상공인실태조사, register-sampled, 2020–2024 (with column names; sales in 2020–23) |
| `연간자료_20261014_52894_데이터.zip` | 전국사업체조사 2000–2004 (no column names) |
| `연간자료_20261014_03868_데이터.zip` | 전국사업체조사 2005–2009 |
| `연간자료_20261014_78290_데이터.zip` | 전국사업체조사 2010–2014 |
| `연간자료_20261014_40487_데이터.zip` | 전국사업체조사 2015–2019 |
| `연간자료_20261014_14068_데이터.zip` | 전국사업체조사 2020–2024 |
| `agg_mfg_size_hist.csv` | Our aggregate output: manufacturing plant counts by size, 2000–2024 (no individual records) |

MDIS terms of use: no disclosure of individual records, use only for the stated
purpose, no sharing or copying, cite the source, and **delete the raw files when
the project ends**.
