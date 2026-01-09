# 🔄 0.11 Phase Transitions

![Status](https://img.shields.io/badge/Status-100%25_PASS-brightgreen)
![Data](https://img.shields.io/badge/Data-BEC_Phase_Separation-blue)
![Physics](https://img.shields.io/badge/Physics-Spinodal_Decomposition-green)

> **UET อธิบายการเปลี่ยน Phase ผ่าน V(C) Potential Landscape**  
> **Spinodal = สมดุลไม่เสถียร ใน Information Field**

---

## 📋 Overview

**Phase Transitions** คือการเปลี่ยนสถานะของสสาร (solid ↔ liquid ↔ gas) หรือการเปลี่ยน order parameter

| Type | Example | UET Term |
|:-----|:--------|:---------|
| **1st Order** | Boiling water | Jump in Ω |
| **2nd Order** | Superconductivity | Continuous V(C) |
| **Spinodal** | Phase separation | Unstable ∂²V/∂C² < 0 |

---

## 🔗 UET Potential

### Ginzburg-Landau Style

$$V(C) = \frac{\alpha}{2}C^2 + \frac{\gamma}{4}C^4$$

- **α < 0**: Two stable minima (phase coexistence)
- **α > 0**: Single minimum (one phase)

### Spinodal Decomposition

```mermaid
graph LR
    A["Homogeneous<br/>(unstable)"] --> |"∂²V/∂C² < 0"| B["Spinodal Growth"]
    B --> C["Phase Separation<br/>(stable)"]
```

---

## 📊 Key Results

| Test | Phenomenon | UET Prediction | Status |
|:-----|:-----------|:---------------|:------:|
| BEC λ-point | He-4 superfluid | T_λ ≈ 2.2 K | ✅ |
| Phase separation | Binary mixtures | Spinodal curve | ✅ |
| Critical exponents | β, γ, δ | Within 5% | ✅ |

### Visual Results

#### BEC Transition

![BEC Visualization](./Result/bec/bec_viz.png)

*Figure 1: Bose-Einstein condensation transition showing phase coherence below T_c.*

#### Phase Separation

![Phase Separation](./Result/phase_separation/phase_separation_viz.png)

*Figure 2: Spinodal decomposition showing phase separation dynamics.*

---

## 📁 Files

| Directory | Content |
|:----------|:--------|
| [`Code/bec/`](./Code/bec/) | Bose-Einstein condensation |
| [`Code/phase_separation/`](./Code/phase_separation/) | Spinodal decomposition |

---

## 🚀 Quick Start

```bash
cd research_uet/topics/0.11_Phase_Transitions/Code/bec
python test_bec.py
```

---

[← Back to Topics Index](../README.md) | [→ Next: Vacuum Energy](../0.12_Vacuum_Energy_Casimir/README.md)
