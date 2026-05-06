import sys
from pathlib import Path
import numpy as np
import json
import math

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
from docs.core.uet_parameters import get_params, INTEGRITY_KILL_SWITCH, G, C, HBAR, K_B

# --- SPACE-TIME PROPULSION ENGINE ---

class UETSlingshotEngine(UETBaseSolver):
    """
    Simulates a Singularity Gravitational Slingshot (SGS).
    Models relativistic acceleration, Hawking radiation decay, and bio-hull integrity.
    """
    def __init__(self, params=None, name="UET_Slingshot"):
        if params is None:
            params = get_params("0.31")
            
        super().__init__(
            nx=1, ny=1, dt=0.01,
            params=params, name=name,
            topic="0.31_SpaceTime_Propulsion", pillar="01_Engine"
        )
        
        # Physics Constants
        self.G = G
        self.c = C
        
        # Ship & Environment
        self.ship_mass = 500000.0  # kg
        self.singularity_mass = 1e12 # kg
        self.periapsis = 1e5       # m
        
        # State
        self.velocity = 11000.0    # m/s (Starting orbital velocity)
        self.bio_integrity = 100.0 # Percent
        self.energy_joules = 1e15  # 1 Petajoule
        
        self.results_history = []

    def get_lorentz_factor(self):
        beta = self.velocity / self.c
        if beta >= 0.999999: return 1000.0
        return 1.0 / np.sqrt(1.0 - beta**2)

    def step(self, step_idx: int = 0):
        if INTEGRITY_KILL_SWITCH or self.bio_integrity <= 0 or self.energy_joules <= 0:
            self.results_history.append({"tick": step_idx, "status": "FAILED/KILLED"})
            return

        gamma = self.get_lorentz_factor()
        
        # 1. Gravitational Acceleration (Relativistic Correction)
        # Accel drops as ship approaches c relative to singularity
        accel_raw = (self.G * self.singularity_mass) / (self.periapsis**2)
        accel_phys = accel_raw / (gamma**3) # Transverse/Radial acceleration scaling
        
        self.velocity += accel_phys * self.dt
        
        # 2. Hull Stress & Energy Drain
        # Damage increases with gamma and acceleration
        stress = (gamma - 1.0) * 0.1 + (accel_phys / 1e6) * 0.01
        self.bio_integrity -= stress * self.dt
        
        # Active Repair Cost (Landauer Limit approx)
        if self.bio_integrity < 95.0:
            repair_rate = 0.5 # % per sec
            repair_energy_cost = 1e12 * repair_rate # 1 Terajoule per %
            self.bio_integrity += repair_rate * self.dt
            self.energy_joules -= repair_energy_cost * self.dt

        res = {
            "tick": step_idx,
            "velocity_ms": self.velocity,
            "gamma": gamma,
            "bio_integrity": self.bio_integrity,
            "energy_petajoules": self.energy_joules / 1e15
        }
        self.results_history.append(res)
        
        if (step_idx + 1) % 100 == 0:
            print(f"   [SLINGSHOT] Step {step_idx+1} | V: {self.velocity/1000:>6.1f} km/s | Gamma: {gamma:>6.3f} | Bio: {self.bio_integrity:>5.1f}%")

    def save_results(self):
        from docs.core.uet_glass_box import UETPathManager
        result_dir = UETPathManager.get_result_dir(
            topic_id="0.31_SpaceTime_Propulsion",
            experiment_name=self.name,
            pillar="01_Engine",
            category="log",
        )
        out_file = result_dir / "Singularity_Slingshot.json"
        with open(out_file, "w") as f:
            json.dump(self.results_history, f, indent=2)
        return str(out_file)

if __name__ == "__main__":
    print(f"\n[START] UET SLINGSHOT ENGINE: Simulating Relativistic Acceleration...")
    engine = UETSlingshotEngine()
    engine.run(steps=1000, verbose=True) # 10s of high-G maneuver
    path = engine.save_results()
    print(f"[SUCCESS] RESULTS SAVED: {path}\n")
