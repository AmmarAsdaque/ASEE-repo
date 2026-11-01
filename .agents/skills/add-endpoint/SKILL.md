---
name: add-endpoint
description: Adds a REST endpoint to the players API with a service function, a thin route and integration tests. Use when the user asks to add, create or expose an endpoint, route or API method, including filtered player lists.
---

# Add an endpoint

## Steps

1. Read `routes/player_route.py` and `services/player_service.py` first and
   follow their patterns. Use a path in the existing style,
   `/players/<noun>/{value}`, like `/players/squadnumber/{squad_number}`.
2. Write the tests first, in `tests/test_main.py` (never a new file), under a
   new section comment `# GET /players/<path> ---`. Follow the existing names
   and Arrange/Act/Assert style. Cover the success case, the no-match case and
   one bad-input case, using the seeded data (26 players). Run
   `uv run pytest -q`; the new tests must fail.
3. Add an async function in `services/player_service.py` that builds the query
   with `select(Player).where(...)`.
4. Add a thin async handler in `routes/player_route.py` with `response_model`,
   `status_code`, `summary`, `tags=["Players"]` and
   `Depends(generate_async_session)`. It only calls the service function.
5. Route order: a one-segment path such as `/players/something` must be
   declared above `/players/{player_id}`, or FastAPI reads it as a UUID and
   returns 422.
6. Status codes:
   - list: 200 with a list, `[]` when nothing matches
   - single player: 200, or 404 via HTTPException when missing
   - create: 201; update and delete: 204
7. Do not add caching unless asked. If asked, use a key that starts with
   "players" (for example "players:team") so existing writes clear it.
8. Add the new path to the endpoint list in the docstrings at the top of
   `routes/player_route.py` and `tests/test_main.py`. Do not edit README.md or
   `rest/players.rest` unless asked.
9. Run `uv run black .`, then `uv run pytest -q`, `uv run flake8 .` and
   `uv run black --check .`. Fix every failure.
10. Reply with: the endpoint added, the tests added, and the final summary line
    of each command.

## Example test

    def test_request_get_players_team_unknown_response_body_empty(client):
        """GET /players/team/{team} with no matching players returns []"""
        # Act
        response = client.get(PATH + "team/Nowhere FC")
        # Assert
        assert response.status_code == 200
        assert response.json() == []

## Edge cases

- Filter on values exactly as they are stored in the seed data (for example
  positions such as "Centre-Back"). Do not invent groupings or synonyms; list
  the stored values and ask.
- Unknown filter value on a list endpoint: 200 with `[]`, not 404.
