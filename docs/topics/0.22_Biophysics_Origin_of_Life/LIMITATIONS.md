# Limitations

- The root baseline comparison is present, but numeric acceptance boundaries are still provisional until a saved artifact is generated and reviewed.
- Current data posture is source-referenced working copies plus a synthetic primary verifier, which is below a fully normalized archival biomedical dataset package.
- The topic title currently outruns the checked-in data package, which is still proxy-heavy and under-normalized.
- The primary verifier is a seeded synthetic biomarker diagnostic; it does not validate clinical biomarkers, TCGA claims, or origin-of-life mechanisms.
- CHB-MIT, Bonn-style EEG, and TCGA/GDC source records are pinned under `docs/data/external/...`, but raw EEG files, official Bonn package metadata, real omics matrices, preprocessing, and exact record/window hashes remain open.
- Cancer/TCGA scripts currently include mock matrices and must not be described as real omics validation.
- Protocell and protein-folding scripts are exploratory simulations with open source/benchmark anchors.
- Internal script execution does not by itself establish external replication, formal proof, or broad physical closure.

## Current Claim Boundary

| Claim area | Allowed wording now | Blocker to stronger wording |
|:--|:--|:--|
| Biophysical complexity | exploratory proxy framework | Source-specific unit contracts and sub-verifiers. |
| Origin of life | hypothesis/simulation sandbox | Real chemistry/reaction-network data and entropy ledger. |
| Neural seizure | source-labeled EEG reference plus model sandbox | Raw windows, preprocessing, classifier metrics, held-out records. |
| Biomarker/cancer | synthetic diagnostic path | Real omics matrix and clinical/statistical baseline. |
| Protein folding | HP-model sandbox | Known benchmark optimum, deterministic search, artifact. |
