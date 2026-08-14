"""Upgrade the canonical MP48 mesh audit with the verified batch engine."""

from pathlib import Path


TARGET = Path(__file__).with_name("audit_topic13_mp48_force_constant_csrc_mesh_convergence.py")


BATCH_FUNCTION = r'''
def reconstruct_rows_batched(
    shape: tuple[int, int, int],
    force_constants: np.ndarray,
    mapping: list[tuple[int, np.ndarray]],
    representative_indices: list[int],
    masses: np.ndarray,
    conversion_factor: float,
) -> tuple[list[dict[str, float]], int, float]:
    """Evaluate the same dynamical matrices in q-point batches."""
    q_values = np.asarray(
        [
            (i / float(shape[0]), j / float(shape[1]), k / float(shape[2]))
            for i in range(shape[0])
            for j in range(shape[1])
            for k in range(shape[2])
        ],
        dtype=float,
    )
    translations = np.asarray([translation for _, translation in mapping], dtype=float)
    row_translations = np.asarray(
        [mapping[index][1] for index in representative_indices], dtype=float
    )
    primitive_indices = np.asarray([primitive for primitive, _ in mapping], dtype=int)
    coefficients = np.zeros((4, len(mapping), 12, 12), dtype=complex)
    for primitive_i, row_index in enumerate(representative_indices):
        for column_index, primitive_j in enumerate(primitive_indices):
            coefficients[
                primitive_i,
                column_index,
                3 * primitive_i : 3 * primitive_i + 3,
                3 * primitive_j : 3 * primitive_j + 3,
            ] = force_constants[row_index, column_index] / np.sqrt(
                masses[primitive_i] * masses[primitive_j]
            )

    frequencies_by_q: list[np.ndarray] = []
    negative_eigenvalue_count = 0
    minimum_eigenvalue = float("inf")
    for start in range(0, len(q_values), 1024):
        q_chunk = q_values[start : start + 1024]
        phase_argument = 2.0j * np.pi * np.einsum(
            "nd,rkd->nrk",
            q_chunk,
            translations[None, :, :] - row_translations[:, None, :],
        )
        phases = np.exp(phase_argument)
        matrices = np.einsum("nrm,rmij->nij", phases, coefficients)
        matrices = (matrices + np.swapaxes(matrices.conj(), 1, 2)) / 2.0
        eigenvalues = np.linalg.eigvalsh(matrices).real
        negative_eigenvalue_count += int(np.sum(eigenvalues < -NEGATIVE_EIGENVALUE_TOLERANCE))
        minimum_eigenvalue = min(minimum_eigenvalue, float(np.min(eigenvalues)))
        frequencies_by_q.append(
            np.sign(eigenvalues) * np.sqrt(np.abs(eigenvalues)) * conversion_factor
        )

    frequencies = np.concatenate(frequencies_by_q, axis=0)
    rows = []
    for temperature in TARGET_TEMPERATURES_K:
        rows.append(
            {
                "temperature_K": temperature,
                "heat_capacity_J_per_mol_cell_K": float(
                    np.sum(mode_heat_capacity(frequencies, temperature))
                    / float(len(frequencies))
                    * AVOGADRO
                ),
            }
        )
    return rows, negative_eigenvalue_count, minimum_eigenvalue
'''


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f"expected text was not found: {old[:80]}")
    return text.replace(old, new, 1)


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    text = replace_once(
        text,
        "MESHES = ((5, 5, 2), (10, 10, 4), (15, 15, 6), (20, 20, 8), (25, 25, 10))",
        "MESHES = ((5, 5, 2), (10, 10, 4), (15, 15, 6), (20, 20, 8), (25, 25, 10), (30, 30, 12), (35, 35, 14))",
    )
    marker = "\ndef main() -> int:\n"
    if "def reconstruct_rows_batched(" not in text:
        text = replace_once(text, marker, BATCH_FUNCTION + marker)
    text = replace_once(
        text,
        "rows, negative_count, minimum_eigenvalue = reconstruct_rows(\n",
        "rows, negative_count, minimum_eigenvalue = reconstruct_rows_batched(\n",
    )
    text = replace_once(
        text,
        'fine_tail_pairs = {(\"15x15x6\", \"20x20x8\"), (\"20x20x8\", \"25x25x10\")}',
        'fine_tail_pairs = {(\"20x20x8\", \"25x25x10\"), (\"25x25x10\", \"30x30x12\"), (\"30x30x12\", \"35x35x14\")}',
    )
    text = replace_once(
        text,
        'if (str(row["from_mesh"]), str(row["to_mesh"])) == ("20x20x8", "25x25x10")',
        'if (str(row["from_mesh"]), str(row["to_mesh"])) == ("30x30x12", "35x35x14")',
    )
    text = replace_once(
        text,
        '["15x15x6", "20x20x8", "25x25x10"]',
        '["20x20x8", "25x25x10", "30x30x12", "35x35x14"]',
    )
    text = replace_once(
        text,
        '["20x20x8", "25x25x10"]',
        '["30x30x12", "35x35x14"]',
    )
    TARGET.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    main()
