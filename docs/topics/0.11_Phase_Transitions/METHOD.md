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
- Cahn-Hilliard simulations should be treated as normalized mechanism diagnostics until seed, grid, morphology, and material-unit gates are added.

## Dependency policy

- `0.4_Superconductivity_Superfluids` may reuse this topic's transition language only as a mechanism analogy until material-specific gates exist.
- `0.13_Thermodynamic_Bridge` may reference critical behavior only with the selected-exponent limitation.
- `0.0_Grand_Unification` should index this topic as a selected benchmark plus normalized mechanism model, not a full universality proof.
