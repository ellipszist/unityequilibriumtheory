from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_ding_c_src_independent_reproduction_boundary.py"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    text = replace_once(
        text,
        '        "mp48_holdout_excluded": package.get("holdout", {}).get("xie_2026_accessed") is False,\n        "mp48_alpha_fit_excluded": package.get("holdout", {}).get("alpha_fit_used") is False,\n',
        '        "mp48_holdout_excluded": package.get("holdout_policy", {}).get("xie_2026_accessed") is False,\n        "mp48_alpha_fit_excluded": package.get("holdout_policy", {}).get("alpha_fit_used") is False,\n',
        "holdout schema",
    )
    TARGET.write_text(text, encoding="utf-8")
    print("patched", TARGET)


if __name__ == "__main__":
    main()
