# Wave 5 Master Equation Alignment Audit

**Status:** alignment audit for the Wave 5 spatial-coupling candidate. This file treats
`docs/core/00_inbox/` as intake evidence, not as canonical proof.

## Intake Evidence

- `docs/core/00_inbox/raw chat.md`: identifies the concern that the current math translates
  the UET space/information/game explanation into local additive terms.
- `docs/core/00_inbox/UET_Master_Equation_Analysis.md`: proposes multiplicative
  information coupling and gradient/interface-sensitive game coupling as candidate repairs.

## Controlling Blocker

`spatially_blind_engine_operator`

The legacy engine and historical 0.11 scaling scripts can add information/game terms without
forcing those terms to depend on spatial structure. That is enough to shift diagnostics, but it
does not by itself establish a universality-class change.

## Code Alignment Matrix

| Concern | Legacy behavior | Wave 5 candidate behavior | Current evidence boundary |
| :-- | :-- | :-- | :-- |
| Information coupling | `beta * C * I` in Omega; C dynamics source `-beta * I` | opt-in `0.5 * beta * C^2 * I`; C dynamics source `-beta * C * I` | heuristic bridge; unit closure still open |
| Game term | `V_game = beta_U * C^2` in Omega; no explicit legacy game force in `dynamics_step_complete` | opt-in `V_game = beta_U * |grad C|^2`; KPZ-style dynamics force from the same core helper | interface diagnostic only |
| Engine default | legacy local mode | unchanged unless `operator_mode="spatial_coupled_v1"` is selected | backward-compatible pilot |
| Phase-transition claim | selected beta JSON projection can pass | dynamics scaling must pass a separate gate | no RG/universality promotion yet |

## Wave 5 Artifact Result

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_spatial_coupling_scaling.json`

- `engine_alignment_gate`: `PASS`
- `spatial_operator_gate`: `PASS`
- `universality_shift_gate`: `BLOCKED`
- beta estimates: baseline `0.4912`, legacy local UET `0.5050`, spatial-coupled candidate `0.5081`

## Core Self-Test Follow-Up

The core script now reports all A11 limit checks as passing after the GL limit verifier was
made deterministic and isolated from UET extras:

- command: `.\.venv\Scripts\python.exe docs/core/uet_master_equation.py`
- `Ginzburg-Landau limit`: `PASS - Initial V=0.5242; Final V=0.0001`

This is verifier hygiene evidence only. It does not change the Wave 5 physics boundary or the
blocked universality-shift gate.


## Wave 6 Sensitivity Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_spatial_coupling_sensitivity.json`

- `coefficient_sensitivity_gate`: `BLOCKED`
- `operator_form_revision_gate`: `BLOCKED`
- tested coefficient cases: `20`
- beta range: `0.4729` to `0.5243`
- best beta found: `0.4729`, still closer to mean-field than to the 3D Ising reference

This narrows the next blocker from general spatial coupling to coefficient-only insufficiency.
The next wave should revise the operator form or estimator rather than merely increasing the
current candidate coefficients.

## Wave 7 Correlation-Length Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_correlation_length_diagnostics.json`

- `critical_window_gate`: `BLOCKED`
- `estimator_adequacy_gate`: `BLOCKED`
- `operator_separation_gate`: `BLOCKED`
- spatial beta: `0.5081`
- spatial `nu_proxy`: `0.0324`
- spatial `xi_near/xi_far`: `1.0668`

This narrows the next blocker again: the current synthetic window and estimator do not expose
critical correlation growth. Stronger claims need finite-size/correlation-length-aware scaling
and a revised operator form, not beta-only curve fitting.

## Wave 8 Finite-Size Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_finite_size_scaling_diagnostics.json`

- `finite_size_coverage_gate`: `PASS`
- `binder_crossing_gate`: `PASS`
- `correlation_window_gate`: `BLOCKED`
- `operator_separation_gate`: `BLOCKED`
- max spatial near-critical `xi/L`: `0.0961`
- max baseline near-critical `xi/L`: `0.1045`

This narrows the next blocker to finite-size window and operator separation. The current grid
coverage can run the diagnostic, but the spatial candidate still does not create enough
near-critical correlation length or baseline separation.

## Wave 9 Critical-Window Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_critical_window_relaxation_diagnostics.json`

- `critical_window_extension_gate`: `BLOCKED`
- `relaxation_sensitivity_gate`: `BLOCKED`
- `operator_separation_gate`: `BLOCKED`
- max spatial `xi/L`: `0.0737`
- max baseline `xi/L`: `0.0797`
- nearest-T relaxation gain from `700` to `2800` steps: `-0.0024`

