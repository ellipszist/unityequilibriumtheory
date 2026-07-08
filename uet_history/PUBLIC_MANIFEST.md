# UET History Public Manifest

**Updated:** 2026-07-08
**Purpose:** Replace the old public `uet_history` tree with a curated structure
that reflects the current local workflow without publishing raw folders.

## Included In This Public Update

| Path | Status | Notes |
| --- | --- | --- |
| `uet_history/README.md` | included | Public orientation for the current history workspace. |
| `uet_history/PIPELINE.md` | included | Raw -> digest -> publish workflow boundary. |
| `uet_history/STATUS_REPORT.md` | included | Current public status summary. |
| `uet_history/2_digest/README.md` | included | Digest-layer orientation. |
| `uet_history/2_digest/_index.json` | included | Empty digest registry scaffold. |
| `uet_history/3_publish/README.md` | included | Publish-layer orientation. |
| `uet_history/3_publish/books/README.md` | included | Book workspace orientation. |
| `uet_history/3_publish/books/00_uet_core_theory/README.md` | included | Core UET theory book placeholder. |
| `uet_history/3_publish/books/origin_of_wealth_and_economics/README.md` | included | Public concept outline for the economics and wealth-origin book track. |
| `uet_history/3_publish/books/origin_of_wealth_and_economics/the_origin_of_wealth_book_blueprint.md` | included | Working public blueprint for review; not treated as a validated economics result. |

## Excluded From This Public Update

| Local area | Reason |
| --- | --- |
| `uet_history/1_raw/` | Raw conversations, notes, transcripts, and source dumps need privacy and provenance review before publication. |
| `uet_history/_archive/` | Local archive and recovery material; not a current public source tree. |
| `uet_history/Dev_history/` | Contains raw development snapshots, ZIPs, videos, and large historical assets. |
| nested `1_raw/` folders inside `3_publish/` | Draft input material; not yet reviewed as public-safe. |
| remaining economics and wealth-origin book drafts | The public outline and blueprint are included, but remaining local drafts still need encoding, claim-strength, source-boundary, and raw/draft review before promotion. |
| media/audio/video/PDF/ZIP files | Large or potentially private assets; should be handled by a separate asset plan. |

## Legacy Paths Retired From Main

The older public paths below are removed from the current `main` tree in this
update because they represented a mixed legacy archive rather than the current
curated workflow:

- `uet_history/documents/`
- `uet_history/equations/`
- `uet_history/media/`
- `uet_history/obsolete/`
- `uet_history/research/`
- `uet_history/theory/`

This does not mean the historical material is erased from Git history. It means
those paths are no longer the active public organization model.
