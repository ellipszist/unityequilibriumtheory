# Data Manifest

Current data reality status: `real source referenced`

The current primary verifier uses the topic-local `critical_exponents.json` working copy.
It cites critical-exponent literature in metadata, but upstream source files are not yet
stored as a normalized external archive.

| Item | Local path | Source | Provenance status |
|:--|:--|:--|:--|
| critical exponent working copy | `Data/03_Research/critical_exponents.json` | Zinn-Justin (2002), Pelissetto & Vicari (2002) metadata in file | Primary beta-exponent benchmark; hash written by verifier artifact |
| NIST critical point summary | `Data/NIST_Critical_Points.csv` | NIST-style critical-point working copy | Future material-data gate; not current primary verifier |
| brownian data helper | `Data/03_Research/brownian_data.py` | Topic-local working copy | Exploratory only |
| legacy black-hole data copy | `Data/03_Research/black_hole_data.json` | Topic-local working copy | Not part of current primary verifier |

## Unit and benchmark roles

| Dataset | Unit convention | Benchmark role |
| :-- | :-- | :-- |
| `critical_exponents.json` | critical exponents are dimensionless | Primary beta benchmark |
| `NIST_Critical_Points.csv` | `Tc` K, `Pc` MPa, critical density kg/m^3 | Future material critical-point benchmark |

Repository note:

- This manifest was created during the repo standards pass and should be tightened further in a later provenance-normalization wave.
- Until upstream URLs, DOIs, preprocessing notes, and hashes are frozen, treat the dataset package as an internal working copy rather than an archival release.
- Future work should store upstream critical-exponent references and critical-point tables under `docs/data/external/phase_transitions/...` before claim upgrades.