This narrows the blocker again: simply moving closer to `Tc` and running longer does not create
measurable connected correlation growth for the current spatial candidate.


## Wave 10 Operator-Form Requirement Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_operator_form_requirement_gate.json`

- `prior_artifact_chain_gate`: `PASS`
- `core_engine_alignment_gate`: `PASS`
- `coefficient_only_path_gate`: `BLOCKED`
- `finite_size_signal_gate`: `BLOCKED`
- `critical_window_path_gate`: `BLOCKED`
- `operator_form_requirement_gate`: `BLOCKED`

This converts the Wave 5-9 blocker chain into an explicit design requirement. The next repair
should not be a coefficient-only sweep or longer run of `spatial_coupled_v1`; it needs a new
opt-in operator form with nonlocal, conserved, or scale-dependent behavior plus fresh unit,
formula, correlation-growth, and finite-size gates.


## Wave 11 Spatial-Coupled V2 Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_spatial_coupled_v2_diagnostic.json`

- `v2_core_operator_gate`: `PASS`
- `v2_spatial_safety_gate`: `PASS`
- `v2_stability_gate`: `PASS`
- `v2_correlation_response_gate`: `BLOCKED`
- `v2_operator_separation_gate`: `BLOCKED`
- max `xi/L`: baseline `0.0798`, v1 `0.0813`, v2 `0.0733`

This implements the first Wave 10-compliant candidate shape, but it does not repair the physics
blocker. The operator is available, opt-in, interface-gated, and conserved on the game-force
lane, yet it still does not create connected-correlation growth or separation from baseline.


## Wave 12 V2 Component-Ablation Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_spatial_coupled_v2_component_ablation.json`

- `ablation_coverage_gate`: `PASS`
- `force_lane_activity_gate`: `PASS`
- `component_improvement_gate`: `BLOCKED`
- `memory_length_response_gate`: `BLOCKED`
- baseline max `xi/L`: `0.0801`
- best v2 profile: `v2_memory_long`, improvement over baseline `-0.0038`

This narrows the v2 blocker: the tested information, game, full, short-memory, and long-memory
profiles are stable and force-isolated, but they remain correlation-neutral or damping relative
to baseline. The next operator revision should not simply recombine these v2 components.


## Wave 13 Model C Conserved-Order Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_model_c_conserved_order_diagnostic.json`

- `model_c_engine_alignment_gate`: `PASS`
- `mass_conservation_gate`: `PASS`
- `domain_growth_gate`: `PASS`
- `operator_distinction_gate`: `PASS`
- `claim_boundary_gate`: `WARN`
- Model C max mass drift: `~2.1e-16`
- median `xi` growth ratio: Model C `30.49`, baseline comparison `24.68`

This does not validate a full phase-transition claim. It does narrow the next repair path: after
v2 components remained correlation-neutral or damping, the conserved order-parameter structure
from Model C is the strongest mechanism-level candidate for future opt-in core integration.


## Wave 14 Conserved-Order Core-Candidate Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_core_candidate.json`

- `core_conserved_alignment_gate`: `PASS`
- `legacy_compatibility_gate`: `PASS`
- `conserved_mass_gate`: `PASS`
- `wave13_bridge_gate`: `PASS`
- `core_mechanism_response_gate`: `BLOCKED`
- `claim_boundary_gate`: `WARN`
- core conserved max mass drift: `~1.0e-17`
- median `xi` growth ratio: core conserved `0.87`, legacy core comparison `1.47`

This makes Model C-style conserved dynamics available through the core engine as an opt-in
candidate, but it does not yet reproduce the stronger topic Cahn-Hilliard mechanism response.
The next repair should focus on the numerical/operator form of the core conserved path.

## Current Boundary

The Wave 5 candidate fixes the narrow implementation blocker that spatial operators were not
available in the core engine. It does not fix the physics blocker: the current candidate still
fits near mean-field behavior and does not shift toward the 3D Ising beta exponent. Wave 14
now records the next controller as `conserved_order_core_candidate_needs_mechanism_tuning`.

## Next Hardening Step

Keep all candidate operators as opt-in diagnostics. The next wave should tune or replace the
explicit finite-difference conserved core path, likely by comparing it against the spectral/semi-implicit
Cahn-Hilliard engine before rerunning finite-size or universality claims.
