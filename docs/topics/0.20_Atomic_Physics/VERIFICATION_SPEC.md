# Verification Spec

## Primary Command

```powershell
python docs/topics/0.20_Atomic_Physics/Code/03_Research/Research_Rydberg_Validation.py
```

## Inputs

| Input | Role | Required identity |
| :-- | :-- | :-- |
| `Data/03_Research/nist_hydrogen_spectrum.json` | NIST hydrogen line working copy plus transcription-rounding wavelength bounds | SHA256, source DOI/URL, uncertainty policy, and line-bound status recorded in artifact |
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
| `Data/03_Research/helium_quantum_defect_holdout_sources.json` | Same-source-family He I holdout rows plus transcription-rounding bounds | SHA256, uncertainty policy, prediction/skipped rows, and source locator status recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_parameter_manifest.json` | Predictive-v1 parameter and leakage policy for the selected helium candidate lane | SHA256, selected lane, calibrated parameter policy, forbidden leakage fields, and future locked-parameter blockers recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_threshold_manifest.json` | Predictive-v1 diagnostic threshold policy for the selected helium candidate lane | SHA256, threshold rows, diagnostic comparison status, validation-readiness status, and blocked claims recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_operator_build_spec_manifest.json` | Predictive-v1 build contract for the first acceptable correction operator | SHA256, lane IDs, required I/O counts, acceptance gates, forbidden shortcuts, and build-spec-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_fixed_ci_input_preflight.json` | Predictive-v1 fixed-CI lane input preflight | SHA256, required input rows, blocking input count, and review-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_fixed_ci_implementation_declaration.json` | Predictive-v1 fixed-CI implementation declaration | SHA256, declared model family, declared convergence policy, and review-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_operator_acceptance_harness_manifest.json` | Predictive-v1 concrete acceptance harness for a future runnable correction operator | SHA256, target module path, local artifact targets, residual schema fields, acceptance checks, and harness-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_candidate_execution_manifest.json` | Predictive-v1 runnable candidate-execution contract for the current operator skeleton | SHA256, target module contract, expected residual artifact, execution checks, and execution-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_kernel_interface_manifest.json` | Predictive-v1 kernel-interface contract for the current fixed-CI/correlated wrapper state | SHA256, target module kernel entrypoint, required kernel fields, missing-core component list, and kernel-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_basis_assembly_manifest.json` | Predictive-v1 contract for the first fixed-CI/correlated basis-assembly scaffold | SHA256, target module basis-contract entrypoint, required contract fields, required input list, and basis-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_hamiltonian_effective_operator_manifest.json` | Predictive-v1 contract for the second fixed-CI/correlated Hamiltonian/effective-operator scaffold | SHA256, target module evaluation-contract entrypoint, required contract fields, required input/output lists, and Hamiltonian-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_parameterized_correction_emission_manifest.json` | Predictive-v1 contract for the third fixed-CI/correlated correction-emission scaffold | SHA256, target module emission-contract entrypoint, required contract fields, required input/output lists, and emission-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_row_level_uncertainty_manifest.json` | Predictive-v1 contract for the fourth fixed-CI/correlated row-level uncertainty scaffold | SHA256, target module uncertainty-contract entrypoint, required contract fields, required input/output lists, linked uncertainty-policy ID, and uncertainty-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_operator_parameter_acceptance_preflight.json` | Predictive-v1 field-level accepted-parameter preflight checklist | SHA256, required parameter-set fields, required parameter fields, lock rules, allowed operator classes, forbidden source policy, blocker count, and preflight-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_operator_parameter_candidate_promotion.json` | Predictive-v1 parameter candidate promotion checklist | SHA256, candidate count, promotion requirement rows, blocking count, and promotion-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_operator_class_selection_review.json` | Predictive-v1 operator-class selection review for the current candidate | SHA256, selection-option rows, recommended option count, recommended first class, and selection-review-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_operator_candidate_implementation_review.json` | Predictive-v1 candidate implementation review record | SHA256, selected operator class, target module review, diagnostic emitter review, uncertainty review, and review-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_operator_training_holdout_split.json` | Predictive-v1 diagnostic row split for current operator lane | SHA256, source package hashes, calibration/holdout/external row counts, overlap count, forbidden parameter-source policy, and split-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_predictive_v1_operator_implementation_provenance.json` | Predictive-v1 implementation provenance checklist | SHA256, provenance evidence rows, evidence-path status, blocker count, and provenance-only claim boundary recorded in artifact |
| `Data/03_Research/external_holdouts/chianti_he_i/source_manifest.json` | CHIANTI He I raw-file capture manifest for external cross-check acquisition | SHA256, raw file hashes, overlap-row locators, source-lineage status, and acquisition-only claim boundary recorded in artifact |
| `Data/03_Research/atomic_formula_bridge_manifest.json` | Generated bridge manifest for Bohr/de Broglie/Rydberg inheritance and UET dependency roles | SHA256 recorded in artifact after generation |

