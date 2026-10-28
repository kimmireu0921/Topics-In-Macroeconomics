"""
EPS model v5: v4 (eps_model.py) with a Pareto productivity tail and a size grid
that can show bunching at the cap steps (Prof. Hur's feedback, Oct 27).

Changes from v4:
  - Productivity s = x * z. x is permanent, drawn at entry from Pareto(1, gamma)
    (gamma = tail parameter, as in AHKR); z follows the v4 AR(1) (rho_s, sigma_s),
    entrants draw z from its stationary distribution. Replaces nu_top.
  - The size grid contains every cap step t and t(1 + 1e-6), and 300(1 - 1e-6), so a
    plant can sit exactly at or just past a step, as a profit maximizer would.
  - Faster solver (dominated grid points pruned; Brent's method for w, theta, p).
Everything else (tasks, premium, cap on h, two types, exit, markets) is as in v4.
"""
import numpy as np
from scipy.optimize import brentq

from eps_model import EPSModel, tauchen, cap_2024

STEPS = (5, 10, 30, 50, 100, 150, 200)     # 2019 and 2024 cap steps (Korean workers)


def pareto_nodes(gamma, nx, top=1e-4):
    """Log-spaced nodes for x ~ Pareto(1, gamma) up to the (1 - top) quantile, with
    the exact probability of each node's interval (the last node takes the tail)."""
    x = np.geomspace(1.0, top ** (-1.0 / gamma), nx)
    mid = np.sqrt(x[1:] * x[:-1])
    cdf = np.concatenate([[0.0], 1 - mid ** (-gamma), [1.0]])
    return x, np.diff(cdf)


class EPSModelV5(EPSModel):
    def __init__(self, types, alpha=0.69, rho=0.5, beta=0.96, ce=2.6, cm=0.5,
                 delta=0.0235, psi=0.0, xi=0.5, phi=1.0, sig_e=0.1, rho_s=0.9, sigma_s=0.2,
                 gamma=3.0, nx=24, nz=11, N=1.0, M=0.0, cap=cap_2024, h_max=20000, l_max=15000,
                 nh=320, nl=200):
        if not (-3 < rho < 1) or abs(rho) < 1e-3:
            raise ValueError("rho must be in (-3, 1) and not 0")
        self.a, self.r, self.beta, self.ce, self.cm = alpha, rho, beta, ce, cm
        self.delta, self.psi, self.xi, self.phi, self.sig_e = delta, psi, xi, phi, sig_e
        self.N, self.M, self.cap, self.gamma = N, M, cap, gamma
        z, Pz = tauchen(rho_s, sigma_s, nz)
        pz = np.ones(nz) / nz
        for _ in range(2000):
            pz = pz @ Pz
        xg, px = pareto_nodes(gamma, nx)
        self.s = np.kron(xg, z)                       # state (x_i, z_j) -> index i*nz + j
        self.P = np.kron(np.eye(nx), Pz)              # x permanent, z Markov
        self.nu = np.kron(px, pz)
        steps = np.array(STEPS, float)
        self.hg = np.unique(np.concatenate([[0.0, 1.0], np.geomspace(0.25, h_max, nh),
                                            steps, steps * (1 + 1e-6), [300 * (1 - 1e-6), 300.0]]))
        self.lg = np.concatenate([[0.0], np.geomspace(0.05, l_max, nl)])
        hh, ll = np.meshgrid(self.hg, self.lg, indexing="ij")
        self.hh, self.ll = hh, ll
        tot = sum(t["share"] for t in types)
        self.types = []
        for t in types:
            with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
                if rho > 0:
                    f = (hh ** rho + t["lam"] * ll ** rho) ** (alpha / rho)
                else:
                    f = np.where((hh > 0) & (ll > 0), (hh ** rho + t["lam"] * ll ** rho) ** (alpha / rho), 0.0)
            f[~np.isfinite(f)] = 0.0
            self.types.append(dict(lam=t["lam"], cf=t["cf"], share=t["share"] / tot, f=f, fr=f.ravel()))
        self.prem = psi * (1 + self.hg) ** (-xi)
        self.capv = cap(self.hg)

    def static(self, t, w, x, regime, m_limit_by_s=None):
        if m_limit_by_s is not None:
            return super().static(t, w, x, regime, m_limit_by_s)
        T = self.types[t]
        cost, M_, K_, RC = (a.ravel() for a in self._plan(w, x, regime))
        # A grid point can be optimal only if no cheaper point produces at least as much.
        o = np.argsort(cost, kind="stable")
        fo = T["fr"][o]
        best_before = np.concatenate([[-np.inf], np.maximum.accumulate(fo)[:-1]])
        cand = o[fo > best_before]
        val = self.s[:, None] * T["fr"][cand][None, :] - cost[cand][None, :]
        j = cand[val.argmax(1)]
        pi = val.max(1)
        return pi - T["cf"], self.hh.ravel()[j], K_[j], M_[j], self.s * T["fr"][j], RC[j]

    def solve_given_x(self, x, regime):
        def entry_value(logw):
            w = np.exp(logw)
            blocks, ve = [], 0.0
            for t, T in enumerate(self.types):
                pi, h, k, m, y, rc = self.static(t, w, x, regime)
                V, stay = self.values(pi)
                ve += T["share"] * (self.nu @ V)
                blocks.append(dict(pi=pi, h=h, k=k, m=m, y=y, rc=rc, V=V, stay=stay))
            entry_value.last = (w, blocks)
            return ve - self.ce

        logw = brentq(entry_value, np.log(1e-3), np.log(50.0), xtol=1e-9)   # free entry pins w
        entry_value(logw)
        w, blocks = entry_value.last
        kor = 0.0
        for t, B in enumerate(blocks):
            B["mu1"] = self.types[t]["share"] * self.stationary(B["stay"])
            kor += B["mu1"] @ (B["h"] + B["k"])
        Me = self.N / max(kor, 1e-300)
        for B in blocks:
            B["mu"] = Me * B["mu1"]
        return dict(w=w, x=x, Me=Me, blocks=blocks)

    def solve(self, regime):
        if regime == "none" or self.M == 0:
            out = self.solve_given_x(0.0, "none")
        else:
            cache = {}

            def excess(v):
                cache[v] = self.solve_given_x(v, regime)
                return self._eps_use(cache[v]) - self.M

            if regime == "current":                   # theta rations by quantity
                if excess(1.0) > 0:
                    th = brentq(excess, 0.0, 1.0, xtol=1e-5)
                    out = cache.get(th) or self.solve_given_x(th, regime)
                else:
                    out = cache[1.0]
            else:                                     # permit price p clears the quota
                if excess(0.0) > 0:
                    lo, hi = 0.0, 1.0
                    while hi < 1e4 and excess(hi) > 0:
                        lo, hi = hi, hi * 4
                    p = brentq(excess, lo, hi, xtol=1e-6)
                    out = cache.get(p) or self.solve_given_x(p, regime)
                else:
                    out = cache[0.0]
        res = self.summarize(out, regime)
        res["eq_error"] = abs(res["eps_total"] - self.M) / self.M if (regime != "none" and self.M > 0) else 0.0
        cat = lambda key: np.concatenate([B[key] for B in out["blocks"]])
        mu, n, m = cat("mu"), cat("h") + cat("k"), cat("m")
        res["share_50plus"] = mu[(n + m) >= 50].sum() / mu.sum()
        return res
