# Data Manifest

Current data reality status: `real source referenced`

The topic has usable local benchmark inputs, but not yet a fully archival upstream
provenance package. Claims must therefore remain below paper-ready status until
source URLs/DOIs, retrieval dates, preprocessing notes, and hashes are normalized.

## Primary Inputs

| Dataset | Local path | Source | Unit convention | Benchmark role | Provenance status |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Scaling-law constants | `Data/03_Research/scaling_laws.json` | Kaplan et al., "Scaling Laws for Neural Language Models", arXiv `2001.08361`, URL `https://arxiv.org/abs/2001.08361` | dimensionless exponents; parameters, tokens, PF-days | primary scaling-law reference | arXiv source and retrieval date pinned; exact table/equation extraction still needs review |
| GPT-3 scaling table | `Data/GPT3_Scaling_Laws.csv` | topic-local GPT-style scaling table | parameters, test loss, FLOPs | independent log-log fit diagnostic | working copy; table provenance not archival |
| Model architecture metadata | `Data/03_Research/deepseek_moe_data.json` | topic-local model metadata package | total/active parameters, context window, tokens | sparse-vs-dense active-fraction diagnostic | mixed: some entries are public-model metadata, some estimated/proprietary |
| Source-lock manifest | `Data/03_Research/source_lock_manifest.json` | topic-derived source-lock package for scaling, CSV fit, and model metadata lanes | inherits per-target unit conventions | binds working-copy data classes and claim boundary | present; improves provenance discipline but does not create upstream archival status by itself |
| Source evidence intake stub | `Data/03_Research/source_evidence_intake_stub.json` | topic-generated intake sheet for unresolved scaling/model source metadata | mixed; each target declares its own expected unit basis | landing zone before data rewrites or claim upgrades | workflow control only; not evidence by itself |
| Source evidence readiness matrix | `Data/03_Research/source_evidence_readiness_matrix.json` | topic-generated readiness gate derived from the intake stub | n/a | tracks completeness of provenance capture | current snapshot: all three targets are `partial`; none is source-review-ready yet |
| Model claim gate | `Data/03_Research/model_claim_gate.json` | topic-generated claim gate for benchmark versus exploratory lanes | n/a | controls allowed claim class per lane | workflow control only; cannot raise claim strength beyond the current internal benchmark |

## Secondary Inputs

| Dataset | Local path | Role | Limitation |
| :-- | :-- | :-- | :-- |
| Foundation notes | `Data/00_Foundation/foundation_basics.txt` | background notes for foundation-model concepts | not a numeric verifier input |
| Tiny Shakespeare | `Data/03_Research/tiny_shakespeare.txt` | possible toy language-model input | not used by the primary verifier |

## Hash Policy

The primary verifier records SHA-256 hashes for all primary inputs in
`Result/artifacts/0_24_artificial_intelligence_verification.json`.

## Next Provenance Work

- Review exact table/equation extraction for the scaling-law source package.
- Add construction date or upstream table lineage for `GPT3_Scaling_Laws.csv`.
- Add public model-card URLs and retrieval date for the architecture metadata package.
- Split public, estimated, and proprietary model metadata into separate tables.
- Move any raw external downloads to `docs/data/external/...`; keep derived
  topic-specific tables under `docs/topics/0.24_Artificial_Intelligence/Data/...`.
- Use `source_evidence_intake_stub.json` and `source_evidence_readiness_matrix.json`
  as the gate before editing working-copy data or upgrading claim language.

## Current Readiness Snapshot

- Scaling-law source package: `6/6` fields complete for source review; exact extraction review is still required before claim upgrades
- GPT-style scaling table provenance package: `5/6` fields complete; missing construction/retrieval date
- Model architecture metadata package: `4/6` fields complete; missing public model-card URLs and retrieval date
