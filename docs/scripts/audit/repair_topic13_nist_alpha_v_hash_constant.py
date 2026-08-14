from pathlib import Path


path = Path("docs/scripts/audit/audit_topic13_nist_graphite_alpha_v_source_boundary.py")
text = path.read_text(encoding="utf-8")
old = 'PDF_SHA256 = "fbcde491cadf6b8105d8b22bd15145e48709926aaf1d4a24335af2a8984c71d2"'
new = 'PDF_SHA256 = "fbcde491cadf6b8105d8b22bd15145e48709926aaf1d4a24335af2a8984c71b2"'
if text.count(old) != 1:
    raise SystemExit(f"expected one hash constant, found {text.count(old)}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("repaired NIST PDF hash constant")
