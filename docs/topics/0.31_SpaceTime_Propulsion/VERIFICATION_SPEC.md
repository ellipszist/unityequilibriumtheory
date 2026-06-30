# Verification Spec: 0.31 SpaceTime Propulsion (Transmedium R&D Standard)

This document defines the strict engineering thresholds for Transmedium and Lattice Anchoring R&D simulations.

## 1. Empirical Target
- **Target Drag Reduction:** >= 90.0% (Using plasma sheath fluid decoupling)
- **Lattice Anchoring Displacement:** <= 50.0 mm under a 5000 N external crosswind force
- **Data Source:** `Data/05_Simulation/empirical_transmedium_profile.json`

## 2. Hardening Logic
To pass the UET R&D validation, the script `Code/05_Simulation/Sim_Transmedium.py` must:
1. Ingest the empirical data matrix (fluid densities, hull drag, lattice constants) rather than hardcoding them.
2. Calculate classical drag vs plasma-sheath drag using empirical bounds.
3. Assert that `achieved_drag_reduction_pct` >= 90.0 AND `lattice_displacement_mm` <= 50.0.

## 3. Artifact
The output is written to `Result/artifacts/rd_transmedium_sim_*.json` containing the status gate (`PASS` / `FAIL`).
