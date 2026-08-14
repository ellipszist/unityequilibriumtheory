"""Update the MP48 regression for the extended fine-tail audit."""

from pathlib import Path


TARGET = Path(__file__).parents[2] / "core/test/test_topic13_mp48_force_constant_csrc_mesh_convergence.py"


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f"expected test text was not found: {old}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    text = replace_once(
        text,
        'assert lane["mesh_policy"]["fine_tail_meshes"] == ["15x15x6", "20x20x8", "25x25x10"]',
        'assert lane["mesh_policy"]["fine_tail_meshes"] == ["20x20x8", "25x25x10", "30x30x12", "35x35x14"]',
    )
    text = replace_once(
        text,
        'assert lane["mesh_policy"]["fine_tail_converged"] is False',
        'assert lane["mesh_policy"]["fine_tail_converged"] is True',
    )
    text = replace_once(
        text,
        'assert lane["mesh_policy"]["fine_tail_max_abs_relative_step"] > lane["mesh_policy"]["acceptance_tolerance_abs_relative_step"]',
        'assert lane["mesh_policy"]["fine_tail_max_abs_relative_step"] < lane["mesh_policy"]["acceptance_tolerance_abs_relative_step"]',
    )
    text = replace_once(
        text,
        'assert lane["mesh_policy"]["finest_pair_meshes"] == ["20x20x8", "25x25x10"]',
        'assert lane["mesh_policy"]["finest_pair_meshes"] == ["30x30x12", "35x35x14"]',
    )
    TARGET.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
