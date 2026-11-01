# Safety config: Codex CLI 0.166.0 on the players API

Launch: `codex --sandbox workspace-write --ask-for-approval on-request` from the repo root (WSL).
Files: config.toml (copy of ~/.codex/config.toml), m5.rules, m9-network.rules and
default.rules (copies of ~/.codex/rules/). The agent cannot edit any of them: they live outside
the workspace, and the sandbox blocks writes there.

| Rule | Risk | Why |
| --- | --- | --- |
| `[apps._default] enabled = false` (config.toml) | R1, R2 | Removes every app connector: GitHub writes, Sites publishing, Hugging Face jobs |
| `web_search = "disabled"` (config.toml) | R1 | No web pages in, no data out in URLs |
| workspace-write sandbox (launch flag) | R1, R2 | Writes only inside the repo; shell network restricted |
| curl, wget, nc, ncat, ssh, scp, sftp, rsync, ftp, telnet: forbidden (m9-network.rules) | R1 | No shell route out, even when the agent asks to escalate |
| gh, aws, az, gcloud: forbidden (m9-network.rules) | R1, R2 | No agent use of my GitHub or cloud accounts |
| git remote/fetch/pull/clone: prompt (m9-network.rules) | R1, R3 | Network git operations need my review |
| git push: forbidden (m5.rules) | R2 | Pushing is done by me |
| rm: forbidden (m5.rules) | R2 | Deleting files is done by me |
| python, python3, bash, sh, mv, cp, sed: prompt (m5.rules) | R3 | Scripts and bulk edits need my review |
| uv add, uv pip: prompt (m5.rules) | R3 | I check every new package name exists first |
| uv run pytest/flake8/black, git status/diff: allow (m5.rules) | none | Easy to undo; needed every task |
| Day-one broad Python-wrapper allowance removed (default.rules) | R1, R3 | It let any code after a fixed prefix run unasked |
| GitHub token removed (`gh auth logout`); log in only to push | R1 | No plain-text token on disk during agent sessions |

Verified with `codex execpolicy check`: curl, gh, aws and `git push` are forbidden;
`uv run pytest -q` is allowed. Session evidence: runs/m9-mitigation-check.md.
Secrets: none in this folder. Sandbox: Codex's own only; no container or VM (see Residual risk).
Versions: Codex CLI 0.166.0; plugins sites 1.1.2, work-pets 0.1.6, plugin-management 0.1.0.