## Metrics

- Per-line predicted vacuum wavelength in nm.
- Per-line wavelength error in ppm.
- Per-line transcription-bound wavelength uncertainty and residual-to-bound ratio.
- Average wavelength error in ppm.
- Maximum wavelength error in ppm.
- Fitted slope through origin for `1/lambda` vs. Rydberg geometric term.
- Slope error relative to CODATA `R_H`.
- Hydrogen Rydberg line transcription-bound row count, maximum absolute wavelength residual, and residual-to-source-uncertainty ratio extrema.
- Hydrogen level-energy benchmark count, average error, and maximum error.
- Count of formula-bridge dependency steps.
- Hydrogen-like reduced-mass benchmark line count, average error, and maximum error.
- Hydrogen-like extended stress-test line count and residuals.
- Hydrogen-like domain-coverage represented `Z` count/range, coverage-check count, blocking-check count, source-status counts, and same-transition flag.
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
- Neutral helium zero-quantum-defect baseline computed-level count, average and maximum binding residuals, and effective quantum-defect range.
- Neutral helium fixed-screening baseline computed-level count, fixed `Z_eff`, average and maximum binding residuals, and count of rows improved versus zero-QD.
- Neutral helium source-calibrated quantum-defect prediction count, skipped-level count, average residual, maximum residual, and series coverage.
- Neutral helium same-source-family holdout row count, unique holdout level count, prediction count, skipped count, average residual, maximum residual, source-uncertainty policy status, predicted levels with source uncertainty, maximum source excitation uncertainty, predicted levels with model uncertainty, and maximum predicted excitation model uncertainty.
- Neutral helium restricted wavelength-holdout prediction count, predicted-vacuum-line count, skipped-line count, skipped-air-line count, average and maximum wavelength residual in angstrom and ppm, source-uncertainty policy status, predicted lines with source uncertainty, maximum source wavelength uncertainty, predicted lines with propagated model uncertainty, and maximum predicted wavelength model uncertainty.
- Atomic prediction baseline-comparator row count, improvement-factor count, missing external/CI comparator count, and named comparator roles.
- Atomic uncertainty-readiness lane count, blocked propagation lane count, partial propagation lane count, and lane-wise source/model/threshold status.
- Atomic residual uncertainty-budget row count, computable source-uncertainty row count, source-uncertainty-missing row count, and residual-to-source-uncertainty ratio extrema.
- Atomic fixed-parameter model-readiness lane count, fixed/standard baseline count, fitted-not-fixed count, missing required model count, and lane-wise parameter policy.
- Atomic predictive-closure check count, open/partial check count, fail-open check count, and linked prediction/residual counts.
- Atomic predictive-model specification development-lane count, blocked-lane count, implementation-blocker count, and blocking implementation-blocker count.
- Atomic first predictive implementation candidate lane count, blocked-lane count, success-criterion count, blocking-criterion count, selected level holdout count, and selected wavelength holdout count.
- Atomic predictive-v1 parameter-lock constant count, calibrated-parameter count, forbidden leakage field count, missing future locked-parameter count, policy fail count, and policy partial count.
- Atomic predictive-v1 threshold count, diagnostic pass/fail count, validation-ready threshold count, validation-reclassification requirement/blocker count, current max level residual, current max wavelength residual, and current max wavelength ppm residual.
- Atomic predictive-v1 fixed-correction operator candidate count, accepted-operator count, missing-candidate count, diagnostic-only-candidate count, contract fail count, and contract blocking count.
- Atomic predictive-v1 operator-candidate resolution count, accepted delta count, rejected existing candidate count, missing acceptable operator path count, fixed-correction contract blocking count, and UET operator blocking requirement count.
- Atomic predictive-v1 operator-build-spec implementation-lane count, implementation-ready lane count, missing-lane count, accepted implemented lane count, required-input/output counts, acceptance-gate count, forbidden-shortcut count, minimum-artifact count, fixed-CI input-preflight required/blocking counts, spec fail count, and spec blocking count.
- Atomic predictive-v1 operator-acceptance-harness check count, pass count, blocking count, target-module-present flag, required-local-artifact present/missing counts, residual-schema field count, operator-acceptance decision/blocker count, and accepted-operator count.
- Atomic predictive-v1 candidate-execution check count, pass count, blocking count, expected/emitted residual-row counts, uncertainty-computable row count, and accepted-operator count.
- Atomic predictive-v1 kernel-interface check count, pass count, blocking count, reported missing-core component count, and accepted-operator count.
- Atomic predictive-v1 basis-assembly check count, pass count, blocking count, required/reported input counts, and contract status.
- Atomic predictive-v1 Hamiltonian/effective-operator check count, pass count, blocking count, required/reported input counts, required/reported output counts, and contract status.
- Atomic predictive-v1 parameterized-correction-emission check count, pass count, blocking count, required/reported input counts, required/reported output counts, and contract status.
- Atomic predictive-v1 row-level-uncertainty check count, pass count, blocking count, required/reported input counts, required/reported output counts, linked uncertainty-policy field count, and contract status.
- Atomic predictive-v1 operator-parameter-preflight parameter-set count, parameter count, required-check count, blocking count, missing field row counts, lock failure count, operator-class failure count, and forbidden-source policy failure count.
- Atomic predictive-v1 operator-parameter-candidate-promotion candidate count, promotion-ready count, blocking count, and candidate requirement rows.
- Atomic predictive-v1 operator-class-selection-review option count, recommended-option count, candidate-promotion blocking count, and UET operator blocking requirement count.
- Atomic predictive-v1 operator-training-holdout-split source-manifest count, calibration row count, holdout row count, external cross-check row count, split-overlap count, and policy-complete flag.
- Atomic predictive-v1 operator-implementation-provenance required-evidence count, ready count, blocking count, candidate-evidence blocker count, accepted-operator count, candidate-implementation-review presence flag, residual/uncertainty artifact presence flags, and linked acceptance-decision blocker count.
- Atomic predictive-v1 diagnostic-report level prediction count, wavelength prediction count, diagnostic pass/fail count, validation blocker count, independent-validation allowed flag, and blocked claim list.
- Atomic predictive-model blueprint step count, blocked-step count, partial-step count, selected v1 lane, and blocked claim list.
- Helium external-holdout acquisition candidate source count, raw file count, raw file hash count, overlap-line candidate count, blocked requirement count, selected candidate ID, and source-lineage decision status.
- Helium external-holdout residual cross-check row count, skipped row count, maximum wavelength delta in A/ppm, maximum upper-energy delta in cm^-1, display-rounding policy status, wavelength pass count, upper-energy source-version review count, and blocked requirement count.
- Helium external-holdout source-version reconciliation row count, upper-energy source-version reconciliation-required count, wavelength display-rounding-consistent count, maximum upper-energy delta, and maximum upper-energy delta-to-rounding-bound ratio.
- Helium external-holdout lineage decision, NIST-lineage raw-file count, cross-check-only overlap-row count, independent-validation allowed flag, and non-NIST source-required flag.

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
- hydrogen Rydberg line transcription-bound diagnostics, line residuals, source-bound basis, and diagnostic-only claim boundary
- atomic formula bridge path/hash and dependency roles
- hydrogen level-energy rows, source anchor, thresholds, residuals, and limitations
- hydrogen-like reduced-mass benchmark rows, source status, benchmark lanes, stress-test residuals, thresholds, and limitations
- hydrogen-like domain-coverage rows, represented `Z`, benchmark lanes, source-status counts, same-transition limitation, next required artifacts, and broad-validation blocker status
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
- neutral helium zero-quantum-defect hydrogenic residual rows, quantum-defect diagnostics, and correlation/CI blocker status
- neutral helium fixed-screening baseline rows, fixed-parameter policy, residual diagnostics, and heuristic-only claim boundary
- neutral helium quantum-defect leave-one-out prediction rows, skipped rows, residual diagnostics, and independent-holdout blocker status
- neutral helium same-source-family holdout rows, prediction/skipped rows, uncertainty policy, transcription-rounding source bounds, fitted-parameter or LOO-RMSE fallback model uncertainty, residual diagnostics, and independent-external-source blocker status
- neutral helium restricted wavelength-holdout rows, predicted-vacuum rows, skipped standard-air rows, uncertainty policy, wavelength source bounds, propagated fitted/fallback model uncertainty, wavelength residual diagnostics, and external-holdout/threshold blocker status
- legacy multi-electron code audit rows, script hashes, evidence exclusion status, and replacement artifact requirements
- UET atomic-operator readiness requirements, blocking dependency list, missing residual-lane status, and blocked UET-derived claim list
- atomic prediction baseline-comparator rows, blocked comparator lanes, and internal-only claim boundary
- atomic uncertainty-readiness lanes, propagation blockers, next required artifacts, and uncertainty-only claim boundary
- atomic residual uncertainty-budget rows, source-uncertainty bases, residual-to-source-uncertainty ratios, missing source-uncertainty row count, hydrogen/helium transcription-bound limitations where used, and diagnostic-only claim boundary
- atomic fixed-parameter model-readiness lanes, legacy smoke/demo script exclusion, missing required model lanes, next required artifacts, and model-readiness-only claim boundary
- atomic predictive-closure checks, promotion requirements, blocked claims, and machine-readable open/fail-open counts
- atomic predictive-model specification contract, development lanes, implementation blockers, minimum first implementation steps, and model-specification-only claim boundary
- atomic first predictive implementation candidate lanes, selected lane, success criteria, implementation blockers, selected holdout metrics, next required artifacts, and diagnostic-only claim boundary
- atomic predictive-v1 parameter manifest, policy checks, forbidden leakage fields, missing future locked parameters, and parameter-lock-only claim boundary
- atomic predictive-v1 threshold manifest, threshold rows, diagnostic pass/fail status, validation-readiness status, validation-reclassification blockers, blocked claims, and threshold-only claim boundary
- atomic predictive-v1 fixed-correction operator manifest, operator candidates, contract checks, pass conditions, blocked claims, and operator-contract-only claim boundary
- atomic predictive-v1 operator-candidate resolution rows, candidate classifications, accepted/rejected/missing path counts, blocked claims, next required artifacts, and resolution-only claim boundary
- atomic predictive-v1 fixed-CI input-preflight manifest, required input rows, current readiness rows, blocked claims, and review-only claim boundary
- atomic predictive-v1 fixed-CI implementation declaration manifest, declared model family, declared convergence policy, blocked claims, and review-only claim boundary
- atomic predictive-v1 operator-build-spec manifest, implementation lanes, required inputs/outputs, acceptance gates, forbidden shortcuts, minimum first-build artifacts, lane-specific fixed-CI input preflight where present, spec checks, and build-spec-only claim boundary
- atomic predictive-v1 operator-acceptance-harness manifest, target module path, required local artifacts, residual schema, acceptance checks, operator-acceptance decision matrix, forbidden acceptance states, next required artifacts, and harness-only claim boundary
- atomic predictive-v1 candidate-execution manifest, target module contract, expected residual artifact, execution checks, uncertainty-field completeness, diagnostic-only execution state, and execution-only claim boundary
- atomic predictive-v1 kernel-interface manifest, target module kernel contract, required kernel fields, required missing-core components, explicit kernel-missing status, and kernel-only claim boundary
- atomic predictive-v1 basis-assembly manifest, target module basis-contract entrypoint, required contract fields, required inputs, explicit contract-only assembly status, and basis-only claim boundary
- atomic predictive-v1 Hamiltonian/effective-operator manifest, target module evaluation-contract entrypoint, required contract fields, required inputs, required outputs, explicit contract-only evaluation status, and Hamiltonian-only claim boundary
- atomic predictive-v1 parameterized-correction-emission manifest, target module emission-contract entrypoint, required contract fields, required inputs, required outputs, explicit contract-only emission status, and emission-only claim boundary
- atomic predictive-v1 row-level-uncertainty manifest, target module uncertainty-contract entrypoint, required contract fields, required inputs, required outputs, explicit contract-only uncertainty status, linked uncertainty-policy ID, and uncertainty-only claim boundary
- atomic predictive-v1 operator-parameter-preflight manifest, required parameter-set fields, required parameter fields, lock-rule checks, allowed operator classes, forbidden source policy, accepted parameter-set blocker rows, and preflight-only claim boundary
- atomic predictive-v1 operator-parameter-candidate-promotion manifest, promotion requirement rows, candidate summary rows, blocking reasons, and promotion-only claim boundary
- atomic predictive-v1 operator-class-selection-review manifest, selection-option rows, recommendation status, recommended first class, blocked claims, next required artifacts, and selection-review-only claim boundary
- atomic predictive-v1 operator-training-holdout-split manifest, source package hashes, calibration/holdout/external rows, overlap checks, forbidden parameter-source policy, and split-only claim boundary
- atomic predictive-v1 operator-candidate-implementation-review manifest, selected operator class, target-module review, diagnostic-emitter review, uncertainty review, blocked claims, and review-only claim boundary
- atomic predictive-v1 operator-implementation-provenance manifest, required evidence rows, evidence-path status, evidence hashes, supporting review-record status where present, blocker reasons, forbidden provenance shortcuts, blocker counts, next required artifacts, and provenance-only claim boundary
- atomic predictive-v1 diagnostic report rows, implementation state, validation blockers, blocked claims, and diagnostic-report-only claim boundary
- atomic predictive-model blueprint steps, first v1 lane, parameter-lock/source-lineage decisions, blocked claims, next required artifacts, and blueprint-only claim boundary
- helium external-holdout acquisition candidates, raw-file captures, SHA256 hashes, overlap lines, source-lineage decision/source-version blockers, and acquisition-only claim boundary
- helium external-holdout residual cross-check rows, wavelength/energy deltas, display-rounding policy, source-lineage decision/source-version blockers, and diagnostic-only claim boundary
- helium external-holdout source-version reconciliation rows, upper-energy delta-to-rounding-bound ratios, wavelength display-rounding status, blocked uses, next required artifacts, and reconciliation-only claim boundary
- helium external-holdout lineage decision checks, allowed/blocked uses, independent-validation flag, non-NIST-source-required flag, and lineage-decision-only claim boundary
- thresholds, metrics, per-line residuals, and limitations
- machine-readable `atomic_claim_scope_gate.controller_status`

