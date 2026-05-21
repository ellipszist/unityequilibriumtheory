# Topic 0.18: Quantum Computing & Circuits - Results

> [!WARNING]
> **Result claim boundary:** This directory contains legacy simulation outputs
> and topic-local surrogate artifacts. It is not theorem evidence, external
> quantum validation, proof-level mathematics, or a P-vs-NP/Riemann/Collatz/BSD
> solution. Current allowed claims are controlled by `README.md`,
> `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `DATA_MANIFEST.md`, and
> `Result/artifacts/0_18_mathnicry_verification.json`.

This directory contains generated outputs from earlier simulation scripts. The
files mirror parts of the `Code/` structure and can support only internal
diagnostic or run-contract review unless a current verifier artifact explicitly
raises the claim class.

---

## 🏛️ Result Architecture (Unified Structure)

| Sub-directory | Content | Verification |
| :--- | :--- | :--- |
| **01_Engine/** | Manifold Resonance Profiles | Energy Stability Checks |
| **02_Proof/** | Fidelity & Entanglement Stats | Legacy internal diagnostic |
| **03_Research/** | Complexity Scaling (P vs NP) | Legacy internal diagnostic |
| **04_Competitor/** | Performance Benchmarks | Speedup vs Classical |

---

## 📊 Summary of Results

### [02_Proof] Bell State Fidelity
- **File:** [02_Proof_Bell_State_Stats.json](./02_Proof/02_Proof_Bell_State_Stats.json)
- **Insight:** Simulated 2-qubit entanglement achieved 100% match with ideal quantum probability distribution.

### [03_Research] Scaling & Complexity (P=NP)
- **File:** [03_Research_P_vs_NP_Scaling.json](./03_Research/03_Research_P_vs_NP_Scaling.json)
- **Insight:** Legacy internal scaling output from 4 to 131,072 states. This is not a P-vs-NP proof or external complexity-theory validation.

---

## 📁 File Manifest
- `01_Engine/`
  - (TBD) `Engine_Quantum_LC_Summary.json` - Hardware level parameters.
- `02_Proof/`
  - [02_Proof_Bell_State_Stats.json](./02_Proof/02_Proof_Bell_State_Stats.json) - Fidelity log.
- `03_Research/`
  - [03_Research_P_vs_NP_Scaling.json](./03_Research/03_Research_P_vs_NP_Scaling.json) - Hardcore scaling data.

---

*Note: All result files are generated automatically by running the corresponding scripts in `Code/*`.*
