#!/usr/bin/env python3
"""
daily_metrics.py — deterministic metric-series extractor for the Life section.

Reads the last N daily notes (Resources/Daily/, with Intelligence/daily/ as an
additional source) and pulls the Figures lines into chronological series. Emits
JSON to stdout for the `life` resolver to drop into data/life.md `metrics:`.

Usage: python3 Skills/dashboard-refresh/scripts/daily_metrics.py [N]
       (default N = 12)
"""
import re
import sys
import json
import glob
from pathlib import Path

VAULT = Path(__file__).resolve().parents[3]
RES_DAILY = VAULT / "Resources" / "Daily"
INT_DAILY = VAULT / "Intelligence" / "daily"

PATTERNS = {
    "Claude active time": (r"screen-time:\s*([\d.]+)\s*min", "min"),
    "Prompts sent":       (r"Prompts sent:\s*(\d+)", ""),
    "Files edited":       (r"Files edited:\s*(\d+)", ""),
    "Emails received":    (r"Emails:\s*(\d+)\s*received", ""),
    "Email signal":       (r"—\s*(\d+)\s*signal", ""),
}
DATE_RE = re.compile(r"(\d{4}-\d{2}-\d{2})\.md$")


def daily_files():
    """Map date -> path, preferring Resources/Daily, falling back to Intelligence/daily."""
    files = {}
    for base in (INT_DAILY, RES_DAILY):  # RES_DAILY second so it wins on overlap
        for p in glob.glob(str(base / "**" / "*.md"), recursive=True):
            m = DATE_RE.search(p)
            if m:
                files[m.group(1)] = p
    return files


def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    files = daily_files()
    dates = sorted(files)[-n:]
    series = {name: [] for name in PATTERNS}
    for d in dates:
        text = Path(files[d]).read_text(encoding="utf-8", errors="replace")
        for name, (pat, _unit) in PATTERNS.items():
            m = re.search(pat, text)
            series[name].append(round(float(m.group(1)), 1) if m else None)

    metrics = []
    for name, (_pat, unit) in PATTERNS.items():
        hist = [v for v in series[name] if v is not None]
        if not hist:
            continue
        val = hist[-1]
        if unit == "" and val == int(val):
            val = int(val)
        metrics.append({"name": name, "value": val, "unit": unit, "history": hist})

    print(json.dumps({"as_of": dates[-1] if dates else None,
                      "window_dates": dates, "metrics": metrics}, indent=2))


if __name__ == "__main__":
    main()
