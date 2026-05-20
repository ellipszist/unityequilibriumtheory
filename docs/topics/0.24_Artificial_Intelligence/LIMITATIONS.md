# Limitations

- Current evidence supports only an internal scaling/sparsity benchmark.
- The `alpha_N ~= kappa_macro` bridge is a heuristic and currently remains a
  blocker for UET constant-identification claims.
- The scaling-law and model metadata tables are topic-local working copies; they
  still need upstream URL/DOI/arXiv, retrieval date, preprocessing notes, and
  source separation for estimated values.
- Provenance is now partially normalized but still incomplete: the scaling-law package is missing DOI/arXiv/URL and retrieval date, the GPT-style table is missing its construction date, and the architecture package is missing public model-card URLs and retrieval date.
- `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`,
  `source_lock_manifest.json`, and `model_claim_gate.json` are workflow controls only. They do not count as
  upstream evidence, derivation, or validation of AI-law claims.
- `ai_claim_scope_gate` is the artifact export controller. It allows only internal scaling/sparsity benchmark wording and blocks alignment, ethics, consciousness, universal-intelligence, alpha-kappa-law, and MoE-performance phrases while current blockers remain open.
- MoE active-parameter fraction is an architecture diagnostic, not a complete
  efficiency, quality, safety, or alignment metric.
- `Research_AI_Detective_V2.py` uses galaxy data from `0.1` and cannot be treated
  as a direct AI verifier.
- No artifact currently validates ethics as a physical law, alignment convergence,
  consciousness, or developmental-AI claims.
- Any README or paper-facing claim must cite the exact artifact, formula ID, and
  dataset row used; otherwise it remains exploratory.
