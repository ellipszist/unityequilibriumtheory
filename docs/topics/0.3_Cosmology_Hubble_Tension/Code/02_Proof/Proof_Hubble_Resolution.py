"""
UET scalar H0 benchmark check.

Topic: 0.3 - Cosmology / Hubble Tension

This legacy proof entry point is retained as a quick engine smoke check. It does
not establish a full Hubble-tension resolution or full cosmology validation.
"""

from pathlib import Path
import sys

def _bootstrap():
    curr = Path(__file__).resolve()
    for parent in [curr] + list(curr.parents):
        if (parent / "docs").exists() and (parent / "docs" / "core").exists():
            if str(parent) not in sys.path:
                sys.path.insert(0, str(parent))
            return parent
    return None


root_path = _bootstrap()
if not root_path:
    print("CRITICAL: UET docs root not found!")
    sys.exit(1)
topic_path = root_path / "docs" / "topics" / "0.3_Cosmology_Hubble_Tension"
engine_path = topic_path / "Code" / "01_Engine"
if str(engine_path) not in sys.path:
    sys.path.insert(0, str(engine_path))

try:
    from Engine_Cosmology import UETCosmologyEngine
except ImportError as e:
    print(f"CRITICAL SETUP ERROR: {e}")
    sys.exit(1)


def prove_hubble_resolution():
    print("=" * 60)
    print("UET SCALAR H0 BENCHMARK CHECK")
    print("=" * 60)

    engine = UETCosmologyEngine()
    engine.step()

    metrics = engine.get_extra_metrics()
    h0_pred = metrics.get("H0_predicted", 0.0)

    print(f"  UET Hubble Parameter H0: {h0_pred:.2f}")

    if 72 < h0_pred < 74:
        print("  PASS: scalar H0 benchmark is inside the legacy expected range.")
        print("  Claim boundary: this is not a full Hubble-tension resolution.")
        return True

    print(f"  FAIL: Predicted H0 ({h0_pred:.2f}) out of expected range (72-74).")
    return False


if __name__ == "__main__":
    prove_hubble_resolution()
