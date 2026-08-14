"""Align Ding Fig. 1d row metadata with the closed printed-legend mapping."""

from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
CSV_REL = "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/ding_2022_fig1d_digitized.csv"
MANIFEST_REL = "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/ding_2022_fig1d_digitized_manifest.json"
OLD_LOCATOR = "Nature Communications 13, 285 (2022), Fig. 1d; color mapping remains open"
NEW_LOCATOR = "Nature Communications 13, 285 (2022), Fig. 1d; printed-legend mapping artifact"
OLD_STATUS = "OPEN_COLOR_TO_GRATING_PERIOD"
NEW_STATUS = "CLOSED_COLOR_TO_GRATING_PERIOD"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    csv_path = ROOT / CSV_REL
    manifest_path = ROOT / MANIFEST_REL
    text = csv_path.read_text(encoding="utf-8-sig")
    before_hash = digest(csv_path)
    locator_count = text.count(OLD_LOCATOR)
    status_count = text.count(OLD_STATUS)
    expected_rows = 432
    if locator_count != expected_rows or status_count != expected_rows:
        raise SystemExit(
            f"expected {expected_rows} stale locator/status values, "
            f"found locator={locator_count}, status={status_count}"
        )
    repaired = text.replace(OLD_LOCATOR, NEW_LOCATOR).replace(OLD_STATUS, NEW_STATUS)
    csv_path.write_text(repaired, encoding="utf-8")
    after_hash = digest(csv_path)

    manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
    manifest["output_sha256"] = after_hash
    manifest["row_metadata_alignment"] = {
        "status": "PASS_ROW_METADATA_ALIGNED_WITH_PRINTED_LEGEND_MAPPING",
        "checked_row_count": expected_rows,
        "changed_fields": ["source_locator", "series_mapping_status"],
        "source_locator": NEW_LOCATOR,
        "series_mapping_status": NEW_STATUS,
        "pre_repair_sha256": before_hash,
        "post_repair_sha256": after_hash,
        "repaired_on": date.today().isoformat(),
        "numeric_values_changed": False,
        "data_role": "FIGURE_DERIVED_NORMALIZED_COMPARISON_NOT_RAW_SOURCE",
    }
    manifest_path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "status": "PASS_REPAIRED_TOPIC13_DING_FIG1D_ROW_METADATA",
        "rows_checked": expected_rows,
        "changed_fields": ["source_locator", "series_mapping_status"],
        "pre_repair_sha256": before_hash,
        "post_repair_sha256": after_hash,
        "numeric_values_changed": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
