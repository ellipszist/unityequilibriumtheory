"""Probe a finer MP48 q-mesh without changing the canonical gate artifact."""

from __future__ import annotations

import json
import time

import numpy as np

from audit_topic13_mp48_force_constant_csrc_mesh_convergence import (
    AVOGADRO,
    TARGET_TEMPERATURES_K,
    build_mapping,
    load_force_constants,
    load_phonopy,
    mode_heat_capacity,
    q_grid,
    representatives,
    spectrum_thz,
)


def run(shape: tuple[int, int, int], force_constants, mapping, representative_indices, masses, conversion_factor):
    start = time.perf_counter()
    frequencies_by_q = []
    negative_count = 0
    for q_fractional in q_grid(shape):
        frequencies, eigenvalues, _ = spectrum_thz(
            q_fractional,
            force_constants,
            mapping,
            representative_indices,
            masses,
            conversion_factor,
        )
        frequencies_by_q.append(frequencies)
        negative_count += int(np.sum(eigenvalues < -1.0e-12))
    rows = []
    for temperature in TARGET_TEMPERATURES_K:
        capacity = (
            sum(float(np.sum(mode_heat_capacity(freq, temperature))) for freq in frequencies_by_q)
            / float(len(frequencies_by_q))
            * AVOGADRO
        )
        rows.append({"temperature_K": temperature, "heat_capacity_J_per_mol_cell_K": capacity})
    return {
        "mesh": "x".join(str(value) for value in shape),
        "q_point_count": int(np.prod(shape)),
        "rows": rows,
        "negative_eigenvalue_count": negative_count,
        "elapsed_seconds": time.perf_counter() - start,
    }


def main() -> None:
    phonopy = load_phonopy()
    force_constants, _, _, _ = load_force_constants()
    mapping, _ = build_mapping(phonopy)
    representative_indices = representatives(mapping)
    masses = np.asarray([point["mass"] for point in phonopy["primitive_cell"]["points"]], dtype=float)
    conversion_factor = float(phonopy["phonopy"]["frequency_unit_conversion_factor"])
    outputs = []
    for shape in ((30, 30, 12), (35, 35, 14)):
        outputs.append(run(shape, force_constants, mapping, representative_indices, masses, conversion_factor))
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()
