"""Moment book for the v8/v9 model: every model moment that a data source can be compared with, computed from a
solved economy, in the size bands of the Ministry request (Korean insured workers n = h + k):
    B bands: 1-5, 6-10, 11-30, 31-50, 51-100, 101-300, 301+
Used by calibrate_v9.py (targets) and results_v9.py (checks). Nothing here changes the model.

Each moment's data counterpart is noted next to it:
  [census]   MDIS business census 2024           [survey]  KDI-World Bank EPS survey 2019
  [moel-k]   Ministry disclosure request item k  [lpy]     Lee, Peri and Yang (2026)
  [mlfs]     Ministry occupational labour force survey at establishments (직종별사업체노동력조사)
"""
import numpy as np

BANDS = [(1, 5), (6, 10), (11, 30), (31, 50), (51, 100), (101, 300), (301, np.inf)]
BAND_NAMES = ["1-5", "6-10", "11-30", "31-50", "51-100", "101-300", "301+"]
USE_BUCKETS = [(0, 0.5), (0.5, 0.9), (0.9, 0.99999), (0.99999, 1.00001), (1.00001, np.inf)]   # [moel-3]
USE_NAMES = ["<50%", "50-90%", "90-<100%", "100%", ">100%"]
MANUAL_BUCKETS = [(-1e-12, 1e-12), (1e-12, 0.25), (0.25, 0.5), (0.5, 0.75), (0.75, 1.0 + 1e-12)]  # [moel-10]
MANUAL_NAMES = ["0%", "0-25%", "25-50%", "50-75%", "75%+"]


def _cat(out, key):
    return np.concatenate([B[key] for B in out["blocks"]])


def _band(n, lo, hi):
    return (n >= lo - 0.5) & (n < hi + 0.5) if np.isfinite(hi) else (n >= lo - 0.5)


def book(mod, r, regime="current"):
    """All moments of a solved economy r (from mod.solve(regime)). Shares are of plant mass."""
    out = r["out"]
    mu, h, k, m, y = (_cat(out, x) for x in ("mu", "h", "k", "m", "y"))
    stay = _cat(out, "stay")
    elig = np.concatenate([np.full(len(B["mu"]), B["eligible"]) for B in out["blocks"]])
    typ = np.concatenate([np.full(len(B["mu"]), B["type"]) for B in out["blocks"]])
    n = h + k                                   # Korean (insured) workers
    tot = n + m
    u = m > 0
    exit_p = 1 - (1 - mod.delta) * stay         # yearly exit probability
    q = mod.cap(n) if regime == "current" else np.full_like(n, np.nan)
    W = mu.sum()
    d = {}
    # ---- census-type moments (all plants, total workers) [census]
    d["avg_size"] = float(mu @ tot / W)
    d["share_small"] = float(mu[tot < 5].sum() / W)
    d["share_50plus"] = float(mu[tot >= 50].sum() / W)
    d["exit_rate"] = float(mu @ exit_p / W)
    # ---- EPS use [moel-2], [census]
    d["users"] = float(mu[u].sum() / W)
    d["eps_share_workers"] = float(mu @ m / (mu @ tot))
    d["eps_per_user"] = float(mu[u] @ m[u] / mu[u].sum()) if u.any() else 0.0
    # ---- by Korean-worker band [moel-1], [moel-2], [moel-3], [moel-7]
    bands = {}
    for name, (lo, hi) in zip(BAND_NAMES, BANDS):
        i = _band(n, lo, hi)
        iu = i & u
        bd = dict(plants=float(mu[i].sum() / W), user_rate=float(mu[iu].sum() / max(mu[i].sum(), 1e-300)),
                  eps_workers=float(mu[iu] @ m[iu] / max(mu @ m, 1e-300)),
                  exit_users=float(mu[iu] @ exit_p[iu] / max(mu[iu].sum(), 1e-300)) if iu.any() else None,
                  exit_nonusers=float(mu[i & ~u] @ exit_p[i & ~u] / max(mu[i & ~u].sum(), 1e-300)) if (i & ~u).any() else None)
        if regime == "current" and iu.any():
            use = m[iu] / q[iu]
            w = mu[iu] / mu[iu].sum()
            bd["cap_use_mean"] = float(w @ use)
            bd["cap_use_buckets"] = {nm: float(w[(use >= a) & (use < b)].sum()) for nm, (a, b) in zip(USE_NAMES, USE_BUCKETS)}
        bands[name] = bd
    d["by_band"] = bands
    # ---- exit by EPS status [moel-7]
    d["exit_users"] = float(mu[u] @ exit_p[u] / mu[u].sum()) if u.any() else None
    d["exit_nonusers"] = float(mu[~u] @ exit_p[~u] / mu[~u].sum())
    # ---- cap use, all users [moel-3], [survey]
    if regime == "current" and u.any():
        use = m[u] / q[u]
        w = mu[u] / mu[u].sum()
        d["cap_use_mean"] = float(w @ use)
        d["at_or_above_cap"] = float(w[use >= 1 - 1e-6].sum())
        d["cap_use_buckets"] = {nm: float(w[(use >= a) & (use < b)].sum()) for nm, (a, b) in zip(USE_NAMES, USE_BUCKETS)}
    # ---- manual share of workers [moel-10]: (k + m) / (h + k + m), all plants
    man = np.where(tot > 0, (k + m) / np.maximum(tot, 1e-12), 0.0)
    d["manual_share_buckets"] = {nm: float(mu[(man > a) & (man <= b)].sum() / W) if a >= 0 else float(mu[man <= b].sum() / W)
                                 for nm, (a, b) in zip(MANUAL_NAMES, MANUAL_BUCKETS)}
    d["manual_intensive_plants"] = float(mu[typ == 1].sum() / W)
    # ---- access [moel-4]: applicants = plants that would use EPS if eligible (static plan at today's prices)
    if regime == "current":
        would = 0.0
        for B in out["blocks"]:
            if B["eligible"]:
                would += B["mu"][B["m"] > 0].sum()
            else:
                b_el = mod.blocks_def.index((B["type"], True))
                _, _, _, m_if, _, _ = mod.static_block(b_el, out["w"], out["x"], regime)
                would += B["mu"][m_if > 0].sum()
        d["applicants"] = float(would / W)
        d["allocation_rate"] = float(d["users"] / max(d["applicants"], 1e-300))
    d["eligible_share_entrants"] = float(out["x"]) if regime == "current" else None
    d["wage"] = float(out["w"])
    return d
