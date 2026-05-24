# 📉 Limitation: The Magnitude Gap
> [!WARNING]
> **Legacy claim boundary:** This file is a concept or legacy analysis note from
> an earlier drafting pass. It is not the topic status authority and must not be
> used to claim the muon g-2 anomaly is resolved, Standard Model discrepancy is
> closed, alternate explanations are ruled out, new-physics mechanism is
> established, first-principles anomaly derivation is complete, parameter-free
> prediction is validated, or downstream particle-theory support is established.
> Current allowed claims are controlled by `README.md`, `LIMITATIONS.md`,
> `VERIFICATION_SPEC.md`, `DATA_MANIFEST.md`, and
> `Result/artifacts/muon_g2_2025_validation.json`.

## The Problem
UET correctly identifies that vacuum information coupling ($\beta$) should scale with mass squared ($(m_\mu/m_e)^2$), creating a larger recoil for the muon than the electron.

However, the originally proposed formula:
$$ \Delta a_\mu^{UET} = \beta \left(\frac{m_\mu}{m_e}\right)^2 \frac{\alpha^3}{4\pi^3} $$
yields a value of $\approx 10^{-4}$, which is **10,000 times larger** than the observed anomaly ($2.5 \times 10^{-9}$).

## The Physics Gap
The "Information Field" must be much stiffer or suppressed by a significantly larger factor than initially estimated to align with reality.
Possible missing suppression factors:
- **Vacuum Density ($\rho_{vac}$):** The field might be extremely dilute.
- **Geometric Factor:** $\alpha_{QED}^2$ might be involved in a different way.

## Honest Admission
The value $\Delta a_\mu^{UET} = 2.5 \times 10^{-9}$ used in our code is a **[CALIBRATED PARAMETER]**.
- It is **Fixed** to match the Fermilab/BNL gap.
- We do **NOT** currently have a first-principles derivation that yields the correct magnitude, only the correct sign and mass scaling behavior.
