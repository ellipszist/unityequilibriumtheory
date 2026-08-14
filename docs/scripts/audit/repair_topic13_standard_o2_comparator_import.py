"""Make the standalone comparator audit resolve the repository package."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "docs/scripts/audit/audit_topic13_standard_o2_finite_temperature_comparator.py"


def main() -> int:
    text = AUDIT.read_text(encoding="utf-8")
    old = "import hashlib\nimport json\nfrom datetime import date\nfrom pathlib import Path\n\nimport numpy as np\n"
    new = "import hashlib\nimport json\nimport sys\nfrom datetime import date\nfrom pathlib import Path\n\nimport numpy as np\n\nif str(Path(__file__).resolve().parents[3]) not in sys.path:\n    sys.path.insert(0, str(Path(__file__).resolve().parents[3]))\n"
    if old not in text:
        raise SystemExit("comparator audit import block not found")
    AUDIT.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("PATCHED_T13_STANDARD_O2_COMPARATOR_IMPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
