"""Make the causal major-result sync refresh an existing register entry."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = ROOT / "docs/scripts/audit/sync_topic13_causal_branch_selection_into_gates.py"
OLD = '''        })
    (ROOT / REGISTER_REL).write_text(json.dumps(register, indent=2, ensure_ascii=True) + "\\n", encoding="utf-8")
'''
NEW = '''        })
    else:
        existing_entry = next(item for item in register["entries"] if item.get("major_result_id") == result_id)
        existing_entry["closure_level"] = action["major_result"]["closure_level"]
        existing_entry["what_is_closed"] = action["major_result"]["what_is_closed"]
        existing_entry["equation_or_mapping"] = action["major_result"]["equation_or_mapping"]
        existing_entry["units"] = action["major_result"]["units"]
        existing_entry["derivation_class"] = action["major_result"]["derivation_class"]
        existing_entry["observable"] = action["major_result"]["observable"]
        existing_entry["data_role"] = action["major_result"]["data_role"]
        existing_entry["verification_status"] = action["status"]
        existing_entry["open_blockers"] = action["major_result"]["open_blockers"]
        existing_entry["dependency_unlocked"] = action["major_result"]["dependency_unlocked"]
        existing_entry["claim_boundary"] = action["major_result"]["claim_boundary"]
        existing_entry["evidence_artifacts"] = [evidence(ACTION_REL, {"status": action["status"]})]
    (ROOT / REGISTER_REL).write_text(json.dumps(register, indent=2, ensure_ascii=True) + "\\n", encoding="utf-8")
'''


def main() -> int:
    content = TARGET.read_text(encoding="utf-8")
    if OLD in content:
        content = content.replace(OLD, NEW, 1)
    elif "existing_entry = next(item for item in register" not in content:
        raise SystemExit("expected causal sync register insertion point not found")
    TARGET.write_text(content, encoding="utf-8")
    print("PASS_REPAIRED_T13_CAUSAL_BRANCH_SYNC_HASH_REFRESH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
