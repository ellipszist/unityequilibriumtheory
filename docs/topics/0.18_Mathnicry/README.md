---
layout: article
title: "UET Topic 0.18: Mathnicry"
description: "Conservative overview for the Mathnicry topic in the UET repository."
---

# 0.18 Mathnicry

## Problem

This topic groups together UET-inspired mathematical and mathematical-physics experiments
related to Riemann-style stability questions, algorithmic complexity, Collatz-like dynamics,
and other proof-oriented explorations.

## Current status

- Metadata status: `Draft`
- Audit tier: `B`
- Data status: `manual or placeholder`
- Claim posture: proof-attempt and research-exploration workspace, not a validated resolution of Millennium Problems

## What currently exists

- Multiple engines, proof scripts, and research scripts under `Code/`
- Topic-local analysis notes in `Doc/`
- Internal result logs and summaries in `Result/`

Representative scripts:

- `Code/01_Engine/Engine_Riemann_Field.py`
- `Code/02_Proof/Proof_Riemann_Siege.py`
- `Code/02_Proof/Proof_P_vs_NP_Scaling.py`
- `Code/02_Proof/Proof_Millennium_Grand_Slam.py`

## What this topic does not currently establish

- It does not establish that the Riemann Hypothesis, P vs NP, Navier-Stokes, or all
  Millennium Problems are solved.
- It does not yet document theorem targets, assumptions, domains of validity, or excluded
  cases in a topic-root `METHOD.md`.
- It does not yet define which proof scripts are heuristic, partial derivations, or
  full-proof attempts.
- It does not yet provide a standards-grade `VERIFICATION_SPEC.md` or `LIMITATIONS.md`.

## Proof-boundary notes

- This topic is the clearest example of why `proof-or-bust` matters.
- The presence of `Code/02_Proof` is not enough by itself to justify proof-level wording.
- Before stronger claims are allowed, the repo needs a document that maps each proof script to
  a precise theorem target, the assumptions used, the validity domain, and the remaining gaps.

## Reproducibility

Current exploratory commands:

```powershell
python docs/topics/0.18_Mathnicry/Code/01_Engine/Engine_Riemann_Field.py
python docs/topics/0.18_Mathnicry/Code/02_Proof/Proof_Riemann_Siege.py
python docs/topics/0.18_Mathnicry/Code/02_Proof/Proof_P_vs_NP_Scaling.py
```

These commands are useful for internal inspection, but they are not yet an audit-grade proof
or verification workflow.

## Next remediation steps

1. Create `METHOD.md` that defines theorem targets, symbols, assumptions, validity domains,
   and excluded cases.
2. Create `VERIFICATION_SPEC.md` that identifies the canonical scripts and required artifacts.
3. Create `LIMITATIONS.md` that lists unresolved cases and alternative interpretations.
4. Reclassify each proof script as heuristic, partial derivation, or full-proof attempt.

## Current readiness status

`Draft`
