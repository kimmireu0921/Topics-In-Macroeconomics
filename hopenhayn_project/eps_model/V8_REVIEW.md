# Review of v8: five questions (Nov 18)

The v8 baseline is unchanged: `eps_model_v8.py`, `v8_best.json` and the results files are as published. Every check below starts from `v8_best.json` and changes one thing:
- `v8_review.py` writes `v8_review.json`.
- `v8_review_swap.py` writes `v8_review_swap.json`.

## 1. The closure slope is 0.000

**The shock code is not the cause.**
- The design matches Lee, Peri and Yang: a two-year 20% cut in each user's EPS workers, at fixed prices.
- Profits fall as they should: users lose 2.5% of profit on average.
- Exit responds through the same logit formula used everywhere else.

**The cause is who uses EPS.** These are plant groups under the 2019 caps:

| Group | Endogenous exit | Plants with Pr(stay) < 0.99 | Lowest productivity in group |
|---|---|---|---|
| Manual-intensive, eligible, users | 0.0% | 0% | 1.45 |
| Manual-intensive, eligible, non-users | 16.4% | 20% | 0.61 |
| Manual-intensive, not eligible | 5.3% | 6% | 0.61 |

- Every plant near the exit margin is a non-user.
- Using EPS has a fixed cost (c_m = 0.73), so only plants well above the exit threshold use it.
- A cut in EPS workers therefore never reaches a plant that is about to close.

**What moves the slope** (one parameter changed, others fixed, not recalibrated):

| Change | Slope | What else changes |
|---|---|---|
| v8 as calibrated | 0.000 | — |
| c_m halved | 0.005 | Cap use falls to 49% (target 62%) |
| c_m quartered | 0.008 | Users now include plants that exit (2.7%); the cut costs them 14% of profit, but extra closure is still 0.04 pp |
| σ_s doubled | 0.000 | Exit rate rises to 8% |

**Is permanent eligibility the reason?** Partly, but it is not the main reason:
- Eligible and non-eligible manual-intensive plants exit at almost the same rate (6.7% and 6.9%).
- The users' distance from the exit margin comes from the fixed cost of using EPS.
- Even with c_m cut to a quarter, a temporary cut barely changes exit. In this model a plant's value depends mostly on its persistent productivity, so a two-year cut changes the value of staying very little.

**History.** v6 and v7 matched 0.15 on the base grid, but the same model gave 0.05 on a finer grid, so that match was partly a grid artefact.

**Not tested:** eligibility that is redrawn over time, for example permits lasting three years. That is a change to the model and needs a team decision.

## 2. Is "caps barely matter" circular?

**Not by assumption, but it follows from one data target and one interpretation.**
- Eligible plants may hire up to their cap. They stop below it whenever their manual work is smaller than the cap.
- Calibrating average cap use to the survey's 62% therefore makes most plants unconstrained.
- Result: 1.6% of users are at the 2024 cap and 10.7% at the 2019 cap (survey 17.6%). An equal limit then changes nothing (0.00%).

**The old θ rule gave the opposite answer by construction.**
- It held every plant at 21% of its cap, so the cap bound for 82% of users.
- The survey rejects that: the median firm uses 60% of its cap.

**The real assumption:** a firm below its cap uses as many EPS workers as it wants.
- The survey disagrees for many firms: 41% of firms below half their cap still want more.
- If those firms are rationed by something other than the cap (allocation rounds, points), caps could matter more than v8 says.

**The data that can decide this:** the Ministry records of applications against permits granted, which we requested.

## 3. The Korean premium (ψ = 1.70, up from 0.92)

**What sets ψ.** Setting ψ back to v6's 0.92, other parameters fixed:

| | Data | v8 (ψ = 1.70) | ψ = 0.92 |
|---|---|---|---|
| Plants using EPS | 8.0% | 7.0% | 4.7% |
| Workers at EPS firms | 20.8 | 18.7 | 26.1 |
| Cap use | 62.4% | 62.4% | 74.8% |

