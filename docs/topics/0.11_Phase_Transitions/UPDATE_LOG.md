# Update Log: 0.11 Phase Transitions


## Wave: Structure-Factor Acceptance-Rule Preflight (Wave 27)

**What changed:**
- Added `Research_Structure_Factor_Acceptance_Rule_Gate.py` to convert the Wave 26 missing-rule blocker into a machine-readable preflight.
- Added artifact `Result/artifacts/0_11_structure_factor_acceptance_rule_gate.json`.
- Updated topic docs and the inbox alignment audit to move the controller from missing acceptance rule to failed absolute-length consistency and estimator reconciliation.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Structure_Factor_Acceptance_Rule_Gate.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Structure_Factor_Acceptance_Rule_Gate.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_structure_factor_larger_grid_probe_needs_acceptance_rule` into `structure_factor_acceptance_rule_defined_current_evidence_fails_consistency`.
- The artifact reports `candidate_rule_definition_gate == PASS` and `admissible_subset_gate == PASS` for candidate grids `L=12,16,20`.
- It also reports `domain_scale_exclusion_gate == BLOCKED`, `absolute_length_consistency_gate == BLOCKED`, and `estimator_reconciliation_gate == BLOCKED`.

**Next controlling blocker:**
- Repair structure-factor absolute-length consistency and reconcile structure-factor versus axis-threshold estimators, or source-back an external estimator benchmark, before rerunning exponent or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 27 defines a conservative preflight rule, but the current evidence fails it and does not support accepted critical length, exponent, universality, material, RG, or phase-transition-solution claims.

---



## Wave: Conserved-Order Spectral Structure-Factor L20 Probe (Wave 26)

**What changed:**
- Added `Research_Conserved_Order_Spectral_Structure_Factor_L20_Probe.py` to test the Wave 25 structure-factor estimator on an `L=20` larger grid.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_structure_factor_l20_probe.json` and CSV `Result/gl_conserved_order_spectral_structure_factor_l20_probe_stats.csv`.
- Updated topic docs and the inbox alignment audit to move the controller from larger-grid probing to a source-backed or derived structure-factor acceptance rule.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Structure_Factor_L20_Probe.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Structure_Factor_L20_Probe.py`
- `.\.venv\Scripts\python.exe docs/scripts/audit/audit_inbox_research_alignment.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_structure_factor_multigrid_domain_scale_saturated` into `spectral_core_structure_factor_larger_grid_probe_needs_acceptance_rule`.
- The artifact reports `larger_grid_probe_gate == PASS`, `l20_margin_gate == PASS`, and `l20_domain_scale_relief_gate == PASS`.
- It also reports `derived_acceptance_rule_gate == BLOCKED`: L20 median `xi/L` is `0.4347`, but prior L8 remains domain-scale, L20/L16 absolute `xi` ratio is `0.9599`, and the structure-factor/lower-axis estimator ratio is `2.6261`.

**Next controlling blocker:**
- Create a source-backed or derived structure-factor acceptance rule before rerunning exponent or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 26 records partial larger-grid relief, not an accepted critical correlation length, universality-class shift, material validation, RG closure, or phase-transition-solution claim.

---



## Wave: Conserved-Order Spectral Structure-Factor Multi-Grid Calibration (Wave 25)

**What changed:**
- Added `Research_Conserved_Order_Spectral_Structure_Factor_Multigrid_Calibration.py` to rerun the Wave 24 threshold-free estimator over `L=8,12,16` and both Wave 20 plus fresh seed sets.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_structure_factor_multigrid_calibration.json` and CSV `Result/gl_conserved_order_spectral_structure_factor_multigrid_calibration_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to move the controller from needing multi-grid calibration to domain-scale saturation under that calibration.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Structure_Factor_Multigrid_Calibration.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Structure_Factor_Multigrid_Calibration.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_l16_structure_factor_domain_scale_needs_multigrid_calibration` into `spectral_core_structure_factor_multigrid_domain_scale_saturated`.
- The artifact reports `wave24_chain_gate == PASS`, `inbox_chain_gate == PASS`, `engine_path_gate == PASS`, and `multigrid_coverage_gate == PASS`.
- It also reports `structure_factor_margin_replication_gate == PASS` but `domain_scale_calibration_gate == BLOCKED`: structure-factor margin passes `18/18` cases, while median `xi/L` is `0.9972` at `L=8`, `0.7166` at `L=12`, and `0.5661` at `L=16`.

**Next controlling blocker:**
- Calibrate the structure-factor estimator against larger grids, known/source-backed benchmarks, or a derived finite-size acceptance rule before rerunning exponent or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 25 records reproducible domain-scale saturation, not an accepted critical correlation length, universality-class shift, material validation, RG closure, or phase-transition-solution claim.

---


## Wave: Conserved-Order Spectral L16 Structure-Factor Estimator (Wave 24)

