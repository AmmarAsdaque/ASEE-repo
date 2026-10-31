Intent: Let clients fetch the players list one page at a time, so they don't
download the whole squad on every request.

Context: The endpoint is GET /players/ in routes/player_route.py. It returns a
plain JSON list and caches it in memory under the single key "players"
(aiocache SimpleMemoryCache, TTL 600 s). The query is in
services/player_service.py (retrieve_all_async). The test database is seeded
with 26 players. Tests are in tests/test_main.py and run with: uv run pytest -q
Lint with: uv run flake8 . and uv run black --check .
Follow the style of the existing GET /players/ tests in tests/test_main.py.

Constraints: Add optional query parameters page (default 1, minimum 1) and
size (default 20, minimum 1, maximum 100). The response stays a JSON list of
players: no wrapper object, no new fields, no count headers. GET /players/ with
no parameters must return exactly what it returns today. Each page must have
its own cache entry. No new dependencies, no database or migration changes.

Boundary: Only edit routes/player_route.py, services/player_service.py and
tests/test_main.py; you may create services/pagination.py. If any other file
must change, stop and ask me first. Do not edit existing tests.

Output contract: Invalid page or size (0, -1, 101, "abc") returns status 422
using FastAPI's standard validation response. When you finish, reply in
exactly this shape:
Files changed: <list>
Tests added: <one line per test>
Commands run: <each command>
Result: <the final summary line of each command>

Done: New tests for defaults, page 3 (last 6 players), an empty page 4, the
422 cases and separate cache entries pass. All existing tests pass unedited.
flake8 and black report no problems.
