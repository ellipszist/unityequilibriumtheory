# Particle Real-Data Audit Results

This report uses source-locked external particle-data artifacts. It is strict about topic linkage:
existing topic scripts that still read embedded/local snapshots are marked as not linked to the new external data.

## PDG Snapshot

| Topic | Particle | Mass | Width | Lifetime |
| :-- | :-- | :-- | :-- | :-- |
| `0.5_Nuclear_Binding_Hadrons` | `p` | `938.27208816+-0.00000029 MeV` | `n/a` | `>9E29 years` |
| `0.5_Nuclear_Binding_Hadrons` | `n` | `939.5654205+-0.0000005 MeV` | `n/a` | `878.4+-0.5 s` |
| `0.5_Nuclear_Binding_Hadrons` | `pi+` | `139.57039+-0.00018 MeV` | `n/a` | `2.6033+-0.0005 s` |
| `0.5_Nuclear_Binding_Hadrons` | `K+` | `493.677+-0.015 MeV` | `n/a` | `1.2380+-0.0020 s` |
| `0.6_Electroweak_Physics` | `W+` | `80.3692+-0.0133 GeV` | `2.14+-0.05 GeV` | `n/a` |
| `0.6_Electroweak_Physics` | `Z0` | `91.1880+-0.0020 GeV` | `2.4955+-0.0023 GeV` | `n/a` |
| `0.6_Electroweak_Physics` | `H` | `125.20+-0.11 GeV` | `3.7+1.9-1.4 MeV` | `n/a` |
| `0.7_Neutrino_Physics` | `e-` | `0.51099895000+-0.00000000015 MeV` | `n/a` | `>6.6E28 yr` |
| `0.7_Neutrino_Physics` | `mu-` | `105.6583755+-0.0000023 MeV` | `n/a` | `2.1969811+-0.0000022 s` |
| `0.7_Neutrino_Physics` | `tau-` | `1776.93+-0.09 MeV` | `n/a` | `290.3+-0.5 s` |
| `0.8_Muon_g2_Anomaly` | `mu-` | `105.6583755+-0.0000023 MeV` | `n/a` | `2.1969811+-0.0000022 s` |

## Electroweak Local Snapshot vs PDG 2025

| Observable | Local | PDG 2025 | Difference |
| :-- | --: | --: | --: |
| `Mass_W` | `80.379` | `80.377` | `0.0025%` |
| `Mass_Z` | `91.1876` | `91.18797809193725` | `0.0004%` |

## Current Theory Verification Linkage

| Topic | Script | Command exit | Uses new external source? | Scientific consequence |
| :-- | :-- | :-- | :-- | :-- |
| `0.5_Nuclear_Binding_Hadrons` | `docs/scripts/data/extract_ame2020_binding_subset.py` | `0` | `True` | Run result is tied to a new source-locked external benchmark; nonzero exit now means the current UET observable package misses the real-data threshold. |
| `0.5_Nuclear_Binding_Hadrons` | `docs/topics/0.5_Nuclear_Binding_Hadrons/Code/03_Research/Research_Nuclear_Binding_SourceLocked.py` | `0` | `True` | Run result is tied to a new source-locked external benchmark; nonzero exit now means the current UET observable package misses the real-data threshold. |
| `0.6_Electroweak_Physics` | `docs/topics/0.6_Electroweak_Physics/Code/03_Research/Research_Electroweak_PDG_Comparison.py` | `0` | `True` | Run result is tied to a new source-locked external benchmark; nonzero exit now means the current UET observable package misses the real-data threshold. |
| `0.6_Electroweak_Physics` | `docs/topics/0.6_Electroweak_Physics/Code/03_Research/Research_Electroweak_Expanded_Benchmark.py` | `0` | `False` | Run result is still an internal-snapshot test; real-data theory error is not fully measured yet. |
| `0.7_Neutrino_Physics` | `docs/scripts/data/validate_nufit_v60_provenance.py` | `0` | `True` | Run result is tied to a new source-locked external benchmark; nonzero exit now means the current UET observable package misses the real-data threshold. |
| `0.7_Neutrino_Physics` | `docs/topics/0.7_Neutrino_Physics/Code/03_Research/Research_NuFit_6_0_Comparison.py` | `0` | `True` | Run result is tied to a new source-locked external benchmark; nonzero exit now means the current UET observable package misses the real-data threshold. |
| `0.8_Muon_g2_Anomaly` | `docs/topics/0.8_Muon_g2_Anomaly/Code/03_Research/Research_Muon_Anomaly_2025.py` | `0` | `True` | Run result is tied to a new source-locked external benchmark; nonzero exit now means the current UET observable package misses the real-data threshold. |
| `0.8_Muon_g2_Anomaly` | `docs/topics/0.8_Muon_g2_Anomaly/Code/03_Research/Research_Muon_Sensitivity_2025.py` | `0` | `True` | Run result is tied to a new source-locked external benchmark; nonzero exit now means the current UET observable package misses the real-data threshold. |

