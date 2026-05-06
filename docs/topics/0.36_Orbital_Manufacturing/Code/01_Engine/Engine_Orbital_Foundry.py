"""
UET Orbital Manufacturing Engine (Topic 0.36)
================================================
Axiomatic simulation of Vacuum Thermodynamics in an Orbital Foundry.
Models radiative cooling bottlenecks and operational duty cycles.
"""

import sys
from pathlib import Path
import numpy as np

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

from docs.core.uet_base_solver import UETBaseSolver
from docs.core.uet_parameters import UETParameters, get_params, INTEGRITY_KILL_SWITCH

# Constants
STEFAN_BOLTZMANN = 5.670374419e-8  # W/(m^2 K^4)
T_SPACE = 2.7  # Cosmic Microwave Background temp in Kelvin (approx vacuum temp)

class UETOrbitalFoundryEngine(UETBaseSolver):
    """
    Simulates the thermal limits of an orbital shipyard.
    Vacuum prevents convection, so heat must be dumped via radiative graphene fins.
    """

    def __init__(self, params=None, name="UET_Orbital_Foundry"):
        if params is None:
            params = get_params("0.36")
            
        super().__init__(
            nx=1, ny=1, dt=1.0, # 1 second steps
            params=params, name=name,
            topic="0.36_Orbital_Manufacturing", pillar="01_Engine"
        )
        
        # Foundry Specs
        self.manufacturing_power_w = 5e7  # 50 MW of heat generated during active welding/fabrication
        self.fin_area_m2 = 1e5            # 100,000 m^2 of radiative graphene fins
        self.fin_emissivity = 0.99        # Graphene metamaterial
        
        # Thermal Mass
        self.shipyard_mass_kg = 1e7       # 10,000 tons
        self.specific_heat_j_kg_k = 900.0 # Aluminum/Carbon baseline
        
        # State
        self.temperature_k = 300.0        # Start at room temp
        self.operating_limit_k = 500.0    # Shut down fabrication if too hot
        self.is_fabricating = True
        
        self.results_history = []
        self.uptime_seconds = 0
        self.downtime_seconds = 0

    def calculate_radiative_cooling(self, temp_k: float) -> float:
        """
        Stefan-Boltzmann Law for radiative cooling in a vacuum.
        P_rad = A * epsilon * sigma * (T^4 - T_space^4)
        """
        power_radiated_w = self.fin_area_m2 * self.fin_emissivity * STEFAN_BOLTZMANN * (temp_k**4 - T_SPACE**4)
        return float(power_radiated_w)

    def step(self, step_idx: int = 0):
        if INTEGRITY_KILL_SWITCH:
            self.results_history.append({"temp_k": np.nan, "status": "KILLED", "duty_cycle": np.nan})
            return

        # 1. Thermal Logic
        heat_generated_j = 0.0
        if self.is_fabricating:
            heat_generated_j = self.manufacturing_power_w * self.dt
            self.uptime_seconds += self.dt
        else:
            self.downtime_seconds += self.dt
            
        heat_radiated_j = self.calculate_radiative_cooling(self.temperature_k) * self.dt
        
        # 2. Temperature Update (Q = mc_p * dT)
        net_heat_j = heat_generated_j - heat_radiated_j
        delta_T = net_heat_j / (self.shipyard_mass_kg * self.specific_heat_j_kg_k)
        
        self.temperature_k += delta_T
        
        # 3. Control System (Thermal Bottleneck)
        if self.temperature_k > self.operating_limit_k:
            self.is_fabricating = False # Pause to cool
        elif self.temperature_k < 350.0:
            self.is_fabricating = True  # Resume when cool enough
            
        duty_cycle = self.uptime_seconds / max(1.0, (self.uptime_seconds + self.downtime_seconds))
        
        self.results_history.append({
            "tick": step_idx,
            "temp_k": self.temperature_k,
            "status": "FABRICATING" if self.is_fabricating else "COOLING",
            "duty_cycle": duty_cycle
        })
        
        if (step_idx + 1) % 1000 == 0:
            print(f"   [ORBITAL FOUNDRY] Tick {step_idx+1} | Temp: {self.temperature_k:.1f} K | Status: {'FABRICATING' if self.is_fabricating else 'COOLING'} | Duty Cycle: {duty_cycle:.1%}")

    def save_results(self):
        import json
        from pathlib import Path
        Path(self.logger.run_dir).mkdir(parents=True, exist_ok=True)
        out_path = Path(self.logger.run_dir) / "orbital_foundry_analysis.json"
        with open(out_path, "w") as f:
            json.dump(self.results_history, f, indent=2)
        return str(out_path)

if __name__ == "__main__":
    print(f"\n🚀 UET ORBITAL FOUNDRY: Simulating Vacuum Thermodynamics...")
    engine = UETOrbitalFoundryEngine()
    engine.run(steps=5000, verbose=True) # Run for 5000 seconds
    path = engine.save_results()
    print(f"✅ Foundry Result: {path}\n")
