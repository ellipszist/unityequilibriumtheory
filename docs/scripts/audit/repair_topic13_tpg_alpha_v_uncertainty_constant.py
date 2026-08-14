from pathlib import Path


path = Path(
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/"
    "ihep_2001_32_tpg_anisotropic_alpha_v_source_package.json"
)
text = path.read_text(encoding="utf-8")
old = '"alpha_V_uncertainty_per_K": 4.565085979e-7'
new = '"alpha_V_uncertainty_per_K": 4.565084884205331e-7'
if text.count(old) != 1:
    raise SystemExit(f"expected one uncertainty constant, found {text.count(old)}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("repaired TPG alpha_V uncertainty constant")
