"""
Replication of Aiyagari (1994, QJE), "Uninsured Idiosyncratic Risk and
Aggregate Saving."

Household problem (his eq. 1a-1b, b = 0 / no borrowing):
    max E0 sum_t beta^t c_t^{1-mu}/(1-mu)
    s.t. c_t + a_{t+1} = w*l_t + (1+r)*a_t,   a_{t+1} >= 0

Solved by the endogenous grid method (EGM); the stationary distribution is
computed by the non-stochastic ("Young 2010") method rather than by Monte
Carlo simulation, which is what Aiyagari himself used. That's a deliberate
deviation: it removes simulation noise, so our numbers land close to but not
exactly on his Table II.
"""
import numpy as np
from tauchen import tauchen


def solve_household(mu, beta, r, w, l_grid, P, a_grid, tol=1e-9, maxiter=2000):
    """EGM solution of the household problem for fixed prices (r, w).

    Returns the savings policy a'(a, e) on `a_grid`, shape (na, ne).
    """
    na, ne = len(a_grid), len(l_grid)
    a_max = a_grid[-1]

    # initial guess: consume all resources up to a modest saving rate
    c = np.maximum(1e-8, w * l_grid[None, :] + r * a_grid[:, None])

    for _ in range(maxiter):
        mu_c = c ** (-mu)                       # (na, ne) marginal utility on a'-grid
        Emu = mu_c @ P.T                        # expected marg. util. next period, (na, ne)
        c_endo = (beta * (1 + r) * Emu) ** (-1 / mu)
        a_endo = (c_endo + a_grid[:, None] - w * l_grid[None, :]) / (1 + r)

        c_new = np.empty_like(c)
        for j in range(ne):
            # invert a_endo(a') -> a'(a) by interpolation, enforcing a' >= 0
            a_pol = np.interp(a_grid, a_endo[:, j], a_grid, left=0.0, right=a_max)
            c_new[:, j] = (1 + r) * a_grid + w * l_grid[j] - a_pol

        c_new = np.maximum(c_new, 1e-10)
        if np.max(np.abs(c_new - c)) < tol:
            c = c_new
            break
        c = c_new

    a_policy = (1 + r) * a_grid[:, None] + w * l_grid[None, :] - c
    a_policy = np.clip(a_policy, 0.0, a_max)
    return a_policy


def stationary_distribution(a_policy, P, a_grid, tol=1e-12, maxiter=10_000):
    """Non-stochastic (Young 2010) stationary distribution over (a, e)."""
    na, ne = a_policy.shape
    idx_lo = np.clip(np.searchsorted(a_grid, a_policy, side="right") - 1, 0, na - 2)
    a_lo = a_grid[idx_lo]
    a_hi = a_grid[idx_lo + 1]
    w_hi = np.clip((a_policy - a_lo) / (a_hi - a_lo), 0.0, 1.0)

    lam = np.ones((na, ne)) / (na * ne)
    for _ in range(maxiter):
        lam_new = np.zeros((na, ne))
        for j in range(ne):
            mass_lo = lam[:, j] * (1 - w_hi[:, j])
            mass_hi = lam[:, j] * w_hi[:, j]
            contrib = np.zeros(na)
            np.add.at(contrib, idx_lo[:, j], mass_lo)
            np.add.at(contrib, idx_lo[:, j] + 1, mass_hi)
            lam_new += np.outer(contrib, P[j])
        if np.max(np.abs(lam_new - lam)) < tol:
            lam = lam_new
            break
        lam = lam_new
    return lam


def firm_k_and_w(r, alpha, delta):
    K = (alpha / (r + delta)) ** (1 / (1 - alpha))
    w = (1 - alpha) * K ** alpha
    return K, w


def asset_supply(mu, beta, alpha, delta, l_grid, P, r, a_grid):
    _, w = firm_k_and_w(r, alpha, delta)
    a_policy = solve_household(mu, beta, r, w, l_grid, P, a_grid)
    lam = stationary_distribution(a_policy, P, a_grid)
    Ea = np.sum(lam * a_grid[:, None])
    return Ea, w, a_policy, lam


def solve_equilibrium(mu, beta, alpha, delta, l_grid, P, a_grid,
                       r_lo=None, r_hi=None, tol=1e-5, maxiter=60):
    """Bisect on r so household asset supply Ea(r) = firm capital demand K(r)."""
    lam_time_pref = 1 / beta - 1
    if r_hi is None:
        r_hi = lam_time_pref - 1e-4
    if r_lo is None:
        # Note: Ea(r) is only monotonic in a neighborhood of the equilibrium;
        # at very negative r the general-equilibrium wage effect makes it
        # non-monotonic (see aiyagari_replication debug notes). All of
        # Aiyagari's Table II equilibria lie in [-0.35%, 4.17%], so -1% is a
        # safe lower bound that avoids that region.
        r_lo = -0.01

    def excess_supply(r):
        Ea, *_ = asset_supply(mu, beta, alpha, delta, l_grid, P, r, a_grid)
        K, _ = firm_k_and_w(r, alpha, delta)
        return Ea - K

    f_lo, f_hi = excess_supply(r_lo), excess_supply(r_hi)
    assert f_lo < 0 < f_hi, f"bisection bracket invalid: f(lo)={f_lo}, f(hi)={f_hi}"

    for _ in range(maxiter):
        r_mid = 0.5 * (r_lo + r_hi)
        f_mid = excess_supply(r_mid)
        if abs(f_mid) < tol:
            break
        if f_mid > 0:
            r_hi = r_mid
        else:
            r_lo = r_mid

    r_star = 0.5 * (r_lo + r_hi)
    K_star, w_star = firm_k_and_w(r_star, alpha, delta)
    saving_rate = delta * K_star / (K_star ** alpha)  # delta*k / f(k,1)
    return r_star, K_star, w_star, saving_rate


def make_asset_grid(a_max, na, curvature=2.0):
    """Grid on [0, a_max], denser near the borrowing constraint at 0."""
    return a_max * np.linspace(0, 1, na) ** curvature
