# Verification Spec

## Primary command

```powershell
python docs/topics/0.9_Quantum_Nonlocality/Code/03_Research/Research_CHSH_Verification.py
```

## Inputs

| Input | Role |
| :-- | :-- |
| `Data/03_Research/bell_test_2015.json` | primary Hensen et al. CHSH working copy with DOI |
| `Data/03_Research/bell_inequality_data.json` | secondary summary of the same benchmark |
| `Data/03_Research/source_lock_manifest.json` | normative provenance map for CHSH branch inputs |
| `docs/data/external/quantum_nonlocality/hensen_2015_chsh_reference_package.json` | extracted/source-referenced external package for the primary CHSH benchmark |
| `docs/data/external/quantum_nonlocality/bell_inequality_summary_reference_package.json` | extracted/source-referenced external package for the secondary Bell summary |

## Metrics

| Metric | Meaning | Threshold |
| :-- | :-- | :-- |
| `S_value` | recorded CHSH parameter | must exceed `2.0` |
| `lower_1sigma` | `S_value - S_error` | must exceed `2.0` |
| `p_value` | recorded statistical p-value | `< 0.05` |
| `tsirelson_rounding_gap` | `abs(qm_max - 2*sqrt(2))` | `<= 0.001` |
| DOI presence | primary source identifier | required |

## Artifact target

`Result/artifacts/0_9_quantum_nonlocality_verification.json`

The artifact must include command, environment, input hashes, DOI/source fields,
formula IDs, thresholds, checks, metrics, blockers, limitations, and the
workflow-gate summaries below.

## Required workflow gates

The primary verifier must also generate and hash:

- `Data/03_Research/source_evidence_intake_stub.json`
- `Data/03_Research/source_evidence_readiness_matrix.json`
- `Data/03_Research/branch_claim_gate.json`

These files do not change the CHSH result by themselves. They define what source
evidence is still missing and which adjacent branches remain blocked.

## Interpretation

- `PASS`: the source-referenced CHSH benchmark violates the local-realist bound,
  clears the p-value gate, and is consistent with the Tsirelson benchmark.
- The extracted external packages are provenance anchors only; they do not mean
  raw Bell event counts are archived yet.
- `WARN`: benchmark is computable but a provenance/statistical/rounding gate is
  incomplete.
- `FAIL`: required CHSH fields cannot be parsed or the benchmark does not clear
  the local-realist gate.

This verifier does not derive UET nonlocality, topological information filaments,
qubit relaxation, double-slit interference, tunneling, or LC-unity claims.
