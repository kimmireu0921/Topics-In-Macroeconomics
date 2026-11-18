# Calibration targets and their sources

Checked Nov 10, 2026. Every target now has a source. The v7 calibration (`run_v7.py`) uses
the new values; v6 (`run_v6.py`, the Nov 3 and Nov 10 slides) used the old ones.

| Target | v6 value | v7 value | Source |
|---|---|---|---|
| Average plant size (workers) | 7.5 | **8.14** | MDIS 전국사업체조사 2024, all 509,467 manufacturing plants. Masked headcounts imputed by digit band (`bunching/census_targets.py`). v6 used unmasked plants with at most 1,000 workers, which leaves out the largest plants. |
| Share of plants with 1–4 workers | 0.70 | **0.713** | Same file |
| Share of plants with 50+ workers | 0.021 | 0.021 | Same file (0.0210 imputed; 0.0213 unmasked) |
| Annual exit rate | 0.08 (assumed) | **0.066** | 국가데이터처, 2025년 기업생멸행정통계(잠정), released 2026-10-22, Table 4 (산업별 소멸기업 현황): manufacturing 소멸률 6.6% in 2024 (provisional), 6.8% in 2023. Counts enterprises, not plants. |
| Share of plants using EPS | 0.10 (no source) | **0.080** | 40,766 manufacturing workplaces employing E-9 workers at the end of 2024 (38,981 E-9 only + 1,785 E-9 and H-2), e-나라지표 1501 고용허가제 고용동향 (고용노동부, 한국고용정보원 EPS data), table 150106, over 509,467 census plants. A workplace (사업장) and a census plant (사업체) may not be the same unit. |
| EPS workers ÷ manufacturing workers (sets the quota M) | 0.055 (no source) | **0.0529** | 219,507 E-9 workers in manufacturing at the end of 2024, e-나라지표 1501, table 150107, over 4,147,204 manufacturing workers in the 2024 census (imputed as above) |
| Average EPS share at EPS firms | 0.369 | 0.369 | Lee, Peri and Yang (2026), Table 3, p. 14 (761 firms, Jan 2020) |
| Average size of EPS firms | 20.78 | 20.78 | Lee, Peri and Yang (2026), Table 3, p. 14 |
| Closure slope on exposure, with size controls | 0.152 | 0.152 | Lee, Peri and Yang (2026), Table 6, p. 23: columns 4 and 5, 0.154 and 0.150 |

Where the old values came from: the 5.5% and 10% were rough figures the AI assistant wrote into
the first model on Oct 15 ("~240k E-9 manufacturing workers / ~4.4m manufacturing workers" and
"~50k EPS manufacturing workplaces / ~510k plants") without looking them up. The 8% exit rate
was labelled an assumption.

Official series for reference (end of year, manufacturing, e-나라지표 1501):

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| E-9 workers | 164,145 | 199,269 | 219,507 | 226,619 |
| Workplaces employing E-9 (incl. E-9 and H-2) | 36,945 | 39,365 | 40,766 | 41,285 |

Parameters set without calibration: α = 0.6916, persistence of productivity 0.8975 (from the
first Hopenhayn calibration in `run_eps.py`'s `FIRM`), β = 0.96, exit taste-shock scale 0.1
(smoothing only).

## v8 (Nov 18, 2026): random eligibility and the full legal cap

`run_v8.py` (model `eps_model_v8.py`) uses the v7 targets above with two changes, after Prof. Hur's
Nov 17 feedback:

| Change | Value | Source / reason |
|---|---|---|
| New target: average share of the 2019 legal cap used by EPS firms | **0.624** | KDI–World Bank EPS survey 2019, 772 firms: EPS workers ÷ 2019 cap from listed Korean workers (`bunching/cap_use_hist.py`, `cap_use_hist.json`; median 0.60). The model computes it the same way, under the 2019 caps, for EPS users. |
| Closure slope (Lee, Peri and Yang, 0.152) moved from target to reported check | — | In v8 eligible plants keep their permits and are rarely near closing; the 16 best of 256 random parameter draws all gave a slope of 0.00–0.07, so targeting it only pulled the other targets off. It was already fragile in v6 (0.15 on the base grid, 0.05 on a finer one). |

The eligible share e is not a parameter: it clears the quota M (5.29%), as theta did in v5–v7.
Fixed as before: α = 0.6916, ρ_s = 0.8975, β = 0.96, σ_ε = 0.1, EPS worker cost = w. Perfect
substitutes between Korean and EPS manual workers are kept (the CES option in `eps_model_v8.py`,
`eta`, stays at 1).
