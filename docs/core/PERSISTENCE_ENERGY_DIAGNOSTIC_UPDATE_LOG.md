# Persistence-Energy Diagnostic Update Log

## 2026-07-27 — Organizational path-cost diagnostic

- Added a normalized diagnostic that keeps relational `C(t)` separate from an
  available-energy ledger.
- Implemented the explicit Rayleigh-type comparator `P_C = eta_C*(dC/dt)^2` and
  a ledger for input power, output power, path work, and persistence threshold.
- Added a same-endpoint synthetic comparison between low-activity and high-activity
  trajectories.
- The result is deliberately labelled `CONSTITUTIVE_ANSATZ`, `DIAGNOSTIC_ONLY`,
  and `SIMULATION_ONLY`; it is not a UET derivation or an SI energy claim.
- Controlling blocker: map `P_C` to a physical lane's measured work, heat, or
  entropy-production observable before interpreting the diagnostic physically.

## 2026-08-01 - Named persistence principle and operational contract

- Added canonical name UET-PRINCIPLE-001: หลักการจัดสรรพลังงานร่วมเพื่อการดำรงอยู่ของระบบ.
- Linked the name to the existing normalized path-cost and available-resource ledger diagnostic.
- Added a generated principle contract and explicit non-intentional/result-based claim boundary.
- Verification: the persistence-energy verifier and targeted tests were rerun after the contract change.
- Claim impact: wording remains CANDIDATE_PRINCIPLE, DIAGNOSTIC_ONLY, and SIMULATION_ONLY; no physical promotion.
- Controlling blocker: map behavior-related path cost to measured work, heat, flux, or entropy production in one declared physical lane.

## 2026-08-01 - Interaction-selection dynamic comparator

- Added uet_resource_selection.py and RESOURCE_SELECTION_DYNAMIC_GAME_SPEC.md.
- The lane treats C as a derived collective compatibility coordinate from an
  interaction matrix; it does not call C mass, energy, force, or intention.
- Verification: five focused tests and the deterministic dynamic-selection audit
  passed; probability-simplex drift was 2.22e-16 and ledger residuals were below
  5e-15 in the cooperative/conflict configurations.
- Result: PASS_WITH_OPEN_PHYSICAL_MAPPING / INTERNAL_DIAGNOSTIC /
  SIMULATION_ONLY; conflict persistence ended at t=4.723 while the declared
  cooperative lane did not cross its threshold in the ten-unit horizon.
- Controlling blocker: map the declared behavior/maintenance costs to measured
  work, heat, entropy production, or failure rate in one physical lane.

## 2026-08-01 - Normalized work and bath-entropy observable bridge

- Added resource_selection_thermal_bridge.py, its targeted tests, deterministic
  verifier, and generated resource_selection_thermal_bridge_verification.json.
- Declared map:
  Q_proxy = alpha_b*W_behavior + alpha_m*W_maintenance,
  Delta S_bath_proxy = Q_proxy/T_bath.
- Verification: 3 focused bridge tests plus the dynamic-selection regression passed;
  both cooperative and conflict ledger residuals were below 5e-15, proxies were
  non-negative, and the conflict lane had the larger dissipated-work proxy.
- Result: PASS_WITH_OPEN_THERMAL_MAPPING / INTERNAL_DIAGNOSTIC /
  SIMULATION_ONLY. Scales are declared inputs and were not fitted.
- Controlling blocker: source-lock one material lane with SI work/heat/temperature
  units, uncertainty, and a measurement operator before external comparison.