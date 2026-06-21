# Jun 2014 Uncertainty Gap

## Purpose

This file isolates the current `Jun 2014` blocker inside the `0.13` Landauer lane.

The broader row-closure and Landauer-row contracts already show that `Jun` is open.
This file exists to say exactly what still keeps the current `Jun` lane below stronger source-normalized closure even after first-pass interval threading.

## Current authority

- Machine-readable artifact: `Data/03_Research/jun_2014_uncertainty_gap.json`
- Supporting files:
  - `Data/03_Research/source_evidence_intake_stub.json`
  - `Data/03_Research/source_evidence_readiness_matrix.json`
  - `Data/03_Research/uncertainty_preprocessing_manifest.json`
  - `Data/03_Research/uncertainty_propagation_summary.json`
  - `LANDAUER_ROW_CONTRACT.md`

## Current runtime state

- source-facing summary value used by the verifier: about `0.01835 eV`
- lower-bound comparator at `300 K`: `0.0179192407638041 eV`
- current status: summary-layer interval present
- current gap: the interval is attached to a pinned source summary, but the legacy `0.028 eV` row is still mixed-lineage context and the summary/file identity is not yet closed tightly enough for stronger source-normalized use

## Minimum closure rule for this row

Do not treat `Jun 2014` as uncertainty-closed unless the topic package has:

1. a stable source identity
2. a declared policy that keeps the legacy `0.028 eV` row out of the Jun closure lane unless a different Jun quantity is justified
3. a row or table locator, or at minimum a tighter original-file identity for the pinned source-facing summary
4. an explicit mapping from that source-facing quantity into the runtime `eV` value
5. confirmation that the attached propagated interval corresponds to that same quantity

## Current claim boundary

While this gap remains open, `Jun 2014` may support:

- summary-layer interval-bearing lower-bound context

It must not support:

- row-level source-normalized Jun closure
- multi-row interval-based promotion of the Landauer lane

## Use rule

Use this file when selecting the next narrow hardening move for `0.13`.
It is a blocker-navigation note, not a promotion artifact.
