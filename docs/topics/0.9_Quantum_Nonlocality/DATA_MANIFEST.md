# Data Manifest

Current data reality status: `real source referenced`

The topic now has extracted/source-referenced Bell benchmark packages under
`docs/data/external/quantum_nonlocality/...` plus a topic-level
`source_lock_manifest.json`. It still lacks a raw Bell event-count or
supplementary-table archive, so it remains below `manifested real dataset`.

## Primary Inputs

| Dataset | Local path | Source | Unit convention | Bytes | SHA-256 | Benchmark role | Provenance status |
| :-- | :-- | :-- | :-- | --: | :-- | :-- | :-- |
| Hensen 2015 Bell test | `Data/03_Research/bell_test_2015.json` | Hensen et al. 2015, DOI `10.1038/nature15759` | dimensionless CHSH `S`, error, p-value | 264 | `7b0088a3e30c039fd7d605c6a7182c3d1589ca1367f6b58adda4d00fdee3acc6` | primary CHSH verifier input | DOI recorded; raw counts not included |
| Hensen 2015 article PDF archive | `Ref/PDF_Downloads/Quantum_Hensen2015_Bell.pdf` | Hensen et al. 2015, DOI `10.1038/nature15759` | article/PDF source record | 3,314,850 | `c4acd5fca880cdc64fd3273f6d80e0c7d3055954b4522f1aa89111891f212d06` | citation/provenance review for CHSH summary values | archived PDF only; not a raw event-count archive |
| Bell inequality summary | `Data/03_Research/bell_inequality_data.json` | Hensen et al. 2015 / local summary | dimensionless CHSH values and p-value | 456 | `8eadfad7a4251821da64ff7aeaeb23163c1563664477036b93e6a8c38cbc5ad6` | secondary consistency input | source text recorded; DOI absent in this file |
| Source-lock manifest | `Data/03_Research/source_lock_manifest.json` | topic-derived CHSH provenance map | inherits per-target unit conventions | 1,918 | `ab022ff4c2302f3dc56e7d23036c7e9cb10a91e1553ee4b7343c6f731f74079d` | normative provenance controller for CHSH branch inputs | source lock present; raw event-count reconstruction still open |
| Hensen 2015 reference package | `docs/data/external/quantum_nonlocality/hensen_2015_chsh_reference_package.json` | extracted/source-referenced package | dimensionless CHSH summary metrics | 1,466 | `70d0e7d850af1dc330aaae5aa5dcbbe7184951aba56a115a22e6b04c2f14e61b` | external provenance package for primary input | DOI locked; raw counts still missing |
| Bell summary reference package | `docs/data/external/quantum_nonlocality/bell_inequality_summary_reference_package.json` | extracted/source-referenced package | dimensionless CHSH summary metrics | 1,098 | `4e6217c13bbe631a77ccc9cf6a1ae5f09648f511e469ba7e2bbc7df598883ba3` | external provenance package for secondary input | DOI locked through reference package |
| Research_CHSH_Verification.py | `Code/03_Research/Research_CHSH_Verification.py` | topic verifier | n/a | 24,816 | `d1cc468346b3d9cb36ae25a74c277970d530c05b17979f484aad3a4dbcd6f552` | regenerates CHSH summary benchmark and claim-scope artifact | executable verifier; does not close raw-event reconstruction or UET-mechanism gates |
| 0_9_quantum_nonlocality_verification.json | `Result/artifacts/0_9_quantum_nonlocality_verification.json` | verifier-generated artifact | n/a | 9,992 | `87eeb233690e471faec1285dff989f6d375054aaa6c8582803a21a4a1447fc45` | machine-readable CHSH benchmark and claim boundary | PASS applies only to the CHSH summary benchmark; raw-event and mechanism gates remain open/blocked |

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

The artifact now embeds `chsh_evidence_gate`, which keeps the passing CHSH
summary benchmark separate from raw-event reconstruction and UET-mechanism
claims:

- `summary_benchmark_gate`: may pass for the recorded CHSH summary values.
- `raw_event_reconstruction_gate`: remains `OPEN` until event counts or
  supplementary tables are archived and reconstructed.
- `uet_mechanism_gate`: remains `BLOCKED` until a separate derivation and
  verifier connect the UET bridge to standard CHSH correlations.

## Workflow Gate Files

| File | Bytes | SHA-256 | Role | Current status |
| :-- | --: | :-- | :-- | :-- |
| `source_lock_manifest.json` | 1918 | `ab022ff4c2302f3dc56e7d23036c7e9cb10a91e1553ee4b7343c6f731f74079d` | normative provenance map for CHSH branch inputs | topic-level source lock |
| `source_evidence_intake_stub.json` | 5129 | `faca03161ed8f2957f3c77bd3f9023cd89123ca6db6274e2f618a5e835f842d2` | provenance intake queue for Bell and adjacent quantum lanes | created by verifier |
| `source_evidence_readiness_matrix.json` | 2060 | `3bc7345fba294417f6218431ea9fdb6da67c1ee1aaed550306e409bf45b933c1` | tracks which source targets are still incomplete | 2 ready for source review, 2 still blocked |
| `branch_claim_gate.json` | 1924 | `96e703a6fd676ea92954a95128783f18faac5d9585c2f5fb1b9f44a2ac1c71db` | caps claim strength by branch | only CHSH benchmark accepted now |

## Next Provenance Work

- Add raw event counts or source tables from the Hensen et al. analysis if
  licensing allows.
- Add DOI/URL/retrieval notes to every local Bell and qubit working copy.
- Keep the extracted external reference packages aligned with the topic-local
  CHSH working copies and update `source_lock_manifest.json` if the normative
  files change.
- Keep raw external sources under `docs/data/external/quantum_nonlocality/...`
  when fetched; keep topic-derived normalized inputs under this topic's `Data/`.
