# Topic 0.3 Analysis Notes

This folder contains legacy and exploratory analysis notes for the cosmology and
Hubble-tension topic. These files are useful for reconstructing how the topic evolved, but
they are not the status authority.

Current claim authority lives in:

- `../README.md`
- `../LIMITATIONS.md`
- `../VERIFICATION_SPEC.md`
- `../DATA_MANIFEST.md`
- `../FORMULA_AUDIT.md`
- `../Result/artifacts/hubble_comparison_validation.json`

## Claim Boundary

The current verified result is a source-backed scalar published-value H0 benchmark. It may
be described as an internal benchmark pass for the implemented z=0 Planck-SH0ES gap rule.

It must not be described as:

- a resolved Hubble-tension literature claim
- a full Planck/SH0ES likelihood replication
- BAO/SN/CMB/high-z consistency closure
- a Lambda-CDM replacement
- a dark-energy or vacuum-energy solution
- a derived proof of `beta_frame = sqrt(alpha_em)`

When a legacy note below says "proof", "resolved", "paper-ready", "replacement", or similar
language, read it through the current controller:
`hubble_claim_scope_gate.controller_status == SCALAR_H0_BENCHMARK_ONLY`.

## Current Controller

The machine-readable controller is embedded in
`../Result/artifacts/hubble_comparison_validation.json`. The scalar benchmark branch can
pass, while bridge derivation, high-z, dark-energy, and full-likelihood claims remain open
or blocked.
