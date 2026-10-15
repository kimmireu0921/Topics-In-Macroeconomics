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
their design). **Use `slope_lpy` as the calibration target** in the next run;
`run_eps.py` still targets `slope`.

## Known issues

- `run_eps.py` targets `slope`, not `slope_lpy`, and uses 2024 caps for the 2020 shock (should be 2019).
- Average plant size 5.7 vs 7.5; EPS share among users 28% vs 37%.
- Parameters at range limits: ρ = 0.8, δ = 0.05, ν_top = 0.9.
- The cap is applied to core Koreans h, approximating the statutory count h + k.
