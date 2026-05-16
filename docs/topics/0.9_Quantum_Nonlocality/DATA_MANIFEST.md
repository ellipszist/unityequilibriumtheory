# Data Manifest

Current data reality status: `real source referenced`

The topic now has extracted/source-referenced Bell benchmark packages under
`docs/data/external/quantum_nonlocality/...` plus a topic-level
`source_lock_manifest.json`. It still lacks a raw Bell event-count or
supplementary-table archive, so it remains below `manifested real dataset`.

## Primary Inputs

| Dataset | Local path | Source | Unit convention | Benchmark role | Provenance status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Hensen 2015 Bell test | `Data/03_Research/bell_test_2015.json` | Hensen et al. 2015, DOI `10.1038/nature15759` | dimensionless CHSH `S`, error, p-value | primary CHSH verifier input | DOI recorded; raw counts not included |
| Hensen 2015 article PDF archive | `Ref/PDF_Downloads/Quantum_Hensen2015_Bell.pdf` | Hensen et al. 2015, DOI `10.1038/nature15759` | article/PDF source record; SHA-256 `c4acd5fca880cdc64fd3273f6d80e0c7d3055954b4522f1aa89111891f212d06` | citation/provenance review for CHSH summary values | archived PDF only; not a raw event-count archive |
| Bell inequality summary | `Data/03_Research/bell_inequality_data.json` | Hensen et al. 2015 / local summary | dimensionless CHSH values and p-value | secondary consistency input | source text recorded; DOI absent in this file |
| Hensen 2015 reference package | `docs/data/external/quantum_nonlocality/hensen_2015_chsh_reference_package.json` | extracted/source-referenced package | dimensionless CHSH summary metrics | external provenance package for primary input | DOI locked; raw counts still missing |
| Bell summary reference package | `docs/data/external/quantum_nonlocality/bell_inequality_summary_reference_package.json` | extracted/source-referenced package | dimensionless CHSH summary metrics | external provenance package for secondary input | DOI locked through reference package |

## Secondary Inputs

| Dataset | Local path | Role | Limitation |
| :-- | :-- | :-- | :-- |
| Bell test data module | `Data/03_Research/bell_test_data.py` | legacy local data helper | not used by primary verifier |
| Double-slit C60 | `Data/03_Research/double_slit_c60.json` | interference lane | not evidence for CHSH nonlocality |
| Qubit/tunneling files | `Data/03_Research/*qubit*`, `*tunnel*` | future lanes | require separate manifests and verifiers |

## Hash Policy

The primary verifier records SHA-256 hashes for the primary input files in
`Result/artifacts/0_9_quantum_nonlocality_verification.json`. It also records
hashes for the workflow gate files:

- `Data/03_Research/source_evidence_intake_stub.json`
- `Data/03_Research/source_evidence_readiness_matrix.json`
- `Data/03_Research/branch_claim_gate.json`

The verifier also records the local Hensen article PDF archive hash. This closes
article-level provenance for the benchmark citation, but it does not close the
raw Bell event-count blocker.

## Workflow Gate Files

| File | Role | Current status |
| :-- | :-- | :-- |
| `source_lock_manifest.json` | normative provenance map for CHSH branch inputs | topic-level source lock |
| `source_evidence_intake_stub.json` | provenance intake queue for Bell and adjacent quantum lanes | created by verifier |
| `source_evidence_readiness_matrix.json` | tracks which source targets are still incomplete | all current targets pending |
| `branch_claim_gate.json` | caps claim strength by branch | only CHSH benchmark accepted now |

## Next Provenance Work

- Add raw event counts or source tables from the Hensen et al. analysis if
  licensing allows.
- Add DOI/URL/retrieval notes to every local Bell and qubit working copy.
- Keep the extracted external reference packages aligned with the topic-local
  CHSH working copies and update `source_lock_manifest.json` if the normative
  files change.
- Keep raw external sources under `docs/data/external/quantum_nonlocality/...`
  when fetched; keep topic-derived normalized inputs under this topic's `Data/`.
