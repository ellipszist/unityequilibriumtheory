# Core Equation Research Instructions

These folder-scoped instructions apply to all work under `docs/core/`.

## Required reading order

Before editing an equation, parameter, operator, verifier, or core narrative, read:

1. the repository root `AGENTS.md`
2. `docs/topics/For Work/01_Project_Research_Constitution.md`
3. `docs/topics/For Work/02_Project_Workflow_and_Lifecycle.md`
4. `docs/topics/For Work/17_Formula_Audit_Standard.md`
5. `docs/topics/For Work/18_Research_Hardening_Workflow.md`
6. `docs/topics/For Work/EQUATION_RESEARCH_AND_PHYSICAL_CORRESPONDENCE_STANDARD.md`
7. `docs/core/artifacts/uet_foundation_dependency_gate.json`
8. `docs/core/artifacts/uet_equation_correspondence_registry.json`
9. `docs/core/artifacts/uet_foundation_equation_inventory.json`
10. `docs/core/artifacts/uet_foundation_correspondence_matrix.json`
11. `docs/core/artifacts/uet_code_surface_inventory.json`
12. `docs/core/artifacts/uet_core_equation_family_contract.json`
13. `docs/core/artifacts/uet_foundation_status_aggregate.json`
14. `docs/core/artifacts/uet_legacy_variational_closure.json`
15. `docs/core/artifacts/matter_space_causal_discretization_diagnostic.json`
16. `docs/core/artifacts/matter_space_causal_reference_verification.json`
17. `docs/core/artifacts/uet_foundation_compatibility_decision.json`

The foundation gate and registry are the controlling status sources for new core work.
Existing topic prose, old badges, and legacy validators do not override them.
The aggregate status is the cross-family stopping boundary: it may expose conditional
compatibility, but it cannot promote a blocked foundation.

## Mandatory workflow

Before changing or adding a core equation, regenerate the F0 inventory with `docs/scripts/audit/build_uet_equation_inventory.py`; its `inventory_gate_status` must remain visible in the wave record.

Every new equation or operator must complete the F0–F8 sequence in the equation research
standard. A blocked upstream gate blocks physical interpretation and downstream promotion.
Exploratory work may continue only when it is explicitly labelled `DRAFT`, `CANDIDATE`,
`INTERNAL`, or `SIMULATION_ONLY`.

Before describing a standard theory as a special case, or describing two UET lanes as the same physical variable, run docs/scripts/audit/audit_uet_foundation_compatibility.py and read docs/core/UET_FOUNDATION_COMPATIBILITY_AUDIT.md. COMPATIBLE_CONDITIONAL is not a global physics proof; CONTRADICTION, CONFLICT, BLOCKED, and REJECTED_REDUCTION remain controlling blockers.

Do not use topic numbers as a work queue. Follow the dependency graph.

## Core symbol rules

- `C` is a system-state coordinate; it is not universally mass.
- `Phi` is an effective response variable; it is not a metric, ether, particle, or
  information substance.
- `Pi` is `∂t Phi`.
- `R` / `I_trace` is a derived causal/history observable with no feedback in the new mode.
- mass, density, charge, stress-energy, and physical energy require explicit lane mappings.
- legacy `I`, `V`, `J_in`, and `J_out` must not be silently reinterpreted as `Phi`.

## Units and derivation rules

Every formula change must update the registry with its unit lane, variable meanings,
constant origin, derivation class, proof status, and failure mode. Normalized simulation
quantities must not be presented as SI physical quantities.

No constitutive ansatz, calibration relation, or benchmark anchor may be described as a
first-principles derivation.

## Compatibility and legacy work

Do not delete or silently rewrite legacy engines. Preserve compatibility adapters and
mark legacy equations as `LEGACY` or `COMPARATOR` in the registry. The historical
`docs/core/README.md` is not a current claim source until its wording is reconciled with
the foundation gate.

The older `docs/scripts/audit/validate_foundation.py` is a legacy validation runner. It is
not the foundation gate and its output must not be used as evidence that the theory is
stable or physically validated.

## Verification and artifacts

Before closing a wave:

- run the equation-foundation audit
- run the foundation compatibility audit when equation meaning, implementation, units, or limiting-case language changed
- run the relevant scientific verifier only if evidence-producing state changed
- check JSON parsing and dependency integrity
- sync core docs and update logs to the controlling blocker
- record the wave in `WORK_LEDGER/YYYY/YYYY-MM-DD.md`

Do not hand-edit generated verification output. Do not hide failed gates with clipping,
fallback parameters, or renamed statuses.

## Git scope

Check `git status` before editing. Preserve unrelated user changes. Stage only the files
belonging to the current standards or equation wave. Commit one coherent wave locally;
do not push or open a pull request unless the user explicitly requests it.
