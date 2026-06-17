# Data Manifest

Current data reality status: `manifested real dataset`

External-source audit status: `raw-table-backed AME2020 table-wide parse plus source-backed proton-radius JSON`.

Priority remediation:

- Keep `Data_AME2020_Binding_FullParsed.json` as the table-wide parsed AME2020 provenance layer.
- Keep `Data_AME2020_Binding_RawSubset.json` as the current pass/fail validation subset for binding-energy checks.
- Keep `Data_AME2020_Benchmark_Manifest.json` as the map between full parsed coverage, validation subset, heavy-nucleus gate, and light-nucleus diagnostics.
- Keep `Result/artifacts/nuclear_binding_full_table_diagnostic.json` as the table-wide behavior report distinct from the strict pass/fail artifact.
- Preserve proton-radius source JSON as a separate benchmark layer with explicit provenance.

| Item | Local path | Bytes | SHA-256 | Source | Provenance status |
| :-- | :-- | --: | :-- | :-- | :-- |
| AME2020 raw mass table | `docs/data/external/particle_physics/ame2020/mass_1.mas20` | 476242 | `94299ea0fec7da4ed827372882dc6bc0c8f63b416d679b2969f4b60988d979b3` | AME2020 / Wang et al. | Source-locked raw ASCII table |
| AME2020 table-wide parse | `Data/03_Research/Data_AME2020_Binding_FullParsed.json` | 1304922 | `24a9fe89c18bf7c5a10ae14b3e2fc2df8257a92372a8f3da61a0d84982511eb1` | Parsed from local `mass_1.mas20` raw table | Table-wide parsed provenance layer |
| AME2020 raw-derived subset | `Data/03_Research/Data_AME2020_Binding_RawSubset.json` | 4049 | `45e887c87a5ac4362c78c0c5032e3a0ba5bc085c3759cef0f98edf7f69c86f6c` | Parsed from local `mass_1.mas20` raw table | Manifested real dataset subset |
| AME2020 benchmark manifest | `Data/03_Research/Data_AME2020_Benchmark_Manifest.json` | 759 | `ccf80757482c98dc764d23d30606a27f720d5601596eff40fd30766dd63c2ce6` | Generated from parser output | Coverage and gate manifest |
| Proton radius benchmark | `Data/03_Research/Data_Proton_Radius.json` | 342 | `7719827f4d3717eb6a608f2cddc450b040d1bda022964a0606c6c5dd04f32850` | PRad 2019 + CODATA 2018 | Source-backed local JSON |
| PDG quark masses snapshot | `Data/03_Research/Data_PDG_Quarks_2024.json` | 630 | `e6e3f7540b6810bcc5056590626998679c1406b126328385bb65d84dd4aca22b` | PDG 2024 working copy | Legacy local snapshot |
| Raw AME downloader | `Data/03_Research/download_ame_masses.py` | 2489 | `7b38cfd2f6583badf05d1ff46c0b67edeecbc77382093f3f9be0aaad15f4b9ba` | AMDC/IAEA mirrors | Acquisition helper, not yet source-locked result |

## Workflow Gate Files

| File | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `source_evidence_intake_stub.json` | 2260 | `8735b3e488b03b6e0396fe6e527f969b5c2f2edd4a42e5ff16245f850cac9ad6` | provenance intake across nuclear, hadron, QCD, and confinement lanes | created by primary verifier |
| `source_evidence_readiness_matrix.json` | 2576 | `e4c25b2c1a0bf4dad5cf78aaceeea468aaca0c8cf980ebcdf84efb8e1e115b86` | tracks which source packages are review-ready | AME2020 and proton radius ready; PDG source package and diagnostic model artifact exist; QCD/confinement still blocked |
| `semf_coefficient_provenance_gate.json` | 4729 | `c30e8bc488afa4b43ac96f7398cb036459212f059f13e7769180e6207715d587` | tracks SEMF coefficient, Yukawa, and rounded-constant provenance | blocks parameter-free and first-principles nuclear-binding claims until coefficient source package and term policy are source-locked |
| `pdg_hadron_qcd_source_mapping_gate.json` | 5999 | `89899701cd5764d23701639dddd9fba218c35557967cde81eacedd74db9cb8f8` | maps available PDG 2025 quark and hadron mass records and records missing QCD integration | source-package model verifier exists, but high residuals keep hadron/QCD validation blocked |
| `pdg_hadron_quark_reference_package.json` | 13401 | `16241283a47b2721d3c8638a59c325a1686d809e8aefdf15d0ba3fa3464268fd` | generated selected PDG 2025 quark/hadron mass package | diagnostic source-linkage package; not a model validation artifact |
| `branch_claim_gate.json` | 2242 | `8b22acf0b9fc76d8d054fb52f8c5ea68313d9920c08eb150f9caeab3fa7d4ae9` | lane-by-lane claim ceiling | heavy binding and proton-radius anchor accepted; 4 branches blocked |

## Result Artifacts

| Artifact | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `Result/artifacts/0_5_nuclear_binding_hadrons_verification.json` | 5029 | `fbb29c6f4574476edc3f22af409dc22fd043fc5a87e1110f5556670d28b10797` | primary wrapper/run-contract artifact | Records scripts present and runnable; does not override branch claim gates |
| `Result/artifacts/nuclear_binding_full_table_diagnostic.json` | 6722 | `af78181bbebd12fb47bdbafc2604e1436d489075134e9d43692c944e549fd4d3` | table-wide behavior diagnostic | Separates broad table behavior from strict pass/fail validation subset |
| `Result/artifacts/nuclear_binding_source_locked_validation.json` | 18703 | `cee37e29e687a66361ecf020810fe73251d645cd70f5c61bf2bca8209cae6835` | source-locked validation artifact | Supports heavy-nucleus subset and proton-radius anchor only; now embeds SEMF decomposition, SEMF coefficient gate status, and PDG source-package diagnostic-blocked status |
| `Result/artifacts/pdg_hadron_quark_source_linkage.json` | 2219 | `e8a72e49daa4c86532cecf7539f027bea0c77034e34087e5163b127b8eb3f66d` | PDG quark/hadron source-linkage artifact | `DIAGNOSTIC_SOURCE_LINKAGE`; records `16/16` found and `0` unit mismatches |
| `Result/artifacts/hadron_model_source_package_diagnostic.json` | 5198 | `9563d71cb0772de1f5e405a8cca38601f011381958ee09084967a32fcd627536` | source-package-driven hadron-model diagnostic | `DIAGNOSTIC_MODEL_SOURCE_PACKAGE`; compares 7 supported labels with `75.33%` mean error and `94.91%` max error |

Repository note:

- Topic `0.5` is no longer limited to an embedded list in the primary verifier.
- The binding-energy benchmark now records table-wide AME2020 coverage. The current pass/fail gate still uses a curated isotope subset, while full-table coverage is reported as provenance and audit metadata.
- The current full-table diagnostic shows that heavy nuclei are broadly well-behaved while many light nuclei remain outside the intended liquid-drop validation regime.
- The SEMF coefficient gate is now present as a machine-readable blocker and is embedded in the 2026-06-17 strict verifier artifact.
- The PDG hadron/quark source-linkage artifact shows that selected quark masses and several hadron masses can be reproduced from the downloaded PDG 2025 SQLite source.
- The hadron source-package diagnostic now reads that package, but the large residuals keep hadron/QCD branches in diagnostic-blocked status.
