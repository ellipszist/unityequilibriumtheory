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
