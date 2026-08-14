from pathlib import Path


path = Path("docs/scripts/audit/audit_topic13_mp48_spectral_csrc_reproduction.py")
text = path.read_text(encoding="utf-8")
old = '"cross_file_residual_is_reported": np.isfinite(max_residual),\n'
new = '"cross_file_residual_is_reported": bool(np.isfinite(max_residual)),\n'
if text.count(old) != 1:
    raise SystemExit("expected one cross-file residual check")
text = text.replace(old, new)
old = '"quadrature_envelope_is_reported": np.isfinite(max_quadrature_difference),\n'
new = '"quadrature_envelope_is_reported": bool(np.isfinite(max_quadrature_difference)),\n'
if text.count(old) != 1:
    raise SystemExit("expected one quadrature envelope check")
text = text.replace(old, new)
path.write_text(text, encoding="utf-8")
print("repaired JSON-native boolean checks")
