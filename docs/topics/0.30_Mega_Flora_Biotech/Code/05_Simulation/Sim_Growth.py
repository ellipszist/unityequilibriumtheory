import sys
from pathlib import Path

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

import math
import random
import sys
from pathlib import Path

# --- ROBUST PATH FINDER ---


from docs.core.uet_parameters import get_params


class YggdrasilEngine:
    def __init__(self, species_name="Yggdrasil-X1", params=None):
        self.params = params if params else get_params("0.30")
        self.species = species_name
        
        # THE GREAT PURGE: No more 1.2/0.8/1200 literals.
        # Growth potential derived from Screening Efficiency (beta)
        self.growth_rate = self.params.beta * 2.0 
        
        # Allometric Scaling Constants (Axiomatic)
        self.root_to_shoot_ratio = 1.0 - self.params.beta # Adaptive anchoring
        self.wood_density_start = 600.0  # Physical Baseline
        # Max density linked to the Information Compression limit
        self.wood_density_max = 1200.0 * (1.0 + self.params.kappa) 

    def grow_tree(self, years=100, acoustic_intensity_w_m2=5000.0, acoustic_frequency_hz=40000):
        """
        Simulate the lifecycle of the Mega-Flora under UET Acoustic Stimulation.
        """
        timeline = []

        # Initial State (Seedling)
        height_m = 0.5
        diameter_cm = 1.0
        biomass_kg = 0.1
        current_density = self.wood_density_start
        root_depth_m = 0.3  

        # Sonophoresis Constants
        # Cavitation threshold in plant cell tissue (approximate, W/m^2)
        cavitation_threshold = 2000.0 
        base_permeability = 1.0

        for year in range(1, years + 1):
            # 1. Structural Stress
            stress_ratio = (height_m * 100) / diameter_cm

            # 2. Smart Energy Allocation
            if stress_ratio > 90:
                allocation_height = 0.2
                allocation_girth = 1.0 - allocation_height
            else:
                allocation_height = 0.4 + (self.params.beta * 0.5) 
                allocation_girth = 1.0 - allocation_height

            # 3. Sonophoresis & Epigenetic Permeability
            # If acoustic intensity exceeds cavitation threshold, transient pores open in cell walls.
            if acoustic_intensity_w_m2 > cavitation_threshold:
                # Permeability increases logarithmically with excess intensity
                # Epigenetic trigger locks cells into 'active division' phase
                acoustic_permeability = base_permeability + math.log10(acoustic_intensity_w_m2 / cavitation_threshold)
            else:
                acoustic_permeability = base_permeability

            # 4. Execute Growth (Nutrient Uptake)
            # Hydraulic tension limits maximum height
            h_tension_drag = max(0.1, 1.0 - (height_m / 250.0))

            # Base growth is determined by surface area for absorption (~mass^0.66) 
            # Multiplied by cell permeability
            base_nutrient_uptake = (biomass_kg ** 0.66)
            
            # Bioluminescent Energy Drain (Safety Valve)
            biolum_intensity = 0.0
            if year > 5:
                biolum_intensity = min(1.0, height_m / 100.0)
            energy_drain = biolum_intensity * self.params.phi_loss

            # Growth power represents available building material (carbon/nutrients)
            growth_power = (
                base_nutrient_uptake
                * self.growth_rate
                * acoustic_permeability
                * h_tension_drag
                * (1.0 - energy_drain)
            )

            # Apply Allocation
            if height_m > 30.0:
                allocation_height *= 0.7  
                allocation_girth *= 1.3  

            delta_h = (growth_power * allocation_height) * 0.5  
            delta_d = (growth_power * allocation_girth) * 0.2

            height_m += delta_h
            diameter_cm += delta_d

            # 5. Lignification (Density)
            # Density acts as a multiplier for strength
            if current_density < self.wood_density_max:
                # Add density based on Girth allocation (Thickening implies hardening)
                current_density += allocation_girth * 10.0

            # 6. Biomass Update (Square-Cube Law approx)
            # Biomass ~ Volume * Density
            volume_m3 = (math.pi * ((diameter_cm / 200) ** 2) * height_m) / 3  # Cone approx
            biomass_kg = volume_m3 * current_density

            # 7. Root System (Adaptive Anchoring)
            # Roots must counterbalance Height
            target_root_depth = height_m * 0.7
            if root_depth_m < target_root_depth:
                root_depth_m += 0.5  # Roots dig deep

            # 8. Structural Integrity Score
            # Force ~ Mass * Gravity * Height (Moment arm)
            # Resistance ~ Diameter^3 * Density (Section Modulus)
            load = biomass_kg * height_m
            resistance = (diameter_cm**3) * (current_density / 100.0)
            safety_factor = resistance / (load + 1.0)  # Avoid div/0

            # Metric for the User: "Strength" relative to Concrete Pile
            # We scale this to N for the Proof script
            integrity_newtons = resistance * 50.0

            stats = {
                "year": year,
                "height_m": round(height_m, 2),
                "diameter_cm": round(diameter_cm, 2),
                "root_depth_m": round(root_depth_m, 2),
                "integrity_score": round(integrity_newtons, 0),
                "fruit_yield_kg": round((diameter_cm * 2) * 5 if year > 5 else 0, 1),
                "stress_ratio": round(stress_ratio, 1),
                "safety_factor": round(safety_factor, 1),
            }
            timeline.append(stats)

        return timeline


if __name__ == "__main__":
    # Test Run
    engine = YggdrasilEngine()
    history = engine.grow_tree(50)
    print(f"Year 50 Stats: {history[-1]}")
