from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    old = '''    artifact["major_result"]["what_remains_open"] = list(dict.fromkeys([
        *artifact["major_result"].get("what_remains_open", []),
        *source_level_blockers,
        *[
            item
            for item in previous_major.get("what_remains_open", [])
            if item not in {
                "formal_conserved_C_no_go_or_explicit_regularization_missing",
                "ttg_numeric_source_package_is_provisional",
                "named finite-cone branch or explicit conserved-C regularization",
                "named_finite_cone_branch_or_explicit_regularization_missing",
                "original_conserved_c_gradient_baseline_blocked",
            }
        ],
    ]))
'''
    new = '''    # Keep the major-result projection readable: only the full-gate
    # controllers belong here. Lane-specific open inputs remain nested in
    # verification_status and evidence artifacts.
    artifact["major_result"]["what_remains_open"] = list(dict.fromkeys(blockers))
'''
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"primary blocker projection: expected one match, found {count}")
    TARGET.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("patched", TARGET)


if __name__ == "__main__":
    main()
