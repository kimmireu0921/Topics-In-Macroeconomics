"""
Reproduce Aiyagari (1994) Table II: net return to capital (%) and the
aggregate saving rate (%), for sigma in {0.2, 0.4}, rho in {0, 0.3, 0.6, 0.9},
mu in {1, 3, 5}.

Paper's numbers (r% / saving rate%), for reference:

  sigma=0.2         mu=1            mu=3            mu=5
  rho=0    4.1666/23.67    4.1456/23.71    4.0858/23.83
  rho=0.3  4.1365/23.73    4.0432/23.91    3.9054/24.19
  rho=0.6  4.0912/23.82    3.8767/24.25    3.5857/24.86
  rho=0.9  3.9305/24.14    3.2903/25.51    2.5260/27.36

  sigma=0.4         mu=1            mu=3            mu=5
  rho=0    4.0649/23.87    3.7816/24.44    3.4177/25.22
  rho=0.3  3.9554/24.09    3.4188/25.22    2.8032/26.66
  rho=0.6  3.7567/24.50    2.7835/26.71    1.8070/29.37
  rho=0.9  3.3054/25.47    1.2894/31.00   -0.3456/37.63

Full-insurance (complete markets) benchmark: r = 4.17%, saving rate = 23.67%.
"""
import time
import numpy as np
from tauchen import tauchen
from aiyagari import make_asset_grid, solve_equilibrium

BETA, ALPHA, DELTA = 0.96, 0.36, 0.08
A_MAX, NA = 100.0, 200
N_STATES = 7

sigmas = [0.2, 0.4]
rhos = [0.0, 0.3, 0.6, 0.9]
mus = [1, 3, 5]

paper = {
    (0.2, 0.0, 1): (4.1666, 23.67), (0.2, 0.0, 3): (4.1456, 23.71), (0.2, 0.0, 5): (4.0858, 23.83),
    (0.2, 0.3, 1): (4.1365, 23.73), (0.2, 0.3, 3): (4.0432, 23.91), (0.2, 0.3, 5): (3.9054, 24.19),
    (0.2, 0.6, 1): (4.0912, 23.82), (0.2, 0.6, 3): (3.8767, 24.25), (0.2, 0.6, 5): (3.5857, 24.86),
    (0.2, 0.9, 1): (3.9305, 24.14), (0.2, 0.9, 3): (3.2903, 25.51), (0.2, 0.9, 5): (2.5260, 27.36),
    (0.4, 0.0, 1): (4.0649, 23.87), (0.4, 0.0, 3): (3.7816, 24.44), (0.4, 0.0, 5): (3.4177, 25.22),
    (0.4, 0.3, 1): (3.9554, 24.09), (0.4, 0.3, 3): (3.4188, 25.22), (0.4, 0.3, 5): (2.8032, 26.66),
    (0.4, 0.6, 1): (3.7567, 24.50), (0.4, 0.6, 3): (2.7835, 26.71), (0.4, 0.6, 5): (1.8070, 29.37),
    (0.4, 0.9, 1): (3.3054, 25.47), (0.4, 0.9, 3): (1.2894, 31.00), (0.4, 0.9, 5): (-0.3456, 37.63),
}

a_grid = make_asset_grid(A_MAX, NA)

print(f"{'sigma':>5} {'rho':>5} {'mu':>3} | {'r (ours)':>9} {'r (paper)':>9} | "
      f"{'save% (ours)':>13} {'save% (paper)':>13}")
print("-" * 78)

t0 = time.time()
for sigma in sigmas:
    for rho in rhos:
        l_grid, P, pi = tauchen(rho, sigma, n=N_STATES)
        for mu in mus:
            r_star, K_star, w_star, s_star = solve_equilibrium(
                mu, BETA, ALPHA, DELTA, l_grid, P, a_grid
            )
            r_paper, s_paper = paper[(sigma, rho, mu)]
            print(f"{sigma:5.1f} {rho:5.1f} {mu:3d} | "
                  f"{100*r_star:9.4f} {r_paper:9.4f} | "
                  f"{100*s_star:13.2f} {s_paper:13.2f}")

print("-" * 78)
print(f"Done in {time.time() - t0:.1f}s")
