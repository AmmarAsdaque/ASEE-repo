# Five-task eval

Tasks: T1 pagination (start 99484fa), T2 health version (a5d8cc4), T3 players count (a5d8cc4),
T4 starting eleven (1c92d3f), T5 players by position (1c92d3f).
Hidden tests live outside the repo in ~/holdouts/evals/T1..T5/test_hidden.py.
Each hidden test is confirmed to fail at its start commit before the agent runs.

| Date | Setup change | Task | Hidden test passed | Agent edited tests | Interventions | Minutes |
|---|---|---|---|---|---|---|
| 2026-11-01 | baseline (AGENTS.md + add-endpoint skill) | T3 players count | yes | no | 0 | 3 |

## Run notes
- T3 baseline: 58,375 tokens (3,044 output). Tests first (3 failed -> 36 passed); route placed above
  /players/{player_id}. Touched 4 files incl. models/player_model.py (+6, response model).
  Log: runs/m6-eval-T3.md
