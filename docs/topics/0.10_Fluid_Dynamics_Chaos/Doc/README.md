# Topic 0.10 Analysis Notes

This folder contains legacy notes, engineering reports, paper drafts, benchmark notes, and
research writeups for the fluid-dynamics and chaos topic. These files are useful for
reconstructing topic history, but they are not the topic status authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/fluid_benchmark_validation.json`

## Current Controller

The current artifact separates internal implementation benchmarks from external CFD and
theorem-level claims:

- internal speed benchmark: `PASS`
- finite-output diagnostic: `PASS`
- external CFD validation: `BLOCKED`
- physical Reynolds-number validation: `BLOCKED`
- Navier-Stokes theorem package: `BLOCKED`
- claim-scope controller: `WARN`

## Claim Boundary

The current topic can export internal solver-engineering benchmark behavior only. Do not
use legacy notes in this folder to claim:

- Navier-Stokes Millennium problem solved
- global smoothness proved
- turbulence closure established
- production CFD replacement
- universal fluid-engine superiority
- external CFD validation
- theorem-level physical closure

When a legacy note says "solved", "proved", "supreme victory", "Millennium", "production",
or similar language, read it through `fluid_claim_scope_gate.controller_status == WARN` and
the blocked export list in the primary artifact.
