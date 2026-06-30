import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd

def run_simulation_v2():
    print("Running UET GL Benchmark v2: Unit-Correct, Full Energy Tracking, Ablation, Multi-seed")
    N = 100         
    dx = 1.0        
    dt = 0.01       
    steps = 2000    
    
    # Parameters
    a = -1.0        
    b = 1.0         
    kappa = 1.0     
    Gamma = 0.1     
    
    # UET Parameters
    mu_G = 0.05     
    eta_U = 0.5     
    phi_noise = 0.05 # J/m^3
    Gamma_N = 0.1    # m^3 / (J * s) -> Unit conversion for Phi_N
    
    seeds = [42, 101, 2024, 7, 99]
    
    results = []

    def calc_gl_energy(C):
        V_c = 0.5 * a * C**2 + 0.25 * b * C**4
        grad_C = np.gradient(C, dx)
        V_grad = 0.5 * kappa * grad_C**2
        return np.sum(V_c + V_grad) * dx

    def calc_full_uet_energy(C, Phi_N_force, game_shift):
        # Tracking GL Energy + effective energy potentials of the UET terms
        # to show true minimization of the full functional.
        base_E = calc_gl_energy(C)
        # Approximate effective potentials (integration of forces)
        # Phi_N acts as a fluctuation energy (~ kinetic/thermal energy)
        phi_energy = np.sum(0.5 * (Phi_N_force/Gamma)**2) * dx
        # Game shift energy (variance of payoff minimization)
        game_energy = np.sum(0.5 * (game_shift/Gamma)**2) * dx
        return base_E - eta_U * game_energy + phi_energy

    def calc_tdgl_step(C):
        laplacian_C = np.gradient(np.gradient(C, dx), dx)
        return -Gamma * (a * C + b * C**3 - kappa * laplacian_C)

    # We will track 4 lanes: Baseline, +Phi_N, +V_game, UET Full
    # Store energy curves for the first seed to plot
    energy_curves = {'Baseline': [], 'PhiN': [], 'Vgame': [], 'UET': []}
    final_states = {}

    for seed_idx, seed in enumerate(seeds):
        np.random.seed(seed)
        C_init = np.random.normal(0, 0.01, N)
        
        C_lanes = {
            'Baseline': np.copy(C_init),
            'PhiN': np.copy(C_init),
            'Vgame': np.copy(C_init),
            'UET': np.copy(C_init)
        }
        
        for t in range(steps):
            if seed_idx == 0:
                energy_curves['Baseline'].append(calc_gl_energy(C_lanes['Baseline']))
                
                # For tracking UET energies, we need the current forces
                # We calculate them for tracking even if we only append for seed 0
                pass
            
            # 1. Baseline
            C_lanes['Baseline'] += calc_tdgl_step(C_lanes['Baseline']) * dt
            
            # 2. PhiN Only
            dC_phi = calc_tdgl_step(C_lanes['PhiN'])
            Phi_N_rate_phi = Gamma_N * phi_noise * np.random.normal(0, 1, N) * (1 - C_lanes['PhiN']**2)
            C_lanes['PhiN'] += (dC_phi + Phi_N_rate_phi) * dt
            
            # 3. Vgame Only
            dC_vgame = calc_tdgl_step(C_lanes['Vgame'])
            P_vgame = -(0.5 * a * C_lanes['Vgame']**2 + 0.25 * b * C_lanes['Vgame']**4)
            game_shift_vgame = mu_G * C_lanes['Vgame'] * (P_vgame - np.mean(P_vgame)) * eta_U
            C_lanes['Vgame'] += (dC_vgame + game_shift_vgame) * dt
            
            # 4. UET Full
            dC_uet = calc_tdgl_step(C_lanes['UET'])
            Phi_N_rate_uet = Gamma_N * phi_noise * np.random.normal(0, 1, N) * (1 - C_lanes['UET']**2)
            P_uet = -(0.5 * a * C_lanes['UET']**2 + 0.25 * b * C_lanes['UET']**4)
            game_shift_uet = mu_G * C_lanes['UET'] * (P_uet - np.mean(P_uet)) * eta_U
            C_lanes['UET'] += (dC_uet + Phi_N_rate_uet + game_shift_uet) * dt
            
            if seed_idx == 0:
                energy_curves['PhiN'].append(calc_full_uet_energy(C_lanes['PhiN'], Phi_N_rate_phi, 0))
                energy_curves['Vgame'].append(calc_full_uet_energy(C_lanes['Vgame'], 0, game_shift_vgame))
                energy_curves['UET'].append(calc_full_uet_energy(C_lanes['UET'], Phi_N_rate_uet, game_shift_uet))
            
            # Boundary Conditions
            for k in C_lanes.keys():
                C_lanes[k][0] = C_lanes[k][-2]
                C_lanes[k][-1] = C_lanes[k][1]

        # Calculate final metrics for the table
        res_row = {'Seed': seed}
        for k in C_lanes.keys():
            res_row[f'{k}_Final_E'] = calc_gl_energy(C_lanes[k])
            
        results.append(res_row)
        if seed_idx == 0:
            final_states = {k: np.copy(C_lanes[k]) for k in C_lanes.keys()}

    # --- Plotting Results (Seed 0) ---
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "Result")
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(14, 6))
    
    time_axis = np.arange(steps) * dt
    plt.subplot(1, 2, 1)
    plt.plot(time_axis, energy_curves['Baseline'], label='TDGL Baseline', color='black')
    plt.plot(time_axis, energy_curves['PhiN'], label='TDGL + $\Phi_N$', color='orange', alpha=0.7)
    plt.plot(time_axis, energy_curves['Vgame'], label='TDGL + $V_{game}$', color='green', alpha=0.7)
    plt.plot(time_axis, energy_curves['UET'], label='Full UET', color='red', linewidth=2)
    plt.title(r"Full $\Omega$ Energy Decay over Time (Ablation)")
    plt.xlabel("Time (s)")
    plt.ylabel(r"Total Energy $\Omega$ (J)")
    plt.legend()
    plt.grid(True)
    
    plt.subplot(1, 2, 2)
    x_axis = np.arange(N) * dx
    plt.plot(x_axis, final_states['Baseline'], label='Baseline', color='black')
    plt.plot(x_axis, final_states['PhiN'], label='+ $\Phi_N$', color='orange', alpha=0.5)
    plt.plot(x_axis, final_states['Vgame'], label='+ $V_{game}$', color='green', alpha=0.5)
    plt.plot(x_axis, final_states['UET'], label='Full UET', color='red', linewidth=2)
    
    eq_val = np.sqrt(-a/b)
    plt.axhline(eq_val, color='gray', linestyle=':')
    plt.axhline(-eq_val, color='gray', linestyle=':')
    plt.title("Final Spatial Order Profile C(x)")
    plt.xlabel("Position x (m)")
    plt.legend()
    plt.grid(True)
    
    plt.tight_layout()
    output_plot = os.path.join(output_dir, 'gl_benchmark_v2_results.png')
    plt.savefig(output_plot, dpi=300)
    
    df = pd.DataFrame(results)
    output_csv = os.path.join(output_dir, 'gl_benchmark_v2_stats.csv')
    df.to_csv(output_csv, index=False)
    
    print("\n--- Multi-Seed Statistical Validation ---")
    print(df.mean(numeric_only=True))
    print(f"\nPlots saved to {output_plot}")
    print(f"Stats saved to {output_csv}")

if __name__ == "__main__":
    run_simulation_v2()
