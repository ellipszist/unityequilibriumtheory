# UPDATE LOG: UET GR Closed-Limit and Non-Closed Response

> **Scope:** `docs/core` with foundation dependency on `0.19_Gravity_GR`
> **Owner:** UET research collaboration
> **Purpose:** Record each blocker-narrowing wave in the GR correspondence
> program without upgrading claims ahead of generated evidence.

## Entries

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
