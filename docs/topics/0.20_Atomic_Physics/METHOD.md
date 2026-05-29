# Method

## Problem Target

This topic tests whether the atomic layer can reproduce selected hydrogen spectral benchmarks with explicit source data, constants, formulas, residuals, and artifact thresholds.

## Evidence Lanes

| Lane | Code/data path | Current status |
| :-- | :-- | :-- |
| Hydrogen Rydberg spectrum | `Research_Rydberg_Validation.py`, NIST/CODATA data | primary artifact, Claim Class C |
| Atomic formula bridge | `atomic_formula_bridge_manifest.json`, artifact `atomic_formula_bridge_manifest` | explicit standard-formula and UET dependency map; manifest only |
| Hydrogen-like ions | `hydrogen_like_ion_spectrum.json`, artifact `hydrogen_like_checkpoint` | provisional selected He+/Li2+ reduced-mass benchmark |
| Engine Balmer demo | `Engine_Atomic_Hydrogen.py` | secondary/demo; local rounded constant |
| Hydrogen level energies | `hydrogen_spectra_data.json`, `Proof_Hydrogen_Spectrum.py` | secondary lane; needs artifact |
| Three-body coupling smoke test | `Research_Atomic_ThreeBody.py` | code-health check, not physics validation |
| Multi-electron comparisons | `Research_Multi_Electron.py` | open lane |

## Variable Framing

| Variable | Meaning | Unit convention | Current role |
| :-- | :-- | :-- | :-- |
| `n_upper`, `n_lower` | transition quantum numbers | dimensionless integers | Rydberg term |
| `lambda` | wavelength | nm in data, m in formula inversion | primary spectral metric |
| `R_H` | Rydberg constant for hydrogen | m^-1 | CODATA benchmark constant |
| `R_infinity` | infinite-mass Rydberg constant | m^-1 | recorded context constant |
| `Z` | nuclear charge for one-electron ions | dimensionless integer | hydrogen-like checkpoint only |
| `E_n` | hydrogen level energy | eV | secondary level lane |
| `ppm` | relative residual | dimensionless parts per million | primary threshold metric |

## Primary Verification Method

1. Load NIST hydrogen spectrum working copy.
2. Load CODATA atomic constants working copy.
3. Parse Balmer and Lyman transitions.
4. Compute predicted vacuum wavelength using `R_H`.
5. Compute per-line residuals and fitted slope through origin.
6. Write `atomic_formula_bridge_manifest.json` to make the inherited Bohr/de Broglie/Rydberg chain and UET dependency roles explicit.
7. Load source-referenced He+ and Li2+ rows, apply reduced-mass hydrogenic scaling, and compute residuals under provisional thresholds.
8. Write artifact with hashes, thresholds, metrics, formula bridge metadata, checkpoint predictions, and limitations.
9. Write `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `branch_claim_gate.json` so the hydrogen benchmark stays separate from broader atomic-theory claims.

## Assumptions

- Vacuum wavelengths are used for the primary metric.
- `R_H` is source-locked from CODATA; this verifier does not derive it.
- Local NIST rows may be rounded or curated and need transcription precision notes before ppm-level public claims.
- Bohr/de Broglie/Rydberg formulas are inherited standard physics unless a separate UET derivation artifact proves otherwise.
- Hydrogen-like ion predictions use reduced-mass scaling for the selected He+ and Li2+ rows. Li III remains provisional because direct ASD row capture is still pending.

## Domain of Validity

- Selected hydrogen Balmer and Lyman lines in the topic-local NIST working copy.
- Claim Class C internal benchmark only.
- Formula bridge manifest language that explains dependency roles without claiming derivation.
- Provisional selected He+/Li2+ one-electron ion residuals under the reduced-mass hydrogenic benchmark gate.

## Excluded Cases

- First-principles UET derivation of `R_H`.
- Broad source-backed validation of hydrogen-like ions beyond the selected provisional He+/Li2+ rows.
- Fine structure, Lamb shift, hyperfine structure.
- Helium or many-electron atomic spectra.
- Full QED validation.

## Dependency Policy

- `0.6_Electroweak_Physics`, `0.17_Mass_Generation`, `0.21_Yang_Mills_Mass_Gap`, `0.23_Unity_Scale_Link`, and `0.0_Grand_Unification` may cite this topic only as a hydrogen Rydberg benchmark unless future artifacts extend the scope.
