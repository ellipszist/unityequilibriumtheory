from pathlib import Path


path = Path("docs/scripts/audit/audit_topic13_mp48_force_constant_harmonic_reconstruction.py")
text = path.read_text(encoding="utf-8")
old = '"summary_frequency_metadata_is_finite": np.isfinite(summary_max_frequency),'
new = '"summary_frequency_metadata_is_finite": bool(np.isfinite(summary_max_frequency)),'
if text.count(old) != 1:
    raise SystemExit(f"expected one serialization match, found {text.count(old)}")
path.write_text(text.replace(old, new), encoding="utf-8")
print("repaired NumPy boolean serialization in MP48 force-constant audit")
