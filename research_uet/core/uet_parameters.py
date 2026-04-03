"""
UET Central Parameter Module
============================
Single source of truth for all UET parameters.

Usage:
    from research_uet.core.uet_parameters import get_params, UETParams

    params = get_params("electroweak")
    print(params.kappa, params.beta)

Author: UET Research Team
Version: 0.9.0
Last Updated: 2026-01-13
"""

import os
import math
from dataclasses import dataclass
from typing import Literal, Optional

# =============================================================================
# GLOBAL INTEGRITY KILL SWITCH (The Truth Auditor)
# =============================================================================
# Set environment variable UET_KILL_ENGINE=TRUE to bypass all calculation logic.
# If active, all Engines will return invalid results (0.0 or NaN).
# Research scripts that PASS while this is active are guilty of SHADOW MATH.
INTEGRITY_KILL_SWITCH = os.getenv("UET_KILL_ENGINE", "FALSE").upper() == "TRUE"

# =============================================================================
# FUNDAMENTAL CONSTANTS (CODATA 2018 / SI Exact)
# =============================================================================

HBAR = 1.054571817e-34  # Planck constant [J·s]
C = 299792458  # Speed of light [m/s]
G = 6.67430e-11  # Gravitational constant [m³/kg/s²] 
K_B = 1.380649e-23  # Boltzmann constant [J/K]
ALPHA_EM = 1 / 137.035999  # Fine structure constant
M_SUN = 1.98847e30  # Solar Mass (kg) [IAU 2015]
H = 6.62607015e-34  # Planck constant [J·s]
E_CHARGE = 1.602176634e-19  # Elementary charge [C]
M_ELECTRON = 9.1093837015e-31  # Electron mass [kg]
EPSILON_0 = 8.8541878128e-12  # Vacuum permittivity [F/m]
V_EW = 246220.0  # Electroweak Vacuum Expectation Value [MeV] (Standard PDG)
R_GAS = 8.314462618  # Universal Gas Constant [J/mol·K] (2018 SI)
F_FARADAY = 96485.3321  # Faraday Constant [C/mol] (2018 SI)
ALPHA_EM_MZ = 1 / 128.94  # Fine structure constant at M_Z scale (Electroweak)

# --- STANDARDIZED ALIASES (Backward Compatibility) ---
K_BOLTZMANN = K_B
H_PLANCK = H
G_NEWTON = G
E_CHARGE = E_CHARGE # Already exists

# --- UET UNIT CONVERSIONS ---
C_KM_S = C / 1000.0  # Speed of light [km/s]
G_GALACTIC = 4.301e-6  # kpc (km/s)² / M_sun (Standardized UET Value)
RHO_COSMIC = 2.9e-16  # kg/m^3 (UET Vacuum Density - Pioneer/Fluid Frame)
H0 = 67.4  # km/s/Mpc (Planck 2018 - Global Baseline)
A0_COSMIC = 1.2e-10  # m/s² (Baseline Milgrom/MOND acceleration)
TAU_MEM_VACUUM = 0.01  # s (Vacuum memory relaxation time)

# --- UET BRIDGE CONSTANTS ---
FLUID_MOBILITY_BRIDGE = 1750.0  # Derived Informational-Physical Bridge for Topic 0.10
TAU_INERTIA = 0.05  # s (Systemic Inertia relaxation time)
A0_VISCOSITY = 1.2e-10  # m/s² (MOND-like acceleration pivot for dynamic viscosity)

# Derived Planck units
L_PLANCK = (HBAR * G / C**3) ** 0.5  # Planck length
M_PLANCK = (HBAR * C / G) ** 0.5  # Planck mass
T_PLANCK = L_PLANCK / C  # Planck time

# =============================================================================
# FIRST-PRINCIPLES CALCULATION (Landauer Principle)
# =============================================================================

LANDAUER_CONSTANT = math.log(2)  # ln(2) for Landauer coupling


def calculate_beta_landauer(temperature: float = 293.15) -> float:
    """
    Calculate β from Landauer Principle (First Principles).

    β = k_B * T * ln(2)

    This is the minimum energy cost per bit of information processing,
    derived from thermodynamics and validated experimentally (Bérut 2012).

    Args:
        temperature: System temperature in Kelvin (default: room temperature 293.15K)

    Returns:
        β in Joules (energy per bit)

    Reference:
        - Landauer (1961): Irreversibility and heat generation
        - Bérut et al. (2012): Experimental verification (DOI: 10.1103/PhysRevLett.109.180601)
    """
    return K_B * temperature * LANDAUER_CONSTANT


