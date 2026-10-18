---
title: "Who Gets the Guest Workers? Size-Dependent Allocation in Korea’s Employment Permit System and Manufacturing Productivity"
---

<p class="authors">Sara Ambre Chekroune (2025462014) · Yitang Donny Chen (2025461008) · Mireu Kim (2025462112)<br>Julian Henry Raymundo (2025462075) · Zachary Benjamin Yoo (2025461053)<br>
ISA6327 Topics in Macroeconomics · Prof. Sewon Hur · Research proposal · October 23, 2026</p>

## 1. The Idea and Its Motivation

**Research question.** Korea’s Employment Permit System (EPS) ties a manufacturing plant’s access to foreign workers to its size. Does this size-dependent allocation keep low-productivity plants in business and lower aggregate productivity, and how much would output change if the *same* national quota were allocated without regard to plant size?

**Why it matters.** Small Korean manufacturers depend on guest workers because they cannot hire Koreans for manual jobs: 82.6% of SMEs employing foreigners cite a domestic labor shortage, against 13.4% citing labor costs (KBIZ 2026), and 53% of EPS firms report receiving “no applicants” for such jobs (Lee, Peri, and Yang 2026). The government has responded by expanding the E-9 quota from 52,000 in 2021 to 165,000 in 2024. Access, however, is rationed by size. Only plants with fewer than 300 workers (or capital of ₩8bn or less) are eligible, and the statutory cap rises in steps with Korean employment: Koreans + 10 for plants with 1–10 Korean workers, 30 for 11–50, up to 60 for 201–300. The maximum foreign share therefore falls from 81% at a plant with 3 Korean workers to 19% at one with 250. The EPS acts as a size-dependent subsidy concentrated on the smallest plants. The stakes became visible in 2020–21, when border closures cut the stock of EPS workers by 22%: moving from zero to full exposure raised a plant’s probability of closing by 12.4–17.7 percentage points, against a baseline of 4.4% (Lee, Peri, and Yang 2026). Access to guest workers matters for which plants survive. Whether the size rule allocates that access efficiently is an open policy question as the quota keeps growing.

## 2. State of the Literature

*Firm dynamics and selection.* Hopenhayn (1992) and Hopenhayn and Rogerson (1993) show how policies that protect incumbents lower measured productivity through the exit margin, even though no individual firm becomes less productive. Asturias et al. (2023) bring this framework to Korea, measuring how entry and exit contribute to aggregate growth.

*Size-dependent policies and misallocation.* Guner, Ventura, and Xu (2008) show that size-contingent policies distort the firm-size distribution and reduce output; Garicano, Lelarge, and Van Reenen (2016) quantify the cost of France’s 50-employee threshold; Hsieh and Klenow (2009) measure the aggregate cost of such distortions. None of these studies covers immigration policy.

*Immigration and firms.* Lee, Peri, and Yang (2026) provide the closest evidence: using the EPS quota schedule as an instrument, they show that plants more exposed to the 2020–21 sudden stop closed more, cut production and downgraded Korean workers. Their analysis is reduced-form and short-run, and they call for work on longer-run adjustments. Mandelman, Mehra, and Shen (2025) add skilled foreign labor to a Hopenhayn–Rogerson model and show that US H-1B frictions hold back young firms, but their frictions do not depend on firm size. Macroeconomic studies of guest workers in aging economies (İmrohoroğlu, Kitao, and Yamada 2017 for Japan; Kim, Han, and Hong 2022 for Korea) use household overlapping-generations models without firm heterogeneity.

*The gap.* No study quantifies the long-run effect of *how* a guest-worker quota is allocated across firm sizes: its effect on entry and exit, the firm-size distribution and aggregate productivity.

## 3. Our Contribution

We provide the first quantitative firm-dynamics model of the EPS allocation rule. The model separates two policy margins that the debate tends to merge: the **quantity** of guest workers and their **allocation** across plants. It is disciplined by Lee, Peri, and Yang’s natural experiment, which we re-create inside the model. This lets us ask a question their reduced-form design cannot: what would happen in the long run if the same workers went to different plants?

## 4. Methodology (Quantitative Approach)

**Building blocks.** We extend the Hopenhayn (1992) / Asturias et al. (2023) model from Week 2, following Mandelman, Mehra, and Shen (2025) in adding foreign labor to a Hopenhayn–Rogerson framework.

**What we add.** Plants with productivity *s* combine core work *h*, done by Korean workers, and manual work ℓ, done by Korean manual workers *k* or EPS workers *m*:
<span class="eq">*y* = *s* (*h*<sup>ρ</sup> + λ<sub>*t*</sub> ℓ<sup>ρ</sup>)<sup>α/ρ</sup>,   ℓ = *k* + *m*.</span>
Four features, each motivated by the evidence above: (i) a recruiting premium for Korean manual workers, *w*(1 + ψ(1 + *h*)<sup>−ξ</sup>), largest at small plants (the “no applicants” shortage); (ii) EPS workers cost about a Korean wage once room and board are included (₩2.93m vs. ₩2.6m a month), and the national quota *M* is rationed by quantity, as under the points system: an eligible plant may hire *m* ≤ θ*q*(*h*), with the statutory cap *q* and a share θ that clears the quota; (iii) two plant types, light and manual-intensive, so that mid-sized EPS-dependent plants can be fragile; (iv) endogenous exit, free entry, and a Korean wage that clears the Korean labor market.

