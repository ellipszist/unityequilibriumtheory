"""Make the remaining Topic 13 compatibility repair safe to rerun."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/repair_topic13_full_gate_remaining_compatibility.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def main() -> int:
    text = TARGET.read_text(encoding="utf-8-sig")
    original = text

    old = '    text, _ = replace_once(text, old, new, "legacy beta status alias")\n'
    new = (
        '    if "beta_alias = artifact[\\"verification_status\\"]" not in text:\n'
        '        text, _ = replace_once(text, old, new, "legacy beta status alias")\n'
    )
    if old in text and new not in text:
        text = replace_once(text, old, new, "beta repair idempotence")

    old = '    text, _ = replace_once(text, old, new, "mp-48 package evidence")\n'
    new = (
        '    if "mp48_package_path = ROOT /" not in text:\n'
        '        text, _ = replace_once(text, old, new, "mp-48 package evidence")\n'
    )
    if old in text and new not in text:
        text = replace_once(text, old, new, "mp-48 repair idempotence")

    old = '    text, _ = replace_once(text, old, new, "full-result evidence preparation")\n'
    new = (
        '    if "t13_evidence = [ref(rel(T13)" not in text:\n'
        '        text, _ = replace_once(text, old, new, "full-result evidence preparation")\n'
    )
    if old in text and new not in text:
        text = replace_once(text, old, new, "register preparation idempotence")

    old = '    text, _ = replace_once(text, old, new, "full-result evidence field")\n'
    new = (
        '    if "\\\"evidence_artifacts\\\": t13_evidence" not in text:\n'
        '        text, _ = replace_once(text, old, new, "full-result evidence field")\n'
    )
    if old in text and new not in text:
        text = replace_once(text, old, new, "register evidence idempotence")

    if text != original:
        TARGET.write_text(text, encoding="utf-8")
    print({"changed": text != original})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
