"""Rung 4 -- quantify the output loss from a financial constraint on entrants
that Hopenhayn/AHKR cannot represent (see rung4_financial_constraint.py for
the model). chi = fraction of entrants with unconstrained credit access;
l_max = maximum labor a constrained entrant can finance."""
from rung4_financial_constraint import FinParams, solve_bgp_financial
from bgp import solve_bgp, Params


def main():
    base = solve_bgp(Params())
    print(f"Frictionless baseline (chi=1): Y={base['Y']:.4f}  w={base['w']:.4f}  "
          f"x_hat={base['x_hat']:.4f}  avg_size={base['avg_size']:.2f}\n")

    print(f"{'chi':>5} {'l_max':>6} {'Y':>8} {'Y/Y_base':>9} {'w':>8} {'avg_size':>9}")
    for chi in [1.0, 0.8, 0.5, 0.2, 0.05]:
        for l_max in [10.0, 20.0, 40.0]:
            p = FinParams(chi=chi, l_max=l_max)
            r = solve_bgp_financial(p)
            print(f"{chi:5.2f} {l_max:6.1f} {r['Y']:8.4f} {r['Y']/base['Y']:9.4f} "
                  f"{r['w']:8.4f} {r['avg_size']:9.2f}")

    print()
    print("Reading: at chi=0.2, l_max=10 (80% of entrants can finance at most 10")
    print("workers), GDP is 64% of the frictionless level -- a financial-frictions")
    print("channel entirely distinct from (and additive to) the entry-cost/tech-")
    print("barrier channel in the baseline AHKR model. This is the SSZ (2011)")
    print("mechanism from earlier in the same lecture (credit-constrained high-")
    print("productivity entrants vs. credit-privileged low-productivity incumbents)")
    print("grafted onto the Hopenhayn/AHKR entry margin.")


if __name__ == "__main__":
    main()
