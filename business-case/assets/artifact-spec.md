# Interactive artifact spec

The Phase 3 artifact is one self-contained HTML page, generated fresh per case
with the case's data embedded as a JS object. Load the `artifact-design` skill
before building it. Republish to the same file path every iteration (same URL).

## Constraints

- No external libraries; inline JS + inline SVG charts only.
- Theme-aware per the Artifact tool's rules (light tokens on `:root`, dark via
  `prefers-color-scheme` guard + `[data-theme="dark"]`).
- Formulas in JS must mirror `npv-irr-method.md` exactly (NPV sum, Newton IRR
  with bisection fallback, both paybacks). The numbers shown on load must equal
  the agent's Phase 2 numbers — verify before publishing.
- Downloads are blocked in the artifact sandbox: the Export tab uses
  copy-to-clipboard (`navigator.clipboard` with a select-all `<textarea>`
  fallback), never `<a download>`.
- Favicon: `📊`, kept stable across republishes.
- `<title>`: short case name (e.g. "Pricing Module Case"), stable.

## Layout (tabs)

**1. Model** (default tab)
- Headline strip: NPV @ current rate, IRR, simple + discounted payback.
  Values update live on any input change.
- Inputs panel: discount-rate slider (range from the agreed band, 0.5% steps,
  numeric readout) + numeric fields for each key driver (initial investment,
  recurring cost, benefit level, growth %, ramp-up %, horizon in years).
  A "reset to base case" button restores Phase 2 values.
- Chart A: cumulative discounted cash flow by year (SVG line/area, zero line
  marked, payback year highlighted).
- Chart B: NPV vs discount rate over the band (current rate marked; IRR is
  visibly the zero crossing).
- Cash-flow table: per-year investment / benefits / costs / net / cumulative
  discounted, recomputed live.
- Sensitivity table: one-way ±20% on the dominant drivers, recomputed live.

**2. Assumptions**
- The assumptions register: assumption, class (estimate / policy /
  risk-appetite), status (confirmed / default / open), owner, rationale.
- Open judgment calls visually flagged (badge) so they are impossible to miss.

**3. Export**
- The full markdown business case (per `case-template.md`) rendered into a
  `<textarea readonly>` with the **current** input values baked in — regenerate
  the markdown string on tab open, not at build time.
- "Copy markdown" button + a note that the agent also writes the file to
  `Tasks/business-case-<slug>-<date>/case.md` on request.

## Behaviour

- All state lives in one JS object; every input mutation triggers one
  `recompute()` that updates headline, charts, tables, and export text.
- No localStorage needed; the agent republishes the artifact when values
  should persist (chat remains the source of truth for the case).
- Numbers formatted with thousands separators and the case's currency symbol;
  rates as percentages with one decimal.
