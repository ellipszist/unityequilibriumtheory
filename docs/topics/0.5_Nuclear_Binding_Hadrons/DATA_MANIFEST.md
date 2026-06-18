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
| `source_evidence_intake_stub.json` | 2361 | `c766613447bab409357b5f476d284221272dd0d457b65740dd01b7bf2056ce36` | provenance intake across nuclear, hadron, QCD, and confinement lanes | created by primary verifier |
| `source_evidence_readiness_matrix.json` | 2646 | `faebb47cff9104695819c0e3bf980648a2018572127f3a452d644a0c47980864` | tracks which source packages are review-ready | AME2020 and proton radius ready; PDG source package and diagnostic model artifact exist; QCD/confinement still blocked |
| `semf_coefficient_provenance_gate.json` | 6259 | `796f51ed455b4b00a83643bfdf4410839b37eb1d01417aa2ba91328c48dac9b2` | tracks SEMF coefficient, Yukawa, and rounded-constant provenance | local package and exact source-candidate match ready; blocks parameter-free and first-principles claims until direct source record and term policy are source-locked |
| `semf_coefficient_local_package.json` | 6712 | `ab4a32d42db189bb9e327e6b6ce3b71ebdded760f573ec871975c151250fbf2a` | local package of exact engine SEMF/Yukawa constants | `LOCAL_PACKAGE_READY_SOURCE_GAP_BLOCKED`; 9 constants extracted, 0 gate mismatches, source record still missing |
| `semf_coefficient_source_candidates.json` | 3925 | `88799eb0f5247f407ae0d8a654cff347f26a918b770f9c049a82152603374d5f` | external source-candidate package for SEMF coefficient set | `SOURCE_CANDIDATE_MATCH_DIRECT_SOURCE_BLOCKED`; 1 exact source-candidate match, 0 direct source records held |
| `pdg_hadron_qcd_source_mapping_gate.json` | 6619 | `1dae879456ced395272c0e17fa0cd75970c0199f04f9f67063d201c3d2dce070` | maps available PDG 2025 quark/hadron mass records and QCD alpha_s source-probe status | hadron source-package verifier exists with high residuals; QCD alpha_s bug is fixed but source row remains missing |
| `pdg_hadron_quark_reference_package.json` | 13546 | `415a2df3d54781baa13e18841f06baf091c0ce78fa81bfccc48ed8b64feff107` | generated selected PDG 2025 quark/hadron mass package | diagnostic source-linkage package; not a model validation artifact |
| `branch_claim_gate.json` | 2338 | `624ff981de0369b5e1fdf04d1feb085fade7fa907a05dc95e08edea510580eb0` | lane-by-lane claim ceiling | heavy binding and proton-radius anchor accepted; 4 branches blocked |

## Result Artifacts

| Artifact | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `Result/artifacts/0_5_nuclear_binding_hadrons_verification.json` | 5029 | `fbb29c6f4574476edc3f22af409dc22fd043fc5a87e1110f5556670d28b10797` | primary wrapper/run-contract artifact | Records scripts present and runnable; does not override branch claim gates |
| `Result/artifacts/nuclear_binding_full_table_diagnostic.json` | 6737 | `7b9dcff2969ec071711ad28972a25244cb2e700bb7a3c5bcfa7859ffa6aee5bd` | table-wide behavior diagnostic | Separates broad table behavior from strict pass/fail validation subset |
| `Result/artifacts/nuclear_binding_source_locked_validation.json` | 19975 | `eccd7eff217c2a710c9c9811e6d1e84479e9d717031c67ab3328bf930517b45c` | source-locked validation artifact | Supports heavy-nucleus subset and proton-radius anchor only; embeds SEMF decomposition, local SEMF package and source-candidate references, SEMF coefficient gate status, and hadron/QCD/confinement diagnostic-blocked status |
| `Result/artifacts/semf_coefficient_provenance_diagnostic.json` | 4314 | `19f436a761361287fe7f8006be92d3cc5cb5c0edaf6f09abcdcc2fc9c49ed0aa` | SEMF coefficient local-package diagnostic | `LOCAL_PACKAGE_READY_SOURCE_GAP_BLOCKED`; 5 SEMF coefficients and 4 correction constants extracted from the engine with 0 local gate mismatches |
| `Result/artifacts/semf_coefficient_source_candidate_audit.json` | 3572 | `ee75f1fc9d5614dc85e740e98568a3f9e377ef5f61cd7225b7f39cbfc27938e5` | SEMF source-candidate audit | `SOURCE_CANDIDATE_MATCH_DIRECT_SOURCE_BLOCKED`; 1 exact candidate match, 0 direct source records held |
| `Result/artifacts/pdg_hadron_quark_source_linkage.json` | 2234 | `a29b3093cb1294931fc02c9954282143661f0e87c68daba58de9440e2081a7cd` | PDG quark/hadron source-linkage artifact | `DIAGNOSTIC_SOURCE_LINKAGE`; records `16/16` found and `0` unit mismatches |
| `Result/artifacts/hadron_model_source_package_diagnostic.json` | 5213 | `9f77746497f9bab8475c73c1ed06ff9741984d30af213ebc3068e096289673df` | source-package-driven hadron-model diagnostic | `DIAGNOSTIC_MODEL_SOURCE_PACKAGE`; compares 7 supported labels with `75.33%` mean error and `94.91%` max error |
| `Result/artifacts/qcd_alpha_s_source_probe.json` | 3043 | `e27153110ba5dc83c95314518d5571b2eb24ca3a118579ae9b52433b5002a1ce` | QCD alpha_s source-probe and smoke-test artifact | `DIAGNOSTIC_QCD_ALPHA_S_SOURCE_PROBE`; `alpha_s_uet_v2` finite at 4/4 checked scales, but no direct local PDG alpha_s row found |
| `Result/artifacts/confinement_proof_gate_diagnostic.json` | 1945 | `e9de60e0bf0f8fbff335d0ea1cac12d3c7422033bed3a3a52d35736168f22fc1` | confinement proof return-contract diagnostic | `DIAGNOSTIC_CONFINEMENT_PROOF_GATE`; proof script return contract works but narrow proton-mass check is `FAIL` at `0.058520 GeV` |

Repository note:

- Topic `0.5` is no longer limited to an embedded list in the primary verifier.
- The binding-energy benchmark now records table-wide AME2020 coverage. The current pass/fail gate still uses a curated isotope subset, while full-table coverage is reported as provenance and audit metadata.
- The current full-table diagnostic shows that heavy nuclei are broadly well-behaved while many light nuclei remain outside the intended liquid-drop validation regime.
- The SEMF coefficient gate, local package, and source-candidate package now make the exact engine constants and an exact external source-candidate match machine-readable and are embedded in the 2026-06-18 strict verifier artifact; direct-source-record and term-policy blockers remain open.
- The PDG hadron/quark source-linkage artifact shows that selected quark masses and several hadron masses can be reproduced from the downloaded PDG 2025 SQLite source.
- The hadron source-package diagnostic now reads that package, but the large residuals keep hadron/QCD branches in diagnostic-blocked status.
- The QCD alpha_s source probe fixes and smoke-tests the local runtime bug, but it does not provide a source-backed QCD-running package.
- The confinement proof gate diagnostic fixes the unconditional-return blocker and records a `FAIL` for the current narrow proton-mass consistency check; it is not a formal confinement proof.