**What changed:**
- Added `Research_Conserved_Order_Spectral_L16_Structure_Factor_Estimator.py` to test a threshold-free Fourier-domain characteristic-length proxy on the same Wave 23 `L=16` fresh-seed fields.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_l16_structure_factor_estimator.json` and CSV `Result/gl_conserved_order_spectral_l16_structure_factor_estimator_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to move the controller from threshold sensitivity to structure-factor multi-grid calibration.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_L16_Structure_Factor_Estimator.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_L16_Structure_Factor_Estimator.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_l16_xi_gate_threshold_sensitive` into `spectral_core_l16_structure_factor_domain_scale_needs_multigrid_calibration`.
- The artifact reports `wave23_chain_gate == PASS`, `engine_path_gate == PASS`, `estimator_case_coverage_gate == PASS`, and `default_estimator_reproduction_gate == PASS`.
- It also reports `structure_factor_margin_gate == PASS` but `domain_scale_guard_gate == WARN`: the structure-factor RMS estimator passes `9/9` cases with min `xi/L = 0.5549`, but max `xi/L = 0.5799` is near the single-grid domain scale.

**Next controlling blocker:**
- Run multi-grid structure-factor calibration/replication, or calibrate the estimator against a source-backed benchmark, before rerunning finite-size, exponent, or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 24 records a threshold-free estimator candidate and a domain-scale calibration blocker; it does not support universality-class shift, material validation, RG closure, or phase-transition-solution claims.

---


## Wave: Conserved-Order Spectral L16 Estimator Sensitivity (Wave 23)

**What changed:**
- Added `Research_Conserved_Order_Spectral_L16_Estimator_Sensitivity.py` to test whether the Wave 22 `L=16` fresh-seed blocker depends on the axis-autocorrelation crossing threshold.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_l16_estimator_sensitivity.json` and CSV `Result/gl_conserved_order_spectral_l16_estimator_sensitivity_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to move the controller from relaxation-only insufficiency to estimator-threshold sensitivity.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_L16_Estimator_Sensitivity.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_L16_Estimator_Sensitivity.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_l16_relaxation_only_repair_blocked` into `spectral_core_l16_xi_gate_threshold_sensitive`.
- The artifact reports `wave22_chain_gate == PASS`, `engine_path_gate == PASS`, `estimator_case_coverage_gate == PASS`, and `default_estimator_reproduction_gate == PASS`.
- It also reports `threshold_sensitivity_gate == PASS`: the default `e^-1` threshold reproduces Wave 22 at `3/9` passes and min `xi/L = 0.1938`, while thresholds `0.30`, `0.25`, and `0.20` pass `9/9` cases without threshold saturation.

**Next controlling blocker:**
- Derive or calibrate the correlation estimator threshold, or replace it with a source-backed structure-factor/correlation estimator, before rerunning finite-size, exponent, or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 23 shows estimator-threshold sensitivity but does not accept a non-default threshold or support universality-class shift, material validation, RG closure, or phase-transition-solution claims.

---

## Wave: Conserved-Order Spectral L16 Relaxation Repair (Wave 22)

**What changed:**
- Added `Research_Conserved_Order_Spectral_L16_Relaxation_Repair.py` to test whether longer `L=16` relaxation repairs the Wave 21 fresh-seed margin blocker.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_l16_relaxation_repair.json` and CSV `Result/gl_conserved_order_spectral_l16_relaxation_repair_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to move the controller from generic finite-size replication to relaxation-only insufficiency.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_L16_Relaxation_Repair.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_L16_Relaxation_Repair.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_finite_size_replication_not_robust` into `spectral_core_l16_relaxation_only_repair_blocked`.
- The artifact reports `wave21_chain_gate == PASS`, `l16_case_coverage_gate == PASS`, and `order_signal_gate == PASS`.
- It also reports `relaxation_repair_gate == BLOCKED`: `4000`, `4800`, and `5600` step groups each pass only `1/3` fresh seeds; the longest group has min `xi/L = 0.1950` despite min order `0.1359`.

**Next controlling blocker:**
- Revise the estimator, finite-size window, or scaling design; do not treat longer single-grid relaxation as the next default repair path.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 22 blocks relaxation-only repair and does not support universality-class shift, material validation, RG closure, or phase-transition-solution claims.

---

## Wave: Conserved-Order Spectral Finite-Size Replication (Wave 21)

**What changed:**
- Added `Research_Conserved_Order_Spectral_Finite_Size_Replication.py` to test the Wave 20 seed-margin-passing window over `L=8,12,16` and two seed sets.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_finite_size_replication.json` and CSV `Result/gl_conserved_order_spectral_finite_size_replication_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to move the controller from single-grid seed-margin to finite-size/grid-seed replication.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Finite_Size_Replication.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Finite_Size_Replication.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_seed_margin_passes_single_grid_needs_finite_size_replication` into `spectral_core_finite_size_replication_not_robust`.
- The artifact reports `wave20_chain_gate == PASS` and `finite_size_coverage_gate == PASS`.
- It also reports `grid_replication_gate == BLOCKED` and `seed_set_generalization_gate == BLOCKED`: `L=8` and `L=12` pass across tested seeds, but `L=16` passes only `4/6` cases and the fresh seed set passes only `1/3` with minimum `xi/L = 0.1944`.

