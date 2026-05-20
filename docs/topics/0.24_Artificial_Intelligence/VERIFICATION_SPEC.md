# Verification Spec

## Primary command

```powershell
python docs/topics/0.24_Artificial_Intelligence/Code/03_Research/Research_AI_Scaling_Audit.py
```

## Inputs

| Input | Role |
| :-- | :-- |
| `Data/03_Research/scaling_laws.json` | reference scaling exponents and critical scales |
| `Data/GPT3_Scaling_Laws.csv` | small topic-local table for an independent log-log exponent fit |
| `Data/03_Research/deepseek_moe_data.json` | dense/MoE architecture metadata for sparsity diagnostics |
| `Data/03_Research/source_lock_manifest.json` | binds benchmark lanes to explicit working-copy source classes and unit conventions |

## Generated workflow artifacts

- `Data/03_Research/source_lock_manifest.json`
- `Data/03_Research/source_evidence_intake_stub.json`
- `Data/03_Research/source_evidence_readiness_matrix.json`
- `Data/03_Research/model_claim_gate.json`

## Current readiness snapshot

- Scaling-law source package: `4/6` complete; missing DOI/arXiv/URL and retrieval date
- GPT-style scaling table package: `5/6` complete; missing construction/retrieval date
- Model architecture metadata package: `4/6` complete; missing public model-card URLs and retrieval date

## Metrics

| Metric | Meaning | Current threshold |
| :-- | :-- | :-- |
| `csv_alpha_delta` | absolute gap between CSV-fitted `alpha_fit` and stored `alpha_N` | `<= 0.20` provisional |
| `min_moe_active_fraction < min_dense_active_fraction` | sparse active-parameter check | required |
| `alpha_kappa_relative_delta` | gap between `alpha_N` and current `kappa_macro=0.1` proxy | `<= 0.25` for PASS; otherwise WARN |

## Artifact target

`Result/artifacts/0_24_artificial_intelligence_verification.json`

The artifact must include `status`, command, environment, formula IDs, input
hashes, thresholds, metrics, per-model sparsity rows, blockers, and limitations.
It must also include `ai_claim_scope_gate.controller_status`, blocked export
phrases, and machine-readable next blockers for integration dashboards.

## Interpretation

- `PASS`: local scaling table, sparsity check, and UET proxy check all clear the
  provisional thresholds.
- `WARN`: at least one scientific blocker remains, but the verifier ran and
  produced an inspectable artifact.
- `FAIL`: verifier cannot parse required inputs or a required check is structurally
  impossible to compute.

Current claims must remain limited to an internal scaling/sparsity benchmark. This
verifier does not prove AI alignment, ethics, consciousness, or universal
intelligence dynamics.
Treat `ai_claim_scope_gate` as the export controller for `0.0` and paper-facing
summaries.
