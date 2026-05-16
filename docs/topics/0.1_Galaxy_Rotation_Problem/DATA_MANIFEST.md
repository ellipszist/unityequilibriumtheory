# Data Manifest

| Item | Local path | Source | Provenance status | Unit convention | Benchmark role |
| :-- | :-- | :-- | :-- | :-- | :-- |
| SPARC working copy summary rows | `Data/03_Research/sparc_data.json` | SPARC-related repository working copy | `checked_local_reference`; upstream archival packaging still incomplete | `R_kpc` in kpc, `v_obs` in km/s, `M_disk_Msun` in solar masses, `R_disk_kpc` in kpc | primary verifier input for summary-row benchmark |
| LITTLE THINGS working copy summary rows | `Data/03_Research/little_things_data.json` | LITTLE THINGS-related repository working copy | `checked_local_reference`; source-lock cleanup still needed | `R_kpc` in kpc, `v_obs` in km/s, gas masses in solar masses | secondary benchmark/reference package |
| Topic bibliography | `Data/03_Research/references.bib` | topic-local references | supplementary only | n/a | citation support |

Repository facts:

- The current `sparc_data.json` checked into this repository contains `154` rows.
- The current verifier uses these rows as one-point-per-galaxy benchmark inputs,
  not as full radial curve arrays.
- The `galaxy_model_gate` emitted by the verifier treats these rows as an internal
  summary-row benchmark and blocks full SPARC or dark-matter replacement claims while
  source-lock, baseline, and residual gates remain open.
- Until upstream files, identifiers, and preprocessing are source-locked, this
  dataset must be described as a repository working copy rather than a fresh
  upstream archival mirror.
