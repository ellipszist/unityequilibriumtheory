# 0.11 Closure Status Audit

**Date:** 2026-07-01
**Scope:** 0.11 Phase Transitions
**Audit type:** status reconstruction and Tier-A closure planning

## Current Answer

Topic 0.11 is important because it is one of the first places where UET tries to move from conceptual equation behavior into a physics benchmark: phase-transition critical behavior.

It is not closed as Tier A right now.

The current controlled status is:

```text
Readiness: Draft
Tier: B
Claim level: selected internal beta benchmark plus diagnostic mechanism lanes
Current controller: structure-factor / estimator-policy formula extraction and acceptance
```

This means the topic has useful internal evidence, but it cannot yet claim a full phase-transition theory, RG closure, universal critical behavior, or accepted dynamics-based 3D Ising scaling.

## What Is Already Working

| Lane | What works | Boundary |
| :-- | :-- | :-- |
| Primary beta benchmark | `Research_Critical_Exponents.py` writes a `PASS` artifact for the selected beta comparison. | This is a selected benchmark, not a full exponent-set or RG result. |
| Spatial-coupled operator | Core opt-in spatial modes exist and pass engine/operator availability gates. | Dynamics stayed mean-field-like in the scaling artifact. |
| Conserved-order spectral core | `conserved_order_spectral_v1` repaired the core implementation bridge to the topic Cahn-Hilliard engine. | Later finite-size/exponent gates remained blocked. |
| Structure-factor work | The blocker was narrowed from vague estimator uncertainty to specific formula/source-policy gates. | The accepted estimator formula and normalization mapping are still missing. |

## Why It Still Cannot Close

The blocker is not that nothing works. The blocker is that the claim-bearing scaling path is not yet accepted.

The latest controlling evidence says:

- The primary beta artifact can support only a selected beta-exponent benchmark.
- The dynamics/scaling artifacts still block universality claims.
- The current structure-factor RMS proxy is diagnostic-only and rejected as a source-backed second-moment estimator replacement.
- The source-family lowest-mode estimator implementation exists, but current conserved-order snapshots do not provide an accepted `S(0)` susceptibility observable.
- Policy-source candidates and abstract formula boundaries are packaged, but full-text formula extraction, UET normalization mapping, and estimator acceptance remain blocked.
- The latest source-archive localization gate only confirms temporary arXiv source archives and TeX member discovery; it does not extract or accept formulas.

## Current Machine-Readable Gate

The audit gate is saved at:

```text
Result/artifacts/0_11_closure_status_audit.json
```

The gate keeps the topic at `WARN` with:

```text
tier_a_closure_gate = BLOCKED
primary_beta_gate = PASS
scaling_claim_gate = BLOCKED
estimator_formula_gate = BLOCKED
source_archive_policy_gate = WARN
```

## Drift Found

The main documentation drift is in the tail of `UPDATE_LOG.md`.

Wave 39-41 wording says the topic is formally verified at the analytical projection level. That wording is not supported by the current topic index, verification spec, formula audit, or latest estimator/source gates. Treat those entries as historical notes that require claim-boundary correction, not as the current topic status.

The current controlling status remains the artifact/gate chain, especially Wave 38 and this closure audit.

## Path To Tier A

Tier A should require a narrow, explicit closure route:

1. Extract exact formula fragments from the localized TeX/PDF math sources for fixed-composition, canonical finite-size, and Cahn-Hilliard structure-factor estimators.
2. Decide an accepted estimator policy for conserved-order phase-transition fields: conserved susceptibility, finite-k/canonical estimator, or explicit rejection with a dynamics/window repair route.
3. Map the accepted estimator into UET normalized lattice units with unit/proxy boundaries.
4. Rerun finite-size/exponent gates using only the accepted estimator policy.
5. Require at least beta, nu/correlation-length behavior, finite-size consistency, and baseline separation before any dynamics-based universality claim.
6. Keep material critical-point calibration and RG closure as separate gates; do not smuggle them into a beta-only pass.
7. Only after the artifact chain passes should README/topic index wording move toward Tier A, and that promotion still needs human review.

## Safe Claim Boundary

Allowed now:

```text
Topic 0.11 has a passing internal selected-beta benchmark and several diagnostic operator lanes. The strongest open blocker is accepted structure-factor/correlation-length estimator policy for conserved-order scaling. The topic is promising but not closed.
```

Not allowed now:

```text
UET has solved phase transitions.
Topic 0.11 is verified as a full theory.
The current engine proves a 3D Ising universality shift.
The analytical beta projection alone closes the topic as Tier A.
```

## Wave 43 Update

Wave 43 narrows the formula-source blocker. The project now has `structure_factor_tex_formula_fragments.json` and `0_11_structure_factor_tex_formula_fragment_gate.json`, with 19 formula fragments preserved from the three localized source lanes. The current rerun reports the temporary source cache missing, so source-cache reproducibility is now part of the controller.

This does not close Tier A. The current controller moves to:

```text
restore_or_archive_sources_then_map_estimator_policy
```

Required next evidence: reacquired or repo-archived source archives with expected hashes, accepted estimator policy, UET normalization mapping, and finite-size admissibility before exponent or universality gates rerun.

## Wave 44 Update

Wave 44 adds `structure_factor_source_archive_policy.json` and `0_11_structure_factor_source_archive_policy_gate.json`. The policy manifest records the three arXiv e-print URLs, expected hashes, and candidate repo archive paths. `formula_fragment_preservation_gate == PASS` and `source_archive_policy_manifest_gate == PASS`, but `repo_archive_availability_gate == BLOCKED` and `temporary_cache_availability_gate == BLOCKED` with `0/3` archives available. The next controller remains source reacquisition or repo archival before estimator-policy mapping.
