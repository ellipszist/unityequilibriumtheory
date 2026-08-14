from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SYNC = ROOT / "docs/scripts/audit/sync_topic13_major_result_lanes.py"
TEST = ROOT / "docs/core/test/test_topic13_major_result_register_sync.py"

sync_text = SYNC.read_text(encoding="utf-8")
old = '    ("T13_HUANG_2023_SUPPLEMENTARY_PAYLOAD_BOUNDARY", "huang_2023_supplementary_payload_boundary"),\n'
new = old + '    ("T13_NIST_AXM5Q1_DENSITY_SOURCE_BOUNDARY", "nist_axm5q1_density_source_boundary"),\n'
assert sync_text.count(old) == 1
SYNC.write_text(sync_text.replace(old, new), encoding="utf-8")

test_text = TEST.read_text(encoding="utf-8")
old = '        "T13_HUANG_2023_SUPPLEMENTARY_PAYLOAD_BOUNDARY",\n'
new = old + '        "T13_NIST_AXM5Q1_DENSITY_SOURCE_BOUNDARY",\n'
assert test_text.count(old) == 1
TEST.write_text(test_text.replace(old, new), encoding="utf-8")

print(SYNC)
print(TEST)