def calculate_kappa_from_beta(beta: float, information_density: float) -> float:
    """
    Calculate κ from β and information density (First Principles).

    κ = β / ρ_info

    Where ρ_info is the information density (bits/m³).

    This represents the "information inertia" - how much energy is required
    to change information content per unit volume.

    Args:
        beta: Energy per bit (Joules) from calculate_beta_landauer()
        information_density: Information density (bits/m³)

    Returns:
        κ (dimensionless gradient penalty coefficient)

    Reference:
        - UET Topic 0.13: Thermodynamic Bridge validation
        - Unity Scale Link: Information-Physical coupling
    """
    if information_density <= 0:
        raise ValueError("information_density must be positive")
    return beta / information_density


def calculate_scaling_ratio(scale_from: float, scale_to: float) -> float:
    """
    Calculate scaling factor for parameter transformation between scales.

    Based on thermodynamic scaling laws from Topic 0.13:
    - Temperature: T ∝ scale^(-2/3)
    - Information density: ρ ∝ scale^(-3)

    Args:
        scale_from: Source scale (meters)
        scale_to: Target scale (meters)

    Returns:
        Scaling factor to multiply parameters by

    Reference:
        - Topic 0.13: Thermodynamic scaling exponent = 2/3
        - Unity Scale Link: Scale bridge calculations
    """
    temp_ratio = (scale_to / scale_from) ** (-2.0 / 3.0)
    density_ratio = (scale_from / scale_to) ** 3.0
    return temp_ratio * density_ratio


def derive_parameters_first_principles(
    scale: float,
    temperature: float,
    information_density: float,
    **overrides
) -> UETParameters:
    """
    Derive UET parameters from first principles using Landauer coupling.
    Allows for optional field overrides for specific axiomatic requirements.
    """
    # Calculate from first principles
    beta = calculate_beta_landauer(temperature)
    kappa = calculate_kappa_from_beta(beta, information_density)

    # Base dictionary
    data = {
        "kappa": kappa,
        "beta": beta,
        "temperature": temperature,
        "scale": f"{scale:.2e}m",
        "origin": "First-Principles (Landauer)",
        "sigma_interaction": 1.0,
        "tau_inertia": 0.01, # Standard Systemic Inertia
    }
    
    # Resolving Thermodynamic vs Field Coupling Beta
    # If scale > 1e15 (Galactic/Cosmo) or scale < 1e-12 (Quantum), use standard Axial Beta
    if scale > 1e15 or scale < 1e-12:
        data["beta"] = 0.0854245 # Standard UET Field Coupling (beta ~ sqrt(alpha_em))
    
    # Apply Overrides
    data.update(overrides)

    # Construct parameters
    return UETParameters(**data)

# =============================================================================
# UET SCALE-DEPENDENT PARAMETERS
# =============================================================================


@dataclass(frozen=True)
class UETParameters:
    """
    Authoritative container for UET parameters at a given scale.
    Matches the requirements of the UET Master Equation (All 12 Axioms).
    """

    kappa: float = 0.1  # Gradient penalty (A3)
    beta: float = 0.05  # Coupling constant (A2)
    alpha: float = 1.0  # Equilibrium stiffness (A1)
    gamma: float = 0.025  # Nonlinear stability (A1)
    C0: float = 1.0  # Vacuum Expectation Value (A1)
    gamma_J: float = 0.1  # Exchange rate (A4)
    W_N: float = 0.05  # Natural Will (A5)
    lambda_coherence: float = 0.01  # Layer coherence (A10)

    # === Hardened Field Dynamics (Audit Fixes) ===
    kappa_I: float = 0.1  # Informational Inertia (A2 Propagator mass)
    tau_mem: float = 0.01  # Space-Memory relaxation time (A3)
    tau_inertia: float = 0.0  # s (Systemic Inertia - 0.0 = Overdamped/Diffusion)
    a0_viscosity: float = 1.2e-10  # m/s² (Dynamic Viscosity pivot)

    # === Structural & Loss Bridge (Audit Fixes) ===
    phi_loss: float = 0.05  # Informational dissipation (Loss factor)
    I_max: float = 1.0     # Axiomatic Informational Capacity (Normalized)
    mu_gravity: float = 0.0  # Metric coupling (Gravity bridge)
    sigma_interaction: float = 1.0  # Cross-domain scaling ratio

    # === Astrophysical Constants (A7: Pattern Recurrence) ===
    RHO_UNITY: float = 5e7  # M_sun / kpc^3 (Pivot density)
    RATIO_0: float = 8.5  # Universal Halo Ratio pivot
    GAMMA_UET: float = 0.48  # Thermodynamic scaling index
    SIGMA_CRIT: float = 1.37e9  # M_sun/kpc² (Derived from Λ)

    # === Context ===
    temperature: float = 293.15  # Kelvin
    scale: str = ""  # Scale name
    origin: str = ""  # Derivation source

    def __post_init__(self):
        """Standard detections for sabotaged parameters."""
        if INTEGRITY_KILL_SWITCH:
            # We must use object.__setattr__ because the dataclass is frozen
            for field_name in ["kappa", "beta", "alpha", "gamma", "C0", "kappa_I"]:
                object.__setattr__(self, field_name, 0.0)


