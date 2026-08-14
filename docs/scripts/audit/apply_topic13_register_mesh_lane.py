"""Add the Topic 13 mesh-convergence lane to the reusable register sync helper."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "docs/scripts/audit/sync_topic13_major_result_lanes.py"


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    anchor = '    ("T13_GRAPHITE_ISOTHERMAL_KT_SOURCE", "graphite_isothermal_kt_source"),\n'
    insertion = anchor + '    ("T13_MP48_FORCE_CONSTANT_C_SRC_MESH_CONVERGENCE", "mp48_force_constant_csrc_mesh_convergence"),\n'
    if '"T13_MP48_FORCE_CONSTANT_C_SRC_MESH_CONVERGENCE"' not in text:
        if anchor not in text:
            raise RuntimeError("register sync lane anchor not found")
        text = text.replace(anchor, insertion, 1)
        PATH.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