**Next controlling blocker:**
- Revise the finite-size/window scaling design or estimator so the `L=16` fresh-seed margin is robust before rerunning exponent or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 21 blocks finite-size replication and does not support universality-class shift, material validation, RG closure, or phase-transition-solution claims.

---

## Wave: Conserved-Order Spectral Seed-Margin Repair (Wave 20)

**What changed:**
- Added `Research_Conserved_Order_Spectral_Seed_Margin.py` to test whether the Wave 19 spinodal target becomes seed-robust with longer relaxation.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_seed_margin.json` and CSV `Result/gl_conserved_order_spectral_seed_margin_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to move the controller from seed-margin repair to finite-size replication.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Seed_Margin.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Seed_Margin.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_spinodal_window_seed_margin_not_robust` into `spectral_core_seed_margin_passes_single_grid_needs_finite_size_replication`.
- The artifact reports `wave19_chain_gate == PASS`, `seed_group_coverage_gate == PASS`, `seed_margin_repair_gate == PASS`, and `relaxation_margin_gate == PASS`.
- It also reports `finite_size_replication_gate == BLOCKED`: the `L=16`, `T=0.900`, `kappa=0.100`, `4000`-step target passes `4/4` seeds with min `xi/L = 0.2004`, but no multi-grid replication has been run.

**Next controlling blocker:**
- Replicate the seed-margin-passing spinodal window across multiple grid sizes and only then rerun exponent or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 20 repairs the single-grid seed-margin blocker, but it does not support universality-class shift, material validation, RG closure, or phase-transition-solution claims.

---

## Wave: Conserved-Order Spectral Spinodal Window (Wave 19)

**What changed:**
- Added `Research_Conserved_Order_Spectral_Spinodal_Window.py` to test a targeted positive spinodal-margin window after the Wave 18 low-signal smoothing blocker.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_spinodal_window.json` and CSV `Result/gl_conserved_order_spectral_spinodal_window_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to record the narrower seed-margin blocker.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Spinodal_Window.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Spinodal_Window.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_xi_window_only_via_low_signal_smoothing` into `spectral_core_spinodal_window_seed_margin_not_robust`.
- The artifact reports `wave18_chain_gate == PASS`, `spinodal_access_gate == PASS`, and `order_signal_window_gate == PASS`.
- It also reports `seed_margin_gate == BLOCKED`: the best viable case reaches `xi/L = 0.204` with order `0.0126`, but the target replicate pass fraction is `0.25` and median replicate `xi/L` is `0.1965`.

**Next controlling blocker:**
- Replicate the spinodal window across seeds and grid sizes, or adjust the estimator/window so the order-preserving `xi/L` margin is robust before rerunning exponent or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 19 finds a candidate order-preserving window, but it does not support universality-class shift, material validation, RG closure, or phase-transition-solution claims.

---

## Wave: Conserved-Order Spectral Window Repair (Wave 18)

**What changed:**
- Added `Research_Conserved_Order_Spectral_Window_Repair.py` to test relaxation/window-only repairs and kappa sensitivity for the Wave 17 finite-size blocker.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_window_repair.json` and CSV `Result/gl_conserved_order_spectral_window_repair_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to separate high `xi/L` smoothing from preserved-signal scaling evidence.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Window_Repair.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Window_Repair.py`

**Which blocker narrowed:**
- Narrowed `spectral_core_finite_size_window_not_established` into `spectral_core_xi_window_only_via_low_signal_smoothing`.
- The artifact reports `wave17_chain_gate == PASS` and `kappa_window_sensitivity_gate == PASS`.
- It also reports `relaxation_window_repair_gate == BLOCKED` and `signal_preservation_gate == BLOCKED`: relaxation/window-only max `xi/L` is `0.113`, kappa max `xi/L` is `0.377`, but the best high-`xi/L` case has order parameter only `0.000377`.

**Next controlling blocker:**
- Design a finite-size/scaling window that preserves order signal while improving `xi/L`, or revise the scaling estimator/operator before rerunning universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 18 identifies a smoothing/signal tradeoff; it does not support universality-class shift, material validation, RG closure, or phase-transition-solution claims.

---

## Wave: Conserved-Order Spectral Scaling (Wave 17)

**What changed:**
- Added `Research_Conserved_Order_Spectral_Scaling.py` to run a normalized 3D finite-size/exponent sweep for `conserved_order_spectral_v1`.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_scaling.json` and CSV `Result/gl_conserved_order_spectral_scaling_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to separate Wave 16 core-bridge success from still-blocked finite-size/exponent claims.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Scaling.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Scaling.py`

