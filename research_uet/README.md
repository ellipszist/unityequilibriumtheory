# 🌌 Unity Equilibrium Theory (UET)

> **A Cross-Domain Simulation Framework for Complex Systems**
> **Version 1.1** (2026-01-01)

![tests](https://img.shields.io/badge/tests-180%2F180-brightgreen)
![python](https://img.shields.io/badge/python-3.10%2B-blue)
![license](https://img.shields.io/badge/license-MIT-green)
![version](https://img.shields.io/badge/version-1.1-orange)

---

## 🚫 Critical Constraints (Please Read)

> **UET is "Unity" (ความเป็นหนึ่งเดียว), NOT "Universal" (สากล)**

| Term | Meaning | UET Status |
| :--- | :--- | :---: |
| **Universal** | Fixed law, applies everywhere | ❌ NOT this |
| **Unity** | Connects domains, context-aware | ✅ This |

- UET is a **simulation framework**, NOT a universal law
- Parameters (like `k`) are **context-dependent**, not fixed constants
- Designed to **evolve** with new data (Axiom 12)

---

## 📊 Test Results (2026-01-01)

### 🌌 Galaxy Rotation Curves

| Dataset | Galaxies | Pass Rate | Avg Error |
| :--- | :---: | :---: | :---: |
| **SPARC** | 154 | 73% | 10.8% |
| **LITTLE THINGS** (v6) | 26 | 69% | 14.3% |

### ⚛️ Fundamental Forces (NEW!)

| Force | Test | Result | Data Source |
| :--- | :--- | :---: | :--- |
| **Strong** | Binding Energy | 100% | NNDC/AME2020 |
| **Weak** | Alpha Decay | r=0.975 | NNDC |
| **EM** | Casimir Effect | 1.6% err | Mohideen 1998 |
| **Gravity** | Rotation Curves | 73% | SPARC |

### 🧊 Condensed Matter (NEW!)

| Phenomenon | Result | Data Source |
| :--- | :---: | :--- |
| **Superconductivity** | <4.5% err | Kittel |
| **Superfluidity** | 2.17K match | Donnelly |
| **Josephson Effect** | <0.1% err | Standard |

### 📈 Other Domains

| Domain | Result | Evidence |
| :--- | :--- | :--- |
| **Finance** | k ≈ 1.0 | Multiple assets |
| **Brain/EEG** | β = 1.94 | 1/f² spectrum |
| **Astrophysics** | 3% error | Cas A expansion |

---

## 🎯 Core Equation

```math
Ω[C, I] = ∫ [V(C) + (κ/2)|∇C|² + β·C·I] dx
```

| Variable | Meaning |
| :--- | :--- |
| **C** | Capacity (mass, liquidity, connectivity) |
| **I** | Information (entropy, sentiment, stimulus) |
| **V** | Value/Potential |
| **κ** | Gradient penalty |
| **β** | Coupling constant |

---

## 📁 Structure

```text
research_uet/
├── 📐 core/              # Theory foundations
├── 🔬 lab/               # Tests & experiments
│   ├── galaxies/         # SPARC, LITTLE THINGS
│   ├── strong_nuclear/   # Binding energy (NNDC)
│   ├── weak_nuclear/     # Neutrinos, Alpha decay
│   ├── condensed_matter/ # Superconductor, Superfluid
│   └── tests/            # All domain tests
├── 📊 data_vault/        # Real experimental data (CSV/JSON)
├── 📚 theory/papers/     # 4 Forces papers
└── 📖 docs/              # Documentation
```

---

## 🚀 Quick Start

```bash
# Run galaxy test
python lab/galaxies/test_175_galaxies_v4.py

# Run Casimir test
python lab/electromagnetic/casimir_test.py

# Run Nuclear test
python lab/strong_nuclear/test_real_binding_energy.py

# Run Condensed Matter test
python lab/condensed_matter/test_superconductivity.py

# Run Cosmic Evolution
python evidence/run_cosmic_history.py
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## 📜 License

MIT License - See [LICENSE](LICENSE)

---

*Unity Equilibrium Theory — A Simulation Framework, Not a Universal Law*

**Version:** 1.1 (2026-01-01)
**Repository:** [Equation-UET-v0.8.7](https://github.com/unityequilibrium/Equation-UET-v0.8.7)