## Interpretation

A PASS supports only a Claim Class C internal hydrogen-spectrum benchmark using the standard Rydberg relation. The formula bridge manifest supports only claim-boundary language about inherited Bohr/de Broglie/Rydberg formulas and dependency roles. The level-energy gate supports only rounded hydrogen n-level benchmark language. The hydrogen-like gate supports only provisional selected He+/Li2+ reduced-mass benchmark language; C VI is a higher-Z stress-test lane and does not count as broad ion validation. The hydrogen-like domain-coverage gate is diagnostic only and currently blocks broad validation with `5/5` open coverage checks. The precision spectroscopy and neutral-helium/many-electron gates are source-package only; the 1S-2S baseline gates are nonrelativistic, leading Dirac, and empirical Lamb-handoff residual diagnostics, while the 21 cm gates are source/wavelength bookkeeping and leading Fermi-contact residual diagnostics. Neutral helium photon energies, term assignments, wavelength-medium normalization, component policy, ground-state baseline residuals, external correlated-reference comparison, excited-state target preparation, zero-quantum-defect residual sizing, fixed-screening heuristic residual sizing, source-calibrated quantum-defect leave-one-out prediction, same-source-family holdout prediction, restricted wavelength-holdout prediction, legacy multi-electron code audit rows, UET atomic-operator readiness rows, internal comparator rows, uncertainty-readiness rows, residual uncertainty-budget rows, and fixed-parameter model-readiness rows are diagnostics only; correlated spectral residual modeling remains blocked. The predictive-closure gate is a claim-control contract only. The predictive-model specification gate defines how a future model must be implemented, but it is not the implementation itself. The first predictive implementation candidate gate selects the same-source-family helium quantum-defect holdout lane as the narrowest current diagnostic path, but it is not independent validation. The predictive-v1 parameter-lock gate records parameter and leakage policy only; it does not implement the missing CI/correlated or UET correction. The predictive-v1 threshold gate records diagnostic thresholds only; zero thresholds are validation-ready and four reclassification blockers remain machine-readable. The predictive-v1 fixed-correction operator gate defines the missing `delta_uet_or_ci` contract and records zero accepted operators; it is not an implementation. The predictive-v1 operator-candidate resolution gate explains why existing Bohr/Rydberg/Dirac/Lamb, fixed-screening, quantum-defect, and legacy lanes are not accepted correction operators, while CI/correlated and UET operator paths remain missing. The predictive-v1 fixed-CI input-preflight record now shows that source-backed helium anchors, excited targets, inherited constants, declared model family, and convergence-lock policy are already available to the first fixed-CI lane. The predictive-v1 fixed-CI implementation declaration records the intended correlated family plus convergence-lock policy. That closes the old undeclared-input blocker, but it does not create an accepted implementation. The predictive-v1 operator-build-spec gate defines the first implementation-ready I/O and acceptance contract, but it is not an implemented model. The predictive-v1 operator-residual gate exports 3 same-source-family diagnostic rows with schema/no-leakage fields, `uncertainty_computable`, and baseline-vs-diagnostic residual improvement metrics, but it is not an accepted correction operator and not independent validation. The predictive-v1 operator-acceptance-harness gate now finds the target module skeleton, entrypoint, parameter manifest, residual rows, and uncertainty policy with 5/5 schema/no-leakage checks passing against a 16-field row schema; its decision matrix still has 3/5 blocking decisions, so accepted correction operators remain zero. The predictive-v1 candidate-execution gate proves that the current target module runs through the verifier, writes the residual artifact, matches the expected same-source-family holdout row count, and fills row-level uncertainty state while still staying diagnostic-only. The predictive-v1 kernel-interface gate then makes the remaining kernel gap explicit: basis assembly, Hamiltonian or effective-operator evaluation, accepted `delta_uet_or_ci` emission, and row-level uncertainty from the accepted operator are all still missing, even though the wrapper and exporter are ready. The predictive-v1 basis-assembly gate narrows the first of those kernel gaps into a contract-only scaffold: it passes 5/5 checks, records the declared basis family, convergence policy, and all five required inputs, and still states `CONTRACT_ONLY_IMPLEMENTATION_MISSING`. That means basis expectations are now auditable, not implemented. The predictive-v1 Hamiltonian/effective-operator gate narrows the second kernel gap the same way: it passes 5/5 checks, records the basis dependency, selected effective-operator identity, all five required inputs, and all three required outputs, and still states `CONTRACT_ONLY_IMPLEMENTATION_MISSING`. That means evaluation expectations are now auditable, not implemented. The predictive-v1 parameterized-correction-emission gate narrows the third kernel gap the same way: it passes 5/5 checks, records the upstream evaluation dependency, emitted operator target `delta_uet_or_ci`, all five required inputs, and all three required outputs, and still states `CONTRACT_ONLY_IMPLEMENTATION_MISSING`. The predictive-v1 row-level-uncertainty gate narrows the fourth kernel gap the same way: it passes 5/5 checks, records the upstream emission dependency, linked uncertainty-policy ID, all five required inputs, and all three required outputs, and still states `CONTRACT_ONLY_IMPLEMENTATION_MISSING` while validation-ready thresholds remain disallowed. That means correction-emission and uncertainty-provenance expectations are now auditable, not implemented. The predictive-v1 operator-parameter preflight gate is now ready with one promoted review-only parameter set, and the parameter-candidate-promotion gate remains ready for the preserved candidate trail. That still does not create an accepted correction operator. The predictive-v1 operator-class selection review gate records the explicit fixed CI/correlated class choice and routes the next work toward accepted-operator implementation rather than candidate cleanup. The predictive-v1 operator-candidate-implementation-review record locks the current candidate module identity, diagnostic residual emitter, and diagnostic uncertainty lane for review only; it is not accepted operator provenance. The predictive-v1 operator-training-holdout-split gate records row separation for the current diagnostic lane only. The predictive-v1 operator-implementation-provenance gate now has 1/5 evidence rows present through the split manifest and 4/5 still blocking, but the blocker chain is narrower: `PROV-02` stays at `BLOCKING_ACCEPTED_OPERATOR_MISSING_PARAMETER_SET_READY`, while `PROV-01/04/05` now explicitly say candidate identity, diagnostic rows, and diagnostic uncertainty are locked for review without satisfying accepted-operator provenance. The predictive-v1 diagnostic report records current same-source-family selected-lane predictions and validation blockers only; it is not independent validation. The predictive-v1 publication-readiness gate blocks publication claims with 3/5 blocking checks: accepted correction operator, validation-ready thresholds, and independent non-NIST source lineage remain missing. The predictive-model blueprint gate defines the build path for a future model and records the current blockers; it is not a predictive implementation. The helium external-holdout acquisition, residual cross-check, source-version-reconciliation, and lineage-decision gates identify candidate source work only; CHIANTI is a raw-captured cross-check candidate with computed deltas, but upper-energy rows still require source-version reconciliation and the lineage decision classifies it as `CROSSCHECK_ONLY_NOT_INDEPENDENT`. It does not derive `R_H` from UET first principles and does not validate broad hydrogen-like ion coverage, first-principles QED, recoil/proton-size corrections, hyperfine Hamiltonian closure, neutral helium spectral residuals, independent helium validation, many-electron atoms, or periodic-table spectra.
Topic-level source-evidence and branch-claim gates further limit this topic to hydrogen-benchmark usage unless dedicated atomic artifacts are added.
`atomic_claim_scope_gate.controller_status == WARN` is expected when the hydrogen benchmark, rounded level-energy benchmark, provisional selected ion benchmark, precision source package, nonrelativistic/Dirac/Lamb-handoff 1S-2S diagnostics, 21 cm source bookkeeping, and neutral helium source/ground/excited/hydrogenic-residual/fixed-screening/quantum-defect-prediction/same-source-holdout/wavelength-holdout package are present while Rydberg derivation, direct level-table precision, direct Li III ASD capture, broad hydrogen-like ion validation, first-principles QED/recoil/proton-size/hyperfine correction models, independent external helium holdouts, standard-air wavelength conversion policy for future holdout rows, correlated helium spectral residuals, and many-electron residual models remain open.
