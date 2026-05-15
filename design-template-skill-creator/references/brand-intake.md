# Brand Intake

Three modes for capturing the brand identity that goes into the generated `references/brand.md`. Pick one based on user preference. Each mode produces the same output shape: a populated brand reference with colors, typography, design rules, voice rules, and "what to avoid" guidance.

## Mode A — Interview

Best when the user knows their brand intuitively but doesn't have it written down. 5-7 short questions, one chat message:

1. **Primary text/border color** — usually a near-black or dark navy. Hex code or describe and you'll suggest one.
2. **Background colors** — base background plus accent backgrounds (1-4). Hex codes or descriptions.
3. **Are there any specific colors you NEVER use?** Pure black? Pure white? Default Excalidraw palette?
4. **Typography** — heading font, body font, fallback. If they don't know, ask: serif or sans-serif feel? Modern or classic?
5. **Signature visual element** — do you have a recognizable design quirk? Solid drop shadows? Hand-drawn outlines? Specific corner radius? Sticker-style cards?
6. **Voice (3 do's, 3 don'ts)** — three things their copy ALWAYS does (e.g. "specific verbs", "real product names", "numbers when relevant") and three things it NEVER does (e.g. "no em dashes", "no AI buzzwords", "no passive voice").
7. **Any audience-specific notes** — terminology to use or avoid (e.g. "say 'agent' not 'bot'"; "say 'workflow' not 'pipeline'").

After answers, present the extracted brand spec back to the user for confirmation:

```
Colors:
  - Text/borders: #...
  - Background: #...
  - Accent 1: #...
  ...

Typography:
  - Headings: ...
  - Body: ...
  - Fallback: ...

Signature: ...

Voice:
  Do: ...
  Don't: ...

Confirm or correct?
```

## Mode B — Pasted brand document

User pastes their brand guidelines into chat, or gives a path to a file (PDF / MD / DOCX / TXT). Read the file and extract:

- **Colors** — search for hex codes (`#[0-9A-Fa-f]{6}`), CMYK / RGB / Pantone references, named colors with usage notes
- **Fonts** — look for "font", "typeface", "typography" sections; capture heading + body + fallback
- **Voice rules** — look for "voice", "tone", "writing", "style" sections; capture do/don't lists or descriptive paragraphs
- **Don't-use** — words / phrases / colors explicitly forbidden
- **Signature elements** — descriptive terms about visual identity (e.g. "drop shadows", "hand-drawn", "minimal")

After extraction, summarize what you found and ask the user to fill gaps:

```
Extracted from your brand doc:
  - Colors: 5 hex codes found (...)
  - Fonts: heading is ..., body is ...
  - Voice: 4 do's and 3 don'ts
  - Forbidden: pure black, em dashes
  - Signature: solid 8px drop shadows

Anything missing or off? Any color usage you want to clarify (e.g. which one is the primary accent)?
```

If the file is a PDF, use Read with the file path — the Read tool handles PDFs.

## Mode C — Scraped URL

User gives a website URL. Use `WebFetch` to fetch the page. Extract:

- **Colors** — from rendered HTML / CSS in the response. Look for inline `style` attributes, prominent hex codes in the visible content. If the fetched page is a marketing site, the hero and primary CTAs usually carry the brand colors.
- **Fonts** — search for `font-family`, `@font-face` declarations.
- **Voice cues** — read the body copy. What kinds of sentences does the site use? Short and punchy? Long and educational? Formal or conversational? Surface specific verbs and phrases.
- **Visual elements** — described in copy ("we believe in clean design", etc.) or inferred from CSS.

If the page is a single-page app and `WebFetch` returns minimal text, fall back to extracting whatever's available and supplementing with Mode A interview questions to fill gaps.

After extraction:

```
From {url}, I pulled:
  - Likely colors: ...
  - Fonts in use: ...
  - Voice signals: short, declarative; uses "ship", "build", "scale" frequently; avoids hype words

This is inferred — confirm or correct, especially the color usage (which is primary, which is accent).
```

## What goes into the generated brand.md

Regardless of mode, the output `brand.md` follows this shape (filled with user's values):

```markdown
# Brand Reference

## Colors

| Color | Hex | Usage |
|-------|-----|-------|
| Text / borders | #... | ... |
| Background | #... | ... |
| Accent 1 | #... | ... |
| Accent 2 | #... | ... |
| ... | ... | ... |

**Never use** {list of forbidden colors, e.g. pure black, default palettes}.

## Color rotation (multi-item layouts)

When a layout has multiple cards / items, rotate accents in this order:
1. Accent 1
2. Accent 2
3. Accent 3
4. (loop)

## Typography

| Usage | Font |
|-------|------|
| Headings | ... |
| Body | ... |
| Fallback | ... |

## Signature visual element

{e.g. "solid 8px drop shadows", "hand-drawn outlines", "sticker-style cards with 4px borders"}

## Voice

**Do:**
- ...
- ...
- ...

**Don't:**
- ...
- ...
- ...

## Forbidden language

- ...
- ...
```

## When to fall back to Mode A

If Mode B's pasted doc is sparse, or Mode C's URL fetch returns very little, ask the user the missing Mode A questions instead of guessing. Brand fidelity matters — guesses end up in every asset the skill produces.