**Which blocker narrowed:**
- Narrowed `conserved_order_spectral_core_candidate_scaling_open` into `spectral_core_finite_size_window_not_established`.
- The artifact reports `wave16_bridge_gate == PASS`, `finite_size_coverage_gate == PASS`, `spectral_stability_gate == PASS`, and `binder_crossing_gate == PASS`.
- It also reports `correlation_window_gate == BLOCKED` and `universality_exponent_gate == BLOCKED`: max near-critical `xi/L` is `0.145`, beta range is `1.61` to `1.83`, and median beta is `1.77`.

**Next controlling blocker:**
- Improve the finite-size/equilibration/scaling-window design for the spectral conserved-order candidate before rerunning exponent or universality gates.

**Current topic-level status after wave:**
- The spectral core candidate remains diagnostic-only. Wave 17 supports stability plus a narrower scaling blocker, not a universality-class shift, material validation, RG closure, or phase-transition-solution claim.

---

## Wave: Conserved-Order Spectral Core Candidate (Wave 16)

**What changed:**
- Added opt-in `conserved_order_spectral_v1` support in `docs/core/uet_master_equation.py` using a semi-implicit spectral conserved-order update that keeps the stiff `kappa*nabla^4` term in the denominator.
- Added unit checks for Wave 13-like mass conservation and uniform-field stationarity without changing legacy defaults.
- Added `Research_Conserved_Order_Spectral_Core_Candidate.py`, machine-readable artifact `Result/artifacts/0_11_conserved_order_spectral_core_candidate.json`, and CSV `Result/gl_conserved_order_spectral_core_candidate_stats.csv`.
- Updated topic docs and the Wave 5 alignment audit to separate implementation bridge success from still-open finite-size/exponent claims.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/core/uet_master_equation.py docs/core/uet_parameters.py docs/core/test/test_spatial_coupling.py docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Core_Candidate.py`
- `.\.venv\Scripts\python.exe docs/core/test/test_spatial_coupling.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Core_Candidate.py`

**Which blocker narrowed:**
- Narrowed `explicit_core_ch_scheme_stiffness_blocks_model_c_response` into `conserved_order_spectral_core_candidate_scaling_open`.
- The artifact reports `core_spectral_alignment_gate == PASS`, `legacy_compatibility_gate == PASS`, `spectral_mass_stability_gate == PASS`, `topic_engine_bridge_gate == PASS`, `mechanism_response_gate == PASS`, and `wave15_repair_gate == PASS`.
- The core spectral max mass drift is `4.86e-16`, max topic-engine field delta is `2.89e-12`, median `xi` growth ratio is `30.49`, and the explicit v1 lane has `0` stable cases under Wave 13-like settings.

**Next controlling blocker:**
- Build and run a finite-size/exponent scaling verifier using the opt-in spectral core candidate. Do not promote phase-transition, universality, material, or RG claims from this implementation bridge alone.

**Current topic-level status after wave:**
- The conserved-order spectral core candidate is implementation/mechanism-bridged but diagnostic-only. No universality-class shift, material validation, RG closure, or phase-transition-solution claim is supported.

---

## Wave: Conserved-Order Numerics Gap (Wave 15)

**What changed:**
- Added `Research_Conserved_Order_Numerics_Gap.py` to compare the Wave 13 spectral Cahn-Hilliard settings against the Wave 14 explicit core candidate using the stiffness proxy `dt * kappa * (pi / dx)^4`.
- Added machine-readable artifact `Result/artifacts/0_11_conserved_order_numerics_gap.json`.
- Updated topic docs and the Wave 5 alignment audit to make the next controller explicit: spectral or semi-implicit conserved-order core integration is required before coefficient-only tuning or finite-size claim reruns.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe -m py_compile docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Numerics_Gap.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Numerics_Gap.py`

**Which blocker narrowed:**
- Narrowed `conserved_order_core_candidate_needs_mechanism_tuning` into `explicit_core_ch_scheme_stiffness_blocks_model_c_response`.
- The artifact reports `artifact_chain_gate == PASS` and `mechanism_gap_gate == PASS`, but `explicit_core_viability_gate == BLOCKED` and `spectral_core_requirement_gate == BLOCKED`.
- The Wave 13 explicit stiffness proxy is `32685`, the Wave 14 explicit proxy is `0.097`, and the ratio is `335544`.

**Next controlling blocker:**
- Implement a spectral or semi-implicit conserved-order core candidate. Mobility-only tuning, recombining current spatial v2 components, or treating `conserved_order_v1` as mechanism-complete are blocked repair paths.

**Current topic-level status after wave:**
- The conserved-order path remains diagnostic-only. Wave 15 supports a narrower implementation requirement, not a dynamics claim, RG closure, universality-class shift, or phase-transition-solution claim.

---

## Wave: Conserved-Order Core Candidate (Wave 14)

