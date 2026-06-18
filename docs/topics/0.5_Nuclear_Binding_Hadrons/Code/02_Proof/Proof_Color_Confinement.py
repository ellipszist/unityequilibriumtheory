"""
UET diagnostic: color confinement / proton-mass consistency.

This script is not a formal confinement proof. It provides a real pass/fail
return contract for the legacy diagnostic check so audit artifacts can record
the result instead of relying on printed text.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path


def _bootstrap() -> Path | None:
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None


ROOT = _bootstrap()
if not ROOT:
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)


ENGINE_PATH = (
    ROOT
    / "docs"
    / "topics"
    / "0.5_Nuclear_Binding_Hadrons"
    / "Code"
    / "01_Engine"
    / "Engine_Hadron_Model.py"
)


def _load_engine_class():
    spec = importlib.util.spec_from_file_location("Engine_Hadron_Model", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load engine: {ENGINE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, "UETNuclearEngine")


UETNuclearEngine = _load_engine_class()


def _default_params():
    try:
        from docs.core.uet_master_equation import UETParameters

        return UETParameters(kappa=1.0, beta=1.0)
    except Exception:

        class MockParams:
            def __init__(self):
                self.kappa = 1.0
                self.beta = 1.0
                self.alpha = 1.0

        return MockParams()


def evaluate_confinement() -> dict:
    """Return the narrow diagnostic confinement/proton-mass check result."""
    engine = UETNuclearEngine(uet_params=_default_params())
    engine.step()
    metrics = engine.get_extra_metrics()
    proton_mass_gev = metrics["proton_mass_gev"]
    passed = 0.9 < proton_mass_gev < 1.01
    return {
        "status": "PASS" if passed else "FAIL",
        "passed": passed,
        "proton_mass_gev": proton_mass_gev,
        "threshold_min_gev": 0.9,
        "threshold_max_gev": 1.01,
        "claim_boundary": (
            "This is a narrow diagnostic proton-mass consistency check. "
            "It is not a formal proof of color confinement."
        ),
    }


def prove_confinement() -> bool:
    print("=" * 60)
    print("UET DIAGNOSTIC: COLOR CONFINEMENT CHECK")
    print("=" * 60)
    result = evaluate_confinement()
    print(f"  Proton Mass (Predicted): {result['proton_mass_gev']:.4f} GeV")
    if result["passed"]:
        print("  PASS: narrow proton-mass diagnostic threshold satisfied.")
    else:
        print("  FAIL: narrow proton-mass diagnostic threshold not satisfied.")
    print("  NOTE: This does not certify a formal confinement proof.")
    return result["passed"]


if __name__ == "__main__":
    sys.exit(0 if prove_confinement() else 1)
