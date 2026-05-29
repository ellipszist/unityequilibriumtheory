# Topic 0.1 Analysis Notes

This folder contains legacy and exploratory analysis notes for the galaxy-rotation topic.
They are useful for reconstruction, but they are not the topic status authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/galaxy_rotation_validation.json`

## Current Controller

The current artifact separates the run contract from model acceptance:

- run contract: `PASS`
- summary-row model gate: `FAIL`
- source-lock gate: `OPEN`
- baseline-comparison gate: `OPEN`
- replacement-claim gate: `BLOCKED`
- claim-scope controller: `FAIL`

## Claim Boundary

The current topic can be discussed as an internal summary-row benchmark over the repository
working copy. It must not be used to claim:

- dark-matter replacement
- full upstream SPARC curve replication
- galaxy-rotation problem solved
- zero curve fitting
- out-of-sample prediction validation
- MOND/dark-matter superiority
- galaxy-dynamics closure

When a legacy note below says "PASS", "solved", "paper-ready", "zero-parameter", or
similar language, read it through `galaxy_claim_scope_gate.controller_status == FAIL` and
`galaxy_model_gate.summary_row_model_gate.status == FAIL`.
