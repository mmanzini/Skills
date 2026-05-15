# Output Skill Scaffold

Parameterized templates for every file the generated skill needs. Fill placeholders (`{LIKE_THIS}`) with values from Phase 1 / 1.5 / 4 of the interview.

Placeholders used throughout:
- `{SKILL_NAME}` — human-readable, e.g. "LinkedIn Carousel Builder"
- `{SLUG}` — kebab-case, e.g. `linkedin-carousel-builder`
- `{ASSET_TYPE}` — singular noun, e.g. "carousel", "slide deck", "one-pager"
- `{ASSET_TYPE_PLURAL}` — plural form, e.g. "carousels", "slide decks"
- `{AUDIENCE}` — one sentence, e.g. "Founders evaluating B2B SaaS tools"
- `{INPUT_TYPES}` — list, e.g. "outline, script, article, brief, transcript"
- `{LAYOUT_COUNT}` — integer, e.g. 27
- `{CATEGORIES}` — emergent list from Phase 4, e.g. "Cards, Hierarchy, Process"
- `{SKIP_RULES}` — asset-specific skip rules from Phase 1
- `{LAYOUTS}` — full layout-by-layout structured data from Phase 4
- `{BRAND_*}` — placeholders for brand fields from Phase 1.5

When a placeholder doesn't apply (e.g. an asset type with no skip rules), omit the section entirely rather than leaving a placeholder string.

---

## SCAFFOLD: SKILL.md (the generated skill's main file)

```markdown
---
name: {SLUG}
description: Plan and produce {ASSET_TYPE_PLURAL} for {AUDIENCE}, using a fixed library of {LAYOUT_COUNT} layouts from a design template. Walks through any input ({INPUT_TYPES}) section by section, proposes 2-4 layout options per section with full copy + icons, gets user confirmation, then compiles a master Markdown file the user pastes into the design tool to render the finished {ASSET_TYPE}. Use whenever the user wants to produce a {ASSET_TYPE} from {INPUT_TYPES}, or mentions "{ASSET_TYPE}", "plan {ASSET_TYPE_PLURAL}", "draft a {ASSET_TYPE}".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# {SKILL_NAME}

You plan and produce {ASSET_TYPE_PLURAL} using a library of {LAYOUT_COUNT} proven layouts from the user's design template. Your output is a master Markdown spec that defines each section's layout, copy, and icons. The user pastes the spec into the design tool to render the finished {ASSET_TYPE}.

## Before you start (mandatory, every conversation)

Before producing your first response, read every reference file. Skip this and you will pick the wrong layout or write copy that doesn't fit the slot.

In this order:

1. Read `references/layout-templates.md` — the index and slot schema for all {LAYOUT_COUNT} layouts.
2. Read `references/plot.md` — the decision guide. Cross-reference matrix + per-layout "when to pick it" + picking heuristic.
3. Read `references/brand.md` and `references/icons.md`.
4. Open and visually scan every PNG in `assets/templates/`. All {LAYOUT_COUNT} files. Build visual vocabulary.
5. Scan `copy-examples/` if present. Calibrate tone and density.

## Output format

One format only: a master Markdown spec. The user pastes it into the design tool, which renders the {ASSET_TYPE}. You do not generate rendered visuals.

Always cite layouts by **number + name** (e.g. "Layout 12 (...)"). The number is the stable identifier from the user's design template; the downstream agent uses it to look up the layout.

## Layout library

All layouts live in this skill. Categories:

{CATEGORIES_TABLE}

Full slot schemas in `references/layout-templates.md`. Decision guide in `references/plot.md`.

## Core rules

1. **Never repeat a layout across one {ASSET_TYPE}.** Track locked layout IDs and exclude them from later options. Variety is the point.
2. **Propose 2-4 options per section.** Different layouts, ideally from different categories. Each option includes full copy + icons. Mark one as the top pick.
3. **Always cite layout ID + name.**
4. **Always include icons or emojis** per the rules in `references/layout-templates.md`. Never propose copy-only.
5. **Never generate without explicit confirmation.** Wait for the user to lock each section.
6. **Iterate section by section.** No batching unless the user explicitly asks.
{SKIP_RULES_BLOCK}
8. **No em dashes.** Use periods, commas, colons, or restructure.
9. **Read the layout PNG and slot schema before committing copy.** Slot shape dictates what fits.
10. **Copy brevity is aggressive.** See brevity budgets in `references/layout-templates.md` and tone calibration in `copy-examples/`.

## Workflow

### Step 0 — Understand the input

Accept any of: {INPUT_TYPES}. Identify which sections / pieces need a layout. {SKIP_GUIDANCE}

If a slug isn't obvious, ask the user for one. The slug becomes the output filename.

### Step 1 — Plan the section count

Decide how many {ASSET_TYPE} sections the input becomes. Default 1:1 mapping. Split when a section contains distinct items each deserving its own visual. Don't split for density alone.

Announce the plan and wait for confirmation.

### Step 2 — Per section, propose 2-4 options

For each section:

1. Re-read the input for this section. Decide the content shape.
2. Use `references/plot.md` decision guide to shortlist 2-4 layouts from different categories.
3. Re-open and visually analyze each candidate PNG.
4. Exclude already-locked layouts.
5. Present options. Format:

```
**Option A — Layout {id} ({name}) · {category}**
Angle: {framing}
Why this fits: {one sentence}.

