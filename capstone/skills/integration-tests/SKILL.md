---
name: integration-tests
description: Use when writing or changing tests in tests/test_main.py that create, update or delete players, depend on cached responses, or need a special database state such as an empty table. Covers cleanup, shared seed data and exact assertions.
---

# Integration tests that touch data

The test suite runs against the real local SQLite file with 26 seeded players, and
tests/test_migrations.py counts those rows. Anything a test leaves behind breaks
other tests, sometimes only on the next run.

## Steps

1. Use the `client` fixture and test data from `tests/player_fake.py`:
   `nonexistent_player()` for a new player, `existing_player()` for a seeded one.
   Never edit `tests/player_fake.py` or existing assertions; if one seems wrong, stop and ask.
2. Every test that POSTs, PUTs or DELETEs restores the database in a `finally` block:
   - created a player: delete it by squad number in `finally`
   - changed a seeded player: PUT `existing_player()` back in `finally`
   - a request that should be rejected: still delete in `finally`, because before the
     feature exists the request may succeed and create the row
3. Never delete or change seeded players to reach a state. For "empty table" or other
   special states, override `generate_async_session` with a separate in-memory engine
   via `app.dependency_overrides`, and remove the override in `finally`.
4. `GET /players/` responses are cached. A test that asserts `X-Cache` or depends on a
   fresh read must not depend on test order: clear the cache first, or assert only
   what a write is guaranteed to change.
5. Assert exact values: `==` on bodies and messages, not `in`; anchor
   `pytest.raises(..., match="^...$")`. A substring check lets a mangled message pass.
6. Follow the naming and layout in `tests/test_main.py`:
   `test_request_<method>_<path>_<case>_response_<expectation>`, Arrange/Act/Assert comments.
7. Run `uv run pytest -q` twice. Both runs must give the same result; a different
   second run means a test left data behind.

## Origin

In Module 5 (runs/m5-players-pagination.md) Codex's plan for the criterion 8 test
POSTed a new player and asserted on it with no guaranteed cleanup, so a failing
assertion would have left the player in the shared database. I corrected it: "use
nonexistent_player() from tests/player_fake.py for the new player, and delete it in a
finally block so cleanup happens even if an assertion fails." The same risk shaped my
Assignment 2 tests, and a2/results/mutation.txt records the related weakness
(x_validate_squad_number__mutmut_7 survived because match= was not anchored).
This skill exists so neither happens again.
