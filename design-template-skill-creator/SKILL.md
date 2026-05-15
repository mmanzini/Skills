---
name: design-template-skill-creator
description: Build a custom skill that turns a numbered-page PDF design template into a section-by-section content generator. The user supplies the PDF plus answers about asset type, brand, voice, audience, and typical inputs. This skill converts each template page to a high-resolution PNG, captures per-layout meaning, and generates a complete skill folder (SKILL.md, references, assets). The generated skill walks any input (outline, script, article, website, brief, transcript) section by section and produces a master Markdown handoff that pastes directly into the design tool to render the finished asset. Use when the user says "create a skill from a design template", "build me a skill for slide decks / one-pagers / LinkedIn carousels / thumbnails / ad creatives", "automate generating {asset type} from my template", or "I have a design template, help me wrap a skill around it".
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# Design Template Skill Creator

You build custom skills that wrap around a user's design template. The user supplies the template as a numbered-page PDF; you interview them, convert pages to PNGs, capture per-layout meaning, and generate a complete skill folder. The generated skill drives a section-by-section content workflow that ends in a master Markdown handoff for the design tool.

This is a meta-skill. Its output is another skill.

## Before you start (mandatory, every conversation)

Before producing your first response, read every reference file in this folder. Do not skip — your interview quality depends on it.

In this order:

1. **`references/interview-questions.md`** — the question bank. You'll draw from it across phases 1, 2, 4.
2. **`references/pdf-pipeline.md`** — how to walk the user through exporting their design template as a numbered PDF, then how you convert each page to a high-resolution PNG.
3. **`references/brand-intake.md`** — three modes for capturing brand identity (interview, pasted brand doc, scraped URL).
4. **`references/output-skill-scaffold.md`** — the parameterized scaffolds for SKILL.md, plot.md, layout-templates.md, brand.md, icons.md that you'll fill out at generation time.
5. **`references/verification.md`** — the post-generation sanity check.

Only after reading all five do you produce your first response.

## What this skill produces

A folder at `~/Downloads/{user-chosen-slug}/` containing:

```
{user-chosen-slug}/
├── SKILL.md
├── assets/
│   └── templates/
│       ├── {category-1}/    {page-num}-{slug}.png ...
│       ├── {category-2}/    ...
│       └── ...
├── copy-examples/    (optional, if user provided reference content samples)
└── references/
    ├── layout-templates.md
    ├── plot.md
    ├── brand.md
    └── icons.md
```

The generated skill's job: take any input the user feeds it (outline / script / article / website / brief / call notes / image), walk section by section through that input, propose 2-4 layout options per section with full copy + icons, get user confirmation on every section, then compile a master Markdown file the user pastes into the design tool.

The generated skill **always outputs a master MD** — that's the universal handoff for the design tool across every asset type.

## Core rules for the meta-skill

1. **The design template must already exist.** The first thing you do — before any other interview question — is gate on this. If the user does not have a finished design template exported as a numbered-page PDF, stop and tell them what they need to do. You do not help build the template. The skill does not work without it.
2. **PDF input only.** HTML loses page numbering and requires extra splitting logic. PDF maps cleanly: one page = one layout = one PNG.
3. **Pages must be numbered.** Each page in the user's template has a serial number that becomes the layout's stable ID. The PNG filenames preserve the number. The number is what the generated skill cites in its handoff so the design tool can look up the layout.
4. **Categories are case-by-case.** Do NOT impose a fixed category framework. Slide decks may have 7 categories; one-pagers may have 3; thumbnails may have 2. The user's template determines categories. You propose them based on visual analysis of the PNGs in Phase 4, then the user confirms or corrects.
5. **Two layout-analysis modes — let the user choose.** Phase 4 can run as (a) a deep-dive interview where the user walks you through every layout and you capture their words, or (b) hands-off where you visually analyze each PNG yourself and propose what each communicates, then the user confirms in one batch. Default to asking which mode they want.
6. **Brand-agnostic templates and scaffolds.** Nothing in this meta-skill or its outputs assumes a specific brand. Colors, voice, typography, icons all come from Phase 1 interview answers. Do not embed brand-specific examples in scaffolds.
7. **The generated skill's output is always a master Markdown file.** Format must be paste-ready into a the design tool chat. Even for asset types where some other format might seem more natural (carousels, ad creatives), MD is the universal handoff because the design tool takes it and renders.
8. **Generated skill workflow is always section-by-section interactive.** The generated skill does not batch. It walks one section at a time, proposes options, waits for confirmation, moves on. Compile the master MD only after every section is locked.
9. **The generated skill follows the same "before you start" discipline you do.** It reads all its own reference files before its first response.

## The 6 phases

### Phase 0 — Gate on the template

Your very first message in a fresh conversation. Before any interview, ask:

