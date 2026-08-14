from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "docs/scripts/audit/audit_topic13_mp48_force_constant_csrc_mesh_convergence.py"
TEST = ROOT / "docs/core/test/test_topic13_mp48_force_constant_csrc_mesh_convergence.py"

text = AUDIT.read_text(encoding="utf-8")
old = "MESHES = ((5, 5, 2), (10, 10, 4), (15, 15, 6))"
new = "MESHES = ((5, 5, 2), (10, 10, 4), (15, 15, 6), (20, 20, 8), (25, 25, 10))"
assert text.count(old) == 1
text = text.replace(old, new)

old = "    source_integrity_pass = all(source_checks.values())\n    mesh_converged = (\n"
new = (
    "    source_integrity_pass = all(source_checks.values())\n"
    "    fine_tail_pairs = {(\"15x15x6\", \"20x20x8\"), (\"20x20x8\", \"25x25x10\")}\n"
    "    fine_tail_relative_steps = [\n"
    "        row for row in relative_steps\n"
    "        if (str(row[\"from_mesh\"]), str(row[\"to_mesh\"])) in fine_tail_pairs\n"
    "    ]\n"
    "    max_fine_tail_relative_step = max(\n"
    "        abs(float(row[\"relative_step\"])) for row in fine_tail_relative_steps\n"
    "    )\n"
    "    fine_tail_converged = (\n"
    "        source_integrity_pass\n"
    "        and max_fine_tail_relative_step <= MESH_STEP_ACCEPTANCE_TOLERANCE\n"
    "    )\n"
    "    mesh_converged = (\n"
)
assert text.count(old) == 1
text = text.replace(old, new)

old = '            "native_mesh": "5x5x2",\n            "continuum_convergence_required_for_Ding_acceptance": True,\n'
new = (
    '            "native_mesh": "5x5x2",\n'
    '            "fine_tail_meshes": ["15x15x6", "20x20x8", "25x25x10"],\n'
    '            "fine_tail_max_abs_relative_step": max_fine_tail_relative_step,\n'
    '            "fine_tail_converged": fine_tail_converged,\n'
    '            "continuum_convergence_required_for_Ding_acceptance": True,\n'
)
assert text.count(old) == 1
text = text.replace(old, new)

old = '        "max_abs_relative_mesh_step": max_relative_step,\n'
new = old + '        "max_abs_relative_fine_tail_mesh_step": max_fine_tail_relative_step,\n'
assert text.count(old) == 2
text = text.replace(old, new, 1)
AUDIT.write_text(text, encoding="utf-8")

test_text = TEST.read_text(encoding="utf-8")
old = '    assert lane["max_abs_relative_mesh_step"] > lane["mesh_policy"]["acceptance_tolerance_abs_relative_step"]\n'
new = (
    old
    + '    assert lane["mesh_policy"]["fine_tail_meshes"] == ["15x15x6", "20x20x8", "25x25x10"]\n'
    + '    assert lane["mesh_policy"]["fine_tail_converged"] is True\n'
    + '    assert lane["mesh_policy"]["fine_tail_max_abs_relative_step"] < lane["mesh_policy"]["acceptance_tolerance_abs_relative_step"]\n'
)
assert test_text.count(old) == 1
TEST.write_text(test_text.replace(old, new), encoding="utf-8")
print(AUDIT)
print(TEST)
