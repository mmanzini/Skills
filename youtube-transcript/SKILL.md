---
name: youtube-transcript
description: >
  Extract a YouTube video's transcript, metadata and useful links from the description,
  then produce a clean readable markdown document. Use this skill whenever the user wants
  to transcribe a YouTube video, extract text from a video, get a video transcript,
  convert a YouTube video to text or markdown, or grab content from a YouTube link.
  Trigger on any mention of YouTube transcripts, video-to-text, or requests involving
  YouTube URLs paired with words like "extract", "transcribe", "transcript", "text",
  "markdown", or "notes". Also use when the user provides a YouTube URL and asks to
  summarise, document, or capture what was said.
---

# YouTube Transcript Extractor

Extract a YouTube video's transcript, description and links, then transform the raw
captions into a clean, readable markdown document.

## Step 1: Extract raw data

Run the bundled extraction script. It handles metadata (title, channel), transcript
fetching, the full description text and description link scraping in one call:

```bash
python3 "$(dirname "$0")/scripts/yt_extract.py" "$URL"
```

Where `$URL` is the YouTube URL from `$ARGUMENTS`.

The script outputs a JSON object with these fields:
- `title` — video title
- `channel` — channel name
- `video_url` — canonical URL
- `description` — full plain-text description as shown on YouTube
- `raw_transcript` — timestamped transcript lines (`[MM:SS] text`)
- `description_links` — array of `{text, url}` from the video description

If there is a `transcript_error` field, tell the user the transcript could not be
extracted (the video may not have captions) and stop.

## Step 2: Transform the transcript into readable prose

This is the creative step. Take the `raw_transcript` and rewrite it into clean,
flowing text:

1. **Remove all timestamps.**
2. **Stitch fragmented subtitle lines** into complete sentences. YouTube auto-captions
   chop sentences at arbitrary points — rejoin them so they read naturally.
3. **Group sentences into paragraphs** by topic. When the speaker shifts to a new idea,
   start a new paragraph.
4. **Add section headings** (##) where the topic clearly changes. Use short, descriptive
   headings that reflect the content. If the `description` includes chapter markers
   (lines like `0:00 Intro`, `2:30 The Demo`), use those as a guide for section
   boundaries and heading names.
5. **Fix obvious speech-to-text errors** — e.g. "claw code" should be "Claude Code",
   "claw.md" should be "CLAUDE.md". Use context to correct brand names and technical
   terms that auto-captions commonly garble.
6. **Keep the speaker's voice.** Do not summarise, paraphrase, or editorialize. The
   output should read like a cleaned-up verbatim transcript, not a rewritten article.
7. **Use UK English** spelling (e.g. "behaviour", "colour", "organise").

## Step 3: Assemble the markdown file

Use this structure:

```markdown
# {title}

**Channel:** {channel}
**Video:** {video_url}

---

## Description

{description — reproduced verbatim, preserving line breaks and any chapter markers}

---

## {First section heading}

{Readable prose paragraphs...}

## {Next section heading}

{More paragraphs...}

---

## Useful links

- **{link text or label}**: {url}
- ...
```

Rules for the **Description** section:
- Reproduce it verbatim — do not summarise or reword.
- Preserve paragraph breaks and line breaks as they appear in the source.
- If the description is empty or not available, omit this section entirely.

Rules for the **Useful links** section:
- Only include links from `description_links` that are genuinely useful (articles,
  newsletters, repos, Discord, social profiles, courses, documentation).
- Skip generic YouTube links, subscriber links, or empty/broken URLs.
- Give each link a short bold label describing what it is (e.g. "AI Hero Newsletter",
  "Matt's Twitter/X").
- If `description_links` is empty, omit the links section entirely.

## Step 4: Save and present

1. Generate a filename from the video title: lowercase, replace spaces with hyphens,
   strip special characters, prefix with `transcript-`, e.g.
   `transcript-your-codebase-is-not-ready-for-ai.md`.
2. Save the file to the user's workspace folder.
3. Present the file to the user with a `computer://` link and a one-line summary of
   what the video covers.
