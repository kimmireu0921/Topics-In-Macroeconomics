"""
Asturias, Hur, Kehoe, and Ruhl (2023), "Firm Entry and Exit and Aggregate
Growth" (AEJ: Macro) -- balanced growth path (BGP) solver.

Model (lecture_week02.pdf slides 45-51; paper sr544.pdf secs. 3-4):
  - Household: max sum beta^t log(C_t), pins q_{t+1} = beta/g_e on the BGP.
  - Firm with efficiency x: d_t(x) = max_l x*l^alpha - w_t*l - f_t,
    l_t(x) = (alpha*x/w_t)^(1/(1-alpha)).
  - V_t(x) = max{ d_t(x) + q_{t+1}*(1-delta)*V_{t+1}(g_{c,t+1}*x), 0 }.
  - Entrants pay kappa_t = kappa*g_e^t, draw x from Pareto
    F_t(x) = 1 - (phi*x/g_e^t)^(-gamma), x >= g_e^t/phi.
  - Free entry: E_x[V_t(x)] = kappa_t. Mass of entrants mu pinned by the
    labor market clearing condition (mu * E_x[labor demand over the firm's
    life] = 1).

Key BGP simplification (Proposition 1 in the paper): because a surviving
incumbent's efficiency *relative to the frontier* shrinks every period
(gc < ge in the US calibration), profitability declines monotonically over a
firm's life, so the exit decision collapses to a *static* zero-profit cutoff
d_t(x_hat_t) = 0 -- no forward-looking value comparison is needed for the
cutoff itself, only for E_x[V] in the free-entry condition.

We solve the BGP by detrending: x~ = x/g_e^t, w~ = w_t/g_e^t. On the BGP
these are time-invariant, d~(x~) = x~*l~^alpha - w~*l~ - f (detrended static
profit) is a time-invariant function, and a firm's efficiency trajectory
after entry is deterministic: x~_s = (gc/ge)^s * x~_entry for age s = 0,1,2,...
It operates while x~_s >= x_hat~, so per-firm lifetime sums (value, labor
demand, output, count) are finite sums evaluated by direct simulation over
age -- no value function iteration needed. Expectations over the Pareto
entry draw are computed by inverse-CDF quadrature.
"""
import numpy as np
from dataclasses import dataclass, replace


@dataclass
class Params:
    alpha: float = 0.67     # returns to scale
    beta: float = 0.98 ** 5  # discount factor, 5-year model period
    delta: float = 1 - 0.96 ** 5  # exogenous death rate
    gamma: float = 6.10     # Pareto tail parameter
    ge: float = 1.02 ** 5   # entrant efficiency growth
    gc: float = 1.019 ** 5  # incumbent (spillover) efficiency growth
    phi: float = 1.0        # barrier to technology adoption
    kappa: float = 0.38     # entry cost
    f: float = 0.46 * 5     # fixed continuation cost


N_QUAD = 4000
MAX_AGE = 300


def pareto_quantiles(phi, gamma, n=N_QUAD):
    """Inverse-CDF (midpoint) quadrature nodes for x ~ Pareto(phi, gamma):
    1 - F(x) = (phi*x)^(-gamma), x >= 1/phi. E[g(x)] ~= mean_i g(x_i)."""
    u = (np.arange(1, n + 1) - 0.5) / n
    x = (1.0 / phi) * u ** (-1.0 / gamma)
    return x


def firm_life_sums(x_entry, x_hat, w, p: Params, max_age=MAX_AGE):
    """For each entry draw in x_entry, sum discounted value, labor demand,
    output, and firm-count over the firm's (deterministic) operating life.
    Returns four arrays same shape as x_entry: V, L, Y, CNT."""
    ratio = p.gc / p.ge
    x_s = x_entry.copy()
    V = np.zeros_like(x_entry)
    L = np.zeros_like(x_entry)
    Y = np.zeros_like(x_entry)
    CNT = np.zeros_like(x_entry)
    disc_v = np.ones_like(x_entry)   # (beta*(1-delta))^s
    disc_l = np.ones_like(x_entry)   # (1-delta)^s
    for _ in range(max_age):
        active = x_s >= x_hat
        if not active.any():
            break
        l = (p.alpha * x_s / w) ** (1.0 / (1.0 - p.alpha))
        d = x_s * l ** p.alpha - w * l - p.f
        V += np.where(active, disc_v * d, 0.0)
        L += np.where(active, disc_l * l, 0.0)
        Y += np.where(active, disc_l * x_s * l ** p.alpha, 0.0)
        CNT += np.where(active, disc_l, 0.0)
        x_s = x_s * ratio
        disc_v = disc_v * p.beta * (1 - p.delta)
        disc_l = disc_l * (1 - p.delta)
    return V, L, Y, CNT


