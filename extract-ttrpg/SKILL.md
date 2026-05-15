---
name: extract-ttrpg
description: >
  Extract and document a TTRPG system from one or more PDFs. Reads the PDFs,
  identifies the game system's mechanics, and produces structured Obsidian markdown
  documentation under Resources/ttrpg-systems/<System Name>/<Version>/.
  Use when the user passes one or more PDF paths pointing to a tabletop RPG rulebook.
argument-hint: "<pdf-path> [pdf-path...] [--system 'Name'] [--version 'V X.Y']"
---

# Extract TTRPG

Read one or more TTRPG PDFs and produce a structured, Obsidian-compatible documentation set capturing all game mechanics, character options, GM tools, and supplementary material.

## Phase 1: Parse Arguments

Extract from `$ARGUMENTS`:

1. **PDF paths** — every argument that ends in `.pdf` or is a quoted path containing `.pdf`
2. **`--system`** flag — optional system name (e.g., `--system 'Moxie'`). If absent, infer from the first PDF's filename or ask the user.
3. **`--version`** flag — optional version string (e.g., `--version 'V 1.4'`). If absent, infer from filename or ask the user.

Validate each PDF exists:
```bash
ls -la "<pdf-path>"
```

If any PDF is missing, report and stop.

Determine the **vault root** by walking upward from the current working directory until you find `schema.md` alongside `Intelligence/`. The target output folder is:

```
<vault-root>/Resources/ttrpg-systems/<System Name>/<Version>/
```

If the vault root can't be found, use the current working directory as the base.

## Phase 2: Read & Analyze PDFs

Read every PDF **completely** — no skipping. TTRPG content is spread unpredictably across pages.

### Reading Strategy

1. Check total page count (attempt reading page 1 to see the PDF metadata)
2. Read in batches of **20 pages** using the Read tool with the `pages` parameter
3. For each batch, extract structured notes covering:

| Extraction Target | What to look for |
|---|---|
| **Core resolution** | Dice mechanic, success/failure thresholds, outcome tiers, modifiers |
| **Stats / attributes** | Names, scales, how they feed into rolls |
| **Character creation** | Steps, choices, starting values, backgrounds/origins |
| **Character advancement** | XP, leveling, milestones, what you gain per level |
| **Character options** | Classes, paths, playbooks, archetypes — their abilities and talents |
| **Combat** | Initiative, actions, damage, health, death/incapacitation, tactical options |
| **Magic / powers** | Spellcasting system, spell lists or freeform rules, resource costs |
| **GM tools** | GM-facing moves, procedures, difficulty setting, encounter building |
| **Exploration** | Travel, mapping, resource management during travel |
| **Social mechanics** | Formalized social systems (not just "roll Charisma") |
| **Bestiary** | Monster/enemy entries, stat block format, creature categories |
| **Equipment / treasure** | Gear lists, weapon stats, armor, magical items, economy |
| **Setting material** | Worldbuilding, factions, geography, history embedded in rules |
| **Adventures / scenarios** | Pre-built scenarios, adventure starters, campaign frameworks |
| **Solo play** | Solo-specific rules or adaptations |
| **Supplementary** | Random tables, character sheets, designer notes, variant rules |

Keep notes **in working memory** — do not write intermediate files.

### Multiple PDFs

If multiple PDFs are provided, read them sequentially and merge their content into a single unified picture. Treat them as chapters/supplements of the same system.

## Phase 3: Design Structure

From the extracted notes, determine which **categories** have enough material to warrant their own subfolder. Every system is different — do not force a category that has no content, and do not omit one that does.

### Standard Category Candidates

| Category Folder | Include When |
|---|---|
| `Core Mechanics/` | Always — every TTRPG has a resolution mechanic |
| `Characters/` | Always — stats, creation, advancement |
| `Character Options/` | Classes, paths, playbooks, or archetypes exist with distinct abilities |
| `Combat/` | Combat has its own subsystem beyond core resolution |
| `Magic/` | Spellcasting or supernatural abilities have formalized rules |
| `GM Toolkit/` | GM-facing tools, moves, procedures, or encounter-building rules |
| `Exploration/` | Travel or exploration has its own mechanical subsystem |
| `Social/` | Social mechanics are formalized (not just a skill check) |
| `Bestiary/` | Monster or enemy entries are documented |
| `Equipment/` | Gear, weapons, armor, or treasure have mechanical weight |
| `Setting/` | Worldbuilding is embedded alongside the rules |
| `Adventures/` | Pre-built scenarios or campaign frameworks are included |
| `Solo Play/` | Solo-specific rules or adaptations exist |
| `Supplementary/` | Random tables, variant rules, designer notes worth preserving |

### File Planning

For each included category, determine the specific files needed. Each file should cover one coherent mechanical subsystem. Guidelines:

