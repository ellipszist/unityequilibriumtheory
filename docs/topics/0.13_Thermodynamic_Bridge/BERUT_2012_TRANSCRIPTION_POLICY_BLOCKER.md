# Berut 2012 Transcription Policy Blocker

## Purpose

This file narrows the next `Berut 2012` provenance move inside `0.13`.

The current repo now knows two things at once:

1. the runtime Berut row is still only a topic-summary row
2. the currently visible Nature page surface looks like a figure-level preview rather than an exposed numeric table

That means the next blocker is no longer just `find the row`.
The repo has now chosen a conservative preferred policy path, so the blocker is narrower than a fully open policy choice.

## Current authority

- Machine-readable artifact: `Data/03_Research/berut_2012_transcription_policy_blocker.json`
- Supporting files:
  - `BERUT_2012_PROVENANCE_GAP.md`
  - `BERUT_2012_SOURCE_SURFACE_NOTE.md`

## Current policy decision

The topic now provisionally selects one explicit path:

1. `figure_level_locator_capture`
   declare one exact figure/panel locator as the current authoritative upstream surface

That locator is now attached in a dedicated follow-on note:

- `Figure 3: Erasure rate and approach to the Landauer limit.`

Other paths remain possible later, but they are no longer the current controller:

- `supplementary_capture` stays deferred until one exact supplementary identifier is visible
- `machine_transcription_from_nonpreview_surface` stays deferred until one non-preview numeric surface is actually archived

## Why this matters

With a declared conservative policy and one attached Figure 3 locator, the repo can now describe the next Berut move more narrowly without sounding more certain than the evidence allows.

The current preview surface supports:

- source identity
- abstract-level meaning
- visible figure labels

It does not yet support:

- direct row-table wording
- implied archival capture of a numeric source row
- one exact numeric point within the selected figure-level locator

## Current claim boundary

While this blocker remains open, `Berut 2012` may support only:

- summary-level lower-bound context
- propagated interval support on a topic-summary row
- one exact preview-level Figure 3 locator attached to that summary row

It must not support:

- row-level source-normalized closure
- wording that implies the upstream numeric row has already been directly archived
