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

- `Berut` is blocked mainly by row-level provenance closure, and the repo now narrows that further by selecting `figure_level_locator_capture`, attaching `Figure 3` as the current preview-level locator, and stating that the remaining controller is now numeric-point capture or one stronger upstream numeric surface rather than locator choice itself
- `Jun` is blocked not only by branch identity, but now by the remaining policy/file-identity step after first-pass interval threading: the pinned `Jun 2014` asymptotic-work summary now carries a summary-layer interval, yet it still does not numerically match the legacy `0.028 eV` runtime row under the current `300 K` verifier baseline
- `Hong` is now narrower than candidate-branch intake only: the alternate source family is staged, the DOI metadata anchor is confirmed, an accessible same-author preprint precursor exposes multiple numeric candidates, and the topic now provisionally prefers the `4.2 +/- 0.9 zJ` temperature-series mean; final-source confirmation and the legacy-row keep/replace/remove policy are still open
- `Peterson` is blocked earlier, at composite source-reference resolution itself; the local `Peterson 2018` label is now also demoted because current evidence separates at least three incompatible candidate families behind it
- `LIGO` and `EHT` context rows already have partial interval support, but only from mass uncertainty
- measured-constant uncertainty is a cross-row support layer, not a single benchmark row

## Current row groups

| Group | Current state | Main blocker |
| :-- | :-- | :-- |
| Berut lower-bound summary row | Figure 3 preview locator now mapped to the topic-summary row under the selected figure-level policy | numeric point/curve capture within Figure 3, or one stronger upstream numeric surface plus explicit mapping boundary |
| Jun lower-bound summary row | pinned source summary now has a summary-layer propagated interval, but it still conflicts quantitatively with the legacy runtime row | split/replace/relabel the legacy runtime row, then archive the source-summary file/row identity tightly enough for stronger closure |
| Hong alternate-source candidate row | candidate source family staged, runtime-row reassignment not closed | primary DOI/article page plus exact source-facing numeric target |
| Peterson quantum branch | composite source-reference blocker with demoted local label | exact upstream source identity |
| LIGO/EHT gravity-context rows | first-pass intervals present | measured-constant and systematic terms still open |
| Measured-constant support layer | provenance anchor present | runtime uncertainty extraction and propagation policy |

## Use rule

Use this matrix when choosing the next `0.13` hardening move.
It is a blocker-navigation tool, not evidence of scientific closure.

