import sys
from pathlib import Path
import numpy as np
import json

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
from docs.core.uet_parameters import get_params, INTEGRITY_KILL_SWITCH

# --- FLASH JOULE HEATING ENGINE ---

class UETFlashJouleEngine(UETBaseSolver):
    """
    Simulates a Flash Joule Heating (FJH) reactor for graphene synthesis.
    Converts carbon waste into high-quality graphene via millisecond high-voltage discharge.
    """
    def __init__(self, params=None, name="UET_Flash_Joule"):
        if params is None:
            params = get_params("0.28")
            
        super().__init__(
            nx=1, ny=1, dt=0.001, # 1ms steps
            params=params, name=name,
            topic="0.28_Material_Synthesis", pillar="01_Engine"
        )
        
        # Reactor Hardware
        self.voltage = 400.0        # Discharge voltage
        self.capacitance = 0.06     # 60mF capacitor bank
        self.resistance_ohm = 5.0   # Sample resistance
        
        # Material Properties (Carbon Black / Biochar)
        self.specific_heat_carbon = 0.710  # J/g/K
        self.graphitization_temp = 2800.0  # K
        self.sublimation_point = 3000.0    # K (volatiles leave)
        
        # State
        self.sample_mass_g = 0.5
        self.temperature_k = 300.0
        self.purity = 0.0
        self.yield_percent = 0.0
        
        self.results_history = []

    def step(self, step_idx: int = 0):
        if INTEGRITY_KILL_SWITCH:
            self.results_history.append({"tick": step_idx, "status": "KILLED"})
            return

        # Discharge energy for the first 10ms (10 ticks)
        energy_input_j = 0.0
        if step_idx < 10:
            # P = V^2 / R
            power_w = (self.voltage ** 2) / self.resistance_ohm
            energy_input_j = power_w * self.dt
            
            # Limit by capacitor bank capacity
            total_energy_stored = 0.5 * self.capacitance * (self.voltage ** 2)
            total_energy_used = sum([r.get("energy_j", 0) for r in self.results_history])
            if total_energy_used + energy_input_j > total_energy_stored:
                energy_input_j = max(0.0, total_energy_stored - total_energy_used)

        # Thermodynamics: dT = Q / (m * c)
        delta_t = energy_input_j / (self.sample_mass_g * self.specific_heat_carbon)
        self.temperature_k += delta_t
        
        # Cooling: Simple radiative/conductive approximation
        cooling_rate = 0.05 * (self.temperature_k - 300.0)
        self.temperature_k -= cooling_rate * self.dt
        
        # Purity & Yield Tracking
        if self.temperature_k > self.sublimation_point:
            self.purity = 0.99
        elif self.temperature_k > 2000.0:
            self.purity = max(self.purity, 0.80)
            
        if self.temperature_k > self.graphitization_temp:
            self.yield_percent = 0.95
        elif self.temperature_k > 2000.0:
            self.yield_percent = max(self.yield_percent, 0.30)
            
        res = {
            "tick": step_idx,
            "temp_k": self.temperature_k,
            "energy_j": energy_input_j,
            "purity": self.purity,
            "yield_percent": self.yield_percent
        }
        self.results_history.append(res)
        
        if (step_idx + 1) % 10 == 0:
            print(f"   [FLASH JOULE] Tick {step_idx+1} | Temp: {self.temperature_k:>6.1f} K | Yield: {self.yield_percent:>4.0%} | Purity: {self.purity:>4.0%}")

    def save_results(self):
        from docs.core.uet_glass_box import UETPathManager
        result_dir = UETPathManager.get_result_dir(
            topic_id="0.28_Material_Synthesis",
            experiment_name=self.name,
            pillar="01_Engine",
            category="log",
        )
        out_file = result_dir / "Flash_Joule_Synthesis.json"
        with open(out_file, "w") as f:
            json.dump(self.results_history, f, indent=2)
        return str(out_file)

if __name__ == "__main__":
    print(f"\n[START] UET FLASH JOULE ENGINE: Simulating Graphene Synthesis...")
    engine = UETFlashJouleEngine()
    engine.run(steps=50, verbose=True) # 50ms pulse/cool cycle
    path = engine.save_results()
    print(f"[SUCCESS] RESULTS SAVED: {path}\n")
