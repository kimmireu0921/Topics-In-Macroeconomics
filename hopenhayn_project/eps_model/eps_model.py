"""
Hopenhayn (1992) with Korea's Employment Permit System (EPS), task-based, two
plant types (v4).

Production uses two tasks:
    y = s * f_t(h, l),   f_t(h, l) = (h^rho + lam_t * l^rho)^(alpha/rho)
    h : core work, done by Korean workers (wage w)
    l : manual work, done by EPS workers m or Korean manual workers k (l = k + m)
Plant types t (drawn at entry with probability share_t) differ in the weight on
manual work lam_t and the fixed operating cost cf_t: a 'light' type and a
'manual-intensive' type (casting, plastics, textiles...). With one type, size and
survival line up exactly and the marginal plants are tiny; with two, mid-sized
manual-intensive plants can be fragile, as in Lee, Peri and Yang (2026).

Korean manual workers are scarce for small plants ("no applicants"):
    cost of k = w * (1 + psi * (1 + h)^(-xi)) per worker   (premium = resource cost)
EPS workers cost phi * w (wage plus room and board; phi = 1 in the data:
W2.93m vs W2.6m for Koreans), plus a fixed cost c_m of using EPS at all.

Current rule: the national quota M is rationed by QUANTITY (the points system):
    m <= theta * 1[1 <= h < 300] * q(h + k),   q(h+k) approximated by q(h),
with theta in (0, 1] set so total EPS use equals M. Plants keep the rent.
Size-neutral counterfactual: the same M allocated by PRICE (tradable permits):
EPS cost phi*w + p, no cap, p clears M (the rent goes to the permit seller).

Dynamics (Week 2 notation, with exogenous exit delta and a logit taste shock in
the exit decision, scale sig_e, which makes exit smooth in the parameters):
    V_t(s) = pi_t(s) + sig_e * log(1 + exp(c_t(s)/sig_e)),  c_t(s) = beta (1-delta) E[V_t(s')|s]
    P(stay | s) = 1 / (1 + exp(-c_t(s)/sig_e))
    free entry: sum_t share_t sum_s nu(s) V_t(s) = c_e
Markets: sum mu (h + k) = N clears w; sum mu m = M clears theta or p.
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
    """Statutory foreign-worker cap by Korean insured workers (eps.go.kr, 2024,
    manufacturing)."""
    n = np.asarray(n, float)
    return np.select(
        [n <= 10, n <= 50, n <= 100, n <= 150, n <= 200, n <= 300],
        [n + 10, np.minimum(30, 2 * n), 35, 40, 50, 60],
        default=80,
    )


class EPSModel:
    def __init__(self, types, alpha=0.69, rho=0.5, beta=0.96, ce=2.6, cm=0.5,
                 delta=0.0235, psi=0.0, xi=0.5, phi=1.0, sig_e=0.3, rho_s=0.9, sigma_s=0.2, ns=40,
                 nu_top=0.68, N=1.0, M=0.0, cap=cap_2024, h_max=6000, l_max=4000):
        """types: list of dicts with keys lam, cf, share (shares sum to 1)."""
        if not (-3 < rho < 1) or abs(rho) < 1e-3:
            raise ValueError("rho must be in (-3, 1) and not 0")
        self.a, self.r, self.beta, self.ce, self.cm = alpha, rho, beta, ce, cm
        self.delta, self.psi, self.xi, self.phi, self.sig_e = delta, psi, xi, phi, sig_e
        self.N, self.M, self.cap = N, M, cap
        self.s, self.P = tauchen(rho_s, sigma_s, ns)
        wts = np.zeros(ns)
        k = int(nu_top * ns)
        wts[:k] = norm.pdf(np.linspace(-2, 2, k))
        self.nu = wts / wts.sum()
        self.hg = np.concatenate([[0.0], np.geomspace(0.25, h_max, 240)])
        self.lg = np.concatenate([[0.0], np.geomspace(0.05, l_max, 190)])
        hh, ll = np.meshgrid(self.hg, self.lg, indexing="ij")
        self.hh, self.ll = hh, ll
        tot = sum(t["share"] for t in types)
        self.types = []
        for t in types:
            with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
                if rho > 0:
                    f = (hh ** rho + t["lam"] * ll ** rho) ** (alpha / rho)
                else:  # complements: both tasks needed
                    f = np.where((hh > 0) & (ll > 0), (hh ** rho + t["lam"] * ll ** rho) ** (alpha / rho), 0.0)
            f[~np.isfinite(f)] = 0.0
            self.types.append(dict(lam=t["lam"], cf=t["cf"], share=t["share"] / tot, f=f))
        self.prem = psi * (1 + self.hg) ** (-xi)                    # Korean manual premium by h
        self.capv = cap(self.hg)

    # ---- static problem ------------------------------------------------
    def _plan(self, w, x, regime, m_limit=None):
        """Cost-minimizing split of manual work on the (h, l) grid. x = theta
        (current rule) or permit price p (neutral). Returns cost, m, k, resource cost."""
        hh, ll = self.hh, self.ll
        wk = (w * (1 + self.prem))[:, None] * np.ones_like(ll)      # Korean manual cost
        base = w * hh
        cost_no = base + wk * ll
        if regime == "none":
            return cost_no, np.zeros_like(ll), ll, (wk - w) * ll
        if regime == "current":
            elig = (hh >= 1) & (hh < 300)
            mcap = np.where(elig, x * self.capv[:, None], 0.0) * np.ones_like(ll)
            wm = self.phi * w
        else:
            mcap = np.where(hh >= 1, np.inf, 0.0) * np.ones_like(ll)
            wm = self.phi * w + x
        if m_limit is not None:
            mcap = np.minimum(mcap, m_limit)
        m_ = np.minimum(ll, mcap)
        m_ = np.where((m_ > 0) & (wm < wk), m_, 0.0)
        cost_use = base + wm * m_ + wk * (ll - m_) + self.cm * (m_ > 0)
        better = cost_use < cost_no
        cost = np.where(better, cost_use, cost_no)
        m = np.where(better, m_, 0.0)
        k = ll - m
        return cost, m, k, (wk - w) * k + self.cm * (m > 0)

    def static(self, t, w, x, regime, m_limit_by_s=None):
        T = self.types[t]
        ns = len(self.s)
        pi, h, k, m, y, rc = (np.zeros(ns) for _ in range(6))
        if m_limit_by_s is None:
            plan = self._plan(w, x, regime)
        for i, si in enumerate(self.s):
            if m_limit_by_s is not None:
                plan = self._plan(w, x, regime, m_limit=m_limit_by_s[i])
            cost, M_, K_, RC = plan
            val = si * T["f"] - cost
            j = np.unravel_index(np.argmax(val), val.shape)
            pi[i], h[i], m[i], k[i], y[i], rc[i] = val[j], self.hh[j], M_[j], K_[j], si * T["f"][j], RC[j]
        return pi - T["cf"], h, k, m, y, rc

    # ---- dynamic problem -----------------------------------------------
    def _bellman(self, pi, V):
        c = self.beta * (1 - self.delta) * self.P @ V
        return pi + self.sig_e * np.logaddexp(0.0, c / self.sig_e), c

    def values(self, pi):
        """Returns V and the probability of staying, P(stay|s) = logistic(c/sig_e)."""
        V = np.maximum(pi, 0)
        for _ in range(6000):
            Vn, c = self._bellman(pi, V)
            if np.max(np.abs(Vn - V)) < 1e-9:
                break
            V = Vn
        c = self.beta * (1 - self.delta) * self.P @ Vn
        return Vn, 1.0 / (1.0 + np.exp(-c / self.sig_e))

    def stationary(self, pstay):
        A = np.eye(len(self.s)) - (1 - self.delta) * self.P.T * pstay[None, :]
        return np.linalg.solve(A, self.nu)

    def solve_given_x(self, x, regime):
        lo, hi = 1e-3, 50.0
        for _ in range(60):                           # free entry pins w
            w = np.sqrt(lo * hi)
            blocks = []
            ve = 0.0
            for t, T in enumerate(self.types):
                pi, h, k, m, y, rc = self.static(t, w, x, regime)
                V, stay = self.values(pi)
                ve += T["share"] * (self.nu @ V)
                blocks.append(dict(pi=pi, h=h, k=k, m=m, y=y, rc=rc, V=V, stay=stay))
            if ve > self.ce:
                lo = w
            else:
                hi = w
            if hi / lo < 1 + 1e-7:
                break
        kor = 0.0
        for t, B in enumerate(blocks):
            B["mu1"] = self.types[t]["share"] * self.stationary(B["stay"])
            kor += B["mu1"] @ (B["h"] + B["k"])
        Me = self.N / max(kor, 1e-300)                # Korean labor market clears
        for B in blocks:
            B["mu"] = Me * B["mu1"]
        return dict(w=w, x=x, Me=Me, blocks=blocks)

    def _eps_use(self, out):
        return sum(B["mu"] @ B["m"] for B in out["blocks"])

    def solve(self, regime):
        if regime == "none" or self.M == 0:
            out = self.solve_given_x(0.0, "none")
        elif regime == "current":                     # theta rations by quantity
            out = self.solve_given_x(1.0, regime)
            if self._eps_use(out) > self.M:
                lo, hi = 0.0, 1.0
                for _ in range(40):
                    th = 0.5 * (lo + hi)
                    out = self.solve_given_x(th, regime)
                    if self._eps_use(out) > self.M:
                        hi = th
                    else:
                        lo = th
                    if hi - lo < 1e-5:
                        break
        else:                                         # permit price p clears the quota
            out = self.solve_given_x(0.0, regime)
            if self._eps_use(out) > self.M:
                lo, hi = 0.0, 1.0
                while hi < 1e4 and self._eps_use(self.solve_given_x(hi, regime)) > self.M:
                    lo, hi = hi, hi * 4
                for _ in range(45):
                    p = 0.5 * (lo + hi)
                    out = self.solve_given_x(p, regime)
                    if self._eps_use(out) > self.M:
                        lo = p
                    else:
                        hi = p
                    if hi - lo < 1e-6 * max(hi, 1e-3):
                        break
        res = self.summarize(out, regime)
        res["eq_error"] = abs(res["eps_total"] - self.M) / self.M if (regime != "none" and self.M > 0) else 0.0
        return res

    def summarize(self, out, regime):
        cat = lambda key: np.concatenate([B[key] for B in out["blocks"]])
        mu, h, k, m, y, rc = cat("mu"), cat("h"), cat("k"), cat("m"), cat("y"), cat("rc")
        n = h + k
        firms = mu.sum()
        L = mu @ (n + m)
        exits = endo = cf_total = 0.0
        for t, B in enumerate(out["blocks"]):
            p = B["stay"]                              # P(stay | s)
            exits += B["mu"] @ (1 - (1 - self.delta) * p)
            endo += B["mu"] @ ((1 - self.delta) * (1 - p))
            cf_total += self.types[t]["cf"] * B["mu"].sum()
        users = m > 0
        type_share = [B["mu"].sum() / firms for B in out["blocks"]]
        return dict(
            regime=regime, Y=mu @ y, net_Y=mu @ (y - rc) - cf_total - self.ce * out["Me"],
            firms=firms, avg_size=L / firms, share_small=mu[(n + m) < 5].sum() / firms,
            exit_rate=exits / firms, endo_exit_share=endo / exits if exits > 0 else 0.0,
            users=mu[users].sum() / firms,
            eps_share_users=(mu[users] @ m[users]) / (mu[users] @ (n[users] + m[users])) if users.any() else 0.0,
            users_size=(mu[users] @ (n[users] + m[users])) / mu[users].sum() if users.any() else 0.0,
            eps_total=mu @ m, eps_share=(mu @ m) / L, type_share=type_share,
            w=out["w"], x=out["x"], Me=out["Me"], out=out,
        )

    # ---- Lee-Peri-Yang experiment ----------------------------------------
    def closure_response(self, res, kappa=0.2, periods=2):
        """Plants learn that EPS inflows stop: each plant's EPS workers are cut by
        kappa for the next `periods` years, at fixed prices; plants re-optimize
        (Korean manual labor at the premium, or less manual work). The extra
        closure probability is P(exit | shock) - P(exit | no shock), smooth because
        of the logit exit shock. Returns the mu-weighted OLS slope of extra closure
        on the plant's EPS share (Lee-Peri-Yang: 0.124-0.177 from zero to full)."""
        out = res["out"]
        disc = self.beta * (1 - self.delta)
        E, C, W, I, U = [], [], [], [], []
        users_close = users_mass = 0.0
        for t, B in enumerate(out["blocks"]):
            pi_sh, *_ = self.static(t, out["w"], out["x"], "current",
                                    m_limit_by_s=(1 - kappa) * B["m"] + 1e-12)
            Vsh = B["V"]
            for _ in range(periods):
                Vsh, _ = self._bellman(pi_sh, Vsh)
            p_sh = 1.0 / (1.0 + np.exp(-(disc * self.P @ Vsh) / self.sig_e))
            extra = (1 - self.delta) * (B["stay"] - p_sh)
            n0 = B["h"] + B["k"]
            e = np.where(n0 + B["m"] > 0, B["m"] / np.maximum(n0 + B["m"], 1e-12), 0.0)
            q = self.cap(n0) * ((B["h"] >= 1) & (B["h"] < 300))      # statutory cap
            imp = np.where(n0 + q > 0, q / np.maximum(n0 + q, 1e-12), 0.0)   # imputed exposure (LPY)
            E.append(e); C.append(extra); W.append(B["mu"]); I.append(imp); U.append(B["m"] > 0)
            u = B["m"] > 0
            users_close += B["mu"][u] @ extra[u]
            users_mass += B["mu"][u].sum()
        e, c, wgt = np.concatenate(E), np.concatenate(C), np.concatenate(W)
        imp, u = np.concatenate(I), np.concatenate(U)

        def ols(x, y, w):
            X = np.column_stack([np.ones_like(x), x])
            return float(np.linalg.lstsq(X * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)[0][1])

        # slope:     all plants, actual EPS share (first measure; NOT comparable to LPY)
        # slope_lpy: EPS users only, statutory (imputed) exposure = Lee-Peri-Yang's design
        return dict(slope=ols(e, c, wgt),
                    slope_lpy=ols(imp[u], c[u], wgt[u]) if u.any() else 0.0,
                    extra_closure_users=float(users_close / users_mass) if users_mass else 0.0)
