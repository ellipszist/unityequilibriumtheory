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
]

__version__ = "0.9.0"