**Data and calibration.** Firm-side targets come from the business census (전국사업체조사, MDIS, 2000–2024): about 70% of manufacturing plants have 1–4 workers, and average plant size is 7–8 workers. EPS targets: about 10% of plants use EPS, the EPS share among users is 37% (Lee, Peri, and Yang 2026), and the closure response to the 2020–21 sudden stop is 0.124–0.177. We match the latter by cutting each plant’s EPS workers by 20% in the model, under the 2019 caps in force at the time, and regressing closures on statutory exposure among EPS users, as in their design. Before choosing EPS, we tested a related idea, Korea’s sales-tiered card-fee rates, for bunching in MDIS small-business data; we found none at any threshold, including across a 2019 reform, and dropped it.

**Counterfactuals.** (1) No EPS; (2) the same quota allocated without the size rule, by a common price (tradable permits) or by points without the cap; (3) the quota expanded or cut by 50%; (4) the 2019 versus 2024 cap schedules. Outcomes: entry and exit, the size distribution, aggregate TFP and net output, and Korean wages.

**Feasibility and preliminary results.** We have calibrated all 13 parameters, computing the 2020–21 closure response under the 2019 caps then in force. Allocating the same quota without the size rule raises manufacturing net output by about **0.4%**, roughly one-ninth of the gain from a 50% larger quota (+3.7%); removing EPS lowers it by 7.5%. An earlier calibration that matched the closure evidence less carefully gave 1.0%, so the magnitude is sensitive to calibration, and robustness is the core of the remaining work. The mechanism is the one hypothesized: under the current rule, EPS workers are spread across twice as many plants (7.2% vs. 3.5%), and manual-intensive plants make up 7.7% of plants instead of 5.7%. The model’s closure response, measured as in Lee, Peri, and Yang (2026), is 0.107 if plants expect the shock to last two years and 0.195 if five, bracketing their estimate of 0.124–0.177. Doubling the caps from the 2019 to the 2024 schedule at a fixed quota changes output by less than 0.1%: with a binding quota, who gets the workers matters more than the size of each plant’s cap. Remaining tasks are to close the fit gaps (average plant size, the share of plants using EPS and the EPS share among users are below target) and to test robustness to the substitution parameter ρ, the expected shock length and the cap schedule. **Kill condition:** if the allocation gain is not positive across robustness checks (substitution parameter, expected shock length, cap schedule), or falls below one-tenth of the gain from a 50% quota expansion, we refocus the project on the quantity margin.

<p class="disclosure"><b>AI use.</b> The team used Claude (Anthropic) for literature search, data processing, model coding and calibration, and drafting. All results were produced by our own code, and sources were checked by the team.</p>

## References

<div class="refs">

Asturias, Jose, Sewon Hur, Timothy J. Kehoe, and Kim J. Ruhl. 2023. “Firm Entry and Exit and Aggregate Growth.” *American Economic Journal: Macroeconomics* 15 (1): 48–105.

Garicano, Luis, Claire Lelarge, and John Van Reenen. 2016. “Firm Size Distortions and the Productivity Distribution: Evidence from France.” *American Economic Review* 106 (11): 3439–79.

Guner, Nezih, Gustavo Ventura, and Yi Xu. 2008. “Macroeconomic Implications of Size-Dependent Policies.” *Review of Economic Dynamics* 11 (4): 721–44.

Hopenhayn, Hugo A. 1992. “Entry, Exit, and Firm Dynamics in Long Run Equilibrium.” *Econometrica* 60 (5): 1127–50.

Hopenhayn, Hugo, and Richard Rogerson. 1993. “Job Turnover and Policy Evaluation: A General Equilibrium Analysis.” *Journal of Political Economy* 101 (5): 915–38.

Hsieh, Chang-Tai, and Peter J. Klenow. 2009. “Misallocation and Manufacturing TFP in China and India.” *Quarterly Journal of Economics* 124 (4): 1403–48.

İmrohoroğlu, Selahattin, Sagiri Kitao, and Tomoaki Yamada. 2017. “Can Guest Workers Solve Japan’s Fiscal Problems?” *Economic Inquiry* 55 (3): 1287–1307.

KBIZ (Korea Federation of SMEs). 2026. *2025 Survey on Difficulties in Employing Foreign Workers* (외국인력 고용 관련 종합애로 실태조사). Seoul: KBIZ.

Kim, Seonbin, Jongsuk Han, and Jae-Hwa Hong. 2022. “Macroeconomic Effects of Utilizing Foreign Labor Force in Population Aging” (외국인력 활용의 거시경제 효과 분석). *한국경제의 분석* 28 (3): 111–58.

Lee, Jongkwan, Giovanni Peri, and Hee-Seung Yang. 2026. “The Effects of a Sudden Stop in Low-Skilled Immigration: Evidence from Korea’s Guest Worker Program.” NBER Working Paper 34927.

Mandelman, Federico, Mishita Mehra, and Hewei Shen. 2025. “Skilled Immigration Frictions as a Barrier for Young Firms.” *Journal of Monetary Economics* 155: 103811.

Statistics Korea. 2000–2024. 전국사업체조사 (Census on Establishments) and 소상공인실태조사 (Survey on Small Business). Microdata Integrated Service (MDIS).

</div>