Copy:
- Headline: "{text}" (highlight: "{word}")
- {slot 1}: {icon or emoji} "{title}" / "{description}"
- ...

{Icon hints if layout has icon slots, emoji per item if emoji-friendly.}
```

Mark a top pick. Ask:

> Pick A / B / C / D, edit (e.g. "B, drop card 3"), regenerate an option, or want a 4th angle?

After lock:

> Locked Section {N} of {total}. Layout {id}, angle: {angle}. Moving to Section {N+1}.

### Step 3 — Compile the master MD

When every section is locked, compile a single MD with:

- YAML frontmatter (asset, slug, sections, generated date)
- Title + one-line description + skipped-section notes
- Structure table (section → layout → category)
- Per-section spec block: Layout ID + name + category + angle + count + slot-filled copy + icon/emoji notes + optional notes for the design tool

Sanity-check before saving: every layout ID is unique, every required slot is filled, no em dashes, brevity budgets respected.

### Step 4 — Save

Always to `~/Downloads/{slug}-{ASSET_TYPE}-{timestamp}.md`. Also to the user's vault if they've given a path.

> Saved to {path}. Paste into the design tool — it has the layout library keyed by ID.

### Step 5 — Iterate

After saving, ask for feedback. Small edits update the file directly. Layout swaps go back to Step 2 for that section.

## Voice

{VOICE_BLOCK}

## Brevity budgets

Filled per layout in `references/layout-templates.md`. General rule: short fragments redundant with voiceover or surrounding context improve retention. Full sentences create a competing read.

## What to skip

{SKIP_DETAILS}

## When no layout fits

If a section genuinely doesn't fit any of the {LAYOUT_COUNT} layouts:

1. Explain why none fits.
2. Suggest the closest layout and what'd need to change.
3. Ask the user whether to force-fit or drop the section.

## Reference files

| File | Contains |
|------|----------|
| `references/layout-templates.md` | Index + slot schemas. Read before committing copy. |
| `references/plot.md` | Decision guide. Read when shortlisting options. |
| `references/brand.md` | Colors, typography, design rules. |
| `references/icons.md` | Emoji palette + concept→icon lookup. |
| `assets/templates/{category}/{id}-{slug}.png` | PNG previews. Visually analyze every candidate. |
| `copy-examples/` | Reference content samples. Scan for tone calibration. |
```

---

## SCAFFOLD: references/layout-templates.md

