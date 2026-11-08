# Project log — ISA6327 Topics in Macroeconomics (Fall 2026)

Team: Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo
Instructor: Prof. Sewon Hur

This log records what we did, what we found, and what each result meant for the
project, day by day. The team worked with the AI assistant Claude (Anthropic),
used for literature search, fact-checking, coding, model runs and drafting, in
line with the course AI policy. All numbers below were produced by the code in
this repository or verified against the cited sources; anything not verified is
marked as such.

**Where things stand (Nov 2):** we are pursuing **Idea 1, Korea's Employment
Permit System (EPS)**. The proposal received an A+. We found firm-level EPS data (772
manufacturers) and corrected three calibration targets that did not match how Lee,
Peri and Yang measure them. Allocating the same number of guest workers *without* the
size-based rule now raises manufacturing net output by about **0.33%** (0.37% on a finer
grid), which is 0.089 (0.101) of what a 50% larger quota would achieve. That is at the
kill threshold of one-tenth, and robustness checks will decide. Two open problems: the
closure slope matches only on the calibration grid (0.15, against 0.05 on the finer
grid), and the model bunches far more than the data at the low cap steps. Version 5's
1.0% used the targets now corrected. The research proposal (submitted Oct 23, with the
version-4 numbers) is in `proposal/`.

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
- [Oct 29–Nov 1 — Proposal comments, the EPS survey and corrected targets](#nov-1)
- [Nov 3 — Presentation feedback: understand the model first](#nov-3)
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

<a id="nov-1"></a>
## Oct 29–Nov 1 — Proposal comments, the EPS survey and corrected targets

**Prof. Hur's comments on the proposal** (Oct 29): A+. He questioned the cap numbers
and Figure 1, and asked us to re-check the schedule and redraw the figure. He noted
that H-1B frictions may in practice depend on firm size, since visa processes can be
daunting for small firms. He liked re-creating Lee, Peri and Yang's experiment inside
the model, and struck out the sentence on the card-fee test.

**Cap schedule.** eps.go.kr confirms the code and Figure 1: Koreans + 10 for 1–10
Korean workers; 30 for 11–50, at most twice the Korean workers; then 35, 40, 50, 60.
The proposal's sentence left out the limit. So 10 Koreans may hire 20 (67%) and 11 may
hire 22 (67%); 30 is first reached at 15.

**New data.** The replication file of Dong, Lee and Yang (2024, *Oxford Economic
Papers*) holds the KDI–World Bank survey behind Lee, Peri and Yang (2026): 772
manufacturers from a stratified sample of 51,619 EPS firms, fielded August–October
2019, with a 27.6% response rate. It has EPS and Korean workers per firm, wages, dorm and meal costs and
how many more EPS workers the firm wants. It covers EPS users only, under the 2019
caps; the January 2021 wave is not in the file. Script: `bunching/eps_survey.py`;
the file stays in `~/EPS_data`, and only aggregates are reported.

| From the survey | Value |
|---|---|
| Workers per firm: total, Korean, EPS | 20.5, 15.5, 5.0 |
| EPS share: simple average; employment-weighted | 37.8%; 24.4% |
| Share of the 2019 cap used: mean; by size bin | 62%; 58–74%, about 60% in most |
| Under half the cap; at or above it | 42%; 18% |
| Would hire more with no limit | 44% |
| Wage plus dorm and meals vs. Korean wage | 96% |
| EPS productivity (Korean = 100), by experience | 74, 87, 96 |

Dong, Lee and Yang also describe rules the model lacks: firms ranked by points with a
cut-off, and at most 3–6 new permits per round.

**Bunching in the data.** The survey counts Korean workers, which the census could not.
Counts dip at 5 and jump at 6, where the 2019 cap rises from 5 to 7: 1.4–1.6 times a
smooth trend (z = 2.1–2.9). There is no clear spike past 10, 30 or 50, and counts of
14 and 15, which are not steps, reach similar z. This is suggestive only: users only,
few firms past 50.

**Corrected targets** (`run_v6.py`; the model code is unchanged). All three are now
computed under the 2019 caps:

| Target | Before | Now |
|---|---|---|
| EPS share at EPS firms | Employment-weighted, against 37% | Simple average across firms, against 36.9% |
| EPS firms' size | Total workers against 13, under 2024 caps | Total workers against 20.78 |
| Closure slope | No size control, against 0.15 | Average of size-bin and cubic controls, against 0.152 (their Table 6, cols 4–5) |

| Moment | Data | v5 parameters, corrected measures | Recalibrated |
|---|---|---|---|
| EPS share at EPS firms | 36.9% | 45.0% | 37.2% |
| Workers per EPS firm | 20.8 | 15.0 | 21.4 |
| Closure slope, size controls | 0.15 | 0.25 | 0.15 (finer grid: 0.05) |
| Plants with 1–4 workers | 0.70 | 0.65 | 0.75 |
| Average plant size | 7.5 | 7.8 | 8.1 |
| Plants with 50+ workers | 2.1% | 1.6% | 1.8% |
| Exit rate (assumed) | 8% | 9.1% | 8.1% |
| Plants using EPS | 10% | 9.6% | 10.7% |

Loss on these targets: 0.64 with the v5 parameters, 0.034 now. Search stopped by hand on
Nov 1 (0.0346 to 0.0336 in over an hour); final point in `v6_best.json`. ρ and ξ are no
longer at their bounds (0.65, 0.23). γ = 3.85.

**Results** (`v6_results.json`; finer grid, 48 × 21: `v6_results_fine.json`, `v6_fine_extra.json`):

| Experiment, net output vs. current rule | Version 5 | Corrected | Corrected, finer grid |
|---|---|---|---|
| Same quota, no size rule | +0.99% | +0.33% | +0.37% |
| Quota +50% | +3.97% | +3.72% | +3.65% |
| Quota −50% | −4.18% | −3.68% | −3.70% |
| No EPS | −8.84% | −7.22% | −7.25% |
| No size rule ÷ quota +50% | 0.25 | 0.089 | 0.101 |

**Bunching, model vs. data.** On the finer grid the model bunches at the upper cap steps
under the 2024 caps (density just past ÷ just below: 1.87, 1.92, 1.76, 1.60 at 50, 100, 150,
200), and this goes away without the size rule (0.76–0.91). At the low steps under the 2019
caps it bunches far more than the survey: 36% of EPS users sit just past 5 against 6–7%
of firms in the data, with almost none in between. A plant in the model faces no frictions and
every plant gets the same share of its cap, which may explain this.

**What it meant.**
- The gain is at the kill threshold of one-tenth (0.089 to 0.101, depending on the grid).
  We keep the threshold as set in the proposal; robustness and realistic rationing decide it.
- The closure slope with size controls relies on small differences within size bins, and it
  falls from 0.15 to 0.05 on the finer grid. It is within about 1.5 standard errors of their
  estimate (se about 0.07), but it is not a clean match. Re-fitting on a finer grid is next.
- The gain is a cost saving. Without the size rule, gross output falls 0.9% (1.6% in version 5),
  while fixed, entry and recruiting costs fall 5.5%, so net output rises. By source, with gross
  output = 100 (`v6_why_no_rule.py`, calibration grid): fixed costs −0.67, entry −0.20, the fixed
  cost of using EPS −0.17, recruiting premium −0.13.
- EPS users now get smaller without the size rule (22 to 14 workers); in version 5 they got
  larger (15 to 25), which we have not explained. In version 6 this is mainly who counts as a user:
  at the permit price (p = 0.34) a Korean manual worker is cheaper than an EPS worker once a plant
  has about 28 core Koreans, so plants past that stop using EPS (their share of EPS goes from 11%
  to 0). Manual-intensive plants as a group get larger (29 to 37 workers), partly because weak ones
  exit. Manual-intensive plants fall from 10.8% to 8.1%, and total plants by 0.9%.
- The no-size-rule experiment changes two things at once: it removes the link to size and it
  charges for permits that are free today (revenue about 1.5% of gross output, a transfer). The
  fall in manual-intensive plants, the largest source of saving, may come from the charge rather
  than from size-neutrality. Not yet separated: this needs size-neutral rationing with free permits.
- The ±50% quota results are nearly symmetric because net output is close to linear in the quota
  (`v6_quota_check.py`; both labor and quota markets clear). ±50% is about ±2.8% of all workers. On
  the calibration grid +50% slightly exceeds −50% (3.72 vs. 3.68), against diminishing returns; on
  the finer grid the order is as expected (3.65 vs. 3.70), so that reversal is grid noise. Steps of
  the same size differ by about 0.1 to 0.2 on the calibration grid, so 0.089 vs. 0.101 is not a
  clean difference.
- σ_s is at 0.051, next to its lower bound of 0.05. To check in the robustness runs.
- Equal rationing holds up on average: the model gives 49% of the cap and the survey 62%,
  roughly flat by size. It is too strong across firms, and in the model every user wants
  more, while 56% in the survey do not.
- The model's EPS firms are still too small in the middle: 10% with 20–49 workers vs. 25%.
- We still need outside data for all plants and the 2024 caps (MOEL, HRD Korea, KEIS), and for
  closures in the 2021 wave (Prof. Lee, Prof. Yang). We plan to raise this with Prof. Hur on
  Nov 3 before contacting anyone; nothing has been sent.

**Prof. Hur's written feedback on Oct 27:** look for administrative data on firm size and EPS
allocation; check that the model bunches and compare it with the data histogram; adjust the Pareto
parameter to match plants with 50+ workers; the COVID shock may help identify parameters. His
summary mentions about −0.5% from removing EPS; our Oct 27 slide showed −7.5%, which we correct
on Nov 3.

---

<a id="nov-3"></a>
## Nov 3 — Presentation feedback: understand the model first

**Prof. Hur's feedback** (our notes may not cover the end of the discussion):
- Before any policy experiment, understand the baseline: plot policy functions, and show which
  plants use EPS, which do not and why, which are at their optimal scale, and where they would be
  with no size restriction. Check that the model's EPS users look like the data's.
- Is the cap binding? How many firms are at or near it, by size, under 2019 and 2024? If no one is
  constrained, there is no paper. 18% at or above the cap is not small.
- He expected large, productive plants to be constrained, so removing the rule should raise their
  EPS use, their size and gross output. Our table shows the opposite, and he doubts it.
- The no-size-rule line in the bunching chart should be smoother; check for approximation error,
  and always compare on the same grid.
- Do not make the model more complicated. Do not get too worked up when the survey contradicts an
  assumption; survey answers are not always reliable.
- Each presentation needs a short refresher: the question, the model's ingredients, the data.
- Contact the Ministry and be persistent, using the formal request process. Do not say the work is
  for his class.
- He warned against reporting tables and slides from an LLM without understanding the model.

**What we can answer from the model** (`v6_why_no_rule.py`, calibration grid):
- Why only 10.7% use EPS: light plants, 89% of plants, have almost no use for manual work and none
  use EPS, while 99% of manual-intensive plants do. The user share (10.7%) is close to the
  manual-intensive share (10.8%), so it is set mostly by the type mix, not by the cap.
- Why large plants do not expand: the recruiting premium falls with size, so at the permit price
  plants with about 28 or more core Koreans prefer Korean manual workers. By assumption, EPS is worth
  most at small plants. This may be why the result runs against his logic. Not yet tested.

**Baseline diagnostics** (`baseline_diagnostics.py`, `make_baseline_figs.py`, `bunching/eps_binding.py`,
outputs in `hopenhayn_project/eps_model/baseline/`; the model and calibration are unchanged):
- In the model, 98% of users would hire more and 82% are at θ × cap (91% under 2019 caps), but none
  reach the legal cap. The quota does the limiting, through θ; the legal cap decides how it is shared.
- With free, unlimited permits at today's wage, manual-intensive plants would be 1.4 to 1.9 times
  larger, and demand would be 8.5 times the quota. In the survey, firms want 1.28 times what they have.
- Survey: 18% of firms are at or above the 2019 cap and 24% would go past it, at every size. With the
  2024 caps on the same firms and answers, both are about 1%. So the current legal cap may barely
  bind. Limits: 2019 firms and answers, users only, and the quota and ranking may still limit firms.
- Without the size rule only a middle band of plants uses EPS (productivity 1.4 to 2.7). The top 1%
  plant goes from 11 EPS workers to none and from 317 to 329 workers. Version 5's premium is flatter:
  plants stop using EPS only past about 2,000 core Koreans, and users got larger. We first thought
  the direction might depend on how fast the premium falls with size; the Nov 10 test below does not
  support that.
- "Every user wants more" on slides 31 and 37 is 98% in the model.

**Checks for Nov 10** (`v6_free_flat.py`, outputs `baseline/free_flat.json`, `premium_slope.json`,
`bumpy_line.json`; no parameter or feature changes; slides 39–53, generator in `presentations/nov10/`):
- Splitting the no-size-rule experiment. Same quota, free permits, one limit for every plant (3.9
  workers): gross output +1.0% (price version −0.9%), net +0.19%, or +0.09% on the finer grid (price
  +0.33%, +0.37%), which is 0.02–0.05 of a 50% larger quota, below the 0.10 line. 62% of EPS goes to
  plants with 0–5 Koreans, more plants survive and costs rise. The top 1% plant does not grow (317 to
  308). This changes the way permits are shared as well as the charge, so it does not isolate the charge.
- Premium slope, nothing recalibrated. Across six (ξ, ψ) pairs, including version 5's, gross output
  falls (−0.7% to −2.2%), net rises (+0.33% to +0.77%), and a top 1% plant changes size by at most
  about 7%. With version 5's premium it keeps EPS (10 to 69 workers) but stays at about 200 workers.
  Why: k and m are perfect substitutes and large plants' next worker is Korean, so a limited permit
  only saves money, and with more permits they swap rather than grow.
- The bumpy no-rule line is mostly grid error, as Prof. Hur suspected. With prices held at the 48 × 21
  solution, roughness falls from 0.68 to 0.22 on a 96 × 41 productivity grid with 1,280 size points,
  and changes of direction fall from 24 to 4. The current-rule line stays jagged (0.60), since its steps
  are real. Step ratios barely move (no rule 0.8–0.9, current rule 1.6–1.9). Full equilibrium was not
  solved on the finest grid.
- Quota: a Dec 2024 report projected about 80,000 E-9 workers against a 165,000 quota for 2024, across
  all sectors, so the quota may not always bind, contrary to the model. Low-scoring firms were still
  waitlisted in 2026 round 4. Ministry request text: `data_requests/moel_disclosure_requests.md`.

**Corrections to what was said in class.** The EPS share (36.9%) is the average, across EPS firms,
of EPS workers ÷ that firm's workers. It is not the share of workers in the economy (5.5%) or the
share of firms using EPS (10.7%). In the model, λ is the manual-work weight by plant type. The
statements that firms may go above the cap by request, by at most 3–6, or only past 300 Korean
workers have no source we can find; 3–6 is the limit on new permits in Dong, Lee and Yang's Table 1.

**Nov 8: slides checked against Prof. Hur's written feedback.** Presenters: Sara 39–41, Donny 42–45,
Julian 46–48, Benjamin 49–52, Mimi 53. Added to the slides and notes (`presentations/nov10/build.py`,
script exported by `export_script.py`):
- Average size of EPS users falls from 21.6 to 13.8 workers with a price because large plants stop
  using EPS; the top 1% plant grows from 317 to 328. Gross output falls to 99.1 while costs fall from
  21.0 to 19.9.
- Optimal scale: light plants (89% of plants) are at it; 98% of EPS users are below it, held back
  by the quota through θ; manual-intensive plants with 300+ core Koreans (0.1%) are ineligible.
- Three EPS shares defined. Average across EPS firms of EPS ÷ that firm's workers: 36.9% (Lee, Peri
  and Yang, Table 3) and 37.2% in the model. EPS ÷ all manufacturing workers: 5.5%, which sets M.
  Share of plants using EPS: about 10%, and 10.7% in the model.
- Survey (`bunching/eps_binding.py`, `by_cap_use`): firms below half their 2019 cap (42% of firms)
  want more workers about as often (41%) as firms at or above the cap (18% of firms, 50%); firms in
  between, 44%. For most firms the cap is not what holds them back.
- Weak plants: the current rule keeps 0.9% more plants than a price (exit rate 8.08% vs 8.02%); an
  equal limit keeps 2.3% more than today.
- EPS productivity (survey: 74–96% of a Korean worker): at 74%, EPS work costs 1.35 × w per unit,
  more than a Korean manual worker at a plant with 150 core Koreans (1.29 × w). Arithmetic only.

**Problems found while checking (not yet fixed):**
- The 5.5% and 10% targets have no recorded source. They date from the first model (Oct 15). The
  5.5% sets the quota M and so θ.
- Net output counts the Korean manual premium as a resource cost. If it is a wage paid to Korean
  workers, as Prof. Hur's "raise the wage" suggests, it is a transfer, and the +0.33% net gain, which
  comes from lower costs, could largely disappear; gross output falls 0.9%.
- In the model the quota is shared in proportion to each plant's cap, so the cap's shape decides
  who gets workers even though no plant reaches its cap. In the survey, wanting more does not depend
  on cap use, which suggests real allocation (quota, ranking, per-round limits) is not proportional
  to the cap. If so, our "size rule" works through a channel the data may not have.
- With one θ for every plant, the model cannot put any plant at its cap; in the survey 18% are at or
  above the 2019 cap.

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
2. **Re-fit the closure slope on a finer grid**, and close the remaining gaps: EPS firms
   with 20–49 workers (10% vs 25%), the spread of EPS shares (0.15 vs 0.22), the pile-up at
   the low cap steps, plants with 50+ workers (1.8% vs 2.1%).
3. **Robustness (decides the kill condition):** CES parameter ρ, shock length (2 vs 5
   years), cap schedule, the exit taste-shock scale, and the Pareto tail γ.
4. **State the model's assumptions explicitly** (Prof. Hur, Oct 27): no households
   (no consumption, saving or remittances; we measure output, not welfare), fixed
   Korean labor and no population growth, EPS workers paid a Korean wage (the survey
   supports this: 96%) and equally productive as Korean manual workers (the survey says
   74–96%), the Korean manual premium as a resource cost, the cap on core Koreans h
   rather than h + k, equal θ for every plant, every user wanting more, no points ranking
   or new-permit limit, the permit fee as a transfer, steady-state comparisons only.
5. **Data still needed:** EPS workers by number of Korean workers for all plants and the
   2024 caps (MOEL, HRD Korea and KEIS hold the records); the January 2021 survey wave
   (Prof. Lee, Prof. Yang). Ask Prof. Hur first. Also make rationing realistic using the survey.
6. **Optional extensions:** a COVID demand shock in the closure experiment; credit
   constraints (links to Song–Storesletten–Zilibotti and our rung 4 code); a
   counterfactual with size-neutral *rationing* (points without the cap) besides allocation by price.
7. **Check with Prof. Hur:** how to model rationing; whether identifying the model from
   the COVID shock (instead of bunching) is acceptable; whether refocusing on the quota
   is acceptable if the gain stays below the threshold.
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
| `hopenhayn_project/eps_model/run_v6.py` | Version-5 model recalibrated to the corrected Lee–Peri–Yang targets |
| `hopenhayn_project/eps_model/v6_best.json` | **Current** calibration (Nov 1, 13 parameters) |
| `hopenhayn_project/eps_model/v6_results.json`, `v6_results_fine.json` | Fit, experiments and bunching; finer-grid check |
| `presentations/nov3/SCRIPT.md` | Nov 3 script by presenter (Benjamin away: Julian 27–29, Mimi 30–32, Sara 33–35, Donny 36–38) |
| `presentations/nov3/build.py`, `notes.py`, `export_script.py` | Generate the Nov 3 slides, speaker notes and script from the results files |
| `hopenhayn_project/eps_model/v6_fine_extra.py`, `v6_fine_extra.json` | Finer grid: quota +50%, and EPS users by Korean workers under the 2019 caps |
| `hopenhayn_project/eps_model/v5_best.json` | Version-5 calibration (Oct 28; targets since corrected) |
| `hopenhayn_project/eps_model/v5_results.json`, `v5_results_fine.json` | Version-5 fit, experiments and bunching; the finer-grid check |
| `hopenhayn_project/eps_model/make_bunch_fig.py`, `bunching_v5.png/.svg` | Bunching histogram in the model, current rule vs. no size rule |
| `hopenhayn_project/eps_model/recal_best.json` | Version-4 calibration (Oct 19; numbers in the proposal and the Oct 27 slides) |
| `hopenhayn_project/eps_model/eps_results_recal.json` | Fit and experiment results for the version-4 calibration |
| `hopenhayn_project/eps_model/eps_by_size.py`, `eps_by_size.json` | EPS workers by plant size, current rule vs. no size rule (Figure 2) |
| `hopenhayn_project/eps_model/local_best.json` | Oct 15 calibration (superseded) |
| `hopenhayn_project/eps_model/experiments_localbest.json` | Oct 15 experiment results (superseded) |
| `hopenhayn_project/eps_model/top_draws.json` | Top 20 draws from the version-4 random search |
| `hopenhayn_project/eps_model/NOTES.md` | Model notes and how to rerun |
| `bunching/` | Bunching estimator, census histogram script, `RESULTS.md`, EPS survey aggregates (`eps_survey.py`) |
| `hopenhayn_project/rung1_hopenhayn/`, `ahkr_model/` | Earlier Hopenhayn/AHKR ladder exercises |
| `course_exercises/aiyagari_replication/` | Aiyagari (1994) Table 2 replication (Week 3 exercise; not part of the EPS project) |

Data source: Statistics Korea, MDIS — 소상공인실태조사 (2018–2024) and
전국사업체조사 (2000–2024). Raw files are not in this repository; teammates who
need them should download them with their own MDIS account.

### Where the EPS survey file is stored

The replication file of Dong, Lee and Yang (2024) comes from the article's "Supplementary
data" on the Oxford University Press site: `eps.dta`, `eps.do`, `Appendix_EPS.pdf`. We keep
it in **`~/EPS_data`**, outside the repository, and report only aggregates. Teammates can
download it from the publisher's page (through the Yonsei library if needed).

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
