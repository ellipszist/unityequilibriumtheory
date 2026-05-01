# Long-Term Core Research Hardening Roadmap

This roadmap turns the core research set, `0.0` through `0.26`, into a managed research
program rather than a collection of isolated topic pages.

## Operating Principle

Every core topic must expose five auditable layers before its public claims are upgraded:

1. Data provenance: upstream source, local path, hash/stable identifier, units, and benchmark role.
2. Formula registry: formulas, variables, units, constants, proof status, failure mode, and next hardening step.
3. Verification contract: command, inputs, threshold, baseline, artifact, and PASS/FAIL interpretation.
4. Claim class: README/METHOD wording mapped to the Claim and Evidence Rubric.
5. Dependency status: upstream topics, inherited assumptions, and downstream claim impact.

## Permanent Commands

```powershell
.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py
.venv\Scripts\python.exe docs\scripts\audit\audit_topic_standards.py
```

Use the first command for core research hardening progress. Use the second command for
repository standards consistency.

## Wave Plan

| Wave | Goal | Done when |
| :-- | :-- | :-- |
| 0 | Governance and audit infrastructure | Core audit, run history, priority report, and dependency map exist |
| 1 | Formula audit coverage | No core topic is missing `FORMULA_AUDIT.md`; bootstrap rows are replaced topic by topic |
| 2 | Real data and provenance | Weak data statuses are upgraded or explicitly limited |
| 3 | Verification hardening | Verifiers use live model outputs and write machine-readable PASS/FAIL artifacts |
| 4 | Cross-topic theory map | Dependencies, inherited limitations, and shared constants are explicit |
| 5 | Claim normalization and paper readiness | README/METHOD claims cite formula, data, verifier, and limitation artifacts |

## Current State

- Wave 0 is implemented as infrastructure.
- Wave 1 has bootstrap coverage for missing core formula audits; the next task is reviewing
  and replacing scaffold rows with explicit formula entries.
- `0.7_Neutrino_Physics` currently has a real verifier failure in the live engine angle gate.
- The audit queue is generated in `docs/meta/core_research_hardening_audit.md`.
- Historical run reports are stored under `docs/meta/core_research_hardening_runs/`.

## Repair Queue Policy

Always choose the next topic from `core_research_hardening_audit.md`, unless the user names a
specific topic. Within a topic, repair in this order:

1. Formula audit entries for main engine/research scripts.
2. DATA_MANIFEST provenance and unit/benchmark roles.
3. VERIFICATION_SPEC command, inputs, thresholds, and artifact path.
4. Verifier code if it uses hardcoded benchmark-compatible values instead of live outputs.
5. LIMITATIONS and README claim class.

## Non-Negotiables

- Do not promote `0.27+` future topics into core evidence.
- Do not treat benchmark-fed runtime values as first-principles derivations.
- Do not use PASS wording unless the artifact records the gate that passed.
- Do not hide FAIL artifacts; turn them into model-hardening work.
- Do not let `0.0_Grand_Unification` function as proof without downstream support.
