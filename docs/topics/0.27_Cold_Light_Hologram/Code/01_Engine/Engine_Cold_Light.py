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

# --- ACOUSTO-OPTIC HOLOGRAPHY ENGINE ---

class UETColdLightEngine(UETBaseSolver):
    """
    Acousto-Optic Levitation & Haptics Engine.
    Simulates the physics of ultrasonic levitation for 3D holographic canvases.
    """
    def __init__(self, params=None, name="UET_Cold_Light"):
        if params is None:
            params = get_params("0.27")
            
        super().__init__(
            nx=1, ny=1, dt=0.01,
            params=params, name=name,
            topic="0.27_Cold_Light_Hologram", pillar="01_Engine"
        )
        
        # Environmental Constants (Air at 20C)
        self.rho_0 = 1.204  # Air density (kg/m^3)
        self.c_0 = 343.0    # Speed of sound in air (m/s)
        self.g = 9.81       # Gravity (m/s^2)

        # Transducer Array Settings
        self.frequency = 40000.0  # 40 kHz (Ultrasonic)
        self.wavelength = self.c_0 / self.frequency
        self.k = 2 * np.pi / self.wavelength # Wave number

        # Particle Settings (Lead-Free Perovskite Dust)
        self.particle_radius = 15e-6  # 15 micrometers
        self.particle_density = 4000.0 # ~4 g/cm^3
        
        self.results_history = []

    def calculate_levitation(self, pressure_amplitude):
        """
        Calculates if the acoustic pressure can levitate the particle.
        Using Gork'ov potential / Acoustic Radiation Force approximation.
        """
        # 1. Gravity Force
        volume = (4.0 / 3.0) * np.pi * (self.particle_radius ** 3)
        mass = volume * self.particle_density
        f_gravity = mass * self.g

        # 2. Max Acoustic Radiation Force
        # F_rad_max = (5*pi/6) * a^3 * (P0^2 / (rho0 * c0^2)) * k
        term1 = (5.0 * np.pi / 6.0) * (self.particle_radius ** 3)
        term2 = (pressure_amplitude ** 2) / (self.rho_0 * (self.c_0 ** 2))
        f_rad_max = term1 * term2 * self.k

        # 3. Levitation Check
        is_levitated = f_rad_max > f_gravity
        safety_factor = f_rad_max / f_gravity if f_gravity > 0 else 0

        # 4. Haptic Feedback (Force on a 1cm^2 fingertip)
        intensity = (pressure_amplitude ** 2) / (2 * self.rho_0 * self.c_0)
        finger_area = 1e-4 # 1 cm^2
        f_haptic = (2 * intensity / self.c_0) * finger_area
        f_haptic_mN = f_haptic * 1000.0

        if f_haptic_mN > 50.0:
            haptic_desc = "DANGER (Too Strong)"
        elif f_haptic_mN > 10.0:
            haptic_desc = "FIRM (Solid Object)"
        elif f_haptic_mN > 1.0:
            haptic_desc = "SOFT (Light Touch)"
        else:
            haptic_desc = "GHOST (Barely Felt)"

        return {
            "pressure_pa": pressure_amplitude,
            "f_gravity_N": f_gravity,
            "f_rad_max_N": f_rad_max,
            "is_levitated": is_levitated,
            "safety_factor": safety_factor,
            "f_haptic_mN": f_haptic_mN,
            "haptic_desc": haptic_desc
        }

    def step(self, step_idx: int = 0):
        if INTEGRITY_KILL_SWITCH:
            self.results_history.append({"tick": step_idx, "status": "KILLED"})
            return

        # Ramp up pressure amplitude
        p0 = 500.0 + (step_idx * 500.0)
        res = self.calculate_levitation(p0)
        res["tick"] = step_idx
        
        self.results_history.append(res)
        
        if (step_idx + 1) % 5 == 0:
            status_icon = "🔵" if res["is_levitated"] else "❌"
            print(f"   [COLD LIGHT] P0: {p0:>5.0f} Pa | {status_icon} SF: {res['safety_factor']:>5.1f} | Haptic: {res['f_haptic_mN']:>5.1f} mN")

    def save_results(self):
        from docs.core.uet_glass_box import UETPathManager
        result_dir = UETPathManager.get_result_dir(
            topic_id="0.27_Cold_Light_Hologram",
            experiment_name=self.name,
            pillar="01_Engine",
            category="log",
        )
        out_file = result_dir / "Acoustic_Levitation.json"
        with open(out_file, "w") as f:
            json.dump(self.results_history, f, indent=2)
        return str(out_file)

if __name__ == "__main__":
    print(f"\n[START] UET COLD LIGHT ENGINE: Simulating Levitation & Haptics...")
    engine = UETColdLightEngine()
    engine.run(steps=20, verbose=True)
    path = engine.save_results()
    print(f"[SUCCESS] RESULTS SAVED: {path}\n")


