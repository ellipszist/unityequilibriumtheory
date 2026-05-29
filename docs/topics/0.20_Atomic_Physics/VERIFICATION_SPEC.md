# Verification Spec

## Primary Command

```powershell
python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Rydberg_Validation.py
```

## Inputs

| Input | Role | Required identity |
| :-- | :-- | :-- |
| `Data/03_Research/nist_hydrogen_spectrum.json` | NIST hydrogen line working copy | SHA256 and source DOI/URL recorded in artifact |
| `Data/03_Research/codata_2018_atomic.json` | CODATA atomic constants working copy | SHA256 and DOI recorded in artifact |
| `Data/03_Research/atomic_formula_bridge_manifest.json` | Generated bridge manifest for Bohr/de Broglie/Rydberg inheritance and UET dependency roles | SHA256 recorded in artifact after generation |

## Metrics

- Per-line predicted vacuum wavelength in nm.
- Per-line wavelength error in ppm.
- Average wavelength error in ppm.
- Maximum wavelength error in ppm.
- Fitted slope through origin for `1/lambda` vs. Rydberg geometric term.
- Slope error relative to CODATA `R_H`.
- Count of formula-bridge dependency steps.
- Hydrogen-like checkpoint prediction count.

## Fixed Thresholds

| Metric | PASS threshold |
| :-- | :-- |
| Average wavelength error | `<= 100 ppm` |
| Maximum wavelength error | `<= 250 ppm` |
| Fitted slope error | `<= 250 ppm` |

## Artifact Target

- `Result/artifacts/0_20_atomic_physics_verification.json`
- `Data/03_Research/source_evidence_intake_stub.json`
- `Data/03_Research/source_evidence_readiness_matrix.json`
- `Data/03_Research/branch_claim_gate.json`
- `Data/03_Research/atomic_formula_bridge_manifest.json`

The artifact must record:

- PASS/FAIL status and claim class
- command and timestamp
- dataset paths, hashes, source labels, DOI/URL
- formula IDs
- atomic formula bridge path/hash and dependency roles
- hydrogen-like checkpoint predictions and limitations
- thresholds, metrics, per-line residuals, and limitations
- machine-readable `atomic_claim_scope_gate.controller_status`

## Interpretation

A PASS supports only a Claim Class C internal hydrogen-spectrum benchmark using the standard Rydberg relation. The formula bridge manifest supports only claim-boundary language about inherited Bohr/de Broglie/Rydberg formulas and dependency roles. It does not derive `R_H` from UET first principles and does not validate hydrogen-like ions, fine structure, Lamb shift, helium, or many-electron atoms.
Topic-level source-evidence and branch-claim gates further limit this topic to hydrogen-benchmark usage unless dedicated atomic artifacts are added.
`atomic_claim_scope_gate.controller_status == WARN` is expected when the hydrogen benchmark passes while Rydberg derivation, level-energy, hydrogen-like ion validation, fine-structure, Lamb-shift, helium, and many-electron branches remain open.
