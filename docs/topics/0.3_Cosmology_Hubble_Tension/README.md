---
layout: article
title: "UET Topic 0.3: Cosmology and Hubble Tension"
description: "Structured documentation for the cosmology and Hubble-tension topic in the UET repository."
---

# 0.3 Cosmology and Hubble Tension

## Problem

This topic studies whether UET-style cosmology components can reproduce the observed gap
between early- and late-universe Hubble-constant measurements under the repository's
internal assumptions.

## Assumptions and scope

- Scope: internal comparison against published H0 reference values and topic-specific scripts
- Out of scope: claiming that the Hubble tension is universally resolved
- The topic includes both a proposed mechanism and explicit negative results for parts of the
  wider cosmology problem space

## Data sources

- Published value references:
  - Planck 2018
  - SH0ES 2022
- Local topic data and experiments:
  - `Data/03_Research/`
  - `Data/03_Research/jwst_highz_calibration.csv` where applicable

## Method summary

- Engine: `Code/01_Engine/Engine_Cosmology.py`
- Comparison script: `Code/03_Research/Research_Hubble_Comparison.py`
- Supporting research scripts: `Research_CMB_Analysis.py`, `Research_Dark_Energy.py`, `Research_highz_galaxies.py`

Supporting standard files:

- [METHOD.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.3_Cosmology_Hubble_Tension/METHOD.md:1)
- [DATA_MANIFEST.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.3_Cosmology_Hubble_Tension/DATA_MANIFEST.md:1)
- [VERIFICATION_SPEC.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.3_Cosmology_Hubble_Tension/VERIFICATION_SPEC.md:1)
- [BASELINE_COMPARISON.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.3_Cosmology_Hubble_Tension/BASELINE_COMPARISON.md:1)
- [LIMITATIONS.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.3_Cosmology_Hubble_Tension/LIMITATIONS.md:1)

## Parameters and fitting status

- Topic scripts rely on repository assumptions about information-coupling behavior
- Public wording should describe this topic as a proposed mechanism with internal benchmark
  comparisons, not as a settled resolution of the Hubble-tension literature

## Metrics and thresholds

- `Research_Hubble_Comparison.py` compares the observed H0 gap against the engine-derived
  gap and currently reports an internal pass when percentage error is below `20%`
- The topic also documents at least one explicit failure mode for the vacuum-energy problem;
  this failure must remain visible in topic summaries

## Baselines

- Primary baseline: published Planck and SH0ES reference values
- Comparator model: LCDM framing as described in topic docs

## Limitations and open risks

- Published-value comparison is not the same as a full cosmology pipeline replication
- The topic does not yet ship a normalized raw-data package for the full observational stack
- Hubble-tension and dark-energy claims must not be collapsed into one status line

## Reproducibility

- Verification command: `python docs/topics/0.3_Cosmology_Hubble_Tension/Code/03_Research/Research_Hubble_Comparison.py`
- Artifact contract: see [VERIFICATION_SPEC.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.3_Cosmology_Hubble_Tension/VERIFICATION_SPEC.md:1)

## Current readiness status

`Structured`
