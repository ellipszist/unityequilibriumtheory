# Data Manifest

Current data reality status: "real source referenced with synthetic primary verifier"

External-source audit status: `CHB-MIT/Bonn/TCGA source records pinned; raw biomedical files and preprocessing still open`.

Priority remediation:

- Normalize CHB-MIT/PhysioNet provenance if seizure/phase datasets remain part of verification.
- Split biomedical EEG, cancer/omics, protein-folding, and origin-of-life chemistry roles instead of treating them as one evidence source.
- Add source URL, license, patient/record identifiers, preprocessing, and local raw hash for any biomedical dataset used in verification.
- Keep synthetic biomarker and mock TCGA data labeled as synthetic until replaced by real source-backed inputs.

| Item | Local path | Source | Unit convention | SHA-256 | Benchmark role | Provenance status |
|:--|:--|:--|:--|:--|:--|:--|
| Source-lock manifest | `data/03_Research/source_lock_manifest.json` | Topic-derived source-lock package | n/a | `3f3ff951d8b259907b75635637d9edca3bbc73860ce18e97a0626465d28738c0` | Binds local EEG summaries/samples and synthetic verifier role to source records | Present; upgrades provenance but not claim class. |
| CHB-MIT source record | `docs/data/external/biophysics/eeg/chb_mit/source_record.json` | PhysioNet CHB-MIT v1.0.0, DOI `10.13026/C2K01R` | Hz and seconds; raw EDF signal units if archived later | `a3755e46d1d58c4fa720574d83a30ee2ff1511a510b79d09472beb533a4360ad` | Future real EEG seizure-window verifier source | Source record present; raw EDF files and exact windows not stored. |
| Bonn EEG source record | `docs/data/external/biophysics/eeg/bonn/source_record.json` | Bonn-style EEG benchmark target; reference DOI `10.1103/PhysRevE.64.061907` | amplitude samples by index; sampling rate still open | `cceee6f66f3788a522562c206c85299b60406c00341e10a9c7b298f40b0e0410` | Future neural-Omega verifier source | Partial source target; official package URL/license/subset identity still open. |
| TCGA/GDC source record | `docs/data/external/biophysics/omics/tcga/source_record.json` | NCI Genomic Data Commons / TCGA portal | expression units must be declared by assay if data are added | `5bf1b5af16b8f33f7e0e8806d4e9d740bae509659c251f313183e051eeea586c` | Future cancer/omics entropy verifier source | Source target only; no real TCGA matrix stored. |
| CHB-MIT reference | `data/03_Research/chb_mit_reference.json` | CHB-MIT Scalp EEG Database, DOI `10.13026/C2K01R`, URL `https://physionet.org/content/chbmit/1.0.0/` | sampling rate Hz, channel count, seizure times seconds | `bec00ad1162ba67fd29f3190ba0ad8eb76523afad09154aa6ee58e0a155ed5d5` | EEG provenance reference | Source-labeled summary; raw EDF files not stored. |
| CHB01 summary | `data/03_Research/chb01_summary.txt` | Topic-local CHB01 summary | seconds/record notes as text | `6a426dc080d337fcd95c00e247133e4ebac38ff3c30dee5988ed2005833fb34f` | EEG notes/reference | Local summary; preprocessing chain open. |
| Seizure phase data | `data/03_Research/seizure_phase_data.json` | Derived local summary from CHB-MIT | band-power fractions, synchrony index, variance proxy | `9a444d0e275e5e977bf7aed40ce56d0a8b17027778d3dfa39344da0209f2a0dd` | Seizure phase reference | Derived working copy; raw window IDs/hashes open. |
| Bonn EEG healthy sample | `data/Bonn_EEG/Z.txt` | Bonn EEG-style local text sample | amplitude samples, normalized in engine at runtime | `f06e7a3f5c327ca5add4731f5179ee98146acc0564e9a334b3c92b10fb2a4d55` | Neural Omega engine input | Local text copy; upstream source/license open. |
| Bonn EEG seizure sample | `data/Bonn_EEG/S.txt` | Bonn EEG-style local text sample | amplitude samples, normalized in engine at runtime | `46782824ac34e3ce6e851294fbf15d9f86a5792a5ed6830504b81b3e511f8bd3` | Neural Omega engine input | Local text copy; upstream source/license open. |
| Synthetic biomarker matrix | generated in `Code/03_Research/Research_Biomarker_Identification.py` | Seeded synthetic positive controls | arbitrary expression units; variance/stability dimensionless | generated per run, seed recorded in artifact | Primary verifier diagnostic | Not external biomedical data. |

## Path Cleanup Note

Older manifests and wrapper artifacts referenced `Data/03_Research/...` and duplicated `03_Research/03_Research/...` paths. The repository files are under lowercase `data/`. New verifier artifacts record the lowercase path used by the current code.

## External Source Targets

| Source target | Required storage path | Current status |
|:--|:--|:--|
| CHB-MIT raw EDF records and exact seizure windows | `docs/data/external/biophysics/eeg/chb_mit/` | Source record stored; raw external files/window hashes not stored. |
| Bonn EEG source package and license | `docs/data/external/biophysics/eeg/bonn/` | Partial source record stored; official package URL/license/subset identity still open. |
| TCGA/omics matrix for cancer entropy work | `docs/data/external/biophysics/omics/tcga/` | Source target stored; no real matrix present; current TCGA script uses mock data. |
| HP protein-folding benchmark sequence/optimum | `docs/data/external/biophysics/protein_hp/` | Not present; current sequence is topic-local. |
| Prebiotic/protocell chemistry yields | `docs/data/external/biophysics/prebiotic/` | Not present or not connected to current verifier. |

Repository note:

- Until raw files, license terms, preprocessing notes, exact record/window identifiers, and raw hashes are frozen, treat the dataset package as source-referenced working copies plus a synthetic primary verifier rather than an archival biomedical release.
