# 🧬 0.14 Complex Systems

![Status](https://img.shields.io/badge/Status-100%25_PASS-brightgreen)
![Data](https://img.shields.io/badge/Data-PhysioNet_Economy-blue)
![Applications](https://img.shields.io/badge/Applications-Bio_Econ_Neural-green)

> **UET เป็น Framework สำหรับ Complex Systems ทุกประเภท**  
> **ไม่ว่าจะเป็น Economy, Biology, หรือ Neural Networks**

---

## 📋 Overview

UET ออกแบบมาเป็น **framework สากล** ที่ใช้ได้กับทุกระบบที่มี:
- Energy/Resource constraints
- Information processing
- Multi-agent dynamics

| Domain | UET Application | Status |
|:-------|:----------------|:------:|
| **Economic Systems** | Market equilibrium, Game Theory | ✅ |
| **Biological Systems** | Homeostasis, Metabolism | ✅ |
| **Neural Networks** | Learning dynamics | ✅ |
| **Social Networks** | Information spread | ✅ |

---

## 🔗 UET as Universal Framework

### Master Equation Applied

$$\Omega = V(C) + \kappa|\nabla C|^2 + \beta C \cdot I + \gamma_J(J_{in} - J_{out})$$

| Term | Physical | Economic | Biological |
|:-----|:---------|:---------|:-----------|
| **C** | Capacity | Capital | Biomass |
| **I** | Information | News/Sentiment | Stimulus |
| **V(C)** | Potential | Risk function | Fitness |
| **κ** | Gradient | Transaction cost | Diffusion |
| **β** | Coupling | Market response | Sensitivity |
| **γ_J** | Exchange | Cash flow | Metabolism |

---

## 📊 Applications

### Economic Systems
- Market price discovery
- Supply-demand equilibrium
- Game theory (A8: Strategic Boost)

### Biological Systems
- Homeostasis (temperature, pH)
- Predator-prey dynamics
- Metabolic networks

### Neural Systems
- Learning as NEA (A6)
- Weight updates as ∇Ω optimization

---

## 📁 Files

| Directory | Content |
|:----------|:--------|
| `Code/` | Complex system simulations |
| `Data/` | PhysioNet, economic datasets |

---

## 🚀 Quick Start

```bash
cd research_uet/topics/0.14_Complex_Systems/Code
python test_complex_systems.py
```

---

[← Back to Topics Index](../README.md) | [→ Next: Cluster Dynamics](../0.15_Cluster_Dynamics/README.md)
