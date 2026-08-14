"""Keep the Berut Figure 3 provenance audit honest about its zero-row state."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT_SCRIPT = ROOT / "docs/scripts/audit/audit_topic13_berut_figure3_binary_identity.py"
TEST_SCRIPT = ROOT / "docs/core/test/test_topic13_berut_figure3_binary_identity.py"
RUNNER = ROOT / "docs/scripts/audit/run_topic13_berut_figure3_binary_identity_wave.py"


def replace_once(path: Path, old: str, new: str) -> bool:
    text = path.read_text(encoding="utf-8-sig")
    if new in text:
        return False
    if old not in text:
        raise SystemExit(f"repair anchor not found: {path}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    return True


def main() -> int:
    changed = []
    if replace_once(
        AUDIT_SCRIPT,
        "        'numeric_rows_emitted': True,\n",
        "        # Provenance and asset identity do not constitute accepted source rows.\n"
        "        'numeric_rows_emitted': False,\n"
        "        'digitization_ready': False,\n"
        "        'numeric_row_contract_status': 'OPEN_PANEL_AXIS_POINT_MAPPING',\n",
    ):
        changed.append(AUDIT_SCRIPT.as_posix())
    if replace_once(
        AUDIT_SCRIPT,
        "        'numeric_rows_emitted': 0,\n        'numeric_alpha_Phi_K_emitted': False,\n",
        "        'numeric_rows_emitted': 0,\n"
        "        'digitization_ready': False,\n"
        "        'numeric_row_contract_status': 'OPEN_PANEL_AXIS_POINT_MAPPING',\n"
        "        'numeric_alpha_Phi_K_emitted': False,\n",
    ):
        changed.append(AUDIT_SCRIPT.as_posix())
    if replace_once(
        TEST_SCRIPT,
        "        if key not in {'xie_2026_not_accessed', 'xie_2026_not_consumed'}\n",
        "        if key not in {\n"
        "            'xie_2026_not_accessed',\n"
        "            'xie_2026_not_consumed',\n"
        "            'numeric_rows_emitted',\n"
        "            'digitization_ready',\n"
        "        }\n",
    ):
        changed.append(TEST_SCRIPT.as_posix())
    if replace_once(
        TEST_SCRIPT,
        "    assert checks['xie_2026_not_consumed'] is True\n",
        "    assert checks['xie_2026_not_consumed'] is True\n"
        "    assert checks['numeric_rows_emitted'] is False\n"
        "    assert checks['digitization_ready'] is False\n",
    ):
        changed.append(TEST_SCRIPT.as_posix())
    if replace_once(
        TEST_SCRIPT,
        "    assert artifact['numeric_rows_emitted'] == 0\n",
        "    assert artifact['numeric_rows_emitted'] == 0\n"
        "    assert artifact['digitization_ready'] is False\n"
        "    assert artifact['numeric_row_contract_status'] == 'OPEN_PANEL_AXIS_POINT_MAPPING'\n",
    ):
        changed.append(TEST_SCRIPT.as_posix())
    if replace_once(
        RUNNER,
        "    for relative in (\n        'audit_topic13_berut_source_package_availability.py',\n",
        "    for relative in (\n        'repair_topic13_berut_figure3_numeric_metadata.py',\n"
        "        'audit_topic13_berut_source_package_availability.py',\n",
    ):
        changed.append(RUNNER.as_posix())
    print({"status": "PASS_BERUT_FIGURE3_NUMERIC_METADATA_REPAIR", "changed": changed})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
