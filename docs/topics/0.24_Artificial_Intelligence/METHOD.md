# Method

## Problem Target

This topic tests whether selected AI scaling and architecture-efficiency
quantities can be represented in a UET-style information framework. The current
hardening pass targets measurable scaling and sparsity diagnostics first.

## Evidence Lanes

| Lane | Files | Current role |
| :-- | :-- | :-- |
| Scaling-law benchmark | `scaling_laws.json`, `GPT3_Scaling_Laws.csv`, `source_lock_manifest.json`, `Research_AI_Scaling_Audit.py` | primary verifier lane |
| Sparse architecture diagnostic | `deepseek_moe_data.json`, `source_lock_manifest.json`, `UET_AI_Core.py`, `Research_AI_Scaling_Audit.py` | primary verifier lane |
| Source evidence workflow | `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, `source_lock_manifest.json` | provenance gate before data or claim upgrades |
| Entropy-learning engine | `UET_AI_Core.py` | implemented but not benchmark-validated |
| AI detective/cross-topic reasoning | `Research_AI_Detective_V2.py` | excluded from primary claim; depends on 0.1 galaxy data |
| Alignment/ethics simulation | `Research_Alignment_Equilibrium.py`, `model_claim_gate.json` | future exploratory lane |
| Consciousness/developmental AI | `Research_Consciousness.py`, `Code/05_Developmental_AI/`, `model_claim_gate.json` | future exploratory lane |

## Variables

| Symbol / field | Meaning | Unit |
| :-- | :-- | :-- |
| `L` | test-loss proxy | dimensionless |
| `N` | parameter count | count |
| `D` | training tokens | count |
| `C` | compute | PF-days or FLOP-derived proxy |
| `alpha_N`, `alpha_D`, `alpha_C` | scaling exponents | dimensionless |
| `kappa_macro` | current UET macro proxy used for comparison | dimensionless |
| `active_fraction` | active parameters divided by total parameters | dimensionless |

## Procedure

1. Load topic-local scaling-law constants and model metadata.
2. Fit a simple log-log exponent from `GPT3_Scaling_Laws.csv`.
3. Compare the fitted exponent with stored `alpha_N`.
4. Compare MoE active fractions with dense active fractions.
5. Check whether the current `kappa_macro=0.1` proxy is close enough to `alpha_N`
   to support a constant-identification claim.
6. Regenerate source-lock, source-evidence, and model-claim workflow files.
7. Write a machine-readable artifact with hashes, metrics, thresholds, blockers,
   and limitations.

## Domain of Validity

The current method applies only to the topic-local scaling/sparsity benchmark
package. It is not a proof of AI alignment, ethics, consciousness, or a general
physical law of intelligence.

## Dependency Policy

`Research_AI_Detective_V2.py` depends on topic `0.1` galaxy data and must not be
used as the primary evidence for topic `0.24` until it is explicitly modeled as a
cross-topic dependency artifact.

## Claim Workflow

1. Run `Research_AI_Scaling_Audit.py` to regenerate the artifact and workflow files.
2. Read `source_lock_manifest.json` as the normative map of which AI benchmark files are source-referenced working copies, topic-local tables, or mixed public/estimated metadata.
3. Fill `source_evidence_intake_stub.json` only with real upstream scaling/model metadata.
4. Use `source_evidence_readiness_matrix.json` as the provenance gate before changing working-copy data or claim class.
5. Check `model_claim_gate.json` before treating heuristic or exploratory lanes as evidence.

## Current provenance gate state

- Scaling-law source package: partial (`4/6` fields complete)
- GPT-style scaling table package: partial (`5/6` fields complete)
- Model architecture metadata package: partial (`4/6` fields complete)
- No lane is source-review-ready yet, but none is an unlabeled blank placeholder anymore
