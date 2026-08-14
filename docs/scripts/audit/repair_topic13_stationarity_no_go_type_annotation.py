from pathlib import Path


path = Path(__file__).resolve().parents[2] / "core" / "uet_o2_gaussian_thermal_stationarity_no_go.py"
text = path.read_text(encoding="utf-8")
old = ") -> tuple[float, float, float, float]:\n    \"\"\"Return roots, their x-derivatives, and the discriminant margin."
new = ") -> tuple[float, float, float, float, float]:\n    \"\"\"Return roots, their x-derivatives, and the discriminant margin."
if old not in text:
    raise SystemExit("expected mode derivative annotation was not found")
path.write_text(text.replace(old, new, 1), encoding="utf-8")
print("repaired", path)