```markdown
# Layout Reference

The {LAYOUT_COUNT} layouts available, organized by category. Use this as the fast-scan slot schema. Visual reference at `assets/templates/{category}/{id}-{slug}.png`.

Cite layouts by **number + name** (e.g. "Layout 12 ({name})"). The number ties back to the design template ID.

## Slot vocabulary

- `headline` — a short framing line, often with a highlighted word (the punchline).
- `h3` / `card title` — a phrase, not a sentence.
- `p` / `body` — a fragment or short sentence.
- `stat` — a very short figure.
- `eyebrow` — a micro-label.
- `axis` — extreme labels on a matrix.
- `col-head` — a column header.

Brevity budgets vary per layout — see each layout entry below.

## Icon and emoji support

| Mode | Layouts |
|------|---------|
| Icon slots (provide semantic hints, no emoji) | {ICON_SLOT_LAYOUTS} |
| Emoji-friendly (one emoji per item in title) | {EMOJI_FRIENDLY_LAYOUTS} |
| Neutral (use emoji only when it reinforces concept) | {NEUTRAL_LAYOUTS} |

---

{FOR_EACH_CATEGORY}
## {CATEGORY_NUM}. {CATEGORY_NAME}

{CATEGORY_DESCRIPTION}

{FOR_EACH_LAYOUT_IN_CATEGORY}
### {ID} {NAME}

- **PNG:** `assets/templates/{CATEGORY_FOLDER}/{ID}-{SLUG}.png`
- **Count:** {COUNT_RANGE}
- **Slots:**
{SLOT_LIST_WITH_BUDGETS}
- **Icon/emoji mode:** {MODE}
- **Best for:** {BEST_FOR_SENTENCE}
- **Pick over {SIMILAR_LAYOUT_ID} when:** {DIFFERENTIATION}
{END_FOR_EACH_LAYOUT}

---
{END_FOR_EACH_CATEGORY}

## Quick reference: count

{COUNT_TABLE}
```

---

## SCAFFOLD: references/plot.md

```markdown
# Decision Guide & Cross-Reference Matrix

The full guide for picking layouts across all {LAYOUT_COUNT}. Use it as the primary lookup when shortlisting 2-4 options. `references/layout-templates.md` has slot-level schemas; this file is about *which layout to reach for given the content shape and message*.

## Brand reference

See `brand.md` for colors, typography, voice, and forbidden language. All copy and the design tool output respects those rules.

## How this is organized

1. **Visual structure** — the layout's shape (what it looks like)
2. **Communicative purpose** — the message the viewer takes away (what it says)

The folder structure groups by visual category. Each layout has a distinct communicative purpose.

## Folder structure

```
assets/templates/
{FOLDER_TREE}
```

Filenames: `{id}-{slug}.png`. The ID is the stable identifier from the user's design template.

---

{FOR_EACH_CATEGORY}
## {CATEGORY_NUM}. {CATEGORY_NAME}

**What this category communicates:** {CATEGORY_PURPOSE}

**Signals in the input that point here:**
{CATEGORY_SIGNALS}

**Avoid when:** {CATEGORY_AVOID}

### When to pick which

| Layout | Best for |
|--------|----------|
{LAYOUT_BEST_FOR_TABLE}

---
{END_FOR_EACH_CATEGORY}

## Cross-reference matrix: communicative purpose × visual category

{CROSS_REFERENCE_MATRIX}

## Quick decision guide: "Which layout do I pick?"

| You want to say... | Top pick | Close second |
|--------------------|----------|--------------|
{DECISION_GUIDE_TABLE}

---

## Picking heuristic when proposing 2-4 options

1. **Different categories first.** Each option should be a different layout, ideally from different categories. Two options from the same category limits creative range.
2. **Match density.** 2-3 items → fixed-small layouts. 4-6 items → flex-mid layouts. 7+ items → split into multiple sections.
3. **Match section position to layout energy.** {OPENING_LAYOUT_NOTES} for openers, {MIDDLE_LAYOUT_NOTES} mid, {CLOSING_LAYOUT_NOTES} for closers.
4. **Enforce uniqueness.** Never repeat a layout in one {ASSET_TYPE}. Track and exclude.
5. **Mark one option as top pick** based on content signals.
```

---

## SCAFFOLD: references/brand.md

Use the populated content from Phase 1.5 directly. The shape is documented in `brand-intake.md` "What goes into the generated brand.md".

---

## SCAFFOLD: references/icons.md

Default starter palette. The user can layer their brand-specific iconography on top.

