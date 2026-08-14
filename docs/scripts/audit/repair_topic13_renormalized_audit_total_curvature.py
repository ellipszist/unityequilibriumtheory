from pathlib import Path


path = Path(__file__).resolve().parent / "audit_topic13_uet_o2_renormalized_normal_branch.py"
text = path.read_text(encoding="utf-8")

old_import = "from docs.core.uet_covariant_response import CovariantResponseConfig\\n"
new_import = "from docs.core.uet_covariant_response import CovariantResponseConfig, response_potential\\n"
if old_import not in text:
    raise SystemExit("expected response import was not found")
text = text.replace(old_import, new_import, 1)

old_block = "\\n".join(
    [
        "    dm_eff_sq_dphi = response.effective_mass_sq",
        "    dm_eff_sq_dphi = (",
        "        response_plus.effective_mass_sq - response_minus.effective_mass_sq",
        "    ) / (2.0 * derivative_step)",
        "",
    ]
)
new_block = "\\n".join(
    [
        "    dm_eff_sq_dphi = (",
        "        response_plus.effective_mass_sq - response_minus.effective_mass_sq",
        "    ) / (2.0 * derivative_step)",
        "",
    ]
)
if old_block not in text:
    raise SystemExit("expected duplicate derivative block was not found")
text = text.replace(old_block, new_block, 1)

old_curvature = "\\n".join(
    [
        "    total_response_curvature_fd = (",
        "        response_plus.total_grand_potential",
        "        - 2.0 * response.total_grand_potential",
        "        + response_minus.total_grand_potential",
        "    ) / derivative_step**2",
        "",
    ]
)
new_curvature = "\\n".join(
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
if old_curvature not in text:
    raise SystemExit("expected total curvature block was not found")
text = text.replace(old_curvature, new_curvature, 1)

path.write_text(text, encoding="utf-8")
print("repaired", path)
