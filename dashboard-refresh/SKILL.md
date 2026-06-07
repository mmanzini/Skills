---
name: dashboard-refresh
description: Refresh the Atlas Obsidian dashboard. Regenerates the YAML-frontmatter data files under Dashboard/data/ (open tasks, GitHub trends with weekly/monthly summary + prediction + what-to-investigate, life executive-summary + metrics, upcoming) from the Intelligence layer and Tasks. Trigger on "/dashboard-refresh", "refresh dashboard", "update my dashboard", "regenerate the dashboard", or when the obsidian-shellcommands button runs `claude -p "/dashboard-refresh"`.
---

# Dashboard Refresh Skill

Regenerate the Atlas dashboard's data layer. You **only** write `Dashboard/data/*.md`.
Never edit `Dashboard/scripts/Dashboard.js` or `Dashboard/Dashboard.md` —
presentation is fixed (see `Dashboard/CLAUDE.md`).

## Hard rules

1. Write only inside `Dashboard/data/`.
2. Preserve each file's frontmatter **schema** (see `assets/schemas/data-files.md`).
   Adding keys is OK; renaming/removing breaks the matching renderer method.
3. Stamp `updated:` / `as_of` on every file you touch.
4. If a source is unavailable, **leave that file's existing data in place** —
   degrade gracefully, never blank a section.
5. One section = one resolver = one data file. New sources are new resolvers.

## Run order

Deterministic resolvers are scripts; prose resolvers are LLM synthesis. Full
detail in `references/resolvers.md` — summary:

1. **tasks** (deterministic): `python3 Skills/dashboard-refresh/scripts/parse_tasks.py`
   → writes `data/tasks.md`. Do not hand-edit.
2. **life metrics** (deterministic): `python3 Skills/dashboard-refresh/scripts/daily_metrics.py 14`
   → JSON; drop its `metrics` array + `as_of` into `data/life.md`.
3. **github-trends** (LLM): synthesize `summary_week`/`summary_month`/`prediction`/
   `investigate` from `Intelligence/github-trends/` → `data/github-trends.md`.
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

- Confirm each touched file's frontmatter parses (valid YAML).
- Dataview auto-refresh (~2.5s) re-renders the open `Dashboard.md`; no reload needed.
- Report one line: which sections refreshed, which were skipped and why.

## Invocation

- **Terminal pane:** `claude` → `/dashboard-refresh`.
- **Button / headless:** `claude -p "Read Skills/dashboard-refresh/SKILL.md and execute it"`
  (cwd = vault root), wired to the obsidian-shellcommands "Refresh Dashboard" command.
