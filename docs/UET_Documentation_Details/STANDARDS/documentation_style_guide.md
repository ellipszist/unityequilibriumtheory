# Documentation Style Guide

## Purpose

This guide standardizes how UET documentation describes evidence, limitations, and status.

## Documentation roles

- `Academic`: methods, assumptions, limitations, references, and evidence claims
- `Technical`: installation, architecture, APIs, package behavior, scripts, and data flow
- `Public`: concise overview and roadmap language for non-specialist readers
- `Archive`: historical context only; not a normative source

## Preferred evidence wording

Use these phrases where they match the actual support level:

- `Hypothesis`
- `Derived`
- `Fitted to existing data`
- `Out-of-sample tested`
- `Reproduced internally`
- `Externally replicated`
- `Peer-reviewed`

## Restricted wording

Do not use the following phrases in academic or technical docs unless explicit evidence and
review history are documented in the same topic:

- `Solved`
- `Verified`
- `Platinum Standard`
- `Production Grade`
- `One Equation to Rule Them All`

## Required claim hygiene

- Distinguish theory from benchmark behavior.
- Distinguish fitting from prediction.
- State when a result is internal only.
- Prefer explicit metrics over adjectives.
- Prefer exact counts from canonical metadata over rounded marketing numbers.

## Topic README minimum sections

- Problem
- Assumptions and scope
- Data sources
- Method
- Parameters and fitting status
- Metrics and thresholds
- Baselines
- Limitations
- Reproducibility
- Current readiness status
