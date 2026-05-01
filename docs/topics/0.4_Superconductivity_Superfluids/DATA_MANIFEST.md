# Data Manifest

Current data reality status: `real source referenced`

The primary verifier currently regenerates `real_superconductor_data.json` from the
in-script working-copy table in `Experiment_Superconductor_Data.py`. That table has cited
literature labels, but it is not yet a normalized upstream archive.

Source-lock package:

- `Data/03_Research/source_lock_manifest.json`
- `docs/data/external/condensed_matter/superconductivity/mcmillan_1968/source_record.json`
- `docs/data/external/condensed_matter/superconductivity/allen_dynes_1975/source_record.json`
- `docs/data/external/condensed_matter/superconductivity/nims_supercon/source_record.json`

| Item | Local path | Source | Provenance status |
|:--|:--|:--|:--|
| raw superconductor working copy | `Data/03_Research/real_superconductor_data.json` | Generated from `Experiment_Superconductor_Data.py`; cites NIMS SuperCon, MIT Junior Lab, Kittel, McMillan 1968 | Primary McMillan baseline input; hash is written by verifier artifact; inverse-McMillan diagnostic now records the `lambda_ep` needed to match each observed `Tc` |
| calibrated superconductor working copy | `Data/03_Research/calibrated_superconductors.json` | Inverse McMillan calibration table | Calibrated input; not valid as no-fit prediction evidence |
| comprehensive superconductor package | `Data/03_Research/comprehensive_superconductor_data.json` | McMillan/Allen-Dynes working package | Engine candidate input; needs separate verifier |
| material summary CSV | `Data/Supercon_Materials.csv` | Topic-local summary table | Context only |
| Casimir files | `Data/03_Research/casimir_data.py`, `Data/03_Research/casimir_force_data.json` | Casimir reference working copy | Not part of current primary verifier |
| source-lock manifest | `Data/03_Research/source_lock_manifest.json` | Topic-derived provenance package tied to McMillan 1968, Allen-Dynes 1975, and NIMS SuperCon source records | Primary verifier hashes this manifest and external source records |

## Unit and benchmark roles

| Dataset | Unit convention | Benchmark role |
| :-- | :-- | :-- |
| `real_superconductor_data.json` | `Tc_K`, `Theta_D_K`, and uncertainty in Kelvin; `lambda_ep` and `mu_star` dimensionless | Primary raw McMillan baseline |
| `calibrated_superconductors.json` | `Tc_K`, `Theta_D_K` in Kelvin; `lambda_calibrated` dimensionless | Calibration diagnostic only |
| `comprehensive_superconductor_data.json` | `Tc_exp_K`, `omega_log_K` in Kelvin; coupling constants dimensionless | Future Allen-Dynes/UET engine gate |

Repository note:

- This manifest was created during the repo standards pass and should be tightened further in a later provenance-normalization wave.
- Until upstream URLs, DOIs, preprocessing notes, and hashes are frozen, treat the dataset package as an internal working copy rather than an archival release.
- Future work should move raw upstream material tables into `docs/data/external/condensed_matter/...` and keep topic-derived calibrated tables under this topic's `Data/` folder.
- The current artifact records `run_status=PASS` but `model_gate_status=FAIL`; this is a scientific blocker for the raw McMillan parameter package, not a file-generation failure.
- The current artifact also records `parameter_mismatch_audit`: 9 of 10 inverse-solvable rows use a declared `lambda_ep` above the value required to reproduce observed `Tc` with the same `Theta_D_K` and `mu_star`. This directs the next data-hardening step toward row-level `lambda_ep`, `Theta_D_K`, and material-specific phonon-scale provenance.
