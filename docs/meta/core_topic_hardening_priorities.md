# Core Topic Hardening Priorities

This file records the operating priority for standards work after the 2026-04-28 scope
clarification.

## Scope Policy

- Primary scientific hardening range: `0.1` through `0.26`.
- Foundation layer: `0.0_Grand_Unification`.
- Future-concept range: `0.27` onward, including both `0.33_*` topic folders and
  `0.39_Bio_Smart_City`.
- Future-concept topics must remain `Draft` / Tier `D` unless a separate standards pass
  adds real data provenance, runnable verification, formula audit coverage, and limitations.

## Hardening Order

1. Repair standards metadata and topic inventory consistency.
2. Harden core topics that already have real external datasets under `docs/data/external/...`.
3. Harden core topics with placeholder, manual, or embedded-local data by writing honest
   manifests and limitations before strengthening claims.
4. Expand `FORMULA_AUDIT.md` coverage across core topics, mapping each important formula to
   code, units, constants, proof status, verification role, and failure mode.

## Current Priority Signals

- Current repo-wide audit artifact: `docs/meta/core_research_hardening_audit.md`.
- Long-term roadmap: `docs/meta/long_term_core_research_hardening_roadmap.md`.
- Cross-topic dependency map: `docs/meta/core_topic_dependency_map.md`.
- Audit command: `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py`.
- Latest audit found 27 core topics, 24 missing `FORMULA_AUDIT.md`, 0 missing root standards docs, 1 machine-readable FAIL artifact, and 9 README overclaim signals.
- Low claim-integrity scores in core topics should be fixed before public-facing wording is
  upgraded.
- Low verification scores mean the topic needs a runnable command, explicit metric,
  threshold, baseline, and artifact target.
- Low data-reality scores mean the topic must either point to a real upstream source or
  clearly label the current data as local, manual, placeholder, or exploratory.
- Missing formula audits block any claim that a topic is mathematically or physically mature.

## First Repair Queue

Use `core_research_hardening_audit.md` as the source of truth for queue order. At the latest
audit, the top blockers are:

1. `0.5_Nuclear_Binding_Hadrons`: missing formula audit, manual/placeholder data status,
   and README overclaim signals.
2. `0.14_Complex_Systems`, `0.17_Mass_Generation`, `0.18_Mathnicry`, and
   `0.0_Grand_Unification`: missing formula audits with high priority scores.
3. `0.7_Neutrino_Physics`: verifier artifact now records a real FAIL in the live engine
   angle gate; do not present it as benchmark-passing until the model path is repaired.

## Verification

Run the standards audit after metadata or standards changes:

```powershell
.venv\Scripts\python.exe docs\scripts\audit\audit_topic_standards.py
```

For each hardened core topic, run the primary command declared in its
`VERIFICATION_SPEC.md`. If the command is absent or only conceptual, record that as a blocker
instead of treating the topic as verified.
