"""Replace the remaining brace-bearing formula literal in the Gaussian sync."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SYNC = ROOT / "docs/scripts/audit/sync_topic13_uet_o2_condensate_gaussian_thermal.py"
RUNNER = ROOT / "docs/scripts/audit/run_topic13_uet_o2_condensate_gaussian_thermal_wave.py"


def main() -> int:
    text = SYNC.read_text(encoding="utf-8-sig")
    old = "sum_{a=+,-}"
    new = "sum_a"
    changed = False
    if old in text:
        SYNC.write_text(text.replace(old, new), encoding="utf-8")
        changed = True
    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    anchor = '    run("repair_topic13_gaussian_thermal_sync_syntax.py")\n'
    addition = anchor + '    run("repair_topic13_gaussian_thermal_formula_literal.py")\n'
    if "repair_topic13_gaussian_thermal_formula_literal.py" not in runner_text:
        if anchor not in runner_text:
            raise SystemExit("Gaussian wave runner repair anchor not found")
        RUNNER.write_text(runner_text.replace(anchor, addition, 1), encoding="utf-8")
        changed = True
    print({"status": "PASS_GAUSSIAN_THERMAL_FORMULA_LITERAL_REPAIR", "changed": changed})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
