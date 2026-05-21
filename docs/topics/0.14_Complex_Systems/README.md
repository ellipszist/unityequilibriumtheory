---
layout: article
title: "UET Topic 0.14: Complex Systems"
description: "Research module for complex-systems diagnostics within the Unity Equilibrium Theory framework."
---

# 0.14 Complex Systems

Topic status: core research, evidence-bounded.

This topic studies whether UET-style complexity metrics can organize selected complex-system examples. The current audit-backed verifier is the HRV branch using topic-local PhysioNet-derived RR interval files. SOC, econophysics, climate, inequality, and social-network material remain research branches until each has a source-backed dataset, baseline, threshold, and artifact-producing verifier.

## Current Claim Class

- Claim class: internal benchmark/run-contract support for the HRV verifier.
- Current artifact: `Result/artifacts/0_14_complex_systems_verification.json`.
- Current verifier: `Code/03_Research/Research_Biology_HRV.py`.
- Current data posture: source-referenced derived RR files; original PhysioNet records and extraction/preprocessing still need archival normalization.

## Evidence Boundary

The repository can currently support conservative statements such as:

- The HRV verifier runs on source-referenced derived RR interval files and records SDNN, RMSSD, Poincare-style metrics, and an internal equilibrium score.
- The SOC and econophysics engines implement simulation formulas that can be hardened into future verifier gates.
- Cross-domain claims require separate artifacts before they can support theory-level conclusions.

The current evidence package does not establish a universal causal law for all complex systems, a market-crash predictor, a clinical HRV classifier, or a climate/inequality proof.

The topic now includes workflow gates that separate source-evidence intake from branch-level claim ceilings, so the broad title cannot quietly outrun the HRV-centered evidence package.

## 5x4 Grid Structure

| Pillar | Purpose |
| :-- | :-- |
| `Doc/` | Topic notes and domain-branch analysis. |
| `Ref/` | Reference collection for complex systems, networks, HRV, climate, and econophysics. |
| `Data/` | Topic-local HRV, economy, climate, inequality, social, and validation working files. |
| `Code/` | Engines, proof-oriented scripts, research scripts, and comparator scripts. |
| `Result/` | Verification artifact, logs, summaries, and visualizations. |

## Core Files

- `FORMULA_AUDIT.md`: reviewed formula registry and open bridges.
- `DATA_MANIFEST.md`: current data posture and provenance gaps.
- `VERIFICATION_SPEC.md`: primary verifier command and artifact contract.
- `METHOD.md`: topic method boundary.
- `LIMITATIONS.md`: known scientific and audit limitations.
- `Code/01_Engine/Engine_Complexity.py`: SOC, HRV, Hurst, and stability metrics.
- `Code/01_Engine/Engine_Econophysics.py`: market simulation branch.
- `Code/03_Research/Research_Biology_HRV.py`: current primary verifier script.
- `Data/03_Research/source_evidence_intake_stub.json`: structured landing zone for missing HRV, SOC, market, climate, inequality, and social source evidence.
- `Data/03_Research/source_evidence_readiness_matrix.json`: workflow gate for which branch source packages are still blocked by missing evidence fields.
- `Data/03_Research/branch_claim_gate.json`: separated claim ceilings for HRV, SOC, econophysics, climate, inequality/social, and universal-complexity branches.
- `Data/03_Research/biology_hrv/source_lock_manifest.json`: provenance map tying the HRV RR working files to PhysioNet record IDs and runtime filter assumptions.
- `Result/artifacts/0_14_complex_systems_verification.json`: embeds `hrv_provenance_gate` and `complexity_claim_gate` so HRV run-contract evidence cannot silently promote non-HRV branches.

## Verification

Primary command:

```powershell
$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; .\.venv\Scripts\python.exe docs\topics\0.14_Complex_Systems\Code\03_Research\Research_Biology_HRV.py
```

The audit wrapper records the current run contract in `Result/artifacts/0_14_complex_systems_verification.json`. A pass means the HRV script ran against the declared local files and produced the expected internal metrics. It does not certify the broader cross-domain branches.

The embedded `complexity_claim_gate.controller_status` keeps current exports at `HRV_RUN_CONTRACT_ONLY`; broader branch claims and universal-complexity phrases need their own source locks, baselines, thresholds, and verifier artifacts.

The embedded `hrv_provenance_gate` is the raw-source controller. It keeps the HRV lane at source-referenced derived-RR evidence until original PhysioNet records, exact extraction commands, tool versions, and preprocessing scripts are archived.

## Next Hardening Tasks

1. Archive original PhysioNet files and exact extraction/preprocessing scripts for the MIT-BIH NSRDB-derived RR files.
2. Add a dedicated SOC verifier with seeded avalanche statistics, exponent fit, goodness-of-fit threshold, and artifact output.
3. Add market/econ verifier using declared tickers/date ranges and a baseline such as Gaussian/GBM or historical volatility clustering.
4. Split climate, inequality, and social claims into separate artifacts before allowing them to feed core theory claims.
5. Replace qualitative PASS scripts with thresholded tests that can honestly fail.
