"""
Hopenhayn (1992) with Korea's Employment Permit System (EPS).

Firm problem (slide 6 of the pitch deck, Week 2 notation):
    pi(s) = max_{n,m} s * f(n,m) - w*n - w_m*m - c_m*1[m>0] - c_f
    f(n,m) = (n^rho + lam * m^rho)^(alpha/rho)     Korean n, EPS m
    m <= 1[eligible] * q(n)                          statutory cap
    V(s) = pi(s) + max{0, beta * E[V(s')|s]},  sum_s nu(s) V(s) = c_e
    sum mu(s) n(s) = N   (clears w);   sum mu(s) m(s) = M  (clears w_m)

Output price p = 1 (numeraire). The Korean labor supply N and the national EPS
quota M are fixed, so every regime uses the same total inputs and differences
in output are differences in measured TFP. w_m is a shadow price that rations
the quota (in reality: the points system), not a wage firms choose.

Regimes:
    'none'     m = 0
    'current'  size-based cap q(n), eligible if n < 300   (2024 schedule)
    'neutral'  no cap, everyone eligible: same M allocated by a common price
               (tradable permits), i.e. the size-neutral counterfactual

All parameters are illustrative, set to hit rough Korean manufacturing
moments (average plant size, annual exit rate, EPS share); see run_eps.py.
"""
import numpy as np
from scipy.stats import norm


def tauchen(rho, sigma, n, m=3.0):
    sd = sigma / np.sqrt(1 - rho ** 2)
    y = np.linspace(-m * sd, m * sd, n)
    h = y[1] - y[0]
    P = np.zeros((n, n))
    for i in range(n):
        z = (y - rho * y[i]) / sigma
        up = norm.cdf(z + h / (2 * sigma))
        lo = norm.cdf(z - h / (2 * sigma))
        P[i] = up - lo
        P[i, 0] = up[0]
        P[i, -1] = 1 - lo[-1]
    return np.exp(y), P / P.sum(axis=1, keepdims=True)


def cap_2024(n):
    """Statutory total foreign-worker cap by number of Korean insured workers
    (eps.go.kr, 2024 standard, manufacturing)."""
    n = np.asarray(n, float)
    q = np.select(
        [n <= 10, n <= 50, n <= 100, n <= 150, n <= 200, n <= 300],
        [n + 10, np.minimum(30, 2 * n), 35, 40, 50, 60],
        default=80,
    )
    return q


