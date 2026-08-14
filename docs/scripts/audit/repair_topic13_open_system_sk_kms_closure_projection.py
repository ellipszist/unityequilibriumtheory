from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"

OLD = '    if discovered_lane_integrations.get("iaea_cv_uncertainty_boundary", {}).get("closure_level") == "CLOSED_FOR_LANE":\n'
NEW = (
    '    if discovered_lane_integrations.get("uet_o2_open_system_sk_kms_entropy_lane", {}).get("closure_level") == "CLOSED_FOR_LANE":\n'
    '        lane_closures.append("formal open-system SK/KMS, FDT, retardedness, and entropy-positivity lane is closed without promoting formal gamma/noise to physical Kubo, SI, alpha, or TTG evidence")\n'
    + OLD
)


def main() -> None:
    text = PATH.read_text(encoding="utf-8-sig")
    if "formal open-system SK/KMS, FDT, retardedness" in text:
        print("closure projection already present")
        return
    if text.count(OLD) != 1:
        raise SystemExit("full-gate closure insertion point is not unique")
    PATH.write_text(text.replace(OLD, NEW), encoding="utf-8")
    print("patched Topic 13 open-system closure projection")


if __name__ == "__main__":
    main()
