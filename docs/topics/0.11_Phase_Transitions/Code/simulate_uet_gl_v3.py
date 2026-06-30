import numpy as np
import matplotlib.pyplot as plt
import os
import pandas as pd
from scipy import stats

def run_simulation_v3():
    print("Running UET GL Benchmark v3: 100 Seeds, Paired Differences, Win Rates")
    N = 100         
    dx = 1.0        
    dt = 0.01       
    steps = 2000    
    
    # Frozen Hyperparameters
    a = -1.0        
    b = 1.0         
    kappa = 1.0     
    Gamma = 0.1     
    
    mu_G = 0.05     
    eta_U = 0.5     
    phi_noise = 0.05
    Gamma_N = 0.1   
    
    n_seeds = 100
    seeds = np.arange(1, n_seeds + 1)
    
    results = []

    def calc_gl_energy(C):
        V_c = 0.5 * a * C**2 + 0.25 * b * C**4
        grad_C = np.gradient(C, dx)
        V_grad = 0.5 * kappa * grad_C**2
        return np.sum(V_c + V_grad) * dx

    def calc_tdgl_step(C):
        laplacian_C = np.gradient(np.gradient(C, dx), dx)
        return -Gamma * (a * C + b * C**3 - kappa * laplacian_C)

    for seed_idx, seed in enumerate(seeds):
        if (seed_idx+1) % 10 == 0:
            print(f"Processing seed {seed_idx+1}/{n_seeds}...")
        
        np.random.seed(seed)
        C_init = np.random.normal(0, 0.01, N)
        
        C_lanes = {
            'Baseline': np.copy(C_init),
            'PhiN': np.copy(C_init),
            'Vgame': np.copy(C_init),
            'UET': np.copy(C_init)
        }
        
        for t in range(steps):
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
            
            # Boundary Conditions
            for k in C_lanes.keys():
                C_lanes[k][0] = C_lanes[k][-2]
                C_lanes[k][-1] = C_lanes[k][1]

        res_row = {'Seed': seed}
        for k in C_lanes.keys():
            res_row[f'{k}_Final_E'] = calc_gl_energy(C_lanes[k])
            
        results.append(res_row)

    df = pd.DataFrame(results)
    
    # Calculate Paired Differences
    df['Paired_Diff_UET_vs_Base'] = df['UET_Final_E'] - df['Baseline_Final_E']
    
    # Calculate Win Rates
    win_rate = (df['Paired_Diff_UET_vs_Base'] < 0).mean() * 100
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "..", "Result")
    os.makedirs(output_dir, exist_ok=True)
    
    # --- Plot 1: Histogram of Final Energies ---
    plt.figure(figsize=(12, 5))
    
    plt.subplot(1, 2, 1)
    plt.hist(df['Baseline_Final_E'], bins=20, alpha=0.5, label='Baseline', color='blue')
    plt.hist(df['UET_Final_E'], bins=20, alpha=0.5, label='UET', color='red')
    plt.title("Distribution of Final GL Energy (100 Seeds)")
    plt.xlabel("Final GL Energy (J)")
    plt.ylabel("Frequency")
    plt.legend()
    
    plt.subplot(1, 2, 2)
    plt.hist(df['Paired_Diff_UET_vs_Base'], bins=20, alpha=0.7, color='purple')
    plt.axvline(0, color='black', linestyle='--')
    plt.title("Paired Difference: E_UET - E_Base")
    plt.xlabel("Energy Difference (J) [Negative = UET won]")
    plt.ylabel("Frequency")
    
    plt.tight_layout()
    output_plot = os.path.join(output_dir, 'gl_benchmark_v3_results.png')
    plt.savefig(output_plot, dpi=300)
    
    output_csv = os.path.join(output_dir, 'gl_benchmark_v3_stats.csv')
    df.to_csv(output_csv, index=False)
    
    # Print Stats
    print("\n" + "="*50)
    print("V3 STATISTICAL VALIDATION (100 Seeds)")
    print("="*50)
    print(f"Baseline Final E : {df['Baseline_Final_E'].mean():.6f} ± {df['Baseline_Final_E'].std():.6f}")
    print(f"PhiN Final E     : {df['PhiN_Final_E'].mean():.6f} ± {df['PhiN_Final_E'].std():.6f}")
    print(f"Vgame Final E    : {df['Vgame_Final_E'].mean():.6f} ± {df['Vgame_Final_E'].std():.6f}")
    print(f"UET Final E      : {df['UET_Final_E'].mean():.6f} ± {df['UET_Final_E'].std():.6f}")
    print("-"*50)
    print(f"Paired Diff Mean : {df['Paired_Diff_UET_vs_Base'].mean():.6f} ± {df['Paired_Diff_UET_vs_Base'].std():.6f}")
    print(f"UET Win Rate     : {win_rate:.1f}%")
    print("="*50)
    
if __name__ == "__main__":
    run_simulation_v3()
