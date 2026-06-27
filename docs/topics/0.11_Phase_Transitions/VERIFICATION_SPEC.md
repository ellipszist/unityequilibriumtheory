# Verification Spec

- Primary command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Critical_Exponents.py`
- Inputs:
  - `Data/03_Research/critical_exponents.json`
- Baseline:
  - 3D Ising / liquid-gas beta exponent values from the topic-local critical-exponent working copy.
- Reported metrics:
  - UET beta projection
  - experimental fluid beta benchmark
  - 3D Ising theoretical beta benchmark
  - relative beta error in percent
  - machine-readable `phase_transition_claim_scope_gate.controller_status`
- Fixed threshold:
  - beta relative error against the experimental fluid benchmark must be <= 5 percent
  - the script must write a machine-readable artifact under `Result/artifacts/`
- Artifact target:
  - Result/artifacts/0_11_phase_transitions_verification.json
  - Data/03_Research/source_evidence_intake_stub.json
  - Data/03_Research/source_evidence_readiness_matrix.json
  - Data/03_Research/branch_claim_gate.json
- Interpretation:
  - Treat output as an internal selected-exponent benchmark only.
  - A pass does not prove the full phase-transition theory, because `gamma`, `nu`, scaling relations, morphology, and material critical-point datasets are not yet primary gates.
  - Topic-level source-evidence and branch-claim gates further limit the topic to selected-benchmark and mechanism-diagnostic usage unless stronger provenance and derivation packages are added.
  - `phase_transition_claim_scope_gate.controller_status == WARN` is expected when the
    selected beta benchmark passes while source archives, full exponent/scaling gates, and
    renormalization-group closure remain open.
## Wave 5 Spatial-Coupling Dynamics Verifier

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupling_Scaling.py`
- Artifact target:
  - `Result/artifacts/0_11_spatial_coupling_scaling.json`
  - `Result/gl_spatial_coupling_scaling_stats.csv`
- Purpose:
  - Test the opt-in `spatial_coupled_v1` core operator against baseline TDGL and the historical local-additive UET lane.
  - Keep this separate from the selected beta projection in `critical_exponents.json`.
- Required gates:
  - `engine_alignment_gate.status == PASS`
  - `spatial_operator_gate.status == PASS`
  - `universality_shift_gate.status == PASS` before any dynamics-based universality-shift claim is allowed.
- Current Wave 5 result:
  - overall status `WARN`
  - `engine_alignment_gate == PASS`
  - `spatial_operator_gate == PASS`
  - `universality_shift_gate == BLOCKED`
  - beta estimates: baseline `0.4912`, legacy local UET `0.5050`, spatial-coupled candidate `0.5081`
- Interpretation:
  - The candidate fixes the implementation availability of spatial operators in core mode.
  - The current candidate does not move the dynamics away from mean-field behavior.
  - Public or README language must not claim RG closure, universality-class shift, or phase-transition solution from this artifact.

## Wave 6 Spatial-Coupling Coefficient Sensitivity

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupling_Sensitivity.py`
- Artifact target:
  - `Result/artifacts/0_11_spatial_coupling_sensitivity.json`
  - `Result/gl_spatial_coupling_sensitivity_stats.csv`
- Purpose:
  - Test whether changing only the spatial-coupled candidate coefficients can move the fitted beta exponent toward the 3D Ising benchmark.
  - Keep this as triage for the blocked `universality_shift_gate`, not as a replacement for the full Wave 5 scaling verifier.
- Required gates:
  - `coefficient_sensitivity_gate.status == PASS` before treating coefficient tuning as a plausible repair path.
  - `operator_form_revision_gate.status != BLOCKED` before rerunning stronger dynamics claims without an operator revision.
- Current Wave 6 result:
  - overall status `WARN`
  - `coefficient_sensitivity_gate == BLOCKED`
  - `operator_form_revision_gate == BLOCKED`
  - tested coefficient cases: `20`
  - best beta found: `0.4729`
  - beta range: `0.4729` to `0.5243`
  - near-3D-Ising cases: `0`
- Interpretation:
  - Coefficient-only tuning of the current spatial candidate remains mean-field-like.
  - The next useful repair path is a revised operator form, nonlocal/scale-dependent term, or correlation-length-aware estimator.

## Wave 7 Correlation-Length Estimator Diagnostic

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Correlation_Length_Diagnostics.py`
- Artifact target:
  - `Result/artifacts/0_11_correlation_length_diagnostics.json`
  - `Result/gl_correlation_length_diagnostics_stats.csv`
