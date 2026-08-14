from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
path = ROOT / "docs/core/test/test_topic13_gatech_volumetric_cp_independence.py"
text = path.read_text(encoding="utf-8")
old = (
    '    assert (\n'
    '        "independent_same_grade_density_or_direct_volumetric_heat_capacity_missing"\n'
    '        in gate["major_result"]["what_remains_open"]\n'
    '    )\n'
)
new = (
    '    assert (\n'
    '        "independent_same_grade_density_or_direct_volumetric_heat_capacity_missing"\n'
    '        not in gate["major_result"]["what_remains_open"]\n'
    '    )\n'
    '    assert "density_uncertainty_not_source_locked" in gate["major_result"]["what_remains_open"]\n'
    '    assert "c_v_source_uncertainty_not_closed" in gate["major_result"]["what_remains_open"]\n'
    '    assert "direct_volumetric_c_v_or_same_state_Cp_source_missing" in gate["major_result"]["what_remains_open"]\n'
)
assert text.count(old) == 1
path.write_text(text.replace(old, new), encoding="utf-8")
print(path)
