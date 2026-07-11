---
name: propagate-engine
description: Propagate Atlas structural changes to the public agentic-knowledge-engine repo — run the Unison sync, then close the gaps Unison is configured to skip (README.md, terminology sweeps, essay/flowchart staleness), branch and push, and confirm nothing is left ahead of origin. Trigger on "/propagate-engine", "propagate to the engine", "update the engine repo", "sync the engine mirror", or after any change to CLAUDE.md, schema.md, vault verbs, memory tiers, or OKF structure.
---

# Propagate Engine

Atlas is the living system; `agentic-knowledge-engine` is its public
template/architecture repo. Unison syncs most files automatically, but it is
**deliberately configured to skip the most visible ones** — that gap is where
every "did you also update the mirror?" turn comes from. This skill closes it.

## Topology (fixed)

| Piece | Path |
|---|---|
| Atlas-side copy | `Resources/projects/agentic-knowledge-engine/` |
| Mirror repo (pushes to GitHub) | `~/Documents/repos/agentic-knowledge-engine/` |
| Sync script | `~/Documents/repos/scripts/sync-repo.sh agentic-knowledge-engine` |
| Unison profile | `~/.unison/agentic-knowledge-engine.prf` |

**Unison-ignored (never auto-synced):** `README.md`, `.claude/`, `.gitignore`,
`.gitattributes`. Anything the run changes in these files must be moved by
hand in phase 3.

## Phase 1 — Scope the change

Establish what structurally changed in Atlas since the mirror's last sync
commit:

```bash
LAST=$(git -C ~/Documents/repos/agentic-knowledge-engine log -1 --format=%cI)
git -C ~/Documents/Atlas log --since="$LAST" --name-only --format="%h %s" -- \
  CLAUDE.md schema.md Intelligence/_search Intelligence/index.md Skills | head -50
```

Plus whatever the user states directly ("we renamed X", "new verb Y").
Classify: **terminology rename** / **structure change** (zones, files, verbs)
/ **behaviour change** (rules, budgets). Trivial typo-level fixes exit early:
sync, commit to main, done.

## Phase 2 — Unison sync

```bash
git -C ~/Documents/repos/agentic-knowledge-engine pull --ff-only
~/Documents/repos/scripts/sync-repo.sh agentic-knowledge-engine
```

Read the tail of `~/Documents/repos/.sync.log`. Unison **skips conflicts**
(same file changed both sides) — any skipped path must be surfaced and
resolved in this run, not left for next time.

## Phase 3 — Close the Unison gaps (the point of this skill)

1. **README parity.** The mirror's `README.md` is the canonical GitHub-facing
   doc. Check it against the change scope from phase 1:
   - structure tree section matches the real engine template layout
     (`ls -R` the mirror, compare)
   - vocabulary matches current Atlas terms (bundle not bucket, index.md not
     _master-index.md, current zone names)
   - verbs/tiers/rules described match current `CLAUDE.md`/`schema.md`
   Update the mirror README, then copy it over the Atlas-side
   `Resources/projects/agentic-knowledge-engine/README.md` so the two stop
   drifting (Unison won't do it).
2. **Terminology sweep** (renames only). Grep the whole mirror for the old
   term, including `AGENTS.md`, `CLAUDE.md`, `schema.md`, template articles:
   ```bash
   grep -rn --exclude-dir=.git -i "<old-term>" ~/Documents/repos/agentic-knowledge-engine
   ```
   Zero hits required before phase 4 (precedent: bucket→bundle missed the
   README because it was Unison-ignored).
3. **Essay + flowcharts staleness.** Grep the changed concepts in
   `Resources/Projects/articles-and-essays/004-the-agentic-knowledge-engine/`
   (essay + `img/*.excalidraw.md` text labels). Fix stale text labels
   directly; if a diagram's *shape* is now wrong, do not redraw — list it in
   the report as a manual follow-up.

## Phase 4 — Publish

- **Structural/behaviour change** → new branch in the mirror
  (`<change-slug>`), commit, push branch (precedent: `okf-alignment`).
  Per vault Git rules, if a PR is opened, squash-merge immediately.
- **Terminology/docs-only** → commit straight to `main`, push.

Commit messages: concise, `docs:`/`sync:` prefix, state what propagated.

## Phase 5 — Verify + report

```bash
git -C ~/Documents/repos/agentic-knowledge-engine status -sb
```

No `ahead` marker, no uncommitted files. Then one table:

```
Unison        synced ✓ (0 conflicts skipped)
README        mirror updated ✓ · Atlas copy refreshed ✓
Term sweep    "<old-term>" 0 hits
Essay/img     essay OK · engine-okf-bundle.excalidraw flagged (shape stale)
Publish       main pushed ✓ (or branch <name> pushed ✓)
```

Verdict derived from command output, never from memory of the edits.
