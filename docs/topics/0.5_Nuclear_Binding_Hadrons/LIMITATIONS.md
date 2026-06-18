# Limitations

- The current strict binding-energy verifier uses a source-backed extracted subset of AME2020, while the wider parsed table is reported through a separate diagnostic artifact rather than a hard pass/fail gate.
- Heavy nuclei pass the current gate, but light nuclei are still intentionally excluded from the strict liquid-drop validation regime.
- The full-table diagnostic layer is expected to show much weaker performance for lighter nuclei, so the topic should not be described as uniformly accurate across the whole AME2020 parsed table.
- The engine uses fixed semi-empirical coefficients plus a UET correction term, so this topic should not yet be presented as fully parameter-free.
- Only the heavy-nucleus subset branch and proton-radius benchmark-anchor branch are currently accepted by the branch claim gate.
- `nuclear_claim_scope_gate` allows those selected checks while blocking full-table, light-nuclei, QCD, hadron-mass, confinement, and complete strong-force exports.
- A topic-local PDG-derived hadron/quark reference package now exists, and a diagnostic hadron-model verifier reads it for supported formula paths, but the resulting residuals remain too weak for validation wording.
- The engine now exposes SEMF-only, entropy-correction, Yukawa-correction, and total binding components in the saved strict artifact.
- In the current heavy selected subset, SEMF-only mean error is lower than the total path after current correction terms, so the correction lane is diagnostic rather than an improvement claim.
- SEMF coefficients are still checked-local constants rather than a source-locked coefficient package, so decomposition does not make the topic parameter-free.
- `semf_coefficient_provenance_gate.json` now makes that coefficient/source-policy blocker machine-readable and explicitly blocks first-principles nuclear-binding wording.
- The proton-radius path currently returns a benchmark-anchor value and should not be described as an independent radius prediction.
- `pdg_hadron_qcd_source_mapping_gate.json`, `pdg_hadron_quark_reference_package.json`, and `Result/artifacts/pdg_hadron_quark_source_linkage.json` show that selected PDG 2025 quark and hadron mass rows are source-mapped (`16/16` found, `0` unit mismatches).
- `Result/artifacts/hadron_model_source_package_diagnostic.json` compares 7 supported source-package labels and records about `75.33%` mean error and `94.91%` max error, so it is a blocker artifact rather than validation evidence.
- The QCD bridge still contains diagnostic/open branches and should not support public QCD-running claims until source-backed inputs and verifier contracts are hardened.
- The `alpha_s_uet_v2` data-shape bug is now fixed and smoke-tested in `qcd_alpha_s_source_probe.json`, but the local PDG SQLite probe found no direct alpha_s/QCD-running source row, so QCD running remains source-blocked.
- The color-confinement proof script now returns real pass/fail status, and `confinement_proof_gate_diagnostic.json` records a `FAIL` for the current narrow proton-mass consistency check; this is still not a formal confinement proof.
- Internal script execution does not by itself establish external replication, theorem-level proof, or broad physical closure.
