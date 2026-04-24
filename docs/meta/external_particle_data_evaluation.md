# External Particle Data Evaluation

This report is strict: source-locked files are not counted as theory validation until a topic verifier reads them.

## Source Artifact Status

| Dataset | Topic | Status | Data grade | Local path |
| :-- | :-- | :-- | :-- | :-- |
| `pdg_2025_sqlite` | `0.5-0.8` | `downloaded` | `benchmark_machine_readable` | `docs\data\external\particle_physics\pdg\pdg-2025-v0.2.2.sqlite` |
| `pdgall_2025_sqlite` | `0.5-0.8` | `downloaded` | `benchmark_machine_readable` | `docs\data\external\particle_physics\pdg\pdgall-2025-v0.2.2.sqlite` |
| `ame2020_mass_1` | `0.5` | `downloaded` | `source_locked_ascii_table` | `docs\data\external\particle_physics\ame2020\mass_1.mas20` |
| `ame2020_full_parsed_json` | `0.5` | `generated` | `table_wide_parsed_layer` | `docs\topics\0.5_Nuclear_Binding_Hadrons\Data\03_Research\Data_AME2020_Binding_FullParsed.json` |
| `ame2020_raw_subset_json` | `0.5` | `generated` | `raw_table_derived_subset` | `docs\topics\0.5_Nuclear_Binding_Hadrons\Data\03_Research\Data_AME2020_Binding_RawSubset.json` |
| `ame2020_benchmark_manifest` | `0.5` | `generated` | `coverage_and_gate_manifest` | `docs\topics\0.5_Nuclear_Binding_Hadrons\Data\03_Research\Data_AME2020_Benchmark_Manifest.json` |
| `nufit_6_0_article_pdf` | `0.7` | `downloaded` | `source_locked_pdf` | `docs\data\external\particle_physics\nufit\NuFIT_6_0_JHEP12_2024_216.pdf` |
| `nufit_v60_table_pdf` | `0.7` | `downloaded` | `source_locked_pdf` | `docs\data\external\particle_physics\nufit\official\v60.tbl-parameters.pdf` |
| `nufit_v60_extracted_json` | `0.7` | `generated` | `source_backed_extracted_table` | `docs\data\external\particle_physics\nufit\official\nufit_v60_parameters_extracted.json` |
| `nufit_v60_provenance_validation` | `0.7` | `generated` | `source_hash_schema_guard` | `docs\data\external\particle_physics\nufit\official\nufit_v60_provenance_validation.json` |
| `electroweak_mapping_audit` | `0.6` | `generated` | `upstream_mapping_audit` | `docs\data\external\particle_physics\pdg\electroweak_mapping_audit.json` |
| `electroweak_reference_package` | `0.6` | `generated` | `structured_reference_package` | `docs\data\external\particle_physics\pdg\electroweak_reference_package.json` |
| `electroweak_benchmark_package` | `0.6` | `generated` | `structured_benchmark_package` | `docs\data\external\particle_physics\pdg\electroweak_benchmark_package.json` |
| `fermilab_muon_g2_2025_press_release` | `0.8` | `downloaded` | `source_locked_html` | `docs\data\external\particle_physics\muon_g2\fermilab_muon_g2_2025_press_release.html` |
| `doe_muon_g2_2025_press_release` | `0.8` | `downloaded` | `source_locked_html` | `docs\data\external\particle_physics\muon_g2\doe_muon_g2_2025_press_release.html` |
| `fermilab_muon_g2_2025_experiment_json` | `0.8` | `generated` | `source_locked_extracted_table` | `docs\data\external\particle_physics\muon_g2\fermilab_muon_g2_2025_experiment.json` |
| `muon_g2_theory_2025_white_paper_html` | `0.8` | `downloaded` | `source_locked_html` | `docs\data\external\particle_physics\muon_g2\theory\muon_g2_theory_white_paper_2025.html` |
| `muon_g2_theory_2025_total_sm_json` | `0.8` | `generated` | `source_locked_extracted_table` | `docs\data\external\particle_physics\muon_g2\theory\muon_g2_theory_2025_total_sm.json` |
| `muon_g2_baseline_package` | `0.8` | `generated` | `structured_baseline_package` | `docs\data\external\particle_physics\muon_g2\theory\muon_g2_baseline_package.json` |

## Topic Verification Linkage

| Topic | Current state | Problem | Next fix |
| :-- | :-- | :-- | :-- |
| `0.5_Nuclear_Binding_Hadrons` | `external-linked and passing with caveat` | The strict verifier now reads a table-wide AME2020 parsed layer with `3558` readable BE/A rows, plus a selected validation subset and proton-radius benchmark. The pass/fail gate still uses the subset rather than full-table scoring. | Expand validation coverage beyond the current selected subset and replace remaining local hadron snapshots where possible. |
| `0.6_Electroweak_Physics` | `external-linked and passing` | The PDG-linked verifier now reads a structured electroweak reference package and passes `sin2(theta_W)`, `m_W`, `m_H`, and `G_F` after unifying the Higgs branch with the same electroweak-running angle path used by the successful mixing-angle branch. The expanded benchmark also passes a checked-local neutron-lifetime gate, while a dedicated SQLite mapping audit currently records no direct upstream weak-mixing-angle match. | Replace the remaining checked-local weak-mixing-angle layer with a direct PDG table mapping if a future upstream route becomes available, and improve the running-angle layer before promoting it beyond diagnostic status. |
| `0.7_Neutrino_Physics` | `external-linked and passing with caveat` | The topic now passes both the official NuFIT 6.0 oscillation benchmark and the official KATRIN 2025 direct mass-limit benchmark after repairing a dimensional inconsistency in the absolute-mass engine path. The NuFIT layer is now guarded by source hashes and schema validation, but it remains checked transcription rather than true PDF table parsing. | Add an explicit PDF/table parsing dependency before replacing the checked-transcription layer with machine parsing, and document the heavy-scale derivation behind the current see-saw-style mass branch more rigorously. |
| `0.8_Muon_g2_Anomaly` | `fully source-locked and passing with caveat` | Both the 2025 experimental result and the 2025 Standard-Model comparator are source-locked, the current engine-linked verifier passes at about `0.42 sigma`, and the sensitivity artifact now separates the canonical 2025 benchmark from historical local theory-package baselines and the stale `2.51e-9` diagnostic reference. | Keep workflow guards active, remove stale hardcoded benchmark comparators from the critical path, and extend sensitivity analysis to additional external theory packages and downstream consistency checks. |

## Scientific Summary

- `0.5` now has a local source-locked raw AME2020 table, a table-wide parsed layer with `3558` readable rows, and a raw-derived benchmark subset; it passes its strict verifier on the current isotope set while reporting coverage metrics.
- `0.6` is now genuinely tied to upstream electroweak data through a structured reference package, passes its current four-observable PDG-linked benchmark package, passes a checked-local neutron-lifetime gate, and explicitly records that the current SQLite workflow still lacks a direct weak-mixing-angle mapping.
- `0.7` is now tied to official NuFIT 6.0 parameter ranges and an official KATRIN 2025 result; the combined verifier passes and the NuFIT checked transcription is guarded by hashes and schema checks.
- `0.8` is now stricter than before because both benchmark sides are source-locked, the current engine-linked verifier passes, and the sensitivity artifact shows both that the stale legacy reference would fail the 2025 benchmark and that the live engine stays stable across the current structured baseline-package set.
