# 📉 Limitation: The Tree-Level Approximation

> [!WARNING]
> **Legacy claim boundary:** This file is a concept, analysis, or legacy note from an earlier drafting pass.
> It is not the topic status authority and must not be used to claim a full electroweak proof,
> gauge-theory derivation, all-observable electroweak fit, Standard Model replacement,
> running-angle proof, or superiority over QFT/SM. Current allowed claims are controlled by
> `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `FORMULA_AUDIT.md`, and
> `Result/artifacts/electroweak_expanded_benchmark.json`: selected benchmark agreement only.

## The Problem
UET calculates the W/Z Mass Ratio using a purely geometric mixing angle derived from Vacuum Equilibrium ($\beta$ vs $\kappa$).

$$ \frac{M_W}{M_Z} = \cos \theta_W = \sqrt{1 - \sin^2 \theta_W} $$

Substituting $\sin^2 \theta_W \approx 0.23121$:
- **UET Prediction:** $0.8768$
- **Observed (PDG):** $0.8815$
- **Discrepancy:** ~0.53%

## The Physics Gap
The Standard Model accounts for this difference via **Radiative Corrections** (Loop diagrams involving the Top Quark and Higgs). This is often parameterized by the Rho parameter ($\rho \approx 1.01$).

$$ \frac{M_W}{M_Z} = \rho \cos \theta_W $$

UET's current "Lite Engine" is a **Tree-Level Theory** (Classical Field Limit). It does not yet automatically calculate these quantum loop corrections, leading to the 0.5% error.

## Honest Admission
1.  **Likely Calibrated:** The values for $\sin^2 \theta_W$ and $M_H$ in our code are currently **Manual Inputs** ([CALIBRATED]) to match the Z-pole and Higgs discovery data.
2.  **Missing Loops:** The 0.53% error in W/Z ratio is a genuine limitation of the current 0D geometric formulation.
