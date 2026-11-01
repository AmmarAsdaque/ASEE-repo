# Position filter implementation plan

1. Confirm scope and reuse existing behavior. Implementation will change only
   `services/player_service.py`, `routes/player_route.py`, and `tests/test_main.py`.
   This planning step writes only `capstone/plan.md`. Preserve existing tests,
   response fields, ordering, status codes, pagination defaults, and write-side
   cache invalidation. Read the integration-tests skill before adding tests that
   create players. No dependencies, migrations, or other file changes are needed.

2. Update `services/player_service.py`. Extend `retrieve_all_async` with an optional
   position argument and perform case-insensitive exact matching in the service.
   Preserve the unfiltered retrieval order by filtering the retrieved collection
   without sorting it. Reuse `paginate_players` after filtering so page boundaries
   apply to matching players. Do not introduce position groupings or substring
   matching.

3. Update `routes/player_route.py`. Add optional `position` query validation with
   `Query(min_length=1)` to the existing list endpoint and pass it to the service.
   Keep filtering and database queries out of the route. Include the position in
   filtered cache keys, followed by page and size when pagination is requested;
   all keys must start with `players`. Preserve the existing unfiltered keys
   (`players` and `players:page=N:size=M`), TTL, and `X-Cache` behavior. Retain
   existing `clear(CACHE_KEY)` calls on writes.
> CORRECTION: The position comes from the URL, so a crafted value can collide with another
> key: ?position=Goalkeeper:page=1:size=2 (unpaginated) gives the same key as
> ?position=Goalkeeper&page=1&size=2 and would cache [] for 10 minutes. Encode the position
> in the key with urllib.parse.quote(position, safe="") (standard library, no new dependency),
> and add one test showing the crafted request does not change what the real paginated
> request returns.

4. Append seven integration tests to `tests/test_main.py`, using Arrange/Act/Assert
   comments and the following acceptance-criterion mapping. Do not edit existing
   tests or `tests/player_fake.py`.

   - **AC 1** — `test_request_get_players_position_ac1_response_goalkeepers`:
     derive the expected Goalkeepers from the unfiltered HTTP response; assert
     the filtered response is 200 and equals that complete expected list,
     including its count and order.
   - **AC 2** — `test_request_get_players_position_ac2_response_case_insensitive`:
     request `Goalkeeper` and `goalkeeper`; assert both return 200 and identical,
     nonempty player lists.
   - **AC 3** — `test_request_get_players_position_ac3_response_empty_list`:
     request `position=Nowhere`; assert 200 and exactly `[]`.
   - **AC 4** — `test_request_get_players_position_ac4_response_unprocessable`:
     request an explicitly empty position; assert 422 and a validation error
     identifying the position query parameter.
   - **AC 5** — `test_request_get_players_position_ac5_response_paginated_matches`:
     derive Centre-Backs from the unfiltered response; request position with
     page 1 and size 2 and assert 200 with exactly the first two expected players.
     Request a page beyond that filtered list and assert 200 with `[]`.
   - **AC 6** — `test_request_get_players_position_ac6_response_isolated_invalidated_cache`:
     clear the players cache, request Goalkeepers and Centre-Backs, and assert
     distinct correct responses with cache misses; repeat both and assert cache
     hits with unchanged bodies. POST a temporary Goalkeeper using an unused,
     valid squad number; assert 201 and that the next Goalkeeper request is a
     cache miss containing the created player. Delete the temporary player in
     `finally`, following the integration-tests skill.
   - **AC 7** — `test_request_get_players_position_ac7_response_unchanged_unfiltered`:
     clear the cache and capture the unfiltered response, exercise filtered
     requests, then assert the next unfiltered response retains the same full
     body, fields, order, 200 status, and cache-hit behavior. Also run every
     existing test unedited, including `tests/test_architecture.py`.

5. Validate the implementation across the whole repository with exactly
   `uv run pytest -q`, `uv run flake8 .`, and `uv run black --check .`.
   If uv encounters its read-only cache failure, request escalation and rerun
   the same command without a wrapper. Resolve failures only within the allowed
   implementation files; stop and ask if an existing test requires modification.
   Review the final diff for scope and report the final summary line of each
   completed validation run. Keep the implementation under about 400 changed
   lines; fill in the AI-disclosure block in any eventual PR description.
