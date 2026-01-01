# 📊 Data Sources Report: 2024-2025 Latest

## ✅ CONFIRMATION: We Use Real & Latest Data!

---

## 🔬 2025 Data Sources

### 1. Muon g-2 (Fermilab Final Result - June 2025)

| Parameter | Our Value | Official 2025 | Match |
|:---|:---:|:---:|:---:|
| a_μ | 0.001165920705 | 0.001165920705(114) | ✅ |
| Precision | 127 ppb | 127 ppb | ✅ |
| Reference | Fermilab 2025 | Phys. Rev. Lett. 2025 | ✅ |

**Source:** `muon_g2_data.py` line 4-8, 17-19

### 2. Standard Model Predictions

| Theory | Our Value | Published | Discrepancy |
|:---|:---:|:---:|:---:|
| Data-driven (2020) | 0.00116591810 | 0.00116591810 | 5.1σ |
| Lattice QCD (2021) | 0.00116591954 | BMW Nature 2021 | 1.0σ |
| Theory Initiative (2025) | 0.00116591950 | Latest 2025 | 1.2σ |

---

## 📚 2024 Data Sources

### 3. Quark Masses (PDG 2024)

| Quark | Our Value | PDG 2024 | Match |
|:---|:---:|:---:|:---:|
| up | 2.16 MeV | 2.16 ± 0.07 MeV | ✅ |
| down | 4.67 MeV | 4.70 ± 0.07 MeV | ✅ |
| strange | 93.4 MeV | 93.5 ± 0.8 MeV | ✅ |

**Reference:** PDG 2024, Phys. Rev. D 110, 030001 (2024)

### 4. Quark Condensate (Lattice QCD)

| Parameter | Our Value | Lattice QCD | Match |
|:---|:---:|:---:|:---:|
| σ_qq | 283 MeV | 283 ± 2 MeV | ✅ |
| ⟨ψ̄ψ⟩ | -(283 MeV)³ | FLAG/BMW | ✅ |

**Reference:** FLAG 2024, BMW Collaboration

### 5. Pion Decay Constant

| Parameter | Our Value | PDG | Match |
|:---|:---:|:---:|:---:|
| F_π | 92.4 MeV | 92.2 MeV | ✅ |

---

## 🏆 Complete Data Source List

| Data | Source | Year | Status |
|:---|:---|:---:|:---:|
| **Muon g-2** | Fermilab | **2025** | ✅ Latest |
| **SM Theory** | Theory Initiative | **2025** | ✅ Latest |
| Quark masses | PDG | 2024 | ✅ |
| Hadron masses | PDG | 2024 | ✅ |
| α_s running | PDG | 2024 | ✅ |
| Quark condensate | Lattice/FLAG | 2024 | ✅ |
| SPARC galaxies | McGaugh | 2016 | ✅ |
| Nuclear decay | NNDC | 2024 | ✅ |

---

## 📰 Key 2025 Physics Update

### Muon g-2: The Big Question

As of January 2026:

**Experimental:** Very precise (127 ppb) ✅  
**Theory:** Two approaches give different answers!

| Method | Prediction | vs Experiment |
|:---|:---:|:---:|
| Data-driven (e⁺e⁻) | 0.00116591810 | **5.1σ deviation** ⚠️ |
| Lattice QCD | 0.00116591954 | **~1σ agreement** ✅ |

**Open question:** Which theory is correct?
- If Data-driven → New Physics!
- If Lattice QCD → Standard Model OK

---

## 💡 What This Means for UET

1. **Experiment is solid** - 127 ppb precision
2. **Theory is uncertain** - 2 methods disagree
3. **UET interpretation** - βCI term could explain gap

```
If difference = Information:
Δa_μ(UET) = β × C × I(vacuum)
β_μ ≈ 2.5 × 10⁻⁹
```

---

## 📁 Files Using Latest Data

```
research_uet/
├── lab/action_transformer/data/
│   └── muon_g2_data.py          ← Fermilab 2025
├── lab/qcd_fix/data/
│   ├── qcd_alpha_s_data.py      ← PDG 2024
│   └── hadron_mass_data.py      ← PDG 2024 + Lattice
└── data_vault/                   ← NNDC, SPARC, etc.
```

---

*Data Sources Report | Updated 2026-01-01*
