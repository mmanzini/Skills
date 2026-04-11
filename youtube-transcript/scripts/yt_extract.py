#!/usr/bin/env python3
"""
Extract metadata, transcript and description links from a YouTube video.
Outputs a JSON object with: title, channel, video_url, raw_transcript, description_links.
"""

import sys
import json
import re
import subprocess
import urllib.request


def ensure_transcript_api():
    """Install youtube-transcript-api if not available."""
    try:
        import youtube_transcript_api  # noqa: F401
    except ImportError:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "youtube-transcript-api",
             "--break-system-packages", "-q"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )


def extract_video_id(url: str) -> str:
    """Parse a YouTube URL into a video ID."""
    patterns = [
        r"(?:v=|/v/|youtu\.be/)([a-zA-Z0-9_-]{11})",
        r"^([a-zA-Z0-9_-]{11})$",
    ]
    for pat in patterns:
        m = re.search(pat, url)
        if m:
            return m.group(1)
    raise ValueError(f"Could not extract video ID from: {url}")


def fetch_metadata(video_id: str) -> dict:
    """Get title and channel via oEmbed."""
    oembed_url = (
        f"https://www.youtube.com/oembed"
        f"?url=https://www.youtube.com/watch?v={video_id}&format=json"
    )
    req = urllib.request.Request(oembed_url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=15).read().decode()
    data = json.loads(resp)
    return {"title": data.get("title", ""), "channel": data.get("author_name", "")}


def fetch_transcript(video_id: str) -> str:
    """Fetch the transcript and return it as plain text with timestamps."""
    from youtube_transcript_api import YouTubeTranscriptApi

    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)
    lines = []
    for entry in transcript.snippets:
        mins = int(entry.start // 60)
        secs = int(entry.start % 60)
        lines.append(f"[{mins:02d}:{secs:02d}] {entry.text}")
    return "\n".join(lines)


def fetch_description_links(video_id: str) -> list[dict]:
    """
    Scrape the YouTube page HTML for ytInitialData and extract links
    from the video description. Returns a list of {text, url} dicts.
    """
    page_url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(page_url, headers={
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    })
    try:
        html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8")
    except Exception:
        return []

    match = re.search(
        r"var ytInitialData\s*=\s*({.*?});\s*</script>", html, re.DOTALL
    )
    if not match:
        return []

    try:
        data = json.loads(match.group(1))
    except json.JSONDecodeError:
        return []

    links = []
    try:
        contents = (
            data["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"]
        )
        for block in contents:
            renderer = block.get("videoSecondaryInfoRenderer")
            if not renderer:
                continue
            desc = renderer.get("attributedDescription", {})
            content = desc.get("content", "")
            runs = desc.get("commandRuns", [])
            for run in runs:
                cmd = run.get("onTap", {}).get("innertubeCommand", {})
                url_endpoint = cmd.get("urlEndpoint", {})
                if not url_endpoint:
                    continue
                raw_url = url_endpoint.get("url", "")
                # Resolve YouTube redirect URLs
                q_match = re.search(r"[?&]q=([^&]+)", raw_url)
                if q_match:
                    resolved = urllib.request.unquote(q_match.group(1))
                else:
                    resolved = raw_url
                # Skip YouTube-internal links
                if "youtube.com/redirect" in resolved:
                    continue
                start = run.get("startIndex", 0)
                length = run.get("length", 0)
                text = content[start:start + length].strip() if content else ""
                # Use URL as text if text is just a relative YouTube path
                if text.startswith("/"):
                    text = resolved
                links.append({"text": text, "url": resolved})
    except (KeyError, IndexError, TypeError):
        pass

    return links


def main():
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: yt_extract.py <youtube-url>"}))
        sys.exit(1)

    url = sys.argv[1]
    try:
        video_id = extract_video_id(url)
    except ValueError as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)

    ensure_transcript_api()

    result = {
        "video_id": video_id,
        "video_url": f"https://www.youtube.com/watch?v={video_id}",
    }

    # Metadata
    try:
        meta = fetch_metadata(video_id)
        result["title"] = meta["title"]
        result["channel"] = meta["channel"]
    except Exception as e:
        result["title"] = ""
        result["channel"] = ""
        result["metadata_error"] = str(e)

    # Transcript
    try:
        result["raw_transcript"] = fetch_transcript(video_id)
    except Exception as e:
        result["raw_transcript"] = ""
        result["transcript_error"] = str(e)

    # Description links
    try:
        result["description_links"] = fetch_description_links(video_id)
    except Exception as e:
        result["description_links"] = []
        result["links_error"] = str(e)

    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()