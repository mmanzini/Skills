# Resolver details

One section = one resolver = one `Dashboard/data/<x>.md`. Tasks + metrics are
**deterministic** (scripts); GitHub + Life prose + Upcoming are **LLM synthesis**.

## 1. tasks → `data/tasks.md`  (deterministic — no LLM)

Run the script; it does everything:

```bash
python3 Skills/dashboard-refresh/scripts/parse_tasks.py
```

It reads `Tasks/TASKS.md` (open = unchecked `- [ ]` line; title + status from the
line, project from the section heading), enriches `project` from the
`Tasks/ledger.md` Area column, and writes `data/tasks.md` with `updated`,
`total_open`, `by_status`, `items:[{id,title,status,project}]`. Do not hand-edit
this file — re-run the script.

## 2. github-trends → `data/github-trends.md`  (LLM)

Read `Intelligence/github-trends/` (+ the github-trending-digest source if
present). Pick the top rising repos → `items:[{repo,stars,delta,lang}]`. Write:

- `summary_week` — where developer/audience attention moved over the **last 7
  days**; what's hot now.
- `summary_month` — the broader **30-day** arc: what's gaining, what's cooling.
- `prediction` — educated call on where attention is heading, grounded in the
  **week-vs-month delta**. Name concrete categories/technologies, not hype.
- `investigate` — **actionable** items mapping rising topics to the user's own
  skill growth and/or Atlas improvements (e.g. "agent-memory repos → benchmark vs
  Atlas episodic memory"). Each ties to a concrete next move; cross-reference the
  Tasks board so items aren't duplicates of existing tasks.

## 3. life → `data/life.md`  (metrics deterministic, prose LLM — the hero block)

**Metrics first (script):**

```bash
python3 Skills/dashboard-refresh/scripts/daily_metrics.py 14
```

It prints JSON `{as_of, window_dates, metrics:[{name,value,unit,history}]}` from
the last 14 daily notes (`Resources/Daily/` + `Intelligence/daily/`). Drop the
`metrics` array verbatim into `data/life.md` and use its `as_of`.

**Prose (LLM):** read those same 14 daily notes' Summary / Decisions / Open-loops
/ Signals sections, cross-check against `Tasks/TASKS.md` so nothing is stale, and
write:
- `happened` — what the last 14 days were about;
- `now` — what's in flight today / this week;
- `coming` — what's upcoming;
- `highlights` — standout wins/events (list);
- `actions` — concrete next to-dos (list);
- `prediction` — a slight, grounded forward read.

Stamp `as_of` (from the script) and `window_days: 14`.

## 3b. political-economy → `data/political-economy.md`  (LLM + live web, no chart)

1. **Standing analysis:** read `Intelligence/political-economy/_master-index.md`
   **and** `Intelligence/philosophy/_master-index.md`, plus their most-covered /
   most-relevant topic `_index.md` and key articles (macro/geopolitical +
   philosophical lenses).
2. **Derive threads dynamically:** the threads to chase are whatever the
   intelligence query surfaces as most salient right now — do **not** hardcode a
   fixed region/topic list. Then **web-search live news** for each derived thread
   for this week's concrete developments.
3. **Blend → frontmatter:** `summary_week`/`summary_month` = the durable analysis
   updated with live events; `prediction` grounded in both; `watch` = upcoming
   events/datapoints to monitor; `investigate` = deeper reads. Stamp
   `news_refreshed` (today) and optional `sources` (live headlines used). If web is
   unavailable, fall back to intel-only and say so in `summary_week`.

## 4. upcoming → `data/upcoming.md`  (LLM)

Derive forward-looking items from Tasks (due dates), dated items in the dailies,
and the Intelligence layer (deadlines, commitments, flagged ideas). Write
`items:[{title,due,kind}]`, `kind ∈ {deadline,event,idea,reminder}`. The renderer
sorts by `due`.

## Frontmatter schemas

Canonical shapes live in `assets/schemas/`. Match them exactly — renaming/removing
a key breaks the matching `Dashboard.js` renderer method.
