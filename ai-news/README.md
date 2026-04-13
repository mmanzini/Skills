# AI News Plugin

Monitor 20+ AI companies across Western and Asian markets for significant news.

## Commands

- `/ai-news` -- Fetch breaking AI news from the last 24 hours, or a weekly digest if nothing dropped recently.

## Companies Covered

**Western**: OpenAI, Anthropic, Google/DeepMind, Meta, Microsoft, xAI, Mistral, Cohere

**Asian**: Alibaba/Qwen, DeepSeek, ByteDance/Doubao, Baidu/ERNIE, Zhipu AI (GLM/ChatGLM), Moonshot AI (Kimi)

**Specialised Tools**: Perplexity, Midjourney, Runway, Stability AI, Character.AI, ElevenLabs, Hugging Face

## Usage

Run `/ai-news` in any session. The command uses WebSearch to check for news, deduplicates against a local cache, and returns a formatted digest.

## Version History

- **1.1.0** -- Added 6 Asian AI companies (Qwen, DeepSeek, ByteDance, Baidu, Zhipu AI, Moonshot AI), fixed dynamic date handling, fixed cache path, expanded significance filter keywords.
- **1.0.0** -- Initial release with Western AI company coverage.
