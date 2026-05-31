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
| `Data/03_Research/hydrogen_like_ion_spectrum.json` | Source-referenced He+ and Li2+ one-electron ion benchmark rows plus C VI higher-Z stress-test row | SHA256, source status, benchmark lane, and row policy recorded in artifact |
| `Data/03_Research/hydrogen_precision_spectroscopy_sources.json` | Precision spectroscopy targets for 1S-2S, Lamb shift, and 21 cm hyperfine | SHA256, target IDs, and model-block status recorded in artifact |
| `Data/03_Research/hydrogen_lamb_shift_correction_sources.json` | Source-referenced 1S and 2S Lamb-shift values for empirical 1S-2S residual handoff | SHA256, source rows, handoff rule, and model-block status recorded in artifact |
| `Data/03_Research/hydrogen_hyperfine_21cm_sources.json` | Source-referenced 21 cm hyperfine target and cross-check | SHA256, reference frequency, wavelength bookkeeping, and model-block status recorded in artifact |
| `Data/03_Research/hydrogen_hyperfine_fermi_constants.json` | Constants for leading Fermi-contact hyperfine baseline | SHA256, proton g factor source, formula role, and claim boundary recorded in artifact |
| `Data/03_Research/helium_many_electron_sources.json` | Neutral helium source targets and many-electron model requirements | SHA256, target wavelengths, and model-block status recorded in artifact |
| `Data/03_Research/helium_transition_assignments.json` | NIST handbook/ASD term assignments for selected He I source rows | SHA256, assigned row count, missing row count, and source locators recorded in artifact |
| `Data/03_Research/helium_ground_state_energy_sources.json` | NIST helium ionization-energy anchors | SHA256, IE1/IE2 values, uncertainties, and baseline-residual claim boundary recorded in artifact |
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
- Hydrogen-like extended stress-test line count and residuals.
- Precision source row count and required model component count.
- Nonrelativistic, leading Dirac, and empirical Lamb-handoff 1S-2S baseline frequencies/corrections, residual Hz, residual ppm, and sigma offsets against source measurement uncertainty where applicable.
- 21 cm hyperfine reference frequency, wavelength, metrology cross-check delta, and topic precision row delta.
- Leading Fermi-contact 21 cm baseline frequency, residual Hz, and residual ppm.
- Neutral helium source row count and required many-electron model component count.
- Neutral helium photon-energy range and count of rows missing transition assignments.
- Neutral helium assigned-row count and remaining missing assignment count.
- Neutral helium air/vacuum medium-normalized row count, missing-normalization count, and derived factor range.
- Neutral helium line-component policy row count, blend row count, component count, and E1 source-policy pass count.
- Neutral helium ground-state observed total binding energy, independent-electron residual, uncorrelated variational residual, correlated-reference target, and gap-to-correlated-reference diagnostics.
- Neutral helium excited-state target unique-level count, transition-target count, excitation-energy range, and air-photon versus level-delta bookkeeping residual.

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
- hydrogen-like reduced-mass benchmark rows, source status, benchmark lanes, stress-test residuals, thresholds, and limitations
- precision spectroscopy source rows, model blockers, and required model components
- precision baseline, leading Dirac, and empirical Lamb-handoff residual values with explicit model-incomplete status
- 21 cm hyperfine source rows, wavelength bookkeeping, and explicit hyperfine-model-blocked status
- Fermi-contact baseline residual values and explicit correction-open status
- neutral helium source rows, model blockers, and required many-electron model components
- neutral helium photon-energy rows and transition-assignment blocker status
- neutral helium wavelength-medium normalization rows and residual-model blocker status
- neutral helium line-component/blend policy rows and residual-model blocker status
- neutral helium ground-state baseline residual rows, external correlated-reference target, and correlation-model blocker status
- neutral helium excited-state target rows, binding targets, air-photon versus level-delta bookkeeping residual, and spectral-model blocker status
- thresholds, metrics, per-line residuals, and limitations
- machine-readable `atomic_claim_scope_gate.controller_status`

## Interpretation

A PASS supports only a Claim Class C internal hydrogen-spectrum benchmark using the standard Rydberg relation. The formula bridge manifest supports only claim-boundary language about inherited Bohr/de Broglie/Rydberg formulas and dependency roles. The level-energy gate supports only rounded hydrogen n-level benchmark language. The hydrogen-like gate supports only provisional selected He+/Li2+ reduced-mass benchmark language; C VI is a higher-Z stress-test lane and does not count as broad ion validation. The precision spectroscopy and neutral-helium/many-electron gates are source-package only; the 1S-2S baseline gates are nonrelativistic, leading Dirac, and empirical Lamb-handoff residual diagnostics, while the 21 cm gates are source/wavelength bookkeeping and leading Fermi-contact residual diagnostics. Neutral helium photon energies, term assignments, wavelength-medium normalization, component policy, ground-state baseline residuals, external correlated-reference comparison, and excited-state target preparation are diagnostics only; correlated spectral residual modeling remains blocked. It does not derive `R_H` from UET first principles and does not validate broad hydrogen-like ion coverage, first-principles QED, recoil/proton-size corrections, hyperfine Hamiltonian closure, neutral helium spectral residuals, or many-electron atoms.
Topic-level source-evidence and branch-claim gates further limit this topic to hydrogen-benchmark usage unless dedicated atomic artifacts are added.
`atomic_claim_scope_gate.controller_status == WARN` is expected when the hydrogen benchmark, rounded level-energy benchmark, provisional selected ion benchmark, precision source package, nonrelativistic/Dirac/Lamb-handoff 1S-2S diagnostics, 21 cm source bookkeeping, and neutral helium source/ground/excited target package are present while Rydberg derivation, direct level-table precision, direct Li III ASD capture, broad hydrogen-like ion validation, first-principles QED/recoil/proton-size/hyperfine correction models, correlated helium spectral residuals, and many-electron residual models remain open.
