# Threat model: players API with Codex

Setup: Codex CLI 0.166.0 (model GPT-6.1-Sol, paid), started in the repo root inside WSL on
Windows with `--sandbox workspace-write --ask-for-approval on-request`. Repo: fork of
nanotaboada/python-samples-fastapi-restful (FastAPI, SQLite, uv). Inventory taken from my own
checks and a read-only Codex inventory session, before the Module 9 changes.

## 1. Inventory

| Item | Type | What it can reach | Source | Trifecta leg |
|---|---|---|---|---|
| Repository source, tests, specs, a2/, capstone/ | Data | All code in ASEE-repo | Mine (fork of a public repo) | Private data (low) |
| ~/.config/gh/hosts.yml: GitHub token, scopes repo, workflow, gist, read:org | Credential | Write access to every repo on my account, incl. GitHub Actions workflows | Mine (gh login, git credential helper) | Private data |
| ~/.codex/auth.json | Credential | My ChatGPT/Codex sign-in | Mine | Private data |
| ~/.aws -> /mnt/c/Users/USER/.aws | Credential (likely) | My AWS account | Mine | Private data |
| All of D: and C: via /mnt | Data | Personal documents (financial statements, WhatsApp docs, photos), FYP and research, other code projects | Mine | Private data |
| Shell (exec_command): workspace-write sandbox, shell network restricted, escalation on request | Tool | Any command I approve; installed: curl, wget, ssh, nc, gh, git | Built in | Way out |
| File edits (apply_patch) | Tool | Writes inside the repo only, including AGENTS.md, .agents/skills/ and tests/; not asked | Built in | None (but can change its own instructions) |
| Web search (web__run) | Tool | Any query or URL | Built in | Untrusted content and way out |
| App connectors (mcp__codex_apps__): GitHub (fetch_issue, fetch_pr_comments, create_commit, update_file, merge_pull_request, add_comment_to_issue, ...), Sites (deploy_site_version), Hugging Face (hf_jobs), image generation, pets, document control, plugin management | MCP connectors | My GitHub account, public web hosting, remote compute | OpenAI-provided, linked to my accounts | Untrusted content and way out |
| Subagents, Codex threads and worktrees | Tool | Delegated work with the same sandbox | Built in | None |
| Skills: add-endpoint, integration-tests | Skill | Edit routes/services/tests; run uv run pytest, flake8, black | Mine | None |
| Bundled skills: skill-installer, skill-creator, imagegen, openai-docs, review-agent; plugins sites 1.1.2, work-pets 0.1.6, plugin-management 0.1.0 | Skill / plugin | skill-installer downloads and installs skills from GitHub; sites publishes; work-pets uploads | Third party (OpenAI) | Untrusted content and way out |
| Upstream files (CLAUDE.md.off, .claude.off/commands, .coderabbit.yaml, docs/, CHANGELOG) | Content | Text written by upstream contributors | Third party | Untrusted content |
| git push through the gh credential helper | Outbound channel | AmmarAsdaque/ASEE-repo (public) | Built in | Way out |
| ~/.codex/config.toml and ~/.codex/rules/*.rules | Config | Outside the workspace, so the agent cannot edit them | Mine | None |

Trifecta check
Private data: a GitHub token with repo and workflow scopes in a plain-text file, my Codex
sign-in, a link to my AWS folder, and every file on D: and C:. The sandbox restricts writes,
not reads, and Codex has already searched outside the repo unprompted (find .. and
rg --files /mnt/d in my Module 3 and Assignment 1 baseline runs).
Untrusted content: upstream issues and PR comments through the GitHub connector, web search,
upstream files in my fork, and third-party skills and plugins.
Way out: GitHub connector writes, Sites publishing, Hugging Face jobs, web requests (a URL can
carry data), curl/wget/ssh/nc after escalation, and git push through the gh helper.

Verdict: before Module 9, all three legs were present in every normal session, because the
connectors and web search were on by default and the shell's network block does not cover them.
My `git push` forbidden rule gave false confidence: the GitHub connector could commit and merge
without the shell.

## 2. Third-party review

Item: skill-installer (bundled Codex system skill).
Source: installed with Codex CLI 0.166.0 at ~/.codex/skills/.system/skill-installer/,
reviewed on 2026-11-01. Publisher: OpenAI, shipped with the Codex CLI (Apache 2.0 licence).
Its description says it installs "curated skills from openai/skills or other repos".

Files read (754 lines): SKILL.md (58), scripts/install-skill-from-github.py (355),
scripts/list-skills.py (106), scripts/github_utils.py (21), agents/openai.yaml (5),
LICENSE.txt (202), assets/skill-installer.png and assets/skill-installer-small.svg (icons).

Pinned (sha256), Codex CLI 0.166.0:
- SKILL.md d68b77e5bbb34dedab89d134da52855f140fc4b4299b80104f534e3b9e98f8ee
- scripts/github_utils.py 61c1bbe2ae217433b4b6f9f09f21aca4df52c12598068343ade719f706e4859b
- scripts/install-skill-from-github.py 38f311b75664bb063808f982c600271ebc4b560830f491705190f88a94e3e781
- scripts/list-skills.py 9d6dfb2abf3afeee7f027a89fb1626b918a973da18f4eb6c25681286301beb41

| Check | Finding | Verdict |
| --- | --- | --- |
| Publisher | OpenAI, bundled with Codex CLI 0.166.0 | OK |
| Packages | Installs no packages; uses only the Python standard library and git | OK |
| Hidden text | No HTML comments or zero-width characters; the long lines are the SVG icon path and prose lines in SKILL.md (description, install notes) | OK |
| Commands | _run_git() runs git through subprocess.run with an argument list, no shell | OK |
| Archive handling | _safe_extract_zip() checks real paths and rejects absolute and ".." paths before extracting | OK |
| Network | api.github.com (listings), codeload.github.com (zip downloads), github.com/<owner>/<repo>.git; "other locations" accepted, so any repo, not only openai/skills; needs escalation in my sandbox | Caution |
| File access | Writes to $CODEX_HOME/skills (~/.codex/skills), so an installed skill loads in every future session | Caution |
| Credentials | Uses GITHUB_TOKEN / GH_TOKEN or existing git credentials for private repos; my git helper was gh, so an install could have used my repo-scope token | Caution, mitigated (gh logged out) |
| Least privilege | Fine for its job, but whatever it installs runs with my user's rights | Caution |

Decision: kept, pinned at the hashes above. The installer itself is clean; the risk is what it
installs. Mitigations: network tools forbidden and the shell network blocked, so it cannot
download without my approval and a rule change; no token on disk during agent sessions; I will
install a skill only from a repo I have reviewed file by file, as for this one, and re-check
these hashes after every Codex update.

## 3. Top 3 risks

| Risk | OWASP ID (ASI01–ASI10) | Likelihood 1–3 | Impact 1–3 | Score = L×I |
|---|---|---|---|---|
| R1. Injected text in an upstream file, a GitHub issue or PR comment fetched through the connector, or a web page makes Codex read ~/.config/gh/hosts.yml or ~/.codex/auth.json and send it out through a connector, a web request URL or an escalated curl | ASI01 Agent Goal Hijack | 2: my repo is a fork of a public project, connectors and web search were on all course, and Codex already searched outside the repo unprompted | 3: the token can write every repo on my account and change Actions workflows | 6 |
| R2. Codex uses the GitHub connector (create_commit, update_file, merge_pull_request, add_comment_to_issue) to change my repo or post publicly on the upstream repo, bypassing my shell-only `git push` forbidden rule | ASI02 Tool Misuse and Exploitation | 2: the tools were exposed in every session and my push rule made me think pushing was blocked | 2: history damage or a public comment under my name; recoverable | 4 |
| R3. A skill installed through skill-installer from GitHub, an auto-updated plugin (sites, work-pets) or a package added with uv add runs code with my user's rights and reads D: or my home folder | ASI04 Agentic Supply Chain Vulnerabilities | 1: needs my approval plus network escalation; I have installed none | 3: code runs as me and can read every file I can | 3 |

## 4. Mitigations

| Risk | Mitigation | Leg broken | Evidence |
|---|---|---|---|
| R1 | Logged out of gh: the plain-text token (repo, workflow) is removed from hosts.yml; I log in only to push, never during an agent session. Disabled all app connectors (`[apps._default] enabled = false`) and web search (`web_search = "disabled"`). Forbidden rules for curl, wget, nc, ncat, ssh, scp, sftp, rsync, ftp, telnet, gh, aws, az, gcloud (m9-network.rules); the shell network stays restricted by the sandbox | Private data (token removed) and way out | runs/m9-mitigation-check.md: no mcp__codex_apps__ tools, no web search; `curl -I` blocked even when Codex retried with escalation ("no outbound network from the agent"); gh auth status: not logged in |
| R2 | Connectors disabled, so the GitHub write tools are gone; `git push` forbidden (m5.rules); `gh` forbidden; token removed | Way out (destructive action) | runs/m9-mitigation-check.md: "No GitHub tool is available"; `git push --dry-run` blocked: "Pushing is done by the human" |
| R3 | skill-installer reviewed and pinned (section 2); network tools forbidden, so it cannot download without a rule change; python/bash and uv add / uv pip need my approval (m5.rules); plugin versions recorded | Untrusted content (no new code without review) | `codex execpolicy check` results in safety-config/README.md; section 2 |

Also applied: removed a broad day-one "always allow" for a Python test wrapper from
default.rules; removed the empty .aws/ and .codex/ folders Codex created inside the repo
(both already in .gitignore, never committed).

## 5. Residual risk

The sandbox still lets Codex read the whole filesystem: my personal files on D:, ~/.codex/auth.json
and the AWS folder on C:. With connectors and web search off, network tools forbidden, git push
forbidden and the GitHub token removed, an injection has no direct way to send them out. One path
stays open by design: anything Codex reads goes to the model provider as conversation context. I
accept that because it is the service I chose, and I never point the agent at personal folders.

My rules match command prefixes, so an equivalent command written another way (for example a
Python script that opens a network connection) is not forbidden. python and bash only need my
approval, and the sandbox's network block is the real barrier; but approval is "on-request", so
Codex can ask to escalate and I could approve by mistake, as I did on day one. File edits inside
the repo are never asked: Codex could change AGENTS.md, its skills or tests, and only my diff
review and tests/test_architecture.py would catch it; no sensor protects AGENTS.md itself.

Disabling connectors relies on a Codex setting with a known bug report (openai/codex #17588)
where connectors stayed visible; I verified they are gone in 0.166.0 and will recheck after
every Codex update. Plugins update from OpenAI's curated source without my review. I use no
separate sandbox (container or VM). If I start reading issues from strangers, turn the
connectors back on, or keep personal files on the same machine long term, I will run Codex in a
dev container with only the repo mounted, no Windows drives and no credentials.
