# Module 5 extension: subagents and worktrees (ungraded)

## Research: direct vs subagent
| Approach | Main-session tokens | Total tokens | Context left | Time | Same findings? |
|---|---|---|---|---|---|
| Direct search | 20.4K | 20.4K (no subagent) | 98% | 1 min 13 s (incl. 2 approvals) | 3 hits: 2 functions + alembic.ini config |
| Subagent | 17K | not shown by Codex; 5h meter 90% -> 89% | 99% | 38 s | same 2 functions; omitted the config line |

## Parallel worktrees
| Change | Tokens | Wall-clock (agent) | My review time | Accepted? |
|---|---|---|---|---|
| GET /health/version | 24.4K | 1 min 21 s | ≤10 min (both reviews combined) | yes |
| GET /players/count | 35.2K | 1 min 25 s | ≤10 min (both reviews combined) | yes |

- Both sessions ran side by side and finished at 12:15: about 1.5 min of wall-clock
  instead of about 3 min one after the other. 5h meter 89% -> 86% for both.
- Merge conflict: no; both merges were clean. Both changes touched
  tests/test_main.py, but in different sections (health near the top, count at the end).
- Cost per accepted change: 59.6K tokens / 2 accepted = about 29.8K tokens.

## What I learned
- Two changes in the same test file still merged cleanly because they edited different sections; parallel work only pays off when the changes really are separate.
- Subagent: kept about 3.4K tokens (~17%) of search out of the main context. Small
  here because the search was small; worth more on bigger searches. Codex does not
  show the subagent's own tokens, so total cost is not visible per session.
- The direct run's extra time was mostly my two approval prompts, not the search.
- Both research runs agree: nothing in the app parses or validates date_of_birth.
- Parallel worktrees halved wall-clock time for two independent changes, but my
  review time does not shrink: I still read two diffs.
- The count agent placed /players/count above /players/{player_id} (skill's
  route-order step) and built an empty in-memory database via a dependency override
  for its "count is 0" test, without touching the shared test data. Worth checking
  how an agent creates special states like "empty database".
- A "trailing whitespace" flag from git diff --check disappeared with
  core.whitespace=cr-at-eol, so it was CRLF line endings on D:, not real whitespace.
