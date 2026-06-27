# Limitations

- The root baseline comparison is present, but numeric acceptance boundaries are still provisional until a saved artifact is generated and reviewed.
- Current data posture is "real source referenced", which is below a fully normalized archival dataset package.
- The topic still needs a clearer split between exploratory test files and the single canonical verification workflow.
- The current primary verifier tests only the beta critical exponent against a topic-local 3D Ising/liquid-gas working copy.
- Gamma, nu, scaling relations, morphology metrics, and material critical-point datasets are not yet gated.
- The spectral Cahn-Hilliard solver is normalized; its grid units and parameters are not yet mapped to a specific material system.
- Internal script execution does not by itself establish external replication, formal proof, or broad physical closure.
- Topic-level source-evidence and branch-claim gates now make that boundary explicit: accepted evidence stops at the selected beta benchmark and normalized mechanism lane, not universal phase-transition closure.
- The artifact-level `phase_transition_claim_scope_gate` is the export controller: a passing
  beta gate remains topic-level `WARN` until source archives, full exponent/scaling checks,
  material critical-point gates, and renormalization-group closure are available.
- Wave 4 synthetic scaling showed the historical UET terms stayed near mean-field behavior, not the 3D Ising exponent.
- Wave 5 adds an opt-in `spatial_coupled_v1` core candidate, but the current dynamics verifier remains `WARN`: engine alignment and spatial-operator gates pass, while `universality_shift_gate` is `BLOCKED`.
- The current spatial-coupled candidate estimates beta near mean-field (`0.5081`), so it must stay a diagnostic heuristic bridge until a revised operator or derivation changes the gate result.
- Wave 6 coefficient sensitivity found beta only in the `0.4729` to `0.5243` range across the tested coefficient grid; coefficient-only tuning is not evidence for escaping mean-field behavior.
- Wave 7 correlation-length diagnostics found only weak correlation growth (`xi_near/xi_far ~= 1.07`, `nu_proxy ~= 0.03`), so the current synthetic window/estimator is not adequate for RG or universality-class claims.
- Wave 8 finite-size diagnostics found `finite_size_coverage_gate == PASS` and `binder_crossing_gate == PASS`, but `correlation_window_gate == BLOCKED` and `operator_separation_gate == BLOCKED`; the current grid/window still cannot support universality-class claims.
- Wave 9 critical-window relaxation found that closer-to-Tc temperatures and longer runs still keep spatial `xi/L` below `0.074`, with no baseline separation; runtime/window extension alone is not a supported repair path.
- Wave 10 operator-form requirement aggregation keeps `operator_form_requirement_gate == BLOCKED`; the next candidate needs a nonlocal, conserved, or scale-dependent operator form plus fresh unit/formula/scaling gates before any dynamics claim can be upgraded.
- Wave 11 adds a first `spatial_coupled_v2` core candidate with screened nonlocal memory and conserved interface/game drive, but the diagnostic still keeps dynamics claims blocked: v2 `max_xi/L` is `0.0733`, below baseline `0.0798`, and lane separation is negative.
- Wave 12 component ablation found that v2 info-only, game-only, full, short-memory, and long-memory profiles all remain below baseline `xi/L`; the current v2 component family should be treated as correlation-neutral or damping under this synthetic window.
- Wave 13 Model C diagnostics pass mechanism gates for conserved-order dynamics, but the result is normalized 2D mechanism evidence only; it still needs opt-in core integration plus finite-size/exponent gates before any dynamics or universality claim is upgraded.
- Wave 14 integrates `conserved_order_v1` as an opt-in core candidate, but the explicit core finite-difference path does not yet reproduce the Wave 13 mechanism response; core conserved median `xi` growth is `0.87`, below the legacy core comparison `1.47`.
- Wave 15 identifies the next blocker as numerical/operator-form stiffness, not coefficient strength: applying the Wave 13 spectral settings to an explicit core path implies a stiffness proxy of `32685`, about `335544x` the Wave 14 explicit candidate setting, so a spectral or semi-implicit conserved-order core path is required before claim upgrades.
- Wave 16 adds `conserved_order_spectral_v1` and passes the core spectral bridge under normalized 2D Wave 13-like settings, but it remains diagnostic-only: finite-size scaling, exponent fits, material calibration, and RG closure are still open.
