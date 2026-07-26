# UET Research Standards Update Log

> Scope: shared research standards and the foundation-first equation workflow.

## [2026-07-26] - Foundation-first equation protocol

- Wave type: `workflow-repair pass`
- Added or changed: `EQUATION_RESEARCH_AND_PHYSICAL_CORRESPONDENCE_STANDARD.md`, core-scoped `AGENTS.md`, equation registry, protocol, dependency gate, and foundation audit.
- Verified with: `.venv\Scripts\python.exe docs/scripts/audit/audit_uet_equation_foundation.py --json`; `git diff --check`.
- Result: audit `PASS`; foundation gate `BLOCKED`.
- Blocker narrowed: equation work now has a named F0-F8 controller instead of relying only on scattered formula, lifecycle, and hardening prose.
- Still open: the initial registry is not exhaustive; complete the repository-wide equation inventory and standard-physics correspondence matrix.
- Next controller: `foundation_inventory_and_correspondence_registry_incomplete`.
- Claim impact: no physical claim upgrade; legacy core wording explicitly quarantined.
- Workflow linkage: applies the shared constitution, lifecycle, formula-audit, and hardening rules to `docs/core/`.
