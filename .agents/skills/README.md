# Skill library

| Skill | Owner | Last reviewed | Source | Notes |
|---|---|---|---|---|
| add-endpoint | Ammar | 2026-11-01 | ours | From the Assignment 1 baseline runs; points to integration-tests for data-writing tests |
| integration-tests | Ammar | 2026-11-01 | ours | Capstone skill; origin: Module 5 AC8 cleanup correction (runs/m5-players-pagination.md) |
| skill-installer (Codex bundled) | OpenAI | 2026-11-01 | third-party, vetted per Module 9 | Pinned by sha256 in capstone/threat-model.md; installs only from repos I have reviewed |
| imagegen, openai-docs, skill-creator, review-agent (Codex bundled) | OpenAI | not reviewed | third-party | Shipped with Codex CLI 0.166.0; not used in this repo |

Library rules: a new or changed skill goes through a PR; a third-party skill gets the
Module 9 review first and is pinned; a skill unused for a quarter is deleted.
