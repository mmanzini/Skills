# AI News Watcher

Monitor 15+ AI companies for significant news from the last 24 hours. If no breaking news is found, provide a weekly digest of the most important updates from the past 7 days.

## Companies Monitored

**Foundation Models**: OpenAI, Anthropic, Google/DeepMind, Meta, Microsoft, xAI, Mistral, Cohere

**Specialized Tools**: Perplexity, Midjourney, Runway, Stability AI, Character.AI, ElevenLabs, Hugging Face

## Workflow

### 1. Search for Breaking News (Last 24 Hours)

Use WebSearch to query each company with 3-5 diverse queries:
- "[Company] release February 2026"
- "[Company] announcement"
- "[Company] update site:[official-domain]"
- "[Company] beta launch"
- "[Company] security update"

Focus on official blogs, release notes, changelogs, and authoritative tech news sources.

### 2. Filter for Significance

Only keep items with these keywords in title or body:
- release, update, launch, beta, feature, security, deprecate, announce, breaking, new

Verify publish dates are within last 24 hours using current date.

### 3. Deduplicate Using Cache

**Cache location**: `/sessions/keen-quirky-meitner/mnt/outputs/.ai-news-cache.json`

**Cache format**:
```json
{
  "urls": {
    "https://example.com/article": "2026-02-10"
  },
  "last_cleanup": "2026-02-10"
}
```

**Process**:
1. Load cache (create if missing)
2. Skip any URL already in cache
3. Add new URLs with today's date
4. Remove entries older than 7 days
5. Keep max 1000 entries
6. Save updated cache

### 4. Output Format

**If breaking news found (last 24h)**:

```
🗞️ **AI News — [DATE]**

• **[Vendor]:** "[Headline]" — [one-line summary]
  🔗 [Read more]([URL])

• **[Vendor]:** "[Headline]" — [one-line summary]
  🔗 [Read more]([URL])

(Show up to 5 items; if more than 5, add "+ N more")
```

**If no breaking news (weekly digest)**:

```
📰 **AI Weekly Digest — [START DATE - END DATE]**

🔥 **Major Releases**
• **[Vendor]** ([Date]): [Headline] — [summary]
  🔗 [Read more]([URL])

📢 **Product Updates**
• **[Vendor]** ([Date]): [Headline] — [summary]
  🔗 [Read more]([URL])

💼 **Partnerships & Business**
• **[Vendor]** ([Date]): [Headline] — [summary]
  🔗 [Read more]([URL])

📊 **Coverage**: OpenAI • Anthropic • Google • Microsoft • xAI • Perplexity • Mistral • Midjourney • Runway
```

### 5. Categorization Rules

**Major Releases**:
- New models or major version launches
- Breakthrough features
- Complete rewrites or architecture changes

**Product Updates**:
- Feature updates and improvements
- Beta releases
- Performance enhancements
- UI/UX updates

**Partnerships & Business**:
- Acquisitions and mergers
- Strategic integrations
- Major business deals
- Corporate restructuring

## Ranking Priority

1. Official announcements > tech news > aggregators
2. Freshness (newer first within category)
3. Headline relevance to keywords

## Important Rules

- Never show the same URL twice within 7 days
- Be strict about the 24-hour window for breaking news
- Each item MUST have a clickable "🔗 Read more" link with the full URL
- Prioritize official sources over Reddit, forums, or low-quality aggregators
- If unsure about publish date, use WebFetch to check the article directly