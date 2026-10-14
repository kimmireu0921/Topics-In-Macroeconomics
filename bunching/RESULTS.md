# Bunching check: EPS quotas vs. card-fee tiers

Prof. Hur's instruction: check which of the two policy thresholds shows clearer
bunching in the data, and pursue that idea.

**Result: neither shows clear bunching at its policy threshold.**

Data: Statistics Korea, MDIS public-use microdata — 소상공인실태조사
(survey-based 2018–2020; register-sampled 2020–2023) and 전국사업체조사 (2000–2024).
Raw files are kept outside the repository (`~/MDIS_data`) under MDIS terms of use;
only aggregate counts are reported here.

Method: Kleven–Waseem style. Counts in 1-unit bins, polynomial counterfactual with
dummies for round numbers (multiples of 10, 50, 100), excluded window at the
threshold, residual-bootstrap standard errors. `b` = excess firms in the window
relative to the counterfactual average bin.

## Card-fee tiers (sales in millions of won)

| Threshold | Register-sampled 2020–23 | Survey 2018–20 |
|---|---|---|
| ₩300m | b = 0.87 (se 3.58) | b = 3.74 (se 4.52) |
| ₩500m | b = 1.19 (se 2.06) | b = 0.40 (se 2.61) |
| ₩1bn | b = 20.7 (se 1.7)* | b = 27.1 (se 2.4)* |

\* Round-number heaping, not policy. Exactly ₩1bn: 875 firms vs. 325 at ₩900m and
181 at ₩1.1bn; excluding that value, just below (287) ≈ just above (269). ₩2bn,
which has no fee threshold, shows the same spike.

- Restaurants (KSIC 56) and retail (KSIC 47) separately: no bunching at ₩300m or
  ₩500m, but samples are small (111 and 216 firms in the window).
- 2019 reform test at ₩500m (notch shrank from about 2.05% vs 1.3% to 1.4% vs 1.3%):
  2018 b = −0.20 (se 2.96); 2019–20 b = 0.82 (se 2.42). No change.
- Placebos (₩250m, ₩400m, ₩700m): no positive excess.
- Caveats: sales are self-reported and heavily rounded (38–48% are multiples of
  ₩10m); samples, not the full population of merchants.

## EPS (manufacturing establishments, total workers)

| Threshold | Pre-EPS 2000–03 | Early EPS 2005–10 | Recent 2015–24 |
|---|---|---|---|
| Eligibility: below 300 (280–299) | b = 3.95 (se 2.74) | b = 4.15 (se 2.38) | b = 1.49 (se 1.31) |
| Cap step 10 (just above) | −1.61 (4.47) | −1.78 (2.74) | −1.62 (0.52) |
| Cap step 30 | 0.09 (0.33) | 0.02 (0.25) | −0.25 (0.20) |
| Cap step 50 | −0.35 (0.61) | −0.54 (0.55) | −0.54 (0.47) |
| Cap step 100 | −0.20 (0.96) | −0.35 (0.84) | −0.52 (0.64) |
| Cap step 150 | 0.73 (1.79) | 0.39 (1.20) | 0.16 (0.76) |
| Cap step 200 | 0.32 (1.70) | 0.57 (1.37) | −0.23 (0.66) |

- No excess appears at the cap steps after EPS began (2004).
- The small excess below 300 exists before EPS too, so it reflects other 300-worker
  rules (SME definition, labor law), not EPS.
- Big caveat: EPS caps count **insured Korean workers**, but the census counts all
  workers, including the foreign workers themselves. That blurs any bunching, so
  this null is weak evidence. The proper test needs employment-insurance records.
- About 13% of manufacturing headcounts are masked (`*`) in the public files.

## Scripts

- `bunching.py` — generic estimator (tested on simulated data: detects planted
  bunching, b = 4.96; placebo b = −0.26).
- `census_hist.py` — builds aggregate manufacturing size histograms from the
  census zips.
