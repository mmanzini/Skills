---
name: atlas-up
description: One-shot Atlas morning routine — run the full dashboard refresh, verify every data file is freshly stamped and parseable, then run the Atlas ↔ GitHub sync including the agentic-knowledge-engine mirror, and report a single per-file/per-repo status table. Trigger on "/atlas-up", "atlas up", "morning routine", "refresh and sync atlas", "bring atlas up to date".
---

# Atlas Up

Replaces the daily `/dashboard-refresh` + `/sync-atlas` pair with one command,
and adds the verification step both were missing: **never report done on a
claim — report done on evidence** (stamps read back from disk, sync log parsed).

## Execution contract

A run has three phases, always in this order, none skippable:

1. **Refresh** — execute `Skills/dashboard-refresh/SKILL.md` in full (all
   resolvers in its Run order, all six `Dashboard/data/*.md` files).
2. **Verify** — prove the refresh landed (see below). A failed verification
   loops back to the failed resolver; it does not proceed to sync.
3. **Sync** — execute `Skills/sync-atlas/commands/sync-atlas.md` in full
   (pull, sync-all, parse log).

Do not touch the Tasks board. Write only inside `Dashboard/data/` (phase 1)
and whatever the sync scripts themselves touch (phase 3).

## Phase 2 — Verify (the point of this skill)

Run this check after the refresh; every file must show today's stamp AND
parse as valid YAML:

```bash
python3 - <<'EOF'
import yaml, glob, re, datetime, sys
today = datetime.date.today().isoformat()
fail = 0
for f in sorted(glob.glob("Dashboard/data/*.md")):
    raw = open(f).read()
    try:
        fm = yaml.safe_load(raw.split("---")[1])
        stamp = str(fm.get("updated") or fm.get("as_of") or "")[:10]
        ok = stamp == today
        print(f"{'OK ' if ok else 'STALE'}  {f}  stamp={stamp or 'none'}")
        fail += 0 if ok else 1
    except Exception as e:
        print(f"BROKEN {f}  yaml={e}")
        fail += 1
sys.exit(fail)
EOF
```

Rules:

- **STALE file** → re-run only that file's resolver from the dashboard-refresh
  Run order, then re-verify. Max two retries per file; after that, report the
  file as failed with the reason (source unavailable, script error) — an
  honestly-reported skip is fine, a silent stale file is not.
- **BROKEN file** → unquoted scalar per dashboard-refresh hard rule 6. Fix the
  offending line, re-verify.
- A resolver whose source is genuinely unavailable is exempt from the stamp
  check but must be named in the final report.

## Phase 3 — Sync, with mirror check

Run the sync per `Skills/sync-atlas/commands/sync-atlas.md` (no argument =
all repos). Then two extra checks the plain sync skips:

1. **Push confirmed** — for each repo the log claims synced, verify
   `git -C ~/Documents/repos/<repo> status -sb` shows no `ahead` marker.
2. **Engine mirror** — confirm `agentic-knowledge-engine` was included in the
   run and is not ahead/behind. If Atlas-side engine docs changed this session
   (anything under `Resources/projects/agentic-knowledge-engine/`), say so
   explicitly in the report so the mirror README/flowcharts don't silently
   drift.

## Final report

One table, nothing else, then a one-line verdict:

```
Dashboard  tasks OK · life OK · github-trends OK · ai-news OK · political-economy OK · upcoming OK
Sync       ai-engineering ✓ · skills ✓ · political-economy ✓ · github-trending-digest ✓ · agentic-knowledge-engine ✓
atlas-up: 6/6 fresh, 5/5 synced
```

Any STALE/BROKEN/unsynced item appears in the table with its reason. The
verdict line is derived from the verification output, never from memory of
what phase 1 "did".
