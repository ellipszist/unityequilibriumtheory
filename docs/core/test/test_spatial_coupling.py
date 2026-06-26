"""Unit checks for Wave 5 spatial-coupling candidate operators."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np


def _bootstrap() -> Path:
    current = Path(__file__).resolve()
    for parent in [current] + list(current.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    raise RuntimeError("UET docs root not found")


_bootstrap()

from docs.core.uet_master_equation import (  # noqa: E402
    LEGACY_OPERATOR_MODE,
    SPATIAL_COUPLED_OPERATOR_MODE,
    dynamics_step_complete,
    game_theory_force,
    game_theory_potential,
    gradient_magnitude_squared,
    information_coupling,
    information_dynamics_source,
)
from docs.core.uet_parameters import UETParameters  # noqa: E402


def _compare_state(left, right) -> None:
    if isinstance(left, tuple):
        assert isinstance(right, tuple)
        assert len(left) == len(right)
        for a, b in zip(left, right):
            np.testing.assert_allclose(a, b)
    else:
        np.testing.assert_allclose(left, right)


def test_legacy_information_coupling_matches_historical_form() -> None:
    params = UETParameters(beta=0.25, operator_mode=LEGACY_OPERATOR_MODE)
    C = np.array([1.0, 2.0, 3.0])
    I = np.array([0.5, -1.0, 2.0])
    dx = 0.2
    expected = params.beta * np.sum(C * I) * dx
    got = information_coupling(C, I, dx, params)
    np.testing.assert_allclose(got, expected)


def test_spatial_information_source_zero_gates() -> None:
    params = UETParameters(beta=0.25, operator_mode=SPATIAL_COUPLED_OPERATOR_MODE)
    C = np.array([0.0, 1.0, 2.0])
    I = np.array([1.0, 0.0, -1.0])
    source = information_dynamics_source(C, I, params)
    expected = -params.beta * params.spatial_information_coupling * C * I
    np.testing.assert_allclose(source, expected)
    np.testing.assert_allclose(information_dynamics_source(np.zeros_like(C), I, params), 0.0)
    np.testing.assert_allclose(information_dynamics_source(C, np.zeros_like(I), params), 0.0)


def test_spatial_game_operator_is_interface_sensitive() -> None:
    params = UETParameters(beta=0.05, operator_mode=SPATIAL_COUPLED_OPERATOR_MODE)
    uniform = np.ones(32)
    interface = np.concatenate([np.zeros(16), np.ones(16)])
    uniform_game = game_theory_potential(
        uniform, params.SIGMA_CRIT, params=params, dx=1.0, operator_mode=SPATIAL_COUPLED_OPERATOR_MODE
    )
    interface_game = game_theory_potential(
        interface, params.SIGMA_CRIT, params=params, dx=1.0, operator_mode=SPATIAL_COUPLED_OPERATOR_MODE
    )
    np.testing.assert_allclose(uniform_game, 0.0)
    assert float(np.linalg.norm(interface_game)) > 0.0


def test_spatial_game_operator_preserves_2d_shape() -> None:
    params = UETParameters(beta=0.05, operator_mode=SPATIAL_COUPLED_OPERATOR_MODE)
    C = np.zeros((8, 8))
    C[:, 4:] = 1.0
    grad_sq = gradient_magnitude_squared(C, 1.0)
    force = game_theory_force(
        C,
        density=params.SIGMA_CRIT,
        scale=1.0,
        dx=1.0,
        params=params,
        operator_mode=SPATIAL_COUPLED_OPERATOR_MODE,
    )
    assert grad_sq.shape == C.shape
    assert force.shape == C.shape
    assert float(np.linalg.norm(force)) > 0.0


def test_default_and_explicit_legacy_dynamics_match() -> None:
    params = UETParameters(beta=0.05, kappa=0.1, W_N=0.0, a0_viscosity=0.0)
    C = np.linspace(-0.2, 0.2, 16)
    I = np.linspace(0.1, 0.2, 16)
    default_state = dynamics_step_complete(C, I=I, dx=0.1, dt=0.01, params=params)
    explicit_legacy_state = dynamics_step_complete(
        C,
        I=I,
        dx=0.1,
        dt=0.01,
        params=params,
        operator_mode=LEGACY_OPERATOR_MODE,
    )
    _compare_state(default_state, explicit_legacy_state)


if __name__ == "__main__":
    test_legacy_information_coupling_matches_historical_form()
    test_spatial_information_source_zero_gates()
    test_spatial_game_operator_is_interface_sensitive()
    test_spatial_game_operator_preserves_2d_shape()
    test_default_and_explicit_legacy_dynamics_match()
    print("Wave 5 spatial coupling unit checks passed")
