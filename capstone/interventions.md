# Interventions: position filter

Rung: 3, Reviewer. Codex wrote the plan, the tests and the code; I reviewed the plan and the
final diff; the sensor, skills and checks judged the steps in between. Safety config:
capstone/safety-config/. Session log: runs/delivery.md

| Time | What I did | Why | Harness follow-up |
| --- | --- | --- | --- |
| 20:44 | Added a > CORRECTION: under plan step 3: encode the position in the cache key (urllib.parse.quote) and test a crafted collision | Joined-string keys let ?position=Goalkeeper:page=1:size=2 collide with the real paginated key and cache [] for 10 min (cache poisoning from untrusted input); no criterion covered it | Candidate check: a test that fuzzes key separators in query values |
| 20:45 | Approved a permission prompt for a read-only batch (git status, sed -n ... p, cat) | The m5.rules "sed" prompt fires on read-only sed -n as well as sed -i; nothing here edits files | Narrow the rule to ["sed", "-i"] so only in-place edits prompt |
| 20:47 | Reviewed and approved the agent's test-append command (cat >> tests/test_main.py, ~200 lines: AC1-AC7 + collision test) | It writes to the test file, so I checked it appends (>>, not >), AC6 cleans up in finally, and the CORRECTION's collision test is present | None |
| 20:49 | Approved the agent's second test-append command (cat >> tests/test_main.py, 194 lines) and reviewed the added tests with git diff | It writes to the test file; I checked it only appends (no existing line changed), AC6 cleans up in finally, and the collision test from my CORRECTION is present | None |
| 20:51 | Approved the agent's python3 edit to services/player_service.py | Script prompt rule; I checked it only adds an optional position argument with an exact case-insensitive (casefold) match inside retrieve_all_async, keeps order, and preserves CRLF line endings | None |
| 20:54 | Approved the agent's python3 edit to routes/player_route.py | Checked Query(min_length=1), the quote()-encoded cache key starting with "players", unchanged unfiltered keys, and no filtering in the route; file is LF so write_text is safe | None |
| 21:00 | Ran the holdout ~/holdouts/capstone/test_holdout.py (never shown to the agent): PASSED | Checks that DELETE also clears position-filtered cache entries; no acceptance criterion covered it | None |
