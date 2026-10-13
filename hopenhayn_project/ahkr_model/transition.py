"""
Rung 3 -- perfect-foresight transition after a one-time, permanent drop in
the entry cost (kappa), starting from the old (distorted) BGP and converging
to the new (undistorted) BGP.

Simplifications relative to the full AHKR (2023) model, stated up front:
  1. gc (incumbent efficiency growth) is held FIXED at its calibrated value
     throughout the transition -- i.e. we do not solve the endogenous
     spillover g_c,t = gbar * g_t^epsilon off the balanced growth path. That
     would require the realized aggregate growth rate g_t as part of the
     fixed point, which is a substantially harder problem. This means Rung 2
     (retargeting epsilon to Korea) shows up here only through its effect on
     the *level* of gc used, not through a live feedback loop during the
     transition.
  2. The reform is a surprise, one-time, permanent change in kappa at t=0
     (an "MIT shock"), matching the paper's own entry-cost experiment.

What is NOT simplified: the exit decision is exactly the static zero-profit
condition (exact both on and off the BGP under simplification 1, since a
firm's efficiency relative to the frontier still declines deterministically
every period at the fixed rate gc/ge). The wage path is solved by exact
backward induction on the free-entry condition -- this part is not an
approximation. See solve_wage_path below for why backward induction works:
free entry at date t, E_x[V_t(x)] = kappa, is an equation in w_t, w_{t+1}, ...
alone (it does not involve the mass of entrants or the inherited population),
so the T+1 free-entry equations can be solved for the T+1 wages by working
backward from a terminal wage assumed equal to the new BGP wage.
"""
import numpy as np
from bgp import Params, solve_bgp, zero_profit_cutoff, pareto_quantiles, N_QUAD as BGP_N_QUAD

N_QUAD = 1500
MAX_AGE = 100
T_END = 16  # periods after the reform; each period = 5 years


def value_along_path(x_entry, w_path, xhat_path, p: Params):
    """E_x[V] etc. for a cohort born at the start of w_path/xhat_path, i.e.
    experiencing w_path[0], w_path[1], ... at ages 0, 1, 2, .... Vectorized
    over x_entry."""
    ratio = p.gc / p.ge
    x_s = x_entry.copy()
    V = np.zeros_like(x_entry)
    L0 = None  # age-0 labor demand (needed separately for entry-period clearing)
    disc_v = np.ones_like(x_entry)
    alive = np.ones_like(x_entry, dtype=bool)
    for s in range(len(w_path)):
        w_s, xhat_s = w_path[s], xhat_path[s]
        alive &= (x_s >= xhat_s)
        if not alive.any():
            break
        l = (p.alpha * x_s / w_s) ** (1.0 / (1.0 - p.alpha))
        d = x_s * l ** p.alpha - w_s * l - p.f
        V += np.where(alive, disc_v * d, 0.0)
        if s == 0:
            L0 = np.where(alive, l, 0.0)
        disc_v = disc_v * p.beta * (1 - p.delta)
        x_s = x_s * ratio
    if L0 is None:
        L0 = np.zeros_like(x_entry)
    return V, L0


def solve_wage_path(p_old: Params, p_new: Params, T_end=T_END, n=N_QUAD, tol=1e-9):
    """Backward induction: find w_0..w_{T_end} such that E_x[V_t(x)] = kappa_new
    for every t, given w_s = w_new for s > T_end."""
    w_new = solve_bgp(p_new)["w"]
    x_entry = pareto_quantiles(p_new.phi, p_new.gamma, n)

    w_path = np.full(T_end + 1, w_new)
    for t in range(T_end, -1, -1):
        future_w = w_path[t + 1:]
        future_xhat = np.array([zero_profit_cutoff(w, p_new) for w in future_w])

        def gap(w_t):
            w_seq = np.concatenate(([w_t], future_w, [w_new] * 20))
            xhat_seq = np.concatenate((
                [zero_profit_cutoff(w_t, p_new)], future_xhat, [zero_profit_cutoff(w_new, p_new)] * 20))
            V, _ = value_along_path(x_entry, w_seq, xhat_seq, p_new)
            return V.mean() - p_new.kappa

        lo, hi = w_new * 0.3, w_new * 3.0
        f_lo, f_hi = gap(lo), gap(hi)
        if not (f_lo > 0 > f_hi):
            lo, hi = w_new * 0.05, w_new * 10.0
            f_lo, f_hi = gap(lo), gap(hi)
        assert f_lo > 0 > f_hi, f"date {t}: wage bracket invalid ({f_lo}, {f_hi})"
        for _ in range(100):
            mid = np.sqrt(lo * hi)
            f_mid = gap(mid)
            if abs(f_mid) < tol:
                lo = hi = mid
                break
            if f_mid > 0:
                lo = mid
            else:
                hi = mid
        w_path[t] = np.sqrt(lo * hi)
    return w_path, w_new, x_entry


