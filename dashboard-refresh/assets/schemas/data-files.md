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
