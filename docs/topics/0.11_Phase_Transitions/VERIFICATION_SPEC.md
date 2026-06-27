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
