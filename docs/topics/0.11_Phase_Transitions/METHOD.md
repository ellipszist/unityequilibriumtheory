# Method

## Problem target

This topic studies whether UET-style transition rules can reproduce selected critical-point and order-parameter benchmarks.

## Core components

### Engine components
- `Code/01_Engine/Engine_Phase.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Order_Parameter.py`

### Research and comparison components
- `Code/03_Research/Research_Critical_Exponents.py`
- `Code/03_Research/Research_Spatial_Coupling_Scaling.py`
- `Code/03_Research/Research_Spatial_Coupling_Sensitivity.py`
- `Code/03_Research/Research_Correlation_Length_Diagnostics.py`
- `Code/03_Research/Research_Finite_Size_Scaling_Diagnostics.py`
- `Code/03_Research/Research_Critical_Window_Relaxation_Diagnostics.py`
- `Code/03_Research/Research_Operator_Form_Requirement_Gate.py`
- `Code/03_Research/Research_Spatial_Coupled_V2_Diagnostic.py`
- `Code/03_Research/Research_Spatial_Coupled_V2_Component_Ablation.py`
- `Code/03_Research/Research_Model_C_Conserved_Order_Diagnostic.py`
- `Code/03_Research/Research_Conserved_Order_Core_Candidate.py`
- `Code/03_Research/test_05_phase_demixing.py`
- `Code/03_Research/test_phase_transitions.py`

## Variable framing

- Primary modeled quantities: critical temperature, order parameter, critical exponents, and transition-scale quantities
- Formula registry: see `FORMULA_AUDIT.md` for the distinction between selected exponent benchmarks, normalized Cahn-Hilliard dynamics, order-parameter diagnostics, and future material-data gates.

## Assumptions

- The topic is currently a phenomenological comparison package tied to selected critical-point datasets.
- The primary verifier also writes `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `branch_claim_gate.json` so selected beta compatibility stays separate from wider universality claims.

## Domain of validity

- Selected fluids and materials transition benchmarks represented in topic-local files.

## Excluded cases

- A general renormalization-group derivation for all transition classes.

## Parameter sensitivity note

- Critical exponents and fit settings remain dependent on the chosen benchmark subset.
- The current primary verifier is deliberately narrow: it checks only the beta critical exponent for a 3D Ising/liquid-gas benchmark.
- The Wave 5 spatial-coupling verifier is a dynamics diagnostic gate; it currently keeps universality-shift claims blocked.
- The Wave 6 coefficient sensitivity verifier narrows the blocker further: coefficient-only tuning remains mean-field-like, so the next repair needs operator-form or estimator revision.
- The Wave 7 correlation-length verifier checks whether the simulation window exposes critical correlation growth; it currently blocks beta-only universality promotion.
- The Wave 8 finite-size verifier checks multi-grid xi/L and Binder-style proxy behavior; it currently blocks universality promotion because xi/L stays small and the spatial lane does not separate from baseline.
- The Wave 9 critical-window relaxation verifier checks whether closer-to-Tc temperatures and longer runs fix the small-xi blocker; it currently shows the window extension is still local.
- The Wave 10 operator-form requirement verifier aggregates Waves 5-9 and blocks claim upgrades until a revised opt-in operator demonstrates nonlocal, conserved, or scale-dependent correlation growth and baseline separation.
- The Wave 11 v2 diagnostic tests the first such opt-in candidate using core-engine screened memory and conserved interface/game helpers; it currently blocks claim upgrades because correlation growth and lane separation did not appear.
- The Wave 12 v2 component-ablation verifier separates information-only, game-only, full, short-memory, and long-memory profiles; it currently shows no tested v2 component improves correlation length over baseline.
- The Wave 13 Model C verifier uses `Engine_Phase.py` to test conserved order-parameter dynamics as a different operator family; it currently supports Model C as a mechanism repair direction while leaving finite-size scaling and core integration open.
- The Wave 14 core-candidate verifier tests `conserved_order_v1` inside `uet_master_equation.py`; it currently confirms opt-in availability, legacy compatibility, and mass conservation, while blocking the explicit core path on mechanism response.
- The Wave 15 numerics-gap verifier compares Wave 13 spectral Cahn-Hilliard settings with the Wave 14 explicit core candidate; it currently blocks coefficient-only repair and requires a spectral or semi-implicit conserved-order core path before rerunning scaling claims.
- The Wave 16 spectral-core verifier tests `conserved_order_spectral_v1` inside `uet_master_equation.py` against the existing topic spectral engine; it passes implementation/mechanism bridge gates and moves the next blocker to finite-size/exponent scaling.
- Cahn-Hilliard simulations should be treated as normalized mechanism diagnostics until seed, grid, morphology, and material-unit gates are added.

## Dependency policy

- `0.4_Superconductivity_Superfluids` may reuse this topic's transition language only as a mechanism analogy until material-specific gates exist.
- `0.13_Thermodynamic_Bridge` may reference critical behavior only with the selected-exponent limitation.
- `0.0_Grand_Unification` should index this topic as a selected benchmark plus normalized mechanism model, not a full universality proof.
