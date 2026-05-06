# Method

## Problem target

This topic studies whether UET-inspired information-drag ideas can reproduce selected particle-mass hierarchy benchmarks.

The current audit-backed method is narrower than the topic title. The primary verifier checks Higgs coupling modifiers against the SM-normalized `kappa = 1` baseline. Lepton/Koide and Planck-exponential branches are diagnostic until they receive separate artifacts and source-locked data choices.

## Core components

### Engine components
- `Code/01_Engine/Engine_Mass_Higgs.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Lepton_Mass.py`

### Research and comparison components
- `Code/03_Research/Research_Higgs_Coupling.py`
- `Code/03_Research/Research_Mass_Mechanism.py`
- `Code/03_Research/Verify_Mass_Generation.py`

The reviewed formula registry is `FORMULA_AUDIT.md`.

## Variable framing

- Primary modeled quantities: particle masses, coupling-strength terms, hierarchy ratios, and Koide-style quantities
- Current verifier-backed quantities: Higgs coupling modifiers `kappa`, particle masses in GeV, and average/max absolute deviation from `kappa = 1`.

## Evidence matrix

| Branch | Current implementation | Evidence class | Use in theory |
|:--|:--|:--|:--|
| Higgs coupling branch | Local `kappa` benchmark plus extracted external reference package | `C/B` | Primary verifier lane only. |
| Koide/tau branch | Diagnostic algebraic calculations with multiple local lepton files | `D/C` | Diagnostic branch only. |
| Planck exponential ansatz | Hardcoded exploratory branch | `D` | Hypothesis or fitted branch only. |
| Mechanism/hierarchy claims | Conceptual framing across branches | `D` | Not evidence by itself. |
| Source / claim workflow | Intake, readiness, and branch-claim gates | `Workflow gate` | Prevents Higgs consistency from being misread as a full mass-generation proof. |

## Assumptions

- The current package is an internal benchmark environment around selected lepton and Higgs-related files.
- The normalized Higgs `kappa` file already encodes a Standard Model comparison; passing the current gate is not by itself evidence for a UET-specific correction.

## Domain of validity

- Selected lepton-mass and coupling comparisons represented in topic-local PDG-style files.
- Current pass/fail interpretation is limited to the Higgs coupling verifier run contract.

## Excluded cases

- A complete derivation of all Standard Model masses or a full replacement of the Higgs mechanism.
- A formal proof of Koide, an independent prediction of tau mass from first principles, and a complete electroweak symmetry-breaking mechanism.

## Parameter sensitivity note

- Hierarchy fits and ratio claims remain sensitive to the chosen benchmark framing.
- Koide/tau claims are sensitive to whether the topic uses `lepton_data.json`, `pdg_2024_leptons.json`, or `PDG_Leptons.csv`.

## Claim Workflow

1. Run `Research_Higgs_Coupling.py` to regenerate the artifact and workflow files.
2. Use `Data/03_Research/source_lock_manifest.json` plus the external packages under `docs/data/external/particle_physics/...` as the normative provenance layer before editing any working-copy benchmark values.
3. Fill `Data/03_Research/source_evidence_intake_stub.json` only with real source evidence for the Higgs and lepton branches.
4. Use `Data/03_Research/source_evidence_readiness_matrix.json` as the provenance gate before changing working-copy data or claim class.
5. Check `Data/03_Research/branch_claim_gate.json` before treating Koide, tau, Planck-ansatz, or mechanism branches as evidence.
