# data/*.md frontmatter schemas (canonical)

Match exactly — a renamed/removed key breaks the matching `Dashboard.js` method.

## tasks.md  (written by scripts/parse_tasks.py)
```yaml
updated: <ISO>
total_open: <int>
by_status: { <status>: <int>, ... }
items:
  - { id: T###, title: <str>, status: <str>, project: <str> }
```

## github-trends.md
```yaml
updated: <ISO>
items:
  - { repo: <str>, stars: <int>, delta: <int>, lang: <str> }
summary_week: <prose>
summary_month: <prose>
prediction: <prose>
investigate: [ <str>, ... ]
```

## ai-news.md  (prose + table, no chart)
```yaml
updated: <ISO>
news_refreshed: <YYYY-MM-DD>
window: "since <YYYY-MM-DD> (max 7d)"
items:                       # NEW items only (not in the body ledger), newest first, cap ~10
  - { vendor: <str>, headline: <str>, summary: <str>, url: <url>,
      date: <YYYY-MM-DD>, category: release|product|business|research|hardware|policy|funding|safety }
reaction: <prose>            # world-reaction recap (markets, press, community)
weekly_digest: <prose>       # always present: 7-day recap, includes previously-shown items
sources: [ <str>, ... ]      # optional
```
File **body** (below frontmatter) holds the dedup ledger — renderer ignores it:
```markdown
## Previously shown
- YYYY-MM-DD — Vendor — "headline" — https://…
```
Resolver reads it before writing (skip listed URLs), appends new items after,
prunes >30-day entries, caps ~300 lines.

## political-economy.md  (prose only, no chart)
```yaml
updated: <ISO>
news_refreshed: <YYYY-MM-DD>
summary_week: <prose>
summary_month: <prose>
prediction: <prose>
watch: [ <str>, ... ]
investigate: [ <str>, ... ]
sources: [ <str>, ... ]   # optional
```

## life.md
```yaml
as_of: <YYYY-MM-DD>
window_days: 14
happened: <prose>
now: <prose>
coming: <prose>
highlights: [ <str>, ... ]
actions: [ <str>, ... ]
prediction: <prose>
metrics:
  - { name: <str>, value: <num>, unit: <str>, history: [<num>, ...] }
```

## upcoming.md
```yaml
updated: <ISO>
items:
  - { title: <str>, due: <YYYY-MM-DD>, kind: deadline|event|idea|reminder }
```
