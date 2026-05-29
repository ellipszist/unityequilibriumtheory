# Topic 0.2 Analysis Notes

This folder contains legacy and exploratory analysis notes for the black-hole topic. They
are useful for reconstructing mechanism ideas, but they are not the topic status authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/0_2_black_hole_physics_verification.json`

## Current Controller

The current artifact allows a selected internal EHT shadow-size benchmark and comparator
geometry only:

- primary EHT benchmark: `PASS`
- comparator geometry: `COMPARATOR_ONLY`
- claim-scope controller: `WARN`
- singularity-resolution claim: `BLOCKED`
- GR replacement / image-domain EHT / GW-ringdown / CCBH claims: `BLOCKED`
- source evidence: topic working copy, not full upstream archive

## Claim Boundary

Do not use legacy notes in this folder to claim:

- black-hole singularity resolved
- GR replacement validated
- EHT image-domain validation
- GW/ringdown validation
- CCBH cosmological coupling proven
- black-hole information problem solved
- universal black-hole mechanism proof

When a legacy note says "resolved", "proved", "all masses resolved", "PASS", or similar
language, read it through `black_hole_claim_scope_gate.controller_status == WARN` and the
blocked-claim list in the primary artifact.
