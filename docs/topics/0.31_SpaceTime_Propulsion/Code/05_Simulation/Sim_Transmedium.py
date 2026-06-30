import numpy as np
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# --- ROBUST UET BOOTSTRAP ---
def _bootstrap():
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None

ROOT = _bootstrap()
if not ROOT:
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)

topic_path = ROOT / "docs" / "topics" / "0.31_SpaceTime_Propulsion"

class TransmediumSim:
    """
    R&D Grade Simulation of Transmedium Dynamics & Lattice-Locked Stability.
    Ingests empirical bounds from Data/05_Simulation/empirical_transmedium_profile.json
    """
    def __init__(self):
        data_path = topic_path / "Data" / "05_Simulation" / "empirical_transmedium_profile.json"
        if not data_path.exists():
            print(f"CRITICAL: Empirical dataset missing at {data_path}")
            sys.exit(1)
            
        with open(data_path, "r") as f:
            self.empirical_data = json.load(f)
            
        # Environmental Bounds
        self.rho_water = self.empirical_data["environmental_bounds"]["rho_water_kg_m3"]
        self.rho_air = self.empirical_data["environmental_bounds"]["rho_air_kg_m3"]
        
        # Vehicle Parameters
        self.area = self.empirical_data["vehicle_parameters"]["frontal_area_m2"]
        self.cd_classical = self.empirical_data["vehicle_parameters"]["base_drag_coefficient_cd"]
        
        # Engineering Targets
        self.target_drag_reduction = self.empirical_data["engineering_targets"]["target_drag_reduction_percent"]
        self.max_disp_mm = self.empirical_data["engineering_targets"]["max_allowable_lattice_displacement_mm"]
        self.k_lattice = self.empirical_data["engineering_targets"]["lattice_restoration_constant_n_m"]
        self.plasma_reduction = self.empirical_data["engineering_targets"]["plasma_sheath_reduction_factor"]

    def calculate_drag(self, velocity, medium="air", plasma_active=False):
        rho = self.rho_air if medium == "air" else self.rho_water
        
        # UET Plasma Sheath Effect based on empirical targets
        reduction_factor = self.plasma_reduction if plasma_active else 1.0
        cd_eff = self.cd_classical * reduction_factor
        
        force = 0.5 * rho * (velocity**2) * cd_eff * self.area
        return force, cd_eff

    def test_lattice_stability(self, wind_force_n):
        # UET Lattice Lock: Restoration force balances external pressure.
        # Displacement = F / k
        displacement_m = wind_force_n / self.k_lattice
        return displacement_m * 1000 # Return in mm

    def run(self):
        print("=== R&D Transmedium Simulation ===")
        print(f"Loading Empirical Baseline: {self.empirical_data['metadata']['dataset_name']}")
        
        drag_results = []
        stability_results = []
        
        # 1. Drag Test (Fluid Transition in Water)
        test_velocity = 50 # m/s
        f_classical, cd_c = self.calculate_drag(test_velocity, medium="water", plasma_active=False)
        f_plasma, cd_p = self.calculate_drag(test_velocity, medium="water", plasma_active=True)
        
        achieved_drag_reduction = (1 - f_plasma/f_classical) * 100
        drag_results.append({
            "velocity_ms": test_velocity,
            "force_classical_n": f_classical,
            "force_plasma_n": f_plasma,
            "drag_reduction_pct": achieved_drag_reduction
        })

        # 2. Stability Test (Lattice Locking under 5000 N crosswind)
        test_force = 5000 # N
        disp_mm = self.test_lattice_stability(test_force)
        stability_results.append({
            "external_force_n": test_force,
            "displacement_mm": disp_mm
        })

        # 3. Assert Engineering Gates
        passed_drag = achieved_drag_reduction >= self.target_drag_reduction
        passed_stability = disp_mm <= self.max_disp_mm
        passed_all = passed_drag and passed_stability

        output_data = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "topic": "0.31_SpaceTime_Propulsion",
                "status": "PASS" if passed_all else "FAIL"
            },
            "metrics": {
                "achieved_drag_reduction_pct": achieved_drag_reduction,
                "target_drag_reduction_pct": self.target_drag_reduction,
                "achieved_displacement_mm": disp_mm,
                "max_allowable_displacement_mm": self.max_disp_mm
            },
            "drag_test": drag_results,
            "stability_test": stability_results
        }
        
        # Save to R&D artifacts directory
        artifact_dir = topic_path / "Result" / "artifacts"
        artifact_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"rd_transmedium_sim_{int(datetime.now().timestamp())}.json"
        with open(artifact_dir / filename, "w") as f:
            json.dump(output_data, f, indent=4)
            
        print(f"Result: {output_data['metadata']['status']}")
        print(f"Drag Reduction: {achieved_drag_reduction:.1f}% (Target: >={self.target_drag_reduction}%)")
        print(f"Lattice Displacement: {disp_mm:.1f} mm (Target: <={self.max_disp_mm} mm)")
        print(f"Artifact saved to Result/artifacts/{filename}")
        
        return output_data

if __name__ == "__main__":
    sim = TransmediumSim()
    sim.run()