- **1 file per distinct subsystem** (e.g., "Core Resolution" is one file, "Damage and Health" is another)
- **Split by function, not by chapter** — reorganize the PDF's structure into mechanical groupings
- **Group character options** — if there are many classes/paths, split into logical groups (martial vs. magic, etc.) rather than one file per class
- **Each file should be 100-400 lines** — split if larger, merge if too thin

### User Approval Gate

**Before writing any files, present the proposed structure to the user:**

```
Proposed structure for <System Name> <Version>:

<System Name>.md (overview + index)

Core Mechanics/
  - Core Resolution.md — <one-line summary>
  - <other files>

Characters/
  - <files>

...

Total: N files across M categories.

Proceed?
```

Wait for user approval. Adjust if they request changes.

## Phase 4: Write Files

### Create Folder Structure

```bash
mkdir -p "<target>/<Category>/" # for each category
```

### Write Overview File

Write `<System Name>.md` in the root of the target folder. This is the entry point. Follow this pattern:

```markdown
# <System Name> (<Version>)

<1-2 paragraph system summary: what kind of game, core mechanic in one sentence, design philosophy>

## Core Principles

<3-5 bullet points capturing the system's identity>

## System Files

### <Category Name>
- [[<File Name>]] — <one-line description>
- ...

### <Next Category>
- ...

## Source

<PDF filename(s), author(s), publisher, license if known>
```

**Reference exemplar:** Read `Resources/ttrpg-systems/Grimwild V 1.4/Moxie System.md` to match the exact style and structure.

### Write Content Files

For each file in the approved structure, write it following these conventions:

**Format:**
- **H1** = file title (matches filename without `.md`)
- **H2** = major sections
- **H3** = subsections
- **Tables** for structured data (outcome tables, stat scales, tier comparisons, item lists)
- **Blockquote examples** using `> **Example:**` format
- **Cross-references** as `[[wiki links]]` to other files in the same system (Obsidian resolves by filename)
- **`## See Also`** section at the bottom with links to related files
- **No comments about the extraction process** — write as if documenting the system directly

**Content rules:**
- **Mechanical precision.** Dice formulas, probability interactions, edge cases, and exception handling all matter. Get them right.
- **Concise.** Describe mechanics, not flavor text. Include flavor only when it's mechanically relevant (e.g., a class's narrative identity shapes what abilities it gets).
- **Tables over prose** for structured data. A table of outcomes is better than a paragraph describing them.
- **Examples for complex mechanics.** If a rule has non-obvious interactions, show a worked example.
- **Wiki links for cross-references.** When one mechanic references another, link to it.

**Reference exemplar:** Read `Resources/ttrpg-systems/Grimwild V 1.4/Core Mechanics/Core Resolution.md` to match the exact style and depth.

### Writing Order

1. Overview file first (establishes the index)
2. Core mechanics (referenced by everything else)
3. Characters (referenced by options and combat)
4. Remaining categories in any order — parallelize with subagents if possible

## Phase 5: Verify

After all files are written:

1. **Count files:**
```bash
find "<target>" -name "*.md" | wc -l
```

2. **Check wiki links resolve:**
```bash
cd "<target>" && grep -rohP '\[\[([^\]|#]+)' **/*.md *.md | sed 's/\[\[//' | sort -u | while read link; do
  if ! find . -name "${link}.md" | grep -q .; then echo "BROKEN: $link"; fi
done
```

3. **Check no empty files:**
```bash
find "<target>" -name "*.md" -empty
```

If any issues, fix them before reporting.

## Phase 6: Report

Output a completion summary:

```
TTRPG extraction complete.

System: <Name> <Version>
Location: Resources/ttrpg-systems/<Name>/<Version>/
Files: N files across M categories
Source: <PDF filename(s)>

Categories:
  Core Mechanics     — 4 files
  Characters         — 3 files
  ...
```

## Key Rules

1. **Read all pages.** Don't skip or skim. TTRPG content can appear anywhere.
2. **Categories are data-driven.** Include what exists. Omit what doesn't. Never force a template.
3. **Preserve mechanical precision.** Dice formulas, modifiers, probability curves, and edge cases matter more in TTRPG docs than in most domains.
4. **Attribution.** Note the source PDF, author, publisher, and license in the overview file's Source section.
5. **Wiki links stay within the system.** No cross-system links.
6. **Ask before writing.** Always present the proposed structure and wait for user approval before Phase 4.
7. **Multiple PDFs = one system.** Merge into a unified documentation set.
8. **No intermediate files.** Keep analysis in working memory. Only write final output.
9. **Obsidian compatibility.** Filenames with spaces are fine. Use `[[wiki links]]` not `[markdown](links)` for cross-references. No frontmatter needed on content files.
