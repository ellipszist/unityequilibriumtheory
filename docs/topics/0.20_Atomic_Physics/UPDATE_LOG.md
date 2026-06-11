# UPDATE LOG: 0.20 Atomic Physics

> **Scope:** `docs/topics/0.20_Atomic_Physics/`
> **Owner:** `Codex + repository collaborators`
> **Purpose:** `Track multi-wave hardening of the hydrogen benchmark, helium predictive-candidate lane, and operator-acceptance blockers without replacing the primary artifact.`

## When to use

Use this log when `0.20` is updated across multiple hardening passes and a
reader needs a quick reconstruction of what changed, what was rerun, and which
blockers were actually narrowed.

## Log rules

- Log completed work, not proposed work.
- Name verifier or review commands only when they were actually run.
- Keep blocker names aligned with the artifact or manifest language.
- Keep each entry short enough to audit quickly.
- Treat the artifact, manifests, and topic package as canonical status.

## Entries

### 2026-06-11 - Add first operator parameter-set blueprint

- Scope: `atomic_predictive_v1_operator_parameters.json`, `Research_Rydberg_Validation.py`, topic docs, primary artifact
- Added or changed: Added a machine-readable blueprint for the first accepted parameter-set candidate, including allowed operator classes, required parameter rows, required source hashes, forbidden sources, and blocked-until items; surfaced that blueprint in the parameter-preflight gate.
- Verified with: `python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Rydberg_Validation.py`
- Result: The parameter lane still has `0` accepted parameter sets, but the next required parameter-set shape is now explicit in the manifest and artifact instead of living only in prose.
- Blocker narrowed: The repo now knows what the first real parameter set must look like before operator acceptance can advance.
- Still open: Accepted fixed CI/UET correction operator, first accepted parameter set, accepted residual emitter, and accepted operator uncertainty provenance.
- Claim impact: `no change`

### 2026-06-11 - Narrow parameter preflight root blocker

- Scope: `Research_Rydberg_Validation.py`, topic docs, primary artifact
- Added or changed: Reworked predictive-v1 parameter preflight reporting so an empty accepted-parameter set now registers as the root blocker, while the remaining field/class/lock/forbidden-source checks stay explicitly not yet evaluable instead of looking like independent failures.
- Verified with: `python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Rydberg_Validation.py`
- Result: Parameter preflight still blocks operator acceptance, but now shows `1` direct blocker and `4` not-yet-evaluated checks rather than a misleading `5/5` failure wall.
- Blocker narrowed: The next required move is now unambiguous: create the first accepted parameter set candidate before deeper parameter-field validation can even begin.
- Still open: Accepted fixed CI/UET correction operator, first accepted parameter set, accepted residual emitter, and accepted operator uncertainty provenance.
- Claim impact: `no change`

### 2026-06-11 - Normalize operator provenance candidate evidence

- Scope: `atomic_predictive_v1_operator_uncertainty_policy.json`, `Research_Rydberg_Validation.py`, primary artifact
- Added or changed: Narrowed the operator uncertainty-policy wording so it distinguishes diagnostic residual rows from accepted operator residual rows, and upgraded the operator implementation-provenance gate to emit live candidate evidence metadata (`exists`, `sha256`, entrypoint/return-key presence, parameter/residual/uncertainty artifact presence).
- Verified with: `python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Rydberg_Validation.py`
- Result: Predictive-v1 provenance still blocks operator acceptance, but the candidate state is now artifact-backed instead of only narrative: target module, parameter manifest, residual rows, and uncertainty policy are all traceable with live file hashes.
- Blocker narrowed: The remaining gap is more concretely "accepted operator missing" rather than "implementation evidence unclear".
- Still open: Accepted fixed CI/UET correction operator, non-empty accepted parameter set, accepted residual emitter, and accepted operator uncertainty provenance.
- Claim impact: `no change`

### 2026-06-11 - Add topic hardening update log

- Scope: `README.md`, `METHOD.md`, `UPDATE_LOG.md`
- Added or changed: Added a topic-level hardening log aligned to `For Work/24_TEMPLATE_UPDATE_LOG.md` and wired it into the topic package so `0.20` progress can be reconstructed without diff hunting.
- Verified with: `python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Rydberg_Validation.py`
- Result: `WARN` topic controller retained; hydrogen benchmark and selected reduced-mass lanes still pass while predictive-v1 publication readiness remains blocked.
- Blocker narrowed: The next work is now easier to trace back to named predictive-v1 blockers instead of broad "atomic model incomplete" wording.
- Still open: Accepted fixed CI/UET correction operator, validation-ready thresholds, and a non-NIST independent helium source package.
- Claim impact: `no change`

### 2026-06-08 - Freeze operator split and acceptance preflight

- Scope: `atomic_predictive_v1_operator_training_holdout_split.json`, `atomic_predictive_v1_operator_implementation_provenance.json`, `atomic_predictive_v1_operator_parameter_acceptance_preflight.json`
- Added or changed: Added the v1 calibration/holdout/cross-check split, narrowed implementation-provenance blockers with candidate evidence paths, and defined the field-level accepted-parameter preflight contract.
- Verified with: `git log --date=short --pretty=format:"%ad %h %s" -- docs/topics/0.20_Atomic_Physics` plus current review of `Result/artifacts/0_20_atomic_physics_verification.json`
- Result: Split gate records `5` calibration rows, `4` same-source-family holdout rows, and `2` CHIANTI cross-check rows with `0` overlap; implementation provenance remains `1/5` ready; parameter preflight remains `5/5` blocking with `0` accepted parameter sets.
- Blocker narrowed: Accepted-operator work is no longer a vague "implementation missing" state; row separation, provenance evidence classes, and future parameter-set fields are now named and machine-readable.
- Still open: Non-empty accepted operator parameters, accepted residual emitter, code identity lock, and operator uncertainty provenance.
- Claim impact: `no change`

### 2026-06-07 - Build predictive-v1 operator lane scaffolding

- Scope: `Research_Atomic_Operator_V1.py`, predictive-v1 manifests and gates, primary artifact
- Added or changed: Added the operator skeleton, diagnostic residual-row export, acceptance harness, publication-readiness gate, threshold validation blockers, and baseline-vs-diagnostic comparison machinery for the first helium predictive lane.
- Verified with: current review of `Result/artifacts/0_20_atomic_physics_verification.json` and topic-local commit history
- Result: Operator residual rows export `3` same-source-family diagnostic rows with populated `delta_energy_eV`; harness schema/no-leakage checks pass `5/5`; publication-readiness remains blocked `3/5`; diagnostic thresholds pass `3/3` but validation-ready thresholds remain `0`.
- Blocker narrowed: The repo now separates diagnostic quantum-defect improvement from an accepted `delta_uet_or_ci` operator and makes the publication blockers explicit.
- Still open: Accepted fixed correction operator, independent non-NIST helium lineage, and validation-ready threshold reclassification.
- Claim impact: `no change`
