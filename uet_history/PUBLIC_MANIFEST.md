# UET History Public Manifest

**Updated:** 2026-07-16
**Purpose:** Describe the curated public history tree and keep its paths
aligned with the local book workflow.

## Included in the public tree

| Path | Status | Notes |
| --- | --- | --- |
| `uet_history/README.md` | included | Public orientation for the history workspace. |
| `uet_history/PIPELINE.md` | included | Raw -> digest -> publish boundary. |
| `uet_history/STATUS_REPORT.md` | included | Public status summary. |
| `uet_history/3_publish/books/README.md` | included | Shared book path and publication rules. |
| `uet_history/3_publish/books/BOOK_REGISTRY.json` | included | Machine-readable registry for every known book track. |
| `uet_history/3_publish/books/00_uet_core_theory/README.md` | included | Core theory scaffold. |
| `uet_history/3_publish/books/0.1 Econmi - The Origin of Wealth/README.md` | included | Canonical public entry point for Book 1. |
| `uet_history/3_publish/books/0.1 Econmi - The Origin of Wealth/book_1_blueprint.md` | included | Curated Book 1 blueprint from the canonical working folder. |

## Path and source policy

`uet_history/3_publish/books/BOOK_REGISTRY.json` is the controlling map. The
existing numbered or named folder wins when a duplicate public path appears.
The registry must be updated before a new book path is introduced.

Raw conversations, source dumps, media, audio, PDFs, archives, and nested
`1_raw/` or `ch_drafts/` folders remain local-only unless explicitly listed as
reviewed public files.

## Local-only book tracks

The registry records the local source paths for the other book tracks without
pretending that their drafts are already public. This separates discoverability
from publication and prevents a missing public file from being mistaken for a
missing local project.

## Retired duplicate

`uet_history/3_publish/books/origin_of_wealth_and_economics/` was a duplicate
public alias for Book 1. It is removed from the active public tree; its Git
history remains available.
