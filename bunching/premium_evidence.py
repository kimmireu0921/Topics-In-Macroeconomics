"""Survey evidence on the Korean manual premium (psi, xi), 2019 KDI-World Bank EPS survey (Dong, Lee and
Yang 2024 replication file). Aggregates only; the survey file stays outside the repository.
  Q4: Korean workers firms planned to hire last year and actually hired, by occupation
      (manual = production + elementary; core = managers/professionals + clerical)
  Q6: difficulty hiring Koreans; Q6-2: main reason (1 = no applicants, 2 = labor cost burden)
  Q13: average monthly wage, Korean and EPS workers
Writes premium_evidence.json.  python3 premium_evidence.py"""
import json, os
import numpy as np, pandas as pd

df = pd.read_stata(os.path.expanduser("~/EPS_data/eps.dta"), convert_categoricals=False)
k = df["korean"].astype(float)
f = lambda c: df[c].astype(float)
plan_m, hire_m = f("q4_4a") + f("q4_6a"), f("q4_4b") + f("q4_6b")
plan_c, hire_c = f("q4_1a") + f("q4_2a"), f("q4_1b") + f("q4_2b")
wf, wk = f("q13_3a"), f("q13_3b")
BINS = [(0, 5), (5, 10), (10, 30), (30, 50), (50, 1e9)]
rows, X, Ya, Yf = {}, [], [], []
for a, b in BINS:
    s = (k > a) & (k <= b)
    pm, pc, ww = s & (plan_m > 0), s & (plan_c > 0), s & (wf > 0) & (wk > 0)
    agg = float(1 - hire_m[pm].sum() / plan_m[pm].sum())
    firm = float((1 - np.minimum(hire_m[pm] / plan_m[pm], 1)).mean())
    rows[f"{a + 1}-{int(b) if b < 1e9 else 'plus'}"] = dict(
        firms=int(s.sum()), firms_planning_manual=int(pm.sum()), unfilled_manual_aggregate=agg, unfilled_manual_firm_mean=firm,
        unfilled_core_aggregate=float(1 - hire_c[pc].sum() / plan_c[pc].sum()) if pc.any() else None,
        wage_ratio_korean_to_eps_median=float((wk[ww] / wf[ww]).median()))
    X.append(float(np.log1p(k[pm]).mean())); Ya.append(np.log(agg)); Yf.append(np.log(firm))
had = f("q6") == 1
res = dict(by_korean_workers=rows,
           slope_log_unfilled_on_log_1_plus_n=dict(aggregate=float(np.polyfit(X, Ya, 1)[0]), firm_mean=float(np.polyfit(X, Yf, 1)[0])),
           share_with_difficulty=float(had.sum() / f("q6").notna().sum()),
           reason_no_applicants=float((f("q6_2") == 1).sum() / had.sum()), reason_labor_cost=float((f("q6_2") == 2).sum() / had.sum()))
json.dump(res, open("premium_evidence.json", "w"), indent=1)
print(json.dumps(res, indent=1))
