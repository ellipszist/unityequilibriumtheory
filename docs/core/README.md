# ⚙️ Core — UET Mathematical Engine

> Foundation-first status: This README contains historical/legacy engine wording and is
> not the controlling claim source. Current equation status is controlled by
> [docs/core/AGENTS.md](./AGENTS.md), the equation registry, and the foundation dependency gate.
> The legacy statement that C universally means mass or that I is a universal physical field
> is not accepted by the current research protocol.

## Current foundation contract

The legacy tables below are retained for historical compatibility. For current equation
work, use this contract:

| Symbol | Current status |
| :-- | :-- |
| C | system-state coordinate with lane-specific physical mapping; not universally mass |
| Phi | effective space-response variable; not a metric or substance |
| Pi | time derivative of Phi |
| R / I_trace | derived causal/history observable with no feedback in the new mode |
| mass, density, charge, stress-energy | separate standard-physics quantities or explicit lane mappings |

Current foundation artifacts:

- [Equation inventory](./UET_FOUNDATION_EQUATION_INVENTORY.md)
- [Correspondence matrix](./UET_FOUNDATION_CORRESPONDENCE_MATRIX.md)
- [Compatibility audit](./UET_FOUNDATION_COMPATIBILITY_AUDIT.md)
- [Machine-readable inventory gate](./artifacts/uet_foundation_equation_inventory.json)
- [Machine-readable correspondence matrix](./artifacts/uet_foundation_correspondence_matrix.json)

> **The Physics Engine solving the Unity Equilibrium Master Equation**  
> **Version 0.9.0** | Last Updated: 2026-01-13

![Engine](https://img.shields.io/badge/Engine-UET_Master_Eq-blue)
![Coverage](https://img.shields.io/badge/Axioms-12%2F12-brightgreen)
![Status](https://img.shields.io/badge/Status-Legacy-Claim-Controlled-yellow)
![Tests](https://img.shields.io/badge/Tests-126_(98.4%25)-green)

---

## 🎯 Purpose

This directory contains the **computational core** of the Unity Equilibrium Theory. It is the "Engine" that solves the fundamental energy functional for all 20 physics domains (from Galaxies to Quantum Mechanics).

**The Rule:** Nature is constrained optimization.
> *The system state evolves to minimize the generalized energy functional $\Omega$.*

**The Value Equation:**
> $$\mathcal{V} = -\Delta\Omega$$
> *When disequilibrium decreases, the system gains Value.*

---

## Legacy master equation (historical form)

The following seven-term functional is retained as a legacy candidate implementation; it is not a closed physical derivation:

$$
\Omega[C,I,J] = \int d^3x \left[ 
\underbrace{V(C)}_{\text{A1: Energy}} + 
\underbrace{\frac{\kappa}{2}|\nabla C|^2}_{\text{A3: Space/Memory}} + 
\underbrace{\beta C \cdot I}_{\text{A2: Info Coupling}} + 
\underbrace{\gamma_J (J_{in} - J_{out}) \cdot C}_{\text{A4: Semi-Open Exchange}} + 
\underbrace{W_N |\nabla \Omega|}_{\text{A5: Natural Will}} + 
\underbrace{\beta_U V_{game}}_{\text{A8: Dynamic Game}} + 
\underbrace{\lambda \Sigma (C_i - C_j)^2}_{\text{A10: Coherence}}
\right]
$$

---

## 🔤 Variable Definition

| Symbol | Name | Mathematical Meaning | Physical Interpretation |
|:------:|:-----|:---------------------|:------------------------|
| **C** | Capacity / Conscious Field | State Vector C(x,t) | Legacy lane label; current work requires explicit physical mapping |
| **I** | Information / Instinctive Field | Legacy entropy/stimulus notation | Legacy/comparator label; current work uses derived I_trace only when declared |
| **J** | Flux Field | J_in - J_out | Open system energy exchange |
| **V(C)** | Potential | (α/2)C² + (γ/4)C⁴ | Cost of Existence (Higgs-like) |
| **κ** | Gradient Cost | \|∇C\|² coefficient | Surface Tension, Space Memory |
| **β** | Coupling | kT ln 2 | Landauer Limit (Info ↔ Energy) |
| **Ω** | Equilibrium Functional | ∫[...] dx | Total disequilibrium (minimize this) |
| **𝒱** | Value | -ΔΩ | Improvement per step |

> 📖 **Full symbol definitions**: See [`SYMBOL_GLOSSARY.md`](./SYMBOL_GLOSSARY.md)

---

## 📄 Engine Components

| File | Role | Description |
|:-----|:-----|:------------|
| [`uet_master_equation.py`](./uet_master_equation.py) | **The Law** | Defines the Ω functional and `dynamics_step` (solver). **Single Source of Truth.** |
| [`uet_matrix_engine.py`](./uet_matrix_engine.py) | **The Solver** | Fast Tensor-based implementation for large-scale grids (3D Galaxies). |
| [`uet_matrix_toolkit.py`](./uet_matrix_toolkit.py) | **The Tools** | Helper functions for visualization and matrix algebra. |
| [`uet_4d_engine.py`](./uet_4d_engine.py) | **Relativity** | Extension for 4D spacetime metrics and tensor operations. |

---

## 📚 Documentation
| [`../Doc/DOMAIN_MAPPING.md`](../Doc/DOMAIN_MAPPING.md) | C/I ในแต่ละสาขา (6 domains) |
| [`../Doc/VALUE_EQUATION.md`](../Doc/VALUE_EQUATION.md) | 𝒱 = -ΔΩ — สมการ Value |

---

## 🌐 Multi-Domain Interpretation

C และ I มีความหมายต่างกันในแต่ละ domain — แต่สมการเดียวกัน:

| Domain | C = | I = |
|:-------|:----|:----|
| **Physics** | Visible matter | Dark matter |
| **Neuroscience** | Excitatory activity | Inhibitory state |
| **Economics** | Market price | Intrinsic value |
| **Biology** | Activator | Inhibitor |
| **Machine Learning** | Observable features | Latent representation |

> 📖 **Full domain mapping**: See [`../Doc/DOMAIN_MAPPING.md`](../Doc/DOMAIN_MAPPING.md)

---

## ✅ Validator Scripts

These scripts ensure the engine adheres to fundamental physics limits (Axiom 11):

| Script | Purpose |
|:-------|:--------|
| [`test/`](./test/) | Unit tests for core functions |
| [`validation/`](./validation/) | Physics validation scripts |

---

## 🔗 Navigation

- **🔙 [Research Root](../README.md)**
- **🧪 [Topics (Applications)](../topics/)**
- **📊 [Data Sources](../DATA_SOURCE_MAP.md)**
- **📖 [Documentation Index](../Doc/DOC_INDEX.md)**

---

*Unity Equilibrium Theory — Core Engine v0.9.0*
*"𝒱 = -ΔΩ — ระบบที่ลดความไม่สมดุล = ระบบที่สร้าง Value"*
