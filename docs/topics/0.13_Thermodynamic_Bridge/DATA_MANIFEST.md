# Data Manifest

Current data reality status: "manual or placeholder"

External-source audit status: `embedded/local thermodynamics snapshots`.

Priority remediation:

- Source-lock Berut 2012 experimental Landauer-principle data or supplementary values.
- Add NIST/CODATA constants used by the thermodynamic bridge with version/date and uncertainty.
- Separate historical theoretical references from experimental datasets used in verification.
- See `docs/meta/core_data_external_source_audit.md` for the cross-topic data-hardening plan.

| Item | Local path | Source | Provenance status |
|:--|:--|:--|:--|
| __init__.py | `Data/03_Research/__init__.py` | Topic-local working copy or generated benchmark input | Manual, placeholder, or partially scripted data handling is still present. |
| berut_2012.json | `Data/03_Research/berut_2012.json` | Information-thermodynamics working copy | Manual, placeholder, or partially scripted data handling is still present. |
| cattaneo_data.json | `Data/03_Research/cattaneo_data.json` | Information-thermodynamics working copy | Manual, placeholder, or partially scripted data handling is still present. |
| experimental_data.py | `Data/03_Research/experimental_data.py` | Topic-local working copy or generated benchmark input | Manual, placeholder, or partially scripted data handling is still present. |

Repository note:

- This manifest was created during the repo standards pass and should be tightened further in a later provenance-normalization wave.
- Until upstream URLs, DOIs, preprocessing notes, and hashes are frozen, treat the dataset package as an internal working copy rather than an archival release.
