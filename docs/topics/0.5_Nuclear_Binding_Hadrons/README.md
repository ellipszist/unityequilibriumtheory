---
layout: article
title: "UET Topic 0.5: Nuclear Binding Hadrons"
description: "Conservative overview for the nuclear-binding and hadron topic in the UET repository."
---

# 0.5 Nuclear Binding Hadrons

## Problem

This topic explores whether UET-style geometric or information-overlap models can reproduce
selected nuclear-binding, hadron-mass, proton-radius, and strong-force benchmark behavior.

## Current status

- Metadata status: `Draft`
- Audit tier: `B`
- Data status: `manual or placeholder`
- Claim posture: internal research workflow only, not a solved strong-force theory

## What currently exists

- Engine scripts for binding-energy, light-nuclei, hadron, and QCD-bridge experiments
- Research scripts for binding-energy comparison, proton radius, quark masses, and related checks
- Topic-local data files including `Data/03_Research/Data_AME2020_Binding.json` and
  `Data/03_Research/Data_PDG_Quarks_2024.json`
- Competitor and visualization folders that support internal comparisons and plotting

## What this topic does not currently establish

- It does not establish a general derivation of QCD from first principles.
- It does not establish a theorem-level proof of confinement.
- It does not yet provide a standards-grade data manifest, verification contract, or
  limitations package at the topic root.
- Any reported match to selected isotopes or radii should therefore be treated as an internal
  benchmark result rather than external confirmation.

## Data and evidence notes

- The topic appears to use real-source-inspired files, but the audit still classifies the data
  workflow as `manual or placeholder`.
- Before stronger wording is justified, this topic needs a root-level `DATA_MANIFEST.md`
  that identifies source URL or DOI, local file used, preprocessing, and benchmark linkage.

## Verification notes

- Candidate scripts:
  - `Code/01_Engine/Engine_Nuclear_Binding.py`
  - `Code/01_Engine/Engine_Light_Nuclei.py`
  - `Code/03_Research/Research_Nuclear_Binding.py`
  - `Code/03_Research/Research_Proton_Radius.py`
- The repository does not yet expose a topic-level `VERIFICATION_SPEC.md` with command,
  metric, threshold, baseline, and artifact path.

## Reproducibility

Current exploratory commands:

```powershell
python docs/topics/0.5_Nuclear_Binding_Hadrons/Code/01_Engine/Engine_Nuclear_Binding.py
python docs/topics/0.5_Nuclear_Binding_Hadrons/Code/03_Research/Research_Nuclear_Binding.py
```

These commands are useful for internal inspection, but they are not yet an audit-grade
verification workflow.

## Next remediation steps

1. Create `DATA_MANIFEST.md` for AME2020, PDG, proton-radius, and QCD-related inputs.
2. Create `VERIFICATION_SPEC.md` that defines the primary benchmark, metric, baseline, and
   output artifact path.
3. Add `METHOD.md` that separates heuristic mechanism claims from any proof-oriented claims.
4. Add `LIMITATIONS.md` that states scope limits for confinement, light nuclei, and selected
   benchmark fits.

## Current readiness status

`Draft`
