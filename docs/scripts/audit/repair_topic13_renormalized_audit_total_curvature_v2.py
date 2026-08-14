from pathlib import Path


path = Path(__file__).resolve().parent / "audit_topic13_uet_o2_renormalized_normal_branch.py"
text = path.read_text(encoding="utf-8")

needle = "from docs.core.uet_covariant_response import CovariantResponseConfig"
if needle not in text:
    raise SystemExit("expected response import was not found")
text = text.replace(
    needle,
    "from docs.core.uet_covariant_response import CovariantResponseConfig, response_potential",
    1,
)
duplicate = "    dm_eff_sq_dphi = response.effective_mass_sq\n"
if duplicate not in text:
    raise SystemExit("expected duplicate derivative assignment was not found")
text = text.replace(duplicate, "", 1)

start = text.index("    total_response_curvature_fd = (")
end = text.index("    pressure_temperature_plus = state(", start)
replacement = "\n".join(
    [
        "    def response_sector_total_grand_potential(item, phi: float) -> float:",
        "        return item.total_grand_potential + float(",
        "            eos_config.response.epsilon_nc",
        "            * response_potential(phi, eos_config.response)",
        "        )",
        "",
        "    total_response_curvature_fd = (",
        "        response_sector_total_grand_potential(",
        "            response_plus, PHI_RESPONSE + derivative_step",
        "        )",
        "        - 2.0 * response_sector_total_grand_potential(response, PHI_RESPONSE)",
        "        + response_sector_total_grand_potential(",
        "            response_minus, PHI_RESPONSE - derivative_step",
        "        )",
        "    ) / derivative_step**2",
        "",
    ]
)
text = text[:start] + replacement + text[end:]
path.write_text(text, encoding="utf-8")
print("repaired", path)
