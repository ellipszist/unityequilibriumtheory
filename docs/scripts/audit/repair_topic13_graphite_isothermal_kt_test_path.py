from pathlib import Path


path = Path("docs/core/test/test_topic13_graphite_isothermal_kt_gate_integration.py")
text = path.read_text(encoding="utf-8")
old = '    assert projected["K_T_GPa"] == 33.8\n    assert projected["K_T_uncertainty_GPa"] == 3.0\n'
new = '    assert projected["source_row"]["K_T_GPa"] == 33.8\n    assert projected["source_row"]["K_T_uncertainty_GPa"] == 3.0\n'
if text.count(old) != 1:
    raise SystemExit("expected one K_T assertion block")
path.write_text(text.replace(old, new), encoding="utf-8")
print("repaired projected K_T test path")
