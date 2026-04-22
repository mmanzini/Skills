---
name: reverie
description: "Nexus-wide vault consolidation — short-term to long-term memory. Runs Intelligence consolidate+refine across all pseudo-RAG vaults, sweeps every top-level Nexus folder for recent signal, reconciles Context/memory.md and Context/about-me.md against that signal, handles conflicts, and logs the outcome. Use when the user says 'reverie', '/reverie', 'refresh Nexus', 'update memory', 'consolidate the vault', or asks for a full-vault reflective pass."
---

# Reverie: Nexus-wide consolidation

You are performing a reverie — a reflective pass over the entire Nexus vault. Intelligence vaults absorb their own short-term inputs (via their `consolidate`/`refine` verbs); you then sweep every top-level folder for activity and reconcile `Context/memory.md` and `Context/about-me.md` against what's actually true now.

This is distinct from the Anthropic `dream` skill, which only consolidates `~/.claude` memory files. Reverie is about the Obsidian vault.

## Arguments

| Invocation | Behaviour |
|---|---|
| `/reverie` | Full run: Intelligence consolidate+refine, folder sweep, reconcile, log. |
| `/reverie --dry-run` | Everything runs, but Phase 1 consolidates are skipped and all writes print a diff instead of applying. |

## Locate

The Nexus vault is the project root (where this skill lives). All paths in this document are relative to that root.

State file: `Context/reverie-log.md`. Read-point for `last_reverie_at` and append-point for each run's entry.

---

## Operating mode

Reverie is typically invoked unattended (nightly scheduled task at 21:00 local). Treat every run as non-interactive:

- Do not prompt the user, ask for confirmation, or stop to clarify.
- If a phase fails (consolidate errors, sweep agent crashes, a write is blocked), record the failure under `### Unresolved` in that run's reverie-log entry and continue with the remaining phases. One phase's failure must never abort the rest of the run.

---

## Phase 0 — Orient

1. Read `Context/memory.md` end-to-end. Note every `##` section heading and its current content — this is the baseline you'll diff against.
2. Read `Context/about-me.md`.
3. Read `Context/reverie-log.md` if it exists. The most recent entry's ISO timestamp is `last_reverie_at`. If the file does not exist, set `last_reverie_at` to 7 days ago.
4. `ls` the Nexus root. Every top-level folder is in scope for the sweep. Classify:
   - **Known-typed** (have specialized sweep prompts below): `Context/`, `Intelligence/`, `Projects/`, `Resources/`, `Daily/`, `Skills/`, `Tasks/`.
   - **Unknown** (anything else): use the generic unknown-folder probe.

Do NOT hard-code the folder list. Whatever `ls` returns is authoritative — a folder added next month must still be picked up.

---

## Phase 1 — Intelligence consolidate + refine

Skip entirely if `--dry-run`.

Otherwise, delegate to `Intelligence/CLAUDE.md` verbatim:

1. Spawn **3 parallel subagents** in a single message, one per pseudo-RAG vault (`tech-research/`, `political-economy/`, `github-trends/`). Each subagent enters its vault and runs `consolidate` per that vault's own `CLAUDE.md`. Pass the vault path and the instruction *"follow the Consolidating section of this folder's CLAUDE.md verbatim"*.
2. Wait for all three. Record which succeeded and which failed. A failed vault does NOT block the rest of the reverie — skip its refine and continue.
3. Spawn **3 parallel subagents** (minus any that failed) to run `refine` per each vault's CLAUDE.md → *Refining* section. Refines are read-only / suggestion-only.
4. Collect a per-vault summary: articles touched, source files cleared, refine findings.

Never re-implement consolidate or refine here. This phase is pure orchestration.

---

## Phase 2 — Folder sweep (parallel, folder-agnostic)

Spawn **one subagent per top-level folder** discovered in Phase 0, all in a single message for parallelism. Each subagent gets `last_reverie_at` and the contract *"return a ≤30-line structured report of what changed in this folder since `last_reverie_at`. Do not copy raw file content. Deltas only."*

Specialised prompts per folder type:

