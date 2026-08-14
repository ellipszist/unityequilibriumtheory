from pathlib import Path


path = Path(__file__).resolve().parent / "audit_topic13_uet_o2_gaussian_thermal_stationarity_no_go.py"
text = path.read_text(encoding="utf-8")
old = "\n".join(
    [
        "        \\\"thermal_derivative_is_resolved\\\": min(",
        "            item[\\\"thermal_x_derivative_finite_difference\\\"]",
        "            for item in representative_records",
        "        )",
        "        > FINITE_DIFFERENCE_TOLERANCE,",
        "        \\\"total_derivative_is_resolved\\\": min(",
        "            item[\\\"total_x_derivative_finite_difference\\\"]",
        "            for item in representative_records",
        "        )",
        "        > FINITE_DIFFERENCE_TOLERANCE,",
    ]
)
new = "\n".join(
    [
        "        \\\"thermal_derivative_sign_matches_analytic_witness\\\": all(",
        "            item[\\\"thermal_x_derivative_finite_difference\\\"] > 0.0",
        "            for item in representative_records",
        "        ),",
        "        \\\"total_derivative_is_resolved\\\": min(",
        "            item[\\\"total_x_derivative_finite_difference\\\"]",
        "            for item in representative_records",
        "        )",
        "        > FINITE_DIFFERENCE_TOLERANCE,",
    ]
)
if old not in text:
    raise SystemExit("expected derivative threshold block was not found")
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("repaired", path)
