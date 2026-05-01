# Formula Audit: 0.22_Biophysics_Origin_of_Life

Audit status: reviewed registry, replacing the bootstrap scaffold.

Scope note: this topic currently combines origin-of-life, neural dynamics, synthetic biomarker, cancer, tissue-grid, protein-folding, and immune-system experiments. The shared theme is biophysical complexity under UET-style information/entropy metrics. Each subclaim must stay separated until each has its own data and verifier gate.

## Formula Registry

| formula_id | relation | code surface | variables and units | constant_origin | proof_status | verification_role | failure_mode | next_hardening_step |
| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |
| `T22-001` | biophysical Omega score from normalized biological/neural field | `Code/01_Engine/Engine_Biophysics.py::simulate_neural_state`; `compute_neural_omega` | `C` = normalized EEG/biological field; `Omega` = dimensionless UET score; `dx` = engine grid spacing | inherited UET core implementation | model score | Supports neural/Omega diagnostic comparisons | Normalized fields can hide physical units and preprocessing choices | Add per-dataset preprocessing manifest and artifact field for raw input identity |
| `T22-002` | life entropy update `S_internal += decay_rate - information_intake` | `Code/01_Engine/Engine_Life_Entropy.py::step` | `S_internal` = normalized entropy proxy; `decay_rate = phi_loss/I_max`; `information_intake = beta/I_max` | UET parameter file, not external biology constant | heuristic bridge | Origin-of-life/homeostasis sandbox | Can be overread as proof of living thermodynamics; lacks energy/environment entropy accounting | Add environment entropy ledger and tie to Topic `0.13` thermodynamic bridge |
| `T22-003` | lower bound `S_internal >= max(0.01, 1-kappa)` | `Engine_Life_Entropy.py::step` | normalized entropy proxy; `kappa` = UET coefficient | topic/model parameter | heuristic clamp | Prevents unphysical negative proxy entropy | Clamp can create artificial pass behavior | Treat as numerical guardrail, not biological law |
| `T22-004` | origin-of-life proxy `Entropy_Reduction = (Omega_random - Omega_life)/(Omega_random + 1e-9)` | `Engine_Biophysics.py::search_origin_of_life`; `Research_DNA_Entropy.py` | Omega scores dimensionless; reduction fraction | topic-generated random vs sinusoidal fields | simulation heuristic | Compares random soup to pre-structured pattern | `C_life` is imposed sinusoid, not emergent chemistry | Replace with a real reaction-network/protocell simulator or label simulation-only |
| `T22-005` | neural diversity `std(state)` after mean-field synchronization | `Code/03_Research/Research_Neural_Seizure.py`; `Proof_Neural_Dynamics.py` | diversity = standard deviation of synthetic neural state; coupling dimensionless | topic-local generator | simulation heuristic | Demonstrates hypersynchrony as low-diversity state | Not CHB-MIT/EEG evidence unless run on real EEG windows | Add real EEG window verifier and report phase labels |
| `T22-006` | EEG phase reference features: band powers, synchrony index, variance | `data/03_Research/seizure_phase_data.json`; `docs/data/external/biophysics/eeg/chb_mit/source_record.json` | band powers dimensionless fractions; synchrony index dimensionless; variance proxy | source-referenced local summary from CHB-MIT DOI `10.13026/C2K01R` | checked local reference, not raw source | Provenance anchor for seizure-phase discussion | Raw EDF files, exact record/window IDs, and preprocessing pipeline are not stored | Add raw PhysioNet source package or exact record/window hashes |
| `T22-007` | biomarker stability `stability = 1/(1+variance)` | `Code/03_Research/Research_Biomarker_Identification.py` | variance of synthetic gene expression; stability dimensionless | synthetic seeded benchmark | diagnostic-only | Primary verifier path; flags seeded positive controls | Synthetic data cannot support clinical biomarker claims | Replace with TCGA/real expression matrix and external provenance |
| `T22-008` | cellular decay `dC/dt = -beta I + kappa laplacian(C)` implemented through UET engine step | `Engine_Biophysics.py::simulate_cellular_decay`; `Research_Cancer_Cell_Chaos.py` | `C` = normalized coherence; `I` = entropy/mutation-pressure proxy; time step = engine dt | UET engine and topic proxy pressure | heuristic bridge | Cancer information-collapse sandbox | Mutation pressure and threshold are synthetic; no clinical calibration | Tie to real omics/cell-state dataset and fixed threshold |
| `T22-009` | TCGA-style coherence `C = 1/(1 + 0.1 mean(var(gene_expression)))` | `Code/03_Research/Research_TCGA_Entropy_Map.py`; `docs/data/external/biophysics/omics/tcga/source_record.json` | expression matrix synthetic; variance expression-unit dependent; `C` dimensionless | synthetic mock data with TCGA/GDC source target | diagnostic-only | Figure-generation and metric-shape demo | Script label says TCGA but generates mock data | Rename as synthetic or ingest real TCGA-derived matrix with cohort/files/hashes |
| `T22-010` | HP folding energy = `-1` per non-bonded H-H contact, divided by two for double counting | `Code/03_Research/Research_Protein_Folding_Siege.py` | lattice contacts dimensionless; energy in HP model units | standard HP lattice-model convention, sequence topic-local | benchmark/model heuristic | Protein-folding sandbox | Script uses biased random search and may overclaim optimality | Add known HP benchmark optimum and deterministic seed/artifact |
| `T22-011` | protocell complexity `sum(I_field)/(std(C_field)+1e-9)` | `Code/03_Research/Research_Self_Organizing_Protocell.py` | `I_field`, `C_field` normalized grid fields; complexity dimensionless | topic-local heuristic | open simulation | Origin-of-life sandbox | Benchmark file path uses `Data/` while repo uses `data/`; data may be absent | Fix path, source-lock prebiotic yields, and write PASS/FAIL artifact |
| `T22-012` | T-cell/cancer/clinical strategy scores | `Research_TCell_Immunity.py`; `Research_Clinical_Strategy_Comparison.py`; `Competitor_Cancer_Models.py` | score units vary by script; mostly normalized proxies | topic-local heuristics | open | Exploratory biomedical extensions | Too many biomedical claims share one verifier gate | Split into separate sub-verifiers or future topics |

## Claim Guardrails

| Claim area | Maximum current claim class | Reason |
| :-- | :-- | :-- |
| Synthetic biomarker verifier | `D` | Seeded synthetic positive-control check with artifact and hashes, not clinical evidence. |
| Neural seizure model | `D/C` | CHB-MIT metadata exists, but primary verifier is not a real EEG classifier. |
| Origin-of-life mechanism | `A/D` | Current simulations impose order/proxy complexity; no real chemical network validation. |
| Cancer/TCGA metrics | `D` | Several scripts use synthetic data while names imply real TCGA or clinical use. |
| Protein folding | `D` | HP-model sandbox without source-locked benchmark optimum. |

## Required Follow-Up

- Split `0.22` claims into sub-gates: life/homeostasis, EEG seizure, synthetic biomarker, cancer/TCGA, protein folding, protocell.
- Archive/source-lock CHB-MIT/PhysioNet raw records or record exact local raw hashes and preprocessing.
- Replace mock TCGA and biomarker matrices with real source-backed omics data before any biomedical claim upgrade.
- Tie homeostasis/negative-entropy language back to `0.13_Thermodynamic_Bridge` with an explicit environment entropy ledger.
- Keep README language at exploratory/model level until each subclaim has a verifier artifact.

## Audit Link

- Core audit report: `docs/meta/core_research_hardening_audit.md`
