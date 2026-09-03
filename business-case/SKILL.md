---
name: business-case
description: >
  Build a business case interactively from a rough brief. Gap analysis first (missing
  data + judgment calls needing a human decision), then an NPV/IRR model with variable
  discount rate, published as an interactive artifact for iteration, exported as a
  markdown business case with a final presentation-strengthening pass. Trigger on
  "/business-case", "build a business case", "business case for", "NPV model for",
  "investment case", "should we invest in".
argument-hint: "<short context, or paste the brief>"
---

# Business Case Builder

Turns a rough brief (a question, some data requirements, general context) into a
defensible business case. The financial core is an NPV/IRR model with a variable
discount rate, presented as an interactive artifact the user iterates on, and
finally exported as a markdown file under `Tasks/business-case-<slug>-<YYYY-MM-DD>/`.

## Operating principles

- **Gaps before prose.** Never draft the case until the gap report (Phase 1) has
  been shown and the user has responded. Every unanswered item becomes a flagged
  assumption that travels through the model, the artifact, and the export — it is
  never silently dropped.
- **Facts vs judgment calls.** A missing *fact* is retrievable (a price, a volume,
  a headcount cost) — name where to get it. A *judgment call* is not retrievable —
  someone must decide it (growth rate, horizon, risk appetite, discount rate).
  Propose a default with a one-line rationale, but mark it as the user's call.
- **One artifact, one URL.** Publish once in Phase 3, then republish to the same
  file path on every iteration. Never create a second artifact for the same case.
- **The agent owns the arithmetic.** Compute NPV, IRR, payback and sensitivity
  yourself per `references/npv-irr-method.md`; the artifact's JS recomputes the
  same formulas live so the two never disagree.
- **User's voice.** All output text follows the user's writing rules (UK English,
  no corporate jargon, no AI-tell lists, no em dashes in prose deliverables).

## Phase 0 — Intake

Parse `$ARGUMENTS` and anything pasted. Then ask **3–5 questions max**
(AskUserQuestion where options are enumerable, chat otherwise), covering only
what the brief did not already answer:

1. What decision is being made, and who makes it?
2. What alternatives are on the table? (Always include do-nothing / status quo.)
3. Time horizon for the evaluation?
4. Main cost and benefit drivers? (Rough magnitudes are fine at this stage.)
5. Discount-rate basis — company WACC, a hurdle rate, or unknown? If unknown,
   propose a band per `references/npv-irr-method.md`.

Confirm the intake back in one paragraph before moving on.

## Phase 1 — Gap report

Compare what is known against the required-data checklist in
`references/case-structure.md`. Output two lists in chat:

- **Missing facts** — each with where/whom to get it from.
- **Judgment calls** — each with a proposed default and rationale, per the
  taxonomy in `references/case-structure.md`.

Let the user answer what they can. Record every resolution; everything
unresolved is logged as a flagged assumption with status `default` or `open`.

## Phase 2 — Model

Build the model per `references/npv-irr-method.md`:

- Yearly net cash-flow table over the horizon (year 0 = investment).
- NPV at the base discount rate; NPV curve across the agreed rate range.
- IRR (Newton with bisection fallback), simple payback.
- Sensitivity of NPV to the 2–3 dominant drivers.

Show the headline numbers in chat in one short paragraph — the full detail
lives in the artifact.

## Phase 3 — Interactive artifact

Load the `artifact-design` skill first, then build and publish one
self-contained HTML artifact following `assets/artifact-spec.md`. In short:
inputs panel (discount-rate slider + key-driver fields), live NPV/IRR/payback
outputs with SVG charts, assumptions register with statuses, and an Export tab
that renders the full markdown case with a copy button. No external libraries;
theme-aware.

## Phase 4 — Iterate

The user tweaks values in the artifact and/or resolves open items in chat.
Fold their answers back into the model, update the assumptions register, and
republish to the same URL. Loop until the user says the numbers hold.

## Phase 5 — Strengthen

Presentation pass on the near-final case:

- Rewrite the executive summary to lead with the decision ask.
- Order the narrative: problem → cost of doing nothing → options →
  recommendation → risks and mitigations.
- Pre-empt the three most likely objections, with the model's numbers.
- Apply the user's writing rules throughout.

Propose the edits in chat; apply on approval.

## Phase 6 — Export

1. Fill `assets/case-template.md` with the final content and write it to
   `Tasks/business-case-<slug>-<YYYY-MM-DD>/case.md` in the vault.
2. Refresh the artifact's Export tab so it matches the file exactly.
3. Close with one line: the file path and the artifact URL.

## Known limitations

- Single-currency, yearly-granularity cash flows. Monthly modelling or FX are
  out of scope; say so if the brief needs them.
- IRR is reported as undefined when cash flows never change sign, and the
  smallest positive root is used when multiple sign changes exist (noted in
  the artifact).

## Verification

After any edit to this skill: run `/business-case` with a toy brief and check
that the gap report separates facts from judgment calls, the artifact's slider
moves NPV live, IRR is consistent with the NPV=0 crossing, and the export file
lands in `Tasks/business-case-*/`.
