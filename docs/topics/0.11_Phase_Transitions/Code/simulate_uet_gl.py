import numpy as np
import matplotlib.pyplot as plt
import os
import sys

def run_simulation():
    # --- 1. Parameters (Unit Checked) ---
    N = 100         # Grid points
    dx = 1.0        # Grid spacing [m]
    dt = 0.01       # Time step [s]
    steps = 2000    # Total time steps
    
    # Ginzburg-Landau Parameters (J/m^3)
    a = -1.0        # J/m^3 (Negative for second-order phase transition)
    b = 1.0         # J/m^3
    kappa = 1.0     # J/m (Gradient energy coefficient)
    
    # Kinetic coefficient (m^3 / (J * s))
    Gamma = 0.1     
    
    # UET Parameters
    mu_G = 0.05     # Mobility coefficient for game term [m^3 / (J * s)]
    eta_U = 0.5     # Game coupling (Dimensionless)
    phi_noise = 0.05 # Phi_N noise amplitude (J/m^3 equivalent)

    # --- 2. Initialization ---
    np.random.seed(42)
    C_base = np.random.normal(0, 0.01, N)
    C_uet = np.copy(C_base)
    
    energy_base = []
    energy_uet = []

    # --- 3. Helper Functions ---
    def calc_energy(C):
        V_c = 0.5 * a * C**2 + 0.25 * b * C**4
        grad_C = np.gradient(C, dx)
        V_grad = 0.5 * kappa * grad_C**2
        return np.sum(V_c + V_grad) * dx

    def calc_tdgl_step(C):
        laplacian_C = np.gradient(np.gradient(C, dx), dx)
        dOmega_dC = a * C + b * C**3 - kappa * laplacian_C
        return -Gamma * dOmega_dC

    # --- 4. Main Time Loop ---
    for t in range(steps):
        energy_base.append(calc_energy(C_base))
        energy_uet.append(calc_energy(C_uet))
        
        # --- Baseline: Standard TDGL ---
        dC_base = calc_tdgl_step(C_base)
        C_base += dC_base * dt
        
        # --- UET Model: TDGL + Phi_N + V_game ---
        dC_uet = calc_tdgl_step(C_uet)
        
        Phi_N_force = phi_noise * np.random.normal(0, 1, N) * (1 - C_uet**2)
        
        V_c = 0.5 * a * C_uet**2 + 0.25 * b * C_uet**4
        P = -V_c 
        P_bar = np.mean(P)
        game_shift = mu_G * C_uet * (P - P_bar) * eta_U
        
        C_uet += (dC_uet + Phi_N_force + game_shift) * dt
        
        # Periodic Boundary Conditions
        C_base[0] = C_base[-2]; C_base[-1] = C_base[1]
        C_uet[0] = C_uet[-2]; C_uet[-1] = C_uet[1]

    # --- 5. Plotting Results ---
    # Setup output directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "Result")
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(12, 5))
    
    # Plot 1: Energy Decay (Convergence)
    plt.subplot(1, 2, 1)
    time_axis = np.arange(steps) * dt
    plt.plot(time_axis, energy_base, label='Baseline (TDGL)', color='blue')
    plt.plot(time_axis, energy_uet, label='UET Model', color='red', linestyle='--')
    plt.title(r"Free Energy ($\Omega$) Decay over Time")
    plt.xlabel("Time (s)")
    plt.ylabel("Total Energy (J)")
    plt.legend()
    plt.grid(True)
    
    # Plot 2: Final Order Parameter Profile
    plt.subplot(1, 2, 2)
    x_axis = np.arange(N) * dx
    plt.plot(x_axis, C_base, label='Baseline Final State', color='blue')
    plt.plot(x_axis, C_uet, label='UET Final State', color='red', linestyle='--')
    
    eq_val = np.sqrt(-a/b)
    plt.axhline(eq_val, color='gray', linestyle=':', label=r'Equilibrium $\pm C_0$')
    plt.axhline(-eq_val, color='gray', linestyle=':')
    plt.title("Final Spatial Order Profile C(x)")
    plt.xlabel("Position x (m)")
    plt.ylabel("Order Parameter C(x)")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    output_file = os.path.join(output_dir, 'gl_benchmark_results.png')
    plt.savefig(output_file, dpi=300)
    print(f"Simulation complete. Results saved to {output_file}")

if __name__ == "__main__":
    run_simulation()
