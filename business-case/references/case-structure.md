# Business-case structure and required data

## Section canon

Every case has these sections, in this order:

1. **Executive summary** — the decision ask in the first sentence, headline
   NPV/IRR, recommendation. Max ~150 words.
2. **Problem / opportunity** — what hurts or what is possible, and for whom.
3. **Cost of doing nothing** — the baseline the options are compared against.
4. **Options considered** — including status quo. One paragraph each; why
   rejected options were rejected.
5. **Financial model** — cash-flow table, NPV at base rate, NPV-vs-rate view,
   IRR, payback, sensitivity. Points to the interactive artifact.
6. **Assumptions register** — every assumption with status
   (`confirmed` / `default` / `open`), owner, and rationale.
7. **Risks and mitigations** — top 3–5, each with likelihood, impact, mitigation.
8. **Recommendation and next steps** — what to decide, by whom, by when.

## Required-data checklist

Used by Phase 1 to generate the gap report. For each item: known / missing
fact / judgment call.

| # | Item | Usual kind |
|---|------|-----------|
| 1 | Decision to be made + decision maker | fact |
| 2 | Alternatives incl. do-nothing | fact |
| 3 | Initial investment (capex, one-off costs) | fact |
| 4 | Recurring costs (run, licences, headcount) | fact |
| 5 | Benefit drivers (revenue uplift, cost avoided, risk reduced) | fact + judgment |
| 6 | Benefit ramp-up / growth rate | judgment |
| 7 | Time horizon | judgment |
| 8 | Discount rate (WACC or hurdle) | fact if company sets one; else judgment |
| 9 | Terminal value treatment | judgment |
| 10 | Currency and inflation treatment | fact |
| 11 | Key risks and their cost impact | judgment |
| 12 | Dependencies (people, systems, other projects) | fact |

## Judgment-call taxonomy

Classify each judgment call so the right person decides it:

- **Estimate** — a number nobody has measured (adoption rate, ramp-up speed).
  Default: propose a conservative/base/optimistic triple; model the base,
  show the spread in sensitivity.
- **Policy** — a choice the organisation must own (horizon, discount rate,
  terminal value, make-vs-buy stance). Default: use the organisation's
  published figure if any; otherwise a defensible convention, clearly flagged.
- **Risk appetite** — how much downside is acceptable (contingency %, worst-case
  planning). Default: show the downside scenario and let the decision maker
  pick the buffer.

Every judgment call in the gap report names its class, the proposed default,
and one line of rationale.
