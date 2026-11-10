"""Calibration targets from the MDIS business census (전국사업체조사), manufacturing, one year.

Run from ~/MDIS_data (raw files stay outside the repository; only aggregates are printed):
  python3 census_targets.py 2024

Headcounts of small or very large plants are masked by digit count: '*' = 1-9 workers,
'**' = 10-99, '***' = 100-999, '****' = 1,000-9,999, '*****' = 10,000+. Masked plants are
counted, and given the mean (and the 1-4 / 50+ shares) of unmasked plants in the same band.
Layout for 2010-2024 except 2013-14: industry letter in column 9, total workers in column 13.
"""
import glob
import sys
import zipfile

import numpy as np
import pandas as pd

YEAR = sys.argv[1] if len(sys.argv) > 1 else "2024"
BANDS = {"*": (1, 9), "**": (10, 99), "***": (100, 999), "****": (1000, 9999), "*****": (10000, 10 ** 7)}

vals, masked = [], []
for z in sorted(glob.glob("연간자료_2026*_데이터.zip")):
    with zipfile.ZipFile(z) as zf:
        for name in zf.namelist():
            if not name.startswith(YEAR):
                continue
            for ch in pd.read_csv(zf.open(name), header=None, dtype=str, encoding="utf-8-sig", chunksize=500_000):
                s = ch[ch[9].str.strip() == "C"][13].str.strip()
                num = pd.to_numeric(s, errors="coerce")
                vals.append(num.dropna().to_numpy())
                masked.append(s[num.isna()].to_numpy())
v = np.concatenate(vals)
mk = pd.Series(np.concatenate(masked)).value_counts()

plants, workers, small, large = len(v) + int(mk.sum()), v.sum(), (v <= 4).sum(), (v >= 50).sum()
for code, (lo, hi) in BANDS.items():
    c, u = int(mk.get(code, 0)), v[(v >= lo) & (v <= hi)]
    if c:
        workers += c * u.mean()
        small += c * (u <= 4).mean()
        large += c * (u >= 50).mean()
print(f"{YEAR}: plants {plants:,}, masked {int(mk.sum()):,} {dict(mk)}")
print(f"workers {workers:,.0f} | average size {workers / plants:.2f} | share 1-4 workers {small / plants:.3f} | "
      f"share 50+ {large / plants:.4f}")
print(f"unmasked only: plants {len(v):,}, average {v.mean():.2f}, share 1-4 {(v <= 4).mean():.3f}, share 50+ {(v >= 50).mean():.4f}")
