# UET Main-Theory Closure Update Log

> **Scope:** `docs/core` main-theory closure program
> **Purpose:** Record completed closure waves, the artifact actually generated,
> and the next controlling blocker without promoting physical claims.

## Entries

### 2026-08-09 - Wave 0 foundation reconstruction and schema repair

- Scope: equation inventory, O(2)/GR program gate, and main-theory dependency graph
- Wave type: artifact and gate pass
- Added or changed: regenerated F0 inventory; removed a case-insensitive duplicate JSON key at its generator; added the Wave 0 audit, dependency graph, and gate
- Files touched: `build_uet_equation_inventory.py` output, `audit_uet_o2_superfluid_transport.py`, `audit_uet_main_theory_wave0.py`, generated artifacts, and focused tests
- Verified with: `.venv\Scripts\python.exe docs\scripts\audit\audit_uet_o2_superfluid_transport.py --strict --print-summary`; `.venv\Scripts\python.exe docs\scripts\audit\audit_uet_main_theory_wave0.py`; focused pytest
- Result: `PASS` for accounting/schema hygiene; foundation physics unchanged
- Blocker narrowed: repository-wide main-theory dependencies are now explicit and all required Wave 0 JSON inputs parse without case-insensitive duplicate keys
- Still open: minimal postulates and the unified parent-theory ontology contract
- Next controller: `main_axioms_and_parent_action_not_unified`
- Claim impact: no physical promotion
- Workflow linkage: first wave of the UET Main-Theory Closure Program
- Notes: the secondary fundamental-unification track is explicitly non-blocking for the primary effective-theory track


### 2026-08-09 - Wave 1 minimal postulates and ontology lock

- Scope: main-theory ontology, collective-coordinate lanes, quantum interpretation boundary, persistence, and closed/non-closed branch policy
- Wave type: contract and gate pass
- Added or changed: main-theory axioms specification, generated axiom registry, ontology gate, focused tests, and core required-reading linkage
- Files touched: UET_MAIN_THEORY_AXIOMS_SPEC.md, audit_uet_main_theory_axioms.py, generated registry/gate, core AGENTS.md, and tests
- Verified with: .venv\Scripts\python.exe docs\scripts\audit\audit_uet_main_theory_axioms.py; focused pytest
- Result: PASS_CONTRACT_ONLY
- Blocker narrowed: nine minimal postulates now have standard counterparts, falsification conditions, and prohibited inferences
- Still open: one integrated conservative covariant parent contract
- Next controller: covariant_parent_contract_not_integrated
- Claim impact: no physical promotion
- Workflow linkage: Wave 1 depends on the Wave 0 accounting gate
- Notes: C remains multi-lane; operational QM is the baseline; QBism/RQM remain comparison adapters


### 2026-08-09 - Wave 2 integrated conservative covariant parent

- Scope: scalar-tensor response, O(2) matter, Noether current, stress-energy, reciprocal coupling, exchange balance, and GR null limit
- Wave type: formula, implementation, registry, and gate pass
- Added or changed: integrated parent composer, public exports, deterministic verifier, formula audit, central-registry entry, and focused tests
- Files touched: uet_covariant_parent.py, audit_uet_covariant_parent.py, parent artifacts/gate, registry addendum/merge, core exports, and tests
- Verified with: parent verifier; equation-foundation audit; foundation compatibility audit with --no-write; 42 focused covariant tests
- Result: PASS_CONSERVATIVE_PARENT_ONLY
- Blocker narrowed: existing response, matter, and balance modules are now callable under one natural-unit conservative parent contract
- Still open: lane-specific covariant coarse-graining, dissipative SK/KMS sector, curved 3+1 evolution, SI observables, and external GR tests
- Next controller: lane_specific_covariant_coarse_graining_not_closed
- Claim impact: no physical promotion
- Workflow linkage: Wave 2 depends on the Wave 1 ontology gate
- Notes: foundation and compatibility statuses remain BLOCKED; the parent is a formula evaluator, not a metric PDE solver

### 2026-08-09 - Wave 3 lane-specific coarse-graining contract

- Scope: phase, charge, density, and telegraph collective-coordinate mappings
- Wave type: implementation, registry, verifier, and gate pass
- Added or changed: explicit many-to-one block-averaging API, provenance records, refinement and scale-dependence audits, public exports, and one central-registry entry
- Files touched: uet_coarse_graining.py, audit_uet_coarse_graining.py, Wave 3 artifacts/gate, registry merger, core exports, and focused tests
- Verified with: Wave 3 verifier; equation-foundation audit; compatibility audit with --no-write; 66 focused tests
- Result: PASS_DECLARED_FIELD_TO_COLLECTIVE_COORDINATE_ONLY
- Blocker narrowed: every active C lane now declares input type, scale, frame, units, information loss, and observable target without asserting a universal C identity
- Still open: microscopic-to-field derivation, covariant averaging, RG beta functions, dimensional observable calibration, and physical open-system memory
- Next controller: open_system_sk_kms_memory_not_derived
- Claim impact: no physical promotion
- Workflow linkage: Wave 3 depends on the integrated conservative parent and remains below the blocked foundation gate
- Notes: scale slopes are descriptive only; the density lane accepts an already-declared density field and does not derive mass from C

### 2026-08-09 - Wave 4 linearized open-system and classical KMS bridge

- Scope: retarded physical memory, Onsager response, classical fluctuation-dissipation, noise positivity, extended entropy accounting, and derived trace separation
- Wave type: constitutive implementation, formula audit, registry, verifier, and gate pass
- Added or changed: provenance-bearing coefficient records, exponential retarded kernel, classical KMS noise kernel, memory-storage ledger, public exports, and one central-registry entry
- Files touched: uet_covariant_open_system.py, audit_uet_covariant_open_system.py, Wave 4 artifacts/gate, registry merger, core exports, and focused tests
- Verified with: Wave 4 verifier; equation-foundation audit; compatibility audit with --no-write; 24 integrated foundation tests
- Result: PASS_LINEAR_CLASSICAL_KMS_CONTROL_ONLY
- Blocker narrowed: physical memory now acts before R_gen and irreversible memory dissipation is separated from reversible storage exchange
- Still open: doubled-field SK action, dynamical KMS symmetry, microscopic influence functional, covariant entropy current, external Kubo coefficients, and curved 3+1 evolution
- Next controller: strongly_hyperbolic_curved_3p1_theory_spine_not_implemented
- Claim impact: no physical promotion
- Workflow linkage: Wave 4 depends on the Wave 3 coarse-graining contract and remains simulation-only
- Notes: this is a linear classical constitutive control, not a full Schwinger-Keldysh derivation
