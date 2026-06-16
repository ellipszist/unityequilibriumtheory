# UPDATE LOG: 0.4 Superconductivity/Superfluids

> **Scope:** `docs/topics/0.4_Superconductivity_Superfluids`
> **Owner:** Human collaborator and AI assistant
> **Purpose:** Record hardening waves that narrow the topic's current verifier and row-source blockers.

## Entries

### 2026-06-16 - Raw McMillan FAIL Cause Classification

- Scope: `0.4_Superconductivity_Superfluids` primary verifier blocker.
- Added or changed: added a machine-readable fail-cause gate classifying the current raw McMillan artifact failure.
- Files touched: `Data/03_Research/raw_mcmillan_fail_cause_gate.json`, `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `UPDATE_LOG.md`.
- Verified with: `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets`.
- Result: audit still reports one FAIL artifact for 0.4; packet points to the raw McMillan verifier artifact as the priority-10 blocker.
- Blocker narrowed: broad artifact `FAIL` is now classified as a mixed raw-McMillan model-family and row-source package blocker, with no current evidence that the 20 percent threshold or verifier run contract is the bug.
- Still open: Vanadium `lambda_ep` and `mu_star` convention review must clear before any coherent row patch can be considered; `Nb3Ge` and broader A15 row-specific numeric capture remain behind it.
- Next controller: `Data/03_Research/vanadium_source_lock_decision.json` remains `PATCH_BLOCKED`, controlled by Vanadium coupling and mu-star convention conflicts.
- Claim impact: no claim upgrade; wording remains an internal baseline diagnostic and blocker analysis only.
- Notes: no primary verifier rerun was done after adding the classification gate because no row input, threshold, or verifier logic changed in this wave.
