# Data Manifest

Current data reality status: "manual or placeholder"

External-source audit status: `conceptually important but under-specified provenance`.

Priority remediation:

- Source-lock Cosmicflows-3/4 records, Laniakea flow references, and Pioneer anomaly source
  tables where they support the dynamic-frame argument.
- Add observer-frame metadata for every cosmic-flow dataset: reference frame, velocity
  convention, distance calibration, redshift correction, and whether values are observed or
  model-inferred.
- Treat local subsets as working derivatives until raw source, preprocessing, and hashes are
  documented.
- See `docs/meta/core_data_external_source_audit.md` for the cross-topic data-hardening plan.

| Item | Local path | Source | Provenance status |
|:--|:--|:--|:--|
| Laniakea_Flows.json | `Data/03_Research/Laniakea_Flows.json` | Topic-local working copy or generated benchmark input | Manual, placeholder, or partially scripted data handling is still present. |
| Cosmicflows_3_Subset.csv | `Data/Cosmicflows_3_Subset.csv` | Cosmicflows or anomaly working copy | Manual, placeholder, or partially scripted data handling is still present. |
| Download_Cosmic_Data.py | `Data/Download_Cosmic_Data.py` | Topic-local working copy or generated benchmark input | Manual, placeholder, or partially scripted data handling is still present. |
| Pioneer_Anomaly_Data.csv | `Data/Pioneer_Anomaly_Data.csv` | Cosmicflows or anomaly working copy | Manual, placeholder, or partially scripted data handling is still present. |

Repository note:

- This manifest was created during the repo standards pass and should be tightened further in a later provenance-normalization wave.
- Until upstream URLs, DOIs, preprocessing notes, and hashes are frozen, treat the dataset package as an internal working copy rather than an archival release.