```markdown
# Icon Reference

Unicode emoji palette for {ASSET_TYPE_PLURAL}. Use these inline in title slots for emoji-friendly layouts. Use semantic hints (e.g. "cloud / moon for always-on") for icon-slot layouts — the downstream rendering picks the actual icon from the hint.

## How to use

- **Always include icons or emojis in proposals.** Never propose copy-only.
- **Place inline** with the title text, prefixed with two spaces after the emoji for breathing room: `"⚡  Real-time"`.
- **One per item.** Multiple icons per item clutters.
- **Skip** only when the user explicitly says no icons.

## Rendering notes

- Single-glyph emoji render reliably.
- Avoid compound (ZWJ) emoji and skin-tone variants — they break in some fonts.

## Curated palette

### Events & Triggers
⚡ 🔔 🚨 🎯 🎬 ▶️ 🚦 🔑 🛎️ 💥

### Time & Schedule
⏰ ⏱️ ⏳ 📅 🗓️ 🌙 🌅 🕐

### Infrastructure & Cloud
☁️ 🖥️ 💻 🗄️ 🔌 🔗 🌐 📡 🛰️ 🏢

### AI & Reasoning
🧠 🤖 ✨ 💡 🧩 🔮 🎛️

### Execution & Tools
⚙️ 🔧 🛠️ 🔨 🧰 🪛 🔩

### Communication
💬 📨 📧 ✉️ 📮 💭 📢 🔊

### Documents & Logs
📋 📝 📄 📃 📜 🗂️ 📁 📂

### People & Teams
👤 👥 🤝 🫂

### Velocity & Growth
🚀 📈 📊 ⬆️ ↗️ 💹

### Money & Billing
💰 💵 💳 🧾 💸

### Security & Access
🔒 🔓 🛡️ 🗝️ 🔐

### Warnings & Limits
⚠️ 🚫 ❌ 🛑 ⛔

### Success & Positive
✅ ☑️ ✔️ 🎉 🏆 🌟

### Flow & Cycles
🔁 🔄 ♻️ 🔃 ➰

### Structure
🧱 📦 🏗️ 🪜

### Observability
🔍 👁️ 🕵️ 📍

## Concept → icon lookup

| Concept | Options |
|---------|---------|
| Trigger / event | 🔔 ⚡ 🚦 🎬 |
| Cloud / remote | ☁️ 🛰️ 🌐 |
| Local / device | 💻 🖥️ |
| AI / reasoning | 🧠 🤖 ✨ |
| Execution / tool | ⚙️ 🛠️ 🔧 |
| Document / record | 📋 📝 📜 |
| Connector / integration | 🔌 🔗 📡 |
| Team / collaboration | 👥 🤝 |
| Individual user | 👤 |
| Money / cost | 💰 💳 🧾 |
| Limit / blocked | 🚫 ⛔ ⚠️ |
| Loop / cycle | 🔁 🔄 🌀 |
| Monitoring | 🔍 👁️ 📊 |
| Success | ✅ 🎉 |
| Failure | ❌ 🛑 |
| Time / schedule | ⏰ 📅 🌙 |

{BRAND_SPECIFIC_ICONS_BLOCK}
```

If the user mentioned brand-specific iconography in Phase 1.5 (e.g. "we always use a star for premium"), append a "Brand-specific overrides" section to the bottom.

---

## How to fill these scaffolds at generation time

1. Walk Phase 4 layout-by-layout records. For each layout, fill the layout-templates.md and plot.md entries.
2. From the per-layout records, derive the icon-slot / emoji-friendly / neutral lists for the icon-mode table.
3. From the categories list, build the category sections in plot.md.
4. From Phase 1 input types, fill the SKILL.md description and Step 0 input handling.
5. From Phase 1 skip rules, fill the {SKIP_RULES_BLOCK}, {SKIP_GUIDANCE}, {SKIP_DETAILS} placeholders. If the user gave no skip rules, omit those sections entirely (don't leave placeholders).
6. From Phase 1.5 brand intake, fill brand.md.
7. From Phase 1's voice rules, fill {VOICE_BLOCK}.
8. From asset type, decide which energy maps to which category for the picking heuristic.
9. Validate every {PLACEHOLDER} is replaced before saving. Search the generated files for `{` to confirm.
