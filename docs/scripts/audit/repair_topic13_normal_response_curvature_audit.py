"""Remove the temporary no-op placeholder from the curvature audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_uet_o2_normal_response_curvature.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = (
        "    thermal_phi_plus = uet_o2_normal_response_curvature_state(\n"
        "        TEMPERATURE,\n"
        "        CHEMICAL_PHEMICAL_POTENTIAL if False else CHEMICAL_POTENTIAL,\n"
        "        PHI + h_phi,\n"
        "        eos_config,\n"
        "        quadrature_order=REFERENCE_ORDER,\n"
        "        cutoff_factor=REFERENCE_CUTOFF_FACTOR,\n"
        "    )\n"
        "    del thermal_phi_plus\n"
    )
    if old in text:
        text = text.replace(old, "", 1)
        TARGET.write_text(text, encoding="utf-8")
    print("PASS_REPAIRED_TOPIC13_NORMAL_RESPONSE_CURVATURE_AUDIT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
