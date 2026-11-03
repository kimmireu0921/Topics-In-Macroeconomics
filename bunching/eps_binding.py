"""Is the EPS cap binding in the survey? Aggregates by number of Korean workers, under the 2019
caps the firms faced and under the 2024 caps applied to the same 2019 headcounts. The survey file
stays outside the repository; only aggregates are printed and saved.

  python3 eps_binding.py [out.json]

A firm "wants past the cap" if EPS workers now + extra workers wanted with no limit (q9) > its cap.
"""
import json
import os
import sys

import numpy as np
import pandas as pd

df = pd.read_stata(os.path.expanduser("~/EPS_data/eps.dta"), convert_categoricals=False)
listed, korean, eps, extra = (df[c].astype(float) for c in ("korean", "q13_1b", "q13_1a", "q9"))
total = korean + eps
share = eps / total


def cap_2019(n):
    return np.select([n <= 5, n <= 10, n <= 30, n <= 50, n <= 100, n <= 150, n <= 200],
                     [5, 7, 10, 12, 15, 20, 25], default=30)


def cap_2024(n):
    return np.select([n <= 10, n <= 50, n <= 100, n <= 150, n <= 200, n <= 300],
                     [n + 10, np.minimum(30, 2 * n), 35, 40, 50, 60], default=80)


def row(s):
    q19, q24 = cap_2019(listed[s]), cap_2024(listed[s])
    q24 = np.maximum(q24, 1)                                    # firms listed with no Korean workers
    e, x, u19 = eps[s], extra[s], eps[s] / q19
    at = u19 >= 1
    return dict(firms=int(s.sum()), eps=float(e.mean()), wanted=float((e + x).mean()), cap_2019_use=float(u19.mean()), under_half=float((u19 < .5).mean()),
                near_cap_90=float((u19 >= .9).mean()), at_or_above=float(at.mean()), exactly_at=float((u19 == 1).mean()),
                above=float((u19 > 1).mean()), want_more=float((x > 0).mean()), extra_if_want=float(x[x > 0].median()) if (x > 0).any() else None,
                at_or_above_firms=int(at.sum()), want_more_if_at=float((x[at] > 0).mean()) if at.any() else None,
                want_past_2019=float((e + x > q19).mean()), cap_2024_use=float((e / q24).mean()),
                at_or_above_2024=float((e >= q24).mean()), want_past_2024=float((e + x > q24).mean()))


BINS = [(0, 5), (5, 10), (10, 30), (30, 50), (50, 100), (100, 300)]
res = dict(all=row(pd.Series(True, index=df.index)), bins={})
for a, b in BINS:
    s = ((listed > a) | (a == 0)) & (listed <= b)
    res["bins"][f"{a + 1 if a else 0}-{b}"] = row(s)

# the same headline on the August count of Korean workers, as a check on timing
res["check_survey_count"] = dict(at_or_above=float((eps / cap_2019(korean) >= 1).mean()),
                                 want_past_2019=float((eps + extra > cap_2019(korean)).mean()))

# EPS firms by total workers: what the model's users are compared with
tot_bins = [(0, 10), (10, 20), (20, 50), (50, 100), (100, 200), (200, 300)]
res["by_total_workers"] = {f"{a}-{b}": dict(share_of_firms=float(((total >= a) & (total < b)).mean()),
                                            eps_share=float(share[(total >= a) & (total < b)].mean()))
                           for a, b in tot_bins}

hdr = ("firms", "eps", "cap_2019_use", "under_half", "near_cap_90", "at_or_above", "want_more", "want_more_if_at",
       "want_past_2019", "cap_2024_use", "at_or_above_2024", "want_past_2024")
print("bin      " + " ".join(f"{h[:11]:>11}" for h in hdr))
for name, r in [("all", res["all"])] + list(res["bins"].items()):
    print(f"{name:<9}" + " ".join(f"{(r[h] if r[h] is not None else float('nan')):>11.3f}" for h in hdr))
print("at or above the cap, firms by bin:", {k: v["at_or_above_firms"] for k, v in res["bins"].items()})
print("August count check:", res["check_survey_count"])
print("by total workers:", json.dumps(res["by_total_workers"]))
if len(sys.argv) > 1:
    json.dump(res, open(sys.argv[1], "w"), indent=1)
