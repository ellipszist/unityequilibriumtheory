# Limitations

- The primary verifier checks a source constant against a local CODATA working copy; it does not derive `G`.
- Planck units are standard definitions computed from constants, not an independent validation of UET gravity.
- Weak-field calculations such as `g = GM/r^2`, `r_s = 2GM/c^2`, and `n(r) ~= 1 + 2GM/(rc^2)` are diagnostics unless tied to source-backed artifacts.
- The equivalence-principle script currently asserts `eta = 0`; it does not compare against the MICROSCOPE 2022 reported value and uncertainty.
- Eot-Wash short-range gravity data exists locally, but no primary artifact currently tests UET parameter values against the exclusion curve.
- This topic does not currently validate light bending, perihelion precession, Einstein field equations, singularity avoidance, or quantum-gravity closure.
- Downstream core topics must inherit these limitations before citing `0.19` for broad GR or cosmology claims.
- Topic-level source-evidence and branch-claim gates now make that boundary explicit: accepted evidence stops at the CODATA constant checkpoint and derived Planck-unit branch, not GR closure.
- The artifact-level `gravity_claim_scope_gate` is the export controller: constant PASS
  cannot be cited as first-principles G derivation, GR validation, equivalence-principle
  proof, short-range gravity validation, singularity resolution, or quantum-gravity closure.
