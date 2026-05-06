# Method

## Problem target

This topic studies whether UET-inspired dynamic-cosmos framing can reproduce selected cosmic-flow and anomaly benchmarks.

## Core components

### Engine components
- `Code/01_Engine/Engine_Dynamic_Universe_v1.py`
- `Code/01_Engine/Engine_Dynamic_Universe_v2_Torus.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Dynamic_Viscosity.py`
- `Code/02_Proof/Proof_Systemic_Persistence.py`
- `Code/02_Proof/Proof_Toroidal_Cycle.py`

### Research and comparison components
- `Code/03_Research/Research_Cosmic_Flows.py`
- `Code/03_Research/Research_GvB_Evolution.py`
- `Code/03_Research/Research_Pioneer_Drag.py`

## Variable framing

- Primary modeled quantities: cosmic-flow quantities, dynamic-viscosity terms, anomaly corrections, and background-frame parameters

## Evidence matrix

| Layer | Current implementation | Evidence class | Use in theory |
|:--|:--|:--|:--|
| Laniakea map | Topic-local landmark flow visualization tied to a pinned source record | `D` | Supports only a provenance-checked visualization scaffold. |
| Cosmicflows subset | Source-referenced working copy for future residual gates | `D/C` | Candidate benchmark scaffold once frame/extraction metadata is locked. |
| Pioneer branch | Source-referenced diagnostic CSV without thermal competitor baseline | `D` | Diagnostic sandbox only. |
| Dependency gate | Claim ceiling inherited from `0.1`, `0.23`, `0.0` | `Workflow gate` | Prevents this topic from over-claiming through linked core topics. |
| Source-evidence gate | Intake stub plus readiness matrix for missing upstream files and frame metadata | `Workflow gate` | Blocks data rewrites and claim upgrades until source evidence is attached. |

## Assumptions

- The current scripts behave like effective cosmology comparisons on selected flow and anomaly datasets.

## Domain of validity

- Selected cosmic-flow, Pioneer-anomaly-style, and related dynamic-cosmos comparisons stored in the topic workspace.

## Excluded cases

- A full replacement of consensus cosmology or a universal derivation of all large-scale structure dynamics.

## Parameter sensitivity note

- Background selection and fitted anomaly terms remain sensitive in the current scripts.

## Dependency layer

| Dependency | Direction | Status |
|:--|:--|:--|
| `0.1_Galaxy_Rotation_Problem` | candidate downstream support target | `0.26` cannot claim galaxy-rotation success while `0.1` remains WARN under its current benchmark gate. |
| `0.23_Unity_Scale_Link` | conceptual bridge dependency | Must inherit exploratory/synthetic limits where cross-scale language is used. |
| `0.0_Grand_Unification` | receives this topic as an integration input | Integration-only until this topic has raw-source lock and residual gates. |

## Provenance hardening workflow

1. Run `Research_Cosmic_Flows.py` to regenerate the verifier artifact plus source/dependency workflow files.
2. Fill `Data/03_Research/source_evidence_intake_stub.json` only with real source path, frame metadata, and extraction evidence.
3. Use `Data/03_Research/source_evidence_readiness_matrix.json` to decide whether provenance is ready for source review.
4. Check `Data/03_Research/dependency_claim_gate.json` before using this topic to support claims that touch `0.1`, `0.23`, or `0.0`.

## Current provenance gate state

- Laniakea package: partial (`5/6` fields complete), blocked only by missing original raw/reconstruction filename
- Cosmicflows package: partial (`4/6` fields complete), blocked by missing original filename and subset-selection rule
- Pioneer anomaly package: partial (`5/6` fields complete), blocked only by missing original raw filename
- Pioneer thermal-recoil competitor baseline: still blank (`0/6` fields complete)
