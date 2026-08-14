"""Repair generated-string syntax and the Gaussian integration-test key."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SYNC = ROOT / "docs/scripts/audit/sync_topic13_uet_o2_condensate_gaussian_thermal.py"
TEST = ROOT / "docs/core/test/test_topic13_uet_o2_condensate_gaussian_thermal_integration.py"
RUNNER = ROOT / "docs/scripts/audit/run_topic13_uet_o2_condensate_gaussian_thermal_wave.py"


def replace_once(path: Path, old: str, new: str) -> bool:
    text = path.read_text(encoding="utf-8-sig")
    if new in text:
        return False
    if old not in text:
        raise SystemExit(f"repair anchor not found: {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> int:
    changed = []
    if replace_once(SYNC, "sum_{a=+,-}", "sum_a"):
        changed.append(SYNC.as_posix())
    if replace_once(
        TEST,
        '    assert partial[result_id.lower()].get("summary", {}).get("major_result_id") == result_id\n',
        '    assert partial["uet_o2_condensate_gaussian_finite_t_lane"]["summary"]["major_result_id"] == result_id\n',
    ):
        changed.append(TEST.as_posix())
    if replace_once(
        RUNNER,
        '    run("repair_topic13_gaussian_thermal_lane_key.py")\n',
        '    run("repair_topic13_gaussian_thermal_lane_key.py")\n'
        '    run("repair_topic13_gaussian_thermal_sync_syntax.py")\n',
    ):
        changed.append(RUNNER.as_posix())
    print({"status": "PASS_GAUSSIAN_THERMAL_SYNC_SYNTAX_REPAIR", "changed": changed})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
