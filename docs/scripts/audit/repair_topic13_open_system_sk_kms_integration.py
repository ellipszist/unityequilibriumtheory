from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]


def patch_full_gate() -> None:
    path = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
    text = path.read_text(encoding="utf-8-sig")
    old = "'T13_GRAPHITE_GREEN_KUBO_SOURCE_BOUNDARY': 'graphite_green_kubo_source_boundary'}"
    new = "'T13_GRAPHITE_GREEN_KUBO_SOURCE_BOUNDARY': 'graphite_green_kubo_source_boundary', 'T13_UET_O2_OPEN_SYSTEM_SK_KMS_ENTROPY_LANE': 'uet_o2_open_system_sk_kms_entropy_lane'}"
    if new in text:
        return
    if text.count(old) != 1:
        raise SystemExit("full-gate lane suffix is not uniquely identifiable")
    path.write_text(text.replace(old, new), encoding="utf-8")


def patch_sync() -> None:
    path = ROOT / "docs/scripts/audit/sync_topic13_major_result_lanes.py"
    text = path.read_text(encoding="utf-8-sig")
    old = '    ("T13_GRAPHITE_GREEN_KUBO_SOURCE_BOUNDARY", "graphite_green_kubo_source_boundary"),\n'
    new = old + '    ("T13_UET_O2_OPEN_SYSTEM_SK_KMS_ENTROPY_LANE", "uet_o2_open_system_sk_kms_entropy_lane"),\n'
    if '"T13_UET_O2_OPEN_SYSTEM_SK_KMS_ENTROPY_LANE"' in text:
        return
    if text.count(old) != 1:
        raise SystemExit("sync lane tuple is not uniquely identifiable")
    path.write_text(text.replace(old, new), encoding="utf-8")


if __name__ == "__main__":
    patch_full_gate()
    patch_sync()
    print("patched Topic 13 open-system SK/KMS lane integration")
