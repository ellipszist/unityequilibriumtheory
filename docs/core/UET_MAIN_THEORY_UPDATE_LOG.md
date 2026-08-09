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
