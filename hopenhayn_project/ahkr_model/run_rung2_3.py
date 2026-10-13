"""
Rung 2 + 3 -- these turn out to be one exercise in this model (see README).

Rung 2 "recalibrate to Korea": the paper's own closed-form result,
FHK entry contribution = 1 - (1-delta)*(gc/ge)^gamma, depends only on
(delta, gc, ge, gamma) -- technology parameters the professor's slide 54
says should be held common across countries. So Korea's empirically much
higher (and declining) net-entry contribution -- 48.0% (1992-97), 37.3%
(2001-06), 25.1% (2009-14), from AHKR's own Table 1 -- cannot be a different
Korean BGP. It has to be a TRANSITION effect: Korea entered its fast-growth
episode from a more policy-distorted starting point (the paper documents
real entry-liberalizing and financial-system reforms in Korea in 1990-1995
and 1998-2004) and grew rapidly while converging back toward the same
common BGP the US is already on.

We size that pre-reform distortion (an entry-cost multiplier tau, holding
US technology fixed) so the model's own first-period growth rate after
eliminating it matches Korea's actual 1992-97 growth rate of 6.1%/year
(source: AHKR Table 1 / this same lecture's citation of Kehoe-Ruhl-style
national accounts). That IS Rung 3: reading off the transition this implies.
"""
import numpy as np
from dataclasses import replace
from bgp import Params, solve_bgp
from transition import run_transition

KOREA_GROWTH_1992_97 = 0.061  # AHKR (2023) Table 1, "Authors' calculations"


def calibrate_tau(target_growth=KOREA_GROWTH_1992_97, T_end_probe=3):
    p_new = Params()

    def g0(tau):
        p_old = replace(p_new, kappa=p_new.kappa * (1 + tau))
        bgp_old = solve_bgp(p_old)
        out = run_transition(p_old, p_new, T_end=T_end_probe)
        return (out["results"][0]["Y"] / bgp_old["Y"]) ** (1 / 5) - 1

    lo, hi = 0.01, 5.0
    for _ in range(30):
        mid = 0.5 * (lo + hi)
        f = g0(mid) - target_growth
        if abs(f) < 0.0015:
            break
        if f > 0:
            hi = mid
        else:
            lo = mid
    return mid, p_new


def main():
    tau_star, p_new = calibrate_tau()
    p_old = replace(p_new, kappa=p_new.kappa * (1 + tau_star))
    bgp_new = solve_bgp(p_new)
    bgp_old = solve_bgp(p_old)

    print(f"Calibrated tau (Korea's pre-reform entry-cost distortion): {tau_star:.3f}")
    print(f"  -> implied kappa_Korea = {p_old.kappa:.3f} vs kappa_US = {p_new.kappa:.3f}")
    print(f"  -> implied pre-reform income, relative to the common BGP: "
          f"{100*bgp_old['Y']/bgp_new['Y']:.1f}%")
    print(f"  -> pre-reform avg. plant size {bgp_old['avg_size']:.1f} vs. "
          f"post-reform {bgp_new['avg_size']:.1f} employees "
          f"(fewer, larger, protected incumbents pre-reform)")
    print()

    out = run_transition(p_old, p_new, T_end=12)
    print("Transition after eliminating the distortion at t=0 (each period = 5 years):")
    print(f"{'t':>3} {'Y growth/yr%':>13} {'entrant emp. share%':>20} {'exit mass share%':>18}")
    Y_prev = bgp_old["Y"]
    for r in out["results"][:8]:
        g = (r["Y"] / Y_prev) ** (1 / 5) - 1
        print(f"{r['t']:3d} {100*g:13.2f} {100*r['entrant_emp_share']:20.2f} {100*r['exit_mass_share']:18.2f}")
        Y_prev = r["Y"]

    print()
    print("Korea's actual data (AHKR 2023 Table 1), for comparison:")
    print("  1992-1997: GDP growth 6.1%/yr, net-entry contribution 48.0%")
    print("  2001-2006: GDP growth 4.3%/yr, net-entry contribution 37.3%")
    print("  2009-2014: GDP growth 3.0%/yr, net-entry contribution 25.1%")
    print()
    print("Finding: the model reproduces the *direction* (a growth/turnover spike that")
    print("decays toward the common BGP) but compresses it into a single ~5-year period,")
    print("not the ~20-year decline Korea shows across three windows. See README for why:")
    print("this points to Korea's growth coming from a SEQUENCE of reforms (AHKR's own")
    print("Section 7.2 documents separate 1990-95 and 1998-2004 reform waves), not the")
    print("single one-shot, instantaneous-relative-price-adjustment reform modeled here.")


if __name__ == "__main__":
    main()
