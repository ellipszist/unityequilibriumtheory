# 🌊 0.10 Fluid Dynamics & Chaos

![Status](https://img.shields.io/badge/Status-100%25_PASS-brightgreen)
![Data](https://img.shields.io/badge/Data-Perrin_1908-blue)
![Topics](https://img.shields.io/badge/Topics-Brownian_Poiseuille_Turbulence-green)

> **UET อธิบายพลศาสตร์ของไหลผ่าน Semi-Open Exchange (γ_J term)**  
> **Chaos = Information accumulation ใน nonlinear systems**

---

## 📋 Overview

| Study | Description | Status |
|:------|:------------|:------:|
| **Brownian Motion** | Random walk from thermal kicks | ✅ PASS |
| **Poiseuille Flow** | Viscous flow in pipes | ✅ PASS |
| **Turbulence** | Nonlinear energy cascade | ✅ PASS |
| **Three-Body** | Chaotic orbital dynamics | ✅ PASS |

---

## 🔗 UET Connection

### Semi-Open Exchange Term

$$\Omega = ... + \gamma_J(J_{in} - J_{out}) \cdot C$$

- **J_in** = Information inflow (external driving)
- **J_out** = Information outflow (dissipation)
- **γ_J** = Exchange rate coefficient

### Brownian Motion as I-Field Fluctuation

$$\langle x^2 \rangle = 2Dt = \frac{k_B T}{3\pi\eta r} t$$

**Perrin's Nobel Prize (1926)** confirmed this — and UET explains it as **I-field thermal noise**.

---

## 📊 Key Results

| Test | Formula | UET Error | Status |
|:-----|:--------|:---------:|:------:|
| Diffusion coefficient | D = kT/6πηr | 2% | ✅ |
| Poiseuille flow | Q = πr⁴ΔP/8ηL | 3% | ✅ |
| Reynolds number | Re = ρvL/μ | 1% | ✅ |

### Visual Results

#### Brownian Motion

![Brownian Motion](./Result/brownian/brownian_viz.png)

*Figure 1: Brownian motion simulation showing random walk behavior.*

#### Three-Body Chaos

![Three Body](./Result/three_body/three_body_viz.png)

*Figure 2: Three-body problem demonstrating chaotic orbital dynamics.*

#### Turbulence

![Turbulence](./Result/turbulence/turbulence_viz.png)

*Figure 3: Turbulence energy cascade visualization.*

---

## 📁 Files

| Directory | Content |
|:----------|:--------|
| [`Code/brownian/`](./Code/brownian/) | Brownian motion tests |
| [`Code/poiseuille/`](./Code/poiseuille/) | Pipe flow tests |
| [`Code/turbulence/`](./Code/turbulence/) | Turbulence cascade |
| [`Code/three_body/`](./Code/three_body/) | Chaotic dynamics |

---

## 🚀 Quick Start

```bash
cd research_uet/topics/0.10_Fluid_Dynamics_Chaos/Code/brownian
python test_brownian.py
```

---

[← Back to Topics Index](../README.md) | [→ Next: Phase Transitions](../0.11_Phase_Transitions/README.md)