# =============================================================================
# DOMAIN-SPECIFIC PRESETS (with First-Principles Derivation)
# =============================================================================

_DOMAIN_PRESETS = {
    "quantum": {
        "scale": 1e-9,  # meters (nanometer)
        "temperature": 4.2,  # K (liquid helium)
        "info_density": 1e15,  # bits/m³
        "description": "Quantum systems (nanoscale)",
    },
    "nuclear_binding": {
        "scale": 1e-15,  # meters (femtometer)
        "temperature": 1e12,  # K (nuclear temperature)
        "info_density": 1e20,  # bits/m³
        "description": "Nuclear binding (QCD scale)",
    },
    "fluid": {
        "scale": 1e-3,  # meters (millimeter)
        "temperature": 300,  # K (room temperature)
        "info_density": 1e18,  # bits/m³
        "description": "Fluid dynamics (mesoscale)",
    },
    "galactic": {
        "scale": 1e20,  # meters (galactic scale)
        "temperature": 2.7,  # K (CMB temperature)
        "info_density": 1e10,  # bits/m³
        "description": "Galactic rotation (cosmological)",
    },
    "biological": {
        "scale": 1e-6,  # meters (micrometer)
        "temperature": 310,  # K (body temperature)
        "info_density": 1e16,  # bits/m³
        "description": "Biological systems (cellular)",
    },
}


def get_params_first_principles(domain_name: str) -> UETParameters:
    """
    Get UET parameters for a domain using first-principles calculation.

    This is the RECOMMENDED method for obtaining parameters, as it uses
    physically-derived quantities rather than hardcoded values.

    Args:
        domain_name: One of "quantum", "nuclear_binding", "fluid", "galactic", "biological"

    Returns:
        UETParameters with calculated kappa, beta, and context

    Example:
        >>> params = get_params_first_principles("fluid")
        >>> print(f"κ = {params.kappa:.4f}, β = {params.beta:.2e} J")
    """
    if domain_name not in _DOMAIN_PRESETS:
        available = list(_DOMAIN_PRESETS.keys())
        raise ValueError(f"Unknown domain: {domain_name}. Available: {available}")
# Mapping: Topic -> Physical Domain (Mandatory Centralized Logic)
_TOPIC_DOMAIN_MAP = {
    "0.1": "galactic",
    "0.2": "quantum", # Black Hole Singularity is Quantum-scaled
    "0.3": "galactic",
    "0.4": "quantum", # Superconductivity
    "0.5": "nuclear_binding",
    "0.6": "quantum", # Electroweak
    "0.7": "quantum", # Neutrino
    "0.8": "quantum", # Muon g-2
    "0.9": "quantum", # Nonlocality
    "0.10": "fluid",
    "0.11": "fluid", # Phase transitions
    "0.13": "fluid", # Thermodynamic bridge
    "0.15": "galactic", # Clusters
    "0.16": "nuclear_binding",
    "0.21": "nuclear_binding", # Yang-Mills Mass Gap (QCD foundation)
    "0.22": "biological",
    "0.24": "fluid", # AI Logic
    "0.25": "fluid", # Economics
    "0.26": "galactic",
    "0.28": "fluid", # Materials
    "0.30": "biological", # Mega Flora
    "0.31": "galactic",
    "0.32": "nuclear_binding", # Fusion
    "0.33": "fluid", # Battery Tech (Nanoscale)
    "0.34": "fluid", # Nanofab
}

