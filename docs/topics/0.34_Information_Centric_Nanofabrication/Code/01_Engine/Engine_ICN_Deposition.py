"""
UET ICN Engine - Information-Centric Nanofabrication (SELECTIVITY FIX)
=====================================================================
Axiomatic simulation of SAW-guided direct-growth of circuits.

Pillar: 01_Engine
Actuator (I): Surface Acoustic Wave Potential (I=0: Equilibrium/Node, I=1: Antinode)
Matter (C): Atom/Molecular Concentration. (Initialized as SEED, not flood)
"""

import numpy as np
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any

# Ensure project root is in path
current_file = Path(__file__).resolve()
project_root = current_file.parents[5] 
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from docs.core.uet_base_solver import UETBaseSolver
from docs.core.uet_parameters import get_params, UETParameters

class ICNEngine(UETBaseSolver):
    def __init__(
        self,
        nx: int = 64,
        ny: int = 128,
        dt: float = 0.01,
        name: str = "ICN_Hardened_SAW",
        pattern_type: str = "S_Logic_Gate"
    ):
        params = get_params("0.34")
        super().__init__(
            nx=nx, ny=ny, dt=dt, params=params, name=name,
            topic="0.34_Information_Centric_Nanofabrication", pillar="01_Engine"
        )
        # SELECTIVITY FIX: Initialize with light SEED concentration (10% density)
        self.C = np.ones((self.ny, self.nx)) * 0.1
        
        self.pattern_type = pattern_type
        self._initialize_saw_field()

    def _initialize_saw_field(self):
        """
        I = SAW Potential (Input Actuator).
        C = Matter Concentration (Result).
        """
        self.I = np.ones((self.ny, self.nx)) # High pressure everywhere (Repulsive)
        cx, cy = self.nx // 2, self.ny // 2
        r = self.nx // 4
        
        # Draw the target 'S' as pressure wells (nodes)
        for y in range(self.ny):
            for x in range(self.nx):
                is_node = False
                if (x - cx)**2 + (y - (cy - r//2))**2 < (r//2)**2:
                    if x > cx: is_node = True
                if (x - cx)**2 + (y - (cy + r//2))**2 < (r//2)**2:
                    if x < cx: is_node = True
                if abs(x - cx) < 2 and abs(y - cy) < r:
                    is_node = True
                
                if is_node:
                    self.I[y, x] = 0.0 # Pressure Node (Trap)

        # Precompute gradients for speed
        self.grad_I_y, self.grad_I_x = np.gradient(self.I, self.dx)

    def step(self, step_idx: int = 0):
        # 1. Standard Physics (Diffusion + Feed Flux)
        # We simulate a constant background flux (vapour) of atoms
        flux_source = 0.05 * self.dt # Background vapor saturation
        self.C += flux_source
        
        # 2. Gradient Drift (SAW Trap Force)
        flux_x = self.C * self.grad_I_x
        flux_y = self.C * self.grad_I_y
        _, div_flux_x = np.gradient(flux_x, self.dx)
        div_flux_y, _ = np.gradient(flux_y, self.dx)
        div_J = div_flux_x + div_flux_y
        
        # Matter traps at nodes
        self.C += self.params.beta * div_J * self.dt
        
        # 3. SELECTIVITY FIX: Background Scouring (Plasma/Vacuum Loss)
        # atoms in the background (I=1) are actively evaporated/removed.
        # phi_loss represents the "Vacuum/Scouring" strength.
        scouring_term = self.params.phi_loss * self.C * self.I * self.dt
        self.C -= scouring_term
        
        self.C = np.clip(self.C, 0.0, 1.25)
        
        # 4. Interactive Feedback
        if (step_idx + 1) % 25 == 0:
            avg_c = np.mean(self.C)
            bar_len = 20
            p = min(1.0, avg_c / 0.5) 
            fill = int(p * bar_len)
            meter = "#" * fill + "." * (bar_len - fill)
            sys.stdout.write(f"\r   [SAW SCOURING] [{meter}] Step {step_idx+1}/500 | Selectivity: {1-np.mean(self.C * self.I):.2f}")
            sys.stdout.flush()

        self.time += self.dt
        self.step_count += 1

    def get_extra_metrics(self) -> Dict[str, Any]:
        target = (self.I < 0.1).astype(float)
        actual = (self.C > 0.4).astype(float) # Lower threshold for growing phase
        bg = (self.I > 0.5).astype(float)
        
        # Fidelity = How much of the 'S' is filled
        fidelity = np.sum(target * actual) / (np.sum(target) + 1e-9)
        # Defect Rate = How much matter is outside the 'S'
        defect_rate = np.sum(bg * actual) / (np.sum(bg) + 1e-9)
        
        return {"fidelity": fidelity, "defect_rate": defect_rate}

def run_research_sim():
    print(f"\n{'='*70}\n🚀 SAW HARDENING: Implementing Selectivity & Scouring\nForce: SAW Trap | Cleanup: Plasma Vacuum (phi_loss)\n{'='*70}\n")
    solver = ICNEngine(nx=64, ny=128, dt=0.01, pattern_type="S_Logic_Gate")
    solver.run(steps=500, verbose=True)
    
    m = solver.get_extra_metrics()
    print(f"\n\n📊 INDUSTRIAL STATUS AUDIT:")
    print(f"   [Fidelity] {m['fidelity']:.2%} (Pattern Logic)")
    print(f"   [Defects ] {m['defect_rate']:.2%} (Selection Efficiency)")
    print(f"   [Status  ] {'INDUSTRIAL GRADE' if m['defect_rate'] < 0.1 else 'PROTOTYPE'}\n")

if __name__ == "__main__":
    run_research_sim()
