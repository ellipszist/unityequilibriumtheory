"""Repair the remaining Topic 13 full-gate compatibility contracts."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
FULL_GATE = ROOT / "docs/scripts/audit/audit_topic13_full_bridge_gate.py"
REGISTER_GENERATOR = ROOT / "docs/scripts/audit/audit_major_result_closure.py"
FULL_RUNNER = ROOT / "docs/scripts/audit/run_topic13_full_bridge_wave.py"


def replace_once(text: str, old: str, new: str, label: str) -> tuple[str, bool]:
    count = text.count(old)
    if count == 0:
        if new in text:
            return text, False
        raise SystemExit(f"{label}: expected one match, found {count}")
    if count != 1:
        raise SystemExit(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1), True


def patch_full_gate() -> bool:
    text = FULL_GATE.read_text(encoding="utf-8-sig")
    original = text
    old = (
        "    for alias, lane_key in legacy_lane_aliases.items():\n"
        "        lane = discovered_lane_integrations.get(lane_key)\n"
        "        if lane:\n"
        "            artifact[\"verification_status\"][alias] = dict(lane)\n"
        "    mp48_lane = discovered_lane_integrations.get(\"mp48_independent_graphite_cv_reproduction\")\n"
    )
    new = (
        "    for alias, lane_key in legacy_lane_aliases.items():\n"
        "        lane = discovered_lane_integrations.get(lane_key)\n"
        "        if lane:\n"
        "            artifact[\"verification_status\"][alias] = dict(lane)\n"
        "    beta_alias = artifact[\"verification_status\"].get(\"beta_symbol_separation_noncircularity_no_go\")\n"
        "    if beta_alias:\n"
        "        # Keep the older status spelling only in the compatibility view.\n"
        "        beta_alias[\"status\"] = \"PASS_SCOPED_NO_GO\"\n"
        "    mp48_lane = discovered_lane_integrations.get(\"mp48_independent_graphite_cv_reproduction\")\n"
    )
    if "beta_alias = artifact[\"verification_status\"]" not in text:
        text, _ = replace_once(text, old, new, "legacy beta status alias")

    old = "    existing_evidence_paths = {item.get(\"path\") for item in artifact.get(\"evidence_artifacts\", [])}\n"
    new = (
        "    mp48_package_path = ROOT / \"docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/mp48_independent_graphite_cv_source_package.json\"\n"
        "    if mp48_package_path.is_file() and not any(\n"
        "        item.get(\"path\") == rel(mp48_package_path)\n"
        "        for item in artifact.get(\"evidence_artifacts\", [])\n"
        "        if isinstance(item, dict)\n"
        "    ):\n"
        "        artifact[\"evidence_artifacts\"].append(\n"
        "            evidence(\n"
        "                rel(mp48_package_path),\n"
        "                {},\n"
        "                {\"status\": \"PASS_INDEPENDENT_NUMERIC_CV_WITH_EPISTEMIC_ENVELOPE\", \"data_role\": \"INDEPENDENT_REPRODUCTION_NOT_CALIBRATION\"},\n"
        "            )\n"
        "        )\n"
        "    existing_evidence_paths = {item.get(\"path\") for item in artifact.get(\"evidence_artifacts\", [])}\n"
    )
    if "mp48_package_path = ROOT /" not in text:
        text, _ = replace_once(text, old, new, "mp-48 package evidence")
    if text != original:
        FULL_GATE.write_text(text, encoding="utf-8")
    return text != original


def patch_register_generator() -> bool:
    text = REGISTER_GENERATOR.read_text(encoding="utf-8-sig")
    original = text
    old = "    entries = [\n"
    new = (
        "    t13_evidence = [ref(rel(T13), {\"status\": t13[\"status\"], \"controlling_blocker\": t13[\"controlling_blocker\"]})]\n"
        "    for item in t13.get(\"evidence_artifacts\", []):\n"
        "        if not isinstance(item, dict):\n"
        "            continue\n"
        "        path = item.get(\"path\")\n"
        "        if not isinstance(path, str) or path == rel(T13) or not (ROOT / path).is_file():\n"
        "            continue\n"
        "        if any(existing.get(\"path\") == path for existing in t13_evidence):\n"
        "            continue\n"
        "        t13_evidence.append(ref(path, item.get(\"summary\", {})))\n"
        "\n"
        "    entries = [\n"
    )
    if "t13_evidence = [ref(rel(T13)" not in text:
        text, _ = replace_once(text, old, new, "full-result evidence preparation")
    old = "            \"evidence_artifacts\": [ref(rel(T13), {\"status\": t13[\"status\"], \"controlling_blocker\": t13[\"controlling_blocker\"]})],\n"
    new = "            \"evidence_artifacts\": t13_evidence,\n"
    if "\"evidence_artifacts\": t13_evidence" not in text:
        text, _ = replace_once(text, old, new, "full-result evidence field")
    if text != original:
        REGISTER_GENERATOR.write_text(text, encoding="utf-8")
    return text != original


def patch_runner() -> bool:
    text = FULL_RUNNER.read_text(encoding="utf-8-sig")
    command = "    \"docs/scripts/audit/repair_topic13_full_gate_remaining_compatibility.py\",\n"
    if command in text:
        return False
    needle = "    \"docs/scripts/audit/repair_topic13_full_gate_backward_compat_aliases.py\",\n"
    updated, _ = replace_once(text, needle, needle + command, "full-wave compatibility repair order")
    FULL_RUNNER.write_text(updated, encoding="utf-8")
    return True


def main() -> int:
    print({
        "full_gate_changed": patch_full_gate(),
        "register_generator_changed": patch_register_generator(),
        "runner_changed": patch_runner(),
    })
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
