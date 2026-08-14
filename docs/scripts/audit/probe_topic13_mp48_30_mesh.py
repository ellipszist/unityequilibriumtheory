"""Run one non-canonical 30x30x12 MP48 mesh probe."""

import json

import numpy as np

from audit_topic13_mp48_force_constant_csrc_mesh_convergence import (
    AVOGADRO,
    build_mapping,
    load_force_constants,
    load_phonopy,
    mode_heat_capacity,
    q_grid,
    representatives,
    spectrum_thz,
    TARGET_TEMPERATURES_K,
)


def main() -> None:
    phonopy = load_phonopy()
    force_constants, _, _, _ = load_force_constants()
    mapping, _ = build_mapping(phonopy)
    representative_indices = representatives(mapping)
    masses = np.asarray(
        [point["mass"] for point in phonopy["primitive_cell"]["points"]],
        dtype=float,
    )
    conversion_factor = float(phonopy["phonopy"]["frequency_unit_conversion_factor"])
    shape = (30, 30, 12)
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
    print(json.dumps({"mesh": "30x30x12", "q_point_count": int(np.prod(shape)), "rows": rows, "negative_eigenvalue_count": negative_count}, indent=2))


if __name__ == "__main__":
    main()
