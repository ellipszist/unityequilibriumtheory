# Topic 0.5 Analysis Notes

This folder contains legacy and exploratory analysis notes for the nuclear-binding,
hadron, QCD, and confinement branches. These files are useful for reconstructing topic
history, but they are not the topic status authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/nuclear_binding_source_locked_validation.json`
- `../Result/artifacts/nuclear_binding_full_table_diagnostic.json`

## Current Controller

The current strict artifact separates selected benchmark success from broader theory
claims:

- heavy-nucleus selected subset: `PASS`
- proton-radius anchor compatibility: `PASS`
- full AME2020 table: `DIAGNOSTIC_ONLY`
- light nuclei: `EXCLUDED_FROM_PASS`
- QCD / hadron / confinement claims: `BLOCKED`
- claim-scope controller: `WARN`

## Claim Boundary

Do not use legacy notes in this folder to claim:

- full AME2020 nuclear-binding pass
- light-nuclei validation
- general QCD derivation
- hadron mass model validation
- formal confinement proof
- complete strong-force theory

When a legacy note says "PASS", "derived", "confinement", "QCD bridge", "prediction", or
similar language, read it through `nuclear_claim_scope_gate.controller_status == WARN` and
the blocked export list in the strict artifact.
