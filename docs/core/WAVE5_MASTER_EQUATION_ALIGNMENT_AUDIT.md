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

## Wave 15 Conserved-Order Numerics-Gap Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_numerics_gap.json`

- `artifact_chain_gate`: `PASS`
- `mechanism_gap_gate`: `PASS`
- `explicit_core_viability_gate`: `BLOCKED`
- `spectral_core_requirement_gate`: `BLOCKED`
- Wave 13 explicit stiffness proxy: `32685`
- Wave 14 explicit stiffness proxy: `0.097`
- Wave 13-to-Wave 14 stiffness ratio: `335544`

This narrows the Wave 14 mechanism gap into a numerical/operator-form requirement. The next
core repair should not be mobility-only tuning or recombination of the current spatial v2
components; it should implement a spectral or semi-implicit conserved-order candidate.

## Wave 16 Conserved-Order Spectral-Core Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_spectral_core_candidate.json`

- `core_spectral_alignment_gate`: `PASS`
- `legacy_compatibility_gate`: `PASS`
- `spectral_mass_stability_gate`: `PASS`
- `topic_engine_bridge_gate`: `PASS`
- `mechanism_response_gate`: `PASS`
- `wave15_repair_gate`: `PASS`
- `claim_boundary_gate`: `WARN`
- core spectral max mass drift: `4.86e-16`
- max topic-engine field delta: `2.89e-12`
- median `xi` growth ratio: core spectral `30.49`, topic spectral reference `30.49`
- explicit `conserved_order_v1` stable cases under Wave 13-like settings: `0`

This repairs the core implementation bridge required by Wave 15 while keeping the candidate
opt-in and diagnostic-only. The next controller is now finite-size/exponent scaling, not core
spectral availability.

## Wave 17 Conserved-Order Spectral-Scaling Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_spectral_scaling.json`

- `wave16_bridge_gate`: `PASS`
- `finite_size_coverage_gate`: `PASS`
- `spectral_stability_gate`: `PASS`
- `binder_crossing_gate`: `PASS`
- `correlation_window_gate`: `BLOCKED`
- `universality_exponent_gate`: `BLOCKED`
- `claim_boundary_gate`: `WARN`
- max near-critical `xi/L`: `0.145`
- beta range: `1.61` to `1.83`
- median beta: `1.77`

This keeps the spectral core candidate claim-bounded: implementation stability is no longer the
controller, but the finite-size window and exponent scaling are not yet adequate for universality
promotion.

## Wave 18 Conserved-Order Spectral Window-Repair Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_spectral_window_repair.json`

- `wave17_chain_gate`: `PASS`
- `relaxation_window_repair_gate`: `BLOCKED`
- `kappa_window_sensitivity_gate`: `PASS`
- `signal_preservation_gate`: `BLOCKED`
- `claim_boundary_gate`: `WARN`
- max relaxation/window-only `xi/L`: `0.113`
- max kappa-sweep `xi/L`: `0.377`
- best high-`xi/L` order parameter: `0.000377`
- viable high-`xi/L` plus preserved-signal cases: `0`

This narrows the finite-size blocker into a signal-preservation problem. Kappa can create large
correlation-length proxies in this window, but not with enough order amplitude to count as
scaling evidence.


## Wave 19 Conserved-Order Spectral Spinodal-Window Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_spectral_spinodal_window.json`

- `wave18_chain_gate`: `PASS`
- `spinodal_access_gate`: `PASS`
- `order_signal_window_gate`: `PASS`
- `seed_margin_gate`: `BLOCKED`
- `finite_size_claim_boundary_gate`: `WARN`
- best viable case: `xi/L = 0.204`, order `0.0126`, `T = 0.900`, `kappa = 0.100`, `steps = 2400`
- target replicate pass fraction: `0.25`
- target replicate median `xi/L`: `0.1965`

This narrows the Wave 18 signal-preservation blocker: an order-preserving spinodal-window
candidate exists, but it is too close to the `xi/L` threshold and not seed-robust. Treat it as a
next-window candidate only, not as finite-size or universality evidence.


## Wave 20 Conserved-Order Spectral Seed-Margin Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_spectral_seed_margin.json`

