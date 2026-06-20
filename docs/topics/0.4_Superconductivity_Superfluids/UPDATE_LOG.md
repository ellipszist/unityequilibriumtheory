# UPDATE LOG: 0.4 Superconductivity/Superfluids

> **Scope:** `docs/topics/0.4_Superconductivity_Superfluids`
> **Owner:** Human collaborator and AI assistant
> **Purpose:** Record hardening waves that narrow the topic's current verifier and row-source blockers.

## Entries

### 2026-06-20 - Raw McMillan FAIL Cause Controller Sync

- Scope: `0.4_Superconductivity_Superfluids` machine-readable FAIL-cause gate used by the core hardening audit packet.
- Added or changed: updated `Data/03_Research/raw_mcmillan_fail_cause_gate.json` so its `current_controller` points to the latest Vanadium branch source-completeness controller instead of the older lambda/mu convention-review wording.
- Files touched: `Data/03_Research/raw_mcmillan_fail_cause_gate.json`, `UPDATE_LOG.md`.
- Verified with: `.venv\Scripts\python.exe -m json.tool` on the fail-cause gate; `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets` after audit packet support was added.
- Result: the audit queue can now report the same current controller as the topic-local branch source-completeness gate: Vanadium `omega_log/omega2` or explicit Eliashberg equation-contract capture.
- Blocker narrowed: the generic FAIL queue now resolves to a named source-completeness controller instead of looping on threshold/verifier/model ambiguity.
- Still open: no primary verifier rerun is required because no model input, row value, threshold, or verifier contract changed.
- Next controller: satisfy `vanadium_eliashberg_equation_contract_first` or `vanadium_allen_dynes_moments_second`, then record Vanadium-specific evidence policy.
- Claim impact: no claim upgrade and no raw-gate membership change.

### 2026-06-20 - Vanadium Branch Source Capture Target Doc Sync

- Scope: `0.4_Superconductivity_Superfluids` packet-recommended docs for the Vanadium branch source-capture controller.
- Added or changed: linked the external Vanadium branch source-capture target from `README.md`, `LIMITATIONS.md`, and `VERIFICATION_SPEC.md` so the next blocker is visible without reading the whole topic.
- Files touched: `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `UPDATE_LOG.md`.
- Verified with: local search for `vanadium_branch_source_capture_target_packet.json` across the packet-recommended docs and source-completeness gate.
- Result: the front-door topic docs now identify the same next controller as the gate: inspect `10.1007/s10948-017-4295-y` first for an Eliashberg/Allen-Dynes equation or reproduction contract, then fall back to compatible `omega_log/omega2` capture.
- Blocker narrowed: the generic source-completeness stop is now surfaced as a named acquisition target sequence in the docs most likely to be opened first.
- Still open: no Vanadium alternate branch input table, verifier, artifact, row migration, or raw-row patch is allowed.
- Next controller: satisfy the source-capture target and then update the source-completeness gate with actual evidence.
- Claim impact: no claim upgrade, no threshold change, no verifier rerun, and no raw-gate membership change.

### 2026-06-20 - Vanadium Branch Source Capture Target

- Scope: `0.4_Superconductivity_Superfluids` Vanadium branch source-completeness acquisition controller.
- Added or changed: added `docs/data/external/condensed_matter/superconductivity/row_resolution_targets/vanadium_branch_source_capture_target_packet.json` and linked it from `Data/03_Research/vanadium_branch_source_completeness_gate.json`.
- Files touched: `docs/data/external/condensed_matter/superconductivity/row_resolution_targets/vanadium_branch_source_capture_target_packet.json`, `Data/03_Research/vanadium_branch_source_completeness_gate.json`, `UPDATE_LOG.md`.
- Verified with: local reconstruction from the existing Vanadium full-text numeric acquisition packet, raw-page checklist, and source-completeness gate; `.venv\Scripts\python.exe -m json.tool` on the new and changed JSON files.
- Result: the next acquisition target is now named explicitly: first inspect the `10.1007/s10948-017-4295-y` source family for an Eliashberg/Allen-Dynes equation or reproduction contract; fallback is source-backed `omega_log/omega2` capture from a compatible phonon-spectrum family.
- Blocker narrowed: the next controller is no longer generic source capture; it is a named branch-source target sequence with first and fallback capture routes.
- Still open: no Vanadium alternate branch input table, verifier, artifact, row migration, or raw-row patch is allowed.
- Next controller: satisfy `vanadium_eliashberg_equation_contract_first` or `vanadium_allen_dynes_moments_second`, then record Vanadium-specific evidence policy.
- Claim impact: no claim upgrade and no raw-gate membership change.

### 2026-06-20 - Vanadium Branch Source-Completeness Gate

- Scope: `0.4_Superconductivity_Superfluids` Vanadium alternate-branch input-table controller.
- Added or changed: added `Data/03_Research/vanadium_branch_source_completeness_gate.json` and linked it from the design packet, raw McMillan row-eligibility policy, `README.md`, `LIMITATIONS.md`, and `VERIFICATION_SPEC.md`.
- Files touched: `Data/03_Research/vanadium_branch_source_completeness_gate.json`, `Data/03_Research/vanadium_alternate_branch_design_packet.json`, `Data/03_Research/raw_mcmillan_row_eligibility_policy.json`, `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `UPDATE_LOG.md`.
- Verified with: local reconstruction from Vanadium `Tc`, `Theta`, `lambda`, and `mu_star` capture records under `docs/data/external/condensed_matter/superconductivity/row_resolution_targets/vanadium/`; `.venv\Scripts\python.exe -m json.tool` on the new/changed JSON gates; `.venv\Scripts\python.exe docs\topics\0.4_Superconductivity_Superfluids\Code\03_Research\Experiment_Superconductor_Data.py`; `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets` command output.
- Result: the Vanadium branch remains `BLOCKED`; `Tc` and Debye-proxy context are available for design, `lambda/mu*` are convention-pending, and `omega_log/omega2` or an explicit Eliashberg equation contract are missing.
- Blocker narrowed: the next controller is no longer generic source-complete input-table creation; it is specifically Vanadium `omega_log/omega2` or Eliashberg equation-contract capture plus branch evidence policy.
- Still open: no Vanadium alternate branch input table, verifier, artifact, row migration, or raw-row patch is allowed.
- Next controller: satisfy `vanadium_branch_source_completeness_gate.json`.
- Claim impact: no claim upgrade and no raw-gate membership change.

