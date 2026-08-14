from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
paths = [
    ROOT / "docs/topics/0.13_Thermodynamic_Bridge/UPDATE_LOG.md",
    ROOT / "docs/topics/0.13_Thermodynamic_Bridge/DATA_MANIFEST.md",
    ROOT / "docs/topics/0.13_Thermodynamic_Bridge/FULL_THERMODYNAMIC_BRIDGE_CORE_READY_CURRENT.md",
    ROOT / "WORK_LEDGER/2026/2026-08-13.md",
]

for path in paths:
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "focused source/register tests passed (`2 passed`)",
        "focused source/register tests passed (`2 passed`); full Topic 13 regression passed (`176 passed, 625 deselected`)",
    )
    path.write_text(text, encoding="utf-8")

print("recorded full regression")
