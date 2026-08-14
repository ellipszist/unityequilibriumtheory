from pathlib import Path


path = Path("docs/scripts/audit/sync_topic13_major_result_lanes.py")
text = path.read_text(encoding="utf-8")
old = '    ("T13_DING_MATERIAL_REGIME_BOUNDARY", "ding_material_regime_boundary"),\n'
new = old + '    ("T13_PHONIX_MP47_GRAPHITE_HARMONIC_COMPARATOR", "phonix_mp47_graphite_harmonic_comparator"),\n'
if old not in text:
    raise SystemExit("expected Topic 13 lane sync anchor not found")
if "T13_PHONIX_MP47_GRAPHITE_HARMONIC_COMPARATOR" not in text:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("integrated Phonix lane into major-result register sync")
