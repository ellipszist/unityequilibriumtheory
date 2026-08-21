"""Run a source-locked Calorine/phono3py graphite PBTE candidate route.

This runner is intentionally a candidate-reproduction tool. It does not map
the result to base Phi, fit alpha_Phi_K, or consume any Topic 13 holdout.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
from typing import Iterable

import numpy as np
from ase import Atoms
from ase.io import read, write
from calorine.calculators import CPUNEP
from calorine.tools import relax_structure
from phono3py import Phono3py
from phono3py.file_IO import read_fc2_from_hdf5, read_fc3_from_hdf5
from phono3py.file_IO import write_fc2_to_hdf5, write_fc3_to_hdf5
from phonopy.interface.calculator import read_crystal_structure


EV_TO_J = 1.602176634e-19
ANGSTROM3_TO_M3 = 1.0e-30
ROOT = Path(__file__).resolve().parents[3]
UPSTREAM_NEP_LOCATOR = "https://github.com/brucefan1983/GPUMD/blob/master/potentials/nep/C_2024_NEP4.txt"
RELATED_ROTATION_DISORDER_RECORD = "https://zenodo.org/records/7811021"
DEFAULT_INPUT_DIR = ROOT / "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/raw/calorine_zenodo_21198312"


def parse_triplet(value: str) -> tuple[int, int, int]:
    parts = tuple(int(item.strip()) for item in value.split(","))
    if len(parts) != 3 or any(item <= 0 for item in parts):
        raise argparse.ArgumentTypeError("expected three positive integers, e.g. 4,4,2")
    return parts


def parse_temperatures(value: str) -> tuple[float, ...]:
    values = tuple(float(item.strip()) for item in value.split(","))
    if not values or any(item <= 0 for item in values):
        raise argparse.ArgumentTypeError("expected positive Kelvin values")
    return values


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_record(path: Path, locator: str | None = None) -> dict[str, object]:
    return {
        "path": path.relative_to(ROOT).as_posix() if path.is_relative_to(ROOT) else str(path),
        "size_bytes": path.stat().st_size,
        "sha256": sha256(path),
        "locator": locator,
    }


def parse_input_paths(input_dir: Path) -> tuple[Path, Path]:
    structure = input_dir / "graphite-prim.xyz"
    potential = input_dir / "nep-C.txt"
    if not structure.is_file() or not potential.is_file():
        raise FileNotFoundError(f"missing Calorine inputs under {input_dir}")
    return structure, potential


def make_phono3py(poscar: Path, dim: tuple[int, int, int]) -> Phono3py:
    unitcell, _ = read_crystal_structure(str(poscar), interface_mode="vasp")
    return Phono3py(unitcell, supercell_matrix=dim, primitive_matrix="P")


def calculate_force_constants(
    input_dir: Path,
    run_dir: Path,
    dim: tuple[int, int, int],
    relax: bool,
) -> dict[str, object]:
    structure_path, potential_path = parse_input_paths(input_dir)
    primitive = read(structure_path)
    if relax:
        primitive.calc = CPUNEP(str(potential_path))
        relax_structure(primitive, fmax=1.0e-5, steps=500)
    poscar = run_dir / "POSCAR"
    write(poscar, primitive, format="vasp")

    ph3 = make_phono3py(poscar, dim)
    ph3.generate_displacements()
    forces: list[np.ndarray] = []
    for index, supercell in enumerate(ph3.supercells_with_displacements):
        atoms = Atoms(
            symbols=supercell.symbols,
            positions=supercell.positions,
            cell=supercell.cell,
            pbc=True,
        )
        atoms.calc = CPUNEP(str(potential_path))
        forces.append(atoms.get_forces())
        if index % 100 == 0:
            print(f"force {index}/{len(ph3.supercells_with_displacements)}", flush=True)
    ph3.forces = np.asarray(forces, dtype=float)
    ph3.produce_fc2()
    write_fc2_to_hdf5(ph3.fc2, filename=run_dir / "fc2.hdf5")
    ph3.produce_fc3()
    write_fc3_to_hdf5(ph3.fc3, filename=run_dir / "fc3.hdf5")
    return {
        "poscar": source_record(poscar),
        "fc2": source_record(run_dir / "fc2.hdf5"),
        "fc3": source_record(run_dir / "fc3.hdf5"),
        "displacement_count": len(forces),
        "supercell_atoms": int(len(ph3.supercell)),
        "force_array_shape": list(ph3.forces.shape),
        "relaxed": relax,
    }


def run_transport(
    run_dir: Path,
    dim: tuple[int, int, int],
    mesh: tuple[int, int, int],
    temperatures: tuple[float, ...],
) -> Path:
    poscar = run_dir / "POSCAR"
    ph3 = make_phono3py(poscar, dim)
    ph3.fc2 = read_fc2_from_hdf5(run_dir / "fc2.hdf5")
    ph3.fc3 = read_fc3_from_hdf5(run_dir / "fc3.hdf5")
    ph3.mesh_numbers = list(mesh)
    current = Path.cwd()
    os.chdir(run_dir)
    try:
        ph3.init_phph_interaction()
        ph3.run_thermal_conductivity(
            temperatures=list(temperatures),
            is_LBTE=False,
            write_kappa=True,
        )
    finally:
        os.chdir(current)
    return run_dir / f"kappa-m{mesh[0]}{mesh[1]}{mesh[2]}.hdf5"


def summarize_csrc(
    run_dir: Path,
    kappa_path: Path,
    input_records: dict[str, object],
    dim: tuple[int, int, int],
    mesh: tuple[int, int, int],
    temperatures: tuple[float, ...],
) -> dict[str, object]:
    import h5py

    poscar = read(run_dir / "POSCAR", format="vasp")
    volume_a3 = float(poscar.get_volume())
    with h5py.File(kappa_path, "r") as handle:
        stored_temperatures = np.asarray(handle["temperature"][:], dtype=float)
        mode_cv_ev_per_k = np.asarray(handle["heat_capacity"][:], dtype=float)
        weights = np.asarray(handle["weight"][:], dtype=float)
        frequencies_thz = np.asarray(handle["frequency"][:], dtype=float)
        stored_mesh = tuple(int(item) for item in handle["mesh"][:])
        qpoints = np.asarray(handle["qpoint"][:], dtype=float)
        kappa = np.asarray(handle["kappa"][:], dtype=float)
    if stored_mesh != mesh:
        raise ValueError(f"HDF5 mesh {stored_mesh} differs from requested {mesh}")
    if not np.allclose(stored_temperatures, np.asarray(temperatures, dtype=float)):
        raise ValueError("HDF5 temperatures differ from requested values")
    if mode_cv_ev_per_k.ndim != 3:
        raise ValueError("expected heat_capacity shape (temperature, q-point, mode)")
    if weights.ndim != 1 or weights.shape[0] != mode_cv_ev_per_k.shape[1]:
        raise ValueError("q-point weight shape does not match mode heat capacity")
    weight_sum = float(weights.sum())
    weighted_mode_cv = np.einsum("g,tgb->t", weights, mode_cv_ev_per_k) / weight_sum
    c_src = weighted_mode_cv * EV_TO_J / (volume_a3 * ANGSTROM3_TO_M3)
    rows = [
        {
            "temperature_K": float(temp),
            "C_src_J_m^-3_K^-1": float(value),
        }
        for temp, value in zip(stored_temperatures, c_src, strict=True)
    ]
    return {
        "schema_version": "t13-calorine-pbte-csrc-run-v1",
        "run_id": run_dir.name,
        "source": input_records,
        "run": {
            "dim": list(dim),
            "mesh": list(mesh),
            "temperatures_K": list(temperatures),
            "transport_solver": "RTA",
            "isotope_scattering": False,
            "holdout_accessed": False,
            "target_curve_used": False,
            "fit_performed": False,
            "alpha_Phi_K_fit_performed": False,
        },
        "unit_contract": {
            "mode_heat_capacity_input": "eV K^-1 per mode per primitive cell",
            "energy_conversion": "1 eV = 1.602176634e-19 J (exact SI)",
            "primitive_volume_input": "A^3 from relaxed POSCAR",
            "volume_conversion": "1 A^3 = 1e-30 m^3",
            "aggregation": "C_src = sum_q w_q sum_mu c_qmu / (sum_q w_q V_primitive)",
            "output": "J m^-3 K^-1",
        },
        "geometry": {
            "primitive_atoms": int(len(poscar)),
            "primitive_formula": poscar.get_chemical_formula(),
            "primitive_volume_A3": volume_a3,
            "q_point_count": int(qpoints.shape[0]),
            "q_weight_sum": weight_sum,
            "mode_count": int(mode_cv_ev_per_k.shape[2]),
            "frequency_range_THz": [float(np.nanmin(frequencies_thz)), float(np.nanmax(frequencies_thz))],
        },
        "c_src_rows": rows,
        "transport_summary": {
            "kappa_shape": list(kappa.shape),
            "kappa_W_m^-1_K^-1": kappa.tolist(),
        },
        "claim_boundary": "Candidate harmonic/RTA PBTE reproduction only; not accepted Ding C_src, not a UET Phi map, not alpha_Phi_K calibration, and not external validation.",
    }


def write_json(path: Path, value: dict[str, object]) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=DEFAULT_INPUT_DIR)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--dim", type=parse_triplet, required=True)
    parser.add_argument("--mesh", type=parse_triplet, required=True)
    parser.add_argument("--temperatures", type=parse_temperatures, default=(200.0, 300.0))
    parser.add_argument("--reuse-force-constants", action="store_true")
    parser.add_argument("--no-relax", action="store_true")
    parser.add_argument(
        "--structure-locator",
        default="https://zenodo.org/api/records/21198312/files/graphite-prim.xyz/content",
    )
    parser.add_argument(
        "--potential-locator",
        default="https://zenodo.org/api/records/21198312/files/nep-C.txt/content",
    )
    parser.add_argument("--model-origin-locator", default=UPSTREAM_NEP_LOCATOR)
    parser.add_argument("--related-record-locator", default=RELATED_ROTATION_DISORDER_RECORD)
    args = parser.parse_args()

    input_dir = args.input_dir.resolve()
    run_dir = args.run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    structure_path, potential_path = parse_input_paths(input_dir)
    input_records = {
        "structure": source_record(
            structure_path,
            args.structure_locator,
        ),
        "potential": source_record(
            potential_path,
            args.potential_locator,
        ),
        "software": {
            "calorine": "3.5",
            "phono3py": "4.4.0",
            "phonopy": "4.4.0",
            "ase": "3.29.0",
        },
    }
    input_records["potential"]["upstream_model_origin"] = {
        "locator": args.model_origin_locator,
        "role": "model-origin locator supplied by the source contract; local bytes remain pinned by hash",
        "related_record": {"locator": args.related_record_locator, "role": "related source record, not necessarily the byte source"},
    }
    fc2 = run_dir / "fc2.hdf5"
    fc3 = run_dir / "fc3.hdf5"
    if not args.reuse_force_constants or not fc2.is_file() or not fc3.is_file():
        force_summary = calculate_force_constants(input_dir, run_dir, args.dim, not args.no_relax)
    else:
        force_summary = {
            "poscar": source_record(run_dir / "POSCAR"),
            "fc2": source_record(fc2),
            "fc3": source_record(fc3),
            "reused": True,
        }
    kappa_path = run_transport(run_dir, args.dim, args.mesh, args.temperatures)
    summary = summarize_csrc(run_dir, kappa_path, input_records, args.dim, args.mesh, args.temperatures)
    summary["force_constant_summary"] = force_summary
    summary["output_artifacts"] = {
        "kappa_hdf5": source_record(kappa_path),
    }
    write_json(run_dir / "csrc_summary.json", summary)
    print(json.dumps({"status": "PASS_CANDIDATE_PBTE_RUN", "run_dir": str(run_dir), "c_src_rows": summary["c_src_rows"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
