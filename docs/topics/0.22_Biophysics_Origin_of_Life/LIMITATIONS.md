# Limitations

- The root baseline comparison is present, but numeric acceptance boundaries are still provisional until a saved artifact is generated and reviewed.
- Current data posture is source-referenced working copies plus a synthetic primary verifier, which is below a fully normalized archival biomedical dataset package.
- The topic title currently outruns the checked-in data package, which is still proxy-heavy and under-normalized.
- The primary verifier is a seeded synthetic biomarker diagnostic; it does not validate clinical biomarkers, TCGA claims, or origin-of-life mechanisms.
- CHB-MIT, Bonn-style EEG, and TCGA/GDC source records are pinned under `docs/data/external/...`, but they are not equally mature: CHB-MIT is review-ready for the current summary package, Bonn is still missing license and source sampling-rate metadata, and TCGA still lacks a real cohort/assay matrix.
- `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `subclaim_gate.json` are workflow controls only. They do not count as biomedical evidence, clinical validation, or origin-of-life proof.
- `biophysics_claim_scope_gate` is the artifact export controller. It allows only synthetic diagnostic/source-governance wording and blocks origin-of-life, clinical, EEG, TCGA, protein-folding, and theory-closure phrases while the current lanes remain open.
- Cancer/TCGA scripts currently include mock matrices and must not be described as real omics validation.
- Protocell and protein-folding scripts are exploratory simulations with open source/benchmark anchors.
- Internal script execution does not by itself establish external replication, formal proof, or broad physical closure.

## Current Claim Boundary

| Claim area | Allowed wording now | Blocker to stronger wording |
|:--|:--|:--|
| Biophysical complexity | exploratory proxy framework | Source-specific unit contracts and sub-verifiers. |
| Origin of life | hypothesis/simulation sandbox | Real chemistry/reaction-network data and entropy ledger. |
| Neural seizure | source-labeled EEG reference plus model sandbox | Raw windows, preprocessing, classifier metrics, held-out records. |
| Biomarker/cancer | synthetic diagnostic path | Real omics matrix, cohort/assay identity, and clinical/statistical baseline. |
| Protein folding | HP-model sandbox | Known benchmark optimum, deterministic search, artifact. |
