# Data Manifest

Current data reality status: "real source referenced"

The topic now has extracted/source-referenced packages under `docs/data/external/particle_physics/...` for the Higgs mass checkpoint and the normative PDG lepton reference, plus a source-lock manifest that ties those packages back to topic-local working copies. It still does not have a raw upstream Higgs coupling table archive, so the topic remains below `manifested real dataset`.

## Source-lock manifest

| Item | Local path | Bytes | SHA256 | Source | Role |
| :-- | :-- | --: | :-- | :-- | :-- |
| `source_lock_manifest.json` | `Data/03_Research/source_lock_manifest.json` | 2388 | `8437155bc8cb83020099fe0a50dab3f39b6cd6b7a2de13464ce021c7aee609b5` | Topic-local provenance manifest | Pins normative benchmark inputs and marks legacy/non-normative files explicitly. |

## Primary Verifier Input Package: Higgs Coupling

| Item | Local path | Bytes | SHA256 | Source | Provenance status | Unit convention | Benchmark role |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- |
| `higgs_coupling_data.json` | `Data/03_Research/higgs_coupling_data.json` | 1648 | `4f5e512e7e62d27ffe03d32f7874fe2c4a50d04535a42c9110678ce565590b9c` | CMS Collaboration, Nature 607, 60-68 (2022), DOI `10.1038/s41586-022-04892-x`, as declared in file metadata | Source referenced, local normalized copy; exact extraction table and license terms not frozen. | `mass_GeV` in GeV; `coupling_kappa_observed` and `uncertainty` dimensionless. | Primary verifier gate for SM-normalized coupling consistency. |
| `higgs_coupling_cms_2022_reference_package.json` | `docs/data/external/particle_physics/higgs/higgs_coupling_cms_2022_reference_package.json` | 2289 | `9db34a19496a54814361bc60020373c1e85623ee2775b0bb80313b2487557003` | Extracted/source-referenced package from topic-local working benchmark; DOI `10.1038/s41586-022-04892-x` | Extracted/source-referenced package; raw CMS table still not archived. | `mass_GeV` in GeV; `coupling_kappa_observed` and `uncertainty` dimensionless. | External provenance package for the primary verifier input. |
| `higgs_mass_combined.json` | `Data/03_Research/higgs_mass_combined.json` | 404 | `a906220bb0da26deba5693db5be5d99be58232dcdcb2939aea5ce97183a42eda` | CMS/ATLAS combined Higgs mass, DOI `10.1103/PhysRevLett.114.191803` | Source referenced, local normalized copy. | Higgs mass in GeV; width in MeV. | Context/reference input; not loaded by current primary script. |
| `higgs_mass_combined_atlas_cms_2015_reference_package.json` | `docs/data/external/particle_physics/higgs/higgs_mass_combined_atlas_cms_2015_reference_package.json` | 1133 | `829b67bd2748513546653b61bf34086652907635684338fff6972c5447092a3d` | ATLAS/CMS combined mass reference package | Extracted/source-referenced package from topic-local working reference. | Higgs mass in GeV; width in MeV. | External provenance package for the Higgs mass checkpoint. |
| `source_evidence_intake_stub.json` | `Data/03_Research/source_evidence_intake_stub.json` | 5605 | `414d3a57c3c43f8b865e113f216e718dab7e16aa5df3470cdcb65b246b16b920` | Topic-generated intake sheet for unresolved Higgs/lepton source metadata | Workflow control only; not evidence by itself. | Mixed; each target declares its own expected convention. | Landing zone before data rewrites or claim upgrades. |
| `source_evidence_readiness_matrix.json` | `Data/03_Research/source_evidence_readiness_matrix.json` | 1878 | `933d34fc2f697b73e124592e44650ccacc003ddee967055a97ace453405eb601` | Topic-generated readiness gate derived from the intake stub | Workflow control only; records completeness, not scientific validation. | Not applicable. | Tracks which source packages still lack required evidence fields. |
| `branch_claim_gate.json` | `Data/03_Research/branch_claim_gate.json` | 1960 | `9dbc69b495ade51961d079c4f0ea773ac358f5952684c98e82be42e01a4ed41c` | Topic-generated claim gate for separate mass-generation branches | Workflow control only; cannot raise claim strength beyond the current Higgs run contract. | Not applicable. | Separates Higgs, Koide/tau, Planck-ansatz, and mechanism claim ceilings. |

