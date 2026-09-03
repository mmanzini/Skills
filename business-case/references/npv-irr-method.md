# NPV / IRR method

Conventions the agent and the artifact's JS must both follow, so their numbers
never disagree.

## Cash-flow table

- Yearly granularity. Year 0 carries the initial investment (negative);
  years 1..N carry net cash flow = benefits − recurring costs for that year.
- Ramp-up applies to benefits only, e.g. 50% in year 1, 100% from year 2,
  unless the brief says otherwise.
- Growth rate `g` compounds benefits from the year after full ramp-up.
- All figures in one currency, nominal (no inflation adjustment) unless the
  discount rate is explicitly real — never mix.
- Terminal value only if agreed as a judgment call; model as a final-year
  lump sum and show it as its own row.

## NPV

```
NPV(r) = Σ_{t=0}^{N} CF_t / (1 + r)^t
```

- Base rate `r` from Phase 0. Show the NPV curve over a range around it
  (default: 0% to max(2·r, 25%), step 0.5%).
- Cumulative discounted cash flow per year gives the payback chart.

## IRR

- IRR = the `r` where NPV(r) = 0.
- Solve with Newton's method from r₀ = 10%; if it fails to converge in 50
  iterations or leaves (−0.99, 10), fall back to bisection on that interval.
- No sign change in cash flows → IRR undefined; report "n/a (cash flows never
  turn positive/negative)".
- Multiple sign changes → multiple roots possible; report the smallest
  positive root and add a note in the assumptions register.
- Sanity check: NPV evaluated at the reported IRR must be ~0, and the NPV
  curve must cross zero at the IRR.

## Payback

- Simple payback: first year where cumulative *undiscounted* cash flow ≥ 0.
- Discounted payback: same on discounted flows. Report both; "beyond horizon"
  if never reached.

## Sensitivity

- Pick the 2–3 drivers with the largest NPV impact (test ±20% on each to rank).
- Output a table: driver ±20% → NPV, ΔNPV vs base.
- One-way only; no Monte Carlo (out of scope — say so if asked).

## Discount-rate guidance

When the organisation has no published WACC/hurdle rate, propose a band and
flag it as a policy judgment call:

| Context | Typical band |
|---------|-------------|
| Internal cost-saving / efficiency project | 8–12% |
| Product investment, established business | 10–15% |
| New venture / high-uncertainty bet | 15–25% |

Default to the band's midpoint for the base case and show the full band on the
NPV curve.
