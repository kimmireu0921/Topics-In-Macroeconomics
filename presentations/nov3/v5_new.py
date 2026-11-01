import json, sys, os
sys.path.insert(0, os.getcwd())
from run_v6 import moments, T
from run_v5 import NAMES
d = json.load(open('v5_best.json')); p = {k: d[k] for k in NAMES}
r = moments(p)
json.dump({k: float(r[k]) for k in T}, open(sys.argv[1], 'w'), indent=1)
print({k: round(float(r[k]), 3) for k in T}, 'loss', round(sum(((r[k]-v)/v)**2 for k,v in T.items()),4))
