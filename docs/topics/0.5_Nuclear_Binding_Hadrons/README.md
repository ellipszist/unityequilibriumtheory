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
- Data status: `manifested real dataset` for AME2020 binding and proton-radius benchmark layers
- Claim posture: source-backed internal benchmark workflow, not a complete strong-force theory

## What currently exists

- Engine scripts for binding-energy, light-nuclei, hadron, and QCD-bridge experiments
- Research scripts for binding-energy comparison, proton radius, quark masses, and related checks
- Topic-local data files including `Data/03_Research/Data_AME2020_Binding.json` and
  `Data/03_Research/Data_PDG_Quarks_2024.json`
- Workflow gate files for source evidence and branch claim ceilings under `Data/03_Research/`
- A SEMF coefficient provenance gate under `Data/03_Research/semf_coefficient_provenance_gate.json`
- A SEMF local coefficient package under `Data/03_Research/semf_coefficient_local_package.json`
- A PDG hadron/QCD source-mapping gate under
  `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json`
- Competitor and visualization folders that support internal comparisons and plotting
- Root standards docs for method, data manifest, baseline, verification, limitations, and
  formula audit

## What this topic does not currently establish

- It does not establish a general derivation of QCD from first principles.
- It does not establish a formal mathematical proof of confinement.
- It does not yet provide a full-table pass/fail proof across AME2020.
- It does not yet source-lock every hadron/QCD embedded constant.
- Any reported match to selected isotopes or radii should therefore be treated as an internal
  benchmark result rather than external confirmation.

## Data and evidence notes

- AME2020 raw table data is locked under `docs/data/external/particle_physics/ame2020/`.
- The strict binding gate uses a raw-derived selected subset, while the full parsed AME2020
  table is reported separately as a diagnostic artifact.
- Proton-radius data is a source-backed local JSON benchmark.
- PDG quark masses and some hadron/QCD constants remain legacy/local snapshots and are not yet
  source-locked at the same standard.
- Branch claim gates now separate heavy-nucleus binding and proton-radius benchmark use from
  light nuclei, hadron mass, QCD running, and confinement branches.
- `semf_coefficient_provenance_gate.json` and
  `semf_coefficient_local_package.json` now record the exact current engine constants
  with `0` local gate mismatches, but still block parameter-free or first-principles wording
  until the SEMF coefficient edition, Yukawa policy, and rounded constants are source-locked.
- `pdg_hadron_qcd_source_mapping_gate.json` and
  `pdg_hadron_quark_reference_package.json` now source-map selected PDG 2025 quark and
  hadron mass rows (`16/16` records found, `0` unit mismatches). A diagnostic
  hadron-model verifier now reads the package for 7 supported hadron labels, but the
  resulting source-package residuals remain weak (`75.33%` mean error, `94.91%` max error),
  so hadron/QCD claims remain blocked.
- `qcd_alpha_s_source_probe.json` shows that `alpha_s_uet_v2` now smoke-tests as finite
  at 4/4 checked scales after the data-shape fix, but the local PDG SQLite query found
  no direct alpha_s/QCD-running source row, so QCD running remains source-blocked.
- `confinement_proof_gate_diagnostic.json` shows that the confinement proof script now
  has a real return contract, but the current narrow proton-mass consistency check fails
  (`0.058520 GeV` versus the `0.9` to `1.01 GeV` diagnostic band), so it remains a
  blocker artifact rather than proof evidence.
- The strict artifact now carries `nuclear_claim_scope_gate`, which lets the heavy-nucleus
  selected-subset and proton-radius anchor checks pass while blocking full-table, light-nuclei,
  QCD, hadron-mass, confinement, and complete strong-force exports.
- The primary verifier now reports SEMF-only, UET entropy, Yukawa, and total binding-energy
  components in the saved strict artifact. In the current heavy-nucleus subset, SEMF-only
  mean error is about `0.86%`, while the total path is about `1.68%`, so the correction lane
  remains diagnostic and must not be described as an improvement.

## Verification notes

- Primary command:
  - `Code/03_Research/Research_Nuclear_Binding_SourceLocked.py`
- Diagnostic command:
  - `Code/03_Research/Research_Nuclear_Binding_FullTable_Diagnostic.py`
- Current strict artifact:
  - `Result/artifacts/nuclear_binding_source_locked_validation.json`
- Current diagnostic artifact:
  - `Result/artifacts/nuclear_binding_full_table_diagnostic.json`
- Workflow artifacts:
  - `Data/03_Research/source_evidence_intake_stub.json`
  - `Data/03_Research/source_evidence_readiness_matrix.json`
  - `Data/03_Research/semf_coefficient_provenance_gate.json`
  - `Data/03_Research/semf_coefficient_local_package.json`
  - `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json`
  - `Data/03_Research/pdg_hadron_quark_reference_package.json`
  - `Data/03_Research/branch_claim_gate.json`
  - `Result/artifacts/semf_coefficient_provenance_diagnostic.json`
  - `Result/artifacts/pdg_hadron_quark_source_linkage.json`
  - `Result/artifacts/hadron_model_source_package_diagnostic.json`
  - `Result/artifacts/qcd_alpha_s_source_probe.json`
  - `Result/artifacts/confinement_proof_gate_diagnostic.json`

## Reproducibility

Current verification commands:

```powershell
python docs/topics/0.5_Nuclear_Binding_Hadrons/Code/03_Research/Research_Nuclear_Binding_SourceLocked.py
python docs/topics/0.5_Nuclear_Binding_Hadrons/Code/03_Research/Research_SEMF_Coefficient_Provenance.py
python docs/topics/0.5_Nuclear_Binding_Hadrons/Code/03_Research/Research_Nuclear_Binding_FullTable_Diagnostic.py
```

The first command is the strict selected-subset gate. The second command extracts the
current SEMF/Yukawa constants into a local package and verifies local gate consistency.
The third command is a diagnostic for broad AME2020 table behavior and must not be
described as a full-table pass.

## Next remediation steps

1. Add a vetted source record for the locally packaged SEMF coefficients and decide whether
   the Yukawa term is baseline physics, a UET bridge term, or a separate diagnostic lane.
2. Decide whether the weak hadron source-package residuals require changing the
   constituent-mass model, demoting the branch, or splitting GMOR and constituent-model lanes.
3. Create a vetted QCD `alpha_s` source package or refine the PDG mapping policy beyond
   the current SQLite query before using that QCD branch in any validation verifier.
4. Define a defensible confinement derivation benchmark before making any proof claim.
5. Keep light nuclei outside the heavy-nucleus pass claim unless a dedicated light-nuclei
   verifier is added.

## Current readiness status

`Draft`
