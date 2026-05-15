# PDF Pipeline

Two halves:

1. How to walk the user through exporting their design template as a numbered PDF.
2. How you convert that PDF into one numbered PNG per page.

## Half 1 — Export from the design tool

Only relevant in Phase 0 if the user is on the **No** path (they haven't exported yet). If they're on the **Yes** path, skip ahead.

Walk them through:

1. **Open the design tool.** Locate the finished template.
2. **Confirm every page is numbered.** Each layout should display its serial number visibly (most design templates do this by default in the corner). The number is the stable identifier — the generated skill's handoff will cite layouts by this number.
3. **Export → PDF.** In the design tool's export menu, choose PDF. If asked about quality, choose the highest available.
4. **Save to a known path.** `~/Downloads/` is fine.
5. **Tell me the absolute path** when ready.

If the template doesn't have numbered pages, stop. The user needs to add page numbers in the design tool first. The skill will not work without them.

If the design tool's export doesn't include all pages (sometimes a draft page or unfinished page is excluded), tell the user to open the PDF, count pages, and confirm the count matches their template.

## Half 2 — Convert PDF to PNGs (300 DPI)

This runs in Phase 3 after the user provides the PDF path.

### Tool: `pdftoppm` (poppler-utils)

If `pdftoppm` is not installed:

```bash
brew install poppler
```

Surface the install command and run it once. After install, `pdftoppm` is available system-wide.

### Per-page rendering

For a PDF with N pages, render each page separately to an output PNG:

```bash
pdftoppm -r 300 -png -f {page-num} -l {page-num} -singlefile "{pdf-path}" "{output-no-ext}"
```

Where:
- `-r 300` = 300 DPI (the standard for clean rendering at typical viewer resolutions)
- `-png` = PNG output
- `-f N -l N -singlefile` = render only page N, skip the suffix `pdftoppm` would otherwise append
- `{output-no-ext}` = output path without `.png` (the tool appends it automatically)

### Bulk render script

For convenience, in Bash:

```bash
PDF="{pdf-path}"
OUT_DIR="$HOME/Downloads/{slug}/assets/templates/_unsorted"
mkdir -p "$OUT_DIR"
PAGES=$(pdfinfo "$PDF" | awk '/^Pages:/ {print $2}')
for i in $(seq 1 "$PAGES"); do
  PADDED=$(printf "%02d" "$i")
  pdftoppm -r 300 -png -f "$i" -l "$i" -singlefile "$PDF" "$OUT_DIR/$PADDED-temp"
done
```

This produces `01-temp.png`, `02-temp.png`, ..., padded to 2 digits so file sort order matches page order.

### Adjust DPI if file size is a concern

300 DPI on a typical 16:9 slide produces ~6000×3375 px PNGs (≈1-3 MB each). If the user's template has 30+ pages and they're concerned about disk usage, drop to 200 DPI. Quality stays acceptable for most viewer resolutions.

### Verify output

After rendering, count the PNGs and confirm they match the page count.

```bash
ls "$OUT_DIR" | wc -l
```

If the count is off, the PDF probably failed mid-render. Re-run.

### Skip pages on user request

If the user said in Phase 2 to skip cover / divider / TOC pages, omit them from the loop. Track which page numbers were skipped — the generated skill's plot.md should not reference IDs that don't exist.

### Rename + relocate (Phase 5, not Phase 3)

In Phase 3 the filenames are `{padded-page-num}-temp.png`. In Phase 5, after categories and slugs are confirmed, rename to `{page-num}-{slug}.png` (no padding needed in the final filename — the user-facing ID matches the numeric template page number) and move into the correct category subfolder.

Example flow:
- Phase 3 output: `01-temp.png`, `02-temp.png`, ..., `27-temp.png` in `_unsorted/`
- Phase 4 output: a mapping `01 → "01-pyramid" → category "03-hierarchy"`, etc.
- Phase 5 actions:
  - `mv _unsorted/01-temp.png ../03-hierarchy/01-pyramid.png`
  - ...
  - `rmdir _unsorted/`