**What changed:**
- Added opt-in `conserved_order_v1` support in `docs/core/uet_master_equation.py` using a Model C-style conserved flow `dC/dt = -M nabla^2(force)` where `force` is the negative functional gradient already assembled by the core path.
- Added `conserved_order_mobility` to `docs/core/uet_parameters.py` and unit checks for conserved mass, shape safety, uniform-field stationarity, and legacy compatibility.
- Added `Research_Conserved_Order_Core_Candidate.py`, machine-readable artifact `Result/artifacts/0_11_conserved_order_core_candidate.json`, and CSV `Result/gl_conserved_order_core_candidate_stats.csv`.
- Updated topic docs to separate opt-in core exposure and mass conservation from the still-blocked mechanism response.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/core/test/test_spatial_coupling.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Core_Candidate.py`

**Which blocker narrowed:**
- Narrowed `model_c_mechanism_promising_scaling_open` into `conserved_order_core_candidate_needs_mechanism_tuning`.
- The artifact reports `core_conserved_alignment_gate == PASS`, `legacy_compatibility_gate == PASS`, `conserved_mass_gate == PASS`, and `wave13_bridge_gate == PASS`.
- It also reports `core_mechanism_response_gate == BLOCKED`: core conserved median `xi` growth ratio is `0.87`, while the legacy core comparison is `1.47`.

**Next controlling blocker:**
- The Model C structure is now available as an opt-in core candidate and conserves mass, but the explicit finite-difference core implementation does not yet reproduce the stronger Wave 13 Cahn-Hilliard mechanism response. The next wave needs mechanism tuning, spectral/semi-implicit core integration, or a finite-size gate that explains the gap.

**Current topic-level status after wave:**
- The conserved-order core candidate remains diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Model C Conserved-Order Diagnostic (Wave 13)

**What changed:**
- Added `Research_Model_C_Conserved_Order_Diagnostic.py` to test Model C / Cahn-Hilliard conserved order-parameter dynamics as a different operator family after v2 component ablation failed to improve correlation growth.
- Added machine-readable artifact `Result/artifacts/0_11_model_c_conserved_order_diagnostic.json` and CSV `Result/gl_model_c_conserved_order_diagnostic_stats.csv`.
- Updated topic docs to treat Model C as a mechanism repair direction while keeping finite-size, exponent, material, and core-integration claims open.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Model_C_Conserved_Order_Diagnostic.py`

**Which blocker narrowed:**
- Narrowed `v2_components_remain_correlation_neutral_or_damping` into `model_c_mechanism_promising_scaling_open`.
- The artifact reports `model_c_engine_alignment_gate == PASS`, `mass_conservation_gate == PASS`, `domain_growth_gate == PASS`, and `operator_distinction_gate == PASS`, with `claim_boundary_gate == WARN`.
- Model C max mass drift is `~2.1e-16`; median Model C `xi` growth ratio is `30.49`; baseline comparison is `24.68`; Model C minus baseline is `5.81`.

**Next controlling blocker:**
- Model C is a plausible mechanism-level repair direction, but it still needs opt-in core integration and finite-size/exponent gates before any dynamics or universality claim can be upgraded.

**Current topic-level status after wave:**
- The spatial v1/v2 candidates remain diagnostic-only. Model C becomes the strongest current repair direction, but no RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Spatial-Coupled V2 Component Ablation (Wave 12)

**What changed:**
- Added `Research_Spatial_Coupled_V2_Component_Ablation.py` to separate the Wave 11 v2 operator into information-only, game-only, full, short-memory, and long-memory profiles.
- Added machine-readable artifact `Result/artifacts/0_11_spatial_coupled_v2_component_ablation.json` and CSV `Result/gl_spatial_coupled_v2_component_ablation_stats.csv`.
- Updated topic docs to distinguish successful force-lane isolation from failed correlation-growth repair.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupled_V2_Component_Ablation.py`

**Which blocker narrowed:**
- Narrowed `spatial_coupled_v2_correlation_not_yet_established` into `v2_components_remain_correlation_neutral_or_damping`.
- The artifact reports `ablation_coverage_gate == PASS` and `force_lane_activity_gate == PASS`, but `component_improvement_gate == BLOCKED` and `memory_length_response_gate == BLOCKED`.
- Baseline max `xi/L` is `0.0801`; all tested v2 profiles are lower. The best profile is `v2_memory_long` with improvement `-0.0038` over baseline.

**Next controlling blocker:**
- The current v2 component family is not a plausible correlation-growth repair under this synthetic window. The next wave needs a different operator structure or a stronger derivation, not recombination or memory-length tuning of the current v2 terms.

**Current topic-level status after wave:**
- The spatial candidates remain diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Spatial-Coupled V2 Candidate Diagnostic (Wave 11)

**What changed:**
- Added opt-in `spatial_coupled_v2` support in `docs/core/uet_master_equation.py` with screened nonlocal memory contrast and a conserved interface/game force.
- Added v2 candidate controls to `docs/core/uet_parameters.py` without changing `legacy_local` defaults or `spatial_coupled_v1` behavior.
- Added core unit checks for v2 zero/uniform gates, 1D/2D shape handling, conserved game-force sum, and explicit v2 dynamics shape preservation.
- Added `Research_Spatial_Coupled_V2_Diagnostic.py`, machine-readable artifact `Result/artifacts/0_11_spatial_coupled_v2_diagnostic.json`, and CSV `Result/gl_spatial_coupled_v2_diagnostic_stats.csv`.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/core/test/test_spatial_coupling.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupled_V2_Diagnostic.py`

