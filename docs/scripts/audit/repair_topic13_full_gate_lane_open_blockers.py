from pathlib import Path


path = Path("docs/scripts/audit/audit_topic13_full_bridge_gate.py")
text = path.read_text(encoding="utf-8")
old = '''                "controlling_blocker": candidate.get("controlling_blocker", major.get("open_blockers", [None])[0]),
                "claim_boundary": major.get("claim_boundary", "artifact-reported boundary"),
'''
new = '''                "controlling_blocker": candidate.get("controlling_blocker", major.get("open_blockers", [None])[0]),
                "open_blockers": major.get("open_blockers", candidate.get("open_blockers", [])),
                "claim_boundary": major.get("claim_boundary", "artifact-reported boundary"),
'''
if text.count(old) != 1:
    raise SystemExit(f"expected one lane record insertion point, found {text.count(old)}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("preserved lane open_blockers in the full-gate discovery projection")
