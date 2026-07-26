# Thermal Observable Bridge Update Log

## 2026-07-27 — C-to-thermal observable bridge diagnostic

- Added an explicit normalized map `T_norm = T0 + alpha_T*C` and kept the gain
  open rather than fitting or treating it as a universal constant.
- Evaluated Fourier and Cattaneo heat-flux controls, entropy-production proxies,
  and the prior C path-cost ledger on the same synthetic periodic trajectory.
- Added a gain-rescaling identifiability test: fixed `C` with different thermal
  gains changes the thermal observable amplitude while leaving C path work fixed.
- The wave remains `SIMULATION_ONLY` and `BLOCKED_OPEN_MAPPING`; no external
  thermal source or SI measurement claim is promoted.
- Controlling blocker: derive or source-lock one dimensional observable map from
  a physical C realization to temperature/heat/entropy before calibration.
