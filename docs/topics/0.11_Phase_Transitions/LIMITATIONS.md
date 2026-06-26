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
