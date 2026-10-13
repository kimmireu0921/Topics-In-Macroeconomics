"""
Run Rung 1: solve Hopenhayn (1992), report the size distribution and the
exit-rate-by-size / exit-rate-by-age patterns, and compare qualitatively to
the BDS facts documented in lecture_week02.pdf (slides 5-8):

  - US establishment entry/exit rates are both around 10-11% per year.
  - About 60% of US firms have fewer than 5 employees but only ~5% of
    employment; firms with 10,000+ employees are a rounding error in counts
    but ~30% of employment (slide 6).
  - Exit rates fall with size and with age (slide 15's theoretical claim,
    which is the standard BDS pattern this model is built to reproduce).
"""
import numpy as np
from hopenhayn import (
    solve_hopenhayn, exit_rate_by_state, cohort_exit_rates_by_age, tauchen,
    entrant_distribution, RHO, SIGMA_INNOV, N_GRID,
)

D_SCALE = 50.0
def D_demand(p):
    return D_SCALE / p  # unit-elastic demand


def main():
    s_grid, P = tauchen(RHO, SIGMA_INNOV, N_GRID)
    nu = entrant_distribution(s_grid)
    eq = solve_hopenhayn(D_demand, s_grid, P, nu)

    p, s_star, k = eq["p_star"], eq["s_star"], eq["cutoff_idx"]
    mu, n_pol = eq["mu"], eq["n_policy"]
    total_firms = mu.sum()
    total_emp = np.dot(n_pol, mu)

    print(f"Equilibrium price p* = {p:.4f}")
    print(f"Exit cutoff s*(p*) = {s_star:.4f}  (grid index {k}/{N_GRID})")
    print(f"Mass of entrants M* = {eq['M_star']:.4f}")
    print(f"Total operating firms = {total_firms:.4f}, total employment = {total_emp:.4f}")
    print(f"Average firm size = {total_emp/total_firms:.2f} employees")

    # Aggregate exit rate (weighted average over the stationary cross-section)
    exit_by_state = exit_rate_by_state(s_grid, P, k)
    agg_exit_rate = np.dot(exit_by_state[k:], mu[k:]) / mu[k:].sum()
    print(f"Aggregate (mass-weighted) exit rate = {100*agg_exit_rate:.2f}%  "
          f"(BDS: US establishment exit rate is about 10-11%, slide 5)")

    # Exit rate by size decile
    print("\nExit rate by employment-size decile (1 = smallest operating firms):")
    order = np.argsort(n_pol[k:])
    n_op, mu_op, exit_op = n_pol[k:][order], mu[k:][order], exit_by_state[k:][order]
    cum_mass = np.cumsum(mu_op)
    deciles = np.searchsorted(cum_mass, np.linspace(0, cum_mass[-1], 11)[1:-1])
    bounds = [0] + list(deciles) + [len(n_op)]
    for d in range(10):
        lo, hi = bounds[d], bounds[d + 1]
        if hi <= lo:
            continue
        avg_n = np.average(n_op[lo:hi], weights=mu_op[lo:hi])
        avg_exit = np.average(exit_op[lo:hi], weights=mu_op[lo:hi])
        print(f"  decile {d+1:2d}: avg size {avg_n:8.1f} employees -> exit rate {100*avg_exit:5.2f}%")

    # Exit rate by age
    print("\nExit rate (hazard) by firm age:")
    hazards = cohort_exit_rates_by_age(s_grid, P, nu, k, n_ages=8)
    for a, h in enumerate(hazards):
        print(f"  age {a}: {100*h:5.2f}%")

    # Employment share of smallest vs largest firms, for the BDS comparison
    small_mask = n_pol[k:] < 5
    huge_mask = n_pol[k:] > np.percentile(n_pol[k:], 99)
    mu_op_all, n_op_all = mu[k:], n_pol[k:]
    firm_share_small = mu_op_all[small_mask].sum() / mu_op_all.sum()
    emp_share_small = np.dot(n_op_all[small_mask], mu_op_all[small_mask]) / total_emp
    emp_share_huge = np.dot(n_op_all[huge_mask], mu_op_all[huge_mask]) / total_emp
    print(f"\nShare of firms with <5 employees: {100*firm_share_small:.1f}%  "
          f"(BDS: ~60%, slide 6)")
    print(f"Employment share of firms with <5 employees: {100*emp_share_small:.1f}%  "
          f"(BDS: ~5%, slide 6)")
    print(f"Employment share of top 1% by size: {100*emp_share_huge:.1f}%  "
          f"(BDS: ~30% for 10,000+ employee firms, slide 6)")


if __name__ == "__main__":
    main()