- Purpose:
  - Test whether the current synthetic temperature window exposes connected correlation-length growth alongside the order-parameter beta fit.
  - Separate beta-only curve fitting from a stronger critical-scaling or universality claim.
- Required gates:
  - `critical_window_gate.status == PASS`
  - `estimator_adequacy_gate.status == PASS`
  - `operator_separation_gate.status == PASS`
- Current Wave 7 result:
  - overall status `WARN`
  - `critical_window_gate == BLOCKED`
  - `estimator_adequacy_gate == BLOCKED`
  - `operator_separation_gate == BLOCKED`
  - spatial beta `0.5081`
  - spatial correlation-length proxy `nu_proxy ~= 0.0324`
  - spatial `xi_near/xi_far ~= 1.0668`
- Interpretation:
  - The current order-parameter beta fit remains mean-field-like and is not paired with critical correlation growth.
  - The next useful repair path is a finite-size/correlation-length-aware scaling design before any stronger universality claim.

## Wave 8 Finite-Size Scaling Readiness Diagnostic

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Finite_Size_Scaling_Diagnostics.py`
- Artifact target:
  - `Result/artifacts/0_11_finite_size_scaling_diagnostics.json`
  - `Result/gl_finite_size_scaling_diagnostics_stats.csv`
- Purpose:
  - Test whether multiple grid sizes show enough near-critical `xi/L`, Binder-style crossing behavior, and spatial-vs-baseline separation to justify a stronger finite-size scaling pass.
- Required gates:
  - `finite_size_coverage_gate.status == PASS`
  - `correlation_window_gate.status == PASS`
  - `binder_crossing_gate.status == PASS`
  - `operator_separation_gate.status == PASS`
- Current Wave 8 result:
  - overall status `WARN`
  - `finite_size_coverage_gate == PASS`
  - `binder_crossing_gate == PASS`
  - `correlation_window_gate == BLOCKED`
  - `operator_separation_gate == BLOCKED`
  - max spatial near-critical `xi/L == 0.0961`
  - max baseline near-critical `xi/L == 0.1045`
  - best Binder-style spread `0.0058`
- Interpretation:
  - The diagnostic has enough grid/temperature coverage to expose the blocker.
  - The current finite-size window keeps correlations too local and does not separate the spatial candidate from baseline.

## Wave 9 Critical-Window Relaxation Diagnostic

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Critical_Window_Relaxation_Diagnostics.py`
- Artifact target:
  - `Result/artifacts/0_11_critical_window_relaxation_diagnostics.json`
  - `Result/gl_critical_window_relaxation_diagnostics_stats.csv`
- Purpose:
  - Test whether moving closer to `Tc` and increasing relaxation steps can lift spatial `xi/L` without changing the operator form.
- Required gates:
  - `critical_window_extension_gate.status == PASS`
  - `relaxation_sensitivity_gate.status == PASS`
  - `operator_separation_gate.status == PASS`
- Current Wave 9 result:
  - overall status `WARN`
  - `critical_window_extension_gate == BLOCKED`
  - `relaxation_sensitivity_gate == BLOCKED`
  - `operator_separation_gate == BLOCKED`
  - max spatial `xi/L == 0.0737`
  - max baseline `xi/L == 0.0797`
  - nearest-T relaxation gain from `700` to `2800` steps: `-0.0024`
- Interpretation:
  - The current small-correlation blocker is not resolved by this closer-to-Tc/longer-run window.
  - The next useful repair path is operator-form or dynamics redesign that creates measurable connected correlation growth.

## Wave 10 Operator-Form Requirement Gate

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Operator_Form_Requirement_Gate.py`
- Artifact target:
  - `Result/artifacts/0_11_operator_form_requirement_gate.json`
- Purpose:
  - Aggregate Waves 5-9 into a machine-readable design gate before proposing any `spatial_coupled_v2` operator.
  - Separate allowed design work from unsupported claim promotion.
- Required gates:
  - `prior_artifact_chain_gate.status == PASS`
  - `core_engine_alignment_gate.status == PASS`
  - `coefficient_only_path_gate.status == PASS` or documented replacement by a revised operator path
  - `finite_size_signal_gate.status == PASS`
  - `critical_window_path_gate.status == PASS`
  - `operator_form_requirement_gate.status == PASS` before describing a new operator as claim-bearing.
- Current Wave 10 result:
  - overall status `WARN`
  - `prior_artifact_chain_gate == PASS`
  - `core_engine_alignment_gate == PASS`
  - `coefficient_only_path_gate == BLOCKED`
  - `finite_size_signal_gate == BLOCKED`
  - `critical_window_path_gate == BLOCKED`
  - `operator_form_requirement_gate == BLOCKED`
- Interpretation:
  - The next useful work is operator-form redesign, not coefficient-only tuning or simply longer runs.
  - A future candidate must remain opt-in, use core engine paths, and demonstrate connected-correlation growth plus baseline separation before any dynamics claim is upgraded.

## Wave 11 Spatial-Coupled V2 Diagnostic

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupled_V2_Diagnostic.py`
- Artifact target:
  - `Result/artifacts/0_11_spatial_coupled_v2_diagnostic.json`
  - `Result/gl_spatial_coupled_v2_diagnostic_stats.csv`
