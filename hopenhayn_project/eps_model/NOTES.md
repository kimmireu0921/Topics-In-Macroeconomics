# EPS model — status (first pass, 2026-10-15)

Hopenhayn model with Korean workers n and EPS workers m (CES), the 2024 statutory
cap m ≤ q(n), eligibility n < 300, at least one Korean worker for EPS users, a fixed
cost of using EPS (c_m), exogenous exit δ, and general equilibrium (Korean wage
clears fixed N; an EPS shadow price rations the fixed quota M).

**Not usable for conclusions yet.**

## First-pass results (ρ = 0.5–0.8, net output, vs. current rule)

| Experiment | Output |
|---|---|
| Size-neutral allocation, same quota | ≈ 0.0% |
| Quota +50% / −50% | +2.6 to +5.1% / −2.6 to −6.3% |
| No EPS | −6 to −18% |

## Why the allocation result is biased toward zero

1. Exit cutoff sits at the bottom of the productivity grid in every regime; 93% of
   exits are exogenous (δ = 0.07). The survival channel can't operate.
2. EPS users in the model are large plants with a 7–9% EPS share; in the data
   (Lee, Peri, Yang 2026) users are small plants with a 37% share.

## Next steps

1. Endogenous exit: lower δ, raise c_f / lower entrant productivity so the cutoff is
   interior; target the Lee–Peri–Yang closure response (+12.4–17.7 pp).
2. Korean-hiring shortage that is heavier for small plants (e.g., a recruiting cost
   for Korean manual workers falling with size) so small plants rely on EPS.
3. Recalibrate. `run_eps.py` still loops over ρ = 0.2 and 0.35, which have no
   equilibrium with this CES (EPS labor becomes implausibly productive); drop them
   or change the production structure.

Firm-side targets from MDIS census 2023–24 (manufacturing): mean size 7–8 workers,
~70% of plants with 1–4 workers.
