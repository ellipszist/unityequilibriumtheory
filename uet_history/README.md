# UET History

`uet_history/` is the curated public history workspace for UET theory notes,
book-development material, digests, and publishable narrative work.

This folder no longer exposes the old legacy tree (`documents/`, `equations/`,
`media/`, `obsolete/`, `research/`, `theory/`) as the current public structure.
Those older paths were useful during recovery, but they mixed raw notes, media,
experiments, and historical drafts in a way that made the repository hard to
read.

## Current Public Structure

```text
uet_history/
  2_digest/       # reviewed summaries, indexes, and structured digests
  3_publish/      # publishable drafts, book structure, and public narrative work
  PIPELINE.md     # raw -> digest -> publish workflow boundary
  PUBLIC_MANIFEST.md
  STATUS_REPORT.md
```

## What Is Intentionally Excluded

Raw folders and private/local source material are not committed here by default.
That includes chat exports, transcript dumps, large media, audio, PDFs, ZIPs,
local archives, and old development snapshots.

Excluded local areas include:

- `uet_history/1_raw/`
- `uet_history/_archive/`
- `uet_history/Dev_history/`
- any nested `1_raw/` folders inside publish work
- large media, audio, video, PDF, ZIP, and cache-like files

Use `PUBLIC_MANIFEST.md` to see what this public tree includes and excludes.