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
