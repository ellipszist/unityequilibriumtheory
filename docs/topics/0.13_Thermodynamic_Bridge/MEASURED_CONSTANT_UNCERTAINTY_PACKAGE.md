# Measured Constant Uncertainty Package

## Purpose

This file isolates the current `measured-constant uncertainty` blocker inside the gravity-adjacent uncertainty lane of `0.13`.

The topic already had a provenance anchor for non-exact constants such as `G`.
What it did not have was a topic-local runtime package stating:

- which measured constants matter in the current verifier
- which numeric uncertainty proxy is currently used
- which rows would inherit that uncertainty
- whether that uncertainty is already threaded into the published intervals

## Current authority

- Machine-readable artifact: `Data/03_Research/measured_constant_uncertainty_package.json`
- Supporting files:
  - `docs/data/external/constants/codata/measured_constants_2022_source_record.json`
  - `docs/topics/0.19_Gravity_GR/Data/03_Research/codata_2018_gravity.json`
  - `Data/03_Research/uncertainty_propagation_summary.json`
  - `ROW_CLOSURE_MATRIX.md`

## Current runtime state

- provenance anchor for measured constants: present
- current runtime uncertainty proxy for `G`: declared
- current black-hole intervals: `mass-only` baseline plus provisional `mass + G-proxy` combined interval
- current measured-constant status in those intervals: `provisional_g_proxy_threaded`

## Current policy boundary

The package currently uses a conservative split:

1. provenance is anchored to the `2022/NIST` source record
2. the numeric runtime uncertainty proxy for `G` is still inherited from the local `0.19` CODATA 2018 checkpoint
3. exact SI constants remain exact in the current repo convention for this lane
4. gravity-context rows now keep the old `mass-only` baseline and also add a provisional `mass + G-proxy` combined interval

## What this closes and does not close

This package closes:

- the absence of an explicit runtime policy for measured constants
- the ambiguity about whether `G` uncertainty had been forgotten or intentionally deferred
- the absence of any declared gravity-context interval layer beyond `mass-only`

This package does not close:

- direct in-topic extraction of `2022` numeric uncertainty values
- replacement of the provisional `G` proxy with direct in-topic `2022` extraction
- spin/systematic astrophysical uncertainty terms

## Use rule

Use this file when deciding whether a gravity-context interval is:

- `mass-only`
- `mass-plus-measured-constant`
- or still too incomplete for stronger wording

It is a blocker-narrowing artifact, not a promotion artifact.
