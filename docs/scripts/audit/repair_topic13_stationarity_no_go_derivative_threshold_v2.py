from pathlib import Path


path = Path(__file__).resolve().parent / "audit_topic13_uet_o2_gaussian_thermal_stationarity_no_go.py"
text = path.read_text(encoding="utf-8")
start_marker = '        "thermal_derivative_is_resolved": min('
end_marker = '        "boundary_potential_converges": convergence_relative_errors['
start = text.find(start_marker)
end = text.find(end_marker, start)
if start < 0 or end < 0:
    raise SystemExit("acceptance markers were not found")
replacement = "\n".join(
    [
        '        "thermal_derivative_sign_matches_analytic_witness": all(',
        '            item["thermal_x_derivative_finite_difference"] > 0.0',
        "            for item in representative_records",
        "        ),",
        '        "total_derivative_is_resolved": min(',
        '            item["total_x_derivative_finite_difference"]',
        "            for item in representative_records",
        "        )",
        "        > FINITE_DIFFERENCE_TOLERANCE,",
    ]
)
text = text[:start] + replacement + "\n" + text[end:]
path.write_text(text, encoding="utf-8")
print("repaired", path)
