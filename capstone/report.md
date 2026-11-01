# Capstone report: ASEE-repo (players API)

## What the harness caught
My guides shaped the run before any check had to fire. The delivery log shows "I'm using the add-endpoint and integration-tests skills"; Codex wrote the tests first (6 failed, 50 passed), put AC6's temporary player behind `finally`, ran the suite twice as the skill's step 7 asks (56 passed both times) and kept the filtering in services/player_service.py, so tests/test_architecture.py passed throughout. The sensor had already proven itself: the planted route query in e5088ab failed with three named problems and the agent's fix in 82a3e8a passed (sensors/evidence.txt). The Module 9 config held too: no connector tools, with curl and git push forbidden.

## What slipped through
The most serious problem got past every automated check. The agent's plan joined strings into cache keys, so ?position=Goalkeeper:page=1:size=2 would produce the same key as the real paginated request and cache [] for ten minutes. No criterion covered it; I caught it reading the plan (interventions.md, 20:44), and Codex then encoded the key with quote() and added a regression test. AC2's test is weak: it was one of the two new tests passing before the feature existed, because two unfiltered lists are trivially equal. Smaller slips: my "sed" rule prompted on a read-only sed -n (20:45), and the route edit used write_text, harmless only because that file is LF.

## Cost of the run
Codex reported 41,852 tokens (35,373 input plus 986,112 cached input, and 6,479 output) for planning and implementation, about 20 tool-calling steps within my 30-step budget. Agent time was 37 seconds for the plan and 10 minutes 12 seconds for the build (20:41 to 20:55). My time was about 20 minutes including verification, with 6 interventions: one plan correction and five permission prompts I read before answering. On my ChatGPT Plus subscription there is no per-token charge, so I did not convert it to a price; the cached input, 96% of all input, shows re-sent context drives the cost.

## Next check to automate
A cache-key test that sends separator characters (":", "=", "%") in every query value of each cached list endpoint and asserts the crafted request never changes what the genuine request returns. It would have caught the poisoning bug without my review. I would also replace the "sed" prompt rule with ["sed", "-i"], because prompts on harmless commands train me to approve without reading, which is how a risky one gets through.

## Ladder level the repo can now support
practice/m8/autonomy-map.md rates "Coding: routine endpoints and validation" High on safety, reversibility and verifiability, checked by my reading, which caps it at rung 3. I ran at rung 3 with more delegation than before: Codex wrote the plan, the tests and the code, and I reviewed the plan and each write; the holdout, never shown to the agent, passed on its first run. The repo can support rung 3 for changes in routes/, services/ and models/. It cannot support rung 4 yet: the worst bug was found only by my reading, AC2 shows agent-written tests can pass without the feature, and no CI runs the checks automatically.
