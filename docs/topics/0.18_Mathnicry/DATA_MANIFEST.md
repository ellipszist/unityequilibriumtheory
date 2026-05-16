# Data Manifest

Current data reality status: "manual or placeholder"

The current primary verifier is a surrogate mathematical demonstration and does not consume a real external theorem dataset. This manifest therefore records the current helper file honestly as a local script dependency rather than as scientific source data.

## Current Declared Input

| Item | Local path | Bytes | SHA256 | Source | Provenance status | Unit convention | Benchmark role |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- |
| `Download_Quantum_Data.py` | `Data/Download_Quantum_Data.py` | 3759 | `e4b82c0ea5093ff2d0042f3cada4f4074ade15399a01b5d6241b0b6f6108e07a` | Topic-local quantum/math helper script | Manual/placeholder; not an upstream dataset and not loaded by the current BSD verifier. | Not applicable; script/helper file. | Declared placeholder input in the current verification spec. |
| `source_evidence_intake_stub.json` | `Data/source_evidence_intake_stub.json` | generated | generated | Topic-generated theorem-branch evidence intake sheet | Workflow control only; not source evidence by itself. | Mixed; each target declares its own expected convention. | Landing zone before data rewrites or claim upgrades. |
| `source_evidence_readiness_matrix.json` | `Data/source_evidence_readiness_matrix.json` | generated | generated | Topic-generated readiness gate derived from the intake stub | Workflow control only; records completeness, not theorem validation. | Not applicable. | Tracks which theorem branches still lack benchmark evidence fields. |
| `branch_claim_gate.json` | `Data/branch_claim_gate.json` | generated | generated | Topic-generated claim gate for theorem-inspired branches | Workflow control only; cannot raise claim strength beyond the current run contract. | Not applicable. | Separates BSD, Riemann, Grover/P-vs-NP, Collatz, quantum, and topology claim ceilings. |
| `theorem_boundary_gate.json` | `Data/theorem_boundary_gate.json` | generated | generated | Topic-generated theorem export gate | Workflow control only; records which theorem-style exports are blocked. | Not applicable. | Allows only surrogate BSD run-contract export while blocking BSD/Riemann/P-vs-NP/Collatz/quantum theorem claims. |

## Missing Provenance for Theorem Branches

- BSD branch: no source-backed elliptic-curve rank table or L-function values are present.
- Riemann branch: known zeros are supplied dynamically by `mpmath.zetazero`; no local zero table, precision manifest, or source version is recorded.
- P-vs-NP/Grover branch: no NP-complete benchmark suite or formal reduction dataset is present.
- Collatz branch: no bounded search manifest, seed/range declaration, or counterexample policy is present.
- Quantum-logic branch: no deterministic gate-test fixture package is present.

## Repository Note

- Future raw/source datasets or benchmark tables should be stored under `docs/data/external/math/...` or `docs/data/external/quantum/...` when shared across topics.
- Topic-specific generated tables or bounded-search outputs should stay under `docs/topics/0.18_Mathnicry/Data/...`.
- A theorem branch cannot be promoted by adding data alone; it also needs a formal theorem target, assumptions, proof status, and artifact with failure modes.
