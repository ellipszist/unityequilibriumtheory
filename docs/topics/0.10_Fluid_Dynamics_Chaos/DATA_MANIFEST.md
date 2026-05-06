# Data Manifest

| Item | Local path | Source | Provenance status |
|:--|:--|:--|:--|
| Canonical fluid reference | `docs/references.bib#reynolds_1883` | Reynolds 1883 | Citation-backed reference |
| Internal benchmark configs | Topic-local files under `Data/` | Repository-generated | Internal benchmark material |
| Benchmark outputs | Topic-local files under `Result/` | Repository-generated | Internal results only |
| Source-lock manifest | `Data/03_Research/source_lock_manifest.json` | Topic-derived provenance package | Hashed by primary verifier |

## Workflow Gate Files

| File | Role | Current status |
| :-- | :-- | :-- |
| `source_evidence_intake_stub.json` | provenance intake across internal benchmark, external CFD, and theorem branches | created by primary verifier |
| `source_evidence_readiness_matrix.json` | tracks review-readiness by branch | internal benchmark ready; external/theorem branches blocked |
| `branch_claim_gate.json` | lane-by-lane claim ceiling | 2 accepted internal branches, 3 blocked branches |

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
