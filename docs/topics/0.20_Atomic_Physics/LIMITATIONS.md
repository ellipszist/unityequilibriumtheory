# Limitations

- The primary verifier uses the standard Rydberg relation with CODATA `R_H`; it does not derive `R_H` from UET first principles.
- The current benchmark covers selected hydrogen Balmer and Lyman lines only.
- The formula bridge manifest records Bohr/de Broglie/Rydberg inheritance and UET dependency roles, but it is not itself a proof that UET derives the atomic spectrum.
- `0.13` can currently be used only as energy/information accounting context for atomic transitions; it does not derive `h`, `R_H`, or the transition operator in this topic.
- `0.6` and `0.17` can currently be used only as dependency context for `alpha`, charge-sector constants, and electron mass; they do not close the atomic Hamiltonian here.
- Hydrogen level-energy rows support only rounded `n`-level benchmark language. Direct ASD per-level precision, fine-structure splitting, Lamb shift, hyperfine structure, and QED level corrections remain outside this gate.
- Hydrogen-like ion rows now support only a provisional selected He+/Li2+ reduced-mass benchmark plus a C VI higher-Z stress-test lane. Li III still needs direct primary ASD capture, and the gate does not validate broad hydrogen-like ion coverage.
- The selected He+/Li2+ and C VI ion rows use representative source wavelengths/blends; they do not resolve or validate fine-structure/QED components.
- Precision spectroscopy rows for 1S-2S, Lamb shift, and 21 cm hyperfine support source-package targets plus nonrelativistic, leading Dirac, empirical Lamb-handoff 1S-2S residual diagnostics, 21 cm wavelength bookkeeping, and a leading Fermi-contact hyperfine baseline only. No first-principles QED/recoil/proton-radius/hyperfine Hamiltonian residual model is primary-gated yet.
- Neutral helium rows are source-package targets with photon energies, NIST term assignments, wavelength-medium normalization, and line-component/blend policy computed only. The two-electron Hamiltonian, correlation treatment, uncertainty propagation, resolved line-shape policy for precision use, and many-electron residual model are not primary-gated yet.
- Local spectral rows may be rounded or curated; source-table transcription precision should be audited before public ppm claims.
- Air wavelengths are present in the data but the primary metric uses vacuum wavelengths only.
- The engine has a local rounded `R_H = 1.09677e7 m^-1`; ppm-level claims should use the CODATA working copy instead.
- The three-body script is a coupling smoke test and does not validate atomic three-body physics.
- Fine structure, Lamb shift, hyperfine structure, neutral-helium residual validation, and many-electron atoms are outside the current artifact.
- Downstream core topics must inherit these limitations before using `0.20` as atomic evidence.
- Topic-level source-evidence and branch-claim gates now make that boundary explicit: accepted evidence stops at the hydrogen Rydberg benchmark and constant-consistency branch, not full atomic-theory closure.
- The artifact-level `atomic_claim_scope_gate` is the export controller: hydrogen benchmark
  PASS cannot be cited as first-principles Rydberg derivation, QED correction validation,
  Lamb-shift explanation, helium validation, many-electron solution, or full atomic-theory closure.