- `wave19_chain_gate`: `PASS`
- `seed_group_coverage_gate`: `PASS`
- `seed_margin_repair_gate`: `PASS`
- `relaxation_margin_gate`: `PASS`
- `finite_size_replication_gate`: `BLOCKED`
- `claim_boundary_gate`: `WARN`
- target group: `T = 0.900`, `kappa = 0.100`, `steps = 4000`, `L = 16`
- target pass fraction: `1.0`
- target minimum `xi/L`: `0.2004`
- target minimum order parameter: `0.0505`

This repairs the Wave 19 seed-margin blocker for one normalized grid. The next controller is now
finite-size replication of the same window, not another single-grid seed retry.


## Wave 21 Conserved-Order Spectral Finite-Size Replication Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_spectral_finite_size_replication.json`

- `wave20_chain_gate`: `PASS`
- `finite_size_coverage_gate`: `PASS`
- `grid_replication_gate`: `BLOCKED`
- `seed_set_generalization_gate`: `BLOCKED`
- `exponent_claim_gate`: `BLOCKED`
- `claim_boundary_gate`: `WARN`
- `L=8` pass fraction: `1.0`, minimum `xi/L`: `0.4499`
- `L=12` pass fraction: `1.0`, minimum `xi/L`: `0.2423`
- `L=16` pass fraction: `0.667`, fresh-seed pass fraction: `0.333`, minimum `xi/L`: `0.1944`

This blocks promotion from the Wave 20 single-grid seed-margin repair. The next controller is a
finite-size/window-scaling or estimator repair for the `L=16` fresh-seed margin, not an exponent
or universality rerun.


## Wave 22 Conserved-Order Spectral L16 Relaxation-Repair Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_spectral_l16_relaxation_repair.json`

- `wave21_chain_gate`: `PASS`
- `l16_case_coverage_gate`: `PASS`
- `relaxation_repair_gate`: `BLOCKED`
- `order_signal_gate`: `PASS`
- `next_path_gate`: `BLOCKED`
- `claim_boundary_gate`: `WARN`
- `4000` step pass fraction: `0.333`, minimum `xi/L`: `0.1944`
- `4800` step pass fraction: `0.333`, minimum `xi/L`: `0.1938`
- `5600` step pass fraction: `0.333`, minimum `xi/L`: `0.1950`
- longest-group minimum order parameter: `0.1359`

This narrows the Wave 21 blocker: the `L=16` problem is not loss of order signal and is not
repaired by simply running longer. The next controller is estimator/window-scaling design.


## Wave 23 Conserved-Order Spectral L16 Estimator-Sensitivity Follow-Up

Artifact: `docs/topics/0.11_Phase_Transitions/Result/artifacts/0_11_conserved_order_spectral_l16_estimator_sensitivity.json`

- `wave22_chain_gate`: `PASS`
- `engine_path_gate`: `PASS`
- `estimator_case_coverage_gate`: `PASS`
- `default_estimator_reproduction_gate`: `PASS`
- `threshold_sensitivity_gate`: `PASS`
- `next_path_gate`: `BLOCKED`
- `claim_boundary_gate`: `WARN`
- default `e^-1` threshold pass fraction: `0.333`, minimum `xi/L`: `0.1938`
- lower threshold `0.30` pass fraction: `1.0`, minimum `xi/L`: `0.2067`
- lower threshold `0.25` pass fraction: `1.0`, minimum `xi/L`: `0.2161`
- lower threshold `0.20` pass fraction: `1.0`, minimum `xi/L`: `0.2256`
- threshold saturation count: `0` for every tested threshold

This narrows the Wave 22 blocker further: the `L=16` fields are stable and order-preserving, but
the declared `xi/L` result depends on an uncalibrated autocorrelation crossing threshold. This is
an estimator-design finding only, not acceptance of a new threshold or a universality result.

## Current Boundary

The Wave 5 candidate fixes the narrow implementation blocker that spatial operators were not
available in the core engine. It does not fix the physics blocker: the current candidate still
fits near mean-field behavior and does not shift toward the 3D Ising beta exponent. Wave 23
now records the next controller as `spectral_core_l16_xi_gate_threshold_sensitive`.

## Next Hardening Step

Keep all candidate operators as opt-in diagnostics. The next wave should derive or calibrate the
correlation estimator threshold, or replace it with a source-backed structure-factor/correlation
estimator, before rerunning finite-size, exponent, or universality gates.
