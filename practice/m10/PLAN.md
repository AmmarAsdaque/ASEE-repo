# My measurement plan (Nov–Dec 2026)

Question: On the players API, does delegating small features to Codex get them merged
faster without more of them coming back?

Measures (per task)
- minutes from starting the agent session to merge (from session and commit times)
- agent: none / assisted / delegated
- review rounds before merge (plan corrections count as one round)
- came back within 14 days? (bug, revert or fix commit) -> my personal change failure rate

Not measured: lines of code, number of commits or PRs, how fast it felt.

Period: 4 weeks, every task that ends in a merge into course-work.
Decision rule: if delegated tasks come back more than twice as often as none/assisted ones,
I add a sensor or a failure-pattern line before delegating more of that kind of task.

Growth goal this quarter: specification. I write numbered acceptance criteria for every
feature, even small ones, and note in the log whether the shipped change matched them.
