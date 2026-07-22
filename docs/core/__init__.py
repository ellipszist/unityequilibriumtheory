"""
UET Core Module
===============
Central module for UET theory, parameters, and equations.

Usage:
    from docs.core import get_params, UETParams, HBAR, C, G

    # Get parameters for a scale
    params = get_params("electroweak")
    print(f"κ = {params.kappa}, β = {params.beta}")

    # Or by topic number
    params = get_params("0.1")  # Galaxy rotation

Author: UET Research Team
Version: 0.9.0
"""

from .uet_parameters import (
    # Main API
    get_params,
    get_kappa_beta,
    UETParameters,
    # Physical constants
    HBAR,
    C,
    G,
    K_B,
    ALPHA_EM,
    L_PLANCK,
    M_PLANCK,
    T_PLANCK,
    # Policy
    PARAMETER_POLICY,
)
from .uet_trace import TraceKernelConfig, UETStepResult
from .uet_matter_space import (
    MATTER_SPACE_OPERATOR_MODE,
    MatterSpaceConfig,
    MatterSpaceState,
    MatterSpaceStabilityError,
    matter_space_step,
)
from .uet_covariant_response import (
    COVARIANT_RESPONSE_MODEL_STATUS,
    CovariantResponseConfig,
    conservative_action_density,
    einstein_gr_residual,
    response_scalar_equation_residual,
    uet_metric_residual,
)
from .uet_covariant_balance import (
    COVARIANT_BALANCE_STATUS,
    CovariantExchangeLedger,
    balance_contract,
    evaluate_balance_identity,
    exchange_completed_ledger,
)
from .uet_covariant_nonclosed import (
    CAUSAL_NONCLOSED_STATUS,
    CausalInfluenceConfig,
    CausalSourceEvent,
    causal_exchange_from_events,
    covariant_retarded_kernel_value,
    retarded_influence_from_events,
    retarded_telegraph_kernel_1p1,
)
from .uet_covariant_reduction import (
    COVARIANT_REDUCTION_STATUS,
    ReducedResponseCoefficients,
    WeakFieldReductionConfig,
    compare_response_reduction,
    derive_response_coefficients,
    matter_space_config_from_reduction,
)
from .uet_covariant_matter import (
    COVARIANT_MATTER_STATUS,
    CovariantMatterConfig,
    coupled_conservative_action_density,
    coupled_matter_stress_tensor,
    coupled_metric_residual,
    coupled_response_scalar_equation_residual,
    matter_action_contract,
    matter_current_divergence,
    matter_eom_residual,
    matter_noether_current,
    reciprocal_interaction_derivatives,
)
from .uet_covariant_diffusion import (
    COVARIANT_DIFFUSION_STATUS,
    ConservedCurrentBridgeConfig,
    ConservedCurrentState,
    CurrentDecomposition,
    causal_current_rhs,
    compare_adiabatic_limit,
    compare_matter_space_conserved_rhs,
    conditioned_matter_chemical_potential,
    conditioned_matter_free_energy,
    current_bridge_contract,
    current_energy_balance,
    current_extended_energy,
    decompose_noether_current,
    matter_equation_config_from_current_bridge,
    model_b_rhs,
    normalize_local_charge_and_current,
    principal_symbol_diagnostics,
)
from .uet_hyperbolic_phase_field import (
    HYPERBOLIC_PHASE_FIELD_SOURCE_ARXIV,
    HYPERBOLIC_PHASE_FIELD_SOURCE_DOI,
    HYPERBOLIC_PHASE_FIELD_STATUS,
    HyperbolicPhaseFieldConfig,
    HyperbolicPhaseFieldRates,
    HyperbolicPhaseFieldState,
    analytic_characteristic_speeds,
    augmented_chemical_potential,
    compare_augmented_to_cahn_hilliard_chemical,
    double_well_curvature,
    double_well_derivative,
    double_well_potential,
    gradient_constraint_rate_residual,
    gradient_constraint_residual,
    hyperbolic_phase_field_contract,
    hyperbolic_phase_field_energy,
    hyperbolic_phase_field_energy_balance,
    hyperbolic_phase_field_rhs,
    hyperbolicity_diagnostics,
    paper_asymptotic_scaling_diagnostics,
    periodic_central_derivative,
    principal_matrix,
    quasistatic_auxiliary_phase,
)

