# Data Manifest

| Item | Local path | Source | Provenance status |
|:--|:--|:--|:--|
| Canonical fluid reference | `docs/references.bib#reynolds_1883` | Reynolds 1883 | Citation-backed reference |
| Internal benchmark configs | Topic-local files under `Data/` | Repository-generated | Internal benchmark material |
| Benchmark outputs | Topic-local files under `Result/` | Repository-generated | Internal results only |

External-source audit status: `internal benchmark package`.

Priority remediation:

- Add at least one external CFD/turbulence validation dataset before treating this topic as
  externally data-grounded.
- Candidate sources: Johns Hopkins Turbulence Database, NASA CFD validation cases, and
  standard ERCOFTAC-style benchmark cases.
- Keep current internal speed/stability artifacts, but do not treat them as replacement for
  real fluid-observation or high-fidelity CFD benchmark data.
