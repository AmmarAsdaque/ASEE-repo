# Spec: validate squad number range

## Goal
Stop players being created or updated with impossible squad numbers. Today the
API accepts any integer, such as 0, -5 or 999, so bad data can reach the database.

## Acceptance criteria
1. POST /players/ with squad_number 0 returns 422 and no player with squad number 0 is saved.
2. POST /players/ with squad_number 100 returns 422 and no player with squad number 100 is saved.
3. Squad numbers 1 and 99 are accepted: validate_squad_number(1) returns 1,
   validate_squad_number(99) returns 99, and POST /players/ with an unused squad_number 99 returns 201.
4. PUT /players/squadnumber/23 with squad_number 100 in the body returns 422 and player 23 is unchanged.
5. A rejected squad number returns FastAPI's standard 422 body whose first detail has
   loc ["body", "squad_number"] and a msg containing "squad_number must be between 1 and 99".
6. Nothing else changes: all existing tests pass with their assertions unchanged. The only
   test-data change is unknown_player()'s squad number 999 -> 98 (still valid and unused).

## Constraints
- Change only models/player_model.py.
- The range check lives in a plain function validate_squad_number(value) in
  models/player_model.py, called from a field validator on PlayerRequestModel, so
  mutation testing can reach it (mutmut does not mutate Field() constraints or decorated methods).
- No new dependencies; no database or migration changes.
- uv run pytest -q, uv run flake8 . and uv run black --check . all pass.

## Non-goals
- No validation of squad numbers in URL paths (GET, PUT or DELETE /players/squadnumber/{n}).
- No changes to players already stored in the database.
- No custom error format; FastAPI's standard 422 body is kept.
- No validation of other fields, such as date_of_birth.
