"""One command for the whole v9 pipeline.

  python3 make_all.py            # check fit at current parameters, run all results, draw figures
  python3 make_all.py calib      # recalibrate first (about 2 hours), then the above

Steps: calibrate_v9.py (optional) -> calibrate_v9.py check -> results_v9.py -> presentations/dec8/figs_v9.py.
Edit targets_v9.json to change targets, their weights or which parameters are set externally.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
FIGS = os.path.join(HERE, "..", "..", "presentations", "dec8")


def run(args, cwd=HERE):
    print(">>", " ".join(args), flush=True)
    subprocess.run([PY] + args, cwd=cwd, check=True)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "calib":
        run(["calibrate_v9.py", "calib", "100", "150"])
    run(["calibrate_v9.py", "check"])
    run(["results_v9.py"])
    if os.path.exists(os.path.join(FIGS, "figs_v9.py")):
        run(["figs_v9.py"], cwd=FIGS)
    print("ALL DONE")