> Before we start: do you have a finished design template, exported as a PDF with numbered pages? The skill we're about to build wraps around that template, so it needs to exist first.
>
> - **Yes** → great. We'll continue. Drop the PDF somewhere on disk and I'll ask for the path in a moment.
> - **No** → here's what you need to do first: open the design tool, gather layout references for your asset type from Figma / Dribbble / Slides / Framer / wherever, paste them into a the design tool chat and ask it to convert them to your brand. Iterate until each layout fits your style. Save the result as a design template. Make sure every page is numbered. Then export as PDF and come back. **I'll be here.**

If the user is on the **No** path, stop here. Do not continue. Ask them to come back when the PDF exists.

If the user is on the **Yes** path, move to Phase 1.

### Phase 1 — Interview

Use questions from `references/interview-questions.md`. Cover:

- **Asset type** (slide deck, one-pager, LinkedIn carousel, thumbnail, ad creative, case study, email, other)
- **Skill name and slug** (slug becomes the output folder name, e.g. `linkedin-carousel-builder`)
- **Audience** the asset is for
- **Typical input** the user will feed the generated skill (outline, script, article, website URL, transcript, brief, reference image, etc.) — there can be more than one
- **Brand intake mode** (see Phase 1.5 below)
- **Voice and tone** (or a pointer to copy examples)
- **Reference content samples** (optional — if provided, becomes `copy-examples/` in the generated skill)
- **Target master-MD format** (default: paste-into-the-design-tool)

Ask the gating questions first (asset type, slug, input type), then the brand questions, then the voice questions. Keep total questions under ~10. Group related ones in a single message.

### Phase 1.5 — Brand intake (3 modes)

Ask the user which mode:

1. **Interview.** You ask 5-7 questions about colors, typography, signature visual elements, what to avoid. Best when the user knows their brand intuitively but doesn't have a written guide.
2. **Pasted brand document.** User pastes (or points to a file containing) brand guidelines. You parse and extract.
3. **Scraped URL.** User gives a website URL. You use `WebFetch` to pull the page, extract colors / fonts / voice cues from the HTML and visible content.

See `references/brand-intake.md` for the question banks and extraction patterns per mode.

### Phase 2 — Get the PDF in place

Ask the user for the absolute path to their exported design template PDF. Verify the file exists, is readable, and is a valid PDF. Confirm the page count.

Brief example:
> Drop the PDF somewhere accessible (Downloads is fine) and paste the absolute path here. I'll verify and tell you how many pages I see.

If the page count looks wrong (e.g. 1 page when you expected many), surface that and confirm with the user before continuing. Some the design tool exports include cover and divider pages — ask whether to include or skip them.

### Phase 3 — Convert PDF to numbered PNGs

Use the recipe in `references/pdf-pipeline.md`. Default: `pdftoppm -r 300 -png` per page, output to a temporary `_unsorted/` folder under `~/Downloads/{slug}/assets/templates/`. Filenames at this stage: `{page-num}-temp.png`. Rename and re-locate happens in Phase 5 once categories and slugs are known.

If `pdftoppm` is not installed, install via Homebrew (`brew install poppler`) and tell the user once.

After conversion, surface the page count and a quick visual check ("rendered 27 PNGs at 300 DPI to `~/Downloads/{slug}/assets/templates/_unsorted/`. Take a look — anything obviously broken?").

### Phase 4 — Walk through each layout

Ask the user which mode:

- **Deep-dive interview.** You go layout by layout, opening each PNG. For each one ask: "What does this communicate? When would you use it? What's the count range / slot shape? Any constraints?" Capture their words. Slow but maximally personalized.
- **Hands-off analysis.** You open every PNG, visually analyze each, and propose: name + slug + category + count range + slot schema + when-to-use, all in one batch. User confirms or corrects.

Default recommendation: hands-off for templates with 10+ layouts (faster), deep-dive for templates with fewer layouts (more personalized). Let the user override.

In either mode, the output of this phase is a structured per-layout record:

```
Layout {page-num}:
  name: {short name}
  slug: {kebab-case}
  category: {category name}
  count: {fixed N | flex M-N}
  slots: {slot list with budgets}
  icon-or-emoji: {icon-slot | emoji-friendly | neutral}
  best-for: {one sentence}
  when-to-pick: {one sentence}
```

You also derive the **list of categories** in this phase. Categories are emergent, not pre-defined. Group layouts by visual similarity and shared communicative role.

When done, present the full layout-by-layout summary in chat, ask the user to confirm or correct in one pass, then move on.

### Phase 5 — Generate the skill folder

Use the scaffolds in `references/output-skill-scaffold.md`. Fill every placeholder from Phase 1 / 1.5 / 4 data.

Generation order:

