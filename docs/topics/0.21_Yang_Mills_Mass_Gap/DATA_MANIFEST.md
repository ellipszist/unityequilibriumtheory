# Data Manifest

## Source Inventory

| Item | Local path | Bytes | SHA-256 | Source | Provenance status | Benchmark role |
|:--|:--|--:|:--|:--|:--|:--|
| External source record | `docs/data/external/particle_physics/glueball/morningstar_peardon_1999/source_record.json` | 1211 | `f289bb3a3d818c5a955292bfcb8fd399488c7f032dd2133aa01d828984ef87a3` | Morningstar and Peardon, DOI `10.1103/PhysRevD.60.034509` | Source-pinned publication record | Primary bibliographic anchor |
| Lattice-QCD working copy | `data/03_Research/lattice_qcd_spectrum.json` | 1026 | `b6c8d4762d59f502686a8f35cebae852bd9a0bc54e29bcd302db9268358c9fbc` | Curated topic working copy from the cited lattice-QCD reference | Derived/local working table; not a full raw-table extraction package | Scalar glueball benchmark input |
| Source-lock manifest | `data/03_Research/source_lock_manifest.json` | 1644 | `f0e1ccc8d1ec7da9572545bc4fbcab749f041b21d68d55feb5a8fb1f869bcbc8` | Topic manifest tying source record, derived table, and verifier | Hashable run input | Reproducibility gate |
| Benchmark verifier script | `Code/03_Research/Research_Mass_Gap.py` | 12840 | `607866fe0e0bdb94ff126c028f978ed3e93a58acf7400c515042443a1432d389` | Topic verifier | Code artifact; not an external mathematical proof | Writes `mass_gap_validation.json` |
| Engine script | `Code/01_Engine/Engine_Mass_Gap.py` | 4557 | `ead8ad9d567b62dea0c8d4c10c80e3f54fbfc62e7a166deaa6fe0c41d74db97e` | Topic engine | Code artifact; fitted alpha sweep remains a calibration branch | Computes curvature-gap benchmark outputs |
| Benchmark citation | `docs/references.bib#morningstar_1999` | n/a | n/a | Published lattice-QCD benchmark | Citation-backed reference | Cross-document citation |

## Unit Convention

| Quantity | Unit | Source or conversion |
|:--|:--|:--|
| `mass_r0_units` | dimensionless lattice `m r0` | Topic working copy |
| `r0_physical_value_fm` | fm | Topic working-copy metadata |
| `hc_mev_fm` | MeV fm | Topic working-copy metadata |
| `mass_mev` | MeV | `mass_r0_units * hc_mev_fm / r0_physical_value_fm` |
| `reference_uncertainty_mev` | MeV | `uncertainty * hc_mev_fm / r0_physical_value_fm` |

## Integrity Requirements

- The verifier records hashes for the lattice working copy, source-lock manifest, benchmark script, engine script, and source record.
- This topic currently keeps its historical lowercase `data/` directory; future normalization can rename it to `Data/` repo-wide, but the verifier and manifest now point to the real tracked path.
- The current dataset is a curated topic table, not a full raw-table extraction package from the publisher.
- Any stronger result must first replace or supplement the working copy with reproducible upstream extraction notes and multi-state benchmark coverage.