## Workflow Guards

| Topic | Guarded path | Passes? | Violations |
| :-- | :-- | :-- | :-- |
| `0.8_Muon_g2_Anomaly` | `docs\topics\0.8_Muon_g2_Anomaly\Code\03_Research\Research_Muon_Anomaly_2025.py` | `True` | none |

## Problems Found

- PDG 2025 data is now downloaded, hashed, and machine-readable for particle masses/widths/lifetimes.
- `0.5` now uses a table-wide AME2020 parsed layer plus a raw-table-derived validation subset and proton-radius benchmark. The strict subset gate passes, and the new full-table diagnostic shows `3480/3487` heavy nuclei under the 15% reference threshold while light nuclei remain much less stable.
- `0.6` now reads a structured PDG-linked electroweak reference package and passes the current four-observable package: `sin2(theta_W)` is off by about 0.13%, `m_W` by about 0.53%, `m_H` by about 0.05%, while `G_F` matches closely. The expanded benchmark also passes a neutron-lifetime gate at about 0.11% error, while a dedicated mapping audit records that no direct weak-mixing-angle match was located in the current PDG SQLite workflow.
- `0.7` now uses a local extracted NuFIT 6.0 benchmark and an official KATRIN 2025 benchmark. After repairing the unit mismatch in `Engine_Neutrino.predict_neutrino_mass()`, the oscillation checks and the direct absolute-mass branch both pass; the checked-transcription NuFIT table is guarded by source hashes and schema validation.
- `0.8` now reads both a source-locked 2025 experimental result and a source-locked 2025 theory comparator. The verifier is tied to `Engine_Muon_G2.py`, the current package passes at about 0.42 sigma, and the sensitivity artifact now separates the canonical 2025 benchmark from historical local theory-package baselines.

## Remaining Scientific Caveats

| Topic | Passes current source-locked benchmark | Remaining caveat | Next scientific hardening step |
| :-- | :-- | :-- | :-- |
| `0.5_Nuclear_Binding_Hadrons` | `yes` | AME2020 is now table-wide parsed, but the strict pass/fail gate still uses a selected validation subset while light nuclei remain much weaker in the full-table diagnostic. | Keep the strict subset gate for now, but treat the full-table diagnostic as the honest broad-behavior summary and split heavy-nucleus claims from light-nucleus behavior. |
| `0.7_Neutrino_Physics` | `yes` | NuFIT remains a checked transcription rather than machine-parsed table extraction. | Add an explicit PDF/table parsing dependency or keep the checked-transcription guard mandatory. |
| `0.8_Muon_g2_Anomaly` | `yes` | Current pass depends on live engine linkage; the sensitivity layer now compares canonical source-locked and historical local theory-package baselines, but broader external alternate theory packages are still not covered. | Keep workflow guards active and extend sensitivity analysis across additional external theory packages and downstream consistency checks. |

## Next Fixes

- `0.6`: replace the remaining checked-local weak-mixing-angle layer with a direct PDG table mapping if a future upstream route becomes available, and improve the running-angle layer before promoting it beyond diagnostic status.
- `0.5`: keep extending broad-table scoring and upgrade hadron-mass layers beyond local snapshots.
- `0.7`: add an explicit PDF/table parsing dependency before replacing the checked-transcription layer with machine parsing, and document the heavy-scale derivation behind the current see-saw-style mass branch more rigorously.
- `0.8`: keep workflow guards active and extend sensitivity analysis from the current baseline-package set to additional external theory packages and downstream consistency checks.
