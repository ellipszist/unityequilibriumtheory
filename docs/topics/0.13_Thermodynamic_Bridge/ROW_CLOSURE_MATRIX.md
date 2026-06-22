# Row Closure Matrix

## Purpose

This file explains the row-by-row closure state behind the current `0.13` provenance and uncertainty blockers.

It exists because the topic no longer has only one broad blocker.
Different rows are blocked for different reasons:

- missing raw or supplementary source rows
- missing row identifiers
- missing one authoritative upstream numeric surface or declared normalization policy
- missing source-backed uncertainty values
- unresolved source identity
- interval packages that currently include only mass uncertainty

## Current authority

- Machine-readable matrix: `Data/03_Research/row_closure_matrix.json`
- Supporting provenance workflow:
  - `Data/03_Research/source_evidence_intake_stub.json`
  - `Data/03_Research/source_evidence_readiness_matrix.json`
- Supporting uncertainty workflow:
  - `Data/03_Research/uncertainty_preprocessing_manifest.json`
  - `Data/03_Research/uncertainty_propagation_summary.json`

## Why this helps

Without a row-closure matrix, it is easy to say only that `0.13` has `source` and `uncertainty` blockers.
That is true but too broad.

The matrix makes the blocker chain narrower:

- `Berut` is blocked mainly by row-level provenance closure, and the repo now narrows that further by selecting `figure_level_locator_capture`, attaching `Figure 3` as the current preview-level locator, capturing the official Fig. 3 PPT route, binary identity, embedded raster candidates, digitization protocol, and automated panel-frame candidates, and stating that the remaining controller is now candidate-frame review plus tick/point mapping rather than locator/source-route/raster-asset/protocol choice itself
- `Jun` is no longer blocked by the legacy-row policy choice itself: the inherited `0.028 eV` row is now demoted to legacy context outside the active Jun lane. The remaining Jun controller is final PRL parity/APS access resolution for the now locally transcribed asymptotic-work summary.
- `Hong` is now narrower than candidate-branch intake only: the alternate source family is staged, the DOI metadata anchor is confirmed, an accessible same-author preprint precursor exposes multiple numeric candidates, and the topic now provisionally prefers the `4.2 +/- 0.9 zJ` temperature-series mean; final-source confirmation and the legacy-row keep/replace/remove policy are still open
- `Peterson` is blocked earlier, at composite source-reference resolution itself; the local `Peterson 2018` label is now also demoted because current evidence separates at least three incompatible candidate families behind it
- `LIGO` and `EHT` context rows already have partial interval support, but only from mass uncertainty
- measured-constant uncertainty is a cross-row support layer, not a single benchmark row

## Current row groups

| Group | Current state | Main blocker |
| :-- | :-- | :-- |
| Berut lower-bound summary row | Official Figure 3 PPT route, binary identity, embedded raster candidates, digitization protocol, and automated panel-frame candidates now captured under the selected figure-level policy | visual review of candidate panel frames, axis tick mapping, selected point/curve capture, or one stronger upstream source-data surface plus explicit mapping boundary |
| Jun lower-bound summary row | pinned source summary now has a summary-layer propagated interval, local arXiv Table I/Figure 4 transcription, and the legacy 0.028 eV row is demoted out of active Jun logic | resolve final PRL parity/APS access for the captured Table I/Figure 4 fit target tightly enough for stronger closure |
| Hong alternate-source candidate row | candidate source family staged, runtime-row reassignment not closed | primary DOI/article page plus exact source-facing numeric target |
| Peterson quantum branch | composite source-reference blocker with demoted local label | exact upstream source identity |
| LIGO/EHT gravity-context rows | first-pass intervals present | measured-constant and systematic terms still open |
| Measured-constant support layer | provenance anchor present | runtime uncertainty extraction and propagation policy |

## Use rule

Use this matrix when choosing the next `0.13` hardening move.
It is a blocker-navigation tool, not evidence of scientific closure.