def zero_profit_cutoff(w, p: Params, lo=1e-8, hi=1e8, tol=1e-12, maxiter=200):
    """Solve d~(x_hat) = 0 for x_hat, given w (detrended static profit)."""
    def d(x):
        l = (p.alpha * x / w) ** (1.0 / (1.0 - p.alpha))
        return x * l ** p.alpha - w * l - p.f
    f_lo, f_hi = d(lo), d(hi)
    assert f_lo < 0 < f_hi, f"cutoff bracket invalid: d(lo)={f_lo}, d(hi)={f_hi}"
    for _ in range(maxiter):
        mid = np.sqrt(lo * hi)  # bisect in logs, profit is convex in x
        f_mid = d(mid)
        if abs(f_mid) < tol:
            return mid
        if f_mid > 0:
            hi = mid
        else:
            lo = mid
    return np.sqrt(lo * hi)


def expected_lifetime_sums(w, p: Params, n=N_QUAD):
    x_hat = zero_profit_cutoff(w, p)
    x_entry = pareto_quantiles(p.phi, p.gamma, n)
    V, L, Y, CNT = firm_life_sums(x_entry, x_hat, w, p)
    return dict(x_hat=x_hat, EV=V.mean(), EL=L.mean(), EY=Y.mean(),
                ECNT=CNT.mean(), x_entry=x_entry, V=V, L=L, Y=Y, CNT=CNT)


def solve_wage(p: Params, w_lo=1e-6, w_hi=1e6, tol=1e-9, maxiter=200):
    """Bisect on w so that free entry E_x[V] = kappa. E[V] is decreasing in w."""
    def gap(w):
        return expected_lifetime_sums(w, p)["EV"] - p.kappa
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


def solve_bgp(p: Params):
    w = solve_wage(p)
    sums = expected_lifetime_sums(w, p)
    mu = 1.0 / sums["EL"]  # labor market clearing: mu * E[L] = 1
    Y = mu * sums["EY"]
    total_mass = mu * sums["ECNT"]
    avg_size = 1.0 / total_mass  # total labor (=1) / mass of firms
    r_annual = (p.ge / p.beta) ** (1.0 / 5.0) - 1.0  # real interest rate, annualized

    # size distribution across (entry quantile, age) cells, for dispersion
    ratio = p.gc / p.ge
    x_s = sums["x_entry"].copy()
    sizes, masses = [], []
    disc_l = np.ones_like(x_s)
    for _ in range(MAX_AGE):
        active = x_s >= sums["x_hat"]
        if not active.any():
            break
        l = (p.alpha * x_s / w) ** (1.0 / (1.0 - p.alpha))
        sizes.append(l[active])
        masses.append((mu * disc_l[active] / N_QUAD))
        x_s = x_s * ratio
        disc_l = disc_l * (1 - p.delta)
    sizes, masses = np.concatenate(sizes), np.concatenate(masses)
    mean_size = np.average(sizes, weights=masses)
    sd_size = np.sqrt(np.average((sizes - mean_size) ** 2, weights=masses))

    fhk_entry_contribution = 1 - (1 - p.delta) * (p.gc / p.ge) ** p.gamma

    return dict(
        w=w, x_hat=sums["x_hat"], mu=mu, Y=Y, total_mass=total_mass,
        avg_size=avg_size, mean_size=mean_size, sd_size=sd_size,
        cv_size=sd_size / mean_size, r_annual=r_annual,
        fhk_entry_contribution=fhk_entry_contribution,
        entry_cost_over_continuation_cost=p.kappa / (p.f / 5),
    )
