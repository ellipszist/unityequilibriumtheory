from pathlib import Path


replacements = {
    Path("docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/bosak_2007_graphite_elastic_bulk_source_package.json"): (
        "5db624c3dbf48dcbed70d749da96ca61816fe6fed480f32d80a947ead649d7d",
        "5db6247c3dbf48dcbed70d749da96ca61816fe6fed480f32d80a947ead649d7d",
    ),
    Path("docs/scripts/audit/audit_topic13_graphite_elastic_bulk_modulus_source.py"): (
        "5db624c3dbf48dcbed70d749da96ca61816fe6fed480f32d80a947ead649d7d",
        "5db6247c3dbf48dcbed70d749da96ca61816fe6fed480f32d80a947ead649d7d",
    ),
}

for path, (old, new) in replacements.items():
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"expected one stale hash in {path}")
    path.write_text(text.replace(old, new), encoding="utf-8")
    print(f"repaired hash constant: {path}")
