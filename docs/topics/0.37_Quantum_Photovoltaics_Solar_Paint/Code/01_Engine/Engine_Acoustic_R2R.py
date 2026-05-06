"""
UET Solar Paint Engine (Topic 0.37)
================================================
Axiomatic simulation of Acoustic Roll-to-Roll (R2R) Perovskite manufacturing.
Models the tradeoff between Roll Speed and Acoustic Crystal Alignment.
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

class UETAcousticR2REngine(UETBaseSolver):
    """
    Simulates a Roll-to-Roll manufacturing line for Perovskite Solar Paint.
    Uses Acoustic Waves (SAW) to align the crystal lattice before it dries.
    """

    def __init__(self, params=None, name="UET_Acoustic_R2R"):
        if params is None:
            params = get_params("0.37")
            
        super().__init__(
            nx=1, ny=1, dt=0.1, 
            params=params, name=name,
            topic="0.37_Quantum_Photovoltaics", pillar="01_Engine"
        )
        
        # Line Parameters
        self.acoustic_zone_length_m = 5.0  # 5 meters of active acoustic vibration
        self.roll_speed_m_s = 0.5          # Initial speed: 0.5 meters per second
        self.acoustic_power_w = 10000.0    # 10 kW acoustic field
        
        # Material Constraints
        self.baseline_efficiency = 0.12    # 12% without alignment
        self.max_theoretical_efficiency = 0.33 # 33% Shockley-Queisser limit approx
        
        self.results_history = []

    def calculate_crystal_alignment(self, roll_speed: float, power: float) -> float:
        """
        Calculates the degree of crystal lattice perfection.
        Time in zone = Length / Speed
        Alignment = 1.0 - exp(-k * Time * Power)
        """
        if roll_speed <= 0:
            return 1.0
            
        time_in_zone = self.acoustic_zone_length_m / roll_speed
        
        # k is a kinetic constant related to perovskite mobility and UET beta
        # We tie it to information coupling (beta)
        k = 1e-5 * self.params.beta 
        
        alignment = 1.0 - np.exp(-k * time_in_zone * power)
        return float(alignment)

    def calculate_solar_efficiency(self, alignment: float) -> float:
        """
        Maps crystal alignment to photovoltaic power conversion efficiency (PCE).
        """
        # Efficiency scales logarithmically or linearly with alignment quality
        efficiency = self.baseline_efficiency + (self.max_theoretical_efficiency - self.baseline_efficiency) * alignment
        
        # Encapsulation penalty (Graphene absorbs ~2.3% of light per layer. We use 2 layers)
        graphene_transmission = (1.0 - 0.023)**2 
        
        final_efficiency = efficiency * graphene_transmission
        return float(final_efficiency)

    def optimize_line_speed(self, target_efficiency: float = 0.25) -> float:
        """
        Finds the maximum roll speed that maintains the target efficiency.
        """
        test_speeds = np.linspace(0.1, 10.0, 100)
        best_speed = 0.1
        
        for speed in test_speeds:
            align = self.calculate_crystal_alignment(speed, self.acoustic_power_w)
            eff = self.calculate_solar_efficiency(align)
            if eff >= target_efficiency:
                best_speed = speed
            else:
                break
                
        return best_speed

    def step(self, step_idx: int = 0):
        if INTEGRITY_KILL_SWITCH:
            self.results_history.append({"speed": np.nan, "efficiency": np.nan, "yield_m2_hr": np.nan})
            return

        # Increase roll speed over time to test limits
        current_speed = 0.1 + (step_idx * 0.01)
        
        alignment = self.calculate_crystal_alignment(current_speed, self.acoustic_power_w)
        efficiency = self.calculate_solar_efficiency(alignment)
        
        # Yield = Speed * Width (Assume 2m wide roll) * 3600 seconds
        yield_m2_hr = current_speed * 2.0 * 3600.0
        
        self.results_history.append({
            "tick": step_idx,
            "speed_m_s": current_speed,
            "alignment": alignment,
            "efficiency": efficiency,
            "yield_m2_hr": yield_m2_hr
        })
        
        if (step_idx + 1) % 50 == 0:
            print(f"   [R2R ENGINE] Speed: {current_speed:.2f} m/s | Efficiency: {efficiency:.1%} | Yield: {yield_m2_hr:,.0f} m^2/hr")

    def save_results(self):
        import json
        from pathlib import Path
        Path(self.logger.run_dir).mkdir(parents=True, exist_ok=True)
        out_path = Path(self.logger.run_dir) / "r2r_analysis.json"
        with open(out_path, "w") as f:
            json.dump(self.results_history, f, indent=2)
        return str(out_path)

if __name__ == "__main__":
    print(f"\n🚀 UET SOLAR PAINT: Simulating Acoustic R2R Production...")
    engine = UETAcousticR2REngine()
    
    optimal_speed = engine.optimize_line_speed(target_efficiency=0.25)
    print(f"🎯 Optimal Speed for 25% Efficiency: {optimal_speed:.2f} m/s")
    
    engine.run(steps=200, verbose=True) 
    path = engine.save_results()
    print(f"✅ R2R Result: {path}\n")