**Which blocker narrowed:**
- Narrowed `operator_form_revision_required` into `spatial_coupled_v2_correlation_not_yet_established`.
- The artifact reports `v2_core_operator_gate == PASS`, `v2_spatial_safety_gate == PASS`, and `v2_stability_gate == PASS`.
- It also reports `v2_correlation_response_gate == BLOCKED` and `v2_operator_separation_gate == BLOCKED`; max `xi/L` is baseline `0.0798`, v1 `0.0813`, and v2 `0.0733`.

**Next controlling blocker:**
- The first v2 operator is structurally safer but still does not create measurable connected-correlation growth. The next wave needs another operator-form revision or a stronger derivation of the nonlocal/conserved dynamics before finite-size or universality claims can be rerun.

**Current topic-level status after wave:**
- The spatial candidates remain diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Operator-Form Requirement Gate (Wave 10)

**What changed:**
- Added `Research_Operator_Form_Requirement_Gate.py` to aggregate Waves 5-9 into a machine-readable design gate before any `spatial_coupled_v2` proposal is treated as claim-bearing.
- Added machine-readable artifact `Result/artifacts/0_11_operator_form_requirement_gate.json`.
- Updated topic docs to make `operator_form_revision_required` the current controller rather than coefficient tuning or longer runtime/window extension.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Operator_Form_Requirement_Gate.py`

**Which blocker narrowed:**
- Narrowed the post-Wave-9 blocker to `operator_form_revision_required`.
- The artifact reports `prior_artifact_chain_gate == PASS` and `core_engine_alignment_gate == PASS`, but `coefficient_only_path_gate == BLOCKED`, `finite_size_signal_gate == BLOCKED`, `critical_window_path_gate == BLOCKED`, and `operator_form_requirement_gate == BLOCKED`.
- The blocked paths show that coefficient-only tuning, finite-size/window adjustments, and longer critical-window relaxation are not sufficient repair paths for the current `spatial_coupled_v1` family.

**Next controlling blocker:**
- Design a new opt-in core-engine operator form with nonlocal, conserved, or scale-dependent dynamics, then rerun unit, formula, correlation-growth, operator-separation, and finite-size gates before any claim upgrade.

**Current topic-level status after wave:**
- The spatial candidate remains diagnostic-only. Wave 10 authorizes only operator-design work, not validation of new physics or universality-class claims.

---
## Wave: Critical-Window Relaxation Diagnostic (Wave 9)

**What changed:**
- Added `Research_Critical_Window_Relaxation_Diagnostics.py` to test closer-to-Tc temperatures and longer relaxation windows without changing the current spatial operator.
- Added machine-readable artifact `Result/artifacts/0_11_critical_window_relaxation_diagnostics.json` and CSV `Result/gl_critical_window_relaxation_diagnostics_stats.csv`.
- Updated topic docs to block the assumption that simply running closer to `Tc` or longer fixes the small-correlation blocker.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Critical_Window_Relaxation_Diagnostics.py`

**Which blocker narrowed:**
- Narrowed the next controller to `critical_window_extension_still_local`.
- The artifact reports `critical_window_extension_gate == BLOCKED`, `relaxation_sensitivity_gate == BLOCKED`, and `operator_separation_gate == BLOCKED`.
- Max spatial `xi/L` remains `0.0737`, max baseline `xi/L` is `0.0797`, and nearest-T relaxation gain from `700` to `2800` steps is `-0.0024`.

**Next controlling blocker:**
- Runtime/window extension alone is not enough. The next wave needs a dynamics/operator-form revision that creates measurable connected correlation growth and separates from baseline.

**Current topic-level status after wave:**
- The spatial candidate remains diagnostic-only. Finite-size scaling and universality-class claims remain blocked.

---
## Wave: Finite-Size Scaling Readiness Diagnostic (Wave 8)

