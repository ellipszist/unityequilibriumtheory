from pathlib import Path


old = "300a6b03af667f71a27fc7c269e7a928af57d4b846bded25feefa0e37b1089e"
new = "300a6b03af667f71a27fc7c269e7a928af57d4b846bded25feaefa0e37b1089e"
paths = [
    Path("docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/hanfland_1989_graphite_isothermal_kt_source_package.json"),
    Path("docs/scripts/audit/audit_topic13_graphite_isothermal_kt_source.py"),
]
for path in paths:
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"expected one stale hash in {path}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"repaired hash constant: {path}")
