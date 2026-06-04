# Method

## Problem Target

This topic tests whether the atomic layer can reproduce selected hydrogen spectral benchmarks with explicit source data, constants, formulas, residuals, and artifact thresholds.

## Evidence Lanes

| Lane | Code/data path | Current status |
| :-- | :-- | :-- |
| Hydrogen Rydberg spectrum | `Research_Rydberg_Validation.py`, NIST/CODATA data | primary artifact, Claim Class C; transcription-bound residual diagnostics only |
| Atomic formula bridge | `atomic_formula_bridge_manifest.json`, artifact `atomic_formula_bridge_manifest` | explicit standard-formula and UET dependency map; manifest only |
| Hydrogen-like ions | `hydrogen_like_ion_spectrum.json`, artifact `hydrogen_like_checkpoint` | provisional selected He+/Li2+ reduced-mass benchmark plus C VI higher-Z stress test |
| Engine Balmer demo | `Engine_Atomic_Hydrogen.py` | secondary/demo; local rounded constant |
| Hydrogen level energies | `hydrogen_spectra_data.json`, artifact `hydrogen_level_energy_benchmark` | rounded source-referenced n-level benchmark |
| Precision spectroscopy targets | `hydrogen_precision_spectroscopy_sources.json`, `hydrogen_lamb_shift_correction_sources.json`, `hydrogen_hyperfine_21cm_sources.json`, `hydrogen_hyperfine_fermi_constants.json`, precision artifacts | source package plus nonrelativistic, leading Dirac, empirical Lamb-handoff, 21 cm bookkeeping, and Fermi-contact diagnostics; QED/recoil/proton-size/hyperfine model blocked |
| Neutral helium / many-electron targets | `helium_many_electron_sources.json`, `helium_transition_assignments.json`, `helium_ground_state_energy_sources.json`, `helium_quantum_defect_holdout_sources.json`, artifacts `helium_many_electron_gate`, `helium_transition_assignment_gap_gate`, `helium_medium_normalization_gate`, `helium_line_component_policy_gate`, `helium_ground_state_baseline_gate`, `helium_excited_state_target_gate`, `helium_excited_hydrogenic_residual_gate`, `helium_fixed_screening_baseline_gate`, `helium_quantum_defect_prediction_gate`, `helium_quantum_defect_holdout_gate`, `helium_quantum_defect_wavelength_holdout_gate` | source package plus photon-energy, term-assignment, medium-normalization, component-policy, ground-state baseline, excited-state target, zero-quantum-defect residual, fixed-screening heuristic baseline, limited quantum-defect prediction, same-source-family holdout, and restricted wavelength-holdout diagnostics; model blocked |
| Atomic prediction comparator | artifact `atomic_prediction_baseline_comparator_gate` | internal named baseline/candidate comparison table; external and CI/correlated comparator lanes remain open |
| Atomic uncertainty readiness | artifact `atomic_uncertainty_readiness_gate` | lane-wise uncertainty readiness map; fitted quantum-defect uncertainty diagnostics are partial, while broader propagation and uncertainty-aware thresholds remain incomplete |
| Atomic residual uncertainty budget | artifact `atomic_residual_uncertainty_budget_gate` | source-uncertainty budget rows where current sources or declared transcription-rounding bounds permit residual-to-uncertainty ratios; claim remains blocked |
| Legacy multi-electron code audit | artifact `legacy_multielectron_code_audit_gate` | classifies existing multi-electron/three-body scripts as smoke/demo code, not primary evidence |
| UET atomic operator readiness | artifact `uet_atomic_operator_readiness_gate` | maps required UET derivation/residual artifacts before any UET-specific atomic prediction claim |
| Fixed-parameter model readiness | artifact `atomic_fixed_parameter_model_readiness_gate` | lane-wise model readiness map including legacy-script exclusion; CI/correlated helium and UET atomic operator lanes remain missing |
| Predictive closure contract | artifact `atomic_predictive_model_closure_gate` | governance gate only; broad atomic prediction blocked until no-leakage splits, independent holdouts, uncertainty propagation, comparator baselines, and fixed-parameter CI/correlated or UET operators exist |
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
7. Compare rounded hydrogen `n=1..8` level rows against `E_n = -13.5984/n^2` using the NIST ionization-energy anchor.
8. Load source-referenced He+, Li2+, and C VI rows, apply reduced-mass hydrogenic scaling, compute He+/Li2+ under provisional thresholds, and record C VI as a higher-Z stress test.
9. Load precision spectroscopy targets for 1S-2S, Lamb shift, and 21 cm hyperfine as source-package rows.
10. Compute the nonrelativistic and leading Dirac 1S-2S baseline residuals as diagnostics, not as full precision correction models.
11. Apply source-referenced Lamb-shift values as an empirical 1S-2S residual handoff, not as a QED derivation.
12. Load 21 cm hyperfine source rows and compute frequency-to-wavelength bookkeeping.
13. Compute the leading Fermi-contact 21 cm baseline as a residual diagnostic, not as a closed hyperfine Hamiltonian.
14. Load neutral helium source rows, compute photon energies, attach upper/lower term assignments, derive vacuum-equivalent wavelengths from level-energy differences, check source line-component/blend policy, compute ground-state baseline residuals from NIST ionization-energy anchors, prepare excited-state binding targets from term energies, compute a zero-quantum-defect hydrogenic residual baseline, compute a fixed-screening heuristic baseline with parameters locked before evaluation, run a limited same-series quantum-defect leave-one-out prediction gate, test additional NIST source-family holdout rows, and predict restricted ground-state holdout wavelengths before any helium claim.
15. Build an internal baseline-comparator table so current prediction-like diagnostics are evaluated against named baselines instead of isolated residuals.
16. Build an uncertainty-readiness matrix so each atomic prediction/precision lane states source uncertainty, model uncertainty, propagation, and threshold status, including hydrogen line transcription-bound diagnostics and limited fitted quantum-defect uncertainty diagnostics where current helium series data permit it.
17. Build a residual uncertainty-budget gate so available source uncertainties are converted into residual-to-uncertainty ratios without promoting incomplete models.
18. Audit legacy multi-electron scripts so smoke/demo code cannot be mistaken for a CI/correlated helium spectral model.
19. Build a UET atomic-operator readiness gate so constant-origin, quantized-action, Hamiltonian/operator, correction, parameter-lock, and residual-gate requirements are explicit before any UET-derived spectrum claim.
20. Build a fixed-parameter model-readiness matrix so standard fixed baselines, empirical handoffs, fitted diagnostics, legacy smoke/demo scripts, and missing generative models cannot be conflated.
21. Build an atomic predictive-closure contract that lists the required no-leakage split, baseline comparator, fixed-parameter model, uncertainty, and domain-expansion gates before broad spectral prediction claims.
22. Write artifact with hashes, thresholds, metrics, formula bridge metadata, level-energy rows, selected ion rows, precision source/baseline gates, Dirac baseline gate, Lamb handoff gate, 21 cm source/Fermi gates, neutral helium source/gap/medium/component/ground-baseline/excited-target/hydrogenic-residual/fixed-screening/quantum-defect-prediction/holdout/wavelength-holdout gates, legacy code audit, UET operator readiness, comparator table, uncertainty readiness, residual uncertainty budget, fixed-parameter readiness, predictive-closure contract, and limitations.
23. Write `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `branch_claim_gate.json` so the hydrogen benchmark stays separate from broader atomic-theory claims.

## Assumptions

- Vacuum wavelengths are used for the primary metric.
- `R_H` is source-locked from CODATA; this verifier does not derive it.
- Local NIST rows may be rounded or curated. Hydrogen wavelength rows and helium holdout rows now include transcription-rounding bounds, but official/upstream source uncertainty and page-level transcription audit remain required before ppm-level public claims.
- Bohr/de Broglie/Rydberg formulas are inherited standard physics unless a separate UET derivation artifact proves otherwise.
- Hydrogen level-energy rows are rounded and source-referenced through the ionization-energy anchor until direct per-level ASD precision is captured.
- Hydrogen-like ion predictions use reduced-mass scaling for the selected He+ and Li2+ rows. Li III remains provisional because direct ASD row capture is still pending. C VI is recorded only as a higher-Z stress-test row until fine/QED policy is added.
- Precision spectroscopy rows support a source package plus nonrelativistic, leading Dirac, empirical Lamb-handoff 1S-2S residuals, 21 cm source bookkeeping, and Fermi-contact baseline only until QED/recoil/proton-radius/hyperfine models and uncertainty propagation are added.
- Neutral helium rows support source targets, photon-energy bookkeeping, term assignments, medium normalization, source component policy, ground-state baseline residual diagnostics, excited-state target preparation, zero-quantum-defect residual sizing, fixed-screening heuristic diagnostics, limited source-calibrated quantum-defect prediction diagnostics, same-source-family holdout diagnostics, and restricted wavelength-holdout diagnostics only until a correlated two-electron Hamiltonian/spectral model, independent holdout source family, official/source uncertainty capture, broader model-parameter uncertainty propagation, standard-air wavelength conversion policy for future holdout rows, resolved line-shape policy for precision use, and residual thresholds are added. Current helium holdout uncertainty fields are transcription-rounding bounds only, not official NIST measurement uncertainties; same-source holdouts use leave-one-out RMSE fallback model uncertainty when direct series scatter is unavailable.
- The fixed-screening helium baseline uses `Z_eff = 2 - 0.85` locked before evaluation. It is a heuristic comparator, not a CI/correlated model and not a UET atomic operator.
- The predictive closure contract is a claim-control artifact only. It does not make the current quantum-defect or hydrogenic gates first-principles predictions.
- The comparator table is internal only; it does not replace missing independent external holdouts or CI/correlated model baselines.
- The uncertainty-readiness matrix is not uncertainty-qualified validation; it records partial propagation for hydrogen transcription-bound and fitted quantum-defect diagnostics and identifies which lanes still need full propagation and uncertainty-aware thresholds.
- The residual uncertainty-budget gate computes ratios only where source uncertainty is already present or a bounded transcription policy is explicitly declared. It does not supply missing model uncertainty, official hydrogen/helium line measurement uncertainty, or pass/fail thresholds.
- The legacy multi-electron code audit is not a model result; it only records that existing multi-electron/three-body scripts are smoke/demo code and cannot substitute for CI/correlated helium evidence.
- The UET atomic-operator readiness gate is not a derivation; it only records the required artifacts before UET can claim to derive constants, quantized action, transition operators, correction terms, or residual predictions.
- The fixed-parameter model-readiness matrix is not a CI or UET atomic model; it only prevents fitted diagnostics, legacy smoke/demo code, and empirical handoffs from being mistaken for fixed-parameter predictions.

## Domain of Validity

- Selected hydrogen Balmer and Lyman lines in the topic-local NIST working copy.
- Claim Class C internal benchmark only.
- Formula bridge manifest language that explains dependency roles without claiming derivation.
- Rounded hydrogen `n=1..8` level-energy benchmark language.
- Provisional selected He+/Li2+ one-electron ion residuals under the reduced-mass hydrogenic benchmark gate, plus C VI stress-test residual language.
- Precision source-package readiness language for 1S-2S, Lamb shift, and 21 cm hyperfine targets, plus nonrelativistic, leading Dirac, empirical Lamb-handoff, 21 cm source-bookkeeping, and Fermi-contact diagnostic language.
- Neutral helium source-package readiness, photon-energy, term-assignment, medium-normalization, component-policy, ground-state baseline, excited-state target, hydrogenic residual, fixed-screening heuristic baseline, quantum-defect prediction, same-source-family holdout, and wavelength-holdout blocker language for future many-electron artifacts.
- Residual uncertainty-budget language for current precision, hyperfine, helium-ground, and helium-holdout diagnostics, without uncertainty-qualified validation.
- Predictive closure language that defines the minimum artifact requirements for future atomic-spectrum prediction claims.

## Excluded Cases

- First-principles UET derivation of `R_H`.
- Broad source-backed validation of hydrogen-like ions beyond the selected provisional He+/Li2+ rows and the C VI stress-test lane.
- Fine structure, Lamb shift, hyperfine structure.
- QED precision correction residual claims.
- Helium or many-electron atomic spectra.
- Full QED validation.

## Dependency Policy

- `0.6_Electroweak_Physics`, `0.17_Mass_Generation`, `0.21_Yang_Mills_Mass_Gap`, `0.23_Unity_Scale_Link`, and `0.0_Grand_Unification` may cite this topic only as a hydrogen Rydberg benchmark unless future artifacts extend the scope.
