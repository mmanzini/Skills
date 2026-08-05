---
name: dashboard-refresh
description: Refresh the Atlas Obsidian dashboard. Regenerates the YAML-frontmatter data files under Dashboard/data/ (open tasks, GitHub trends with weekly/monthly summary + prediction + what-to-investigate, life executive-summary + metrics, upcoming) from the Intelligence layer and Tasks. Trigger on "/dashboard-refresh", "refresh dashboard", "update my dashboard", "regenerate the dashboard", or when the obsidian-shellcommands button runs `claude -p "/dashboard-refresh"`.
---

# Dashboard Refresh Skill

Regenerate the Atlas dashboard's data layer. You **only** write `Dashboard/data/*.md`.
Never edit `Dashboard/scripts/Dashboard.js` or `Dashboard/Dashboard.md` —
presentation is fixed (see `Dashboard/CLAUDE.md`).

## Execution contract (read first)

This skill is **not done after one step**. A run MUST process **every** resolver
in the Run order below and leave **all six** `Dashboard/data/*.md` files with a
fresh `updated:`/`as_of:` stamp (today) — unless a source is genuinely
unavailable, in which case leave that one file untouched and say so in the final
report. Do not stop after the deterministic `tasks` script; the LLM-synthesis
resolvers (github-trends, ai-news, political-economy, life prose, upcoming) are
the point of the refresh and are mandatory.

**This is a dashboard-only task. Do NOT touch the Tasks board** (`Tasks/TASKS.md`,
`Tasks/ledger.md`, `_tasks-archive.md`). If a Stop hook or session reminder asks
you to reconcile the task board, that is out of scope for this run — finish the
dashboard first; the board is maintained in interactive sessions, not here.

Checklist — tick all before finishing:
`tasks` · `life metrics` · `github-trends` · `ai-news` · `political-economy` ·
`life prose` · `upcoming`.

## Hard rules

1. Write only inside `Dashboard/data/`.
2. Preserve each file's frontmatter **schema** (see `assets/schemas/data-files.md`).
   Adding keys is OK; renaming/removing breaks the matching renderer method.
3. Stamp `updated:` / `as_of` on every file you touch — from the real clock in
   **local time** (`date +%Y-%m-%dT%H:%M`), never guessed and never `date -u`.
   The renderer's freshness badges compare stamps against local now and the
   deterministic tasks script stamps local, so a UTC stamp makes every section
   read hours stale (seen 2026-07-25).
4. If a source is unavailable, **leave that file's existing data in place** —
   degrade gracefully, never blank a section.
5. One section = one resolver = one data file. New sources are new resolvers.
6. **Quote risky scalars.** Any string value or list item containing `: `
   (colon-space), a leading `-`/`?`/`[`/`{`/`@`/`` ` ``, or `#` mid-line must be
   wrapped in double quotes. A bare `: ` makes YAML parse the item as a `key:
   value` map and silently breaks the whole file's frontmatter → the section
   vanishes from the dashboard. Block scalars (`>-`, `|-`) are safe; plain
   list items (`highlights`, `actions`, `investigate`, `watch`) are not.

## Execution strategy — fan out the LLM resolvers

Run the five LLM resolvers (github-trends, ai-news, political-economy, life
prose, upcoming) as **parallel subagents** (Task tool or Workflow), one per
resolver, each given its exact input file paths and required output schema.
The orchestrator (you) runs only the deterministic scripts, collects the
subagent outputs, and writes the data files (single writer — apply hard rule
6 quoting; stamp `updated:` from the real clock via `date`, never a guessed
time). This matters twice over:

- **Context ceiling.** A serial headless run accumulates every web sweep in
  one context and can cross the 200K long-context gate ("Usage credits are
  required for long context requests"). Subagents each get a fresh, small
  context; the orchestrator stays far under the gate.
- **Wall clock.** The web sweeps (ai-news, political-economy) dominate the
  run; in parallel the whole refresh takes ~7 min instead of serial ~7 min
  per-sweep stacking.

If the runtime has no subagent support, fall back to serial — but then keep
each sweep lean (cap search rounds) to stay under the context gate.

## Run order

Deterministic resolvers are scripts; prose resolvers are LLM synthesis. Full
detail in `references/resolvers.md` — summary:

1. **tasks** (deterministic): `python3 Skills/dashboard-refresh/scripts/parse_tasks.py`
   → writes `data/tasks.md`. Do not hand-edit.
2. **life metrics** (deterministic): `python3 Skills/dashboard-refresh/scripts/daily_metrics.py 14`
   → JSON; drop its `metrics` array + `as_of` into `data/life.md`.
3. **github-trends** (LLM): synthesize `summary_week`/`summary_month`/`prediction`/
   `investigate` from `Intelligence/github-trends/` → `data/github-trends.md`.
3a. **ai-news** (LLM + live web): sweep AI-industry news since the last refresh
   (max 7 days), dedup against the `## Previously shown` ledger in the file body,
   add a world-reaction recap and an always-on weekly digest →
   `data/ai-news.md`. See `references/resolvers.md`.
3b. **political-economy** (LLM + live web): blend `Intelligence/political-economy/`
   + `Intelligence/philosophy/` with live web-news (threads derived dynamically) →
   `data/political-economy.md`. See `references/resolvers.md`.
4. **life prose** (LLM): from the last 14 daily notes write `happened`/`now`/
   `coming`/`highlights`/`actions`/`prediction` into `data/life.md` (alongside the
   metrics from step 2). Cross-check `Tasks/TASKS.md` so actions aren't stale.
5. **upcoming** (LLM): forward items from Tasks + dailies + Intelligence →
   `data/upcoming.md`.

See `references/resolvers.md` for the precise rules of each.

## After writing

- Confirm each touched file's frontmatter parses (valid YAML). Run:
  `python3 -c "import yaml,sys; yaml.safe_load(open(f).read().split('---')[1])"`
  per touched file. A parse failure means an unquoted scalar (hard rule 6) —
  fix and re-check before reporting done.
- Dataview auto-refresh (~2.5s) re-renders the open `Dashboard.md`; no reload needed.
- Report one line: which sections refreshed, which were skipped and why.

## Invocation

- **Terminal pane:** `claude` → `/dashboard-refresh`.
- **Button / headless:**
  `env -u ANTHROPIC_API_KEY claude --model claude-opus-4-8 -p "/dashboard-refresh"`
  (cwd = vault root), wired to the obsidian-shellcommands "Refresh Dashboard"
  command. `env -u` guards against a stale system-level API key shadowing the
  keychain login; the Opus pin avoids the Sonnet long-context tier routing that
  gates headless runs behind usage credits.
