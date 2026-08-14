from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
AUDIT = ROOT / "docs/scripts/audit/audit_topic13_mp48_force_constant_csrc_mesh_convergence.py"
TEST = ROOT / "docs/core/test/test_topic13_mp48_force_constant_csrc_mesh_convergence.py"

text = AUDIT.read_text(encoding="utf-8")
old = (
    "    fine_tail_converged = (\n"
    "        source_integrity_pass\n"
    "        and max_fine_tail_relative_step <= MESH_STEP_ACCEPTANCE_TOLERANCE\n"
    "    )\n"
    "    mesh_converged = (\n"
)
new = (
    "    fine_tail_converged = (\n"
    "        source_integrity_pass\n"
    "        and max_fine_tail_relative_step <= MESH_STEP_ACCEPTANCE_TOLERANCE\n"
    "    )\n"
    "    finest_pair_relative_steps = [\n"
    "        row for row in relative_steps\n"
    "        if (str(row[\"from_mesh\"]), str(row[\"to_mesh\"])) == (\"20x20x8\", \"25x25x10\")\n"
    "    ]\n"
    "    max_finest_pair_relative_step = max(\n"
    "        abs(float(row[\"relative_step\"])) for row in finest_pair_relative_steps\n"
    "    )\n"
    "    finest_pair_converged = (\n"
    "        source_integrity_pass\n"
    "        and max_finest_pair_relative_step <= MESH_STEP_ACCEPTANCE_TOLERANCE\n"
    "    )\n"
    "    mesh_converged = (\n"
)
assert text.count(old) == 1
text = text.replace(old, new)

old = (
    '            "fine_tail_converged": fine_tail_converged,\n'
    '            "continuum_convergence_required_for_Ding_acceptance": True,\n'
)
new = (
    '            "fine_tail_converged": fine_tail_converged,\n'
    '            "finest_pair_meshes": ["20x20x8", "25x25x10"],\n'
    '            "finest_pair_max_abs_relative_step": max_finest_pair_relative_step,\n'
    '            "finest_pair_converged": finest_pair_converged,\n'
    '            "continuum_convergence_required_for_Ding_acceptance": True,\n'
)
assert text.count(old) == 1
text = text.replace(old, new)

old = '        "max_abs_relative_fine_tail_mesh_step": max_fine_tail_relative_step,\n'
new = old + '        "max_abs_relative_finest_pair_mesh_step": max_finest_pair_relative_step,\n'
assert text.count(old) == 1
text = text.replace(old, new)
AUDIT.write_text(text, encoding="utf-8")

test_text = TEST.read_text(encoding="utf-8")
old = '    assert lane["mesh_policy"]["fine_tail_max_abs_relative_step"] < lane["mesh_policy"]["acceptance_tolerance_abs_relative_step"]\n'
new = (
    old
    + '    assert lane["mesh_policy"]["finest_pair_meshes"] == ["20x20x8", "25x25x10"]\n'
    + '    assert lane["mesh_policy"]["finest_pair_converged"] is True\n'
    + '    assert lane["mesh_policy"]["finest_pair_max_abs_relative_step"] < lane["mesh_policy"]["acceptance_tolerance_abs_relative_step"]\n'
)
assert test_text.count(old) == 1
TEST.write_text(test_text.replace(old, new), encoding="utf-8")
print(AUDIT)
print(TEST)
