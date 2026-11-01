# Spec: filter the players list by position

## Goal
Clients can list only the players in one stored position (for example all Goalkeepers),
alone or together with pagination, without downloading and filtering the whole squad.

## Acceptance criteria
1. GET /players/?position=Goalkeeper returns 200 with only players whose position is
   "Goalkeeper", and the same number of players as the unfiltered list has with that position.
2. Matching is case-insensitive: ?position=goalkeeper returns the same players as ?position=Goalkeeper.
3. An unknown position (?position=Nowhere) returns 200 with [].
4. An empty position (?position=) returns 422.
5. Position works with pagination: ?position=Centre-Back&page=1&size=2 returns the first two
   Centre-Backs in the order of the unfiltered list, and a page past the end returns [].
6. Filtered responses are cached separately: ?position=Goalkeeper then ?position=Centre-Back
   return different players; after POST /players/ creates a new Goalkeeper,
   ?position=Goalkeeper includes it on the next request.
7. GET /players/ without position returns the same response as before this change; all
   existing tests pass unedited, including tests/test_architecture.py.

## Constraints
- Only routes/player_route.py, services/player_service.py and tests/test_main.py change.
- Filtering lives in services/player_service.py; the route only reads the query parameter
  and calls the service (tests/test_architecture.py must pass).
- Cache keys for filtered responses start with "players", so existing writes clear them.
- Tests that create players follow the integration-tests skill (cleanup in finally).
- No new dependencies; no database or migration changes.
- uv run pytest -q, uv run flake8 . and uv run black --check . all pass.

## Non-goals
- Groupings such as "Defenders"; only exact stored positions.
- Partial or substring matches, or several positions at once.
- Filtering by any other field, and new sort orders.
