# Method

## Problem Target

This topic tests whether the atomic layer can reproduce selected hydrogen spectral benchmarks with explicit source data, constants, formulas, residuals, and artifact thresholds.

For multi-wave hardening history, use `UPDATE_LOG.md`. It records what changed,
what was rerun, and which predictive-v1 blockers were narrowed without
replacing the artifact as the canonical status source.

## Evidence Lanes

| Lane | Code/data path | Current status |
| :-- | :-- | :-- |
| Hydrogen Rydberg spectrum | `Research_Rydberg_Validation.py`, NIST/CODATA data | primary artifact, Claim Class C; transcription-bound residual diagnostics only |
| Atomic formula bridge | `atomic_formula_bridge_manifest.json`, artifact `atomic_formula_bridge_manifest` | explicit standard-formula and UET dependency map; manifest only |
| Hydrogen-like ions | `hydrogen_like_ion_spectrum.json`, artifact `hydrogen_like_checkpoint` | provisional selected He+/Li2+ reduced-mass benchmark plus C VI higher-Z stress test |
| Hydrogen-like domain coverage | artifact `hydrogen_like_domain_coverage_gate` | coverage diagnostic only; maps represented `Z=2,3,6`, source-status counts, same-transition limitation, and broad-validation blockers |
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
| Predictive model specification | artifact `atomic_predictive_model_spec_gate` | model-specification only; requires `standard_baseline + delta_uet_or_ci`, locked parameters, holdouts, comparators, uncertainty propagation, and domain lanes |
| First predictive implementation candidate | artifact `atomic_first_predictive_implementation_candidate_gate` | selects helium quantum-defect same-source-family holdouts as the first diagnostic implementation lane; independent external validation remains blocked |
| Predictive v1 parameter lock | `atomic_predictive_v1_parameter_manifest.json`, artifact `atomic_predictive_v1_parameter_lock_gate` | locks constants, calibrated quantum-defect parameter policy, forbidden holdout/external leakage fields, and missing future CI/UET correction parameters for the selected v1 lane |
| Predictive v1 threshold gate | `atomic_predictive_v1_threshold_manifest.json`, artifact `atomic_predictive_v1_threshold_gate` | declares diagnostic level/wavelength thresholds for the selected v1 lane and records validation-reclassification requirements; 3/3 current diagnostics pass, but 0 thresholds are validation-ready and 4 reclassification blockers remain |
| Predictive v1 fixed-correction operator | `atomic_predictive_v1_fixed_correction_operator_manifest.json`, artifact `atomic_predictive_v1_fixed_correction_operator_gate` | defines the required `delta_uet_or_ci` operator contract, allowed CI/UET operator classes, inputs/outputs/units, parameter-lock rule, holdout exclusion rule, and current implementation blocker |
| Predictive v1 operator candidate resolution | artifact `atomic_predictive_v1_operator_candidate_resolution_gate` | resolves current standard, heuristic, empirical, legacy, CI/correlated, and UET candidates against the `delta_uet_or_ci` contract |
| Predictive v1 operator build spec | `atomic_predictive_v1_operator_build_spec_manifest.json`, artifact `atomic_predictive_v1_operator_build_spec_gate` | defines implementation lanes, required I/O, acceptance gates, forbidden shortcuts, and minimum first-build artifacts for the missing correction operator |
| Predictive v1 operator residual rows | `Research_Atomic_Operator_V1.py`, `atomic_predictive_v1_operator_residual_rows.json`, artifact `atomic_predictive_v1_operator_residual_gate` | exports 3 same-source-family He I diagnostic residual rows in `zero-QD baseline + diagnostic quantum-defect delta` form with schema/no-leakage fields and baseline-vs-diagnostic improvement metrics; accepted `delta_uet_or_ci` operator count remains 0 |
| Predictive v1 operator acceptance harness | `atomic_predictive_v1_operator_acceptance_harness_manifest.json`, `Research_Atomic_Operator_V1.py`, `atomic_predictive_v1_operator_parameters.json`, `atomic_predictive_v1_operator_uncertainty_policy.json`, `atomic_predictive_v1_operator_residual_rows.json`, artifact `atomic_predictive_v1_operator_acceptance_harness_gate` | names the target module, entrypoint, required local artifacts, residual-row schema, and operator acceptance decision matrix for accepting a future runnable operator; target skeleton, parameter manifest, uncertainty policy, residual-row schema, and no-leakage checks pass, but 3 operator acceptance decisions remain blocking and no correction operator is accepted |
| Predictive v1 operator parameter preflight | `atomic_predictive_v1_operator_parameter_acceptance_preflight.json`, `atomic_predictive_v1_operator_parameters.json`, artifact `atomic_predictive_v1_operator_parameter_acceptance_preflight_gate` | defines accepted-parameter field, lock, class, uncertainty, and forbidden-source checks; current review-only parameter set count is 1 and preflight now passes |
| Predictive v1 parameter candidate promotion | `atomic_predictive_v1_operator_parameter_candidate_promotion.json`, `atomic_predictive_v1_operator_parameters.json`, artifact `atomic_predictive_v1_operator_parameter_candidate_promotion_gate` | reviews when a candidate parameter set is concrete enough to be promoted into `parameter_sets`; current candidate count is 1 and the candidate is now review-ready, though still unaccepted |
| Predictive v1 operator-class selection review | `atomic_predictive_v1_operator_class_selection_review.json`, artifact `atomic_predictive_v1_operator_class_selection_review_gate` | compares the allowed CI/correlated and explicit UET lanes against build-spec priority and current blocker state so the repo can recommend and then track the first explicit implementation-class choice for the candidate |
| Predictive v1 operator training/holdout split | `atomic_predictive_v1_operator_training_holdout_split.json`, artifact `atomic_predictive_v1_operator_training_holdout_split_gate` | freezes the selected diagnostic split: 5 calibration rows, 4 same-source-family holdout rows, 2 CHIANTI cross-check rows, 0 overlap rows, and holdout/cross-check parameter-use prohibition |
| Predictive v1 operator implementation provenance | `atomic_predictive_v1_operator_implementation_provenance.json`, `atomic_predictive_v1_operator_candidate_implementation_review.json`, artifact `atomic_predictive_v1_operator_implementation_provenance_gate` | narrows the accepted-operator blocker into 5 required provenance artifacts; the training/holdout split is present, and the remaining 4 blockers now distinguish parameter-set readiness from missing accepted operator plus a locked candidate module/emitter/uncertainty review state |
| Predictive v1 publication readiness | artifact `atomic_predictive_v1_publication_readiness_gate` | blocks publication claims until residual hygiene, baseline improvement, accepted operator, validation thresholds, and independent source lineage all pass |
| Predictive v1 diagnostic report | artifact `atomic_predictive_v1_diagnostic_report_gate` | collects the current selected-lane level and wavelength predictions, threshold checks, parameter-lock status, and lineage decision; ready as a diagnostic report but validation-blocked |
| Predictive model blueprint | artifact `atomic_predictive_model_blueprint_gate` | seven-step build plan for turning diagnostics into a predictive model; records selected lane, equation form, parameter lock, holdout protocol, comparator, uncertainty threshold, and source-lineage decision |
| Helium external holdout acquisition | artifact `helium_external_holdout_acquisition_gate` | identifies CHIANTI He I as a cross-check candidate with raw files and hashes captured; lineage decision marks it NIST-dependent and source-version reconciliation remains open |
| Helium external holdout residual cross-check | artifact `helium_external_holdout_residual_crosscheck_gate` | computes CHIANTI-vs-current holdout deltas for 2 raw-captured overlap rows; display-rounding policy declared, diagnostic only because CHIANTI is NIST-dependent and source-version reconciliation remains open |
| Helium external holdout source-version reconciliation | artifact `helium_external_holdout_source_version_reconciliation_gate` | classifies CHIANTI/current upper-energy deltas separately from wavelength display-rounding consistency; diagnostic source bookkeeping only |
| Helium external holdout lineage decision | artifact `helium_external_holdout_lineage_decision_gate` | classifies CHIANTI He I as `CROSSCHECK_ONLY_NOT_INDEPENDENT` because captured metadata records NIST ASD lineage; non-NIST source package remains required |
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
8. Load source-referenced He+, Li2+, and C VI rows, apply reduced-mass hydrogenic scaling, compute He+/Li2+ under provisional thresholds, record C VI as a higher-Z stress test, and emit a hydrogen-like domain-coverage gate.
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
22. Build a predictive-model specification gate that defines the required baseline-plus-correction form, parameter manifest, holdout protocol, uncertainty protocol, and domain lanes before implementation.
23. Build a first predictive implementation candidate gate that selects the narrowest current lane and records candidate-lane blockers before implementation.
24. Build a helium external-holdout acquisition gate that identifies external/cross-check source candidates and keeps raw-capture, hash, lineage, and threshold blockers machine-readable.
25. Build a helium external-holdout residual cross-check gate that computes CHIANTI-vs-current holdout deltas after raw capture without treating them as validation.
26. Build a helium external-holdout source-version reconciliation gate that classifies upper-energy source-version deltas separately from wavelength display-rounding consistency.
27. Build a predictive-v1 parameter-lock gate that reads the parameter manifest and records allowed calibration rows, forbidden holdout/external leakage fields, and missing future correction parameters.
28. Build a predictive-v1 threshold gate that reads the threshold manifest, compares current diagnostic residuals against declared thresholds, and keeps validation blocked until thresholds are reclassified with source uncertainty, accepted operator, independent source lineage, and preregistered validation-ready policy.
29. Build a helium external-holdout lineage decision gate that classifies CHIANTI use as cross-check-only or independent-validation-eligible before external residuals can affect claims.
30. Build a predictive-v1 fixed-correction operator gate that reads the operator manifest and keeps empirical quantum-defect diagnostics separate from acceptable CI/UET correction operators.
31. Build a predictive-v1 operator candidate resolution gate that classifies existing formulas/model lanes and missing acceptable operator paths against the `delta_uet_or_ci` contract.
32. Build a predictive-v1 operator build-spec gate that reads the build-spec manifest and verifies implementation lanes, required inputs/outputs, acceptance gates, forbidden shortcuts, and minimum artifacts before implementation work.
33. Build a predictive-v1 operator acceptance-harness gate that resolves the target module path, local artifact paths, residual-row schema, and operator-acceptance decision matrix needed before an operator can be accepted.
34. Build a predictive-v1 operator training/holdout split gate that verifies row separation before any operator provenance upgrade.
35. Build a predictive-v1 operator-class selection review gate that compares the allowed CI/correlated and explicit UET lanes against current build-spec and derivation blockers before any candidate class is explicitly chosen.
36. Build a predictive-v1 operator implementation-provenance gate that records the evidence required before residual rows can count as accepted `delta_uet_or_ci` output.
37. Build a predictive-v1 diagnostic report gate that collects the selected-lane predictions, parameter-lock state, threshold rows, operator-contract state, lineage decision, and validation blockers.
38. Build a predictive-model blueprint gate that turns the build path into auditable steps: domain lane, model equation, parameter lock, holdout protocol, baseline comparator, uncertainty threshold, and source lineage.
38. Write artifact with hashes, thresholds, metrics, formula bridge metadata, level-energy rows, selected ion rows, hydrogen-like domain-coverage rows, precision source/baseline gates, Dirac baseline gate, Lamb handoff gate, 21 cm source/Fermi gates, neutral helium source/gap/medium/component/ground-baseline/excited-target/hydrogenic-residual/fixed-screening/quantum-defect-prediction/holdout/wavelength-holdout gates, legacy code audit, UET operator readiness, comparator table, uncertainty readiness, residual uncertainty budget, fixed-parameter readiness, predictive-closure contract, predictive-model specification, first implementation candidate, external-holdout acquisition/cross-check/source-version-reconciliation gates, predictive-v1 parameter lock, predictive-v1 threshold gate, external-holdout lineage decision, predictive-v1 fixed-correction operator, predictive-v1 operator candidate resolution, predictive-v1 operator build spec, predictive-v1 operator residual rows, predictive-v1 operator acceptance harness, predictive-v1 operator training/holdout split, predictive-v1 operator implementation provenance, predictive-v1 diagnostic report, predictive-v1 publication readiness, predictive-model blueprint, and limitations.
33. Write `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `branch_claim_gate.json` so the hydrogen benchmark stays separate from broader atomic-theory claims.

## Assumptions

- Vacuum wavelengths are used for the primary metric.
- `R_H` is source-locked from CODATA; this verifier does not derive it.
- Local NIST rows may be rounded or curated. Hydrogen wavelength rows and helium holdout rows now include transcription-rounding bounds, but official/upstream source uncertainty and page-level transcription audit remain required before ppm-level public claims.
- Bohr/de Broglie/Rydberg formulas are inherited standard physics unless a separate UET derivation artifact proves otherwise.
- Hydrogen level-energy rows are rounded and source-referenced through the ionization-energy anchor until direct per-level ASD precision is captured.
- Hydrogen-like ion predictions use reduced-mass scaling for the selected He+ and Li2+ rows. The current domain-coverage gate records only `Z=2,3,6`; all current rows are 2 -> 1 Lyman-alpha style targets. Li III remains provisional because direct ASD row capture is still pending. C VI is recorded only as a higher-Z stress-test row until fine/QED policy is added.
- Precision spectroscopy rows support a source package plus nonrelativistic, leading Dirac, empirical Lamb-handoff 1S-2S residuals, 21 cm source bookkeeping, and Fermi-contact baseline only until QED/recoil/proton-radius/hyperfine models and uncertainty propagation are added.
- Neutral helium rows support source targets, photon-energy bookkeeping, term assignments, medium normalization, source component policy, ground-state baseline residual diagnostics, excited-state target preparation, zero-quantum-defect residual sizing, fixed-screening heuristic diagnostics, limited source-calibrated quantum-defect prediction diagnostics, same-source-family holdout diagnostics, and restricted wavelength-holdout diagnostics only until a correlated two-electron Hamiltonian/spectral model, independent holdout source family, official/source uncertainty capture, broader model-parameter uncertainty propagation, standard-air wavelength conversion policy for future holdout rows, resolved line-shape policy for precision use, and residual thresholds are added. Current helium holdout uncertainty fields are transcription-rounding bounds only, not official NIST measurement uncertainties; same-source holdouts use leave-one-out RMSE fallback model uncertainty when direct series scatter is unavailable.
- The fixed-screening helium baseline uses `Z_eff = 2 - 0.85` locked before evaluation. It is a heuristic comparator, not a CI/correlated model and not a UET atomic operator.
- The predictive closure contract is a claim-control artifact only. It does not make the current quantum-defect or hydrogenic gates first-principles predictions.
- The predictive-model specification is not an implementation. It requires a future model to use `standard_baseline + delta_uet_or_ci` with locked parameters, source-backed holdouts, named baseline comparators, uncertainty-aware thresholds, and domain-specific gates.
- The first predictive implementation candidate gate selects the helium quantum-defect same-source-family holdout lane because it has current level and wavelength holdout predictions. It remains diagnostic only until independent external holdouts, uncertainty-aware thresholds, and a CI/correlated or UET operator are added.
- The predictive-v1 parameter-lock gate records `3` inherited constants, `1` calibrated quantum-defect policy row, `4` forbidden leakage fields, and `1` missing future locked parameter. It has `0` policy failures, but it remains diagnostic because the CI/UET correction operator is still missing.
- The predictive-v1 threshold gate records `3` diagnostic thresholds and all `3` pass current same-source-family diagnostics, but `0` thresholds are validation-ready. It now records `4` machine-readable validation-reclassification blockers: official/source uncertainty capture, accepted fixed CI/UET correction operator, non-NIST independent source package, and preregistered validation-ready threshold revision.
- The predictive-v1 fixed-correction operator gate defines the `delta_uet_or_ci` contract and records `3` operator candidates. It accepts `0` as implemented; the empirical quantum-defect lane is explicitly diagnostic-only.
- The predictive-v1 operator candidate resolution gate records `7` candidate formulas/model lanes. It accepts `0` as `delta_uet_or_ci`, rejects `5` existing candidates as baseline/heuristic/empirical/smoke-test roles, and leaves `2` acceptable operator paths missing.
- The predictive-v1 operator build-spec gate records `2` implementation lanes with required inputs, outputs, acceptance gates, forbidden shortcuts, and first-build artifacts. It is implementation-ready as a spec, but `0` lanes are implemented.
- The predictive-v1 operator residual gate exports `3` same-source-family He I diagnostic rows with locked-parameter and no-fit flags; all `3` rows now populate `delta_energy_eV` against the zero-quantum-defect baseline and improve over that baseline (`avg abs residual ~0.01616 eV -> ~0.000956 eV`), but accepted `delta_uet_or_ci` operators remain `0`.
- The predictive-v1 operator acceptance-harness gate records the concrete target module, residual schema, and operator acceptance decision matrix for acceptance. It passes `5/5` schema/no-leakage checks after adding the target module skeleton, parameter manifest, uncertainty policy, and generated residual rows; it still does not accept a correction operator because `3/5` operator acceptance decisions remain blocking and the rows are diagnostic-only.
- The predictive-v1 operator parameter preflight gate records `5` field-level acceptance checks for future operator parameters. It now has `1` promoted review-only parameter set, so all `5/5` field/class/lock/forbidden-source checks pass; this still does not mean the operator is accepted, only that the parameter-set structure is now audit-ready.
- The predictive-v1 parameter candidate promotion gate sits one step before accepted `parameter_sets`. It now passes for the current candidate because the fixed CI/correlated class is selected, selected-class noncomputable placeholders are explicitly locked, and the review timestamp is recorded; this still does not create an accepted parameter set or an implemented operator.
- The predictive-v1 operator-class selection review gate now records that the current candidate explicitly selects the fixed CI/correlated lane because that lane is already priority-1 in the build spec and does not wait on a new UET derivation artifact. The gate still does not implement the operator or create a validation claim; it only narrows the next work to parameter rows and lock state.
- The predictive-v1 operator training/holdout split gate records `5` calibration rows, `4` same-source-family holdout rows, and `2` CHIANTI cross-check rows, with `0` overlap rows and a policy that holdout/cross-check rows cannot set accepted operator parameters.
- The predictive-v1 operator implementation-provenance gate records `5` required provenance evidence rows. `1/5` is present through the split manifest; `4/5` remain blocking, but all 4 now have candidate evidence paths/hashes and machine-readable blocker reasons for accepted code identity, non-empty locked parameters, accepted residual emitter, and operator uncertainty provenance.
- The predictive-v1 publication-readiness gate passes `2/5` checks for clean residual rows and baseline improvement, but blocks `3/5` publication checks because accepted correction operator, validation-ready thresholds, and independent non-NIST source lineage remain missing.
- The predictive-v1 diagnostic report records `3` selected-lane level predictions and `2` wavelength predictions, with `3/3` diagnostic thresholds passing. It remains validation-blocked by the missing fixed CI/UET correction operator, non-NIST source package, and validation-ready threshold policy.
- The predictive-model blueprint answers how a predictive atomic model should be built, but it is not the implementation. It records seven steps; source lineage is decided as cross-check-only, while parameter lock, holdout protocol, thresholding, and non-NIST external validation remain partial.
- The helium external-holdout acquisition gate identifies CHIANTI He I as a cross-check candidate, not as independent validation, because CHIANTI metadata records NIST ASD lineage for observed He I data. Raw files, hashes, and two overlap locators are captured; source-version reconciliation remains required and independent validation requires a non-NIST source package.
- The helium external-holdout residual cross-check gate computes CHIANTI-vs-current deltas for two overlap rows. The display-rounding policy records 2/2 wavelength rows as consistent and 2/2 upper-energy rows as requiring source-version review, so it remains diagnostic only.
- The helium external-holdout source-version reconciliation gate records 2/2 upper-energy rows as requiring source-version reconciliation and keeps them out of validation even though 2/2 wavelength rows pass display-rounding consistency.
- The helium external-holdout lineage decision gate classifies CHIANTI He I as `CROSSCHECK_ONLY_NOT_INDEPENDENT`; independent validation still requires a non-NIST source package.
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
- Hydrogen-like domain-coverage diagnostic language only; it maps represented `Z`, benchmark lanes, source status, and missing broad-validation requirements.
- Precision source-package readiness language for 1S-2S, Lamb shift, and 21 cm hyperfine targets, plus nonrelativistic, leading Dirac, empirical Lamb-handoff, 21 cm source-bookkeeping, and Fermi-contact diagnostic language.
- Neutral helium source-package readiness, photon-energy, term-assignment, medium-normalization, component-policy, ground-state baseline, excited-state target, hydrogenic residual, fixed-screening heuristic baseline, quantum-defect prediction, same-source-family holdout, and wavelength-holdout blocker language for future many-electron artifacts.
- Residual uncertainty-budget language for current precision, hyperfine, helium-ground, and helium-holdout diagnostics, without uncertainty-qualified validation.
- Predictive closure language that defines the minimum artifact requirements for future atomic-spectrum prediction claims.
- Predictive-model specification language that defines the model form and implementation blockers without claiming the model exists.
- First predictive implementation candidate language that identifies helium same-source-family holdouts as the current narrow next lane while keeping independent validation blocked.
- Predictive-v1 parameter-lock language that freezes the current diagnostic parameter policy and forbidden leakage fields without claiming a generative model exists.
- Predictive-v1 threshold language that freezes diagnostic thresholds for reruns and lists the `4` missing reclassification artifacts before any threshold can be treated as validation-ready.
- Predictive-model blueprint and v1 diagnostic-report language that defines the first practical build path and current same-source-family prediction report, while keeping validation blocked until parameter lock, fixed correction operator, uncertainty thresholds, and independent source lineage are closed.
- Helium external-holdout acquisition, residual cross-check, source-version-reconciliation, and lineage-decision language that narrows the independent-validation blocker to a non-NIST source package and source-version reconciliation.

## Excluded Cases

- First-principles UET derivation of `R_H`.
- Broad source-backed validation of hydrogen-like ions beyond the selected provisional He+/Li2+ rows and the C VI stress-test lane.
- Multi-transition or full hydrogen-like ion coverage; the current domain gate records `5/5` blocking coverage checks.
- Fine structure, Lamb shift, hyperfine structure.
- QED precision correction residual claims.
- Helium or many-electron atomic spectra.
- Full QED validation.

## Dependency Policy

- `0.6_Electroweak_Physics`, `0.17_Mass_Generation`, `0.21_Yang_Mills_Mass_Gap`, `0.23_Unity_Scale_Link`, and `0.0_Grand_Unification` may cite this topic only as a hydrogen Rydberg benchmark unless future artifacts extend the scope.
