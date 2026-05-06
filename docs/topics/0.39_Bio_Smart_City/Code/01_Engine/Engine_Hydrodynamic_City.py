"""
UET Bio-Smart City Engine (Topic 0.39)
================================================
Axiomatic simulation of Hydrodynamic Network Integration.
Models the transition from static concrete levees to dynamic flood-absorption infrastructure.
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

class UETHydrodynamicCityEngine(UETBaseSolver):
    """
    Simulates urban resilience against flood events.
    Compares traditional "Static Resistance" (concrete walls) vs UET "Hydrodynamic Routing" (absorption).
    """

    def __init__(self, params=None, name="UET_Bio_Smart_City"):
        if params is None:
            params = get_params("0.39")
            
        super().__init__(
            nx=1, ny=1, dt=1.0, # 1 Day per step
            params=params, name=name,
            topic="0.39_Bio_Smart_City", pillar="01_Engine"
        )
        
        # Environmental Forcing
        self.base_river_flow_m3_day = 1e6
        
        # Legacy Infrastructure (Static Concrete)
        self.static_levee_capacity_m3_day = 5e6
        
        # UET Infrastructure (Bio-Synthetic Levees & Reservoirs)
        self.bio_levee_capacity_m3_day = 4e6
        self.reservoir_absorption_rate = 0.5 # 50% of excess water is routed to agriculture/cooling
        self.max_reservoir_capacity_m3 = 50e6
        
        # State
        self.current_reservoir_volume_m3 = 0.0
        self.legacy_damage_cost_usd = 0.0
        self.uet_damage_cost_usd = 0.0
        self.uet_agricultural_value_usd = 0.0
        
        self.damage_multiplier = 100.0 # $100 per m3 of floodwater overflow
        self.agri_value_multiplier = 2.0 # $2 per m3 of routed water utilized
        
        self.results_history = []

    def simulate_flood_event(self, day: int) -> float:
        """
        Simulates seasonal monsoon spikes.
        """
        # Create a massive 10-day flood peak around day 30
        if 25 <= day <= 35:
            # Peak at 10 million m3/day (double the static levee capacity)
            return self.base_river_flow_m3_day + 9e6 * np.sin(np.pi * (day - 25) / 10.0)
        return self.base_river_flow_m3_day

    def step(self, step_idx: int = 0):
        if INTEGRITY_KILL_SWITCH:
            self.results_history.append({"legacy_cost": np.nan, "uet_cost": np.nan})
            return

        inflow = self.simulate_flood_event(step_idx)
        
        # 1. Legacy Static System
        legacy_overflow = max(0.0, inflow - self.static_levee_capacity_m3_day)
        if legacy_overflow > 0:
            # Concrete failure is often catastrophic. We model a 1.5x penalty for breach.
            self.legacy_damage_cost_usd += (legacy_overflow * self.damage_multiplier * 1.5)
            
        # 2. UET Hydrodynamic System
        uet_overflow = max(0.0, inflow - self.bio_levee_capacity_m3_day)
        routed_water = 0.0
        
        if uet_overflow > 0:
            # Attempt to absorb excess
            available_space = self.max_reservoir_capacity_m3 - self.current_reservoir_volume_m3
            absorbable = uet_overflow * self.reservoir_absorption_rate
            actually_absorbed = min(absorbable, available_space)
            
            self.current_reservoir_volume_m3 += actually_absorbed
            routed_water = actually_absorbed
            
            # Remaining overflow causes damage (but levees don't catastrophically breach due to bio-synthetic healing)
            remaining_overflow = uet_overflow - actually_absorbed
            self.uet_damage_cost_usd += (remaining_overflow * self.damage_multiplier)
            
        # Utilize stored water over time
        if self.current_reservoir_volume_m3 > 0:
            utilized = min(self.current_reservoir_volume_m3, 5e5) # Use 500,000 m3 per day
            self.current_reservoir_volume_m3 -= utilized
            self.uet_agricultural_value_usd += (utilized * self.agri_value_multiplier)
            
        # Calculate net economic position for UET
        uet_net_cost = self.uet_damage_cost_usd - self.uet_agricultural_value_usd

        self.results_history.append({
            "day": step_idx,
            "inflow": inflow,
            "legacy_overflow": legacy_overflow,
            "legacy_cumulative_damage": self.legacy_damage_cost_usd,
            "uet_cumulative_damage": self.uet_damage_cost_usd,
            "uet_agricultural_value": self.uet_agricultural_value_usd,
            "uet_net_cost": uet_net_cost
        })
        
        if (step_idx + 1) % 10 == 0:
            print(f"   [BIO-CITY] Day {step_idx+1} | Inflow: {inflow/1e6:.1f}M m3 | Legacy Dmg: ${self.legacy_damage_cost_usd/1e6:.1f}M | UET Net: ${uet_net_cost/1e6:.1f}M")

    def save_results(self):
        import json
        from pathlib import Path
        Path(self.logger.run_dir).mkdir(parents=True, exist_ok=True)
        out_path = Path(self.logger.run_dir) / "hydrodynamic_city_analysis.json"
        with open(out_path, "w") as f:
            json.dump(self.results_history, f, indent=2)
        return str(out_path)

if __name__ == "__main__":
    print(f"\n🚀 UET BIO-SMART CITY: Simulating 60-Day Monsoon Season...")
    engine = UETHydrodynamicCityEngine()
    engine.run(steps=60, verbose=True) # Run for 60 Days
    path = engine.save_results()
    
    # Final Report
    leg_cost = engine.legacy_damage_cost_usd
    uet_net = engine.uet_damage_cost_usd - engine.uet_agricultural_value_usd
    
    print(f"\n[URBAN RESILIENCE REPORT]")
    print(f"Legacy Concrete Damage : ${leg_cost/1e6:,.1f} Million")
    print(f"UET Hydrodynamic Net   : ${uet_net/1e6:,.1f} Million")
    if uet_net < leg_cost:
        savings = leg_cost - uet_net
        print(f"✅ PASS: UET City Architecture saved ${savings/1e6:,.1f} Million during catastrophic flood event.")
    else:
        print(f"❌ FAIL: Hydrodynamic routing failed to offset damage costs.")
        
    print(f"✅ Result Saved: {path}\n")
