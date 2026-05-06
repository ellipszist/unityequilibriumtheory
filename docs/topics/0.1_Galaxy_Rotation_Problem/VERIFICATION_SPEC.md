# Verification Spec

- Primary command:
  - `python docs/topics/0.1_Galaxy_Rotation_Problem/Code/03_Research/Research_Galaxy_Rotation.py`
- Primary input:
  - `Data/03_Research/sparc_data.json`
- Input contract:
  - The current checked-in working copy is a summary-row benchmark table.
  - Required fields for each processed row are `name`, `R_kpc`, `v_obs`,
    `M_disk_Msun`, and `R_disk_kpc`.
  - Optional support fields are `M_bulge_Msun`, `redshift`, and `type`.
- Metric definition:
  - Per-row error: `abs(v_pred - v_obs) / v_obs * 100`
  - Topic gate: average absolute percent error across processed rows
  - Secondary metric: pass rate for rows below `15%` error
- Thresholds:
  - `PASS`: average absolute percent error `< 15.0`
  - `WARN`: verifier runs and produces valid comparisons, but average absolute
    percent error is `>= 15.0`
  - `FAIL`: verifier produces no valid comparisons or crashes
- Artifact target:
  - `Result/artifacts/galaxy_rotation_validation.json`
- Required artifact fields:
  - run metadata and command
  - dataset hash and file hash for `sparc_data.json`
  - processed row count and skipped row count
  - average error percent and pass rate percent when valid comparisons exist
  - per-galaxy result rows
  - claim boundary describing the benchmark as an internal summary-row test
- Interpretation:
  - Treat this verifier as an internal benchmark over the repository working copy.
  - Do not describe it as full upstream SPARC curve replication.
  - Stronger galaxy-dynamics claims require source-locked curve arrays and
    comparator baseline artifacts.