- **Context/** — check whether `memory.md`, `about-me.md`, `writing-rules.md`, or `CLAUDE.md` structure (section headings, not content) changed since `last_reverie_at`. Usually nothing; report `no change` if so.
- **Intelligence/** — for each pseudo-RAG vault, diff `_master-index.md` against its state at `last_reverie_at` (use git if available, otherwise just list what's there). Report topics added. Check free-form subfolders (`competitors/`, `decisions/`, `market/`, `processes/`, `transcriptions/`) — report any that now hold material (`memory.md` lists these only once populated).
- **Projects/** — for each project folder: does it still exist? has `CLAUDE.md`? any content modified since `last_reverie_at`? signs of archival (empty, `ARCHIVED` marker, no recent mtime)? If a project's CLAUDE.md grew a verb list (new slash-commands), report the full updated list.
- **Resources/** — each subfolder is a candidate (currently `frameworks/`, `prompts/`, `templates/`, `tools/`). Report adds/removes at depth 2. For `frameworks/`, also report per-framework CLAUDE.md presence and content changes.
- **Daily/** — read every `Daily/YYYY-MM-DD.md` with filename date newer than `last_reverie_at`. Extract from each: `### Decisions & agreements`, `### Model insights`, tool mentions (for about-me), working-style observations, and any line starting with "remember that" / "don't forget" / similar explicit retention asks. Aggregate across all daily notes — recurring themes are worth reporting once with a count, one-offs can be listed verbatim.
- **Skills/** — list every skill folder. Report any added since `last_reverie_at`. Note which have non-trivial `SKILL.md` content.
- **Tasks/** — list depth-1 content. Report recurring themes or structural changes.
- **Unknown folders** — report folder name, depth-1 contents (names only), and a ≤5-line summary of any `CLAUDE.md` or `README.md` found. Flag whether the folder has substantive content.

Each subagent returns a structured report, not prose. Main agent never holds raw daily notes or project files.

---

## Phase 3 — Reconcile `memory.md` (section-scalable)

`memory.md` sections are a living map over what exists in the vault, NOT a fixed schema. Walk the current file section by section, apply the rules below, and produce the updated file.

### Section lifecycle

- **Existing, still populated** — diff entries against the relevant sweep; update in place.
- **Existing, now empty** — remove the section header entirely. Don't leave an empty `##` with no items.
- **New top-level folder with substantive content** — propose a new `##` section. **Threshold** (any one is enough):
  - folder has a `CLAUDE.md`, OR
  - folder has ≥3 files with non-trivial content, OR
  - folder exposes verbs (slash-commands mentioned in a CLAUDE.md).
  - Below threshold → do NOT add a section. Record in the reverie log under `Watching:`.
- **Rename** — if an old folder name is in `memory.md` but a same-kind folder exists under a new name, rename in place (don't remove-then-add). Use CLAUDE.md content or obvious naming overlap as the hint.

Formatting for any new section must match the existing style in `memory.md`: wikilinks in the form `[[folder/CLAUDE|Display Name]]`, two-space indent for continuation lines, no bullet sub-structure.

### Per-section update rules

- **`## Projects`** — add new projects (with `(no CLAUDE.md yet)` marker if absent), rename, remove when gone, refresh the verb list when a project's CLAUDE.md grew.
- **`## Knowledge bases`** — update free-form subfolder entries only when they hold material. Don't invent verbs — only record verbs that actually exist in a vault's CLAUDE.md.
- **`## Frameworks`** — same rules as Projects, applied to `Resources/frameworks/*`.
- **`## Live decisions & watch-list`**:
  - **Add** new decisions from Daily `### Decisions & agreements`, timestamped `YYYY-MM-DD`, deduplicated against existing entries.
  - **Resolve** old items that have a matching "done" decision in a newer Daily note — remove them.
  - **Prune** items older than 30 days with no activity → remove from `memory.md` and record under `Archived:` in the reverie log entry.
- **`## Remember (user-asked)`** — only touch when Daily notes contain an explicit user retention ask ("remember that X", "don't forget Y"). Otherwise leave untouched. Never auto-prune.

### Sections you must NOT change

- `## How to use`
- `## Companion context files`

These are the rulebook. They don't derive from activity.

### First-run idempotent addition

If `memory.md` does NOT yet contain a `## Reverie` section, add this one-liner near the bottom (after `## Live decisions & watch-list`):

```markdown
## Reverie

Last run and history: [[Context/reverie-log|reverie-log]]. Run `/reverie` to refresh Nexus navigation, Intelligence vaults, and identity context.
```

Idempotent: if it's already there, leave it.

---

## Phase 4 — Reconcile `about-me.md`

Conservative. Only edit when Daily signal meets a clear threshold:

- **Tools I actually use** — add a tool when it's mentioned in ≥3 distinct Daily notes and isn't already listed. Remove a tool that hasn't appeared in any Daily note in the last 30 days (but only if confidence is high — "I stopped using X" beats absence alone).
- **Working style** — add a pattern only when the user explicitly confirmed it ("yes, keep doing that", "that's exactly right"). Absence of correction is not confirmation.
- **Day-one assumptions for any agent working with me** — same rule as Working style.
- **Domains of work** — add a new domain when it appears in ≥5 distinct Daily notes and has its own decisions/output, not just incidental mentions.

If nothing meets the bar, leave the file untouched and record "no change" in the reverie log.

**Never** edit:
- The Who-I-am section (identity-level, only changes on explicit user ask).
- Tone or voice (that's `writing-rules.md`'s domain).

---

## Phase 5 — Conflict rules

When signals disagree, resolve using this strict priority:

1. **Folder state beats `memory.md` claim.** If `memory.md` lists a project that no longer exists as a folder, remove it. (`Context/CLAUDE.md` already codifies this: "If `memory.md` conflicts with a live observation, trust what you observe.")
2. **Newer decision beats older.** A Daily from this week that contradicts a `## Live decisions` entry from last month replaces the entry. Note the supersession in the reverie log.
3. **Explicit user ask beats inference.** `## Remember (user-asked)` items are never auto-pruned or auto-edited.
4. **Unresolvable conflicts get flagged, not guessed.** Two Daily notes disagreeing, neither clearly newer or authoritative → leave both versions in place and record under `### Unresolved` in the reverie log entry for user review. Do NOT pick a side.

---

## Phase 6 — Write reverie log

Append a new entry at the top of `Context/reverie-log.md` (newest first). If the file doesn't exist, create it with a header:

```markdown
# Reverie log

Outcome of each `/reverie` run. Newest first. Trimmed to last 20.
```

Entry format (each entry ≤15 lines):

```markdown
## 2026-04-22T18:30 — reverie run
- Intelligence: tech-research +3 articles, political-economy +1, github-trends +2; 6 source files cleared. Refine flagged 2 missing cross-links.
- memory.md sections changed: [section names with one-word action, e.g. "Projects +1 -1, Frameworks +1, new section Skills"].
- memory.md Live decisions: +N added, -N resolved, -N archived.
- about-me.md: [one-line summary | no change].
- Watching: [sub-threshold candidates — folder names only].
- Archived (30-day rule): [decisions removed from watch-list].
- Superseded: [memory.md claims replaced by newer Daily decisions].
- Unresolved: [conflicts with both sides, user attention needed | none].
- Next cutoff: 2026-04-22
```

After appending, trim the file to the most recent 20 entries by truncating older ones from the bottom.

**Timestamp format**: ISO 8601 with minute precision in local time, e.g. `2026-04-22T18:30`. The next reverie reads this as `last_reverie_at`.

---

## Dry-run mode

When invoked with `--dry-run`:

- Skip Phase 1 entirely (no Intelligence consolidate/refine).
- Run Phase 0 and Phase 2 normally.
- In Phases 3–6, compute the intended changes but print a unified-diff-style preview of what would be written instead of writing. Preview format:

```
=== Context/memory.md ===
<diff>

=== Context/about-me.md ===
<diff | no change>

=== Context/reverie-log.md ===
<would prepend: [full entry]>
```

Then return the normal summary output with a `[DRY RUN — no changes applied]` banner.

---

## Output

Return this exact structure after a run:

```
## Reverie Complete — Nexus  [DRY RUN if applicable]

### Intelligence
- tech-research: [summary]
- political-economy: [summary]
- github-trends: [summary]

### memory.md
- [what changed, by section. Be specific: "Projects: added Experiments (has CLAUDE.md); removed Open Data apps investigation (folder gone)"]

### about-me.md
- [changed: <one-line summary> | no change]

### Watching
- [sub-threshold candidates for next run]

### Unresolved
- [conflicts needing user attention | none]
```

Keep it terse. The log file has the detail; this output is the scannable summary.

---

## Principles (lifted from `dream`)

- **Procedurally simple.** This is one SKILL.md file. No scripts, no templates.
- **Merge > duplicate.** Update existing entries rather than adding parallel ones.
- **Absolute dates only.** Convert every "yesterday" / "last week" / "a few days ago" to an ISO date before writing.
- **Bounded state.** `memory.md` stays scannable. `reverie-log.md` caps at 20 entries. Neither grows unbounded.
- **Folder-agnostic.** The sweep discovers folders dynamically. Never hard-code the folder list.
- **Delegate, don't re-implement.** Intelligence consolidate/refine lives in `Intelligence/CLAUDE.md`. Reverie orchestrates; vault CLAUDE.md files execute.

## What reverie does NOT touch

- `Context/writing-rules.md` — external constraint, not derived from activity.
- `~/.claude/projects/.../memory/` — that's the original `dream` skill's scope.
- `Daily/*.md` files — historical record, never deleted or edited.
- `## How to use` and `## Companion context files` sections of `memory.md` — rulebook, not activity-derived.
