---
description: Get AI industry news from the last 24 hours or weekly digest if no breaking news
argument-hint: ""
---

# AI News Watcher

Monitor 20+ AI companies across Western and Asian markets for significant news from the last 24 hours. If no breaking news is found, provide a weekly digest of the most important updates from the past 7 days.

## Companies Monitored

**Foundation Models (Western)**: OpenAI, Anthropic, Google/DeepMind, Meta, Microsoft, xAI, Mistral, Cohere

**Foundation Models (Asian)**: Alibaba/Qwen, DeepSeek, ByteDance/Doubao, Baidu/ERNIE, Zhipu AI (GLM/ChatGLM), Moonshot AI (Kimi)

**Specialised Tools**: Perplexity, Midjourney, Runway, Stability AI, Character.AI, ElevenLabs, Hugging Face

## Workflow

### 1. Search for Breaking News (Last 24 Hours)

Use WebSearch to query each company with 3-5 diverse queries. Use the current month and year (check today's date) in date-scoped queries -- never hardcode a specific month.

**For Western companies:**
- "[Company] release [current month] [current year]"
- "[Company] announcement"
- "[Company] update site:[official-domain]"
- "[Company] beta launch"
- "[Company] security update"

**For Asian companies**, English-language coverage is thinner so cast a wider net:
- "[Company/Model name] release [current month] [current year]"
- "[Company/Model name] announcement new model"
- "[Company/Model name] update launch"
- "[Company/Model name] open source release"
- Search using the model name directly when it differs from the company name. For example, search "Qwen" not just "Alibaba", search "Kimi" not just "Moonshot", search "Doubao" not just "ByteDance", search "ERNIE" alongside "Baidu", and search "GLM" or "ChatGLM" alongside "Zhipu".

**Useful English-language sources for Asian AI news**: South China Morning Post, TechNode, Pandaily, 36Kr English, TechCrunch, The Information, Reuters, Bloomberg. These often cover Chinese AI releases faster than the companies' own English blogs.

Focus on official blogs, release notes, changelogs, and authoritative tech news sources.

### 2. Filter for Significance

Only keep items with these keywords in title or body:
- release, update, launch, beta, feature, security, deprecate, announce, breaking, new, open-source, benchmark, model

Verify publish dates are within last 24 hours using current date.

### 3. Deduplicate Using Cache

**Cache location**: Use the current session's outputs directory, e.g. `<outputs-dir>/.ai-news-cache.json`. Do not hardcode a specific session path.

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
🗞️ **AI News -- [DATE]**

• **[Vendor]:** "[Headline]" -- [one-line summary]
  🔗 [Read more]([URL])

• **[Vendor]:** "[Headline]" -- [one-line summary]
  🔗 [Read more]([URL])

(Show up to 5 items; if more than 5, add "+ N more")
```

**If no breaking news (weekly digest)**:

```
📰 **AI Weekly Digest -- [START DATE - END DATE]**

🔥 **Major Releases**
• **[Vendor]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

📢 **Product Updates**
• **[Vendor]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

💼 **Partnerships & Business**
• **[Vendor]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

📊 **Coverage**: OpenAI • Anthropic • Google • Microsoft • Meta • xAI • Mistral • Perplexity • Qwen • DeepSeek • ByteDance • Baidu • Zhipu AI • Moonshot AI • Midjourney • Runway • ElevenLabs • Hugging Face
```

### 5. Categorisation Rules

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
- Prioritise official sources over Reddit, forums, or low-quality aggregators
- If unsure about publish date, use WebFetch to check the article directly
- For Asian companies, English-language sources are preferred but Chinese-language official announcements can be cited if no English coverage exists
