from pathlib import Path


path = Path("docs/scripts/audit/audit_topic13_mp48_phi_e_dimensional_comparator.py")
text = path.read_text(encoding="utf-8")
text = text.replace(
    "def read_dos() -> tuple[np.ndarray, np.ndarray]:",
    "def read_dos() -> tuple[np.ndarray, np.ndarray, int]:",
)
text = text.replace(
    "    return values[positive, 0], values[positive, 1]\n",
    "    return values[positive, 0], values[positive, 1], len(values)\n",
)
text = text.replace(
    "    frequencies_thz, density_per_thz = read_dos()\n",
    "    frequencies_thz, density_per_thz, source_row_count = read_dos()\n",
)
text = text.replace(
    '"dos_row_count_is_201": len(frequencies_thz) == 184,',
    '"dos_row_count_is_201": source_row_count == 201,',
)
if "source_row_count" not in text:
    raise SystemExit("row-count repair did not apply")
path.write_text(text, encoding="utf-8")
print("repaired MP48 Phi_E comparator source-row count")
