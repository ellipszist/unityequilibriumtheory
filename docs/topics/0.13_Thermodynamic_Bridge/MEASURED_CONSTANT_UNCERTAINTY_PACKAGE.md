# Measured Constant Uncertainty Package

## Purpose

This file isolates the current `measured-constant uncertainty` blocker inside the gravity-adjacent uncertainty lane of `0.13`.

The topic already had a provenance anchor for non-exact constants such as `G`.
What it did not have was a topic-local runtime package stating:

- which measured constants matter in the current verifier
- which direct CODATA 2022 numeric uncertainty extract is currently used
- which rows would inherit that uncertainty
- whether that uncertainty is already threaded into the published intervals

## Current authority

- Machine-readable artifact: `Data/03_Research/measured_constant_uncertainty_package.json`
- Supporting files:
  - `docs/data/external/constants/codata/measured_constants_2022_source_record.json`
  - `docs/data/external/constants/codata/codata_2022_measured_constants_extract.json`
  - `Data/03_Research/uncertainty_propagation_summary.json`
  - `ROW_CLOSURE_MATRIX.md`

## Current runtime state

- provenance anchor for measured constants: present
- current runtime uncertainty extract for `G`: direct CODATA 2022 extract declared
- current black-hole intervals: `mass-only` baseline plus `mass + direct-2022-G` combined interval
- current measured-constant status in those intervals: `direct_2022_g_threaded`

## Current policy boundary

The package currently uses a conservative split:

1. provenance is anchored to the `2022/NIST` source record
2. the numeric runtime uncertainty for `G` now comes from a direct local CODATA 2022 extract
3. exact SI constants remain exact in the current repo convention for this lane
4. gravity-context rows now keep the old `mass-only` baseline and also add a `mass + direct-2022-G` combined interval

## What this closes and does not close

This package closes:

- the absence of an explicit runtime policy for measured constants
- the ambiguity about whether `G` uncertainty had been forgotten or intentionally deferred
- the absence of any declared gravity-context interval layer beyond `mass-only`

This package does not close:

- broader CODATA table archival beyond the current topic-needed `G` extract
- spin/systematic astrophysical uncertainty terms

## Use rule

Use this file when deciding whether a gravity-context interval is:

- `mass-only`
- `mass-plus-direct-2022-G`
- or still too incomplete for stronger wording

It is a blocker-narrowing artifact, not a promotion artifact.
