import numpy as np
import pytest

from docs.core.uet_master_equation import (
    LEGACY_OPERATOR_MODE,
    LEGACY_VARIATIONAL_OPERATOR_MODE,
    SUPPORTED_OPERATOR_MODES,
    dynamics_step_complete,
    information_propagator_step,
    legacy_reaction_derivative,
    potential_V,
    potential_derivative,
)
from docs.core.uet_parameters import UETParameters


def _pure_params(**overrides):
    values = dict(
        alpha=1.0,
        gamma=0.025,
        C0=1.0,
        kappa=0.0,
        beta=0.0,
        W_N=0.0,
        a0_viscosity=0.0,
        tau_inertia=0.0,
    )
    values.update(overrides)
    return UETParameters(**values)


def test_variational_mode_is_explicitly_opt_in():
    assert LEGACY_VARIATIONAL_OPERATOR_MODE == "legacy_variational_v1"
    assert LEGACY_VARIATIONAL_OPERATOR_MODE in SUPPORTED_OPERATOR_MODES
    assert UETParameters().operator_mode == LEGACY_OPERATOR_MODE


def test_declared_radial_potential_and_derivative_are_a_pair():
    params = _pure_params()
    C = np.array([-1.5, -0.75, 0.0, 0.5, 1.0, 1.5, 2.0])
    epsilon = 1.0e-6
    finite_difference = (
        potential_V(C + epsilon, params) - potential_V(C - epsilon, params)
    ) / (2.0 * epsilon)
    np.testing.assert_allclose(
        potential_derivative(C, params), finite_difference, rtol=0.0, atol=1.0e-8
    )


def test_legacy_local_preserves_historical_reaction_while_variational_mode_uses_exact_pair():
    params = _pure_params()
    C = np.array([0.5, 1.5])
    dt = 0.01
    legacy = dynamics_step_complete(C, dt=dt, params=params)
    variational = dynamics_step_complete(
        C, dt=dt, params=params, operator_mode=LEGACY_VARIATIONAL_OPERATOR_MODE
    )
    np.testing.assert_allclose(
        legacy, C - dt * legacy_reaction_derivative(C, params), rtol=0.0, atol=1.0e-14
    )
    np.testing.assert_allclose(
        variational, C - dt * potential_derivative(C, params), rtol=0.0, atol=1.0e-14
    )
    assert not np.allclose(legacy, variational)


def test_variational_information_source_matches_positive_coupling_gradient():
    params = _pure_params(beta=0.2, kappa_I=0.0)
    C = np.ones(4)
    I = np.zeros(4)
    dt = 0.1
    updated = information_propagator_step(
        I, C, dx=1.0, dt=dt, params=params,
        operator_mode=LEGACY_VARIATIONAL_OPERATOR_MODE,
    )
    np.testing.assert_allclose(updated, -dt * params.beta * C)


def test_variational_mode_rejects_unclosed_legacy_forces():
    params = _pure_params(W_N=0.1)
    with pytest.raises(ValueError, match="pure normalized gradient terms"):
        dynamics_step_complete(
            np.ones(4), dt=0.01, params=params,
            operator_mode=LEGACY_VARIATIONAL_OPERATOR_MODE,
        )
