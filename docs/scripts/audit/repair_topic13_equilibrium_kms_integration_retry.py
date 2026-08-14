"""Retry the Topic 13 KMS integration with gate indentation compatibility."""

from __future__ import annotations

from docs.scripts.audit import repair_topic13_equilibrium_kms_integration as repair


_original_replace_once = repair.replace_once


def flexible_replace(text: str, old: str, new: str, label: str) -> str:
    if old not in text and "iaea_graphite_cv_rel" in old:
        old = old.replace("      iaea_graphite_cv_rel", "    iaea_graphite_cv_rel", 1)
        new = "\n".join(
            line[2:] if line.startswith("  ") else line
            for line in new.splitlines()
        )
    return _original_replace_once(text, old, new, label)


repair.replace_once = flexible_replace


if __name__ == "__main__":
    raise SystemExit(repair.main())

