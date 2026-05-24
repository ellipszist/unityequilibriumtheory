> [!WARNING]
> **Legacy claim boundary:** This file is a legacy analysis, paper draft, research note, or bibliography note, not the topic status authority. It must not be used to claim Navier-Stokes/Millennium proof, global regularity or smoothness proof, turbulence closure, production CFD replacement, universal fluid-engine superiority, external CFD validation, or theorem-level physical closure. Current allowed claims are controlled by `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `FORMULA_AUDIT.md`, and `Result/artifacts/fluid_benchmark_validation.json`: internal speed benchmark and finite-output stress diagnostic only.
# After: UET Poiseuille Flow

## 1. Problem Definition: Viscosity
Viscosity is the internal friction of a fluid. In a pipe, this creates a parabolic velocity profile (Poiseuille Flow).
- **Physical Law**: $v(r) = v_{max} (1 - r^2/R^2)$.
- **Origin**: Why do fluids resist flow? Standard Model says molecular collisions.

## 2. UET Solution: Information Friction
In UET, viscosity arises from the "Information Friction" ($\kappa$) between the fluid's Complex Information Field and the boundary walls.
- **No-Slip Condition**: The information density at the wall is fixed (pinned).
- **Shear Stress**: The gradient of the Information Field creates a force opposing motion.
- **Matrix Engine**: The UET Matrix Engine simulates this by evolving the field tensor according to $\nabla \cdot (\nu \nabla v)$, which is derived from the Information transport equations.

## 3. Results Analysis

### Velocity Profile
![Poiseuille Viz](../../../Result/03_Research/poiseuille/poiseuille_viz.png)
*Fig 1: Velocity Profile. The Matrix Engine simulation (Blue) recovers the theoretical Parabolic Profile (Red Dashed) from first principles of information flow.*

## 4. Conclusion
Viscosity is Information Friction. UET correctly models fluid dynamics as the preservation of information topology under flow.