## Lepton/Koide Working Inputs

| Item | Local path | Bytes | SHA256 | Source | Provenance status | Unit convention | Benchmark role |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- |
| `lepton_data.json` | `Data/03_Research/lepton_data.json` | 666 | `3269a3c4fbcf4b195e861f1f417e0db87f3418e1ff7c7bab80b91949c5f7da53` | CODATA 2018 / PDG 2020, as declared in file metadata | Source referenced, local normalized copy; exact extraction not frozen. | Charged-lepton masses in MeV. | Diagnostic Koide/mass-mechanism branch. |
| `pdg_2024_leptons.json` | `Data/03_Research/pdg_2024_leptons.json` | 826 | `75cd3477e6d37b1d9a987ac15adeba35311cee21d85c578d2be0d31cc8b3109e` | Particle Data Group 2024, DOI `10.1093/ptep/ptac097`, URL `https://pdg.lbl.gov/` | Source referenced, local normalized copy; raw PDG source not cached. | Charged-lepton masses in MeV and kg; lifetimes in us/fs where present. | Preferred source-referenced lepton data candidate for future Koide verifier. |
| `pdg_2024_leptons_reference_package.json` | `docs/data/external/particle_physics/pdg/pdg_2024_leptons_reference_package.json` | 1480 | `c75e9aac94a1390c3ec4fb17b40a84c854c1c6cb87395bd25b65c9fcf22c590b` | PDG 2024 charged lepton reference package | Extracted/source-referenced package from topic-local working reference. | Charged-lepton masses in MeV and kg; lifetimes in us/fs where present. | External provenance package for the normative lepton dataset choice. |
| `PDG_Leptons.csv` | `Data/PDG_Leptons.csv` | 119 | `8bffd3d691898abd5fb680d25b1d962436e2b2abde0a613e695fe9a2b9caafef` | PDG-style local CSV generated/downloaded by topic tooling | Local working copy; source year and extraction path not frozen in the file. | Charged-lepton masses in MeV. | Used by `Engine_Mass_Higgs.py` fallback/engine branch. |
| `PDG_Standard_Model_2024.csv` | `Data/PDG_Standard_Model_2024.csv` | 734 | `fe6827b8f01d3d1b9657c221e1d0984c3b7560565d12f5f9eaddb2fe2504d50d` | PDG-style local CSV generated/downloaded by topic tooling | Local working copy; source extraction path not frozen. | Mixed particle properties; units must be checked column-by-column before use. | Exploratory/reference only until tied to a verifier. |

## Data Preparation Scripts

| Item | Local path | Bytes | SHA256 | Role |
| :-- | :-- | --: | :-- | :-- |
| `Download_PDG.py` | `Data/Download_PDG.py` | 2224 | `7befbf6a313c5e54d198c8a5b5847538bba8dea6640761e3c7ed2d4181e65684` | Topic-local data acquisition/preparation helper. |
| `download_data.py` | `Data/03_Research/download_data.py` | 2766 | `57e55905a0684a68e3804893bf9d163ce767f8ce6d45d0fc1d40768a9a77c4f8` | Research data preparation helper. |

## Verification Artifacts

| Item | Local path | Bytes | SHA256 | Role |
| :-- | :-- | --: | :-- | :-- |
| `Research_Higgs_Coupling.py` | `Code/03_Research/Research_Higgs_Coupling.py` | 25902 | `b3560e793005b957b41619de6763943f3d1b6739e3f91e5cce0f1a02d144d674` | Primary verifier for the SM-normalized Higgs kappa consistency benchmark. |
| `0_17_mass_generation_verification.json` | `Result/artifacts/0_17_mass_generation_verification.json` | 10017 | `aabb0f0e12ccb3b893ac9995e2ccc60f7fd66e59de5928c0f2ba4b1541ce5633` | Machine-readable claim-scope artifact; PASS applies only to the Higgs kappa benchmark while uncertainty-aware mechanism gates remain open or blocked. |

## Repository Note

- The current primary verifier still loads `higgs_coupling_data.json`; the external packages added here are provenance anchors plus normative-reference declarations.
- The next provenance wave should store exact raw Higgs coupling source tables under `docs/data/external/particle_physics/...` and document preprocessing from raw source to these normalized files.
- Claims using Koide or tau prediction must name `pdg_2024_leptons.json` or another normative file explicitly; `lepton_data.json` remains legacy until a branch-specific verifier replaces it.
