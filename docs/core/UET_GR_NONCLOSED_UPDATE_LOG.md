# UPDATE LOG: UET GR Closed-Limit and Non-Closed Response

> **Scope:** `docs/core` with foundation dependency on `0.19_Gravity_GR`
> **Owner:** UET research collaboration
> **Purpose:** Record each blocker-narrowing wave in the GR correspondence
> program without upgrading claims ahead of generated evidence.

## Entries

### 2026-07-22 - Add conserved-current bridge and restrict causal scope

- Scope: local-frame decomposition of the O(2) Noether current into a coarse-grained conserved density and spatial current in a normalized 1D constitutive lane
- Wave type: formula-closure, discrete-conservation, energy-ledger, adiabatic-limit, principal-symbol, and claim-boundary pass
- Added or changed: covariant diffusion module, public exports, strict verifier, three generated artifacts, focused tests, monotonic upstream gates, and specification/reduction drift repair
- Files touched: `uet_covariant_diffusion.py`, its audit and tests, public exports, diffusion/program artifacts, upstream audits/tests/artifacts, the reduction contract, and this specification/log
- Verified with: six strict audits in dependency order and a 164-test combined covariant, causal, reduction, matter-action, diffusion, legacy-alignment, and matter-space regression suite
- Result: audit `PASS`, evidence `PARTIAL`, formula audit `WARN`; mass residual at most `5.55e-17`, energy-identity residual at most `2.88e-16`, Model-B limit residual at most `2.27e-13`, matter-space RHS mismatch `0.0`, exact-null-branch response mismatch `0.0`, and local-cone leakage/arrival error `0.0`
- Blocker narrowed: the regular covariant-to-diffusive map closes only as a declared coarse-grained constitutive-current bridge with an exact semi-discrete Model-B limit
- Still open: microscopic amplitude-to-charge-density matching, first-order hyperbolic closure for gradient/spinodal phase fields, closed-time-path/KMS coefficient matching, dissipative Bianchi closure, curved 3+1 reduction, SI mapping, and physical validation
- Next controller: `first_order_hyperbolic_phase_field_uv_closure_missing`
- Claim impact: class B retained; program remains `BLOCKED`; Topic 0.11 and Topic 0.19 status remain unchanged; global-universe closure remains unresolved
- Workflow linkage: the formula and claim audits separate the causal local-convex control from the fourth-order ultraviolet obstruction in the full Cahn-Hilliard lane
- Notes: finite flux relaxation alone does not make the gradient/spinodal equation relativistically causal; the trace remains derived and has no feedback, and no scalar amplitude is identified with density

### 2026-07-22 - Add conservative covariant matter-action pilot

- Scope: one complex scalar represented by an O(2) real doublet, coupled reciprocally to the covariant response scalar through one conservative action
- Wave type: formula-closure, action-reciprocity, current-conservation, dependency-gate, and claim-boundary pass
- Added or changed: covariant matter module, exact interaction derivatives, O(2) Noether current identity, coupled metric residual, strict verifier, three generated artifacts, focused tests, public exports, and monotonic upstream generators
- Files touched: `uet_covariant_matter.py`, `audit_uet_gr_covariant_matter.py`, core exports, two matter test files, generated matter/program artifacts, upstream audits/tests, and this specification/log
- Verified with: five strict audits in dependency order and a 129-test combined covariant, causal, reduction, matter-action, legacy-alignment, and matter-space regression suite
- Result: audit `PASS`, evidence `PARTIAL`, formula audit `WARN`; reciprocal finite-difference error `1.77e-13`, Noether identity and on-shell current-divergence errors `0.0`, tensor transformation error `6.94e-18`, and exact `epsilon_nc = 0` interaction residual `0.0`
- Blocker narrowed: a conservative scalar pilot now derives reciprocal response/matter coupling and an on-shell O(2) current from the same action
- Still open: amplitude-to-density identification, regular covariant-to-diffusive reduction, Cahn-Hilliard/closed-time-path derivation, coupled Bianchi identity with the new matter action, SI map, and particle or antimatter identification
- Next controller: `regular_covariant_to_diffusive_matter_reduction_missing`
- Claim impact: class B retained; program remains `BLOCKED`; Topic 0.11 and Topic 0.19 status remain unchanged
- Workflow linkage: the formula and claim audits separate exact conservative identities from the still-missing dissipative constitutive bridge
- Notes: the conserved O(2) charge is not yet the normalized matter field `C`; it establishes neither global-universe closure nor a particle-species interpretation

### 2026-07-22 - Map the covariant response sector to the normalized matter-space operator

- Scope: declared local-rest-frame and weak-curvature reduction of the response equation only
- Wave type: controlled-reduction, formula-map, dependency-gate, and claim-boundary pass
- Added or changed: exact coefficient/scaling map, reduction adapter, strict verifier, generated reduction contract, focused tests, public exports, and monotonic upstream generators
- Files touched: `uet_covariant_reduction.py`, `audit_uet_gr_weak_field_reduction.py`, core exports, two reduction test files, generated reduction artifacts, upstream audits/tests, and this specification/log
- Verified with: four strict audits in dependency order and a 110-test combined covariant, causal, reduction, legacy-alignment, and matter-space regression suite
- Result: audit `PASS`, evidence `PARTIAL`; response-acceleration mismatch `8.33e-17`, mapped speed error `0.0`, matter template preserved, and the `epsilon_nc = 0` adapter branch rejected
- Blocker narrowed: `controlled_covariant_to_matter_space_reduction_missing` is closed only for the response-sector coefficient map
- Still open: covariant matter action, reciprocal matter coupling, derivation of the required causal source, curved 3+1 reduction, principal/ghost analysis, SI map, and physical validation
- Next controller: `covariant_matter_action_and_reciprocal_coupling_missing`
- Claim impact: class B retained; program remains `BLOCKED`; Topic 0.11 and Topic 0.19 status remain unchanged
- Workflow linkage: formula and claim audits force the partial result to remain distinct from a full coupled derivation
- Notes: no derived trace feeds back; the reduction is disabled at the exact GR null branch and does not establish global-universe non-closure

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
