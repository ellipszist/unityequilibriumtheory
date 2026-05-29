# Topic 0.8 Analysis Notes

This folder contains legacy and exploratory analysis notes for the muon g-2 topic. They
are useful for reconstructing benchmark history, but they are not the topic status
authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/muon_g2_2025_validation.json`
- `../Result/artifacts/muon_g2_2025_sensitivity.json`

## Current Controller

The current artifact separates source-locked 2025 benchmark compatibility from anomaly
closure:

- 2025 benchmark compatibility gate: `PASS`
- anomaly status gate: `BENCHMARK_ONLY`
- derivation gate: `OPEN`
- alternate-theory gate: `BLOCKED`
- downstream particle-support gate: `BLOCKED`
- claim-scope controller: `WARN`

## Claim Boundary

The current topic can export source-locked 2025 benchmark compatibility only. Do not use
legacy notes in this folder to claim:

- muon g-2 anomaly resolved
- Standard Model discrepancy closed
- alternate explanations ruled out
- new physics mechanism established
- first-principles anomaly derivation complete
- parameter-free prediction validated
- downstream particle-theory support established

When a legacy note says "resolved", "matched", "prediction", "proof", "final", or similar
language, read it through `muon_g2_claim_scope_gate.controller_status == WARN` and the
blocked export list in the canonical 2025 artifact.
