# 📁 UET Lab Structure Guide

*Reorganized: 2026-01-01 13:13*

---

## ✅ New Folder Structure

```
research_uet/lab/
│
├── 📄 LAB_COMPLETE_ANALYSIS.md     # Complete analysis
├── 📄 STRUCTURE_GUIDE.md           # This file
├── 📄 MASTER_REFERENCES.py         # All citations
├── 📄 RESEARCH_SUMMARY.md          # Main overview
│
├── 01_particle_physics/            # 🔬 Particle Physics
│   ├── qcd_fix/                    # ⭐ QCD & Hadrons (7.6%, 3.9%)
│   ├── strong_nuclear/             # Strong force
│   ├── weak_nuclear/               # Beta decay
│   ├── neutrinos/                  # PMNS matrix
│   └── standard_model/             # W/Z, sin²θ_W
│
├── 02_astrophysics/                # 🌌 Astrophysics
│   ├── galaxies/                   # ⭐ SPARC 175 (10.8%)
│   └── black_holes/                # EHT M87*
│
├── 03_condensed_matter/            # 🧲 Condensed Matter & EM
│   ├── electromagnetic/            # ⭐ Casimir (1.6%)
│   ├── condensed_matter/           # ⭐ Josephson (0.08%)
│   ├── superfluids/                # He-4 λ-point
│   └── plasma/                     # Fusion (future)
│
├── 04_quantum/                     # ⚛️ Quantum Foundations
│   └── quantum/                    # Bell tests (Nobel 2022)
│
├── 05_unified_theory/              # 🎯 UET Core Theory
│   ├── action_transformer/         # ⭐ Muon g-2 2025
│   ├── effect_of_motion/           # Phase separation
│   └── extensions/                 # Future ideas
│
├── 06_complex_systems/             # 🧠 Complex Systems
│   ├── brain/                      # 1/f noise
│   └── economy/                    # Econophysics
│
└── 07_utilities/                   # 🔧 Utilities
    ├── tests/                      # Integration tests
    └── analysis/                   # Analysis tools
```

---

## 📊 Category Summary

| Category | Path | Modules | Files | Key Test |
|:---|:---|:---:|:---:|:---|
| Particle Physics | `01_particle_physics/` | 5 | 22 | α_s, hadrons |
| Astrophysics | `02_astrophysics/` | 2 | 11 | Galaxies |
| Condensed Matter | `03_condensed_matter/` | 4 | 9 | Casimir, Josephson |
| Quantum | `04_quantum/` | 1 | 2 | Bell tests |
| Unified Theory | `05_unified_theory/` | 3 | 19 | Muon g-2 |
| Complex Systems | `06_complex_systems/` | 2 | 7 | Brain, Economy |
| Utilities | `07_utilities/` | 2 | 47 | Integration |

**Total: 19 modules, 117 files**

---

## ⭐ Priority Modules

| Rank | Path | Error | Status |
|:---:|:---|:---:|:---:|
| 1 | `01_particle_physics/qcd_fix/` | 3.9% | ✅ |
| 2 | `05_unified_theory/action_transformer/` | Core | ✅ |
| 3 | `03_condensed_matter/electromagnetic/` | 1.6% | ✅ |
| 4 | `02_astrophysics/galaxies/` | 10.8% | ✅ |
| 5 | `03_condensed_matter/condensed_matter/` | 0.08% | ✅ |

---

## 🚀 Quick Start Commands

```bash
# Run QCD test
python research_uet/lab/01_particle_physics/qcd_fix/uet_hadron_model.py

# Run Casimir test
python research_uet/lab/03_condensed_matter/electromagnetic/casimir_test.py

# Run Josephson test
python research_uet/lab/03_condensed_matter/condensed_matter/test_josephson_tunneling.py

# Run all integration tests
python research_uet/lab/07_utilities/tests/run_all_tests.py
```

---

## 🔗 Connection Map

```
                    ┌─────────────────────────┐
                    │   05_unified_theory     │
                    │   (action_transformer)  │
                    └───────────┬─────────────┘
                                │ βCI
        ┌───────────────────────┼───────────────────────┐
        ▼                       ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ 01_particle   │       │ 02_astrophysics│      │ 03_condensed  │
│ physics       │◄─────►│               │       │ matter        │
│ (QCD, Weak,   │       │ (Galaxies,    │       │ (Casimir,     │
│  Neutrinos)   │       │  Black Holes) │       │  Josephson)   │
└───────────────┘       └───────────────┘       └───────────────┘
                                │
                        ┌───────┴───────┐
                        ▼               ▼
                ┌───────────────┐ ┌───────────────┐
                │ 04_quantum    │ │ 06_complex    │
                │ (Bell tests)  │ │ (Brain, Econ) │
                └───────────────┘ └───────────────┘
```

---

## 📚 Data Sources by Category

| Category | Source | Year |
|:---|:---|:---:|
| 01_particle | PDG 2024, Lattice QCD | 2024 |
| 02_astro | SPARC, EHT | 2016-2022 |
| 03_condensed | Mohideen, Lamoreaux | 1997-1998 |
| 04_quantum | Aspect, Delft, NIST | 1982-2015 |
| 05_unified | Fermilab g-2 | **2025** |

---

## 📋 For New Researchers

1. **Read first:** `LAB_COMPLETE_ANALYSIS.md`
2. **Core theory:** `05_unified_theory/action_transformer/README.md`
3. **Best test:** `03_condensed_matter/electromagnetic/casimir_test.py`
4. **Main fix:** `01_particle_physics/qcd_fix/uet_hadron_model.py`

---

*Structure Guide v2.0 | Reorganized 2026-01-01*
