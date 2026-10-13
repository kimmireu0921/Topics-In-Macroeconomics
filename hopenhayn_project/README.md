# The Ladder of Feasible Projects (lecture_week02.pdf, slide 60)

Sewon Hur's four rungs, built on the Hopenhayn (1992) / Asturias-Hur-Kehoe-Ruhl
(2023, AEJ:Macro) machinery from Weeks 2-3 of Topics in Macroeconomics.

## Rung 1 -- Replicate (`rung1_hopenhayn/`)

Plain Hopenhayn (1992): endogenous exit cutoff, free entry, stationary
distribution solved as one linear system (slides 13-19). Technology
parameters (alpha, beta, cf, ce) reused from AHKR's own US calibration for
consistency across rungs; the AR(1) shock process (rho, sigma) has no
numerical value anywhere in the lecture material, so it's an illustrative
choice, documented in the code.

Run: `python3 rung1_hopenhayn/run_rung1.py`

**Result**: exit rate falls sharply with size (30% -> 0% across deciles) and
age (67% -> 4%), matching BDS's qualitative pattern (slide 5-8) and getting
the share of firms with <5 employees right (58% vs. BDS's ~60%). It
under-generates the fat right tail (top-1% employment share 3.7% vs. BDS's
~30%) -- an honest limitation, and exactly why AHKR use a Pareto entrant
distribution instead of a persistent AR(1) alone.

## The AHKR (2023) engine (`ahkr_model/bgp.py`)

Solves the balanced growth path by detrending (x~ = x/g_e^t): a firm's
efficiency relative to the frontier shrinks deterministically every period
(gc < ge), so the exit decision collapses to a *static* zero-profit cutoff
(Proposition 1 in the paper) -- no value function iteration needed, just
direct summation over each firm's deterministic lifetime and Pareto
quadrature for the entry-margin expectation.

**Validated** against the paper's own Table 4 (US calibration): entry-cost /
continuation-cost ratio 0.826 vs. their 0.82; real interest rate 4.08% vs.
4%; average plant size 16.9 vs. 14.0; FHK entry contribution 20.9% vs. 25%.
The size-*dispersion* target (SD=89.0) doesn't match (model gives 15.6) --
flagged rather than hidden; likely a difference in how that specific moment
was constructed in the paper's simulated panel vs. our closed-form BGP.

## Rungs 2 + 3 -- these are one exercise here (`ahkr_model/run_rung2_3.py`)

The paper's own closed form, FHK contribution = 1-(1-delta)(gc/ge)^gamma,
depends only on technology parameters common to every country on the same
BGP (slide 54's "same technology, different policy" design). So Korea's
empirically declining net-entry contribution -- 48.0% (1992-97) -> 37.3%
(2001-06) -> 25.1% (2009-14), AHKR's own Table 1 -- cannot be a different
Korean *steady state*. It has to be a **transition** (slide 52's point
exactly). We size a pre-reform entry-cost distortion (tau) so eliminating it
reproduces Korea's actual 6.1%/year growth in the first post-reform period,
then read off the model's predicted decay.

**Finding**: the model gets the *direction* right (growth and turnover spike,
then decay toward the common BGP) but compresses it into a single 5-year
period rather than the ~20-year decline Korea shows across three windows.
That gap is itself informative: AHKR's own Section 7.2 documents *two*
separate Korean reform waves (1990-95 and 1998-2004), not one. A single
one-shot MIT shock can't reproduce a multi-decade decay; a sequence of
reforms plausibly could. That's a real finding, not a bug -- though see the
simplifications below, which likely also make the model's own convergence
faster than it should be.

**Simplifications, stated up front (`transition.py` docstring)**: gc is held
fixed through the transition (no endogenous spillover feedback g_c,t =
gbar*g_t^epsilon off the BGP -- that needs the realized aggregate growth rate
as part of the fixed point, a materially harder problem); the wage path is
solved by exact backward induction on free entry (not an approximation, but
it does mean the labor market clears through the entrant margin alone,
which likely makes the reallocation happen faster than the true forward-
looking equilibrium would).

## Rung 4 -- Add a feature (`ahkr_model/rung4_financial_constraint.py`, `run_rung4.py`)

A financial constraint on entrants: fraction `chi` have unconstrained credit
access (chaebol-style), the rest can only finance up to `l_max` workers --
the Song-Storesletten-Zilibotti (2011) F-firm/E-firm story from earlier in
the same lecture, grafted onto the AHKR entry margin. Comparative statics on
the BGP (not the full transition, to keep scope bounded).

**Result**: at chi=0.2, l_max=10 (80% of entrants capped at 10 workers), GDP
is 64% of the frictionless level -- a channel entirely additive to, and
distinct from, the entry-cost/tech-barrier channel already in the model.

## How to run everything

```
python3 rung1_hopenhayn/run_rung1.py
python3 ahkr_model/run_rung2_3.py
python3 ahkr_model/run_rung4.py
```

## What would need to change for a submission

- Rung 1's (rho, sigma) should be targeted to something (even a rough BDS
  moment) rather than left illustrative.
- Rungs 2-3's transition would benefit from relaxing the "gc fixed" and
  "myopic-free-labor-clearing" simplifications -- likely via a proper
  perfect-foresight shooting algorithm over both the wage path *and* a
  time-varying gc,t, which is a substantially larger undertaking.
- Rung 4 is a BGP comparative static, not a transition; extending it to a
  transition (financial constraints loosening over time) would connect it
  back to Rung 3's reform story.
