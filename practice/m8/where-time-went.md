# Where did the time go? Upstream change: issue #2 -> PR #563 -> release PR #566

Source: GitHub API for nanotaboada/python-samples-fastapi-restful (issue, PR, reviews, release PR); all times UTC.

| Timestamp | When (UTC) | Detail |
|---|---|---|
| Ticket opened | 2021-08-16 23:23 | issue #2 by nanotaboada |
| First commit | 2026-04-09 21:30 | 10 commits |
| PR opened | 2026-04-09 21:31 | PR #563 |
| First review | 2026-04-09 21:39 | review comment by coderabbitai[bot] |
| Merged | 2026-04-10 01:35 | PR #563 merged |
| Released | 2026-04-12 03:21 | release PR #566 merged (docs(changelog): release v2.1.1 Eriksson) |

| Stage | From -> to | Hours | Share |
|---|---|---|---|
| Waiting to start | Ticket opened -> first commit | 40726.1 | 100% |
| Coding | First commit -> PR opened | 0.0 | 0% |
| Waiting for review | PR opened -> first review | 0.1 | 0% |
| Review and fixes | First review -> merged | 3.9 | 0% |
| Waiting to release | Merged -> released | 49.8 | 0% |
| **Total** | | **40780.0** | **100%** |

If coding were twice as fast, this change would have shipped about 0.0% sooner (0.0 of 40780.0 hours).
Leaving out the backlog wait (ticket -> first commit), coding was 0% of the remaining 53.9 hours; twice-as-fast coding would save 0% of that.

## What the numbers mean
- The "Coding" row (0.0 h) is misleading: PR #563 was opened 1 minute after the first commit,
  so the main feature was written locally before any commit, and that time is not recorded
  anywhere. Measured coding time here is a lower bound, not the real figure.
- The first review was a bot (coderabbitai[bot], 8 minutes after the PR opened). The PR's
  10 commits ran from 21:30 to 22:51 UTC, including "address code review findings" (21:47)
  right after the bot review (21:39): about 1.4 h of fixes, then about 2.7 h with no commits
  before the merge at 01:35.
- The issue waited about 4.6 years in the backlog (opened 2021-08-16). Leaving that out, the
  remaining 53.9 hours were 92% waiting to release (49.8 h), 7% review and fixes (3.9 h),
  under 1% everything else.

## Takeaway
If coding were twice as fast, this change would have shipped about 0% sooner. The time went
to the backlog and to waiting for a release, not to writing code. Speeding up the agent would
not have moved this change; deciding to start it, and releasing it sooner, would.
