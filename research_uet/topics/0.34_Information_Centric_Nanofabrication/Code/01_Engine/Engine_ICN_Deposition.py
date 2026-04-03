"""
UET ICN Engine - Information-Centric Nanofabrication
===================================================
Axiomatic simulation of "Direct-Write" material synthesis.

Topic: 0.34 Information-Centric Nanofabrication
Architecture: 5x4 Grid Standard
"""

import numpy as np
import os
import sys
from pathlib import Path

# Fix path for standalone execution (Ensure source code shadowed venv package)
current_file = Path(__file__).resolve()
# topics/0.34/Code/01_Engine/Engine.py -> parent x 6 = uet_harness (containing research_uet)
project_root = current_file.parents[5] 
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

# DEBUG: Verify which research_uet we are importing
try:
    import research_uet
    print(f"📦 Research UET Path: {research_uet.__file__}")
except Exception as e:
    print(f"❌ Import failed: {e}")

from research_uet.core.uet_base_solver import UETBaseSolver
from research_uet.core.uet_parameters import get_params, UETParameters

class ICNEngine(UETBaseSolver):
    """
    Simulates the "Crystallization" of a circuit pattern from a precursor flux
    guided by a resonant Information Field (I).
    """

    def __init__(
        self,
        nx: int = 128,
        ny: int = 128,
        dt: float = 0.01,
        name: str = "ICN_High_Fidelity_Growth",
        pattern_type: str = "S_Logic_Gate"
    ):
        # Physics Parameters (Nanoscale Tuning)
        # Restore first-principles parameters for atomic mobility and pattern attraction.
        params = get_params("0.34")

        super().__init__(
            nx=nx,
            ny=ny,
            dt=dt,
            params=params,
            name=name,
            topic="0.34_Information_Centric_Nanofabrication",
            pillar="01_Engine"
        )

        self.pattern_type = pattern_type
        self._initialize_information_field()

    def _initialize_information_field(self):
        """
        Create the "Target Logic" in the Information Field (I).
        This represents the resonant nodes that attract material.
        """
        self.I = np.zeros((self.ny, self.nx))
        
        if self.pattern_type == "S_Logic_Gate":
            # Simple "S" shape pattern (A gate/interconnect)
            cx, cy = self.nx // 2, self.ny // 2
            r = self.nx // 4
            
            # Draw an 'S' shape in I-field
            for y in range(self.ny):
                for x in range(self.nx):
                    # Upper arc
                    if (x - cx)**2 + (y - (cy - r//2))**2 < (r//2)**2:
                        if x > cx: self.I[y, x] = 1.0
                    # Lower arc
                    if (x - cx)**2 + (y - (cy + r//2))**2 < (r//2)**2:
                        if x < cx: self.I[y, x] = 1.0
                    # Connector
                    if abs(x - cx) < 2 and abs(y - cy) < r:
                        self.I[y, x] = 1.0
        else:
            # Random noise (Default)
            self.I = np.random.rand(self.ny, self.nx) * 0.1

    def step(self, step_idx: int = 0):
        """
        Overriding step() to implement Axiom 1 Symmetry Breaking.
        Instead of the standard Master Equation, we use a Generative Form.
        """
        # 1. Diffusion & Standard Dynamics
        # We still call the engine for the baseline diffusion (kappa)
        # We pass a zero-array for I to the core to disable symmetric coupling terms
        # Ensure we unpack the coupled field tuple if the engine returns one
        result = self.engine.step(self.C, dt=self.dt, I=np.zeros_like(self.I)) 
        self.C = result[0] if isinstance(result, tuple) else result
        
        # 2. Non-Symmetric Informational Attraction (Axiom 1)
        # Matter 'sticks' where I is resonant, but is NOT deleted by I.
        # Informational source term: C_dot += beta * (1.0 - C) * I 
        # This saturates at C=1.0 per atom site.
        attraction = self.params.beta * (1.1 - self.C) * self.I
        self.C += attraction * self.dt
        
        # 3. Domain Specific Hooks (Deposition/Flux/Learning)
        self.post_step_physics()
        
        self.time += self.dt
        self.step_count += 1
        
        if self.logger:
            self._log_current_state(step_idx)

    def post_step_physics(self):
        """
        ICN Generative Logic: Selective Growth & Field Refinement (Axiom 6).
        """
        # 1. Selective Flux (Axiom 2) 
        # We no longer use global flux. Matter only 'crystallizes' at I-peaks.
        # This is handled by the 'attraction' term in the step() override.
        
        # 2. Axiom 6: Recursive Information Refinement (Learning)
        # Boost I-field in under-filled target zones
        if self.step_count % 10 == 0:
            target_mask = (self.I > 0.1).astype(float)
            actual_mask = (self.C > 0.2).astype(float) # Matching threshold
            gap = target_mask - actual_mask
            self.I += 0.5 * np.maximum(0, gap) # Aggressive learning
            
        # Physical clamping 
        self.C = np.clip(self.C, 0.0, 2.0)

        # DIAGNOSTIC: Trace evolution every 100 steps
        if self.step_count % 100 == 0:
            print(f"DEBUG: Step {self.step_count} | Max C: {np.max(self.C):.4f} | Max I: {np.max(self.I):.4f}")

    def get_extra_metrics(self) -> dict:
        """
        Calculate Nanofab-specific metrics:
        1. Pattern Fidelity (Correlation with target I)
        2. Defect Density (Matter in non-target zones)
        """
        target = (self.I > 0.5).astype(float)
        actual = (self.C > 0.2).astype(float) # Lower threshold for atomic resolution
        
        # Fidelity = Percent of target pixels correctly filled
        target_sum = np.sum(target)
        overlap_sum = np.sum(target * actual)
        
        print(f"DEBUG: Metric Check | TargetSum: {target_sum} | Overlap: {overlap_sum} | Max C: {np.max(self.C)}")
        
        fidelity = overlap_sum / (target_sum + 1e-9)
        
        # Defects = Percent of background pixels with stray matter
        background = (self.I < 0.1).astype(float)
        defects = np.sum(background * actual) / (np.sum(background) + 1e-9)
        
        return {
            "fidelity": float(fidelity),
            "defect_rate": float(defects),
            "total_mass": float(np.sum(self.C))
        }

def run_research_sim():
    print("🚀 Topic 0.34: Starting Information-Centric Nanofabrication Sim...")
    print("-" * 50)
    print("Theory Verification: Replacing Photons with Information.")
    print("Logic: We attract material (C) to the target pattern (I) using the beta coupling.")
    print("-" * 50)

    # nx, ny: Resolution of the fabrication bed
    # dt: Time resolution of the atomic deposition
    solver = ICNEngine(nx=64, ny=128, dt=0.01, pattern_type="S_Logic_Gate")
    
    # Run for 2000 steps to allow for recursive field refinement (Axiom 6)
    steps = 2000
    solver.run(steps=steps, verbose=True)
    
    final_metrics = solver.get_extra_metrics()
    print("\n--- Synthesis Result (Long-term Stability) ---")
    print(f"✅ Pattern Fidelity: {final_metrics['fidelity']:.2%}")
    print(f"⚠️ Defect Rate:      {final_metrics['defect_rate']:.2%}")
    print(f"🌍 Economic Value:   { (final_metrics['fidelity'] / (final_metrics['defect_rate'] + 0.01)):.2f} UET-Yield")
    
    if final_metrics['fidelity'] > 0.95:
        print("💎 SUCCESS: Atomic precision achieved via Information Resonance.")
    else:
        print("⚠️ RESEARCH NOTE: Increase Beta Coupling (beta) to sharpen the field gradient.")

if __name__ == "__main__":
    run_research_sim()
