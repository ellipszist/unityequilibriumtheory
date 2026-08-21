"""Run the Topic 13 PBTE runner with a pinned legacy Calorine NEP backend.

The repository's current Calorine backend supports newer NEP formats. This
adapter keeps the existing force-constant/PBTE workflow and swaps only the
calculator implementation for a separately pinned Calorine 1.0 legacy
NEP2/NEP1-compatible extension. It does not perform calibration, fitting, or
holdout access.
"""

from __future__ import annotations

import argparse
import runpy
import sys
import types
from pathlib import Path


def build_legacy_calculator(legacy_path: Path):
    """Load the pinned extension and expose it through the current API shape."""

    sys.path.insert(0, str(legacy_path))
    from ase.calculators.calculator import Calculator, all_changes
    import numpy as np
    from calorine.nepy.nep import get_potential_forces_and_virials

    class LegacyNEP(Calculator):
        implemented_properties = ["energy", "forces"]

        def __init__(self, potential_filename: str, **kwargs: object) -> None:
            super().__init__(**kwargs)
            self.potential_filename = str(potential_filename)

        def calculate(
            self,
            atoms=None,
            properties=("energy",),
            system_changes=all_changes,
        ) -> None:
            super().calculate(atoms, properties, system_changes)
            energies, forces, _ = get_potential_forces_and_virials(
                atoms,
                self.potential_filename,
                debug=False,
            )
            self.results["energy"] = float(np.sum(energies))
            self.results["forces"] = np.asarray(forces, dtype=float)

    return LegacyNEP


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--legacy-calorine-path", type=Path, required=True)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--potential-path", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--dim", required=True)
    parser.add_argument("--mesh", required=True)
    parser.add_argument("--temperatures", default="200,300")
    parser.add_argument("--no-relax", action="store_true")
    parser.add_argument("--reuse-force-constants", action="store_true")
    parser.add_argument("--structure-locator", required=True)
    parser.add_argument("--potential-locator", required=True)
    parser.add_argument("--model-origin-locator", required=True)
    parser.add_argument("--related-record-locator", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    legacy_path = args.legacy_calorine_path.resolve()
    input_dir = args.input_dir.resolve()
    potential_path = args.potential_path.resolve()
    if not legacy_path.is_dir():
        raise FileNotFoundError(f"legacy Calorine path does not exist: {legacy_path}")
    if not (input_dir / "graphite-prim.xyz").is_file():
        raise FileNotFoundError(f"missing graphite-prim.xyz under {input_dir}")
    if not potential_path.is_file():
        raise FileNotFoundError(f"missing legacy potential: {potential_path}")

    legacy_nep = build_legacy_calculator(legacy_path)
    calculators = types.ModuleType("calorine.calculators")
    calculators.CPUNEP = legacy_nep
    tools = types.ModuleType("calorine.tools")
    tools.relax_structure = lambda *unused_args, **unused_kwargs: None
    sys.modules["calorine.calculators"] = calculators
    sys.modules["calorine.tools"] = tools

    runner_path = Path(__file__).with_name("run_topic13_calorine_pbte_reproduction.py")
    runner = runpy.run_path(str(runner_path), run_name="topic13_calorine_pbte_runner")

    def parse_input_paths(_input_dir: Path) -> tuple[Path, Path]:
        return input_dir / "graphite-prim.xyz", potential_path

    runner["parse_input_paths"] = parse_input_paths
    sys.argv = [
        str(runner_path),
        "--input-dir",
        str(input_dir),
        "--run-dir",
        str(args.run_dir.resolve()),
        "--dim",
        args.dim,
        "--mesh",
        args.mesh,
        "--temperatures",
        args.temperatures,
        "--structure-locator",
        args.structure_locator,
        "--potential-locator",
        args.potential_locator,
        "--model-origin-locator",
        args.model_origin_locator,
    ]
    if args.related_record_locator:
        sys.argv.extend(["--related-record-locator", args.related_record_locator])
    if args.no_relax:
        sys.argv.append("--no-relax")
    if args.reuse_force_constants:
        sys.argv.append("--reuse-force-constants")
    return int(runner["main"]())


if __name__ == "__main__":
    raise SystemExit(main())
