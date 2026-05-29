# Limitations

- The primary verifier uses the standard Rydberg relation with CODATA `R_H`; it does not derive `R_H` from UET first principles.
- The current benchmark covers selected hydrogen Balmer and Lyman lines only.
- The formula bridge manifest records Bohr/de Broglie/Rydberg inheritance and UET dependency roles, but it is not itself a proof that UET derives the atomic spectrum.
- `0.13` can currently be used only as energy/information accounting context for atomic transitions; it does not derive `h`, `R_H`, or the transition operator in this topic.
- `0.6` and `0.17` can currently be used only as dependency context for `alpha`, charge-sector constants, and electron mass; they do not close the atomic Hamiltonian here.
- Hydrogen-like ion predictions are checkpoint-only rows using simplified `Z^2` scaling. They do not validate He+, Li2+, or other one-electron ions until source-backed spectra, reduced-mass conventions, nuclear masses, uncertainty policy, and thresholds are added.
- Local spectral rows may be rounded or curated; source-table transcription precision should be audited before public ppm claims.
- Air wavelengths are present in the data but the primary metric uses vacuum wavelengths only.
- The engine has a local rounded `R_H = 1.09677e7 m^-1`; ppm-level claims should use the CODATA working copy instead.
- The three-body script is a coupling smoke test and does not validate atomic three-body physics.
- Fine structure, Lamb shift, hyperfine structure, helium, and many-electron atoms are outside the current artifact.
- Downstream core topics must inherit these limitations before using `0.20` as atomic evidence.
- Topic-level source-evidence and branch-claim gates now make that boundary explicit: accepted evidence stops at the hydrogen Rydberg benchmark and constant-consistency branch, not full atomic-theory closure.
- The artifact-level `atomic_claim_scope_gate` is the export controller: hydrogen benchmark
  PASS cannot be cited as first-principles Rydberg derivation, QED correction validation,
  Lamb-shift explanation, helium validation, many-electron solution, or full atomic-theory closure.