def run_transition(p_old: Params, p_new: Params, T_end=T_END):
    w_path, w_new, x_entry_new = solve_wage_path(p_old, p_new, T_end)
    xhat_path = np.array([zero_profit_cutoff(w, p_new) for w in w_path])

    # --- Old population, as of t=-1 (the instant before the reform) ---
    bgp_old = solve_bgp(p_old)
    w_old = bgp_old["w"]
    ratio = p_old.gc / p_old.ge
    x_entry_old = pareto_quantiles(p_old.phi, p_old.gamma, N_QUAD)
    xhat_old = bgp_old["x_hat"]

    # build the (quantile, age) grid of surviving old firms' current x-level
    old_x = []       # x-value of cell (quantile i, age a) at t=-1
    old_mass = []    # mass of that cell, per unit of mu_old
    x_a = x_entry_old.copy()
    disc = 1.0
    for a in range(MAX_AGE):
        alive = x_a >= xhat_old
        if not alive.any():
            break
        old_x.append(np.where(alive, x_a, np.nan))
        old_mass.append(np.where(alive, disc / N_QUAD, 0.0))
        x_a = x_a * ratio
        disc *= (1 - p_old.delta)
    old_x = np.array(old_x)       # (n_ages, N_QUAD)
    old_mass = np.array(old_mass) * bgp_old["mu"]  # absolute mass

    # --- Simulate forward: age the old population, add new cohorts each date ---
    results = []
    new_cohorts_x = []      # list of arrays: current x of each surviving new cohort
    new_cohorts_alive_mass = []  # scalar mass-per-quantile for each cohort (mu_t/N_QUAD), updated by survival
    ratio_new = p_new.gc / p_new.ge

    old_x_t = old_x.copy()  # will be aged forward each period

    prev_total_mass = old_mass.sum()
    for t in range(T_end + 1):
        xhat_t = xhat_path[t]
        w_t = w_path[t]

        with np.errstate(invalid="ignore"):
            # age + filter the old population by one more period
            old_x_t = old_x_t * ratio_new  # gc/ge assumed same for old firms post-reform (simplification 1)
            old_alive = old_x_t >= xhat_t
        old_mass_t = np.where(old_alive, old_mass, 0.0)
        l_old = np.where(old_alive, (p_new.alpha * old_x_t / w_t) ** (1 / (1 - p_new.alpha)), 0.0)
        old_L = np.nansum(l_old * old_mass_t)
        old_Y = np.nansum(np.where(old_alive, old_x_t * l_old ** p_new.alpha, 0.0) * old_mass_t)
        n_exit_old = np.nansum(old_mass) - np.nansum(old_mass_t)  # mass that just died
        old_mass = old_mass_t  # cells that just died stay dead forever
        old_mass_total = np.nansum(old_mass)

        # age + filter existing new cohorts
        new_L, new_Y, n_exit_new = 0.0, 0.0, 0.0
        for k in range(len(new_cohorts_x)):
            with np.errstate(invalid="ignore"):
                new_cohorts_x[k] = new_cohorts_x[k] * ratio_new
                alive_k = new_cohorts_x[k] >= xhat_t
            mass_before = new_cohorts_alive_mass[k].sum()
            new_cohorts_alive_mass[k] = np.where(alive_k, new_cohorts_alive_mass[k], 0.0)
            n_exit_new += mass_before - new_cohorts_alive_mass[k].sum()
            l_k = np.where(alive_k, (p_new.alpha * new_cohorts_x[k] / w_t) ** (1 / (1 - p_new.alpha)), 0.0)
            new_L += np.sum(l_k * new_cohorts_alive_mass[k])
            new_Y += np.sum(np.where(alive_k, new_cohorts_x[k] * l_k ** p_new.alpha, 0.0) * new_cohorts_alive_mass[k])

        # solve this period's entrant mass from labor market clearing
        entrant_alive = x_entry_new >= xhat_t
        l_entrant = np.where(entrant_alive, (p_new.alpha * x_entry_new / w_t) ** (1 / (1 - p_new.alpha)), 0.0)
        E_l_entrant = l_entrant.mean()
        remaining_labor = 1.0 - old_L - new_L
        mu_t = max(remaining_labor, 0.0) / E_l_entrant
        Y_entrant = np.mean(np.where(entrant_alive, x_entry_new * l_entrant ** p_new.alpha, 0.0)) * mu_t

        # register this period's cohort for future aging
        new_cohorts_x.append(x_entry_new.copy())
        new_cohorts_alive_mass.append(np.where(entrant_alive, mu_t / N_QUAD, 0.0))

        total_mass = old_mass_total + sum(m.sum() for m in new_cohorts_alive_mass)
        Y_t = old_Y + new_Y + Y_entrant
        entrant_emp_share = mu_t * E_l_entrant  # this period's brand-new entrants' share of total labor (=1)
        exit_mass_share = (n_exit_old + n_exit_new) / max(prev_total_mass, 1e-12)
        prev_total_mass = total_mass

        results.append(dict(t=t, w=w_t, x_hat=xhat_t, mu_entrants=mu_t, Y=Y_t,
                             old_mass=old_mass_total, total_mass=total_mass,
                             labor_old=old_L, labor_new=new_L,
                             entrant_emp_share=entrant_emp_share,
                             exit_mass_share=exit_mass_share))

    return dict(w_path=w_path, xhat_path=xhat_path, w_old=w_old, w_new=w_new,
                bgp_old=bgp_old, results=results)
