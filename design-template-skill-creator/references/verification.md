# Verification Checklist

Run this against the generated skill folder before declaring the build done. If any check fails, fix it; do not present a half-built skill to the user.

## 1. Folder structure

- [ ] `~/Downloads/{slug}/` exists.
- [ ] `~/Downloads/{slug}/SKILL.md` exists.
- [ ] `~/Downloads/{slug}/references/` exists with `layout-templates.md`, `plot.md`, `brand.md`, `icons.md`.
- [ ] `~/Downloads/{slug}/assets/templates/` exists with one subfolder per category from Phase 4.
- [ ] `~/Downloads/{slug}/copy-examples/` exists if the user provided reference samples.
- [ ] `_unsorted/` is gone (or empty).

## 2. PNG count and placement

- [ ] PNG count under `assets/templates/` matches the number of layouts the user kept (template page count minus skipped pages).
- [ ] Every PNG is in the correct category subfolder per Phase 4.
- [ ] Every PNG is named `{id}-{slug}.png` (no `-temp` suffix anywhere).
- [ ] Every layout ID referenced in `layout-templates.md` and `plot.md` exists as a real file at the cited path. Run a quick check:

```bash
grep -oE 'assets/templates/[^"`)]+\.png' ~/Downloads/{slug}/references/*.md | sort -u | while read p; do test -f ~/Downloads/{slug}/$p || echo "MISSING: $p"; done
```

## 3. Frontmatter validity

- [ ] `SKILL.md` has YAML frontmatter with `name`, `description`, `allowed-tools`.
- [ ] `name` matches `{slug}` exactly.
- [ ] `description` is filled, not a placeholder.
- [ ] `allowed-tools` includes the tools the generated skill needs (Read, Write, Edit, Glob, Grep, Bash at minimum).

## 4. No leaked placeholders

Search every generated file for `{` to find unresolved templates:

```bash
grep -rn '{[A-Z_]*}' ~/Downloads/{slug}/ | grep -v '\.png:'
```

Should return nothing. Any hit is a placeholder you forgot to fill.

Also search for stub language that shouldn't ship:
```bash
grep -rni 'TODO\|FIXME\|placeholder\|fill in\|to be determined' ~/Downloads/{slug}/
```

## 5. Cross-references resolve

- [ ] Every `references/...` path mentioned in `SKILL.md` exists.
- [ ] Every layout ID mentioned in `plot.md` decision guide also has an entry in `layout-templates.md`.
- [ ] Every category folder in `assets/templates/` is mentioned in `plot.md` and `layout-templates.md`.

## 6. Brand and voice content is real

- [ ] `brand.md` colors are real hex codes (not `#XXXXXX` placeholders).
- [ ] `brand.md` fonts are named, not placeholder strings.
- [ ] Voice do/don't lists have at least 3 entries each.
- [ ] No generic stub phrases like "your brand here" or "describe your voice".

## 7. Description triggers work

- [ ] The generated `SKILL.md` description mentions:
  - The asset type by name (singular and plural)
  - At least 2 input types the user named in Phase 1
  - Trigger phrases ("plan {asset_type}", "draft a {asset_type}", etc.)
- [ ] Description is one paragraph, not bulleted.

## 8. Asset-type personalization

- [ ] Skip rules in SKILL.md match what the user said in Phase 1 (or are omitted entirely if the user said no skips apply).
- [ ] Voice block in SKILL.md matches Phase 1 voice rules.
- [ ] Decision guide tables don't reference categories from a different asset type's example.

## 9. No leaked source material

- [ ] No reference to "Ben AI" anywhere unless the user explicitly is Ben AI.
- [ ] No reference to other branded examples that crept in from sample data.
- [ ] No reference to the meta-skill itself (`design-template-skill-creator`) inside the generated skill.

## 10. Render check

- [ ] Open the generated `SKILL.md` and skim — does it read coherently from top to bottom? Are the workflow steps in order? Do examples match the asset type?
- [ ] Open `plot.md` decision guide table — does each row make sense? Do the "Top pick" and "Close second" recommendations actually correspond to layouts in the catalog?

## What to do when a check fails

- Fix the file directly. Don't ask the user — they've already given you everything they need to.
- After fixing, re-run the checklist for that section.
- Only escalate to the user if a check reveals genuinely missing input (e.g. the user never confirmed a layout's category and you have no defensible default).

## After all checks pass

```bash
open ~/Downloads/{slug}/
```

Brief the user with the path and three next steps:
1. How to invoke the new skill.
2. Where its master MD output will save (`~/Downloads/{slug}-{asset}-{timestamp}.md`).
3. How to extend it later (currently out of scope; mention it would be a re-run with a fresh PDF).
