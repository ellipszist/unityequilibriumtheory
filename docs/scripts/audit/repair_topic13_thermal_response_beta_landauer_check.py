"""Tighten the beta-contract audit to inspect equations rather than labels."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_thermal_response_beta_contract.py"
OLD = '"landauer_is_not_used": branch["beta_th_identity"] == "not used" and "Landauer" not in contract_text,'
NEW = '"landauer_is_not_used": branch["beta_th_identity"] == "not used" and "k_B" not in contract_text and "ln(2)" not in contract_text,'


def main() -> int:
    content = TARGET.read_text(encoding="utf-8")
    if OLD not in content and NEW not in content:
        raise SystemExit("expected Landauer audit condition not found")
    TARGET.write_text(content.replace(OLD, NEW, 1), encoding="utf-8")
    print("PASS_REPAIRED_T13_THERMAL_RESPONSE_BETA_LANDAUER_CHECK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
