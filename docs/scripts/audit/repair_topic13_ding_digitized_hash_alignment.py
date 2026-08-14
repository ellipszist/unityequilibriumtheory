"""Align all Ding Figure 1d manifest hashes with the archived CSV bytes."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CSV = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/ding_2022_fig1d_digitized.csv"
PACKAGE = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_second_sound_source_package.json"
REVIEW = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/matter_space_thermal_source_review.json"
MANIFEST = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/ding_2022_fig1d_digitized_manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    digest = sha256(CSV)
    package = json.loads(PACKAGE.read_text(encoding="utf-8-sig"))
    review = json.loads(REVIEW.read_text(encoding="utf-8-sig"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8-sig"))
    for row in package.get("sources", []):
        if row.get("source_id") == "ding_2022_fig1d_digitized":
            row["output_hash"] = digest
    for row in review.get("sources", []):
        if row.get("source_id") == "ding_2022_fig1d_digitized":
            row["local_numeric_hash"] = digest
            row["external_numeric_status"] = "figure_asset_digitized_locally_with_closed_mapping"
    manifest["output_sha256"] = digest
    PACKAGE.write_text(json.dumps(package, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    REVIEW.write_text(json.dumps(review, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS_DING_FIG1D_HASH_ALIGNMENT", "sha256": digest}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
