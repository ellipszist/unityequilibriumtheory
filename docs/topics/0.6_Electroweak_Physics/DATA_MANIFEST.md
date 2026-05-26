# Data Manifest

Current data reality status: `manifested real dataset`

External-source audit status: `PDG 2025 masses are source-locked through SQLite; the effective weak-mixing-angle and Fermi-constant reference are carried in a structured checked reference package; the current PDG SQLite mapping audit records no direct upstream weak-mixing-angle match.`

Priority remediation:

- Keep `docs/data/external/particle_physics/pdg/pdg-2025-v0.2.2.sqlite` as the primary upstream source for `mW`, `mZ`, and `mH`.
- Keep `docs/data/external/particle_physics/pdg/electroweak_mapping_audit.json` as the explicit record of the upstream mapping search for `sin^2(theta_W)`.
- Keep `docs/data/external/particle_physics/pdg/electroweak_reference_package.json` as the structured electroweak comparison package for topic `0.6`.
- Keep `docs/data/external/particle_physics/pdg/electroweak_benchmark_package.json` as the expanded benchmark package that separates source-linked core observables from checked-local neutron and running-angle layers.
- Keep `Data/03_Research/source_lock_manifest.json` as the topic-local source-lock manifest that binds external source files, package hashes, unit roles, and benchmark roles for the verifier artifacts.
- Preserve `Data/03_Research/pdg_electroweak_2024.json` only as the checked local reference that currently supplies the effective weak-mixing-angle and Fermi-constant layer until a direct upstream mapping is added.
- Treat `Data/Download_Electroweak.py` as a legacy helper, not as the canonical scientific data path.

| Item | Local path | Bytes | SHA-256 | Source | Provenance status |
| :-- | :-- | --: | :-- | :-- | :-- |
| PDG 2025 SQLite | `docs/data/external/particle_physics/pdg/pdg-2025-v0.2.2.sqlite` | 24526848 | `3de494ba22d7229eda9ba3047660b345fd82d3eea0e10747b7119bb4c2947196` | PDG 2025 | Source-locked machine-readable benchmark |
| Electroweak mapping audit | `docs/data/external/particle_physics/pdg/electroweak_mapping_audit.json` | 892 | `4e77122bc0f37034347529e704e976798efc3816627f8ba27cfec4ae85d59b8c` | Query audit over PDG 2025 SQLite | Upstream mapping audit |
| Electroweak reference package | `docs/data/external/particle_physics/pdg/electroweak_reference_package.json` | 1915 | `273cab8ac548b9b031979de840b55dec252822a6b627517623b35a19286ee349` | Built from PDG 2025 SQLite plus checked local electroweak reference | Structured comparison package |
| Electroweak benchmark package | `docs/data/external/particle_physics/pdg/electroweak_benchmark_package.json` | 3198 | `20131262984227751a0046d34acfc44eaa9442c2c282eeead8b7fe143e48e8b2` | Built from the reference package plus checked-local neutron and running-angle layers | Structured benchmark package |
| Source-lock manifest | `Data/03_Research/source_lock_manifest.json` | 2493 | `48e8c233f9f41e8c099e26f7ed2a91a38ee9c9dfbc0354a5c184533e94c6eabc` | Topic-derived provenance package | Hashed by both primary verifier artifacts |
| Checked local electroweak reference | `Data/03_Research/pdg_electroweak_2024.json` | 664 | `c889ac1f8028a19dd5e22277026a3bb13d03ecdec27c7f9a409b3eb1c0aedc0e` | Topic-local checked reference | Checked local reference |
| Legacy electroweak CSV snapshot | `Data/Electroweak_LEP.csv` | 270 | `156f8ec63bc55f54b803066ac5302da478c9108aea579da6da0dfc74261ac7c4` | Topic-local working copy | Legacy local snapshot |
| Legacy downloader | `Data/Download_Electroweak.py` | 1231 | `63d59da9162f42aae4cd7a5cb31647429a990fb71356f83b729c664cabd82898` | Topic-local helper | Legacy acquisition helper |

## Workflow Gate Files

| File | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `source_evidence_intake_stub.json` | 2150 | `9368ec1e1f441944088f0fd49dce033f4e18c1d5456666534b7feb43c6e03d82` | provenance intake queue across electroweak branches | created by both primary verifiers |
| `source_evidence_readiness_matrix.json` | 2666 | `c6bb8f4f9960ec14b60ee54b4579c42b8f77663228ca745f5fd69549844fae88` | tracks review-readiness by branch | PDG core ready; other lanes still caveated or blocked |
| `branch_claim_gate.json` | 2297 | `17de302455c6cea7edaa3ab9a8d443b4271cebc066573f6aabb43c25123e7615` | lane-by-lane claim ceiling | 3 accepted benchmark branches, 3 blocked theory branches |

## Result Artifacts

| Artifact | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `Result/artifacts/0_6_electroweak_physics_verification.json` | 2569 | `1284decd7f42292ea896c422cff730b6dfdffbe2cbe46e89cc558170356e9d33` | primary wrapper/run-contract artifact | Confirms scripts/artifacts are present; does not override branch gates |
| `Result/artifacts/electroweak_pdg_validation.json` | 9273 | `298dbff108bdb35d3cff069f286c4fd04241358f176541ff1677c45cf82a8bb9` | source-locked PDG comparison artifact | Core PDG mass benchmark with explicit weak-mixing-angle mapping caveat |
| `Result/artifacts/electroweak_expanded_benchmark.json` | 13482 | `d8e776fd544f2e22327aa81dcf6426504248bfa6ac9f81b0395cbde499549dcf` | expanded electroweak benchmark artifact | Separates accepted benchmark branches from blocked theory branches |
| `Result/artifacts/electroweak_higgs_diagnosis.json` | 1577 | `e92d73c41b8ac05d5596146cd415f5baa56f207543f5646db388e912a1163b55` | Higgs diagnostic artifact | Diagnostic lane only; not a theory-closure artifact |

Repository note:

- Topic `0.6` now reads a structured electroweak reference package rather than carrying the weak-mixing-angle note inline in the verifier.
- Topic `0.6` also has an expanded benchmark package that keeps neutron lifetime as a checked-local benchmark gate and running-angle points as diagnostic-only.
- Both current verifier artifacts record hashes for the source-lock manifest, PDG SQLite files, mapping audit, reference package, and expanded benchmark package.
- The remaining caveat is specific and explicit: the effective weak-mixing-angle observable is not yet sourced from a direct upstream mapping in the current PDG SQLite workflow, and the mapping audit file records that negative result directly.
