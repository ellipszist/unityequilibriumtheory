"""Extend the Topic 13 register-sync regression expectation for the mesh lane."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PATH = ROOT / "docs/core/test/test_topic13_major_result_register_sync.py"


def main() -> None:
    text = PATH.read_text(encoding="utf-8")
    anchor = '        "T13_GRAPHITE_ISOTHERMAL_KT_SOURCE",\n'
    insertion = anchor + '        "T13_MP48_FORCE_CONSTANT_C_SRC_MESH_CONVERGENCE",\n'
    if '"T13_MP48_FORCE_CONSTANT_C_SRC_MESH_CONVERGENCE"' not in text:
        if anchor not in text:
            raise RuntimeError("register-sync test anchor not found")
        PATH.write_text(text.replace(anchor, insertion, 1), encoding="utf-8")


if __name__ == "__main__":
    main()
