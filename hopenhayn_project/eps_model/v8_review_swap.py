"""Review, point 4: is the sign change in gross output from the new structure or the new parameters?
Solves today's rule and the price in both structures (theta rule = v5 code, random eligibility = v8 code)
with both parameter sets (v6_best, v8_best), same quota M. Writes v8_review_swap.json."""
import json
from multiprocessing import Pool

import run_v5
import run_v8

M = run_v8.M


def params(f):
    d = json.load(open(f))
    return {k: d[k] for k in run_v8.NAMES}


def job(j):
    struct, pf = j
    p = params(pf)
    b = run_v5.build if struct == "theta rule" else run_v8.build
    out = {}
    for reg in ("current", "neutral"):
        r = b(p, M).solve(reg)
        out[reg] = dict(Y=float(r["Y"]), net_Y=float(r["net_Y"]), firms=float(r["firms"]), users=float(r["users"]), x=float(r["x"]),
                        eq_error=float(r["eq_error"]))
    c, n = out["current"], out["neutral"]
    return dict(structure=struct, params=pf, gross=n["Y"] / c["Y"] - 1, net=n["net_Y"] / c["net_Y"] - 1,
                plants=n["firms"] / c["firms"] - 1, users_today=c["users"], users_price=n["users"], rule_var=c["x"],
                eq_error=max(c["eq_error"], n["eq_error"]))


if __name__ == "__main__":
    jobs = [(s, f) for s in ("theta rule", "random eligibility") for f in ("v6_best.json", "v8_best.json")]
    with Pool(4) as pool:
        res = pool.map(job, jobs)
    json.dump(res, open("v8_review_swap.json", "w"), indent=1)
    for d in res:
        print(f"{d['structure']:<19} {d['params']:<13} gross {100*d['gross']:+.2f}% net {100*d['net']:+.2f}% plants {100*d['plants']:+.2f}% "
              f"users {100*d['users_today']:.1f}% -> {100*d['users_price']:.1f}%  (theta or e = {d['rule_var']:.3f}, eq err {d['eq_error']:.3f})")
