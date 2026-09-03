# Business case: {{Title}}

**Date:** {{YYYY-MM-DD}} · **Author:** {{Author}} · **Decision maker:** {{Decision maker}}
**Status:** {{draft | for decision}}

## Executive summary

{{Decision ask in the first sentence. Headline NPV at base rate, IRR, payback.
Recommendation in plain words. Max ~150 words.}}

## Problem / opportunity

{{What hurts or what is possible, for whom, and why now.}}

## Cost of doing nothing

{{The baseline: what happens over the horizon if no option is chosen.}}

## Options considered

### Option A — {{name}} (recommended)
{{One paragraph.}}

### Option B — {{name}}
{{One paragraph, incl. why not recommended.}}

### Option C — Status quo
{{One paragraph.}}

## Financial model

Interactive version: {{artifact URL}}

| Year | {{Y0}} | {{Y1}} | {{Y2}} | {{…}} |
|------|-------:|-------:|-------:|------:|
| Investment | {{}} | | | |
| Benefits | | {{}} | {{}} | {{}} |
| Recurring costs | | {{}} | {{}} | {{}} |
| Net cash flow | {{}} | {{}} | {{}} | {{}} |
| Cumulative (discounted @ {{r}}%) | {{}} | {{}} | {{}} | {{}} |

- **NPV @ {{r}}%:** {{value}}
- **IRR:** {{value}}
- **Payback:** {{simple}} (simple) / {{discounted}} (discounted)

**Sensitivity (NPV, one-way ±20%):**

| Driver | −20% | Base | +20% |
|--------|-----:|-----:|-----:|
| {{driver 1}} | {{}} | {{}} | {{}} |
| {{driver 2}} | {{}} | {{}} | {{}} |

## Assumptions register

| # | Assumption | Class | Status | Owner | Rationale |
|---|-----------|-------|--------|-------|-----------|
| 1 | {{}} | {{estimate/policy/risk-appetite}} | {{confirmed/default/open}} | {{}} | {{}} |

## Risks and mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {{}} | {{}} | {{}} | {{}} |

## Recommendation and next steps

{{What to decide, by whom, by when. Then the first three concrete steps.}}
