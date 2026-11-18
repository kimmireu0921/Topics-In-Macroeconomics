"""
EPS model v8 (Nov 18, 2026): v5/v7 with random EPS eligibility and the legal cap on all Korean
workers, following Prof. Hur's Nov 17 feedback. Replaces the "theta" rule.

What changes from v5 (eps_model_v5.py):
  1. Eligibility is random. At entry each plant draws, independently of its type and productivity,
     whether it may hire EPS workers (probability e). The draw is permanent.
  2. An eligible plant may hire EPS workers up to its full legal cap:
         m <= q(n),   n = h + k = all Korean workers (the law counts insured Korean workers),
     and only if 1 <= h and n < 300 (manufacturing eligibility, fewer than 300 workers; Korean
     workers here). v5 used theta * q(h) for every plant, with theta = 0.21.
  3. The quota M is rationed by access, not by size: e is the share of entrants that are eligible
     and adjusts so total EPS use equals M (as theta did). This stands in for the points ranking and
     waiting lists: demand exceeds the quota, and which firm gets workers is partly luck.
  4. Korean and EPS manual workers are imperfect substitutes: manual work is
         l = (k^eta + m^eta)^(1/eta),   0 < eta < 1  (eta -> 1 is v5's l = k + m).
     With perfect substitutes an eligible plant always fills its whole cap (EPS workers are
     cheaper), so the model cannot match the survey: EPS firms use 62% of their cap on average.
     eta is set by that average. It also removes the corner where a large plant swaps all its
     Korean manual workers for EPS workers when limits are lifted.
  Everything else is as in v5: two plant types (light, manual-intensive), Pareto productivity tail,
  AR(1) shocks, Korean manual premium w * psi * (1 + h)^(-xi), fixed cost c_m of using EPS, free
  entry, logit exit shock, Korean labour N = 1.

Regimes (x is the variable that clears the quota):
  "none"     no EPS at all
  "current"  random eligibility + legal cap q(h + k); x = e, the eligible share of entrants
  "neutral"  tradable permits: every plant with h >= 1 may buy any number at price x; no cap
  "flat"     the same eligible plants as the baseline (share e0), the size-linked cap replaced by one
             limit x for every eligible plant (n < 300 kept); x clears the quota

Choice set: the (h, l) grid of v5 plus, for every h, the points where all Korean workers n sit just
past each cap step (or just under 300) with m at the cap, so plants can bunch at the steps of n.
For each grid point the largest feasible m given the cap is computed once (it does not depend on
prices); since an EPS worker costs less than a Korean manual worker, a plant that uses EPS uses
that much.
"""
import numpy as np
from scipy.optimize import brentq

from eps_model import cap_2024
from eps_model_v5 import EPSModelV5

N_STEPS = (5, 10, 30, 50, 100, 150, 200)          # cap steps in Korean workers, 2019 and 2024 rules
ELIG_MAX = 300.0


def k_of(m, L, eta):
    """Korean manual workers needed, with m EPS workers, for manual work L."""
    if eta >= 0.999:
        return np.maximum(L - m, 0.0)
    return np.maximum(L ** eta - np.minimum(m, L) ** eta, 0.0) ** (1 / eta)


def m_of(k, L, eta):
    """EPS workers needed, with k Korean manual workers, for manual work L (k <= L)."""
    if eta >= 0.999:
        return np.maximum(L - k, 0.0)
    return np.maximum(L ** eta - np.minimum(k, L) ** eta, 0.0) ** (1 / eta)


def compose(k, m, eta):
    if eta >= 0.999:
        return k + m
    return (k ** eta + m ** eta) ** (1 / eta)


def max_m(H, L, capfun, eta=1.0, iters=60):
    """Largest m in [0, L] with m <= capfun(n), n = H + k(m) Korean workers, H >= 1 and n < 300.
    capfun is nondecreasing in n below 300 and k(m) falls in m, so g(m) = capfun(n) - m falls in m."""
    room = ELIG_MAX * (1 - 1e-12) - H
    lo = np.where(room > 0, m_of(np.maximum(room, 0.0), L, eta), np.inf)
    lo = np.where(H + L < ELIG_MAX * (1 - 1e-12), 0.0, lo)      # n < 300 already with m = 0
    lo = np.minimum(lo, L + 1)
    g = lambda m: capfun(H + k_of(m, L, eta)) - m
    ok = (H >= 1) & (lo <= L) & (g(lo) >= 0)
    full = ok & (g(L) >= 0)
    a, b = lo.copy(), L.copy()
    for _ in range(iters):
        c = 0.5 * (a + b)
        good = g(c) >= 0
        a = np.where(good, c, a)
        b = np.where(good, b, c)
    return np.where(full, L, np.where(ok, a, 0.0))


