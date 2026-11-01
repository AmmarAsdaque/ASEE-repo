# Module 6 Exercise 6.1
- File: databases/player_database.py (get_database_url); 15 mutants
- Before: 15/15 killed (100%) with Codex's tests. After: 15/15, nothing to strengthen.
- Weakest agent assertion: line 89, `assert isinstance(exception, GeneratorExit)`:
  a type check that repeats line 88.
- Run time: 17.5 s total including mutmut install; mutation testing itself ~2.4 s
  (6.3 mutations/second).
- Hand mutant (module-level, not mutated by mutmut):
  DATABASE_URL.startswith("sqlite") -> startswith("postgres"): tests PASSED (survived).
  killed 0 / survived 1
- Lessons:
  - A 100% mutmut score only covers code mutmut mutated (inside functions);
    module-level setup like _connect_args was never tested.
  - Most agent tests mock the internals of generate_async_session
    (__aenter__/__aexit__ awaited), so they check how it is written, not what it does.
- Why not services/player_service.py: database-bound; most mutants timed out.
