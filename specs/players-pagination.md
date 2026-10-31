# Spec: pagination on GET /players/

## Goal
Clients can fetch the players list one page at a time with ?page= and ?size=,
so they don't have to download the whole squad on every request.

## Acceptance criteria
1. GET /players/?page=1&size=10 returns 200 with exactly 10 players.
2. Pages 1, 2 and 3 with size=10, joined in order, equal GET /players/ with no
   parameters: the same players, in the same order, with no duplicates or gaps.
3. GET /players/?page=3&size=10 returns the last 6 players, and
   GET /players/?page=4&size=10 returns 200 with an empty list [].
4. GET /players/?page=2 with no size uses size 20 and returns players 21 to 26.
5. Each of these returns 422: size=0, size=101, size=abc, page=0, page=-1.
6. GET /players/?page=1&size=10 followed by GET /players/?page=2&size=10 returns
   different players (pages do not share a cache entry), and a later GET /players/
   still returns all 26 players.
7. GET /players/ with no parameters returns the same response as before this change,
   and all existing tests pass without being edited.

## Constraints
- No new dependencies.
- Only these files change: routes/player_route.py, services/player_service.py,
  tests/test_main.py, and optionally one new file services/pagination.py.
- The response stays a JSON list of players (no wrapper object, no new fields).
- No database schema or migration changes.
- Maximum page size is 100; default page is 1 and default size is 20.
- uv run pytest -q, uv run flake8 . and uv run black --check . all pass.

## Non-goals
- Total-count fields, X-Total-Count or Link headers.
- Sorting or filtering parameters.
- Cursor-based pagination.
- Pagination on any other endpoint.
- Changing the cache TTL or the caching library.
