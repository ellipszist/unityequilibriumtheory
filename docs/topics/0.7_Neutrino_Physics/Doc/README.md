# Topic 0.7 Analysis Notes

This folder contains legacy and exploratory analysis notes for the neutrino topic. They are
useful for reconstructing hierarchy, mixing, oscillation, and benchmark-history work, but
they are not the topic status authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/nufit_6_0_validation.json`

## Current Controller

The current artifact separates NuFIT/KATRIN benchmark compatibility from neutrino-sector
derivation claims:

- live angle gate: `PASS`
- runtime mass-splitting gate: `PASS`
- absolute-mass KATRIN gate: `PASS`
- NuFIT provenance guard: `PASS`
- source pipeline gate: `PARTIAL`
- derivation gate: `OPEN`
- hierarchy gate: `BLOCKED`
- claim-scope controller: `WARN`

## Claim Boundary

The current topic can export NuFIT/KATRIN benchmark compatibility only. Do not use legacy
notes in this folder to claim:

- neutrino mass origin derived
- full PMNS matrix proved from UET
- mass hierarchy resolved
- sterile-neutrino prediction established
- full neutrino-sector closure
- unification evidence beyond benchmark constraint

When a legacy note says "PASS", "verified", "prediction", "hierarchy solution", "PMNS
proof", or similar language, read it through
`neutrino_claim_scope_gate.controller_status == WARN` and the blocked export list in the
primary artifact.
