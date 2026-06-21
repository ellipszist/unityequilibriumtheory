# Berut 2012 Figure Locator Mapping

## Purpose

This file records the first exact locator captured under the selected `figure_level_locator_capture` policy for the `Berut 2012` row inside `0.13`.

The goal is narrower than row-level closure: name one exact visible figure locator on the currently accessible Nature preview surface and state exactly how far that locator is allowed to support the current runtime summary row.

## Current authority

- Machine-readable artifact: `Data/03_Research/berut_2012_figure_locator_mapping.json`
- Supporting files:
  - `BERUT_2012_SOURCE_SURFACE_NOTE.md`
  - `BERUT_2012_TRANSCRIPTION_POLICY_BLOCKER.md`
  - `BERUT_2012_TRANSCRIPTION_POLICY_DECISION.md`
  - `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`

## Selected preview locator

The currently visible Nature preview surface exposes this exact figure label:

- `Figure 3: Erasure rate and approach to the Landauer limit.`

Checked against the preview surface on `2026-06-21`.

## Why Figure 3 is the current best locator

Among the visible figure labels, `Figure 3` is the one that most directly names what the current local Berut summary row is trying to represent: a dissipated-heat quantity discussed relative to the Landauer limit.

This is a conservative figure-level locator only. It is not yet an archived numeric point, panel coordinate, or source-data row.

## Runtime mapping allowed by this locator

The current topic-summary runtime row is:

- `T = 300 K`
- `measured_heat_J = 3.0e-21`
- `error_J = 5.0e-22`

Under the current hardening boundary, `Figure 3` may support only this limited statement: the local Berut summary row is intended as a topic-level summary of the visible `approach to the Landauer limit` figure-level result, not as a claim that one exact numeric point or one exact source-table row has already been archived.

## What remains open

1. one numeric point, curve label, or panel-specific identifier within `Figure 3`
2. one machine-transcribed numeric value from that exact figure-level surface, or one stronger upstream numeric surface
3. one explicit rule showing how that figure-level support becomes the current runtime central value and uncertainty
4. one archived original file or supplement identifier if a stronger surface is later found

## New next controller

`figure_3_locator_captured_numeric_point_or_stronger_surface_still_required`

## Claim boundary

This file narrows the Berut blocker by attaching one exact visible figure locator and one explicit mapping boundary to the current runtime summary row. It does not yet provide row-level source normalization, machine-transcribed numeric closure, or a stronger upstream numeric surface.
