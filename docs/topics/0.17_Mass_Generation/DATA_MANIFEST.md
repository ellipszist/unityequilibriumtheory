# Data Manifest

Current data reality status: "real source referenced"

The topic now has extracted/source-referenced packages under `docs/data/external/particle_physics/...` for the Higgs mass checkpoint and the normative PDG lepton reference, plus a source-lock manifest that ties those packages back to topic-local working copies. It still does not have a raw upstream Higgs coupling table archive, so the topic remains below `manifested real dataset`.

## Source-lock manifest

| Item | Local path | Source | Role |
| :-- | :-- | :-- | :-- |
| `source_lock_manifest.json` | `Data/03_Research/source_lock_manifest.json` | Topic-local provenance manifest | Pins normative benchmark inputs and marks legacy/non-normative files explicitly. |

## Primary Verifier Input Package: Higgs Coupling

| Item | Local path | Bytes | SHA256 | Source | Provenance status | Unit convention | Benchmark role |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- |
| `higgs_coupling_data.json` | `Data/03_Research/higgs_coupling_data.json` | generated | generated | CMS Collaboration, Nature 607, 60-68 (2022), DOI `10.1038/s41586-022-04892-x`, as declared in file metadata | Source referenced, local normalized copy; exact extraction table and license terms not frozen. | `mass_GeV` in GeV; `coupling_kappa_observed` and `uncertainty` dimensionless. | Primary verifier gate for SM-normalized coupling consistency. |
| `higgs_coupling_cms_2022_reference_package.json` | `docs/data/external/particle_physics/higgs/higgs_coupling_cms_2022_reference_package.json` | external package | extracted/source-referenced package from topic-local working benchmark; DOI `10.1038/s41586-022-04892-x` | Extracted/source-referenced package; raw CMS table still not archived. | `mass_GeV` in GeV; `coupling_kappa_observed` and `uncertainty` dimensionless. | External provenance package for the primary verifier input. |
| `higgs_mass_combined.json` | `Data/03_Research/higgs_mass_combined.json` | 404 | `a906220bb0da26deba5693db5be5d99be58232dcdcb2939aea5ce97183a42eda` | CMS/ATLAS combined Higgs mass, DOI `10.1103/PhysRevLett.114.191803` | Source referenced, local normalized copy. | Higgs mass in GeV; width in MeV. | Context/reference input; not loaded by current primary script. |
| `higgs_mass_combined_atlas_cms_2015_reference_package.json` | `docs/data/external/particle_physics/higgs/higgs_mass_combined_atlas_cms_2015_reference_package.json` | external package | ATLAS/CMS combined mass reference package | Extracted/source-referenced package from topic-local working reference. | Higgs mass in GeV; width in MeV. | External provenance package for the Higgs mass checkpoint. |
| `source_evidence_intake_stub.json` | `Data/03_Research/source_evidence_intake_stub.json` | generated | generated | Topic-generated intake sheet for unresolved Higgs/lepton source metadata | Workflow control only; not evidence by itself. | Mixed; each target declares its own expected convention. | Landing zone before data rewrites or claim upgrades. |
| `source_evidence_readiness_matrix.json` | `Data/03_Research/source_evidence_readiness_matrix.json` | generated | generated | Topic-generated readiness gate derived from the intake stub | Workflow control only; records completeness, not scientific validation. | Not applicable. | Tracks which source packages still lack required evidence fields. |
| `branch_claim_gate.json` | `Data/03_Research/branch_claim_gate.json` | generated | generated | Topic-generated claim gate for separate mass-generation branches | Workflow control only; cannot raise claim strength beyond the current Higgs run contract. | Not applicable. | Separates Higgs, Koide/tau, Planck-ansatz, and mechanism claim ceilings. |

## Lepton/Koide Working Inputs

| Item | Local path | Bytes | SHA256 | Source | Provenance status | Unit convention | Benchmark role |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- |
| `lepton_data.json` | `Data/03_Research/lepton_data.json` | 666 | `3269a3c4fbcf4b195e861f1f417e0db87f3418e1ff7c7bab80b91949c5f7da53` | CODATA 2018 / PDG 2020, as declared in file metadata | Source referenced, local normalized copy; exact extraction not frozen. | Charged-lepton masses in MeV. | Diagnostic Koide/mass-mechanism branch. |
| `pdg_2024_leptons.json` | `Data/03_Research/pdg_2024_leptons.json` | 826 | `75cd3477e6d37b1d9a987ac15adeba35311cee21d85c578d2be0d31cc8b3109e` | Particle Data Group 2024, DOI `10.1093/ptep/ptac097`, URL `https://pdg.lbl.gov/` | Source referenced, local normalized copy; raw PDG source not cached. | Charged-lepton masses in MeV and kg; lifetimes in us/fs where present. | Preferred source-referenced lepton data candidate for future Koide verifier. |
| `pdg_2024_leptons_reference_package.json` | `docs/data/external/particle_physics/pdg/pdg_2024_leptons_reference_package.json` | external package | PDG 2024 charged lepton reference package | Extracted/source-referenced package from topic-local working reference. | Charged-lepton masses in MeV and kg; lifetimes in us/fs where present. | External provenance package for the normative lepton dataset choice. |
| `PDG_Leptons.csv` | `Data/PDG_Leptons.csv` | 119 | `8bffd3d691898abd5fb680d25b1d962436e2b2abde0a613e695fe9a2b9caafef` | PDG-style local CSV generated/downloaded by topic tooling | Local working copy; source year and extraction path not frozen in the file. | Charged-lepton masses in MeV. | Used by `Engine_Mass_Higgs.py` fallback/engine branch. |
| `PDG_Standard_Model_2024.csv` | `Data/PDG_Standard_Model_2024.csv` | 734 | `fe6827b8f01d3d1b9657c221e1d0984c3b7560565d12f5f9eaddb2fe2504d50d` | PDG-style local CSV generated/downloaded by topic tooling | Local working copy; source extraction path not frozen. | Mixed particle properties; units must be checked column-by-column before use. | Exploratory/reference only until tied to a verifier. |

## Data Preparation Scripts

| Item | Local path | Bytes | SHA256 | Role |
| :-- | :-- | --: | :-- | :-- |
| `Download_PDG.py` | `Data/Download_PDG.py` | 2224 | `7befbf6a313c5e54d198c8a5b5847538bba8dea6640761e3c7ed2d4181e65684` | Topic-local data acquisition/preparation helper. |
| `download_data.py` | `Data/03_Research/download_data.py` | 2766 | `57e55905a0684a68e3804893bf9d163ce767f8ce6d45d0fc1d40768a9a77c4f8` | Research data preparation helper. |

## Repository Note

- The current primary verifier still loads `higgs_coupling_data.json`; the external packages added here are provenance anchors plus normative-reference declarations.
- The next provenance wave should store exact raw Higgs coupling source tables under `docs/data/external/particle_physics/...` and document preprocessing from raw source to these normalized files.
- Claims using Koide or tau prediction must name `pdg_2024_leptons.json` or another normative file explicitly; `lepton_data.json` remains legacy until a branch-specific verifier replaces it.