- Purpose:
  - Test the first opt-in `spatial_coupled_v2` core candidate required by Wave 10.
  - Keep candidate availability, safety, stability, correlation response, and operator separation as separate gates.
- Required gates:
  - `v2_core_operator_gate.status == PASS`
  - `v2_spatial_safety_gate.status == PASS`
  - `v2_stability_gate.status == PASS`
  - `v2_correlation_response_gate.status == PASS`
  - `v2_operator_separation_gate.status == PASS`
- Current Wave 11 result:
  - overall status `WARN`
  - `v2_core_operator_gate == PASS`
  - `v2_spatial_safety_gate == PASS`
  - `v2_stability_gate == PASS`
  - `v2_correlation_response_gate == BLOCKED`
  - `v2_operator_separation_gate == BLOCKED`
  - max `xi/L`: baseline `0.0798`, v1 `0.0813`, v2 `0.0733`
  - v2 minus baseline `xi/L`: `-0.0065`
- Interpretation:
  - The first v2 candidate satisfies the code-surface and safety requirements but does not yet create connected-correlation growth or lane separation.
  - The next useful repair path is another operator-form revision or stronger derivation of the nonlocal/conserved dynamics, not claim promotion.

## Wave 12 Spatial-Coupled V2 Component Ablation

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Spatial_Coupled_V2_Component_Ablation.py`
- Artifact target:
  - `Result/artifacts/0_11_spatial_coupled_v2_component_ablation.json`
  - `Result/gl_spatial_coupled_v2_component_ablation_stats.csv`
- Purpose:
  - Separate `spatial_coupled_v2` into information-only, game-only, full, short-memory, and long-memory profiles.
  - Determine whether any existing v2 component is a plausible correlation-growth repair direction before designing another operator form.
- Required gates:
  - `ablation_coverage_gate.status == PASS`
  - `force_lane_activity_gate.status == PASS`
  - `component_improvement_gate.status == PASS` before treating any v2 component profile as a plausible repair path.
  - `memory_length_response_gate.status == PASS` before treating memory-length changes as a plausible repair path.
- Current Wave 12 result:
  - overall status `WARN`
  - `ablation_coverage_gate == PASS`
  - `force_lane_activity_gate == PASS`
  - `component_improvement_gate == BLOCKED`
  - `memory_length_response_gate == BLOCKED`
  - baseline max `xi/L == 0.0801`
  - best profile: `v2_memory_long`, improvement over baseline `-0.0038`
- Interpretation:
  - The tested v2 components are correctly isolated and stable, but none improves correlation length over baseline.
  - The next useful repair path is a different operator structure or derivation, not recombining or length-tuning the current v2 components.

## Wave 13 Model C Conserved-Order Diagnostic

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Model_C_Conserved_Order_Diagnostic.py`
- Artifact target:
  - `Result/artifacts/0_11_model_c_conserved_order_diagnostic.json`
  - `Result/gl_model_c_conserved_order_diagnostic_stats.csv`
- Purpose:
  - Test Model C / Cahn-Hilliard conserved order-parameter dynamics as a different operator family after v2 component ablation blocked the current spatial-coupled terms.
  - Use the topic `Engine_Phase.py` Cahn-Hilliard engine rather than a hidden standalone accepted-equation lane.
- Required gates:
  - `model_c_engine_alignment_gate.status == PASS`
  - `mass_conservation_gate.status == PASS`
  - `domain_growth_gate.status == PASS`
  - `operator_distinction_gate.status == PASS`
  - `claim_boundary_gate.status == WARN` until finite-size/exponent gates and core formula integration exist.
- Current Wave 13 result:
  - overall status `PASS` for mechanism triage
  - `model_c_engine_alignment_gate == PASS`
  - `mass_conservation_gate == PASS`
  - `domain_growth_gate == PASS`
  - `operator_distinction_gate == PASS`
  - `claim_boundary_gate == WARN`
  - Model C max mass drift `~2.1e-16`
  - Model C median `xi` growth ratio `30.49`; baseline comparison `24.68`
  - Model C minus baseline median `xi` growth ratio `5.81`