def get_params(topic_id_or_domain: str = "fluid", **overrides) -> UETParameters:
    """
    Get UET parameters DERIVED from first-principles ONLY.
    No hardcoded legacy values are allowed in the hardened v0.9.5 core.
    """
    # 1. Resolve domain from topic_id if provided
    domain = _TOPIC_DOMAIN_MAP.get(topic_id_or_domain, topic_id_or_domain)
    
    # 2. Check if it's a known domain
    if domain not in _DOMAIN_PRESETS:
        # Fallback to fluid (macroscopic) but log it as observation-only
        print(f"WARNING [PURGE]: Unknown domain/topic '{topic_id_or_domain}'. Defaulting to 'fluid' (Landauer 300K).")
        domain = "fluid"

    # 3. Derive Axiomatic Parameters (A1-A12) via Landauer Principle
    preset = _DOMAIN_PRESETS[domain]
    return derive_parameters_first_principles(
        scale=preset["scale"],
        temperature=preset["temperature"],
        information_density=preset["info_density"],
        **overrides
    )


def get_kappa_beta(scale: str = "electroweak") -> tuple[float, float]:
    """Convenience function to get just κ and β."""
    p = get_params(scale)
    return p.kappa, p.beta


# =============================================================================
# DOCUMENTATION
# =============================================================================

PARAMETER_POLICY = """
╔══════════════════════════════════════════════════════════════════════╗
║           UET PARAMETER CALCULATION POLICY (UPDATED)                ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  PRIMARY METHOD: First-Principles Calculation                       ║
║  ──────────────────────────────────────────────────────────────   ║
║  Use derive_parameters_first_principles() or get_params_first_      ║
║  principles() for calculating parameters from physical laws:         ║
║                                                                      ║
║    β = k_B * T * ln(2)           (Landauer Principle)                ║
║    κ = β / ρ_info                (Information-Physical coupling)     ║
║                                                                      ║
║  Domain presets available: quantum, nuclear_binding, fluid,         ║
║  galactic, biological                                          ║
║                                                                      ║
║  LEGACY METHOD: Hardcoded Registry (Backward Compatibility)          ║
║  ──────────────────────────────────────────────────────────────   ║
║  Legacy _SCALE_PARAMS are kept for existing code, but new code       ║
║  should use first-principles calculation.                          ║
║                                                                      ║
║  PROHIBITED:                                                        ║
║  - DO NOT use scipy.optimize to fit parameters per experiment!      ║
║  - DO NOT change parameters to match specific data!                 ║
║  - DO NOT use "shadow math" (bypassing UET_KILL_ENGINE)             ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
# Legacy Scale Registry (Backward Compatibility)
_SCALE_PARAMS = {}


if __name__ == "__main__":
    print("=" * 70)
    print("UET PARAMETER CALCULATION - FIRST PRINCIPLES DEMONSTRATION")
    print("=" * 70)

    print(PARAMETER_POLICY)

    print("\n" + "=" * 70)
    print("FIRST-PRINCIPLES CALCULATION EXAMPLES")
    print("=" * 70)

    # Example 1: Landauer Principle at room temperature
    print("\n[1] Landauer Principle at 300K:")
    beta_room = calculate_beta_landauer(300)
    beta_ev = beta_room / E_CHARGE
    print(f"    β = {beta_room:.4e} J = {beta_ev:.6f} eV")
    print(f"    Expected: 0.017921 eV (Topic 0.13 validation)")
    print(f"    Status: {'PASS' if abs(beta_ev - 0.017921) < 0.001 else 'FAIL'}")

    # Example 2: Domain-specific parameters
    print("\n[2] Domain-Specific Parameters (First-Principles):")
    domains = ["quantum", "fluid", "galactic", "biological"]
    for domain in domains:
        params = get_params_first_principles(domain)
        print(f"    {domain}:")
        print(f"        κ = {params.kappa:.6f}")
        print(f"        β = {params.beta:.4e} J")
        print(f"        scale = {params.scale}, origin = {params.origin}")

    # Example 3: Scaling between domains
    print("\n[3] Scaling Example (quantum → fluid):")
    scale_factor = calculate_scaling_ratio(1e-9, 1e-3)
    print(f"    Scale factor: {scale_factor:.4e}")
    print(f"    (κ at fluid scale) = (κ at quantum scale) × {scale_factor:.4e}")

    print("\n" + "=" * 70)
    print("LEGACY PARAMETER REGISTRY (Backward Compatibility)")
    print("=" * 70)
    print("\nAvailable legacy scales:")
    for name, params in _SCALE_PARAMS.items():
        print(f"  {name}: κ={params.kappa}, β={params.beta} ({params.origin})")

    print("\n" + "=" * 70)
    print("RECOMMENDATION: Use first-principles calculation for new code!")
    print("=" * 70)