**What changed:**
- Added `Research_Finite_Size_Scaling_Diagnostics.py` to compare baseline TDGL and the spatial candidate across grid sizes `8`, `12`, and `16`.
- Added machine-readable artifact `Result/artifacts/0_11_finite_size_scaling_diagnostics.json` and CSV `Result/gl_finite_size_scaling_diagnostics_stats.csv`.
- Updated topic docs to keep finite-size scaling claims blocked until xi/L and operator-separation gates pass.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Finite_Size_Scaling_Diagnostics.py`

**Which blocker narrowed:**
- Narrowed the next controller to `finite_size_scaling_window_not_established`.
- The artifact reports `finite_size_coverage_gate == PASS` and `binder_crossing_gate == PASS`, but `correlation_window_gate == BLOCKED` and `operator_separation_gate == BLOCKED`.
- Max near-critical `xi/L` remains small: spatial `0.0961`, baseline `0.1045`.

**Next controlling blocker:**
- Redesign the finite-size window and/or operator form so the spatial lane creates measurable near-critical correlation length and separates from the baseline.

**Current topic-level status after wave:**
- The spatial candidate remains diagnostic-only. Finite-size scaling and universality-class claims remain blocked.

---
## Wave: Correlation-Length Estimator Diagnostic (Wave 7)

**What changed:**
- Added `Research_Correlation_Length_Diagnostics.py` to compute order-parameter beta and a connected autocorrelation-length proxy from the same baseline, legacy, and spatial candidate lanes.
- Added machine-readable artifact `Result/artifacts/0_11_correlation_length_diagnostics.json` and CSV `Result/gl_correlation_length_diagnostics_stats.csv`.
- Updated topic docs to block beta-only universality promotion unless correlation-window and estimator gates also pass.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Correlation_Length_Diagnostics.py`

**Which blocker narrowed:**
- Narrowed the next controller to `critical_window_or_operator_form_not_resolved`.
- The artifact reports `critical_window_gate == BLOCKED`, `estimator_adequacy_gate == BLOCKED`, and `operator_separation_gate == BLOCKED`.
- Spatial beta remains `0.5081`, while spatial `nu_proxy` is only `0.0324` and `xi_near/xi_far` is only `1.0668`.

**Next controlling blocker:**
- Build finite-size/correlation-length-aware scaling and revise the operator form so the spatial lane separates from the baseline in both beta and correlation diagnostics.

**Current topic-level status after wave:**
- The spatial candidate remains diagnostic-only. The current synthetic window does not support RG closure, universality-class shift, or phase-transition-solution claims.

---
## Wave: Spatial-Coupling Coefficient Sensitivity (Wave 6)

**What changed:**
- Added `Research_Spatial_Coupling_Sensitivity.py` to test whether coefficient-only tuning of the current `spatial_coupled_v1` operator can move beta away from mean-field.
- Added machine-readable artifact `Result/artifacts/0_11_spatial_coupling_sensitivity.json` and CSV `Result/gl_spatial_coupling_sensitivity_stats.csv`.
- Updated topic docs to treat coefficient-only tuning as a blocked repair path rather than a likely route to a universality shift.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupling_Sensitivity.py`

**Which blocker narrowed:**
- Narrowed `universality_shift_gate` into `coefficient_only_spatial_operator_still_mean_field`.
- The sensitivity artifact tested 20 coefficient cases and found beta range `0.4729` to `0.5243`; best beta was `0.4729`, with zero cases near the 3D Ising reference under the declared tolerance.

**Next controlling blocker:**
- Coefficient tuning is not enough. The next wave needs a revised operator form, nonlocal/scale-dependent term, or correlation-length-aware estimator before rerunning stronger scaling claims.

**Current topic-level status after wave:**
- The spatial candidate remains diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Core GL Limit Verifier Stabilization (Wave 5 follow-up)

**What changed:**
- Made `verify_ginzburg_landau_limit()` deterministic and explicitly pure-GL: seeded RNG, disabled UET extras (`W_N`, exchange, viscosity, inertia), and used enough integration time for the local potential to relax toward the `C0` minimum.
- Did not change the core dynamics operator or promote the spatial-coupled candidate claim.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/core/uet_master_equation.py`
- `.\.venv\Scripts\python.exe docs/core/test/test_spatial_coupling.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Critical_Exponents.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupling_Scaling.py`

**Which blocker narrowed:**
- Narrowed the residual core self-test blocker: `Ginzburg-Landau limit` changed from `FAIL - Final V about 0.5212` to `PASS - Initial V=0.5242; Final V=0.0001`.
- The Wave 5 spatial artifact still records `engine_alignment_gate == PASS`, `spatial_operator_gate == PASS`, and `universality_shift_gate == BLOCKED`.

**Next controlling blocker:**
- `universality_shift_gate` remains the controlling topic blocker. Current beta estimates remain near mean-field: baseline `0.4912`, legacy local UET `0.5050`, spatial-coupled candidate `0.5081`.

**Current topic-level status after wave:**
- Core verifier hygiene improved, but the phase-transition dynamics claim remains diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Spatial-Coupling Candidate Gate (Wave 5)

