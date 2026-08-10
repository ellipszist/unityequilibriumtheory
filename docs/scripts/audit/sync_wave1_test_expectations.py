"""Synchronize legacy tests with the Wave 1 provisional-intake boundary.

The replacements are guarded by exact old text so this helper cannot rewrite
unrelated test content.
"""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"expected exactly one guarded match in {path}: {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def main() -> int:
    mapping = ROOT / "docs/core/test/test_thermal_source_observable_mapping.py"
    replace_once(
        mapping,
        '    assert not artifact["gates"]["local_numeric_source_package_present"]\n',
        '    assert artifact["gates"]["local_numeric_source_package_present"]\n',
    )
    replace_once(
        mapping,
        '    assert all(row["local_numeric_path"] is None for row in payload["sources"])\n',
        '    non_holdout = [row for row in payload["sources"] if "holdout" not in row["source_id"]]\n'
        '    assert any(row["local_numeric_path"] for row in non_holdout)\n'
        '    holdout = next(row for row in payload["sources"] if "holdout" in row["source_id"])\n'
        '    assert holdout["local_numeric_path"] is None\n',
    )
    pilot = ROOT / "docs/core/test/test_matter_space_thermal_pilot.py"
    replace_once(pilot, "def test_source_package_is_metadata_only_and_holdout_locked() -> None:\n", "def test_source_package_is_provisional_intake_and_holdout_locked() -> None:\n")
    replace_once(pilot, '    assert package["status"] == "BLOCKED"\n', '    assert package["status"] == "PROVISIONAL_NUMERIC_SOURCE_INTAKE"\n')
    replace_once(pilot, '    assert package["usage_policy"]["observable_map_status"] == "MISSING"\n', '    assert package["usage_policy"]["observable_map_status"] == "NORMALIZED_DEFINED_DIMENSIONAL_BLOCKED"\n')
    replace_once(
        pilot,
        '    assert all(source["local_raw_path"] is None for source in package["sources"])\n',
        '    assert any(source.get("local_numeric_path") for source in package["sources"] if "holdout" not in source["source_id"])\n'
        '    assert all(source.get("local_numeric_path") is None for source in package["sources"] if "holdout" in source["source_id"])\n',
    )
    print("status=PASS_GUARDED_WAVE1_TEST_EXPECTATIONS_SYNCED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
