# UET Foundation Compatibility Decision

This is a generated status synthesis, not a proof that UET is physically complete.
It answers three separate questions: internal mathematical consistency, correspondence
to standard physics, and whether an older theory is actually recovered as a special case.

## Decision

- Mathematical consistency: `BLOCKED_BY_REMAINING_LEGACY_OPERATOR_CONFLICT`
- Standard-physics correspondence: `PARTIAL_CONDITIONAL_NOT_GLOBAL`
- Old-theory nesting: `CONDITIONAL_ONLY`
- Overall foundation: `FOUNDATION_NOT_CLOSED`

The current answer is therefore: the canonical legacy_variational_v1 potential/source contract
is conditionally closed, legacy_local remains a quarantined comparator, and remaining operator/unit
conflicts plus unresolved physical correspondences still block the foundation.

## Conditional closures

| ID | Mode | Status | Meaning |
|---|---|---|---|
| `legacy_potential_derivative_pair` | `legacy_variational_v1` | `COMPATIBLE_CONDITIONAL` | The canonical radial derivative is closed conditionally; legacy_local remains explicitly non-variational. |
| `legacy_information_gradient_sign` | `legacy_variational_v1` | `COMPATIBLE_CONDITIONAL` | The canonical information-source sign matches the declared positive coupling; the historical sign is comparator-only. |

## Hard contradictions and conflicts

| ID | Status | Meaning |
|---|---|---|
| `legacy_information_operator` | `CONFLICT` | The declared box equation and the implemented first-order parabolic proxy are not the same equation without a derived limit and coefficient map. |
| `legacy_beta_unit_semantics` | `CONFLICT` | A dimensionless normalized coupling cannot be identified directly with Landauer energy in joules. |

## Special-case boundary

| Lane | Current decision |
|---|---|
| GR | Conditional local/algebraic closed limit only; not Einstein field equations |
| O(2) finite-density | Tree-level natural-unit EOS and ideal constitutive sector only |
| Legacy double well | Rejected reduction under the locked residual gate |
| Matter-space causality | Full candidate blocked; strict-CFL frozen-C reference passes |
| Global universe-open claim | Not established |

## Coverage boundary

- Core families inventoried: `12`
- Topic formula rows inventoried: `260` across `27` files
- Inventory gate: `BLOCKED`
- Code-only equation surfaces and complete observable/unit maps remain open.

## Claim boundary

The current repository evidence closes the potential/source contract only inside legacy_variational_v1, keeps legacy_local as a quarantined comparator, and retains declared operator/unit conflicts plus unresolved physical correspondences. It does not establish that all old theories are special cases of one UET equation, nor that UET is physically complete.

## Next controller

Resolve the remaining legacy information-operator and beta-unit conflicts, complete code-level F0-F3 correspondence and units, prove full coupled causal/energy behavior, then build observable and holdout tests before any universal or real-data claim.

Generated from `uet_foundation_compatibility_decision.json`; do not edit the generated result by hand.
