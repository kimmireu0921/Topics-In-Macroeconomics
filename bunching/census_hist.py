"""Aggregate manufacturing headcount histograms from MDIS 전국사업체조사 files (counts only).

Run from ~/MDIS_data: python3 census_hist.py agg_mfg_size_hist.csv
Layouts: 2000-2009 = 29 cols (industry letter col 3, total workers col 28);
2013-2014 = letter col 4, total col 27; other 2010-2024 = letter col 9, total col 13.
Manufacturing = D through 2005 (KSIC 8), C from 2006 (files recoded to KSIC 9+).
"""
import zipfile, glob, sys
import pandas as pd, numpy as np
out = []
for z in sorted(glob.glob('연간자료_2026*_데이터.zip')):
    with zipfile.ZipFile(z) as zf:
        for n in sorted(zf.namelist()):
            yr = int(n[:4])
            parts = []
            for ch in pd.read_csv(zf.open(n), header=None, dtype=str, encoding='utf-8-sig', chunksize=500_000):
                man = 'D' if yr <= 2005 else 'C'
                if ch.shape[1] == 29:     letter, tot = 3, 28
                elif yr in (2013, 2014):  letter, tot = 4, 27
                else:                     letter, tot = 9, 13
                m = ch[ch[letter].str.strip() == man][tot].str.strip()
                parts.append(m)
            s = pd.concat(parts)
            num = pd.to_numeric(s, errors='coerce')
            masked = s[num.isna()].value_counts().to_dict()
            h = num.dropna().astype(int).value_counts()
            h = h[h.index <= 1000]
            row = {'year': yr, 'n_mfg': len(s), 'masked_star3': masked.get('***', 0), 'masked_all': int(num.isna().sum())}
            row.update({f'n{k}': int(h.get(k, 0)) for k in range(1, 1001)})
            out.append(row)
            print(yr, 'mfg establishments', len(s), 'masked', row['masked_all'], '(*** =', row['masked_star3'], ')', flush=True)
pd.DataFrame(out).to_csv(sys.argv[1], index=False)
