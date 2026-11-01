# Module 7 harness retrospective

## Where the agent struggled or I corrected it
| # | Where | What happened | Repeat? | Fix |
|---|---|---|---|---|
| 1 | runs/setup-test.md; runs/a1-task1-without.md; runs/a1-task2-without.md | Ran tests through its own Python wrapper instead of `uv run pytest -q` | 3x | AGENTS.md (done in A1; with-runs used uv run pytest) |
| 2 | runs/a1-task1-without.md; runs/a1-task2-without.md | Created new test files instead of tests/test_main.py | 2x | AGENTS.md + add-endpoint skill (done) |
| 3 | runs/a1-task1-without.md; runs/a1-task2-without.md | Edited README / rest/ / docs unasked | 2x | AGENTS.md boundary (done) |
| 4 | runs/a1-task1-without.md; runs/a1-task2-without.md | Searched folders above the repo for AGENTS.md | 2x | AGENTS.md boundary (done) |
| 5 | runs/setup-test.md; runs/a1-task1-without.md | Reported "all tests pass" from an interrupted run | 2x | AGENTS.md (done) |
| 6 | runs/a1-task2-without.md | Invented a "Defenders" grouping absent from the data | 1x | AGENTS.md boundary (done; it asked in task2-with) |
| 7 | specs/players-pagination-plan.md, step 4 correction | Planned to edit POST/PUT/DELETE to clear page caches instead of using the "players" key prefix | 1x | skill candidate (cache keys) |
| 8 | runs/m5-players-pagination.md, my correction to step 4 | AC8 test created a player with no guaranteed cleanup (no finally) | 1x (same risk designed around in A2 tests) | skill candidate (integration tests that write data) |
| 9 | runs/m5-players-pagination.md, my correction to step 2 | Planned a new Pydantic model for query params, outside the allowed files | 1x | AGENTS.md conflict (see below) |
| 10 | runs/a1-task2-with.md; runs/m6-eval-T3.md; m5 count session | `git diff --check` reported "trailing whitespace" that was CRLF line endings | 3x | design/tool change: .gitattributes |
| 11 | runs/a2-implement.md; runs/m5-players-pagination.md; runs/m6-eval-T3.md | First test run fails on uv's read-only cache in the sandbox, then reruns | 3x+ | tool config / AGENTS.md wording |
| 12 | a2/plan.md, baseline + correction | black flagged tests/test_main.py although pyproject.toml tries to exclude it (the exclude pattern never matches) | 1x | design change: fix or delete the exclude line |
| 13 | practice/m6/notes.md | Agent tests for generate_async_session mocked internals; a module-level hand mutant survived | 1x | skill candidate (test style) |

## Capstone skill candidate
Integration tests that write data must clean up in `finally` and never depend on shared
rows (from #8, recorded in runs/m5-players-pagination.md; same rule used in the A2 tests).

## Conflicts and drift found in AGENTS.md
- Conflict: "Input validation lives in the Pydantic models" vs query parameters validated
  with FastAPI Query() (#9).
- Drift: cache line mentions only the key "players"; page keys "players:page=N:size=M" now exist.
- Drift: "Tests hang at the first HTTP request" is not what happens; the uv cache is
  read-only in the sandbox (#11).
- Drift: "Trailing whitespace left behind" is usually CRLF, not whitespace (#10).
