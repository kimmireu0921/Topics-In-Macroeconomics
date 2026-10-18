import numpy as np
from scipy.stats import norm


def tauchen(rho, sigma, n=7, m=3):
    """
    Discretize log(l_t) = rho * log(l_{t-1}) + sigma * sqrt(1 - rho**2) * eps_t,
    eps_t ~ N(0, 1), into an n-state Markov chain (Tauchen 1986), following the
    procedure Aiyagari (1994, Sec. IV) attributes to Deaton (1991, p. 1232).

    sigma is the *unconditional* std of log(l_t) (Aiyagari's coefficient of
    variation). The innovation std is sigma * sqrt(1 - rho**2).

    Returns
    -------
    l_grid : (n,) grid of labor-endowment levels exp(y), normalized so that
             the stationary mean equals 1.
    P      : (n, n) transition matrix.
    pi     : (n,) stationary distribution of the chain.
    """
    sigma_u = sigma * np.sqrt(1 - rho ** 2)
    y_max = m * sigma
    y_min = -y_max
    y_grid = np.linspace(y_min, y_max, n)
    step = (y_max - y_min) / (n - 1)

    P = np.zeros((n, n))
    for i in range(n):
        mean = rho * y_grid[i]
        for j in range(n):
            lo = (y_grid[j] - mean - step / 2) / sigma_u
            hi = (y_grid[j] - mean + step / 2) / sigma_u
            if j == 0:
                P[i, j] = norm.cdf(hi)
            elif j == n - 1:
                P[i, j] = 1 - norm.cdf(lo)
            else:
                P[i, j] = norm.cdf(hi) - norm.cdf(lo)
        P[i] /= P[i].sum()

    pi = stationary_dist(P)
    l_grid = np.exp(y_grid)
    l_grid /= np.dot(pi, l_grid)  # normalize E[l] = 1
    return l_grid, P, pi


def stationary_dist(P, tol=1e-14, maxiter=100_000):
    n = P.shape[0]
    pi = np.ones(n) / n
    for _ in range(maxiter):
        pi_new = pi @ P
        if np.max(np.abs(pi_new - pi)) < tol:
            return pi_new
        pi = pi_new
    return pi
