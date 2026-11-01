# Assignment 2 report: squad number range

## The change
POST and PUT bodies now reject squad numbers outside 1 to 99 with FastAPI's standard 422. The rule lives in a plain function, validate_squad_number(), in models/player_model.py, called from a field validator on PlayerRequestModel; the implementation commit changed only that file. Before any code, I changed unknown_player() from 999 to 98 in my own test commit, because two existing tests used 999 as a valid but unknown number and would have turned into 422s. In Module 4, Codex made that same change on its own without asking.

## Plan corrections
The most important correction concerned black. The plan's baseline said black flags tests/test_main.py and that the agent would leave it unchanged. The cause was the formatting of my new A2 tests, so I fixed it myself in a layout-only test commit and corrected the plan: black must report no files to reformat, and a black failure under tests/ means stop and ask. Without this, the implementation run could not pass all three checks without editing tests or ignoring a failing check. I also corrected step 1, which called the 98 fixture "already" true.

## What the tests caught
Before implementation, 5 tests failed and 39 passed: test_c1_request_post_player_squadnumber_zero_response_status_unprocessable, test_c2_request_post_player_squadnumber_hundred_response_status_unprocessable, test_c3_validate_squad_number_boundaries (ImportError: the function did not exist), test_c4_request_put_player_squadnumber_hundred_response_status_unprocessable and test_c5_request_post_player_squadnumber_invalid_response_body_detail. In the implementation run, Codex's first pytest after its edit still reported 5 failed, and the next run reported 44 passed with no further edit. Codex did not explain this, so I reran the suite three times: 44 passed each time. The final run is in results/tests.txt.

## What mutation testing caught
mutmut produced 8 mutants in validate_squad_number. BEFORE: 7 killed, 1 survived (87.5%). The survivor, x_validate_squad_number__mutmut_7, wrapped the message in "XX...XX". It survived because pytest.raises(match=...) searches for the text rather than matching it exactly. I anchored the pattern with ^ and $ and made test_c5 compare the exact 422 message, in a test-only commit. AFTER: 8 killed, 0 survived (100%). The score has limits: mutmut does not mutate Field() bounds or decorated methods, which is why the spec requires a plain function, and the mutation run uses only the unit test because API tests hang under mutmut. The validator wiring is covered by the API tests c1 to c5 instead.

## What the holdout caught
The holdout sends camelCase JSON ("squadNumber") with -5, 100 and 99. It passed on the first run. Every visible test uses snake_case, so the alias path was otherwise untested.

## Agent mistakes and interventions
None during implementation. git diff against my test commits showed no test changes. During planning, Codex declined to fix black itself: "resolving this existing formatting failure requires permission under AGENTS.md".

## What I would automate next
A pre-commit sensor that rejects any commit touching tests/ together with source files, so an agent weakening tests is caught automatically rather than by my manual git diff.
