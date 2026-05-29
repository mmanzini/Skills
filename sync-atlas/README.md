# Sync Atlas Plugin

Trigger the Atlas ↔ GitHub bidirectional sync and get a per-repo status report.

## Commands

- `/sync-atlas` — sync all five repos and report results
- `/sync-atlas <repo-name>` — sync a single repo (e.g. `/sync-atlas ai-engineering`)

## Repos synced

| Repo | Atlas path | Direction |
|------|-----------|-----------|
| `ai-engineering` | `Intelligence/ai-engineering/` | outbound |
| `political-economy` | `Intelligence/political-economy/` | outbound |
| `github-trending-digest` | `Resources/github-trends/` | inbound |
| `skills` | `Skills/` | mirror |
| `agentic-knowledge-engine` | `Resources/projects/agentic-knowledge-engine/` | outbound |

## What the sync does

Each repo run: `git pull` both sides → Unison bidirectional sync → `git commit + push` if the public clone changed. Atlas-side commits are handled by Obsidian Git separately.

Conflicts (same file edited on both sides) are skipped and logged — never silently overwritten. Resolve with `-prefer` flag as shown in the conflict hint.

## Version History

- **1.0.0** — Initial release. Runs sync-all.sh or sync-repo.sh, parses log, reports per-repo status table with conflict resolution hints.