- Interpretation:
  - Model C is now the strongest mechanism-level repair direction found after v2 ablation.
  - This does not validate a universality-class shift; next work needs opt-in core integration and finite-size/exponent gates.

## Wave 14 Conserved-Order Core Candidate

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Core_Candidate.py`
- Artifact target:
  - `Result/artifacts/0_11_conserved_order_core_candidate.json`
  - `Result/gl_conserved_order_core_candidate_stats.csv`
- Purpose:
  - Verify that the Model C repair direction can be exposed through `docs/core/uet_master_equation.py` as opt-in `operator_mode="conserved_order_v1"` without changing legacy defaults.
  - Separate core integration, mass conservation, and mechanism response gates.
- Required gates:
  - `core_conserved_alignment_gate.status == PASS`
  - `legacy_compatibility_gate.status == PASS`
  - `conserved_mass_gate.status == PASS`
  - `core_mechanism_response_gate.status == PASS` before treating the explicit core path as a mechanism repair.
  - `claim_boundary_gate.status == WARN` until finite-size/exponent gates and formula audit closure exist.
- Current Wave 14 result:
  - overall status `WARN`
  - `core_conserved_alignment_gate == PASS`
  - `legacy_compatibility_gate == PASS`
  - `conserved_mass_gate == PASS`
  - `wave13_bridge_gate == PASS`
  - `core_mechanism_response_gate == BLOCKED`
  - `claim_boundary_gate == WARN`
  - core conserved max mass drift `~1.0e-17`; legacy core max mass drift `0.0149`
  - core conserved median `xi` growth ratio `0.87`; legacy core comparison `1.47`
- Interpretation:
  - Core exposure and conservation are now available as an opt-in candidate.
  - The explicit finite-difference core path does not yet reproduce the Wave 13 Cahn-Hilliard mechanism response; the next useful work is mechanism tuning or spectral/semi-implicit core integration, not claim promotion.

## Wave 15 Conserved-Order Numerics-Gap Diagnostic

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Numerics_Gap.py`
- Artifact target:
  - `Result/artifacts/0_11_conserved_order_numerics_gap.json`
- Purpose:
  - Compare Wave 13 spectral Cahn-Hilliard settings and Wave 14 explicit core settings using the dimensionless stiffness proxy `dt * kappa * (pi / dx)^4`.
  - Decide whether the next core repair can be coefficient or mobility tuning, or whether it needs a spectral/semi-implicit conserved-order update.
- Required gates:
  - `artifact_chain_gate.status == PASS`
  - `mechanism_gap_gate.status == PASS`
  - `explicit_core_viability_gate.status == PASS` before treating the explicit core finite-difference path as a viable direct replacement.
  - `spectral_core_requirement_gate.status != BLOCKED` before proceeding with coefficient-only tuning.
- Current Wave 15 result:
  - overall status `WARN`
  - `artifact_chain_gate == PASS`
  - `mechanism_gap_gate == PASS`
  - `explicit_core_viability_gate == BLOCKED`
  - `spectral_core_requirement_gate == BLOCKED`
  - Wave 13 explicit stiffness proxy `32685`
  - Wave 14 explicit stiffness proxy `0.097`
  - Wave 13-to-Wave 14 stiffness ratio `335544`
- Interpretation:
  - The explicit core conserved-order path is not yet a viable direct replacement under Wave 13-like settings.
  - The next supported implementation path is a spectral or semi-implicit conserved-order core candidate, not mobility-only tuning or recombining the current spatial v2 components.