1. Create folder structure at `~/Downloads/{slug}/`. Subfolders per category (named `01-{category}/`, `02-{category}/`, etc.).
2. Move PNGs from `_unsorted/` to the correct category subfolders. Rename from `{page-num}-temp.png` to `{page-num}-{slug-from-Phase-4}.png`.
3. Write `references/layout-templates.md` (slot schemas + per-layout best-for). Format follows the scaffold.
4. Write `references/plot.md` (decision guide + cross-reference matrix + picking heuristic).
5. Write `references/brand.md` from Phase 1.5 brand intake.
6. Write `references/icons.md` from a default Unicode emoji palette. If the user gave brand-specific iconography hints, layer those on top.
7. If the user provided reference content samples, write them to `copy-examples/`.
8. Write `SKILL.md` last (it cross-references everything else).
9. Delete the `_unsorted/` directory.

The generated `SKILL.md` must include:

- Frontmatter (name, description, allowed-tools)
- "Before you start" prelude (read all reference files)
- Output format declaration ("master MD only")
- Library description (categories + IDs)
- Core rules: deck-wide template uniqueness, 2-4 options per section, ID + name citation, icons or emojis required, no batching, intro/skip handling if applicable for the asset type, voice rules
- The 4-step workflow (input → plan → propose → compile MD)
- Decision guide summary + pointer to plot.md
- Skip rules tailored to the asset type
- Edge cases
- Reference file table

Do not embed Ben AI specifics or any other branded language. Voice and tone language comes from Phase 1 answers.

### Phase 6 — Verify and ship

Run the checklist in `references/verification.md`. Common checks:

- Every PNG referenced from `references/layout-templates.md` exists at the cited path
- Every category referenced has at least one PNG
- All cross-references between scaffolds resolve
- Frontmatter is valid YAML
- No template-creator placeholder text leaked through

Fix any issues. Then `open ~/Downloads/{slug}/` to surface the folder in Finder.

Brief the user:

> Skill is built at `~/Downloads/{slug}/`. To use it: drop the folder into your skills directory (or invoke from this path), feed it any input (outline / script / article / brief / etc.), and walk through section by section. Output is a master Markdown file at `~/Downloads/{slug}-output-{timestamp}.md` that you paste into a the design tool chat to render.

## Edge cases

- **User's PDF has cover, divider, or table-of-contents pages.** Detect and ask: "Pages X, Y, Z look like cover or divider pages. Skip them, or include as templates?"
- **PDF page count doesn't match user expectation.** Surface mismatch before converting. The user may have exported the wrong file or forgotten to include some pages.
- **Two PNGs look near-identical.** During Phase 4, flag for the user — they may be two valid variants (e.g. blue vs green palette) or one might be a duplicate to skip.
- **User cannot articulate brand details.** If interview mode stalls, suggest pasted-doc or scraped-URL mode. Or fall back to "we'll write a minimal brand.md and you can fill it in later."
- **User's chosen slug clashes with an existing folder in `~/Downloads/`.** Append `-v2` or ask for a new slug.
- **User wants to add layouts later.** That's a different operation — extending an existing skill. Out of scope for v1. Tell the user to re-run from Phase 2 with a fresh PDF.
- **`pdftoppm` not installed.** Install via Homebrew. Surface the install command and run it.
- **PDF is password-protected or corrupted.** Surface the error, ask the user to re-export.

## When to escalate to the user

- Any time you'd otherwise guess. Categories, slugs, slot definitions, voice tone — when in doubt, ask.
- Before deleting anything. The `_unsorted/` cleanup at the end of Phase 5 is the only deletion you do without confirmation.
- Before overwriting an existing folder at `~/Downloads/{slug}/`.

## What this skill never does

- Help build the design template itself. That's an upstream creative process the user owns.
- Embed brand-specific examples (Ben AI or otherwise) in any generated file.
- Generate rendered visuals (no Excalidraw, no SVG, no HTML render). The generated skill's output is always Markdown.
- Skip the interview to "save time". The interview is where personalization comes from. Without it, the generated skill is generic and the output suffers.

## Reference files

| File | Purpose |
|------|---------|
| `references/interview-questions.md` | Question bank for Phase 1 (asset/audience/input), Phase 1.5 (brand), Phase 4 (per-layout). |
| `references/pdf-pipeline.md` | How to guide the the design tool PDF export and how to convert it to numbered PNGs at 300 DPI. |
| `references/brand-intake.md` | Three brand-capture modes (interview, pasted doc, scraped URL) with extraction patterns. |
| `references/output-skill-scaffold.md` | Parameterized scaffolds for the generated SKILL.md, plot.md, layout-templates.md, brand.md, icons.md. |
| `references/verification.md` | Post-generation sanity-check checklist. Run before declaring the skill done. |
