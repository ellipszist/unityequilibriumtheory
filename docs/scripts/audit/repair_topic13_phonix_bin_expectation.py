from pathlib import Path


path = Path("docs/scripts/audit/audit_topic13_phonix_mp47_graphite_comparator.py")
text = path.read_text(encoding="utf-8")
old = 'len(frequencies) == len(dos) and len(frequencies) == 50'
new = 'len(frequencies) == len(dos) and len(frequencies) == 51'
if old not in text:
    raise SystemExit("expected Phonix bin expectation was not found")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("repaired Phonix bin expectation")
