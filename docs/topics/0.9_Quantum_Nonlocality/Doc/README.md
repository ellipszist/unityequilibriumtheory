# Topic 0.9 Analysis Notes

This folder contains legacy and exploratory analysis notes for CHSH/Bell tests, quantum
nonlocality, topology mechanisms, qubits, tunneling, double-slit work, and adjacent quantum
lanes. These files are useful for reconstruction, but they are not the topic status
authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/0_9_quantum_nonlocality_verification.json`

## Current Controller

The current artifact separates CHSH summary benchmark success from raw reconstruction and
mechanism claims:

- CHSH summary benchmark: `PASS`
- raw event reconstruction: `OPEN`
- UET mechanism gate: `BLOCKED`
- source evidence: partially ready, with blocked targets remaining
- claim-scope controller: `CHSH_SUMMARY_ONLY_RAW_AND_MECHANISM_BLOCKED`

## Claim Boundary

The current topic can export the source-referenced CHSH summary benchmark only. Do not use
legacy notes in this folder to claim:

- UET proves nonlocality
- nonlocality solved
- topological filament derivation verified
- standard quantum framework replaced
- raw Bell counts reconstructed
- qubit claims inherit CHSH PASS
- double-slit explained by CHSH
- tunneling validated by CHSH
- LC unity quantum mechanism proved

When a legacy note says "proof", "explains", "perfect", "4/4 PASS", or similar language,
read it through `chsh_claim_scope_gate.controller_status ==
CHSH_SUMMARY_ONLY_RAW_AND_MECHANISM_BLOCKED` and the blocked export list in the primary
artifact.