A larger premium makes EPS worth more to small plants. That gives more users, who are smaller and use less of their cap. Those three targets push ψ up.

**The price gain as ψ moves**, other parameters fixed:

| ψ | Net output | Net output if the premium is pay |
|---|---|---|
| 0.92 | +0.13% | +0.11% |
| 1.36 (×0.8) | +0.51% | +0.26% |
| 1.70 (v8) | +0.39% | +0.02% |
| 2.04 (×1.2) | +0.47% | −0.08% |

**Why the gain depends on the premium.** It is built into the model, not a new problem:
- Korean and EPS manual workers are perfect substitutes, so moving EPS workers between plants changes only the premium saved, the fixed costs and entry.
- v6 had the same dependence.
- The premium is 2.7% of gross output.

**What would help:** a direct measure.
- The survey has monthly wages for Korean and EPS workers by firm (Q13). If Korean wages at small firms are not higher, the premium is a non-wage cost (vacancies, recruiting), which supports treating it as a resource cost.

## 4. Why gross output now rises with a price

**Swapping structure and parameters** (same quota):

| Gross output change with a price | v6 parameters | v8 parameters |
|---|---|---|
| θ rule | −0.85% | +0.32% |
| Random eligibility | −0.28% | +0.23% |

The sign changes mainly with the parameters, under both structures.

**Mechanism in v8.** Today only 22% of entrants have access. A price extends EPS to plants that were not eligible:
- Users rise from 7.0% to 8.7% of plants.
- Korean manual workers fall by 3.5%, and those workers move to core jobs.
- Plants rise by 1.3%, mostly light ones (light output +2.4%, manual-intensive output −0.4%).

**Mechanism in v6.** Every manual-intensive plant had access. A price took EPS away from small plants, and a quarter of manual-intensive plants closed.

**Not yet isolated:** which recalibrated parameters drive the switch. Candidates are the manual-intensive share (0.18 → 0.45), the weight on manual work (1.47 → 0.70), and how fast the premium falls with size (ξ 0.23 → 0.59). The next check is to swap these one group at a time.

## 5. Is productivity tracked as s only?

**This is notation only, not a code error.**
- The code's state is the pair (x, z): 264 states, 24 levels of x times 11 of z.
- The transition matrix is block-diagonal in x, with probability 0 of moving between x levels.
- No two states share the same s.
- So two plants with the same s but different x are different states, with their own values and exit choices.

The model note now says so.

## Addendum: survey evidence on ψ and ξ (`bunching/premium_evidence.py`)

The 2019 survey has no direct measure of the premium, but three questions bear on it. These checks were not used in the calibration.

**Hiring shortfall (Q4).** Share of planned Korean manual hires (production and elementary jobs) that firms did not fill last year, by Korean workers:

| Korean workers | 1–5 | 6–10 | 11–30 | 31–50 | 51+ |
|---|---|---|---|---|---|
| Not filled | 56% | 44% | 39% | 19% | 11% |

- Core jobs (managers and clerical) were filled much more often: 26% unfilled at the smallest firms, about 0–4% at firms with 31 or more Korean workers.
- So Korean manual workers are hard to find, much harder at small plants, and harder than core workers. All three are what the model's premium assumes.

**How fast the shortfall falls with size.** On a log scale, the slope is −0.50 for total hires and −0.22 if each firm counts equally. The v8 premium falls with ξ = 0.59 (v6: 0.23). The direction matches; v8's decline is somewhat steeper than the survey's. The size of ψ is not pinned down, because turning an unfilled share into a cost needs a further assumption.

**Wages (Q13).** The median Korean wage is 1.12 times the EPS wage at firms with up to 50 Korean workers and 1.07 above that. That is flat across size. So small plants do not pay Korean workers more; the premium shows up as unfilled jobs. This supports treating it as a real cost (search, vacancies, lost output) rather than pay.

**Reasons (Q6).** 77% of firms that tried to hire Koreans had difficulty. Of those:
- 49% gave "no applicants" as the main reason;
- 21% gave labour costs.
