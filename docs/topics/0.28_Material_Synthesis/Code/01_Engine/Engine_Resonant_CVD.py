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

import numpy as np
import time
import sys
import random
from pathlib import Path

# --- ROBUST PATH FINDER ---


from docs.core.uet_parameters import get_params
from docs.core.uet_glass_box import UETPathManager


class ResonantCVDEngine:
    def __init__(self, size=50, params=None):
        self.params = params if params else get_params("0.28")
        self.size = size
        self.grid = np.zeros((size, size))
        self.target_atoms = int((size * size / 2) * 0.95)

    def run_simulation(self, mode="RANDOM_THERMAL"):
        print(f"\n🏭 FACTORY MODE: {mode}")
        print("-" * 50)

        self.grid = np.zeros((self.size, self.size))

        # Perfect Lattice Template
        lattice_map = np.zeros((self.size, self.size))
        for i in range(self.size):
            for j in range(self.size):
                if (i + j) % 2 == 0:
                    lattice_map[i][j] = 1.0

        defects = 0
        placed = 0
        attempts = 0
        start_time = time.time()

        # Simulation: High Flux Injection
        # We stop when we reach target coverage OR fail too many times
        max_attempts = self.target_atoms * 5

        while placed < self.target_atoms and attempts < max_attempts:
            attempts += 1
            x, y = random.randint(0, self.size - 1), random.randint(0, self.size - 1)

            if mode == "RANDOM_THERMAL":
                # Standard CVD: High Rejection Rate required for Quality
                # But here we simulate "Mass Production" (High Flux)
                # Atoms stick indiscriminately -> High Defect Rate

                if self.grid[x][y] == 1:
                    defects += 1  # Overlap
                elif lattice_map[x][y] == 0:
                    self.grid[x][y] = 1
                    defects += 1
                    placed += 1  # Misalignment
                else:
                    self.grid[x][y] = 1
                    placed += 1  # Success

            elif mode == "UET_RESONANT":
                # Resonant CVD: Guided by Surface Acoustic Wave (SAW) Potential
                # The substrate vibrates, creating a standing wave potential U(x,y)
                # U(x,y) = U_0 * sin^2(k*x) * sin^2(k*y)
                # Particles experience force F = -nabla U, pushing them to the nodes (minima).
                
                # To simulate this physically without a full PDE solver,
                # we calculate the distance to the nearest theoretical lattice node.
                # If the thermal energy kT < Acoustic Potential U, the atom is trapped.
                
                # Find nearest ideal node
                ideal_dx = 0
                ideal_dy = 0
                min_dist = float('inf')
                
                # In a honeycomb lattice, valid points have (i+j)%2 == 0
                # We search the immediate neighborhood for a valid potential well
                candidates = []
                for dx in range(-3, 4):
                    for dy in range(-3, 4):
                        candidates.append((dx, dy))
                
                candidates.sort(key=lambda p: p[0]**2 + p[1]**2)
                
                slide_success = False
                for dx, dy in candidates:
                    nx, ny = (x + dx) % self.size, (y + dy) % self.size
                    
                    if lattice_map[nx][ny] == 1.0 and self.grid[nx][ny] == 0:
                        # Acoustic trapping condition (simulated)
                        # The further the drift, the higher the required acoustic amplitude U_0
                        # Let's say capture probability depends on distance and Acoustic Energy vs Thermal Noise
                        # P_capture = exp(- (dx^2 + dy^2) / Lambda^2)
                        # Where Lambda is the acoustic trapping range
                        lambda_trap = 2.5 # Effective trapping range in lattice units
                        dist_sq = dx**2 + dy**2
                        p_capture = np.exp(-dist_sq / (lambda_trap**2))
                        
                        if random.random() < p_capture:
                            self.grid[nx][ny] = 1
                            placed += 1
                            slide_success = True
                            break
                
                if not slide_success:
                    # If it fails to trap in a valid well, it becomes a defect or escapes
                    # Thermal noise overrides the acoustic trap
                    if random.random() < 0.05: # 5% chance to stick as defect
                        defects += 1

        end_time = time.time()
        duration = end_time - start_time

        # Metrics
        efficiency = (placed / attempts) * 100  # How much material was useful?
        defect_rate = (defects / (placed + defects)) * 100 if placed > 0 else 100
        quality_score = 100.0 - defect_rate

        print(f"   ⏱️  Time: {duration:.4f}s")
        print(f"   ⚠️  Defects: {defects}")
        print(f"   📉 Waste (Attempts): {attempts - placed}")
        print(f"   💎 Quality: {quality_score:.2f}%")
        print(f"   ⚡ Efficiency: {efficiency:.2f}%")

        return quality_score, efficiency


if __name__ == "__main__":
    print("🔬 UET MATERIAL SYNTHESIS: GRAPHENE PRODUCTION")
    print("============================================")

    engine = ResonantCVDEngine(size=80)

    # 1. Random (Standard)
    q1, e1 = engine.run_simulation("RANDOM_THERMAL")

    # 2. Resonant (UET)
    q2, e2 = engine.run_simulation("UET_RESONANT")

    print("\n📊 COMPARISON REPORT")
    print("============================================")
    # The true "Speed Up" is how many *Good Atoms* we get per attempt
    score1 = q1 * e1
    score2 = q2 * e2
    improvement = score2 / score1 if score1 > 0 else 100.0

    print(f"Standard Score (Q*E): {score1:.1f}")
    print(f"Resonant Score (Q*E): {score2:.1f}")
    print(f"Overall Gain: {improvement:.1f}x BETTER")

    # SAVE PLOT (Method 1: Matplotlib Bar Chart)
    # Get current script directory and Result dir
    import matplotlib.pyplot as plt

    # Use UETPathManager for consistent result storage
    result_dir = UETPathManager.get_result_dir(
        topic_id="0.28_Material_Synthesis",
        experiment_name="Engine_Resonant_CVD",
        pillar="01_Engine",
        category="log",
    )

    labels = ["Standard CVD", "UET Resonant CVD"]
    efficiencies = [e1, e2]
    qualities = [q1, q2]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 6))
    rects1 = ax.bar(x - width / 2, efficiencies, width, label="Efficiency (%)", color="gray")
    rects2 = ax.bar(x + width / 2, qualities, width, label="Quality (%)", color="green")

    ax.set_ylabel("Percentage")
    ax.set_title("UET Graphene Synthesis: Standard vs Resonant")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    ax.set_ylim(0, 110)

    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(
                f"{height:.1f}%",
                xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3),  # 3 points vertical offset
                textcoords="offset points",
                ha="center",
                va="bottom",
            )

    autolabel(rects1)
    autolabel(rects2)

    output_path = result_dir / "Res_CVD_Comparison.png"
    plt.savefig(output_path)
    print(f"📊 Comparison Plot saved to: {output_path}")
    plt.close()

    if improvement > 1.5:
        print("\n✅ CONCLUSION: Resonant Manufacturing resolves the bottleneck.")
        print("   High-Efficiency Graphene is viable (Speed + Purity).")
    else:
        print("\n❌ CONCLUSION: Failed to prove advantage.")
