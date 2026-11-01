# Plan: validate squad number range

1. Keep implementation changes confined to `models/player_model.py`.
   Preserve all test files, routes, services, response models, dependencies,
   database records, and migrations. `unknown_player()` already uses squad
   number 98, satisfying the fixture requirement and c6 without any edit.
> CORRECTION: unknown_player() is 98 because I changed it (999 -> 98) in my tests commit,
> as spec criterion 6 says: a deliberate test-data decision, not something already true.
> Do not touch tests/player_fake.py.

2. Add a plain module-level function `validate_squad_number(value)` with integer
   input and return annotations. Reject values below 1 or above 99 by raising
   `ValueError("squad_number must be between 1 and 99")`; return accepted values
   unchanged. Keep the comparisons in this function so mutation testing can
   exercise them. This covers c3's direct checks for 0, 1, 99, and 100.

3. Import Pydantic's `field_validator` and add a validator for `squad_number`
   on `PlayerRequestModel`. Use the default after-validation mode and a
   classmethod that delegates to the plain function and returns its result.
   Retain the existing integer field and model alias configuration. Do not
   replace the function with `Field()` bounds or put the comparisons inside
   the decorated method.

4. Rely on the existing shared request model to reject invalid POST and PUT
   bodies before route handlers execute. Keep FastAPI's standard validation
   response: c1 and c2 require 422 and subsequent lookups returning 404 for
   numbers 0 and 100; c4 requires PUT with body number 100 to return 422 and
   leave player 23 unchanged. Leave URL path validation unchanged.

5. Verify the supplied acceptance tests without changing their assertions:
   - c3 also requires POST with unused number 99 to return 201.
   - c5 requires the first validation detail to locate
     `["body", "squad_number"]` and include the exact range message.
   - c6 requires the existing unknown-player fixture's valid number to remain
     absent from the database.
   Preserve existing successful responses and existing behavior for valid
   numbers, including PUT body/path mismatches.

6. Run the required whole-repository checks exactly as documented:
   `uv run pytest -q`, `uv run flake8 .`, and `uv run black --check .`.
   If pytest hangs at the first HTTP request in the sandbox, request an
   outside-sandbox rerun of `uv run pytest -q`; do not introduce a wrapper.
   If formatting needs correction, confine edits to the implementation file
   and rerun all three checks. Investigate failures without altering tests;
   stop and ask if a test-file change proves necessary.

7. Review the final diff to confirm only `models/player_model.py` changed
   during implementation, apart from this requested plan. Report the final
   completed check results, quoting their last summary lines (or noting no
   output for a successful silent command). Do not claim acceptance until all
   three checks pass.
> CORRECTION: "All three checks pass" now includes black reporting no files to reformat.
> Only models/player_model.py may change; a test file in the final diff means stop.

## Baseline checks during planning

- `uv run pytest -q`: `5 failed, 39 passed in 4.50s`. Failures are c1,
  c2, the direct c3 helper test, c4, and c5, before implementation.
- `uv run flake8 .`: `0` (exit status 0).
- `uv run black --check .`:
  `1 file would be reformatted, 21 files would be left unchanged.`
  The reported file is `tests/test_main.py`. Leave it unchanged; resolving
  this existing formatting failure requires permission under AGENTS.md and
  conflicts with the current instruction not to change test files.
> CORRECTION: The black failure came from the formatting of my new A2 tests. I fixed it
> myself in a separate test-only commit before implementation, with no assertion changes.
> Black must now pass with 0 files to reformat; if it flags anything under tests/ again,
> stop and tell me instead of editing tests.
