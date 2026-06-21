# Berut 2012 Transcription Policy Decision

## Purpose

This file records the current conservative policy choice for how `0.13` should
handle the `Berut 2012` row while the accessible Nature surface still behaves
like a figure-level preview.

The repo no longer needs to leave the policy choice fully open.
Given the current evidence, the most conservative next move is to prefer a
figure-level locator policy rather than pretending that a direct row table or a
non-preview machine transcription surface is already in hand.

## Current authority

- Machine-readable artifact:
  `Data/03_Research/berut_2012_transcription_policy_decision.json`
- Supporting files:
  - `BERUT_2012_SOURCE_SURFACE_NOTE.md`
  - `BERUT_2012_TRANSCRIPTION_POLICY_BLOCKER.md`
  - `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`

## Chosen policy

- selected policy:
  `figure_level_locator_capture`
- current rationale:
  the visible primary surface exposes figure labels but not a directly visible
  numeric row table or supplementary identifier

## Why this policy is preferred now

### Preferred over `supplementary_capture`

A supplementary file may still exist, but the currently archived evidence does
not yet expose one exact supplementary identifier.
So supplementary capture remains a possible future improvement, not the current
controlling next move.

### Preferred over `machine_transcription_from_nonpreview_surface`

The repo does not yet have one archived non-preview numeric surface to
transcribe from.
Choosing machine transcription now would risk sounding as if a stronger surface
already exists.

### Preferred over leaving the policy fully open

Leaving the policy open keeps the Berut blocker broader than necessary.
The current preview evidence already supports one narrower and auditable next
step: identify one exact figure or panel locator, then map that locator to the
runtime summary row conservatively. That follow-on step is now completed at the
figure-label level by attaching `Figure 3`.

## New next controller after this decision

After this policy choice, the next Berut controller becomes:

`figure_3_locator_captured_numeric_point_or_stronger_surface_still_required`

That means the next useful artifact should name:

1. one exact figure locator (`Figure 3`)
2. the exact runtime summary quantity that locator is allowed to support
3. the remaining boundary between figure-level support and numeric-point or stronger-surface closure

## Claim boundary

This decision narrows the Berut blocker by selecting one conservative evidence
path.
It does not yet provide a row-level source capture, a direct numeric table, or a
fully source-normalized Berut benchmark row.
