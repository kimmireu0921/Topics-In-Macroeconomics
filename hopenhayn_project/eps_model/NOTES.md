# EPS model — notes (version 4, Oct 15, 2026)

See `PROJECT_LOG.md` at the repository root for the full history and results.

## Model

Hopenhayn (1992) with Korea's Employment Permit System:
- Task-based production: core work (Korean workers h) and manual work l = k + m
  (Korean manual workers k, EPS workers m), CES with parameter ρ.
- Korean manual workers carry a recruiting premium ψ(1+h)^(−ξ), largest at small plants.
- EPS workers cost φ·w (φ = 1) plus a fixed cost c_m of using EPS.
- Current rule: quota rationed by quantity, m ≤ θ·q(h) with the 2024 cap schedule,
  eligibility 1 ≤ h < 300; θ clears the national quota M.
- Size-neutral counterfactual: same quota allocated by a permit price, no cap.
- Two plant types (light / manual-intensive) with different manual weights and fixed costs.
- Exit with exogenous δ plus a logit taste shock (scale σ_ε = 0.1) on the continue/exit decision.
- General equilibrium: Korean wage clears fixed Korean labor N; θ or the permit price clears M.

## Rerun

```
cd hopenhayn_project/eps_model
python3 -c "import json; from run_eps import build, NAMES, M; \
d=json.load(open('local_best.json')); p={k:d[k] for k in NAMES}; \
[print(reg, build(p, M).solve(reg)['net_Y']) for reg in ('current','neutral')]"
python3 run_eps.py eps_results.json refine 200     # full re-calibration (~1 hour)
```

`closure_response()` returns two slopes: `slope` (all plants, actual EPS share; not
comparable to Lee–Peri–Yang) and `slope_lpy` (EPS users only, statutory exposure;
their design). Since Oct 19, `run_eps.py` targets `slope_lpy`, computed together with
the EPS share among users under the **2019 caps** (`cap_2019`, Lee–Peri–Yang Table 4);
the other moments use the 2024 caps. Recalibration:

```
python3 run_eps.py eps_results_recal.json recal 150   # starts from local_best.json (~1.5 h)
```

Current calibration: `recal_best.json`; results: `eps_results_recal.json`.

## Known issues

- Fit gaps: average plant size 5.9 vs 7.5; share of plants using EPS 7.2% vs 10%; EPS share among users 29% vs 37%.
- Parameters at range limits: δ = 0.05, ν_top = 0.9, ξ = 0.1, cf_A = 0.4.
- The cap is applied to core Koreans h, approximating the statutory count h + k.
- The same national quota M is assumed under the 2019 and 2024 caps.
- Robustness (ρ, shock length, taste-shock scale) not yet run; it decides the kill condition.
