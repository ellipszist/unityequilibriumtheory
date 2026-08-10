"""Synchronize the Topic 0.3 index from the nested scalar artifact status."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
INDEX = ROOT / "docs/topics/README.md"
ARTIFACT = ROOT / "docs/topics/0.3_Cosmology_Hubble_Tension/Result/artifacts/hubble_comparison_validation.json"


def main() -> int:
    artifact = json.loads(ARTIFACT.read_text(encoding="utf-8-sig"))
    status = artifact.get("status", artifact.get("audit_status", artifact.get("results", {}).get("status")))
    text = INDEX.read_text(encoding="utf-8")
    changed = False
    if status == "PASS":
        replacements = {
            "0.3 currently fails its stated verification threshold": "the latest scalar Hubble artifact for 0.3 passes its stated benchmark threshold; full cosmology remains blocked",
            "but the current Hubble artifact fails its stated threshold": "the latest scalar Hubble artifact passes its stated threshold; full cosmology remains blocked",
        }
        for old, new in replacements.items():
            if old in text:
                text = text.replace(old, new)
                changed = True
    if changed:
        INDEX.write_text(text, encoding="utf-8")
    print(json.dumps({"artifact_status": status, "index_changed": changed}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
