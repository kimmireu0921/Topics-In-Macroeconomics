"""
Rung 1 -- Replicate Hopenhayn (1992), "Entry, Exit, and Firm Dynamics in Long
Run Equilibrium," Econometrica.

Follows the exposition in lecture_week02.pdf, slides 13-19:
  - firms on a grid of productivity s_1 < ... < s_N, following a monotone,
    persistent Markov chain F(s'|s) (Tauchen discretization of an AR(1) in
    log s);
  - production q = s*n^alpha (decreasing returns, alpha < 1), a fixed
    operating cost cf, wage normalized to 1;
  - an unlimited pool of entrants who pay ce to draw s ~ nu;
  - a single equilibrium object, the price p, pinned down by free entry
    V^e(p) = ce;
  - the stationary distribution and mass of entrants M solved as a linear
    system, then scaled to clear the goods market.

No source in the lecture material gives numerical values for the Markov
chain (rho, sigma) -- Hopenhayn (1992) predates BDS and the slides don't
calibrate this model to data, they only describe the mechanism. Technology
parameters (alpha, beta, cf, ce) are reused from the Asturias-Hur-Kehoe-Ruhl
(2023) US calibration (lecture slide 53, Table 4) so that Rung 1 and
Rungs 2-4 share one consistent technology; (rho, sigma) for the AR(1) and the
entrant distribution nu are illustrative choices, documented below, chosen to
produce a plausible size distribution -- not fit to any data. That is
appropriate for Rung 1: the point is the *mechanism* (does exit fall in size
and age?), not decimal-matching BDS.
"""
import numpy as np
from scipy.stats import norm

# ---- Technology parameters, reused from AHKR (2023) Table 4, US calibration ----
ALPHA = 0.67          # returns to scale
BETA = 0.98 ** 5       # discount factor (AHKR use a 5-year model period)
CF = 0.46 * 5          # fixed operating cost ("continuation cost" in AHKR)
CE = 0.38              # entry cost
WAGE = 1.0             # numeraire

# ---- Illustrative Markov chain for log(s), NOT targeted to any moment ----
RHO = 0.9
SIGMA_INNOV = 0.25
N_GRID = 25


def tauchen(rho, sigma_innov, n, m=3.5):
    sigma_y = sigma_innov / np.sqrt(1 - rho ** 2)
    y = np.linspace(-m * sigma_y, m * sigma_y, n)
    step = y[1] - y[0]
    P = np.zeros((n, n))
    for i in range(n):
        mean = rho * y[i]
        for j in range(n):
            lo, hi = (y[j] - mean - step / 2) / sigma_innov, (y[j] - mean + step / 2) / sigma_innov
            if j == 0:
                P[i, j] = norm.cdf(hi)
            elif j == n - 1:
                P[i, j] = 1 - norm.cdf(lo)
            else:
                P[i, j] = norm.cdf(hi) - norm.cdf(lo)
        P[i] /= P[i].sum()
    return np.exp(y), P


def entrant_distribution(s_grid):
    """nu: entrants draw disproportionately from the lower part of the grid
    (a new plant starts small) -- a lognormal-ish density truncated to the
    bottom 60% of the grid, renormalized to sum to 1. Illustrative, as noted
    above."""
    n = len(s_grid)
    weights = np.zeros(n)
    cutoff = int(0.6 * n)
    weights[:cutoff] = norm.pdf(np.linspace(-2, 2, cutoff))
    return weights / weights.sum()


def firm_policy(s_grid, p, alpha=ALPHA, wage=WAGE):
    n = (p * s_grid * alpha / wage) ** (1 / (1 - alpha))
    revenue = p * s_grid * n ** alpha
    profit = revenue - wage * n
    return n, profit


def solve_value_and_cutoff(s_grid, P, p, cf=CF, beta=BETA, tol=1e-10, maxiter=5000):
    n, pi_static = firm_policy(s_grid, p)
    pi_static = pi_static - cf
    V = np.maximum(pi_static, 0.0)
    for _ in range(maxiter):
        cont = beta * (P @ V)
        V_new = pi_static + np.maximum(cont, 0.0)
        if np.max(np.abs(V_new - V)) < tol:
            V = V_new
            break
        V = V_new
    cont = beta * (P @ V)
    operate = cont >= 0.0
    cutoff_idx = np.argmax(operate) if operate.any() else len(s_grid)
    return V, n, pi_static, cutoff_idx


