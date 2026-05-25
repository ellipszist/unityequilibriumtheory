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

| Item | Local path | Source | Unit convention | Benchmark role | Provenance status |
|:--|:--|:--|:--|:--|:--|
| Laniakea source record | `docs/data/external/cosmology/laniakea/tully_2014/source_record.json` | Tully et al. 2014 Nature, DOI `10.1038/nature13674` | Supergalactic coordinates and peculiar-velocity context as declared by source record | Upstream provenance anchor for the local landmark working copy | Source record present; SHA-256 `880397cf02e92fd472b434a1e9f8d2bee6a0ac09d03c40daf90ebf5bb6c40eec`; raw peculiar-velocity reconstruction not stored. |
| Cosmicflows-3 source record | `docs/data/external/cosmology/cosmicflows/cosmicflows3/source_record.json` | Tully, Courtois, Sorce 2016 AJ, DOI `10.3847/0004-6256/152/2/50` | Distance/velocity conventions depend on upstream catalog and subset extraction | Upstream provenance anchor for local subset and future residual gate | Source record present; SHA-256 `72c130a7c003dc69e01d82adb8ba1d9e3a4aa6426caf585f0fd5b64a2af70b17`; raw catalog extraction not verified. |
| Pioneer anomaly source record | `docs/data/external/spacecraft/pioneer_anomaly/anderson_2002/source_record.json` | Anderson et al. 2002 PRD, DOI `10.1103/PhysRevD.65.082004` | Acceleration/residual units remain tied to upstream analysis conventions | Upstream provenance anchor for diagnostic anomaly branch | Source record present; SHA-256 `aa71373b211ffb9e1f36e72bc16cdae00f6917d4b2b17a6364bc0d3e921c612f`; telemetry/residual raw tables not stored. |
| source_lock_manifest.json | `Data/03_Research/source_lock_manifest.json` | Topic-derived source-lock package tying local working copies to source records | Mixed local conventions declared per file | Connects verifier inputs to upstream source records | Present; SHA-256 `b9aa4fb10e3f588e6a76e681b08b236db4161326b3c12f89a71afc71d9840c22`; upgrades provenance but not physical claim class. |
| source_evidence_intake_stub.json | `Data/03_Research/source_evidence_intake_stub.json` | Topic-generated intake sheet for unresolved upstream raw/source packages | Mixed; each target declares its own expected frame or unit basis | Landing zone before data rewrites or claim upgrades | Workflow control only; not evidence by itself. |
| source_evidence_readiness_matrix.json | `Data/03_Research/source_evidence_readiness_matrix.json` | Topic-generated readiness gate derived from intake stub | n/a | Tracks completeness of evidence capture | Current snapshot: Laniakea `5/6`, Cosmicflows `4/6`, Pioneer anomaly `5/6`, thermal-recoil competitor `0/6`. Workflow control only; records completeness, not scientific validation. |
| dependency_claim_gate.json | `Data/03_Research/dependency_claim_gate.json` | Topic-generated dependency gate referencing `0.1`, `0.23`, and `0.0` | n/a | Controls inherited claim ceiling from upstream core topics | Workflow control only; cannot raise claim class above linked upstream limits. |
| Laniakea_Flows.json | `Data/03_Research/Laniakea_Flows.json` | Topic-local landmark working copy tied to Laniakea source record | `coords` in supergalactic Mpc; `velocity_mag` in km/s where present | Primary visualization input | Visualization input only; not raw flow reconstruction. |
| Cosmicflows_3_Subset.csv | `Data/Cosmicflows_3_Subset.csv` | Topic-local subset tied to Cosmicflows-3 source record | Working-copy CSV; observer frame and calibration still open | Future residual/baseline scaffold | Working copy; frame, calibration, and extraction path still need audit. |
| Download_Cosmic_Data.py | `Data/Download_Cosmic_Data.py` | Topic-local working copy or generated benchmark input | n/a | Manual or partial data handling helper | Manual, placeholder, or partially scripted data handling is still present. |
| Pioneer_Anomaly_Data.csv | `Data/Pioneer_Anomaly_Data.csv` | Topic-local working copy tied to Pioneer anomaly source record | Working-copy anomaly values; thermal-recoil competitor absent | Diagnostic-only branch input | Diagnostic only; competitor thermal-recoil baseline absent. |

Repository note:

- This manifest was created during the repo standards pass and should be tightened further in a later provenance-normalization wave.
- Until raw tables, observer-frame metadata, preprocessing notes, and upstream hashes are frozen, treat the dataset package as source-referenced working copies rather than an archival release.
- `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `dependency_claim_gate.json` are workflow artifacts. They support provenance and dependency control but do not themselves validate the dynamic-frame mechanism.

## Current Readiness Snapshot

- Laniakea package: `5/6` fields complete; missing `original_file_name`
- Cosmicflows-3 subset package: `4/6` fields complete; missing `original_file_name` and `subset_selection_rule`
- Pioneer anomaly package: `5/6` fields complete; missing `original_file_name`
- Pioneer thermal-recoil competitor baseline: `0/6` fields complete; still a fully open competitor lane
