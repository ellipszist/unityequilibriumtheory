"""Vectorized non-canonical MP48 mesh probe.

The dynamical matrix and Bose heat-capacity equations are identical to the
canonical audit; only q-point batching is changed to make deeper meshes
computable without changing any acceptance rule.
"""

from __future__ import annotations

import json

import numpy as np

from audit_topic13_mp48_force_constant_csrc_mesh_convergence import (
    AVOGADRO,
    BOLTZMANN,
    PLANCK,
    TARGET_TEMPERATURES_K,
    build_mapping,
    load_force_constants,
    load_phonopy,
)


def mode_heat_capacity(frequency_thz: np.ndarray, temperature_K: float) -> np.ndarray:
    x = PLANCK * np.abs(frequency_thz) * 1.0e12 / (BOLTZMANN * temperature_K)
    result = np.empty_like(x, dtype=float)
    small = np.abs(x) < 1.0e-7
    result[small] = BOLTZMANN
    regular = ~small
    exponent = np.exp(np.clip(x[regular], -700.0, 700.0))
    result[regular] = BOLTZMANN * x[regular] ** 2 * exponent / (exponent - 1.0) ** 2
    return result


def q_grid(shape: tuple[int, int, int]) -> np.ndarray:
    nx, ny, nz = shape
    return np.asarray(
        [(i / float(nx), j / float(ny), k / float(nz))
         for i in range(nx) for j in range(ny) for k in range(nz)],
        dtype=float,
    )


def batched_spectra(shape, force_constants, mapping, representatives, masses, conversion_factor):
    q_values = q_grid(shape)
    translations = np.asarray([translation for _, translation in mapping], dtype=float)
    row_translations = np.asarray([mapping[index][1] for index in representatives], dtype=float)
    primitive_indices = np.asarray([primitive for primitive, _ in mapping], dtype=int)
    row_primitive_indices = np.arange(4, dtype=int)
    coefficients = np.empty((4, len(mapping), 12, 12), dtype=complex)
    coefficients.fill(0.0)
    for primitive_i, row_index in enumerate(representatives):
        for column_index, primitive_j in enumerate(primitive_indices):
            coefficients[primitive_i, column_index,
                         3 * primitive_i:3 * primitive_i + 3,
                         3 * primitive_j:3 * primitive_j + 3] = (
                force_constants[row_index, column_index]
                / np.sqrt(masses[primitive_i] * masses[primitive_j])
            )

    all_frequencies = []
    negative_count = 0
    chunk_size = 1024
    for start in range(0, len(q_values), chunk_size):
        q_chunk = q_values[start:start + chunk_size]
        phase_argument = 2.0j * np.pi * np.einsum(
            "nd,rkd->nrk", q_chunk, translations[None, :, :] - row_translations[:, None, :]
        )
        phases = np.exp(phase_argument)
        matrices = np.einsum("nrm,rmij->nij", phases, coefficients)
        matrices = (matrices + np.swapaxes(matrices.conj(), 1, 2)) / 2.0
        eigenvalues = np.linalg.eigvalsh(matrices).real
        negative_count += int(np.sum(eigenvalues < -1.0e-12))
        all_frequencies.append(np.sign(eigenvalues) * np.sqrt(np.abs(eigenvalues)) * conversion_factor)
    return np.concatenate(all_frequencies, axis=0), negative_count


def main() -> None:
    phonopy = load_phonopy()
    force_constants, _, _, _ = load_force_constants()
    mapping, _ = build_mapping(phonopy)
    representative_indices = [
        index for index in range(len(mapping))
        if mapping[index][0] in range(4)
        and any(
            mapping[other][0] == mapping[index][0]
            and np.array_equal(mapping[other][1], np.zeros(3, dtype=int))
            for other in [index]
        )
    ]
    # Match the canonical representative selection exactly.
    representative_indices = []
    for primitive_index in range(4):
        central = [
            index for index, (mapped_index, translation) in enumerate(mapping)
            if mapped_index == primitive_index
            and np.array_equal(translation, np.zeros(3, dtype=int))
        ]
        representative_indices.append(central[0] if central else next(
            index for index, (mapped_index, _) in enumerate(mapping)
            if mapped_index == primitive_index
        ))
    masses = np.asarray([point["mass"] for point in phonopy["primitive_cell"]["points"]], dtype=float)
    conversion_factor = float(phonopy["phonopy"]["frequency_unit_conversion_factor"])
    outputs = []
    for shape in ((30, 30, 12), (35, 35, 14)):
        frequencies, negative_count = batched_spectra(
            shape, force_constants, mapping, representative_indices, masses, conversion_factor
        )
        rows = []
        for temperature in TARGET_TEMPERATURES_K:
            rows.append({
                "temperature_K": temperature,
                "heat_capacity_J_per_mol_cell_K": float(
                    np.sum(mode_heat_capacity(frequencies, temperature))
                    / float(len(frequencies))
                    * AVOGADRO
                ),
            })
        outputs.append({
            "mesh": "x".join(str(value) for value in shape),
            "q_point_count": int(np.prod(shape)),
            "rows": rows,
            "negative_eigenvalue_count": negative_count,
        })
    print(json.dumps(outputs, indent=2))


if __name__ == "__main__":
    main()
