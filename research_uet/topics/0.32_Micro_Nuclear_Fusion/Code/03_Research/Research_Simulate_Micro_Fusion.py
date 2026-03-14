import numpy as np
import matplotlib.pyplot as plt
import sys
from pathlib import Path

# Setup paths for importing UET core modules if needed
PROJECT_ROOT = Path(__file__).resolve().parents[5]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

from research_uet.core.uet_parameters import get_params, K_B

class MicroFusionSimulator:
    """
    Simulates the UET-guided Micro Nuclear Fusion process.
    Models the energy output of fusion events within a Graphene confinement tube
    and the direct energy conversion efficiency of a Perovskite layer.
    """
    
    def __init__(self):
        # Base Parameters
        self.k_b = K_B
        self.room_temp = 300  # K
        
        # Traditional Fusion Parameters (D-T fusion baseline)
        self.traditional_barrier_ev = 1e5  # Approx 100 keV for D-T
        self.traditional_cross_section = 5.0  # barns (max at ~64 keV)
        
        # UET Confinement Parameters
        self.graphene_q_factor = 1e5  # Quality factor of the graphene lattice resonance
        self.resonance_coupling = 0.98 # How well UET field couples to nuclei
        self.perovskite_efficiency = 0.85 # Direct conversion efficiency (theoretical max ~ 85-90%)
        
        # Fuel Types: (Barrier in eV, Energy released per fusion in eV)
        # Note: Barriers are approximations for the Coulomb barrier peak
        self.fuels = {
            "D-T": {"barrier": 1e5, "energy_ev": 17.6e6, "desc": "Deuterium-Tritium (Baseline)"},
            "D-D": {"barrier": 4e5, "energy_ev": 3.65e6, "desc": "Deuterium-Deuterium (Abundant)"},
            "p-B11": {"barrier": 6e5, "energy_ev": 8.7e6, "desc": "Proton-Boron (Aneutronic / Safe)"}
        }
        self.current_fuel = "p-B11" # We target p-B11 for safe micro-devices
        
        # Derived UET Effects for current fuel
        self.update_fuel(self.current_fuel)
        
        # Thermal Quenching Limit (Fail-Safe Mechanism)
        self.quenching_temperature_k = 1500  # Above 1500K, UET resonance collapses
        
    def update_fuel(self, fuel_name):
        self.current_fuel = fuel_name
        self.traditional_barrier_ev = self.fuels[fuel_name]["barrier"]
        self.uet_barrier_ev = self.traditional_barrier_ev * (1.0 - self.resonance_coupling)
        
    def calculate_fusion_probability(self, temp_k, use_uet=False):
        """
        Calculates the relative probability of a fusion event based on temperature and barrier.
        Uses a simplified Gamow factor approximation modified by UET resonance.
        """
        energy_ev = self.k_b * temp_k  # Thermal energy in eV
        
        barrier = self.uet_barrier_ev if use_uet else self.traditional_barrier_ev
        
        # Simplified probability (exponential decay based on barrier vs thermal energy)
        # In reality, this involves quantum tunneling (Gamow window).
        # We model the UET enhancement as a massive reduction in the effective barrier.
        
        if energy_ev <= 0: return 0.0
        
        # UET Resonance Multiplier (Phi_UET)
        phi_uet = 1.0
        if use_uet:
            # Thermal Quenching (Safety Mechanism):
            # If the temperature gets too high, the lattice deforms, resonance breaks,
            # and the Coulomb barrier returns to normal (reaction stops).
            if temp_k > self.quenching_temperature_k:
                return 0.0 # Instant shutdown
            
            # At resonance (omega/omega0 = 1), the multiplier is proportional to Q-factor
            phi_uet = 1.0 + self.graphene_q_factor
            
        # Standard exponential decay + UET multiplier
        prob = np.exp(-barrier / energy_ev) * phi_uet
        
        # Cap probability at 1.0 for simplicity
        return min(prob, 1.0)

    def simulate_power_output(self, temps_k, num_tubes=1):
        """
        Simulates the power output (Watts) across different temperatures for a given scale.
        """
        energy_ev = self.fuels[self.current_fuel]["energy_ev"]
        energy_per_fusion_j = energy_ev * 1.602e-19  # Joules
        
        # Assume a base collision rate inside a single micro-tube
        collision_rate_per_tube = 1e12  # collisions per second
        total_collision_rate = collision_rate_per_tube * num_tubes
        
        power_trad = []
        power_uet = []
        
        for t in temps_k:
            prob_trad = self.calculate_fusion_probability(t, use_uet=False)
            prob_uet = self.calculate_fusion_probability(t, use_uet=True)
            
            # Raw power = events * energy per event
            p_trad = (prob_trad * total_collision_rate) * energy_per_fusion_j
            
            # UET power includes Perovskite direct conversion efficiency
            p_uet = (prob_uet * total_collision_rate) * energy_per_fusion_j * self.perovskite_efficiency
            
            power_trad.append(p_trad)
            power_uet.append(p_uet)
            
        return np.array(power_trad), np.array(power_uet)

    def print_scaling_economics(self):
        print("\n--- Scaling & Economics (Aneutronic p-B11) ---")
        energy_j = self.fuels["p-B11"]["energy_ev"] * 1.602e-19
        
        # Under active UET resonant stimulation (acoustic/EM), the effective probability 
        # is no longer strictly thermal. We assume a conservative fusion probability 
        # per collision under perfect phase-lock resonance.
        active_uet_prob = 1e-8  # 1 event per 100 million collisions when "turned on"
        watts_per_tube = active_uet_prob * 1e12 * energy_j * self.perovskite_efficiency
        
        print(f"Theoretical Power output per Micro-Tube (Active Resonance): {watts_per_tube:.2e} Watts")
        
        scales = {
            "Smartphone Chip (1 cm^2)": 1e8,   # 100 million tubes
            "Laptop / Drone Size": 1e9,        # 1 billion tubes
            "EV Battery Size": 1e10,           # 10 billion tubes
            "Industrial Grid Module": 1e12,    # 1 trillion tubes
            "City-Scale Monolith (100m^3)": 1e18, # 1 Quintillion tubes
            "Stellar-Class Core (Topic 0.31)": 1e22 # For SpaceTime Propulsion (Black Hole Gen)
        }
        
        for name, num_tubes in scales.items():
            power = watts_per_tube * num_tubes
            if power < 1:
                power_str = f"{power*1000:.2f} mW"
            elif power < 1000:
                power_str = f"{power:.2f} W"
            elif power < 1e6:
                power_str = f"{power/1000:.2f} kW"
            elif power < 1e9:
                power_str = f"{power/1e6:.2f} MW"
            elif power < 1e12:
                power_str = f"{power/1e9:.2f} GW (Gigawatts)"
            elif power < 1e15:
                power_str = f"{power/1e12:.2f} TW (Terawatts)"
            else:
                power_str = f"{power/1e15:.2f} PW (Petawatts)"
                
            print(f"- {name} ({num_tubes:.0e} tubes): ~ {power_str}")
        
        print("\nCost Breakdown:")
        print("- Graphene Lattice: Extremely cheap (Carbon-based, synthesized via sound/CVD).")
        print("- Perovskite Layer: Low cost, easily painted/printed.")
        print("- Fuel (Boron/Hydrogen): Essentially free compared to Tritium or Uranium.")
        print("- Total estimated cost: Pennies per cm^2 once mass-produced.")

    def run_comparison(self):
        """
        Runs the simulation and generates a comparison plot.
        """
        print("=== UET Micro Nuclear Fusion Simulation ===")
        print(f"Fuel Type: {self.fuels[self.current_fuel]['desc']}")
        print(f"Traditional Coulomb Barrier: {self.traditional_barrier_ev/1e3:.1f} keV")
        print(f"UET Resonant Barrier:      {self.uet_barrier_ev/1e3:.1f} keV")
        print(f"Perovskite Conversion Eff: {self.perovskite_efficiency*100:.1f} %")
        
        # Temperature range from Room Temp (300K) to 100 Million K
        # We use a log scale for temperature to capture the massive difference
        temps_k = np.logspace(2, 8, 100) 
        
        p_trad, p_uet = self.simulate_power_output(temps_k)
        
        # Plotting
        plt.figure(figsize=(10, 6))
        
        # Plot UET Power
        plt.plot(temps_k, p_uet, label='UET Micro-Fusion (Perovskite Direct)', color='blue', linewidth=2)
        
        # Plot Traditional Power
        plt.plot(temps_k, p_trad, label='Traditional Fusion (Raw Output)', color='red', linestyle='--')
        
        # Formatting
        plt.xscale('log')
        plt.yscale('log')
        plt.xlabel('Temperature (Kelvin)')
        plt.ylabel('Power Output per Micro-Tube (Watts)')
        plt.title('Fusion Power Output: UET Micro-Reactor vs Traditional')
        plt.grid(True, which="both", ls="-", alpha=0.2)
        plt.legend()
        
        # Highlight regions
        plt.axvspan(300, 1000, color='green', alpha=0.1, label='Room Temp / Low Energy Range')
        plt.axvline(1e8, color='orange', linestyle=':', label='Traditional Tokamak Temp')
        
        # Ensure Result directory exists
        result_dir = Path(__file__).parent.parent.parent / "Result"
        result_dir.mkdir(parents=True, exist_ok=True)
        
        save_path = result_dir / "micro_fusion_comparison.png"
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"\nSimulation complete. Plot saved to: {save_path}")
        
        # Find ignition temperature (where power > 1 microWatt for example)
        target_power = 1e-6
        uet_ignition_idx = np.argmax(p_uet > target_power)
        trad_ignition_idx = np.argmax(p_trad > target_power)
        
        print("\n--- Results ---")
        if uet_ignition_idx > 0:
            print(f"UET Ignition Temp (>1µW): ~{temps_k[uet_ignition_idx]:.2e} K")
        if trad_ignition_idx > 0:
            print(f"Traditional Ignition Temp (>1µW): ~{temps_k[trad_ignition_idx]:.2e} K")
        else:
            print(f"Traditional Ignition Temp (>1µW): Off the chart (>1e8 K)")
            
        self.print_scaling_economics()

if __name__ == "__main__":
    sim = MicroFusionSimulator()
    sim.run_comparison()
