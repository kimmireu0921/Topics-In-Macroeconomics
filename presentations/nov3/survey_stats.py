import json, os, sys, numpy as np, pandas as pd
df = pd.read_stata(os.path.expanduser('~/EPS_data/eps.dta'), convert_categoricals=False)
kl, ks, m = df.korean.astype(float), df.q13_1b.astype(float), df.q13_1a.astype(float)
def cap(n): return np.select([n<=5,n<=10,n<=30,n<=50,n<=100,n<=150,n<=200],[5,7,10,12,15,20,25],30)
r = m/cap(kl); q9 = df.q9.astype(float)
o = dict(n=len(df), list_counts=[int((kl==k).sum()) for k in range(1,21)], survey_counts=[int((ks==k).sum()) for k in range(1,21)],
         use_mean=r.mean(), use_median=r.median(), below_half=(r<.5).mean(), at_or_above=(r>=1).mean(), want_more=(q9>0).mean(), want_mean=q9.mean(),
         want_more_below_half=(q9[r<.5]>0).mean(), want_more_at_cap=(q9[r==1]>0).mean(), total=(ks+m).mean(), eps=m.mean(), korean=ks.mean(), share=(m/(ks+m)).mean(),
         sd_share=(m/(ks+m)).std(), wage_ratio=(df.q13_3a+df.q21_2).mean()/df.q13_3b.mean(), prod=[df.q14_1.mean(),df.q14_2.mean(),df.q14_3.mean()], wage_eps=df.q13_3a.mean(), wage_kor=df.q13_3b.mean(), dorm=df.q21_2.mean(),
         size=[((ks+m>=a)&(ks+m<b)).mean() for a,b in [(0,10),(10,20),(20,50),(50,100),(100,200),(200,300)]])
print(json.dumps(o,indent=0))
json.dump(o, open(sys.argv[1],'w'))
