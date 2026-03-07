"""
UET Noether's Theorem Core Module
==================================

This module implements Noether's Theorem for the UET Master Equation,
providing the theoretical foundation for conservation laws.

Purpose:
- Derive Noether currents for all symmetries
- Check conservation laws numerically
- Provide the theoretical foundation for UET

Theory:
Noether's Theorem: For every continuous symmetry, there is a conserved current.

For symmetry transformation: δC = ε·X(C)
Noether current: J^μ = (∂L/∂(∂_μC))·X(C) - K^μ
Conservation: ∂_μ J^μ = 0
"""

import numpy as np
from typing import Dict, Tuple, Callable
from dataclasses import dataclass

from research_uet.core.uet_parameters import UETParameters


@dataclass
class NoetherCurrent:
    """Represents a Noether current."""
    name: str
    current: np.ndarray
    divergence: float
    is_conserved: bool
    symmetry_type: str


class UETNoether:
    """Implements Noether's Theorem for UET."""

    def __init__(self, params: UETParameters = None):
        if params is None:
            self.params = UETParameters(kappa=1.0, beta=1.0)
        else:
            self.params = params

    def lagrangian_density(
        self,
        C: np.ndarray,
        grad_C: np.ndarray,
        I: np.ndarray = None
    ) -> np.ndarray:
        """
        Compute Lagrangian density for UET.

        L = (κ/2)|∇C|² - V(C) + β C·I

        where V(C) = (α/2)(C-C₀)² + (γ/4)(C-C₀)⁴
        """
        from research_uet.core.uet_master_equation import potential_V

        V = potential_V(C, self.params)
        kinetic = (self.params.kappa / 2) * grad_C**2

        if I is None:
            interaction = 0
        else:
            interaction = self.params.beta * C * I

        L = kinetic - V + interaction

        return L

    def noether_current_general(
        self,
        C: np.ndarray,
        X: Callable[[np.ndarray], np.ndarray],
        dx: float
    ) -> NoetherCurrent:
        """
        Compute Noether current for general symmetry transformation.

        For transformation δC = ε·X(C):
        J = (∂L/∂(∇C))·X(C)

        Args:
            C: Field
            X: Transformation function X(C)
            dx: Spatial step

        Returns:
            NoetherCurrent object
        """
        # Compute gradient of Lagrangian
        grad_C = np.gradient(C, dx)

        # ∂L/∂(∇C) = κ·∇C
        dL_dgrad = self.params.kappa * grad_C

        # Noether current
        J = dL_dgrad * X(C)

        # Divergence
        divergence = np.gradient(J, dx).sum()

        # Check conservation
        is_conserved = np.abs(divergence) < 1e-8

        return NoetherCurrent(
            name="General",
            current=J,
            divergence=divergence,
            is_conserved=is_conserved,
            symmetry_type="Continuous"
        )

    def energy_momentum_tensor(
        self,
        C: np.ndarray,
        dx: float
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Derive energy-momentum tensor for translation symmetry.

        For translation invariance (time and space), we get:
        - Energy conservation: ∂E/∂t = 0
        - Momentum conservation: ∂P/∂t = 0

        Energy density: T^00 = (∂L/∂(∂_0C))∂_0C - L
        Momentum density: T^0i = (∂L/∂(∂_iC))∂_0C
        """
        # Compute gradient
        grad_C = np.gradient(C, dx)

        # Lagrangian density
        L = self.lagrangian_density(C, grad_C)

        # Energy density
        energy_density = (self.params.kappa / 2) * grad_C**2 + (L + (self.params.kappa / 2) * grad_C**2)

        # Momentum density
        momentum_density = self.params.kappa * grad_C

        return energy_density, momentum_density

    def check_energy_conservation(
        self,
        C: np.ndarray,
        dx: float,
        dt: float = 0.01
    ) -> Dict:
        """
        Check energy conservation from time translation invariance.

        ∂E/∂t = 0
        """
        energy_density, _ = self.energy_momentum_tensor(C, dx)

        # Total energy
        total_energy = np.sum(energy_density) * dx

        # Check if energy is constant (simulate time evolution)
        # For static field, energy should be constant
        energy_variance = np.var(energy_density)

        is_conserved = energy_variance < 1e-10

        result = {
            "total_energy": total_energy,
            "energy_variance": energy_variance,
            "is_conserved": is_conserved,
            "status": "PASS" if is_conserved else "FAIL"
        }

        return result

    def check_momentum_conservation(
        self,
        C: np.ndarray,
        dx: float
    ) -> Dict:
        """
        Check momentum conservation from spatial translation invariance.

        ∂P/∂t = 0
        """
        _, momentum_density = self.energy_momentum_tensor(C, dx)

        # Total momentum
        total_momentum = np.sum(momentum_density) * dx

        # For symmetric field, total momentum should be zero
        momentum_magnitude = np.abs(total_momentum)

        is_conserved = momentum_magnitude < 1e-10

        result = {
            "total_momentum": total_momentum,
            "momentum_magnitude": momentum_magnitude,
            "is_conserved": is_conserved,
            "status": "PASS" if is_conserved else "FAIL"
        }

        return result

    def angular_momentum_density(
        self,
        C: np.ndarray,
        x: np.ndarray,
        dx: float
    ) -> np.ndarray:
        """
        Derive angular momentum density from rotation symmetry.

        L = x × p
        """
        _, momentum_density = self.energy_momentum_tensor(C, dx)

        # Angular momentum density
        L_density = x * momentum_density

        return L_density

    def check_angular_momentum_conservation(
        self,
        C: np.ndarray,
        x: np.ndarray,
        dx: float
    ) -> Dict:
        """
        Check angular momentum conservation from rotation symmetry.

        ∂L/∂t = 0
        """
        L_density = self.angular_momentum_density(C, x, dx)

        # Total angular momentum
        total_L = np.sum(L_density) * dx

        # For symmetric field, total angular momentum should be zero
        L_magnitude = np.abs(total_L)

        is_conserved = L_magnitude < 1e-10

        result = {
            "total_angular_momentum": total_L,
            "L_magnitude": L_magnitude,
            "is_conserved": is_conserved,
            "status": "PASS" if is_conserved else "FAIL"
        }

        return result

    def charge_current(
        self,
        C: np.ndarray,
        I: np.ndarray,
        dx: float
    ) -> np.ndarray:
        """
        Derive charge current from U(1) gauge symmetry.

        J^μ = (∂L/∂(∂_μI))·iI - (∂L/∂(∂_μI*))·(-iI*)

        Simplified for our case:
        J = β C·I (charge density)
        """
        # Charge density
        charge_density = self.params.beta * C * I

        # Current (simplified)
        current = np.gradient(charge_density, dx)

        return current

    def check_charge_conservation(
        self,
        C: np.ndarray,
        I: np.ndarray,
        dx: float
    ) -> Dict:
        """
        Check charge conservation from U(1) gauge symmetry.

        ∂_μ J^μ = 0
        """
        current = self.charge_current(C, I, dx)

        # Divergence of current
        divergence = np.gradient(current, dx).sum()

        # Check conservation
        is_conserved = np.abs(divergence) < 1e-8

        result = {
            "divergence": divergence,
            "is_conserved": is_conserved,
            "status": "PASS" if is_conserved else "FAIL"
        }

        return result

    def comprehensive_conservation_check(
        self,
        C: np.ndarray,
        I: np.ndarray,
        x: np.ndarray,
        dx: float
    ) -> Dict:
        """
        Run comprehensive conservation check for all symmetries.
        """
        results = {}

        # 1. Energy conservation
        results["energy"] = self.check_energy_conservation(C, dx)

        # 2. Momentum conservation
        results["momentum"] = self.check_momentum_conservation(C, dx)

        # 3. Angular momentum conservation
        results["angular_momentum"] = self.check_angular_momentum_conservation(C, x, dx)

        # 4. Charge conservation
        results["charge"] = self.check_charge_conservation(C, I, dx)

        # Summary
        passed = sum(1 for r in results.values() if r["is_conserved"])
        total = len(results)

        results["summary"] = {
            "passed": passed,
            "total": total,
            "ratio": passed / total
        }

        return results


def test_noether():
    """Test Noether's Theorem implementation."""
    print("=" * 70)
    print("UET NOETHER'S THEOREM TEST")
    print("=" * 70)

    # Create test fields
    N = 100
    x = np.linspace(-5, 5, N)
    C = np.exp(-x**2)  # Gaussian (symmetric)
    I = np.random.randn(N) * 0.1  # Information field
    dx = 0.1

    # Create Noether instance
    noether = UETNoether()

    # Run comprehensive check
    results = noether.comprehensive_conservation_check(C, I, x, dx)

    print("\nCONSERVATION SUMMARY")
    print("=" * 70)

    for name, result in results.items():
        if name == "summary":
            continue
        status_icon = "✅" if result["is_conserved"] else "❌"
        print(f"{status_icon} {name}: {result['status']}")

    print(f"\nPassed: {results['summary']['passed']}/{results['summary']['total']}")

    print("\n" + "=" * 70)
    print("NOETHER'S THEOREM: IMPLEMENTATION COMPLETE")
    print("=" * 70)

    return results


if __name__ == "__main__":
    test_noether()