class EPSModelV8(EPSModelV5):
    def __init__(self, types, e0=None, eta=1.0, **kw):
        super().__init__(types, **kw)
        self.e0, self.eta = e0, eta                                     # baseline eligible share, for "flat"
        H0, L0 = self.hh.ravel(), self.ll.ravel()
        extra_H, extra_L = [], []
        targets = [t * (1 + 1e-6) for t in N_STEPS] + [ELIG_MAX * (1 - 1e-6)]
        hs = self.hg[self.hg >= 1]
        for nt in targets:
            mq = float(self.cap(np.array([nt]))[0])
            h = hs[hs < nt]
            extra_H.append(h)
            extra_L.append(compose(nt - h, mq, eta))    # k = nt - h Korean manual, m = cap
        self.H = np.concatenate([H0] + extra_H)
        self.Lab = np.concatenate([L0] + extra_L)
        self.n_mesh = len(H0)
        a, r = self.a, self.r
        for T in self.types:
            with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
                f = (self.H ** r + T["lam"] * self.Lab ** r) ** (a / r)
            f[~np.isfinite(f)] = 0.0
            T["fr"] = f
        self.premH = self.psi * (1 + self.H) ** (-self.xi)
        self.mbar = max_m(self.H, self.Lab, lambda n: self.cap(n), eta)
        self._flat_cache = {}
        # blocks: (type, eligible)
        self.blocks_def = [(t, el) for t in range(len(self.types)) for el in (True, False)]

    # ---- static -----------------------------------------------------------
    def _mcap(self, regime, x, eligible):
        if regime == "none" or (regime in ("current", "flat") and not eligible):
            return None
        if regime == "current":
            return self.mbar
        if regime == "flat":
            key = round(float(x), 12)
            if key not in self._flat_cache:
                if len(self._flat_cache) > 64:
                    self._flat_cache.clear()
                self._flat_cache[key] = max_m(self.H, self.Lab, lambda n: np.full_like(n, x), self.eta)
            return self._flat_cache[key]
        return np.where(self.H >= 1, self.Lab, 0.0)     # neutral: no cap

    def plan(self, w, x, regime, eligible, m_limit=None):
        """Cost, m, k and resource cost at every candidate point. Given manual work l, the
        cost-minimizing split has m / k = (wk / wm)^sigma, sigma = 1 / (1 - eta); the cap binds
        if that m is above the largest feasible m."""
        wk = w * (1 + self.premH)
        cost_no = w * self.H + wk * self.Lab
        mc = self._mcap(regime, x, eligible)
        if mc is None:
            return cost_no, np.zeros_like(cost_no), self.Lab.copy(), (wk - w) * self.Lab
        wm = self.phi * w + (x if regime == "neutral" else 0.0)
        eta = self.eta
        if eta >= 0.999:
            m_star = np.where(wm < wk, self.Lab, 0.0)
        else:
            r = (wm / wk) ** (eta / (1 - eta))
            m_star = self.Lab * (1 + r) ** (-1 / eta)
        m_ = np.minimum(m_star, mc)
        if m_limit is not None:
            m_ = np.minimum(m_, m_limit)
        k_ = k_of(m_, self.Lab, eta)
        cost_use = w * self.H + wm * m_ + wk * k_ + self.cm * (m_ > 0)
        better = (m_ > 0) & (cost_use < cost_no)
        m = np.where(better, m_, 0.0)
        k = np.where(better, k_, self.Lab)
        return np.where(better, cost_use, cost_no), m, k, (wk - w) * k + self.cm * (m > 0)

    def static_block(self, b, w, x, regime, m_limit_by_s=None):
        t, el = self.blocks_def[b]
        T = self.types[t]
        if m_limit_by_s is None:
            cost, M_, K_, RC = self.plan(w, x, regime, el)
            o = np.argsort(cost, kind="stable")
            fo = T["fr"][o]
            best_before = np.concatenate([[-np.inf], np.maximum.accumulate(fo)[:-1]])
            cand = o[fo > best_before]
            val = self.s[:, None] * T["fr"][cand][None, :] - cost[cand][None, :]
            j = cand[val.argmax(1)]
            pi = val.max(1)
        else:
            ns = len(self.s)
            j = np.zeros(ns, int)
            pi = np.zeros(ns)
            K_, M_, RC = (np.zeros(ns) for _ in range(3))
            for i in range(ns):
                cost, m_i, k_i, rc_i = self.plan(w, x, regime, el, m_limit=m_limit_by_s[i])
                v = self.s[i] * T["fr"] - cost
                jj = int(v.argmax())
                j[i], pi[i], M_[i], K_[i], RC[i] = jj, v[jj], m_i[jj], k_i[jj], rc_i[jj]
            return pi - T["cf"], self.H[j], K_, M_, self.s * T["fr"][j], RC
        return pi - T["cf"], self.H[j], K_[j], M_[j], self.s * T["fr"][j], RC[j]

    def block_share(self, b, regime, x):
        t, el = self.blocks_def[b]
        sh = self.types[t]["share"]
        if regime == "current":
            e = x
        elif regime == "flat":
            e = self.e0
        else:
            e = 1.0 if el else 0.0                       # eligibility irrelevant: one block per type
        return sh * (e if el else 1 - e)

    # ---- equilibrium ----------------------------------------------------------
    def solve_given_x(self, x, regime):
        nb = len(self.blocks_def)
        shares = [self.block_share(b, regime, x) for b in range(nb)]
        live = [b for b in range(nb) if shares[b] > 0]

        def entry_value(logw):
            w = np.exp(logw)
            blocks, ve = {}, 0.0
            for b in live:
                pi, h, k, m, y, rc = self.static_block(b, w, x, regime)
                V, stay = self.values(pi)
                ve += shares[b] * (self.nu @ V)
                blocks[b] = dict(pi=pi, h=h, k=k, m=m, y=y, rc=rc, V=V, stay=stay)
            entry_value.last = (w, blocks)
            return ve - self.ce

        logw = brentq(entry_value, np.log(1e-3), np.log(50.0), xtol=1e-9)
        entry_value(logw)
        w, blocks = entry_value.last
        kor = 0.0
        out_blocks = []
        for b in live:
            B = blocks[b]
            t, el = self.blocks_def[b]
            B.update(block=b, type=t, eligible=el, share=shares[b])
            B["mu1"] = shares[b] * self.stationary(B["stay"])
            kor += B["mu1"] @ (B["h"] + B["k"])
            out_blocks.append(B)
        Me = self.N / max(kor, 1e-300)
        for B in out_blocks:
            B["mu"] = Me * B["mu1"]
        return dict(w=w, x=x, Me=Me, blocks=out_blocks, regime=regime)

    def solve(self, regime):
        cache = {}

        def excess(v):
            cache[v] = self.solve_given_x(v, regime)
            return self._eps_use(cache[v]) - self.M

        if regime == "none" or self.M == 0:
            out = self.solve_given_x(0.0, "none")
        elif regime == "current":                        # e clears the quota
            if excess(1.0) > 0:
                e = brentq(excess, 1e-4, 1.0, xtol=1e-6)
                out = cache.get(e) or self.solve_given_x(e, regime)
            else:
                out = cache[1.0]
        elif regime == "flat":                           # one limit L for every eligible plant
            lo, hi = 0.0, 1.0
            excess(lo)
            while hi < 2e4 and excess(hi) < 0:
                lo, hi = hi, hi * 2
            L = brentq(excess, lo, hi, xtol=1e-6)
            out = cache.get(L) or self.solve_given_x(L, regime)
        else:                                            # permit price p clears the quota
            if excess(0.0) > 0:
                lo, hi = 0.0, 1.0
                while hi < 1e4 and excess(hi) > 0:
                    lo, hi = hi, hi * 4
                p = brentq(excess, lo, hi, xtol=1e-7)
                out = cache.get(p) or self.solve_given_x(p, regime)
            else:
                out = cache[0.0]
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
        type_mass = np.zeros(len(self.types))
        elig_mass = 0.0
        for B in out["blocks"]:
            p = B["stay"]
            exits += B["mu"] @ (1 - (1 - self.delta) * p)
            endo += B["mu"] @ ((1 - self.delta) * (1 - p))
            cf_total += self.types[B["type"]]["cf"] * B["mu"].sum()
            type_mass[B["type"]] += B["mu"].sum()
            if B["eligible"]:
                elig_mass += B["mu"].sum()
        users = m > 0
        return dict(
            regime=regime, Y=mu @ y, net_Y=mu @ (y - rc) - cf_total - self.ce * out["Me"],
            firms=firms, avg_size=L / firms, share_small=mu[(n + m) < 5].sum() / firms,
            share_50plus=mu[(n + m) >= 50].sum() / firms,
            exit_rate=exits / firms, endo_exit_share=endo / exits if exits > 0 else 0.0,
            users=mu[users].sum() / firms,
            eps_share_users=(mu[users] @ (m[users] / (n[users] + m[users]))) / mu[users].sum() if users.any() else 0.0,
            users_size=(mu[users] @ (n[users] + m[users])) / mu[users].sum() if users.any() else 0.0,
            eps_total=mu @ m, eps_share=(mu @ m) / L, type_share=list(type_mass / firms),
            elig_share_plants=elig_mass / firms,
            w=out["w"], x=out["x"], Me=out["Me"], out=out,
        )
