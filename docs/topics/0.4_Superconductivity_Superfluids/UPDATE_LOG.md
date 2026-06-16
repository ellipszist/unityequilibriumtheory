# UPDATE LOG: 0.4 Superconductivity/Superfluids

> **Scope:** `docs/topics/0.4_Superconductivity_Superfluids`
> **Owner:** Human collaborator and AI assistant
> **Purpose:** Record hardening waves that narrow the topic's current verifier and row-source blockers.

## Entries

### 2026-06-16 - Raw McMillan Row-Eligibility Policy

- Scope: `0.4_Superconductivity_Superfluids` raw McMillan benchmark membership policy.
- Added or changed: added a machine-readable row-eligibility policy defining include, skip, non-exclusion, and branch-migration requirements for the raw McMillan diagnostic gate.
- Files touched: `Data/03_Research/raw_mcmillan_row_eligibility_policy.json`, `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `UPDATE_LOG.md`.
- Verified with: local reconstruction from verifier behavior, formula audit, row evidence gates, and Vanadium membership gate; `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets`.
- Result: the policy now blocks one-row cosmetic exclusion and makes High-Tc/non-BCS skipping versus raw-input diagnostic inclusion explicit.
- Blocker narrowed: the next controller is executable policy integration or a branch design packet, not an ad hoc Vanadium decision.
- Still open: the primary verifier does not yet emit the policy path/hash or separate included, skipped, excluded, and branch-migration row classes.
- Next controller: implement the policy in verifier schema or design a Vanadium-compatible alternate branch verifier.
- Claim impact: no claim upgrade and no metric change.
- Notes: this is a hardening control only; it preserves current raw-gate meaning.

### 2026-06-16 - Vanadium Benchmark Membership Gate

- Scope: `0.4_Superconductivity_Superfluids` Vanadium raw-gate membership controller.
- Added or changed: added a machine-readable membership gate deciding that Vanadium stays in the raw McMillan gate as a documented failure diagnostic for now.
- Files touched: `Data/03_Research/vanadium_benchmark_membership_gate.json`, `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `UPDATE_LOG.md`.
- Verified with: local evidence reconstruction from the raw artifact, Vanadium source-lock decision, convention-impact gate, formula audit, and branch claim gate; `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets`.
- Result: patch, exclusion, and immediate branch migration are all blocked; retaining Vanadium as a raw-gate failure diagnostic is the selected conservative state.
- Blocker narrowed: the next controller is no longer "what do we do with Vanadium?" broadly; it is a uniform raw McMillan row-eligibility and branch-migration policy.
- Still open: decide whether the next implementation wave should add verifier-level row-eligibility logic or design a source-labeled Vanadium-compatible alternate branch.
- Next controller: raw McMillan row-eligibility and branch-migration policy gate.
- Claim impact: no claim upgrade; this prevents cosmetic PASS-seeking and preserves the current artifact meaning.
- Notes: excluding Vanadium alone would still leave the raw McMillan average around 51.9 percent, so exclusion would not solve the topic-level FAIL.

### 2026-06-16 - Vanadium Convention Impact Gate

- Scope: `0.4_Superconductivity_Superfluids` Vanadium residual-row controller.
- Added or changed: added a machine-readable convention-impact gate comparing current, primary-page, source-backed coupling, and unsupported older-preview Vanadium McMillan cases.
- Files touched: `Data/03_Research/vanadium_convention_impact_gate.json`, `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `UPDATE_LOG.md`.
- Verified with: local McMillan formula preview over Vanadium candidate cases; `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets`.
- Result: source-backed `lambda=0.91` plus captured `mu_star` conventions still fail the raw McMillan row, with best source-backed preview still about 107 percent relative error; older `lambda=0.6` preview remains near-threshold but unsupported.
- Blocker narrowed: Vanadium is no longer just "lambda/mu convention unclear"; current source-backed convention values also do not rescue the raw McMillan gate.
- Still open: decide whether Vanadium remains a documented raw-McMillan row-source/model-family failure, moves to an Eliashberg/Allen-Dynes-compatible branch, or is excluded from the raw McMillan gate with explicit source-backed rationale.
- Next controller: Vanadium formula-family/benchmark membership decision before any row patch.
- Claim impact: no claim upgrade; working row remains unchanged and the primary raw McMillan artifact remains FAIL.
- Notes: no primary verifier rerun was done because no source-backed row patch was applied.

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
