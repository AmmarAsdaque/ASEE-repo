# AGENTS.md

Players API: a FastAPI REST API for football players (Argentina 2022 squad).
Python 3.13, uv, async SQLAlchemy, SQLite, Alembic.

## Commands

- Install: `uv sync --all-groups`
- Create or upgrade the database: `uv run alembic upgrade head`
- Run all tests: `uv run pytest -q`
- Lint: `uv run flake8 .`
- Check formatting: `uv run black --check .` (fix with `uv run black .`)
- Run locally: `uv run uvicorn main:app --reload --port 9000`

Use these commands exactly; do not wrap pytest in your own Python script.
Before saying a task is done, run `uv run pytest -q`, `uv run flake8 .` and
`uv run black --check .` on the whole repo, and quote the final summary line of
each from the last run. Never report a result from an interrupted run.

## Project layout

- `main.py` creates the app and includes the routers
- `routes/player_route.py` HTTP layer; `routes/health_route.py` health check
- `services/player_service.py` all database queries (async SQLAlchemy)
- `models/player_model.py` Pydantic request and response models
- `schemas/player_schema.py` SQLAlchemy table model
- `databases/player_database.py` async engine and `generate_async_session`
- `alembic/versions/` migrations and seed data (26 players)
- `tests/test_main.py` integration tests; `tests/player_fake.py` test data;
  `tests/conftest.py` fixtures
- `docs/adr/` architecture decisions (background for humans)
- `specs/` specs for changes

## Conventions

- Routes stay thin and call a function in `services/player_service.py`;
  routes never build queries.
- Request-body validation lives in `models/player_model.py`; query and path
  limits use FastAPI `Query()`/`Path()` in the route. Invalid input returns 422.
- A missing single player returns 404 via HTTPException; an empty list returns
  200 with `[]`.
- Tests are integration-only and go in `tests/test_main.py`, named
  `test_request_<method>_<path>_<case>_response_<expectation>`, with
  Arrange/Act/Assert comments. Do not create new test files.
  Why: `docs/adr/0007-integration-only-test-strategy.md` (background only).
- `GET /players/` caches under keys that start with "players" (full list
  "players", pages "players:page=N:size=M"); writes clear them all with
  `simple_memory_cache.clear(CACHE_KEY)`.
- Commit messages follow Conventional Commits (`feat:`, `fix:`, `test:`, `docs:`).
- Repeatable procedures live in `.agents/skills/`; use `add-endpoint` when
  adding a route.

## Boundaries

- Routes never import `schemas/` or SQL tools and never run queries; enforced
  by `tests/test_architecture.py`. If it fails, follow its HOW TO FIX line;
  never edit the test.
- Only edit files the task needs. Do not edit README.md, CHANGELOG.md,
  rest/players.rest or docs/ unless asked.
- Never edit existing tests or `tests/player_fake.py` to make tests pass.
  If one must change, stop and ask, and say why.
- Never edit committed files in `alembic/versions/`; add a new migration.
- Ask before adding a dependency to `pyproject.toml`.
- Existing responses keep their fields, order and status codes.
- Stay inside this repository; do not search or read folders above it.
- Never commit `.env` or anything with keys or passwords.
- If a request needs a rule the data does not contain (for example, grouping
  positions into "Defenders"), list what the data has and ask before inventing one.

## Known failure patterns

- The first `uv run pytest` in the sandbox can fail on uv's read-only cache:
  ask to rerun the same command outside the sandbox; do not write a wrapper.
- `git diff --check` "trailing whitespace" is usually CRLF line endings on D:;
  confirm with `git -c core.whitespace=cr-at-eol diff --check`.
- A new endpoint returns 422 unexpectedly: check route order (add-endpoint skill).
