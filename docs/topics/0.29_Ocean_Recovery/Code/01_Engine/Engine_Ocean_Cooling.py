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

# --- OCEAN COOLING ENGINE ---

class UETOceanCoolingEngine(UETBaseSolver):
    """
    Simulates passive radiative cooling (PRC) thermal shields for coral protection.
    Models the heat balance between solar influx, convective exchange, and infrared emission.
    """
    def __init__(self, params=None, name="UET_Ocean_Cooling"):
        if params is None:
            params = get_params("0.29")
            
        super().__init__(
            nx=1, ny=1, dt=600, # 10-minute steps
            params=params, name=name,
            topic="0.29_Ocean_Recovery", pillar="01_Engine"
        )
        
        # Shield Properties
        self.area_m2 = 100.0
        self.emissivity_ir = 0.95
        self.solar_absorptance = 0.05 # 95% albedo
        
        # Environmental Constants
        self.sigma = 5.67e-8         # Stefan-Boltzmann
        self.sky_temp_k = 250.0      # Deep sky temp
        self.solar_flux_peak = 1000.0 # W/m^2
        self.water_mass_kg = 100.0 * 1.0 * 1025.0 # Top 1m layer
        self.c_water = 4186.0        # J/kg/K
        
        # State
        self.water_temp_k = 302.15   # 29°C (Bleaching threshold)
        self.ambient_air_k = 305.15  # 32°C ambient
        
        self.results_history = []

    def step(self, step_idx: int = 0):
        if INTEGRITY_KILL_SWITCH:
            self.results_history.append({"tick": step_idx, "status": "KILLED"})
            return

        # 1. Radiative Loss (Outgoing)
        p_rad = self.area_m2 * self.emissivity_ir * self.sigma * (self.water_temp_k**4 - self.sky_temp_k**4)
        
        # 2. Solar Input (Incoming)
        # Simple diurnal cycle (sine wave)
        diurnal_factor = max(0, np.sin(2 * np.pi * step_idx * self.dt / 86400))
        p_sun = self.area_m2 * self.solar_flux_peak * self.solar_absorptance * diurnal_factor
        
        # 3. Convective Exchange (Incoming/Outgoing)
        h_air = 10.0 # W/m^2 K
        p_conv = self.area_m2 * h_air * (self.ambient_air_k - self.water_temp_k)
        
        # 4. Net Balance (Applied to water mass)
        # mixing_efficiency accounts for currents bringing in warm water
        mixing_efficiency = 0.20
        p_net = (p_sun + p_conv - p_rad) * mixing_efficiency
        
        # 5. Update Temp
        delta_t = (p_net * self.dt) / (self.water_mass_kg * self.c_water)
        self.water_temp_k += delta_t
        
        res = {
            "tick": step_idx,
            "hour": (step_idx * self.dt) / 3600.0,
            "temp_c": self.water_temp_k - 273.15,
            "p_rad": p_rad,
            "p_sun": p_sun,
            "p_net": p_net
        }
        self.results_history.append(res)
        
        if (step_idx + 1) % 12 == 0: # Print every 2 hours
            print(f"   [OCEAN COOLING] Hour {res['hour']:>4.1f} | Temp: {res['temp_c']:>5.2f} °C | Net Power: {p_net:>6.1f} W")

    def save_results(self):
        from docs.core.uet_glass_box import UETPathManager
        result_dir = UETPathManager.get_result_dir(
            topic_id="0.29_Ocean_Recovery",
            experiment_name=self.name,
            pillar="01_Engine",
            category="log",
        )
        out_file = result_dir / "Ocean_Thermal_Recovery.json"
        with open(out_file, "w") as f:
            json.dump(self.results_history, f, indent=2)
        return str(out_file)

if __name__ == "__main__":
    print(f"\n[START] UET OCEAN COOLING ENGINE: Simulating Thermal Shield Efficacy...")
    engine = UETOceanCoolingEngine()
    engine.run(steps=144, verbose=True) # 24 hours simulation
    path = engine.save_results()
    print(f"[SUCCESS] RESULTS SAVED: {path}\n")
