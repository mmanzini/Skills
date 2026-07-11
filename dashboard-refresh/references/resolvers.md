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

Stamp `updated` (real refresh clock, e.g. `date -u +%Y-%m-%dT%H:%M`), `as_of`
(from the script — the latest daily note, which may lag `updated` by a day when
today's daily note doesn't exist yet), and `window_days: 14`. The renderer badge
reads `updated ?? as_of`; without `updated`, life reads a day stale next to the
other sections whenever today's daily note hasn't been written.

## 3a. ai-news → `data/ai-news.md`  (LLM + live web, dedup ledger)

Expanded version of the `/ai-news` command (`Skills/ai-news/commands/ai-news.md`
holds the full company/category list and query templates — reuse them).

1. **Window:** read `data/ai-news.md`. Window = since its `news_refreshed` date,
   capped at **7 days** back (file missing/blank → 7 days). Parse the
   `## Previously shown` ledger in the file **body** → set of already-shown URLs.
2. **Sweep:** WebSearch across the coverage list in
   `Skills/ai-news/commands/ai-news.md` — Western + Asian foundation models,
   agent/dev tooling, hardware/infra, policy/regulation, funding & business,
   research/safety. Date-scope queries with the current month/year; use the
   Asian-coverage source hints (SCMP, TechNode, Pandaily, 36Kr, Reuters …);
   search model names (Qwen, Kimi, Doubao, ERNIE, GLM) not just company names.
3. **Filter + dedup:** keep significant items (release/launch/update/model/
   policy/funding/safety…), verify publish dates fall in the window, drop any
   URL already in the ledger. Newest first, cap ~10 →
   `items:[{vendor,headline,summary,url,date,category}]`,
   `category ∈ {release,product,business,research,hardware,policy,funding,safety}`.
4. **Reaction:** one extra search pass on the 2–3 biggest items
   ("<headline> reaction", market/analyst/community coverage) → `reaction` =
   3–5 sentence prose on how markets, press, and the community are responding.
5. **Weekly digest (always):** `weekly_digest` = prose recap of the full last
   7 days grouped by theme — includes previously-shown items, not just new ones.
6. **Write:** frontmatter per `assets/schemas/data-files.md` (`updated` ISO,
   `news_refreshed` today, `window`, optional `sources`). Then **append** the new
   items to the `## Previously shown` ledger
   (`- YYYY-MM-DD — Vendor — "headline" — URL`), prune entries older than 30
   days, cap ~300 lines. If web is unavailable, leave the file untouched
   (hard rule 4).

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
