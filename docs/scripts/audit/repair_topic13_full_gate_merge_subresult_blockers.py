"""Merge preserved source-level blockers into the Topic 13 full result."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
RUNNER = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    old = (
        '            for item in previous_major.get("what_remains_open", [])\n'
        '            if item not in {\n'
    )
    new = (
        '        *source_level_blockers,\n'
        '        *[\n'
        '            item\n'
        '            for item in previous_major.get("what_remains_open", [])\n'
        '            if item not in {\n'
    )
    if (
        "        *source_level_blockers,\n" not in text
        and "source_level_blockers =" not in text
    ):
        if text.count(old) != 1:
            raise SystemExit(f"source blocker merge anchor: expected one match, found {text.count(old)}")
        text = text.replace(
            '        *[\n'
            '            item\n'
            '            for item in previous_major.get("what_remains_open", [])\n'
            '            if item not in {\n',
            new,
            1,
        )
        TARGET.write_text(text, encoding="utf-8")

    runner_text = RUNNER.read_text(encoding="utf-8-sig")
    command = '    "docs/scripts/audit/repair_topic13_full_gate_merge_subresult_blockers.py",\n'
    if command not in runner_text:
        needle = '    "docs/scripts/audit/repair_topic13_full_gate_preserve_subresult_blockers.py",\n'
        if runner_text.count(needle) != 1:
            raise SystemExit("runner subresult blocker anchor not found")
        RUNNER.write_text(runner_text.replace(needle, needle + command, 1), encoding="utf-8")
    print("TOPIC13_SUBRESULT_BLOCKERS_MERGED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
