"""
Rung 4 -- add a feature Hopenhayn/AHKR cannot capture: a financial
constraint on entrants, in the spirit of the Song-Storesletten-Zilibotti
(2011) discussion earlier in the same lecture (F firms: low productivity,
good bank credit; E firms: high productivity, no external finance, must
self-fund) and motivated by Korea's own bank-directed, chaebol-favoring
financial system.

Modeling choice (kept deliberately simple, to stay tractable): a fraction
chi of potential entrants are "unconstrained" (chaebol-affiliated / good
collateral -- draw x freely from the Pareto) and are exactly the AHKR model.
The remaining (1-chi) are "constrained": operating at efficiency x requires
financing labor hires of l(x) up front, and a constrained entrant can only
finance up to l_max, i.e. can only ever operate at x <= x_cap (defined by
l(x_cap) = l_max). A constrained entrant who draws x > x_cap does not get to
operate at x -- it is capped at x_cap (it still enters and operates, just
below its "true" efficiency; this is the Midrigan-Xu-style "constrained
firms are too small" distortion, not exclusion from entry altogether).

This is a comparative-statics extension of the BGP (not the transition): we
resolve the free-entry / labor-clearing system with a mixture distribution
for the entrant draw and compare the resulting BGP to the frictionless one.
"""
import numpy as np
from dataclasses import dataclass
from bgp import Params, pareto_quantiles, zero_profit_cutoff, firm_life_sums, N_QUAD, MAX_AGE


@dataclass
class FinParams(Params):
    chi: float = 0.5       # fraction of entrants that are financially unconstrained
    l_max: float = 5.0     # max labor a constrained entrant can finance


_SHUFFLE_SEED = 12345


def capped_quantiles(p: FinParams, n=N_QUAD):
    """Draw n entrant efficiencies: chi unconstrained (raw Pareto), (1-chi)
    constrained (Pareto draw capped at x_cap, the efficiency level whose
    frictionless labor demand equals l_max, evaluated at a reference wage).
    Financial access (constrained vs not) is assigned *independently* of the
    entrepreneur's latent draw x -- credit access is not perfectly correlated
    with talent -- via a fixed pseudo-random permutation of quantile indices,
    so results vary smoothly and monotonically in chi."""
    x = pareto_quantiles(p.phi, p.gamma, n)
    perm = np.random.RandomState(_SHUFFLE_SEED).permutation(n)
    is_constrained = np.zeros(n, dtype=bool)
    is_constrained[perm[: int(round((1 - p.chi) * n))]] = True
    return x, is_constrained


def expected_lifetime_sums_financial(w, p: FinParams, n=N_QUAD):
    x_cap = (p.l_max) ** (1 - p.alpha) * w / p.alpha  # invert l(x)=(alpha x/w)^{1/(1-alpha)} = l_max
    x_raw, is_constrained = capped_quantiles(p, n)
    x_entry = np.where(is_constrained, np.minimum(x_raw, x_cap), x_raw)
    x_hat = zero_profit_cutoff(w, p)
    V, L, Y, CNT = firm_life_sums(x_entry, x_hat, w, p)
    return dict(x_hat=x_hat, x_cap=x_cap, EV=V.mean(), EL=L.mean(), EY=Y.mean(), ECNT=CNT.mean())


def solve_wage_financial(p: FinParams, w_lo=1e-6, w_hi=1e6, tol=1e-9, maxiter=200):
    def gap(w):
        return expected_lifetime_sums_financial(w, p)["EV"] - p.kappa
    f_lo, f_hi = gap(w_lo), gap(w_hi)
    assert f_lo > 0 > f_hi, f"wage bracket invalid: gap(lo)={f_lo}, gap(hi)={f_hi}"
    for _ in range(maxiter):
        w_mid = np.sqrt(w_lo * w_hi)
        f_mid = gap(w_mid)
        if abs(f_mid) < tol:
            return w_mid
        if f_mid > 0:
            w_lo = w_mid
        else:
            w_hi = w_mid
    return np.sqrt(w_lo * w_hi)


def solve_bgp_financial(p: FinParams):
    w = solve_wage_financial(p)
    sums = expected_lifetime_sums_financial(w, p)
    mu = 1.0 / sums["EL"]
    Y = mu * sums["EY"]
    total_mass = mu * sums["ECNT"]
    return dict(w=w, x_hat=sums["x_hat"], x_cap=sums["x_cap"], mu=mu, Y=Y,
                total_mass=total_mass, avg_size=1.0 / total_mass)
