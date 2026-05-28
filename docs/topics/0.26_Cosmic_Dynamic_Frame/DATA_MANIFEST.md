# Data Manifest

Current data reality status: "real source referenced with local working copies"

External-source audit status: `Laniakea/Cosmicflows/Pioneer source records pinned; raw tables and preprocessing still open`.

Priority remediation:

- Archive raw Cosmicflows/Laniakea flow tables and Pioneer residual/telemetry tables where
  they support the dynamic-frame argument.
- Add observer-frame metadata for every cosmic-flow dataset: reference frame, velocity
  convention, distance calibration, redshift correction, and whether values are observed or
  model-inferred.
- Treat local subsets as working derivatives until raw source, preprocessing, and hashes are
  documented.
- See `docs/meta/core_data_external_source_audit.md` for the cross-topic data-hardening plan.

| Item | Local path | Source | Unit convention | Benchmark role | Bytes | SHA-256 | Provenance status |
|:--|:--|:--|:--|:--|--:|:--|:--|
| Laniakea source record | `docs/data/external/cosmology/laniakea/tully_2014/source_record.json` | Tully et al. 2014 Nature, DOI `10.1038/nature13674` | Supergalactic coordinates and peculiar-velocity context as declared by source record | Upstream provenance anchor for the local landmark working copy | 1,232 | `880397cf02e92fd472b434a1e9f8d2bee6a0ac09d03c40daf90ebf5bb6c40eec` | Source record present; raw peculiar-velocity reconstruction not stored. |
| Cosmicflows-3 source record | `docs/data/external/cosmology/cosmicflows/cosmicflows3/source_record.json` | Tully, Courtois, Sorce 2016 AJ, DOI `10.3847/0004-6256/152/2/50` | Distance/velocity conventions depend on upstream catalog and subset extraction | Upstream provenance anchor for local subset and future residual gate | 1,119 | `72c130a7c003dc69e01d82adb8ba1d9e3a4aa6426caf585f0fd5b64a2af70b17` | Source record present; raw catalog extraction not verified. |
| Pioneer anomaly source record | `docs/data/external/spacecraft/pioneer_anomaly/anderson_2002/source_record.json` | Anderson et al. 2002 PRD, DOI `10.1103/PhysRevD.65.082004` | Acceleration/residual units remain tied to upstream analysis conventions | Upstream provenance anchor for diagnostic anomaly branch | 1,361 | `aa71373b211ffb9e1f36e72bc16cdae00f6917d4b2b17a6364bc0d3e921c612f` | Source record present; telemetry/residual raw tables not stored. |
| Pioneer thermal-recoil source record | `docs/data/external/spacecraft/pioneer_anomaly/turyshev_2012_thermal_recoil/source_record.json` | Turyshev et al. thermal-recoil competitor record | Source-specific thermal model terms after future extraction | Upstream competitor anchor for Pioneer branch | 1,138 | `8ec35ee9ebfa1cb900c65837d099b2689dd41d8034152a295d009616ebe5445d` | Source record present; no numeric competitor package archived. |
| source_lock_manifest.json | `Data/03_Research/source_lock_manifest.json` | Topic-derived source-lock package tying local working copies to source records | Mixed local conventions declared per file | Connects verifier inputs to upstream source records | 4,264 | `b9aa4fb10e3f588e6a76e681b08b236db4161326b3c12f89a71afc71d9840c22` | Present; upgrades provenance but not physical claim class. |
| source_evidence_intake_stub.json | `Data/03_Research/source_evidence_intake_stub.json` | Topic-generated intake sheet for unresolved upstream raw/source packages | Mixed; each target declares its own expected frame or unit basis | Landing zone before data rewrites or claim upgrades | 5,584 | `98427fcf260fdaca73fc6224b3a6abeaa2d5981c1067841c655e990459037e3d` | Workflow control only; not evidence by itself. |
| source_evidence_readiness_matrix.json | `Data/03_Research/source_evidence_readiness_matrix.json` | Topic-generated readiness gate derived from intake stub | n/a | Tracks completeness of evidence capture | 2,330 | `575efc62d29bc0b135fc763625e2adb966daa521d074da1dc29ad6abe6006ef5` | Current snapshot: Laniakea `5/6`, Cosmicflows `4/6`, Pioneer anomaly `5/6`, thermal-recoil competitor `1/6`. Workflow control only; records completeness, not scientific validation. |
| dependency_claim_gate.json | `Data/03_Research/dependency_claim_gate.json` | Topic-generated dependency gate referencing `0.1`, `0.23`, and `0.0` | n/a | Controls inherited claim ceiling from upstream core topics | 2,115 | `13fa161b9bc834f410e3b8135d674cdb8280b72d5133f9f00046d03bf0e41309` | Workflow control only; cannot raise claim class above linked upstream limits. |
| Laniakea_Flows.json | `Data/03_Research/Laniakea_Flows.json` | Topic-local landmark working copy tied to Laniakea source record | `coords` in supergalactic Mpc; `velocity_mag` in km/s where present | Primary visualization input | 1,345 | `d706e14d9fa50725e4afc164da517693cc2f15dfbfeef9f2c0a90a78ee66c862` | Visualization input only; not raw flow reconstruction. |
| Cosmicflows_3_Subset.csv | `Data/Cosmicflows_3_Subset.csv` | Topic-local subset tied to Cosmicflows-3 source record | Working-copy CSV; observer frame and calibration still open | Future residual/baseline scaffold | 4,131 | `dfa7ed92f2490c3cdc035a97fc24706de831c7e59b88c5820eb09bd68d9f669f` | Working copy; frame, calibration, and extraction path still need audit. |
| Download_Cosmic_Data.py | `Data/Download_Cosmic_Data.py` | Topic-local working copy or generated benchmark input | n/a | Manual or partial data handling helper | 2,238 | `6ce5e95c3ebce442b6b128412e2feea17edae213f8e577c7f84d5899e1c86fd6` | Manual, placeholder, or partially scripted data handling is still present. |
| Pioneer_Anomaly_Data.csv | `Data/Pioneer_Anomaly_Data.csv` | Topic-local working copy tied to Pioneer anomaly source record | Working-copy anomaly values; thermal-recoil competitor absent | Diagnostic-only branch input | 307 | `f0a050dac03333b471d27214251e36f11d63684d48a555235e61e7eed471bb25` | Diagnostic only; competitor thermal-recoil baseline absent. |
| Research_Cosmic_Flows.py | `Code/03_Research/Research_Cosmic_Flows.py` | Topic verifier | n/a | Regenerates provenance/status artifact and Laniakea flow-map figure | 27,436 | `ddbf79e9433de931add02c3a5bec26d8b5f81218585a49ce7757d8b8103e456d` | Executable verifier; visualization/provenance gate only. |
| 0_26_cosmic_dynamic_frame_verification.json | `Result/artifacts/0_26_cosmic_dynamic_frame_verification.json` | Generated verifier artifact | n/a | Machine-readable claim/status controller | 10,997 | `bc3dbba10e701ac163744b8c6c7f5f598caccbd59765de8d8527cab46465eca5` | Current artifact reports topic `WARN` and theory-level dynamic-frame claims `BLOCKED`. |
| Laniakea_Flow_Map.png | `Result/01_Showcase/Laniakea_Flow_Map.png` | Generated from `Research_Cosmic_Flows.py` and `Laniakea_Flows.json` | Visual supergalactic landmark map | Visualization artifact | 634,517 | `2c0ff5499428009af08b2e6fb7c0353bdbe32f530b099fc697974fc1fe638cf0` | Supports visualization/provenance only; not a numeric cosmology fit. |

Repository note:

- This manifest was created during the repo standards pass and should be tightened further in a later provenance-normalization wave.
- Until raw tables, observer-frame metadata, preprocessing notes, and upstream hashes are frozen, treat the dataset package as source-referenced working copies rather than an archival release.
- `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `dependency_claim_gate.json` are workflow artifacts. They support provenance and dependency control but do not themselves validate the dynamic-frame mechanism.

## Current Readiness Snapshot

- Laniakea package: `5/6` fields complete; missing `original_file_name`
- Cosmicflows-3 subset package: `4/6` fields complete; missing `original_file_name` and `subset_selection_rule`
- Pioneer anomaly package: `5/6` fields complete; missing `original_file_name`
- Pioneer thermal-recoil competitor baseline: `0/6` fields complete; still a fully open competitor lane
