# Topics in Macroeconomics (ISA6327), Fall 2026

Group project repository for ISA6327 Topics in Macroeconomics at Yonsei University (Prof. Sewon Hur).

**Team:** Sara Ambre Chekroune · Yitang Donny Chen · Mireu Kim · Julian Henry Raymundo · Zachary Benjamin Yoo

## Contents

| Folder | What it is |
|---|---|
| `hopenhayn_project/` | Hopenhayn (1992) and Asturias, Hur, Kehoe and Ruhl (2023) models, worked through the four rungs of the course's project ladder. See its own README. |
| `aiyagari_replication/` | Replication of Table 2 in Aiyagari (1994). |

Lecture slides and the syllabus are not included; they are the instructor's course materials.

## Running the code

Requires Python 3 with NumPy and SciPy:

```
pip install -r aiyagari_replication/requirements.txt
python3 aiyagari_replication/replicate_table2.py
python3 hopenhayn_project/rung1_hopenhayn/run_rung1.py
python3 hopenhayn_project/ahkr_model/run_rung2_3.py
python3 hopenhayn_project/ahkr_model/run_rung4.py
```

## AI use

Following the course policy, we disclose that code, literature search and drafting in this repository were assisted by Claude (Anthropic). The team is responsible for all content.