def free_entry_gap(p, s_grid, P, nu, ce=CE):
    V, *_ = solve_value_and_cutoff(s_grid, P, p)
    return np.dot(nu, V) - ce


def solve_equilibrium_price(s_grid, P, nu, p_lo=0.01, p_hi=50.0, tol=1e-8, maxiter=100):
    f_lo, f_hi = free_entry_gap(p_lo, s_grid, P, nu), free_entry_gap(p_hi, s_grid, P, nu)
    assert f_lo < 0 < f_hi, f"bracket invalid: f(lo)={f_lo}, f(hi)={f_hi}"
    for _ in range(maxiter):
        p_mid = 0.5 * (p_lo + p_hi)
        f_mid = free_entry_gap(p_mid, s_grid, P, nu)
        if abs(f_mid) < tol:
            return p_mid
        if f_mid > 0:
            p_hi = p_mid
        else:
            p_lo = p_mid
    return 0.5 * (p_lo + p_hi)


def stationary_distribution(s_grid, P, nu, cutoff_idx, M=1.0):
    """mu(s') = sum_{s>=s*} F(s'|s) mu(s) + M * nu(s') * 1{s'>=s*}

    i.e. entrants draw s ~ nu and, if s >= cutoff, operate *immediately*
    (collecting pi(s,p) the period they draw); the stationary cross-section
    is everyone currently operating, incumbents and this period's entrants
    alike. See module docstring for why this convention was chosen over the
    one implied by a literal reading of slide 18.
    """
    n = len(s_grid)
    D = np.zeros(n)
    D[cutoff_idx:] = 1.0
    A = np.eye(n) - P.T * D[np.newaxis, :]  # (I - P^T D), D acting on incoming state s
    rhs = M * D * nu
    mu = np.linalg.solve(A, rhs)
    return mu


def solve_hopenhayn(D_demand, s_grid=None, P=None, nu=None):
    """Full equilibrium: price, cutoff, value/policy functions, and the
    stationary distribution scaled to clear the goods market D_demand(p)."""
    if s_grid is None:
        s_grid, P = tauchen(RHO, SIGMA_INNOV, N_GRID)
        nu = entrant_distribution(s_grid)

    p_star = solve_equilibrium_price(s_grid, P, nu)
    V, n_pol, pi_static, cutoff_idx = solve_value_and_cutoff(s_grid, P, p_star)
    mu_unit = stationary_distribution(s_grid, P, nu, cutoff_idx, M=1.0)

    output_unit = np.dot(s_grid * n_pol ** ALPHA, mu_unit)
    M_star = D_demand(p_star) / output_unit
    mu = mu_unit * M_star

    return {
        "s_grid": s_grid, "P": P, "nu": nu, "p_star": p_star,
        "cutoff_idx": cutoff_idx, "s_star": s_grid[cutoff_idx],
        "V": V, "n_policy": n_pol, "pi_static": pi_static,
        "mu": mu, "M_star": M_star,
    }


def exit_rate_by_state(s_grid, P, cutoff_idx):
    """Probability an operating firm at s_i draws s' below cutoff next period."""
    survive_prob = P[:, cutoff_idx:].sum(axis=1)
    exit_rate = 1.0 - survive_prob
    return exit_rate  # defined for all i; only i >= cutoff_idx is meaningful


def cohort_exit_rates_by_age(s_grid, P, nu, cutoff_idx, n_ages=10):
    """Track one entering cohort forward; return the hazard of exit at each
    age. Age-0 mass is nu itself: every entrant produces (collects pi(s,p),
    per the Bellman equation) in its draw period regardless of s, then exits
    if s < s*. Age-a>=1 mass may also straddle the cutoff, since F can carry
    a survivor's state anywhere next period."""
    n = len(s_grid)
    D = np.zeros(n)
    D[cutoff_idx:] = 1.0
    cohort = nu.copy()
    hazards = []
    for _ in range(n_ages):
        total = cohort.sum()
        survivors = D * cohort
        hazards.append(1 - survivors.sum() / total)
        cohort = P.T @ survivors
    return np.array(hazards)
