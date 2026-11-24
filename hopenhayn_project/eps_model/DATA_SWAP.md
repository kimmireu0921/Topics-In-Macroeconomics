# Using the Ministry data (expected about Nov 30)

The v9 pipeline is set up so that new data changes numbers, not code.

1. **Put each number in `targets_v9.json`**: its value, source and status. Set `weight` to 1 to fit it, or 0 to report it as a check.
2. **Run `python3 make_all.py calib`.** This recalibrates (about 2 hours), runs every experiment and check, and redraws the figures.
3. Without `calib`, the same command keeps the current parameters and only updates checks and figures.

Every model moment is computed in `moments_v9.py`, in the same size bands as the request: Korean insured workers 1–5, 6–10, 11–30, 31–50, 51–100, 101–300, 301+.

## Request item → use in the model

| Item | What it is | Model moment (`moments_v9.book`) | Planned use |
|---|---|---|---|
| 1 | Insured workplaces by size | `by_band.*.plants` | Check the plant-size distribution (census already targeted) |
| 2 | E-9 workplaces and workers by size | `users`, `by_band.*.user_rate`, `by_band.*.eps_workers` | **Target**: users (replaces the e-나라지표 ratio). **Check**: users by size |
| 3 | Allowed workers; cap-use buckets (<50, 50–90, 90–<100, 100, >100%) by size | `cap_use_mean`, `at_or_above_cap`, `cap_use_buckets`, `by_band.*.cap_use_buckets` | **Target**: 2024 average cap use and the share at or above the cap, alongside the 2019 survey. Decides whether caps bind in 2024 |
| 4 | Applicants, allocations, waiting lists by round and size | `applicants`, `allocation_rate` | **Target**: allocation rate. Pins the access rate e separately from the manual-intensive share |
| 5 | Manufacturing quota, use, allocations by year and round | `eligible_share_entrants`; quota M | **Check** whether the quota binds. If arrivals fall far short of the quota, reconsider "quota fully used" |
| 6 | Caps, extra allowances, points table, new-hire limits | `cap_2024`, `cap_2019` in `eps_model.py` / `run_eps.py` | Correct the cap schedules if they differ |
| 7 | New and closed workplaces by E-9 status | `exit_users`, `exit_nonusers` | **Target or check**: exit of EPS users vs non-users. Can replace the closure slope |
| 8 | 2019 workplaces by E-9 share; closures by 2021 and 2023 | `slope_lpy` design | **Check**: closure by EPS exposure |
| 9 | Size transitions by E-9 status | (to add: transition matrix by band) | Check growth of users |
| 10 | Workplaces by share of KSCO 7, 8, 9 insured workers | `manual_share_buckets`, `manual_intensive_plants` | **Check**: the manual-intensive share. Model manual work = tasks EPS can do (mainly KSCO 8–9), so compare with care |
| 11 | Korean recruitment before application: openings, applicants, hires by size | (premium by band) | **Discipline the premium**: the unfilled share by size gives how fast it falls (ξ) |
| 12 | Monthly pay, Korean vs E-9, by size | `wage` | **Check**: Korean pay does not rise at small plants (premium is not pay); EPS cost ratio (φ = 1) |
| 13 | E-9 re-employment, workplace changes, departures | — | Context for permanent vs redrawn eligibility |
| 14 | Items 2–4 by industry, region, root industry | — | Robustness |

## Data already in hand that feeds the same slots

- **Survey 2019** (`bunching/`): cap-use histogram, EPS share by size, hiring shortfall by size (`premium_evidence.json`), EPS costs (Q21).
- **Ministry occupational labour force survey at establishments** (`PROJECT_LOG.md`, Nov 24): shortage rates by size in manufacturing.
