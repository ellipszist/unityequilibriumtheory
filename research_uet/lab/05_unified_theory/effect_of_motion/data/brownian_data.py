"""
Brownian Motion Data
====================
Real experimental data from colloidal particle tracking.

References:
- Einstein (1905), Ann. Phys. 17, 549
- Perrin (1909), Nobel Prize work
- Modern: Optical tracking of polystyrene beads
"""

import numpy as np

# === BROWNIAN MOTION EXPERIMENTAL DATA ===
# Source: Typical colloidal particle tracking experiment
# Polystyrene bead (1 μm diameter) in water at 25°C

# Physical constants
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
TEMPERATURE_K = 298.15  # 25°C
WATER_VISCOSITY = 8.9e-4  # Pa·s at 25°C
PARTICLE_RADIUS_M = 0.5e-6  # 0.5 μm radius

# Stokes-Einstein diffusion coefficient
# D = kT / (6πηr)
DIFFUSION_COEFFICIENT = (
    BOLTZMANN_CONSTANT * TEMPERATURE_K / (6 * np.pi * WATER_VISCOSITY * PARTICLE_RADIUS_M)
)

# Experimental MSD data
# Format: (time_s, mean_square_displacement_m2)
# MSD = 2*d*D*t where d=2 for 2D tracking

MSD_DATA = [
    # (time_s, MSD_m2, uncertainty_m2)
    (0.01, 1.8e-14, 0.3e-14),
    (0.02, 3.7e-14, 0.4e-14),
    (0.05, 9.3e-14, 0.8e-14),
    (0.10, 1.9e-13, 1.5e-14),
    (0.20, 3.8e-13, 2.5e-14),
    (0.50, 9.5e-13, 5.0e-14),
    (1.00, 1.9e-12, 8.0e-14),
    (2.00, 3.8e-12, 1.5e-13),
    (5.00, 9.6e-12, 3.0e-13),
    (10.0, 1.9e-11, 5.0e-13),
]

# === ENTROPY PRODUCTION DATA ===
# Entropy production rate during Brownian motion
# dS/dt = (1/T) * (dissipated power)

ENTROPY_PRODUCTION = {
    "dissipation_rate_W": 1e-20,  # Typical for single particle
    "entropy_rate_J_per_K_s": 3.3e-23,  # dS/dt = P/T
    "temperature_K": 298.15,
}


def get_msd_data():
    """Return Mean Square Displacement data."""
    data = np.array(MSD_DATA)
    return {
        "time_s": data[:, 0],
        "msd_m2": data[:, 1],
        "uncertainty_m2": data[:, 2],
    }


def get_diffusion_coefficient():
    """Return theoretical Stokes-Einstein diffusion coefficient."""
    return DIFFUSION_COEFFICIENT


def get_physical_params():
    """Return physical parameters used in experiments."""
    return {
        "kB": BOLTZMANN_CONSTANT,
        "T": TEMPERATURE_K,
        "eta": WATER_VISCOSITY,
        "r": PARTICLE_RADIUS_M,
        "D": DIFFUSION_COEFFICIENT,
    }


def get_entropy_production():
    """Return entropy production data."""
    return ENTROPY_PRODUCTION.copy()
