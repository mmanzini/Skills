# Interview Question Bank

Questions to draw from across the three interview phases. Group related questions in a single chat message — don't ask one at a time, that creates dead turns.

## Phase 0 — Template gating (always first, alone, before any other interview)

Just one question, before anything else:

> Do you have a finished design template, exported as a PDF with numbered pages? **Yes** = we continue. **No** = you need to build the template first; come back when you have the PDF.

If the user says yes, ask in the same flow:

> Where on disk is the PDF? Drop the absolute path.

(You don't need to verify the file yet — Phase 2 does that. This question is just to keep momentum.)

## Phase 1 — Asset, audience, input

Ask these in one combined message after the user confirms the template exists. Required:

1. **What asset type does the template produce?** (slide deck, one-pager, LinkedIn carousel, thumbnail, ad creative, case study, email layout, sales-page, other)
2. **What should we call the skill?** Plain name + short slug for the folder. Example: name `LinkedIn Carousel Builder`, slug `linkedin-carousel-builder`.
3. **Who is the audience for the asset?** One sentence. Example: "Founders evaluating B2B SaaS tools."
4. **What kind of input will you typically feed this skill?** Multi-select fine. Common: video outline, full script, blog article, website URL, transcript, brief / call notes, reference image, raw bullet points, RFP, customer interview. Capture all that apply — the generated skill should accommodate every input type the user names.
5. **Any sections / inputs the skill should always skip?** Example for slide decks: intros, hooks, B-roll, demos. Skip rules vary wildly by asset type — for a sales one-pager there may be no skips. Ask explicitly.

Optional but useful:

6. **What's the typical output size?** (number of slides for a deck, number of cards for a carousel, number of pages for a one-pager). This becomes a default the generated skill uses for sanity-checking.
7. **Do you have any reference content samples** (existing finished assets in this format that the skill should calibrate tone and density against)? If yes, get paths or copy text — these become `copy-examples/` in the generated skill.

## Phase 1.5 — Brand intake

Ask the user which mode first:

> Three ways to capture your brand, pick one:
> a. **Interview** — I ask 5-7 questions and you answer in chat.
> b. **Pasted doc** — you paste your brand guidelines (or a path to a file containing them) and I extract.
> c. **Scraped URL** — you give me a website URL and I pull colors / fonts / voice cues from it.

Then run the chosen mode using `references/brand-intake.md`.

## Phase 4 — Per-layout walkthrough

Ask the user which mode first:

> Two ways to walk through your template's layouts:
> a. **Deep-dive** — we go layout by layout. You tell me what each communicates and I capture your words. Slow, maximally personalized. Good for templates with under ~10 layouts.
> b. **Hands-off** — I open every PNG, visually analyze, and propose a name / category / use-case for each in one batch. You confirm or correct. Fast, still personalized via your corrections. Good for templates with 10+ layouts.

### Deep-dive mode questions (one PNG at a time)

For each layout:

1. **What does this layout communicate?** Force them to answer in one sentence. "This shows a parallel comparison" or "This is a 4-step cycle" — not "it's a list".
2. **When would you reach for this?** Example use cases. "When the content has 3 peers of equal weight" or "When the section is anchored on a single stat".
3. **What's the count range?** Fixed (always exactly N items) or flex (M to N items)?
4. **What slots does it have?** Walk through the visible elements. Headline, sub-head, cards / rows / segments, body text, icon slots, etc. For each slot capture a brevity budget (1-4 words / 3-8 words / etc.).
5. **Does it have icon slots, support inline emojis, or neither?** Crucial for the generated skill's icon/emoji rules.
6. **Anything to avoid?** "Don't put more than 4 cards", "Never use this for sequential content", etc.

### Hands-off mode questions (one batch at the end)

After visually analyzing all PNGs, present a table to the user:

```
| Page | Proposed name        | Proposed category | Count   | Slots                        | Communicates                  |
|------|----------------------|-------------------|---------|------------------------------|-------------------------------|
| 01   | Pyramid              | Hierarchy         | fixed 3 | tier h3, tier p              | Tiered priority, foundation   |
| 02   | Three Cards          | Cards & Lists     | flex 3-6| h3 + p per card              | Parallel ideas, equal weight  |
| ...  | ...                  | ...               | ...     | ...                          | ...                           |
```

Ask:

> Confirm or correct: any names to change? Any categories to merge or split? Any layouts I read wrong? Any I should drop entirely?

## Phase 6 — Wrap-up (after generation)

> Skill is built at `{path}`. Want me to walk you through how to invoke it the first time, or are you good?

Optional follow-ups:

- Do you want a sample input the skill could practice on right now?
- Want me to add this skill to your skills directory automatically?
