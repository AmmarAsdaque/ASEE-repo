# Autonomy map: players API (me + Codex)

Context: solo course repo, fork of nanotaboada/python-samples-fastapi-restful. No production
deployment. Drafted with a chat assistant from my course logs; every rating and rung decided by me.
Ceiling rule: any Low -> rung 1 max; any Medium -> rung 2 max; all High -> rung 3;
all High and verified automatically -> rung 4. Rung 5 is out of scope.

| Stage | Safety | Reversible | Verifiable | Rung today | Rung allowed | Evidence for next rung | Lights-on gate |
|---|---|---|---|---|---|---|---|
| Requirements (specs/, a2/spec.md) | Medium | High | Low | 1 | 1 | None: intent stays human | I approve every spec and every acceptance criterion |
| Design decisions (docs/adr/) | Medium | Medium | Low | 0 | 1 | 3 agent-drafted ADRs pass my review checklist with no missed trade-off | Only I change an ADR's status |
| Plans (specs/*-plan.md, a2/plan.md) | High | High | Medium | 3 | 2 | The 4 plan checks from Module 3 catch every planted flaw in 5 sample plans | I commit the reviewed plan before any code |
| Coding: routine endpoints and validation | High | High | High (read by me) | 3 | 3 | 5-task eval: hidden tests pass 5/5 with "agent edited tests: no" across 2 setup changes, and CI runs pytest + the architecture sensor on every push | Changes to alembic/versions/, tests/player_fake.py or tests/test_architecture.py need my explicit approval |
| Tests (acceptance) | Medium | High | Medium | 2 | 2 | Not yet: tests are my check. Before any move: agent-drafted tests reach 90%+ mutation score in 3 tasks with no assertion I had to fix | I write or approve every acceptance test; the agent never edits existing assertions |
| Code review | Medium | High | Medium | 1 | 2 | An agent reviewer finds the planted flaw in 4 of 5 practice PRs | I approve every merge into course-work |
| Documentation (README, rest/, docstrings) | High | High | Medium | 1 | 2 | CI runs every README command and stays green for 4 weeks (would make Verifiable High) | None beyond my review |
| Database migrations and seed data (alembic/, tools/) | Low | Medium | Medium | 0 | 1 | An agent-written migration passes upgrade and downgrade on a copy of the DB 5 times | I write or approve every migration |
| Dependency updates (pyproject.toml, uv.lock) | Medium | High | Medium | 0 | 2 | Full suite + sensor green on 5 dependency-update PRs | I approve every new dependency (AGENTS.md rule) |
| Deploy / release (Docker image, CD workflow) | Low | Medium | Low | 0 | 1 | A tested rollback and health check in a drill | I trigger every release |

## What the map shows
- Four different rungs at once (0, 1, 2, 3): normal, because stages differ.
- Gap: plans run at rung 3 today (Codex writes, I correct), but Medium verifiability caps
  them at rung 2. Reading plans is my only check; the evidence above would justify the practice.
- Coding is the only stage at its rung-3 ceiling, earned with tests, the architecture sensor,
  mutation testing and a holdout. Rung 4 needs automated verification (CI) instead of my reading.
- Requirements, design, migrations and release stay at rung 0-1: intent, data and release are human.
- Exercise 8.1 shows why coding autonomy is not the lever: upstream PR #563 spent 92% of its
  active time waiting for a release and almost none measurably coding
  (practice/m8/where-time-went.md).
