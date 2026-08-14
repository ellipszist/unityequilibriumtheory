from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
path = ROOT / "docs/core/test/test_topic13_mp48_force_constant_csrc_mesh_convergence.py"
text = path.read_text(encoding="utf-8")
old = '    assert lane["mesh_policy"]["fine_tail_max_abs_relative_step"] < lane["mesh_policy"]["acceptance_tolerance_abs_relative_step"]\n'
new = '    assert lane["mesh_policy"]["fine_tail_max_abs_relative_step"] > lane["mesh_policy"]["acceptance_tolerance_abs_relative_step"]\n'
assert text.count(old) == 1
path.write_text(text.replace(old, new), encoding="utf-8")
print(path)
