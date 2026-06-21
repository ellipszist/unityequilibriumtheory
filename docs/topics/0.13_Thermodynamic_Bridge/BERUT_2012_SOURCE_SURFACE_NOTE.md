# Berut 2012 Source Surface Note

## Purpose

This file narrows one part of the `Berut 2012` provenance blocker inside `0.13`.

The earlier blocker wording said that the row locator was still missing.
This note makes that statement more specific:
the currently visible primary page surface does not yet look like an exposed numeric table surface.

## Current authority

- Machine-readable artifact: `Data/03_Research/berut_2012_source_surface_note.json`
- Supporting source record:
  - `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`

## Current primary-surface observation

On the currently accessible Nature preview surface for `10.1038/nature10872`, the repo can directly see:

- the abstract
- `Figure 1`
- `Figure 2`
- `Figure 3`

The same visible preview surface does not currently expose:

- a directly visible numeric row table
- a source-data table
- a directly visible supplementary-file identifier

This is a statement about the currently visible preview surface only.
It is not proof that no supplementary material exists behind the access wall.

## Why this matters

This narrows the blocker chain.

Instead of saying only `row label missing`, the topic can now say something more precise:

- the visible primary surface currently behaves like a figure-level preview
- so row-level closure may require one of:
  1. supplementary capture
  2. figure-level locator capture
  3. explicit machine-transcription policy from a non-preview source surface

## Current claim boundary

While this note remains open, `Berut 2012` may support only:

- summary-level lower-bound context
- propagated interval support on a topic-summary row

It must not support:

- row-level source-normalized closure
- wording that implies a directly archived source row already exists