__all__ = [
    # Parameters
    "get_params",
    "get_kappa_beta",
    "UETParameters",
    # Constants
    "HBAR",
    "C",
    "G",
    "K_B",
    "ALPHA_EM",
    "L_PLANCK",
    "M_PLANCK",
    "T_PLANCK",
    # Policy
    "PARAMETER_POLICY",
    "TraceKernelConfig",
    "UETStepResult",
    "MATTER_SPACE_OPERATOR_MODE",
    "MatterSpaceConfig",
    "MatterSpaceState",
    "MatterSpaceStabilityError",
    "matter_space_step",
    "COVARIANT_RESPONSE_MODEL_STATUS",
    "CovariantResponseConfig",
    "conservative_action_density",
    "einstein_gr_residual",
    "response_scalar_equation_residual",
    "uet_metric_residual",
    "COVARIANT_BALANCE_STATUS",
    "CovariantExchangeLedger",
    "balance_contract",
    "evaluate_balance_identity",
    "exchange_completed_ledger",
    "CAUSAL_NONCLOSED_STATUS",
    "CausalInfluenceConfig",
    "CausalSourceEvent",
    "causal_exchange_from_events",
    "covariant_retarded_kernel_value",
    "retarded_influence_from_events",
    "retarded_telegraph_kernel_1p1",
    "COVARIANT_REDUCTION_STATUS",
    "ReducedResponseCoefficients",
    "WeakFieldReductionConfig",
    "compare_response_reduction",
    "derive_response_coefficients",
    "matter_space_config_from_reduction",
    "COVARIANT_MATTER_STATUS",
    "CovariantMatterConfig",
    "coupled_conservative_action_density",
    "coupled_matter_stress_tensor",
    "coupled_metric_residual",
    "coupled_response_scalar_equation_residual",
    "matter_action_contract",
    "matter_current_divergence",
    "matter_eom_residual",
    "matter_noether_current",
    "reciprocal_interaction_derivatives",
    "COVARIANT_DIFFUSION_STATUS",
    "ConservedCurrentBridgeConfig",
    "ConservedCurrentState",
    "CurrentDecomposition",
    "causal_current_rhs",
    "compare_adiabatic_limit",
    "compare_matter_space_conserved_rhs",
    "conditioned_matter_chemical_potential",
    "conditioned_matter_free_energy",
    "current_bridge_contract",
    "current_energy_balance",
    "current_extended_energy",
    "decompose_noether_current",
    "matter_equation_config_from_current_bridge",
    "model_b_rhs",
    "normalize_local_charge_and_current",
    "principal_symbol_diagnostics",
    "HYPERBOLIC_PHASE_FIELD_SOURCE_ARXIV",
    "HYPERBOLIC_PHASE_FIELD_SOURCE_DOI",
    "HYPERBOLIC_PHASE_FIELD_STATUS",
    "HyperbolicPhaseFieldConfig",
    "HyperbolicPhaseFieldRates",
    "HyperbolicPhaseFieldState",
    "analytic_characteristic_speeds",
    "augmented_chemical_potential",
    "compare_augmented_to_cahn_hilliard_chemical",
    "double_well_curvature",
    "double_well_derivative",
    "double_well_potential",
    "gradient_constraint_rate_residual",
    "gradient_constraint_residual",
    "hyperbolic_phase_field_contract",
    "hyperbolic_phase_field_energy",
    "hyperbolic_phase_field_energy_balance",
    "hyperbolic_phase_field_rhs",
    "hyperbolicity_diagnostics",
    "paper_asymptotic_scaling_diagnostics",
    "periodic_central_derivative",
    "principal_matrix",
    "quasistatic_auxiliary_phase",

]
__version__ = "0.9.0"
