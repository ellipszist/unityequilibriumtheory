# Data Manifest

| Item | Local path | Bytes | SHA-256 | Source | Provenance status |
|:--|:--|--:|:--|:--|:--|
| Planck 2018 reference values | `docs/data/external/cosmology/hubble_tension/planck_2018/source_record.json` | 1236 | `501576dcff9ce7d421b417461800166d952e65f56de2500b53e14bc24f53721e` | Planck Collaboration, DOI `10.1051/0004-6361/201833910` | Source-locked scalar H0 value |
| SH0ES 2022 reference values | `docs/data/external/cosmology/hubble_tension/shoes_2022/source_record.json` | 1183 | `4bec055ed73b8b3ee6830c0908520148b6d6c40829fb6d7073111b328782d047` | Riess et al. 2022, DOI `10.3847/2041-8213/ac5c5b` | Source-locked scalar H0 value |
| Fine-structure constant | `docs/data/external/constants/codata/fine_structure/source_record.json` | 1213 | `880b37d2214778a624ada9c35c581c357e753cf3d6bf33ade03d62525063f8bd` | NIST/CODATA inverse fine-structure constant | Source-locked constant record; repository value is truncated |
| Hubble source-lock manifest | `Data/03_Research/source_lock_manifest.json` | 1930 | `134cf5b7e584a2764ce8409636dc7c582676bdba16723a7632a32a8736fc891a` | Topic-derived provenance package | Primary verifier hashes this manifest and source records |
| JWST high-z calibration file | `Data/03_Research/jwst_highz_calibration.csv` | 292 | `38104d06fc6ba2a290a81a13a8e571fc0569ec3fd1ce9e841b2795130dd191dc` | Topic-local working data | Needs a fuller provenance note before external release |

## Workflow Gate Files

| File | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `source_evidence_intake_stub.json` | 2226 | `8c5552bd0bdf7f8f777b8477b53127a15cb275674b1db42cc2684efd62ff366d` | provenance intake across scalar H0, bridge, high-z, and dark-energy branches | created by primary verifier |
| `source_evidence_readiness_matrix.json` | 2835 | `81a7082a8d62c033de6be2c4d99def36ac6354ebc5b3da9d683154fe62627105` | tracks branch review-readiness | scalar H0 ready; bridge/high-z/dark-energy/full-likelihood still blocked |
| `branch_claim_gate.json` | 2059 | `0ef1b364dc6b07d9a97a312a418e538033b91919b113d8ad43b0729d11175af9` | lane-by-lane claim ceiling | 1 accepted branch, 1 diagnostic/provisional branch, 3 blocked branches |

## Result Artifact

| Artifact | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `Result/artifacts/hubble_comparison_validation.json` | 10565 | `ec902f3709b7c6feb5c1d7f9be5b1057ed2a06620be245ee54a0f36b5e3e1e46` | primary scalar H0 comparison artifact | `PASS` for scalar benchmark only; controller remains `SCALAR_H0_BENCHMARK_ONLY` |

## Unit and benchmark roles

| Dataset / constant | Unit convention | Benchmark role |
| :-- | :-- | :-- |
| Planck H0 | `km s^-1 Mpc^-1` | early/CMB H0 baseline |
| SH0ES H0 | `km s^-1 Mpc^-1` | late/local H0 comparator |
| `alpha_em` | dimensionless | no-fit bridge constant for `beta_frame = sqrt(alpha_em)` |
| JWST high-z calibration | mixed topic-local columns | future high-z diagnostic only |

Repository note:

- The current structured topic pass focuses on explicit citation and local-path tracking.
- Full observational packaging remains future work.
- The current primary verifier uses scalar published H0 values, not full Planck chains,
  SH0ES covariance tables, BAO data, or SN likelihoods.
