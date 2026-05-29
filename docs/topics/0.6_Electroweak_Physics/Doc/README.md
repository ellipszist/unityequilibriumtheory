# Topic 0.6 Analysis Notes

This folder contains legacy and exploratory analysis notes for the electroweak topic. They
are useful for reconstructing benchmark history, but they are not the topic status
authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/electroweak_pdg_validation.json`
- `../Result/artifacts/electroweak_expanded_benchmark.json`

## Current Controller

The expanded artifact separates selected benchmark agreement from theory closure:

- selected electroweak benchmark gate: `PASS`
- neutron-lifetime checked-local gate: `PASS`
- running-angle gate: `DIAGNOSTIC_ONLY`
- provenance caveat gate: `OPEN`
- theory-closure gate: `BLOCKED`
- claim-scope controller: `WARN`

## Claim Boundary

The current topic can export selected benchmark agreement only. Do not use legacy notes in
this folder to claim:

- full electroweak-sector closure
- Standard Model replacement
- gauge-theory derivation proved
- running weak-angle prediction validated
- all electroweak observables source-locked and passed
- superiority over QFT or the Standard Model

When a legacy note says "verified", "proved", "unified", "prediction", "smoking gun", or
similar language, read it through `electroweak_claim_scope_gate.controller_status == WARN`
and the blocked export list in the expanded artifact.
