"""Add the Oxford numeric-row lane to the Topic 13 register sync."""

from pathlib import Path


path = Path("docs/scripts/audit/sync_topic13_major_result_lanes.py")
text = path.read_text(encoding="utf-8")
old = '    ("T13_PHONIX_MP47_GRAPHITE_HARMONIC_COMPARATOR", "phonix_mp47_graphite_harmonic_comparator"),\n'
new = old + '    ("T13_OXFORD_TGS_NUMERIC_ROWS_COMPARATOR", "oxford_tgs_numeric_rows_comparator"),\n'
if "T13_OXFORD_TGS_NUMERIC_ROWS_COMPARATOR" not in text:
    if old not in text:
        raise SystemExit("expected Phonix lane sync anchor not found")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("integrated Oxford numeric-row lane into major-result register sync")
