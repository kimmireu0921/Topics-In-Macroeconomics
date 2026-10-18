# Topics in Macroeconomics (ISA6327), Fall 2026

Group project repository for ISA6327 Topics in Macroeconomics at Yonsei University (Prof. Sewon Hur).

**Team:** Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo

**Project:** *Who Gets the Guest Workers? Size-Dependent Allocation in Korea’s Employment Permit System and Manufacturing Productivity.*

**Start here: [`PROJECT_LOG.md`](PROJECT_LOG.md)** — day-by-day record of what we did, the results, and what they mean.

## How the project was built: climbing the course’s project ladder

The course’s “ladder of feasible projects” (Week 2, slide 60) goes from replicating a
lecture model, to recalibrating it to Korea, to running a policy experiment, to adding
a feature. Our work follows that path:

| Rung | What we did | Folder |
|---|---|---|
| 1. Replicate | Solved Hopenhayn (1992) and reproduced its exit patterns by plant size and age | `hopenhayn_project/rung1_hopenhayn/` |
| 2–3. Korea and policy | Worked through Asturias, Hur, Kehoe and Ruhl’s (2023) balanced growth path and a Korean entry-cost reform transition | `hopenhayn_project/ahkr_model/` |
| 4. Add a feature | Extended the Hopenhayn model with Korea’s Employment Permit System: Korean and guest workers, the size-based cap, a rationed national quota, and two plant types; calibrated to Korean manufacturing | `hopenhayn_project/eps_model/` |

Supporting evidence: `bunching/` tests the card-fee and EPS thresholds with MDIS
microdata (the card-fee idea was dropped after finding no bunching).

## Contents

| Folder | What it is |
|---|---|
| `proposal/` | Research proposal (due Oct 23): Markdown source and PDF. |
| `hopenhayn_project/eps_model/` | Our project model: calibration, experiments, results (`NOTES.md`). |
| `hopenhayn_project/` | The ladder exercises (rungs 1–4) that preceded the EPS model. See its own README. |
| `bunching/` | Bunching tests (MDIS microdata; aggregate results only, in `RESULTS.md`). |
| `course_exercises/aiyagari_replication/` | Replication of Table 2 in Aiyagari (1994), a Week 3 exercise; not part of the EPS project. |

Not included: lecture slides, the syllabus and handouts (the instructor’s materials), and
the MDIS microdata (licensed; see `PROJECT_LOG.md` for where it is stored).

## Running the code

Requires Python 3 with NumPy and SciPy:

```
pip install -r course_exercises/aiyagari_replication/requirements.txt
python3 hopenhayn_project/rung1_hopenhayn/run_rung1.py
python3 hopenhayn_project/ahkr_model/run_rung2_3.py
python3 hopenhayn_project/ahkr_model/run_rung4.py
cd hopenhayn_project/eps_model && python3 run_eps.py eps_results_recal.json recal 150   # ~1.5 h
```

## AI use

Following the course policy, we disclose that code, literature search and drafting in this repository were assisted by Claude (Anthropic). The team is responsible for all content.
