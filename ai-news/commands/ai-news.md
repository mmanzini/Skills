---
description: Get AI industry news from the last 24 hours plus an always-on weekly digest (models, tooling, hardware, policy, funding, research)
argument-hint: ""
---

# AI News Watcher

Monitor 40+ AI companies, labs, and policy bodies across Western and Asian markets for significant news from the last 24 hours, then always close with a weekly digest of the most important updates from the past 7 days.

## Coverage

**Foundation Models (Western)**: OpenAI, Anthropic, Google/DeepMind, Meta, Microsoft, xAI, Mistral, Cohere, Amazon (Nova), Apple, AI2 (Allen Institute)

**Foundation Models (Asian)**: Alibaba/Qwen, DeepSeek, ByteDance/Doubao, Baidu/ERNIE, Zhipu AI (GLM/ChatGLM), Moonshot AI (Kimi), Tencent (Hunyuan), MiniMax, 01.AI (Yi), StepFun

**Agent & Dev Tooling**: Cursor, Cognition (Devin), Replit, GitHub Copilot, Windsurf, OpenHands

**Specialised Tools**: Perplexity, Midjourney, Runway, Stability AI, Character.AI, ElevenLabs, Hugging Face

**Hardware & Infrastructure**: Nvidia, AMD, Groq, Cerebras, TSMC (AI-relevant), CoreWeave

**Policy & Regulation**: EU AI Act developments, US executive/Congressional actions, China AI regulations, UK AISI and other safety institutes

**Funding & Business**: major funding rounds, acquisitions, valuation news across the AI sector

**Research & Safety**: notable papers, new benchmarks, safety-institute and lab safety reports

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

**For agent/dev tooling:**
- "[Tool] release [current month] [current year]"
- "[Tool] new feature agent"
- "[Tool] changelog update"

**For hardware/infra:**
- "[Company] AI chip announcement [current month] [current year]"
- "[Company] datacenter GPU launch"

**For policy/regulation:**
- "EU AI Act [current month] [current year]"
- "AI regulation announcement [current month] [current year]"
- "AI executive order congress bill"
- "China AI regulation [current year]"

**For funding & business:**
- "AI startup funding round [current month] [current year]"
- "AI acquisition [current month] [current year]"

**For research & safety:**
- "AI benchmark paper [current month] [current year]"
- "AI safety institute report [current month] [current year]"

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

**If breaking news found (last 24h)**, lead with it:

```
🗞️ **AI News -- [DATE]**

• **[Vendor]:** "[Headline]" -- [one-line summary]
  🔗 [Read more]([URL])

• **[Vendor]:** "[Headline]" -- [one-line summary]
  🔗 [Read more]([URL])

(Show up to 5 items; if more than 5, add "+ N more")
```

**Weekly digest (ALWAYS included — after breaking news if any, alone otherwise)**:

```
📰 **AI Weekly Digest -- [START DATE - END DATE]**

🔥 **Major Releases**
• **[Vendor]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

📢 **Product Updates**
• **[Vendor]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

💼 **Partnerships & Business / Funding**
• **[Vendor]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

🔬 **Research & Safety**
• **[Lab/Body]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

🖥️ **Hardware & Infrastructure**
• **[Vendor]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

🏛️ **Policy & Regulation**
• **[Body]** ([Date]): [Headline] -- [summary]
  🔗 [Read more]([URL])

(Omit any category with no items this week.)

📊 **Coverage**: OpenAI • Anthropic • Google • Microsoft • Meta • xAI • Mistral • Amazon • Apple • AI2 • Perplexity • Qwen • DeepSeek • ByteDance • Baidu • Zhipu AI • Moonshot AI • Tencent • MiniMax • 01.AI • StepFun • Cursor • Cognition • Replit • Copilot • Windsurf • Midjourney • Runway • ElevenLabs • Hugging Face • Nvidia • AMD • Groq • Cerebras • CoreWeave • Policy (EU/US/CN/UK)
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

**Partnerships & Business / Funding**:
- Acquisitions and mergers
- Strategic integrations
- Major business deals and funding rounds
- Corporate restructuring

**Research & Safety**:
- Notable papers and new benchmarks
- Safety-institute and lab safety reports
- Significant open-source research releases

**Hardware & Infrastructure**:
- Chip launches and roadmaps
- Datacenter/compute buildouts and capacity deals

**Policy & Regulation**:
- New laws, regulations, executive actions
- Enforcement actions and major government AI initiatives

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
