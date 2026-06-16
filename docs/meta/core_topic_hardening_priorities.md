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
4. Review and narrow existing `FORMULA_AUDIT.md` entries topic by topic, mapping each
   important formula to code, units, constants, proof status, verification role, and failure
   mode.
5. Use generated research wave packets to avoid reconstructing the same topic state from
   scratch in every AI session.

## Current Priority Signals

- Current repo-wide audit artifact: `docs/meta/core_research_hardening_audit.md`.
- Token-saving next-action queue: `docs/meta/core_research_next_actions.json`.
- Long-term roadmap: `docs/meta/long_term_core_research_hardening_roadmap.md`.
- Cross-topic dependency map: `docs/meta/core_topic_dependency_map.md`.
- Audit command: `.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py`.
- Latest audit found 27 core topics, 0 missing `FORMULA_AUDIT.md`, 0 missing root standards docs, 1 machine-readable FAIL artifact, and 0 README overclaim signals.
- Low claim-integrity scores in core topics should be fixed before public-facing wording is
  upgraded.
- Low verification scores mean the topic needs a runnable command, explicit metric,
  threshold, baseline, and artifact target.
- Low data-reality scores mean the topic must either point to a real upstream source or
  clearly label the current data as local, manual, placeholder, or exploratory.
- Missing, bootstrap, or open formula-audit entries block any claim that a topic is
  mathematically or physically mature.
- For token-saving work, generate the next-action packet first:

```powershell
.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --json --top 5
```

## First Repair Queue

Use `core_research_hardening_audit.md` as the source of truth for queue order. At the latest
audit, the top blockers are:

1. `0.4_Superconductivity_Superfluids`: verifier artifact records a machine-readable FAIL;
   treat this as the controlling model or threshold blocker.
2. `0.18_Mathnicry`: data status remains manual or placeholder; upgrade provenance or keep
   the limitation explicit.
3. Priority-4 data-provenance topics: `0.9_Quantum_Nonlocality`, `0.14_Complex_Systems`,
   `0.17_Mass_Generation`, `0.22_Biophysics_Origin_of_Life`,
   `0.24_Artificial_Intelligence`, `0.25_Strategy_Power_Economics`, and
   `0.26_Cosmic_Dynamic_Frame`.

For a compact packet for a single topic, run:

```powershell
.venv\Scripts\python.exe docs\scripts\audit\audit_core_research_hardening.py --topic 0.4_Superconductivity_Superfluids --emit-packets
```

## Verification

Run the standards audit after metadata or standards changes:

```powershell
.venv\Scripts\python.exe docs\scripts\audit\audit_topic_standards.py
```

For each hardened core topic, run the primary command declared in its
`VERIFICATION_SPEC.md`. If the command is absent or only conceptual, record that as a blocker
instead of treating the topic as verified.