class EPSModel:
    def __init__(self, alpha=0.80, rho=0.5, lam=0.5, beta=0.96, cf=1.0, ce=4.0, cm=0.5, delta=0.05,
                 rho_s=0.92, sigma_s=0.22, ns=40, nu_top=0.55,
                 N=1.0, M=0.0, cap=cap_2024, n_max=6000, m_max=3000):
        self.a, self.r, self.lam, self.beta, self.cf, self.ce, self.cm = alpha, rho, lam, beta, cf, ce, cm
        self.N, self.M, self.cap, self.delta = N, M, cap, delta
        self.s, self.P = tauchen(rho_s, sigma_s, ns)
        w = np.zeros(ns)
        k = int(nu_top * ns)
        w[:k] = norm.pdf(np.linspace(-2, 2, k))
        self.nu = w / w.sum()
        self.ng = np.concatenate([[0.0], np.geomspace(0.25, n_max, 260)])
        self.mg = np.concatenate([[0.0], np.geomspace(0.05, m_max, 170)])
        nn, mm = np.meshgrid(self.ng, self.mg, indexing="ij")
        if not 0 < rho < 1:
            raise ValueError("rho must be in (0,1): with rho <= 0 a firm with no EPS workers produces nothing")
        with np.errstate(divide="ignore", invalid="ignore"):
            agg = nn ** rho + lam * mm ** rho
            f = np.where(agg > 0, agg, 0.0) ** (alpha / rho)
        f[~np.isfinite(f)] = 0.0
        self.f = f                      # production per unit s, on (n, m) grid
        self.nn, self.mm = nn, mm

    # ---- static problem ------------------------------------------------
    def static(self, w, wm, regime):
        if regime == "none":
            feas = self.mm == 0
        elif regime == "current":
            feas = ((self.mm <= self.cap(self.nn)) & (self.nn >= 1) & (self.nn < 300)) | (self.mm == 0)
        elif regime == "neutral":
            feas = (self.nn >= 1) | (self.mm == 0)   # law: an EPS employer must have >= 1 Korean worker
        cost = w * self.nn + wm * self.mm + self.cm * (self.mm > 0)   # cm: fixed cost of using EPS
        pi = np.full(len(self.s), -np.inf)
        n = np.zeros(len(self.s)); m = np.zeros(len(self.s)); y = np.zeros(len(self.s))
        for i, si in enumerate(self.s):
            val = np.where(feas, si * self.f - cost, -np.inf)
            j = np.unravel_index(np.argmax(val), val.shape)
            pi[i], n[i], m[i], y[i] = val[j], self.nn[j], self.mm[j], si * self.f[j]
        return pi - self.cf, n, m, y

    # ---- dynamic problem -----------------------------------------------
    def values(self, pi):
        V = np.maximum(pi, 0)
        for _ in range(3000):
            Vn = pi + np.maximum(self.beta * (1 - self.delta) * self.P @ V, 0)
            if np.max(np.abs(Vn - V)) < 1e-9:
                break
            V = Vn
        stay = self.beta * (1 - self.delta) * self.P @ Vn >= 0
        return Vn, stay

    def stationary(self, stay):
        D = stay.astype(float)
        A = np.eye(len(self.s)) - (1 - self.delta) * self.P.T * D[None, :]
        return np.linalg.solve(A, self.nu)          # per unit mass of entrants

    def solve_given_wm(self, wm, regime):
        lo, hi = 1e-3, 50.0
        for _ in range(60):                         # free entry pins w
            w = np.sqrt(lo * hi)
            pi, n, m, y = self.static(w, wm, regime)
            V, stay = self.values(pi)
            if self.nu @ V > self.ce:
                lo = w
            else:
                hi = w
            if hi / lo < 1 + 1e-7:
                break
        mu1 = self.stationary(stay)
        Me = self.N / (mu1 @ n)                     # Korean labor market clears
        return dict(w=w, wm=wm, n=n, m=m, y=y, stay=stay, mu=Me * mu1, Me=Me)

    def solve(self, regime):
        if regime == "none" or self.M == 0:
            out = self.solve_given_wm(1e6, "none")
        else:
            lo, hi = 1e-4, 1e3                      # w_m rations the quota M
            for _ in range(80):
                wm = np.sqrt(lo * hi)
                out = self.solve_given_wm(wm, regime)
                demand = out["mu"] @ out["m"]
                if demand > self.M:
                    lo = wm
                else:
                    hi = wm
                if hi / lo < 1 + 1e-6:
                    break
        res = self.summarize(out, regime)
        if regime != "none" and self.M > 0:
            res["eq_error"] = abs(res["eps_total"] - self.M) / self.M   # must be ~0 in equilibrium
        else:
            res["eq_error"] = 0.0
        return res

    def summarize(self, o, regime):
        mu, n, m, y, stay = o["mu"], o["n"], o["m"], o["y"], o["stay"]
        firms = mu.sum()
        L = mu @ (n + m)
        exit_rate = (mu @ (1 - (1 - self.delta) * (self.P[:, stay]).sum(axis=1))) / firms   # exogenous + endogenous
        users = m > 0
        share_users = (mu[users] @ m[users]) / (mu[users] @ (n[users] + m[users])) if users.any() else 0.0
        small = (n + m) < 5
        return dict(
            regime=regime, share_small=(mu[small].sum() / firms), users=(mu[users].sum() / firms), Y=mu @ y, firms=firms, avg_size=L / firms,
            exit_rate=exit_rate, cutoff=self.s[np.argmax(stay)],
            w=o["w"], wm=o["wm"], eps_total=mu @ m, eps_share=(mu @ m) / L,
            eps_share_users=share_users,
            avg_s=(mu @ self.s) / firms,
            mu=mu, n=n, m=m, s=self.s,
        )
