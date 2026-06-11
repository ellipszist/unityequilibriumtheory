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
