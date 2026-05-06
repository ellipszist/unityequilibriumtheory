"""
UET Bio-Synthetic Integration Engine (Topic 0.38)
================================================
Axiomatic simulation of Accelerated Biomineralization for self-healing infrastructure.
Models Hydroxyapatite crystallization accelerated by acoustic frequencies and metabolic repair.
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

class UETBioSyntheticEngine(UETBaseSolver):
    """
    Simulates Bio-Synthetic Material integrity over time.
    Compares Closed-System (Metal) decay vs Open-System (Acoustic Bone) growth/repair.
    """

    def __init__(self, params=None, name="UET_Bio_Synthetic"):
        if params is None:
            params = get_params("0.38")
            
        super().__init__(
            nx=1, ny=1, dt=1.0, # 1 Year per step for macroscopic structural simulation
            params=params, name=name,
            topic="0.38_Bio_Synthetic_Integration", pillar="01_Engine"
        )
        
        # System constraints
        self.max_integrity = 1.0
        self.metal_decay_rate = 0.03 # 3% structural fatigue per year
        self.wear_rate = 0.02        # 2% entropy/wear per year on the hybrid hull
        
        # Acoustic / Biomineralization constraints
        self.acoustic_power = 50.0   # 50 W applied locally for crystallization
        self.nutrient_flux = 1.0     # Normalized nutrient supply rate
        
        # State
        self.metal_integrity = 1.0   # Starts perfect, decays
        self.bone_integrity = 0.1    # Starts as a scaffold, grows to 1.0
        
        self.results_history = []

    def calculate_acoustic_crystallization(self, current_integrity: float) -> float:
        """
        Acoustically driven crystallization of Hydroxyapatite.
        Growth Rate = k * Nutrient_Flux * Acoustic_Power * (1 - Integrity/Max)
        """
        # UET Information transfer constant
        k_growth = 0.005 * self.params.beta
        
        # Logistic growth curve bounded by available space/nutrients
        space_remaining = max(0.0, self.max_integrity - current_integrity)
        growth = k_growth * self.nutrient_flux * self.acoustic_power * space_remaining
        
        return float(growth)

    def step(self, step_idx: int = 0):
        if INTEGRITY_KILL_SWITCH:
            self.results_history.append({"metal": np.nan, "bone": np.nan})
            return

        # 1. Closed-System Metal Decay (Entropy)
        self.metal_integrity *= np.exp(-self.metal_decay_rate * self.dt)
        
        # 2. Open-System Bio-Bone Repair (Metabolism)
        growth = self.calculate_acoustic_crystallization(self.bone_integrity) * self.dt
        wear = self.wear_rate * self.bone_integrity * self.dt
        
        self.bone_integrity += (growth - wear)
        self.bone_integrity = min(self.bone_integrity, self.max_integrity)
        
        self.results_history.append({
            "year": step_idx,
            "metal_integrity": self.metal_integrity,
            "bone_integrity": self.bone_integrity
        })
        
        if (step_idx + 1) % 10 == 0:
            print(f"   [BIO-SYNTHETIC] Year {step_idx+1} | Metal: {self.metal_integrity:.1%} | Bone Hull: {self.bone_integrity:.1%}")

    def save_results(self):
        import json
        from pathlib import Path
        Path(self.logger.run_dir).mkdir(parents=True, exist_ok=True)
        out_path = Path(self.logger.run_dir) / "bio_growth_comparison.json"
        with open(out_path, "w") as f:
            json.dump(self.results_history, f, indent=2)
        return str(out_path)

if __name__ == "__main__":
    print(f"\n🚀 UET BIO-SYNTHETIC INTEGRATION: Simulating 50 Years...")
    engine = UETBioSyntheticEngine()
    engine.run(steps=50, verbose=True) # Run for 50 Years
    path = engine.save_results()
    
    # Extract year 30 results for benchmark
    try:
        metal_30 = engine.results_history[29]["metal_integrity"]
        bone_30 = engine.results_history[29]["bone_integrity"]
        adv = bone_30 / metal_30
        print(f"\n[INTEGRITY REPORT @ YEAR 30]")
        print(f"Legacy Metal Chassis: {metal_30:.1%} (Needs Replacement)")
        print(f"Bio-Synthetic Bone  : {bone_30:.1%} (Self-Maintained)")
        if adv > 2.0:
            print(f"✅ PASS: Bio-Synthetic structural advantage confirmed (>2x life).")
        else:
            print(f"❌ FAIL: Metabolic repair rates insufficient.")
    except Exception as e:
        print("Error evaluating benchmark:", e)
        
    print(f"✅ Result Saved: {path}\n")
