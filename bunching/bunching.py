"""Bunching estimator for a threshold in a firm-level distribution.

Follows Chetty, Friedman, Olsen and Pistaferri (2011) and Kleven and Waseem
(2013): bin the running variable, fit a polynomial to the bin counts outside an
excluded window around the threshold, and compare actual counts inside the
window with the polynomial counterfactual.

    b = excess mass just below the threshold / average counterfactual count
        per bin in the window

b = 2 means two extra bins' worth of firms sit just below the threshold.
Standard errors come from a residual bootstrap.

Used for both project candidates:
  - Card fees: running variable = annual sales, thresholds at 300m, 500m, 1bn won.
  - EPS:       running variable = number of (Korean) workers, cap steps at
               10/11, 50/51, 100/101, 150/151, 200/201, eligibility at 300.

Usage:
  python3 bunching.py data.csv --var sales --threshold 300 --binwidth 5 \
      --window 280 300 --range 150 450 [--weight w] [--filter "industry==56"]
Run with --demo to check the estimator on simulated data with known bunching.
"""

import argparse

import numpy as np
import pandas as pd


def bin_counts(x, w, lo, hi, width):
    edges = np.arange(lo, hi + width, width)
    counts, _ = np.histogram(x, bins=edges, weights=w)
    mids = edges[:-1] + width / 2
    return mids, counts


def estimate(mids, counts, window, degree=7):
    """Excess mass b in [window[0], window[1]) relative to a polynomial fit."""
    inside = (mids >= window[0]) & (mids < window[1])
    z = (mids - mids.mean()) / mids.std()
    coef = np.polyfit(z[~inside], counts[~inside], degree)
    cf = np.polyval(coef, z)
    excess = (counts[inside] - cf[inside]).sum()
    return excess / cf[inside].mean(), cf, inside


def bunching(x, w, threshold, width, window, rng_lo, rng_hi, degree=7, reps=500, seed=0):
    mids, counts = bin_counts(x, w, rng_lo, rng_hi, width)
    b, cf, inside = estimate(mids, counts, window, degree)
    resid = counts - cf
    rng = np.random.default_rng(seed)
    boot = []
    for _ in range(reps):
        fake = cf + rng.choice(resid[~inside], size=len(cf), replace=True)
        boot.append(estimate(mids, fake, window, degree)[0])
    table = pd.DataFrame({"bin_mid": mids, "count": counts, "counterfactual": cf, "in_window": inside})
    return b, float(np.std(boot)), table


def demo():
    """Lognormal 'sales' with 3% of firms just above 300 moved to just below it."""
    rng = np.random.default_rng(1)
    x = rng.lognormal(mean=np.log(200), sigma=0.6, size=200_000)
    movers = (x > 300) & (x < 330) & (rng.random(x.size) < 0.6)
    x[movers] = rng.uniform(285, 300, movers.sum())
    for label, data in [("with planted bunching", x), ("placebo threshold 400", x)]:
        thr = 300 if "planted" in label else 400
        b, se, _ = bunching(data, None, thr, 5, (thr - 15, thr), thr - 150, thr + 150)
        print(f"{label:>24}: b = {b:6.2f}  (se {se:.2f})")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("csv", nargs="?")
    p.add_argument("--var")
    p.add_argument("--threshold", type=float)
    p.add_argument("--binwidth", type=float, default=5)
    p.add_argument("--window", type=float, nargs=2, help="excluded window [lower, upper)")
    p.add_argument("--range", type=float, nargs=2, dest="rng")
    p.add_argument("--weight")
    p.add_argument("--filter", help="pandas query string, e.g. \"industry==56\"")
    p.add_argument("--degree", type=int, default=7)
    p.add_argument("--out", help="save binned counts and counterfactual to this CSV")
    p.add_argument("--demo", action="store_true")
    a = p.parse_args()
    if a.demo:
        demo()
        return
    df = pd.read_csv(a.csv)
    if a.filter:
        df = df.query(a.filter)
    x = df[a.var].to_numpy(float)
    w = df[a.weight].to_numpy(float) if a.weight else None
    b, se, table = bunching(x, w, a.threshold, a.binwidth, a.window, *a.rng, degree=a.degree)
    n_near = ((x >= a.window[0]) & (x < a.window[1])).sum()
    print(f"threshold {a.threshold}: b = {b:.2f} (se {se:.2f}); firms in window: {n_near}")
    if a.out:
        table.to_csv(a.out, index=False)


if __name__ == "__main__":
    main()