## Wave 16 Conserved-Order Spectral Core Candidate

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Core_Candidate.py`
- Artifact target:
  - `Result/artifacts/0_11_conserved_order_spectral_core_candidate.json`
  - `Result/gl_conserved_order_spectral_core_candidate_stats.csv`
- Purpose:
  - Verify that `operator_mode="conserved_order_spectral_v1"` is exposed through `docs/core/uet_master_equation.py` without changing legacy defaults.
  - Compare the opt-in core spectral lane against the existing topic spectral Cahn-Hilliard engine under Wave 13-like settings.
  - Confirm that the Wave 15 explicit-core stiffness blocker is repaired by a stable spectral/semi-implicit core path before rerunning scaling claims.
- Required gates:
  - `core_spectral_alignment_gate.status == PASS`
  - `legacy_compatibility_gate.status == PASS`
  - `spectral_mass_stability_gate.status == PASS`
  - `topic_engine_bridge_gate.status == PASS`
  - `mechanism_response_gate.status == PASS`
  - `wave15_repair_gate.status == PASS`
  - `claim_boundary_gate.status == WARN` until finite-size/exponent gates and formula audit closure exist.
- Current Wave 16 result:
  - overall status `PASS`
  - `core_spectral_alignment_gate == PASS`
  - `legacy_compatibility_gate == PASS`
  - `spectral_mass_stability_gate == PASS`
  - `topic_engine_bridge_gate == PASS`
  - `mechanism_response_gate == PASS`
  - `wave15_repair_gate == PASS`
  - `claim_boundary_gate == WARN`
  - core spectral max mass drift `4.86e-16`
  - max topic-engine field delta `2.89e-12`
  - core spectral median `xi` growth ratio `30.49`
  - explicit `conserved_order_v1` stable case count under Wave 13-like settings `0`
- Interpretation:
  - The core spectral candidate repairs the implementation bridge blocker identified in Wave 15.
  - The next useful work is a finite-size/exponent scaling verifier using the opt-in spectral core candidate; this result is not a universality, material, or RG-closure claim.

## Wave 17 Conserved-Order Spectral Finite-Size Scaling

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Scaling.py`
- Artifact target:
  - `Result/artifacts/0_11_conserved_order_spectral_scaling.json`
  - `Result/gl_conserved_order_spectral_scaling_stats.csv`
- Purpose:
  - Run a normalized 3D finite-size/exponent sweep using the opt-in `conserved_order_spectral_v1` core candidate.
  - Keep implementation stability separate from finite-size correlation-window and universality-exponent claims.
- Required gates:
  - `wave16_bridge_gate.status == PASS`
  - `finite_size_coverage_gate.status == PASS`
  - `spectral_stability_gate.status == PASS`
  - `correlation_window_gate.status == PASS` before treating `xi/L` as adequate for finite-size scaling claims.
  - `universality_exponent_gate.status == PASS` before claiming a 3D Ising-like exponent shift.
  - `claim_boundary_gate.status == WARN` until material and RG closure gates exist.
- Current Wave 17 result:
  - overall status `WARN`
  - `wave16_bridge_gate == PASS`
  - `finite_size_coverage_gate == PASS`
  - `spectral_stability_gate == PASS`
  - `binder_crossing_gate == PASS`
  - `correlation_window_gate == BLOCKED`
  - `universality_exponent_gate == BLOCKED`
  - `claim_boundary_gate == WARN`
  - max near-critical `xi/L` `0.145`
  - beta range `1.61` to `1.83`; median beta `1.77`
  - median beta fit `R^2` `0.912`
- Interpretation:
  - The spectral core candidate remains stable in this normalized 3D sweep, but the finite-size window is still too local for universality claims.
  - The next useful work is a better finite-size/equilibration/scaling-window design, not claim promotion.

## Wave 18 Conserved-Order Spectral Window Repair

- Candidate command:
  - `python docs/topics/0.11_Phase_Transitions/Code/03_Research/Research_Conserved_Order_Spectral_Window_Repair.py`
- Artifact target:
  - `Result/artifacts/0_11_conserved_order_spectral_window_repair.json`
  - `Result/gl_conserved_order_spectral_window_repair_stats.csv`
- Purpose:
  - Test whether longer relaxation or closer-to-Tc windows repair the Wave 17 `xi/L` blocker.
  - Test whether kappa sensitivity can lift `xi/L` while preserving order-parameter signal.
- Required gates:
  - `wave17_chain_gate.status == PASS`
  - `relaxation_window_repair_gate.status == PASS` before treating runtime/window-only changes as sufficient.
  - `kappa_window_sensitivity_gate.status == PASS` only records that kappa can lift `xi/L`; it is not enough without signal preservation.
  - `signal_preservation_gate.status == PASS` before treating a high-`xi/L` case as scaling evidence.
  - `claim_boundary_gate.status == WARN` until full finite-size/exponent, material, and RG gates exist.
- Current Wave 18 result:
  - overall status `WARN`
  - `wave17_chain_gate == PASS`
  - `relaxation_window_repair_gate == BLOCKED`
  - `kappa_window_sensitivity_gate == PASS`
  - `signal_preservation_gate == BLOCKED`
  - `claim_boundary_gate == WARN`
  - max relaxation/window-only `xi/L` `0.113`
  - max kappa-sweep `xi/L` `0.377`
  - best high-`xi/L` order parameter `0.000377`
  - viable high-`xi/L` plus preserved-signal case count `0`
- Interpretation:
  - Relaxation/window-only changes do not repair the finite-size blocker.
  - Kappa can increase `xi/L`, but only by producing a very low-amplitude order signal in this diagnostic; this should be treated as a smoothing tradeoff, not universality evidence.
