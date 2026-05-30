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
| `Data/03_Research/hydrogen_spectra_data.json` | Rounded hydrogen n-level working copy | SHA256 and NIST ionization-energy anchor recorded in artifact |
| `Data/03_Research/hydrogen_like_ion_spectrum.json` | Source-referenced He+ and Li2+ one-electron ion rows | SHA256, source status, and row policy recorded in artifact |
| `Data/03_Research/hydrogen_precision_spectroscopy_sources.json` | Precision spectroscopy targets for 1S-2S, Lamb shift, and 21 cm hyperfine | SHA256, target IDs, and model-block status recorded in artifact |
| `Data/03_Research/hydrogen_lamb_shift_correction_sources.json` | Source-referenced 1S and 2S Lamb-shift values for empirical 1S-2S residual handoff | SHA256, source rows, handoff rule, and model-block status recorded in artifact |
| `Data/03_Research/hydrogen_hyperfine_21cm_sources.json` | Source-referenced 21 cm hyperfine target and cross-check | SHA256, reference frequency, wavelength bookkeeping, and model-block status recorded in artifact |
| `Data/03_Research/hydrogen_hyperfine_fermi_constants.json` | Constants for leading Fermi-contact hyperfine baseline | SHA256, proton g factor source, formula role, and claim boundary recorded in artifact |
| `Data/03_Research/helium_many_electron_sources.json` | Neutral helium source targets and many-electron model requirements | SHA256, target wavelengths, and model-block status recorded in artifact |
| `Data/03_Research/atomic_formula_bridge_manifest.json` | Generated bridge manifest for Bohr/de Broglie/Rydberg inheritance and UET dependency roles | SHA256 recorded in artifact after generation |

## Metrics

- Per-line predicted vacuum wavelength in nm.
- Per-line wavelength error in ppm.
- Average wavelength error in ppm.
- Maximum wavelength error in ppm.
- Fitted slope through origin for `1/lambda` vs. Rydberg geometric term.
- Slope error relative to CODATA `R_H`.
- Hydrogen level-energy benchmark count, average error, and maximum error.
- Count of formula-bridge dependency steps.
- Hydrogen-like reduced-mass benchmark line count, average error, and maximum error.
- Precision source row count and required model component count.
- Nonrelativistic, leading Dirac, and empirical Lamb-handoff 1S-2S baseline frequencies/corrections, residual Hz, residual ppm, and sigma offsets against source measurement uncertainty where applicable.
- 21 cm hyperfine reference frequency, wavelength, metrology cross-check delta, and topic precision row delta.
- Leading Fermi-contact 21 cm baseline frequency, residual Hz, and residual ppm.
- Neutral helium source row count and required many-electron model component count.

## Fixed Thresholds

| Metric | PASS threshold |
| :-- | :-- |
| Average wavelength error | `<= 100 ppm` |
| Maximum wavelength error | `<= 250 ppm` |
| Fitted slope error | `<= 250 ppm` |
| Hydrogen level-energy average error | `<= 150 ppm` |
| Hydrogen level-energy maximum error | `<= 250 ppm` |
| Hydrogen-like average wavelength error | `<= 200 ppm` |
| Hydrogen-like maximum wavelength error | `<= 300 ppm` |

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
- hydrogen level-energy rows, source anchor, thresholds, residuals, and limitations
- hydrogen-like reduced-mass benchmark rows, source status, thresholds, residuals, and limitations
- precision spectroscopy source rows, model blockers, and required model components
- precision baseline, leading Dirac, and empirical Lamb-handoff residual values with explicit model-incomplete status
- 21 cm hyperfine source rows, wavelength bookkeeping, and explicit hyperfine-model-blocked status
- Fermi-contact baseline residual values and explicit correction-open status
- neutral helium source rows, model blockers, and required many-electron model components
- thresholds, metrics, per-line residuals, and limitations
- machine-readable `atomic_claim_scope_gate.controller_status`

## Interpretation

A PASS supports only a Claim Class C internal hydrogen-spectrum benchmark using the standard Rydberg relation. The formula bridge manifest supports only claim-boundary language about inherited Bohr/de Broglie/Rydberg formulas and dependency roles. The level-energy gate supports only rounded hydrogen n-level benchmark language. The hydrogen-like gate supports only provisional selected He+/Li2+ reduced-mass benchmark language. The precision spectroscopy and neutral-helium/many-electron gates are source-package only; the 1S-2S baseline gates are nonrelativistic, leading Dirac, and empirical Lamb-handoff residual diagnostics, while the 21 cm gates are source/wavelength bookkeeping and leading Fermi-contact residual diagnostics. It does not derive `R_H` from UET first principles and does not validate broad hydrogen-like ion coverage, first-principles QED, recoil/proton-size corrections, hyperfine Hamiltonian closure, neutral helium residuals, or many-electron atoms.
Topic-level source-evidence and branch-claim gates further limit this topic to hydrogen-benchmark usage unless dedicated atomic artifacts are added.
`atomic_claim_scope_gate.controller_status == WARN` is expected when the hydrogen benchmark, rounded level-energy benchmark, provisional selected ion benchmark, precision source package, nonrelativistic/Dirac/Lamb-handoff 1S-2S diagnostics, 21 cm source bookkeeping, and neutral helium source package are present while Rydberg derivation, direct level-table precision, direct Li III ASD capture, broad hydrogen-like ion validation, first-principles QED/recoil/proton-size/hyperfine correction models, and many-electron residual models remain open.
