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
| `source_evidence_intake_stub.json` | 2130 | `e0df023c733c790c4cc5abc5d33a6defaf20950c7fed16d9f40fa918f71e026d` | provenance intake across nuclear, hadron, QCD, and confinement lanes | created by primary verifier |
| `source_evidence_readiness_matrix.json` | 2589 | `651a8f316c9a1127808587a9804e2215643d34e1ee9d69ae62070549a3a192c7` | tracks which source packages are review-ready | AME2020 and proton radius ready; PDG/QCD/confinement still blocked |
| `branch_claim_gate.json` | 2242 | `8b22acf0b9fc76d8d054fb52f8c5ea68313d9920c08eb150f9caeab3fa7d4ae9` | lane-by-lane claim ceiling | heavy binding and proton-radius anchor accepted; 4 branches blocked |

## Result Artifacts

| Artifact | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `Result/artifacts/0_5_nuclear_binding_hadrons_verification.json` | 5029 | `fbb29c6f4574476edc3f22af409dc22fd043fc5a87e1110f5556670d28b10797` | primary wrapper/run-contract artifact | Records scripts present and runnable; does not override branch claim gates |
| `Result/artifacts/nuclear_binding_full_table_diagnostic.json` | 6729 | `291ce76ca6dca4f710c51857d4ea4d0b262bfd9876f5e3174ff1fdff9c1e0432` | table-wide behavior diagnostic | Separates broad table behavior from strict pass/fail validation subset |
| `Result/artifacts/nuclear_binding_source_locked_validation.json` | 12341 | `4184383711b5fe1335a114ac6d492877498cb65dd1165a84a9aeff08861224b4` | source-locked validation artifact | Supports heavy-nucleus subset and proton-radius anchor only |

Repository note:

- Topic `0.5` is no longer limited to an embedded list in the primary verifier.
- The binding-energy benchmark now records table-wide AME2020 coverage. The current pass/fail gate still uses a curated isotope subset, while full-table coverage is reported as provenance and audit metadata.
- The current full-table diagnostic shows that heavy nuclei are broadly well-behaved while many light nuclei remain outside the intended liquid-drop validation regime.
