| What I corrected | Home | Why |
|---|---|---|
| Ran tests through its own Python wrapper instead of `uv run pytest -q` | Instruction file (Commands) | True for every task |
| Never ran `uv run flake8 .` or `uv run black --check .` | Instruction file (Commands) | Every task must pass lint before "done" |
| Changed an existing test fixture (999 → 98) without asking | Instruction file (Boundaries) | "Never edit existing tests or fixtures to make them pass; ask first" applies to every task |
| Said "39 passed" although its last test run was interrupted | Instruction file (Done) | Every task: report the final command and its real output |
| Chose model-level validation returning 422 on its own | Instruction file (Conventions) | Where validation lives is true for all input rules |
| Searched folders above the repo for AGENTS.md | Instruction file (Boundaries) | Applies to every session |
| Edited docs and rest/players.rest when I only asked for code | Instruction file (Boundaries) | A scope rule for all tasks |
| Changed the order of an existing list response | Instruction file (Boundaries) | "Existing responses stay unchanged" applies everywhere |
| Left trailing whitespace; earlier runs rewrote whole files (line endings) | Tool or config (black, .gitattributes) | A formatter and git setting fix it reliably; text can't |
| Why tests are integration-only | Docs (link docs/adr/0007) | Background for humans; AGENTS.md just links it |