### 2026-06-19 - Vanadium Alternate Branch Design Packet

- Scope: `0.4_Superconductivity_Superfluids` Vanadium branch-migration controller.
- Added or changed: added a design-only packet for a future source-labeled Vanadium Eliashberg or Allen-Dynes branch verifier.
- Files touched: `Data/03_Research/vanadium_alternate_branch_design_packet.json`, `Data/03_Research/raw_mcmillan_row_eligibility_policy.json`, `Code/03_Research/Experiment_Superconductor_Data.py`, `Code/03_Research/Experiment_Allen_Dynes_Data.py`, `Code/03_Research/Experiment_Allen_Dynes_Policy_Dry_Run.py`, `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `UPDATE_LOG.md`.
- Verified with: local evidence reconstruction from Vanadium Tc/Theta/lambda/mu capture records and the existing Nb3Sn Allen-Dynes branch pattern; `.venv\Scripts\python.exe docs\topics\0.4_Superconductivity_Superfluids\Code\03_Research\Experiment_Superconductor_Data.py`; `C:\Users\santa\Desktop\uet_harness\.venv\Scripts\python.exe Experiment_Superconductor_Data.py` and `C:\Users\santa\Desktop\uet_harness\.venv\Scripts\python.exe Experiment_Allen_Dynes_Data.py` from `Code/03_Research` after path-root hardening; `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets`.
- Result: branch migration remains blocked; the packet records missing `omega_log/omega2` or explicit Eliashberg equation contract, cross-source convention review, and Vanadium-specific evidence policy.
- Blocker narrowed: the next controller is no longer generic "alternate branch"; it is a source-complete Vanadium branch input table.
- Still open: no Vanadium alternate branch verifier or artifact exists yet.
- Next controller: `vanadium_alternate_branch_source_labeled_inputs.json` after compatible source fields are captured.
- Claim impact: no claim upgrade and no raw-gate membership change.
- Notes: this mirrors the successful Nb3Sn Allen-Dynes branch pattern while keeping Vanadium design-only. The artifact-writing scripts now resolve back to repository root before using existing relative paths, preventing future reruns from writing under `Code/03_Research/docs/topics/...`. The hardening audit still reports one FAIL artifact, which is expected for this wave because the goal is blocker narrowing rather than raw-gate promotion.

### 2026-06-16 - Executable Row-Eligibility Artifact Schema

- Scope: `0.4_Superconductivity_Superfluids` primary raw McMillan verifier schema.
- Added or changed: updated the primary verifier to emit raw McMillan row-eligibility policy path/hash plus included, skipped, excluded, and branch-migration-candidate row classes.
- Files touched: `Code/03_Research/Experiment_Superconductor_Data.py`, `Result/artifacts/0_4_superconductivity_superfluids_verification.json`, `Data/03_Research/raw_mcmillan_row_eligibility_policy.json`, `Data/03_Research/branch_claim_gate.json`, `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `UPDATE_LOG.md`.
- Verified with: `.venv\Scripts\python.exe docs\topics\0.4_Superconductivity_Superfluids\Code\03_Research\Experiment_Superconductor_Data.py`; `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets`.
- Result: primary artifact schema is now `1.4`; `row_eligibility.summary` reports 10 included rows, 2 skipped rows, 0 excluded rows, 4 branch-migration candidates, and `metrics_changed_by_policy=false`.
- Blocker narrowed: the row-eligibility policy is now executable in the artifact schema; the next controller is branch design or stricter exclusion-rule implementation, not policy visibility.
- Still open: no Vanadium-compatible alternate branch verifier exists yet, and no row has a source-backed migration or exclusion decision.
- Next controller: source-labeled alternate branch design for Vanadium or stricter executable exclusion rules.
- Claim impact: no claim upgrade and no metric change; raw McMillan artifact remains FAIL.
- Notes: the branch-claim gate hash changed because the primary verifier regenerated it with the current Allen-Dynes artifact hash.

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