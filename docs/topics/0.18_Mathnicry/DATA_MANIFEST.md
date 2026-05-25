# Data Manifest

Current data reality status: "manual or placeholder"

The current primary verifier is a surrogate mathematical demonstration and does not consume a real external theorem dataset. This manifest therefore records the current helper file honestly as a local script dependency rather than as scientific source data.

## Current Declared Input

| Item | Local path | Bytes | SHA256 | Source | Provenance status | Unit convention | Benchmark role |
| :-- | :-- | --: | :-- | :-- | :-- | :-- | :-- |
| `Download_Quantum_Data.py` | `Data/Download_Quantum_Data.py` | 3759 | `e4b82c0ea5093ff2d0042f3cada4f4074ade15399a01b5d6241b0b6f6108e07a` | Topic-local quantum/math helper script | Manual/placeholder; not an upstream dataset and not loaded by the current BSD verifier. | Not applicable; script/helper file. | Declared placeholder input in the current verification spec. |
| `Engine_Elliptic_Resonance.py` | `Code/01_Engine/Engine_Elliptic_Resonance.py` | 3153 | `7d4191f5457e5e2a40db7e0c86e8d83a0935f4525f53384d8defa24c5f180f6c` | Topic-local surrogate engine | Local code dependency; not mathematical source data. | Dimensionless local surrogate potential and parity rank indicator. | Loaded by the primary verifier; controls current BSD surrogate behavior. |
| `Research_BSD_Elliptic_Unity.py` | `Code/03_Research/Research_BSD_Elliptic_Unity.py` | 28863 | `93adaa987620e8418b4fefd14fa626f51e9261620966254be9abe51c4c2ca12c` | Topic-local verifier and fixture declaration | Local code dependency; not mathematical source data. | Two local curve fixtures with declared narrative roles. | Primary run-contract artifact generator. |
| `source_evidence_intake_stub.json` | `Data/source_evidence_intake_stub.json` | 5215 | `05dd0fbb8264466c227f9c4fe0d451dad7ca6780b0e7125486d3e9a3349150e6` | Topic-generated theorem-branch evidence intake sheet | Workflow control only; not source evidence by itself. | Mixed; each target declares its own expected convention. | Landing zone before data rewrites or claim upgrades. |
| `source_evidence_readiness_matrix.json` | `Data/source_evidence_readiness_matrix.json` | 3210 | `3384cb4f574defac4d7d03a4b61161cd8c5d48da144e52e84be07002a3c2a3eb` | Topic-generated readiness gate derived from the intake stub | Workflow control only; records completeness, not theorem validation. | Not applicable. | Tracks which theorem branches still lack benchmark evidence fields. |
| `branch_claim_gate.json` | `Data/branch_claim_gate.json` | 2112 | `2c4915963e4da54d7665b1ddf9ca6d18b0db712a47419741c505d2fd4c76fa5d` | Topic-generated claim gate for theorem-inspired branches | Workflow control only; cannot raise claim strength beyond the current run contract. | Not applicable. | Separates BSD, Riemann, Grover/P-vs-NP, Collatz, quantum, and topology claim ceilings. |
| `theorem_boundary_gate.json` | `Data/theorem_boundary_gate.json` | 3835 | `3a599b8a7ac4a69394145500475dd421080c1b4df80650622f9c50a793d985ec` | Topic-generated theorem export gate | Workflow control only; records which theorem-style exports are blocked. | Not applicable. | Allows only surrogate BSD run-contract export while blocking BSD/Riemann/P-vs-NP/Collatz/quantum theorem claims. |
| `data_posture_gate.json` | `Data/data_posture_gate.json` | 3084 | `ba1242b7458bed5e6a80b0cd35ad7c8ea236502c4a92c793c659857a42018e5b` | Topic-generated data-posture gate for theorem-inspired branches | Workflow control only; states that the current primary verifier is `SURROGATE_ONLY`. | Dimensionless local surrogate outputs; integer curve fixture coefficients. | Blocks proof/theorem/external-validation wording until source-backed theorem benchmark packages exist. |
| `surrogate_run_contract_gate` | embedded in `Result/artifacts/0_18_mathnicry_verification.json` | generated | generated | Verifier-generated gate for local BSD surrogate fixtures | Workflow/code-path gate only; not theorem evidence. | Dimensionless local surrogate output and mismatch count. | Separates local surrogate execution from blocked BSD/L-function/formal-proof claims. |

## Data Posture Gate

The primary verifier emits `Data/data_posture_gate.json` and embeds its identity in
`Result/artifacts/0_18_mathnicry_verification.json`.

Current controller status:

- `data_reality_status`: `manual_or_placeholder`
- `controller_status`: `SURROGATE_ONLY`
- `primary_verifier_input_class`: `local_code_fixture_package`

This is intentional, not a hidden failure. The gate preserves a narrow export:
the local BSD-style surrogate script ran and reported its mismatch count. It
blocks theorem-level, proof-level, and external-validation wording until a real
benchmark/source package exists.

## Current Surrogate Fixture Package

The current BSD lane is a local fixture package, not an external theorem dataset:

| Fixture | Curve | Declared role | Current surrogate basis | Claim boundary |
| :-- | :-- | :-- | :-- | :-- |
| Curve A | `y^2 = x^3 + x + 1` | rank-0 narrative candidate | local parity rule `(a+b)%2` plus surrogate `Omega(s)` | diagnostic only; not an elliptic-curve rank computation |
| Curve B | `y^2 = x^3 + 2x + 4` | rank-1+ narrative candidate | local parity rule `(a+b)%2` plus surrogate `Omega(s)` | diagnostic only; not an L-function order-of-vanishing computation |

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
