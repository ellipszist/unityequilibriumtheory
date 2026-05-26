# Data Manifest

| Item | Local path | Bytes | SHA-256 | Source | Provenance status |
|:--|:--|--:|:--|:--|:--|
| Canonical fluid reference | `docs/references.bib#reynolds_1883` | n/a | n/a | Reynolds 1883 | Citation-backed reference |
| Source-lock manifest | `Data/03_Research/source_lock_manifest.json` | 1467 | `d65719d433e75fe2dd99ae9d37fcc9aedb7a3070dccaa1bbea54d103657ea17b` | Topic-derived provenance package | Hashed by primary verifier |
| Fluid properties config | `Data/03_Research/fluid_properties.json` | 456 | `35486e696b5f4de9b12bba22427a80bc2b52b1c6c818666ca3ba62083a07f947` | Repository-generated internal benchmark config | Internal benchmark material |
| Water properties config | `Data/03_Research/water_properties_20C.json` | 255 | `e655509dcdd69f29c8068649f4ba1a6937d7ad70d3e43bcd6157bb41e835f322` | Repository-generated internal benchmark config | Internal benchmark material |
| Air properties config | `Data/03_Research/air_properties_20C.json` | 255 | `b8fcf33a0c6be87d660adfd07b0f110588cba0a20425915fe6ba16b07cd33eee` | Repository-generated internal benchmark config | Internal benchmark material |
| Kolmogorov constants config | `Data/03_Research/kolmogorov_constants.json` | 306 | `6882eb8c6cc554c351e8cd4668c1618af215e02deb089cc0381abad79594bdbc` | Repository-generated internal benchmark config | Internal diagnostic material |
| Benchmark verifier script | `Code/03_Research/Verify_Fluid_Turbulence.py` | 1978 | `98fab4e5586b27847aa1e773853de5beb81c30a25acce9c29be0e32efe8ffe26` | Topic-local verifier | Generates primary internal benchmark artifact |
| Benchmark output artifact | `Result/artifacts/fluid_benchmark_validation.json` | 8482 | `ec0afa70860bb79dbcffe694c252d61d8104a185eff9b865545e2d45116d813d` | Repository-generated | Internal speed/stability benchmark only; controller remains `WARN` |

## Workflow Gate Files

| File | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `source_evidence_intake_stub.json` | 2246 | `842ae12732e2b720b1934396b3eea36ce733a6b99f2804e3d06681a34d443e13` | provenance intake across internal benchmark, external CFD, and theorem branches | created by primary verifier |
| `source_evidence_readiness_matrix.json` | 2874 | `9e6cb9544d0c8c38078ababeda7b03436c35f5f849635800d402df030773bbfb` | tracks review-readiness by branch | internal benchmark ready; external/theorem branches blocked |
| `branch_claim_gate.json` | 2051 | `8fb310883a9e42ae6d084c412e4d926013006e1a811d995927135df6d70068d3` | lane-by-lane claim ceiling | 2 accepted internal branches, 3 blocked branches |

External-source audit status: `internal benchmark package`.

Priority remediation:

- Add at least one external CFD/turbulence validation dataset before treating this topic as
  externally data-grounded.
- Candidate sources: Johns Hopkins Turbulence Database, NASA CFD validation cases, and
  standard ERCOFTAC-style benchmark cases.
- Keep current internal speed/stability artifacts, but do not treat them as replacement for
  real fluid-observation or high-fidelity CFD benchmark data.
- Current primary artifact now records the source-lock manifest hash, benchmark-script hash,
  and core master-equation hash.
