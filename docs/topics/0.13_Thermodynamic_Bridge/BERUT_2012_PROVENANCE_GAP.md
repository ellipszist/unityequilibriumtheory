# Berut 2012 Provenance Gap

## Purpose

This file isolates the current `Berut 2012` blocker inside the `0.13` Landauer lane.

Unlike `Jun 2014`, the Berut row already has an attached uncertainty and propagated interval.
Its main problem is row-level provenance closure rather than missing uncertainty capture.
The new source-surface note narrows one part of that problem again: the currently visible Nature page surface behaves like a figure-level preview rather than an exposed numeric row table.
The new transcription-policy blocker narrowed it one step further, and the new figure-locator mapping note narrows it again: the repo now fixes `Figure 3` as the current preview-level locator, so the remaining Berut gap is no longer locator choice but numeric-point capture or one stronger upstream numeric surface.

## Current authority

- Machine-readable artifact: `Data/03_Research/berut_2012_provenance_gap.json`
- Supporting files:
  - `Data/03_Research/source_evidence_intake_stub.json`
  - `Data/03_Research/source_evidence_readiness_matrix.json`
  - `Data/03_Research/uncertainty_preprocessing_manifest.json`
  - `Data/03_Research/uncertainty_propagation_summary.json`
  - `LANDAUER_ROW_CONTRACT.md`
  - `BERUT_2012_SOURCE_SURFACE_NOTE.md`
  - `BERUT_2012_TRANSCRIPTION_POLICY_BLOCKER.md`

## Current runtime state

- runtime value: `3.0e-21 J`
- runtime uncertainty: `5.0e-22 J`
- lower-bound comparator at `300 K`: `2.870978885078724e-21 J`
- current status: propagated interval exists, but only on a topic-summary row

## Minimum closure rule for this row

Do not treat `Berut 2012` as source-normalized unless the topic package has:

1. a stable source identity
2. an archived source file or supplement identifier
3. one numeric point, curve label, or panel-specific identifier within the selected `Figure 3` locator
4. one stronger upstream numeric surface or one machine-transcribed numeric capture if no direct table is exposed
5. a machine-transcribed or archived source row
6. an explicit mapping from that source row into the runtime summary value and uncertainty

## Current claim boundary

While this gap remains open, `Berut 2012` may support only:

- summary-level lower-bound context
- propagated interval attached to a topic-summary row

It must not support:

- row-level source-normalized Landauer closure
- stronger provenance wording than the current summary-row status allows

## Use rule

Use this file when selecting the next narrow hardening move for `0.13`.
It is a blocker-navigation note, not a promotion artifact.
