| Task | Rung used | Safety | Reversible | Verifiable | Ceiling rung | Mode | Note |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Ask Codex to run the test suite (setup) | 3 | High | High | High (my own run gave the same 25 passed) | 3 | Generate | Fine, but I approved a broad "always run" command; next time approve once |
| Write parse_pagination (M1, three runs) | 3 | High (new file, not wired in) | High (rm the file) | Medium (manual checks only, no tests) | 2 | Generate | Worked above my ceiling; all runs left size uncapped, which a test would have caught |
| Set up WSL, uv, Codex and GitHub auth | n/a (learning) | Medium | High | Medium (I could explain each step) | n/a (learning) | Learn | AI explained each step; I ran every command myself |
| Validate squad_number and date_of_birth on POST/PUT (planned) | planned: 1 | Medium (changes the API contract) | Medium (clients may adapt to it) | Medium (no bad-input tests yet) | 2 | Learn | Planned for later: ask Codex to explain current validation and seed data first, then write the rules myself |

I let Codex write parse_pagination at rung 3, but with no tests its real ceiling was rung 2; writing tests first for defaults, max size and bad input would raise it to rung 4.
