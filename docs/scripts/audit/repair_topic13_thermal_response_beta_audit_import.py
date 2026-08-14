"""Repair the local import bootstrap in the new Topic 13 beta audit."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_thermal_response_beta_contract.py"
OLD = "import hashlib\nimport json\nfrom datetime import date\nfrom pathlib import Path\nfrom typing import Any\n\nfrom docs.core.thermal_response_beta_contract import ("
NEW = "import hashlib\nimport json\nimport sys\nfrom datetime import date\nfrom pathlib import Path\nfrom typing import Any\n\nROOT = Path(__file__).resolve().parents[3]\nif str(ROOT) not in sys.path:\n    sys.path.insert(0, str(ROOT))\n\nfrom docs.core.thermal_response_beta_contract import ("


def main() -> int:
    content = TARGET.read_text(encoding="utf-8")
    if OLD in content:
        content = content.replace(OLD, NEW, 1)
    duplicate = "\nROOT = Path(__file__).resolve().parents[3]\nCONTRACT_REL ="
    if duplicate in content:
        content = content.replace(duplicate, "\nCONTRACT_REL =", 1)
    TARGET.write_text(content, encoding="utf-8")
    print("PASS_REPAIRED_T13_THERMAL_RESPONSE_BETA_AUDIT_IMPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
