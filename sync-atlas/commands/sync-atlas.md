---
description: Trigger Atlas ↔ GitHub sync and report per-repo status
argument-hint: "[repo-name]"
---

# Atlas Sync

Trigger the Atlas ↔ GitHub bidirectional sync and report results.

## Repos

The five configured repos and their Atlas paths:

| Repo | Atlas path |
|------|-----------|
| `ai-engineering` | `Intelligence/ai-engineering/` |
| `political-economy` | `Intelligence/political-economy/` |
| `github-trending-digest` | `Resources/github-trends/` |
| `skills` | `Skills/` |
| `agentic-persistent-knowledge-management-system` | `Resources/projects/agentic-persistent-knowledge-management-system/` |

## Workflow

### 0. Pull latest from GitHub

Pull the latest from each configured repo before syncing so local clones are up to date:

```bash
for repo in ai-engineering skills political-economy github-trending-digest agentic-persistent-knowledge-management-system; do
  git -C ~/Documents/repos/$repo pull --ff-only
done
```

If any repo fails to fast-forward (diverged history), surface the error and stop before proceeding with the sync.

### 1. Determine scope

If the user passed an argument (`$ARGUMENTS`), run only that repo:
```bash
~/Documents/repos/scripts/sync-repo.sh <repo-name>
```

If no argument, run all repos:
```bash
~/Documents/repos/scripts/sync-all.sh
```

Always capture stdout+stderr.

### 2. Parse results from the log

After the script finishes, read the last 60 lines of `~/Documents/repos/.sync.log` and extract rows that belong to this run (timestamp within the last 2 minutes). For each repo, determine its outcome:

- **clean** — log contains `unison: clean` and `done`
- **conflicts** — log contains `unison: some files skipped` (sync still succeeded; files were skipped due to both-sides edits)
- **pushed** — log contains `pushed` (the public GitHub repo received new content)
- **unchanged** — log contains `unchanged`
- **failed** — log contains `FAIL` or `failed rc=` — capture the reason

### 3. Report

Output a compact table:

```
Atlas sync — <timestamp>

Repo                                         Status       Detail
ai-engineering                               ✓ clean      —
political-economy                            ✓ clean      —
github-trending-digest                       ⚠ conflicts  1 file skipped
skills                                       ✓ pushed     3 files → GitHub
agentic-persistent-knowledge-management-..  ✓ clean      —

Overall: 4 clean · 1 conflict · 0 failed
```

Status icons:
- `✓` — clean or pushed (success)
- `⚠` — conflicts present (sync ran but some files were skipped)
- `✗` — failed (script exited with error)

If any repo failed, append the raw log lines for that repo under the table so the user can diagnose.

### 4. Push changes to GitHub

After the sync, check each repo for uncommitted or unpushed changes and push:

```bash
for repo in ai-engineering skills political-economy github-trending-digest agentic-persistent-knowledge-management-system; do
  repo_path=~/Documents/repos/$repo
  if [[ -n "$(git -C $repo_path status --porcelain | grep -v '.DS_Store')" ]]; then
    git -C $repo_path add -A ':!*.DS_Store'
    git -C $repo_path commit -m "sync: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
    git -C $repo_path push
  fi
done
```

Note: The sync script already handles push automatically for most cases — this step catches anything left unstaged.

### 5. Conflict resolution hint

If any repo has conflicts, append:

```
Conflict resolution:
  prefer Atlas:  unison <repo> -prefer ~/Documents/Atlas/<atlas-path>
  prefer GitHub: unison <repo> -prefer ~/Documents/repos/<repo>

Exception — github-trending-digest syncs only the trending/ subfolder of the repo:
  prefer Atlas:  unison github-trending-digest -prefer ~/Documents/Atlas/Resources/github-trends
  prefer GitHub: unison github-trending-digest -prefer ~/Documents/repos/github-trending-digest/trending
```

## Important rules

- Run the script as-is — do not modify or re-implement the sync logic
- Never push to Atlas git directly; the script leaves that to Obsidian Git
- If the script itself fails to execute (permission error), remind the user to run:
  `xattr -d com.apple.quarantine ~/Documents/repos/scripts/sync-all.sh ~/Documents/repos/scripts/sync-repo.sh`
