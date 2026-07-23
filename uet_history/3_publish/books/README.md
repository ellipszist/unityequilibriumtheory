# UET Book Workspace

This directory is the public-facing book workspace. `BOOK_REGISTRY.json` is
the source of truth for book identity, canonical paths, public paths, and
publication state.

## Path rule

Existing book folders are canonical. Agents must inspect this directory and
the registry before creating a path. A new semantic alias for an existing book
is not allowed.

The working source and public output use the same book identity. Raw material
and chapter drafts may remain local, but they must not be silently replaced by
a renamed public copy.

## Current public tree

| Book | Public path | State |
| --- | --- | --- |
| Core UET theory | `00_uet_core_theory/` | curated scaffold |
| The Origin of Wealth | `0.1 Econmi - The Origin of Wealth/` | curated blueprint |

The remaining book tracks are recorded in `BOOK_REGISTRY.json` as local-only
until their reviewed public files are promoted. The previous
`origin_of_wealth_and_economics/` path was a duplicate alias and is retired.

## Publication workflow

1. Update the existing canonical book folder.
2. Keep `1_raw/` and `ch_drafts/` outside the public file list.
3. Update the registry state and public file list.
4. Commit the coherent book change and verify the public `main` path.

One workflow applies to every book. A book-specific change must not create a
book-specific directory convention.
