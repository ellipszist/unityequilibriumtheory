# UPDATE LOG: UET GR Closed-Limit and Non-Closed Response

> **Scope:** `docs/core` with foundation dependency on `0.19_Gravity_GR`
> **Owner:** UET research collaboration
> **Purpose:** Record each blocker-narrowing wave in the GR correspondence
> program without upgrading claims ahead of generated evidence.

## Entries

### 2026-07-21 - Add restricted causal non-closed constitutive kernel

- Scope: retarded source history on a declared 1+1-dimensional local rest-frame slice
- Wave type: causal-support, characteristic, exchange, and claim-boundary pass
- Added or changed: exact telegraph Green evaluator, event-history convolution, causal exchange adapter, strict verifier, formula/contract artifacts, public API, tests, and monotonic upstream gates
- Files touched: `uet_covariant_nonclosed.py`, `audit_uet_gr_causal_nonclosed.py`, two focused test files, core exports, generated artifacts, and upstream generators/tests
- Verified with: strict causal audit, 20 focused tests, and a 92-test combined covariant/causal/legacy/matter-space regression suite
- Result: outside-cone leakage `0.0`, arrival error `0.0`, coordinate-scalar error `2.22e-16`, future-event influence `0.0`, and exchange closure `0.0`
- Blocker narrowed: a causal constitutive source exists on the restricted local slice
- Still open: closed-time-path derivation, curved 3+1 Green solver, parent-action ghost analysis, observable source map, controlled reduction, and physical validation
- Next controller: `controlled_covariant_to_matter_space_reduction_missing`
- Claim impact: class B retained; causal result is a constitutive ansatz and Topic 0.19 remains unchanged
- Notes: the physical source `j_phi` is not the derived trace `R`; global-universe closure remains unresolved

### 2026-07-21 - Close the conservative covariant exchange identity

- Scope: `docs/core` Noether/Bianchi identity and exchange-completed local ledger
- Wave type: derivation, gate, and claim-boundary pass
- Added or changed: covariant balance module, strict symbolic/numeric verifier, exchange contract, public exports, focused tests, and monotonic upstream generator behavior
- Files touched: `uet_covariant_balance.py`, `audit_uet_gr_covariant_balance.py`, two focused test files, core exports, generated artifacts, and prior closed-limit generator/tests
- Verified with: strict balance audit and a 72-test combined covariant, legacy-alignment, and matter-space regression suite
- Result: symbolic identity exact; numeric identity difference `1.39e-17`; exchange and sourced-shell closure `0.0`
- Blocker narrowed: `covariant_bianchi_exchange_balance_missing` is closed for the local candidate identity scope
- Still open: no causal source kernel, influence functional, curved-derivative solver, global energy theorem, characteristic analysis, or physical validation
- Next controller: `causal_nonclosed_influence_functional_missing`
- Claim impact: class B retained; program and Topic 0.19 remain blocked
- Notes: matter-number conservation remains an independent equation and global-universe closure remains unresolved

### 2026-07-21 - Implement conservative covariant parent and exact GR null limit

- Scope: `docs/core` covariant response formula evaluator and generated evidence
- Wave type: formula-closure and exact-limit verification pass
- Added or changed: natural-unit scalar-response action evaluator, tensor residuals, public exports, verifier, focused tests, and three generated artifacts
- Files touched: `uet_covariant_response.py`, `__init__.py`, `audit_uet_gr_closed_limit.py`, two focused test files, and core artifacts
- Verified with: strict generated audit and a 61-test covariant, legacy-alignment, and matter-space regression suite
- Result: exact GR closed-limit residual `0.0`; local tensor-transformation error `2.22e-16`; 61 tests passed
- Blocker narrowed: `covariant_parent_action_missing` is closed for the candidate formula-evaluator scope
- Still open: no Bianchi/exchange identity, causal influence functional, characteristic analysis, metric PDE solver, SI map, or physical GR validation
- Next controller: `covariant_bianchi_exchange_balance_missing`
- Claim impact: model evidence advances to class B; program and Topic 0.19 promotion remain blocked
- Notes: `epsilon_nc` is a nesting parameter, not a percentage openness; global-universe closure remains unresolved

### 2026-07-21 - Quarantine legacy Lorentz and Noether proof exports

- Scope: `docs/core/uet_lorentz.py`, `docs/core/uet_noether.py`, and generated alignment evidence
- Wave type: gate pass and claim-boundary pass
- Added or changed: explicit legacy evidence-status constants, removed completion banners, source audit, regression tests, and machine-readable alignment gate
- Files touched: `uet_lorentz.py`, `uet_noether.py`, `docs/scripts/audit/audit_uet_gr_legacy_alignment.py`, `test/test_gr_legacy_alignment.py`, `artifacts/legacy_covariance_alignment_gate.json`
- Verified with: `python docs/scripts/audit/audit_uet_gr_legacy_alignment.py --print-summary --strict` and `python -m pytest docs/core/test/test_gr_legacy_alignment.py -q`
- Result: audit `PASS`; physical covariance evidence `BLOCKED`; 5 tests passed
- Blocker narrowed: legacy PASS labels can no longer be exported as Lorentz, curved-spacetime, Noether, or Einstein-equation evidence
- Still open: six field-transform methods alias the original field; curved metrics are not wired; Noether diagnostics use an ad hoc spatial update
- Next controller: `covariant_parent_action_missing`
- Claim impact: wording narrowed; no readiness or evidence upgrade
- Workflow linkage: formula and claim audit applied before creating the replacement parent
- Notes: the legacy APIs remain available for compatibility and code archaeology
- Regression note: the broader legacy suite retains two failures in its time-dependent Noether case because a 1,000-point flattened field is combined with a 100-point coordinate vector; this pre-existing path remains outside proof use

### 2026-07-21 - Lock closure taxonomy and GR null hypothesis

- Scope: core ontology and research contract
- Wave type: claim-boundary pass
- Added or changed: research specification, ontology contract, claim gate, and
  handoff from the normalized matter-space prototype
- Files touched: `UET_GR_NONCLOSED_RESEARCH_SPEC.md`,
  `artifacts/gr_nonclosed_ontology_contract.json`,
  `artifacts/gr_correspondence_claim_gate.json`
- Verified with: JSON parse and focused document/claim review
- Result: `PASS` for ontology visibility; program remains `BLOCKED`
- Blocker narrowed: `universe_open_wording_ambiguous` is replaced by separate
  matter-number, stress-exchange, GR-limit, and global-closure states
- Still open: no covariant parent action or generated GR-limit artifact exists
- Next controller: `covariant_parent_action_missing`
- Claim impact: wording narrowed; no evidence or readiness upgrade
- Workflow linkage: applies the shared hardening and formula-audit standards
- Notes: global closure is explicitly unresolved; `epsilon_nc = 0` is the GR
  null model and `epsilon_nc != 0` remains an empirical hypothesis
