# Data Manifest

Current data reality status: "manual or placeholder"

External-source audit status: `mixed biomedical working data, not source locked`.

Priority remediation:

- Normalize the CHB-MIT/PhysioNet provenance if seizure/phase datasets remain part of this
  topic's verification.
- If the topic is about origin-of-life biophysics rather than EEG/seizure dynamics, split the
  biomedical dataset role from the origin-of-life mechanism role.
- Add source URL, license, patient/record identifiers, preprocessing, and local raw hash for
  any biomedical dataset used in verification.
- See `docs/meta/core_data_external_source_audit.md` for the cross-topic data-hardening plan.

| Item | Local path | Source | Provenance status |
|:--|:--|:--|:--|
| chb_mit_reference.json | `Data/03_Research/03_Research/chb_mit_reference.json` | Topic-local working copy or generated benchmark input | Manual, placeholder, or partially scripted data handling is still present. |
| chb01_summary.txt | `Data/03_Research/03_Research/chb01_summary.txt` | Topic-local working copy or generated benchmark input | Manual, placeholder, or partially scripted data handling is still present. |
| seizure_phase_data.json | `Data/03_Research/03_Research/seizure_phase_data.json` | Topic-local working copy or generated benchmark input | Manual, placeholder, or partially scripted data handling is still present. |
| chb_mit_reference.json | `Data/03_Research/chb_mit_reference.json` | Topic-local working copy or generated benchmark input | Manual, placeholder, or partially scripted data handling is still present. |

Repository note:

- This manifest was created during the repo standards pass and should be tightened further in a later provenance-normalization wave.
- Until upstream URLs, DOIs, preprocessing notes, and hashes are frozen, treat the dataset package as an internal working copy rather than an archival release.
