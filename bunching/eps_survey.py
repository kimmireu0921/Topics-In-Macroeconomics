"""Aggregates from the EPS employer survey (KDI with the World Bank, 2019), the replication
file of Dong, Lee and Yang (2024, Oxford Economic Papers 76(2)). The file stays outside the
repository (~/EPS_data/eps.dta); only aggregates are printed.

  python3 eps_survey.py

Korean workers: `korean` (EPS firm list, Feb 2019) and q13_1b (survey answer, Aug 2019).
EPS workers: q13_1a. q9: extra EPS workers the firm would hire with no limit on the number.
Trend for the bunching check: Poisson regression of firm counts at 1-40 Korean workers on a
quartic in log workers, with a dummy for the count being tested.
"""
import os

import numpy as np
import pandas as pd
from scipy.optimize import minimize

df = pd.read_stata(os.path.expanduser("~/EPS_data/eps.dta"), convert_categoricals=False)
listed, korean, eps, extra = (df[c].astype(float) for c in ("korean", "q13_1b", "q13_1a", "q9"))


def cap_2019(n):
    return np.select([n <= 5, n <= 10, n <= 30, n <= 50, n <= 100, n <= 150, n <= 200],
                     [5, 7, 10, 12, 15, 20, 25], default=30)


use = eps / cap_2019(listed)
total, share = korean + eps, eps / (korean + eps)
print(f"firms {len(df)}; workers {total.mean():.2f}, Korean {korean.mean():.2f}, EPS {eps.mean():.2f}")
print(f"EPS share: simple average {share.mean():.3f} (SD {share.std():.3f}), employment-weighted {eps.sum() / total.sum():.3f}")
print(f"wage + dorm and meals, as a share of the Korean wage: {(df.q13_3a + df.q21_2).mean() / df.q13_3b.mean():.3f}")
print(f"EPS productivity, Korean = 100 (under 1 year, 1-2, 3-5): {df.q14_1.mean():.1f}, {df.q14_2.mean():.1f}, {df.q14_3.mean():.1f}")
print(f"share of cap used: mean {use.mean():.3f}, median {use.median():.3f}; under half {(use < .5).mean():.3f}; "
      f"at or above {(use >= 1).mean():.3f}; above {(use > 1).mean():.3f}")
over_survey = eps > cap_2019(korean)
print(f"above the cap: within 20% {((use > 1) & (use <= 1.2)).mean():.3f}, beyond 20% {(use > 1.2).mean():.3f}, "
      f"more than double {(use > 2).mean():.3f}; firms above on the list count {(use > 1).sum()}, also above on the survey count {((use > 1) & over_survey).sum()}")
print(f"would hire more with no limit: {(extra > 0).mean():.3f} (mean {extra.mean():.2f}); "
      f"among firms under half their cap {(extra[use < .5] > 0).mean():.3f}; exactly at the cap {(extra[use == 1] > 0).mean():.3f}")

print("\nKorean workers | firms | EPS | share of cap used | want more")
for a, b in [(0, 5), (5, 10), (10, 30), (30, 50), (50, 100), (100, 300)]:
    s = ((listed > a) | (a == 0)) & (listed <= b)                # the first bin includes firms with none
    print(f"{a + 1 if a else 0:>4}-{b:<4} {s.sum():>5} {eps[s].mean():6.1f} {use[s].mean():8.2f} {(extra[s] > 0).mean():8.2f}")

print("\nworkers per firm, share of firms:", {f"{a}-{b}": round(float(((total >= a) & (total < b)).mean()), 3)
                                              for a, b in [(0, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 300)]})


def excess(counts, k, t):
    """Count at t against the trend: ratio and z-statistic of the dummy for t."""
    x = np.log(k) - np.log(k).mean()
    X = np.column_stack([x ** p for p in range(5)] + [(k == t).astype(float)])
    b = minimize(lambda v: np.sum(np.exp(X @ v) - counts * (X @ v)), np.r_[np.log(counts.mean()), np.zeros(5)],
                 jac=lambda v: X.T @ (np.exp(X @ v) - counts), method="BFGS", options=dict(maxiter=5000)).x
    se = np.sqrt(np.diag(np.linalg.inv((X * np.exp(X @ b)[:, None]).T @ X)))
    return np.exp(b[5]), b[5] / se[5]


k = np.arange(1, 41)
for name, n in (("list, Feb 2019", listed), ("survey, Aug 2019", korean)):
    counts = np.array([(n == i).sum() for i in k], float)
    print(f"\n{name}: firms with 1-20 Korean workers:", counts[:20].astype(int).tolist())
    for t in (6, 11, 31):
        print("  just past a cap step, t = %d: ratio %.2f, z %.2f" % (t, *excess(counts, k, t)))
    z = {t: round(excess(counts, k, t)[1], 2) for t in range(3, 26) if t not in (6, 11)}
    print("  other counts, largest z:", sorted(z.items(), key=lambda p: -abs(p[1]))[:3])