**What changed:**
- Added an opt-in `spatial_coupled_v1` operator mode to the core master equation while preserving `legacy_local` as the default.
- Added candidate information coupling `0.5 beta C^2 I` and interface-sensitive game coupling through `|grad C|^2`.
- Added `Research_Spatial_Coupling_Scaling.py` to compare baseline TDGL, historical local UET, and the new spatial-coupled candidate.
- Added `docs/core/WAVE5_MASTER_EQUATION_ALIGNMENT_AUDIT.md` to map inbox claims to code behavior without treating inbox text as canonical proof.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/core/test/test_spatial_coupling.py`
- `.\.venv\Scripts\python.exe docs/core/uet_master_equation.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Critical_Exponents.py`
- `.\.venv\Scripts\python.exe docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupling_Scaling.py`

**Which blocker narrowed:**
- Narrowed `spatially_blind_engine_operator`: the core engine now exposes an opt-in spatial candidate and the artifact records `engine_alignment_gate == PASS` and `spatial_operator_gate == PASS`.

**Next controlling blocker:**
- `universality_shift_gate` remains `BLOCKED`. The Wave 5 artifact estimates beta near mean-field: baseline `0.4912`, legacy local UET `0.5050`, spatial-coupled candidate `0.5081`, versus 3D Ising reference `0.3265`.

**Current topic-level status after wave:**
- Spatial operator availability is hardened, but the candidate remains diagnostic-only. No RG closure, universality-class shift, or phase-transition-solution claim is supported.

---
## Wave: Synthetic GL V4 Benchmark (Scaling Analysis & Critical Exponents)

**What changed:**
- Opening Wave 4 to move beyond energy convergence into New Physics verification.
- Implemented `simulate_uet_scaling.py` using a 3D grid ($16 \times 16 \times 16$) to properly reflect 3D system topology.
- Converted static parameter $a$ to temperature-dependent $a(T) = a_0 \frac{T - T_c}{T_c}$.
- Injected strict Langevin thermal noise to the baseline TDGL to allow proper phase fluctuations near $T_c$.
- Extracted the Order Parameter Exponent ($\beta$) via Log-Log linear regression.

**Which verifier was run:**
- `uv run --with numpy --with matplotlib --with pandas --with scipy docs/topics/0.11_Phase_Transitions/Code/simulate_uet_scaling.py`

**Which blocker narrowed:**
- Evaluated the hypothesis that UET modifies the universality class ($\beta \to 0.33$).
- Result: Baseline yielded $\beta \approx 0.5188$. Full UET yielded $\beta \approx 0.4983$.

**Next controlling blocker:**
- The UET terms ($\Phi_N$ and $V_{game}$) in their current mathematical form do **not** break the system out of the Mean-Field universality class. The theoretical claim that UET shifts universality to 3D Ising is currently refuted by empirical simulation.
- Theoretical derivation must be revised: Is the game-shift term modifying the $C^4$ scaling, or is it merely shifting the effective temperature $T_c$?

**Current topic-level status after wave:**
- Critical Exponent hypothesis failed empirical validation. UET remains in the Mean-Field class.

---

## Wave: Synthetic GL V3 Benchmark (Statistical Validation)

**What changed:**
- Added `simulate_uet_gl_v3.py` to scale the diagnostic to 100 seeds.
- Froze hyperparameters (`a`, `b`, `kappa`, `Gamma`, `mu_G`, `eta_U`, `phi_noise`, `Gamma_N`) before execution.
- Added Paired Difference ($E_{UET} - E_{Baseline}$) and Win Rate calculation logic.

**Which verifier was run:**
- `uv run --with numpy --with matplotlib --with pandas --with scipy docs/topics/0.11_Phase_Transitions/Code/simulate_uet_gl_v3.py`

**Which blocker narrowed:**
- Addressed the small sample size (5 seeds) caveat from V2.
- The V3 result over 100 seeds shows UET wins 60% of the time, with a paired difference mean of -0.000511 ± 0.002225 J.
- Internally measured a small effect-size signal, though variance remains high.

**Next controlling blocker:**
- The effect size (mean paired difference) is modest. We need to analyze whether the UET components can be calibrated to a broader physical scope, or if the transition rules need scaling analysis (e.g., studying critical exponents at the transition boundary rather than just final energy depths).

**Current topic-level status after wave:**
- UET passes the first synthetic GL smoke benchmark: the Full UET lane achieves a lower mean final GL energy and beats the TDGL baseline in 60% of seeds. However, this is not yet a formal benchmark pass due to effect size bounds.

---

## Wave: Synthetic GL V2 Benchmark

**What changed:**
- Added `simulate_uet_gl_v2.py` as a diagnostic artifact.
- Fixed unit leakage in $\Phi_N$ by introducing rate coefficient $\Gamma_N$ ($m^3/(J\cdot s)$).
- Implemented full $\Omega_{UET}$ energy tracking instead of just GL free energy.
- Added ablation lanes (Baseline, PhiN, Vgame, UET) and multi-seed statistical validation (5 seeds).

**Which verifier was run:**
- `uv run --with numpy --with matplotlib --with pandas docs/topics/0.11_Phase_Transitions/Code/simulate_uet_gl_v2.py`

**Which blocker narrowed:**
- Removed unit error blocker and eliminated conflated evidence by tracking the full functional.

**Current topic-level status after wave:**
- Smoke Test Pass with caveats.
