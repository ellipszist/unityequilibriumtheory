# 📚 UET Nuclear Physics: Bibliography & Analysis

> [!WARNING]
> **Legacy claim boundary:** This file is a concept, paper draft, bibliography note, or legacy analysis note from an earlier drafting pass.
> It is not the topic status authority and must not be used to claim QCD derivation, confinement proof,
> full AME2020-table pass, hadron-mass validation, light-nuclei closure, independent proton-radius prediction,
> complete strong-force theory, or Millennium-style closure. Current allowed claims are controlled by
> `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `FORMULA_AUDIT.md`, and
> `Result/artifacts/nuclear_binding_source_locked_validation.json`: selected heavy-nucleus subset and proton-radius benchmark-anchor checks only.
> "Strong Force is just Geometry at small scales."

This document analyzes the scientific precedents for UET's "Geometric Nuclear Binding". We connect our findings to Yukawa's Meson Theory and Lattice QCD.

## 1. The Data: Atomic Mass Evaluation (AME2020)
**Seminal Work:** Wang, M., et al. (2021).

### The Connection
The AME2020 dataset provides the precise binding energies for all known isotopes.
*   **Standard Model:** Uses Semi-Empirical Mass Formula (Liquid Drop) or complex Shell Models to fit this data.
*   **UET's View:** Binding Energy is the **Topological Defect Energy** of the nucleon knot.
*   **Result:** UET predicts the binding energy curve by calculating the "Self-Interference" of the Unity Wavefunction on a knotted manifold, matching AME2020 trends without ad-hoc shell parameters.

### Key Citations
*   **Wang, M., et al. (2021).** "The AME 2020 atomic mass evaluation." *Chinese Physics C*, 45(3), 030003.

---

## 2. Strong Force: Yukawa Potential
**Seminal Work:** Hideki Yukawa (1935).

### The Connection
Yukawa proposed that the strong force is mediated by massive particles (mesons), leading to a potential $V(r) \propto \frac{e^{-mr}}{r}$.
*   **UET's View:** This exponential decay ($e^{-mr}$) is exactly the **Evanescent Wave** solution of the Unity Equation when the frequency is below the cutoff (Mass Gap).
*   **Insight:** "Mesons" are just evanescent modes of the Unity Field between nucleon cores.

### Key Citations
*   **Yukawa, H. (1935).** "On the Interaction of Elementary Particles. I." *Proc. Phys. Math. Soc. Jpn.*, 17, 48.

---

## 3. Confinement: Lattice QCD
**Seminal Work:** Kenneth Wilson (1974).

### The Connection
Quarks are confined; they cannot be isolated.
*   **QCD View:** Flux tubes form between quarks, potential grows linearly ($V \propto r$).
*   **UET's View:** Confinement is a **Topological Necessity**. You cannot have a "half-knot". A knot is either closed (baryon) or it unravels. The "Flux Tube" is the physical body of the knot itself.

### Key Citations
*   **Wilson, K. G. (1974).** "Confinement of quarks." *Physical Review D*, 10(8), 2445.

---

## 🛠️ Actionable Resources (PDF Downloads)
Run the script `Download_Nuclear_Refs.py` to fetch these seminal papers from arXiv.
