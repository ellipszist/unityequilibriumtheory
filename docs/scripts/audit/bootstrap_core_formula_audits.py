"""
Bootstrap FORMULA_AUDIT.md files for core topics that do not have one.

The output is deliberately conservative. It inventories calculation surfaces from real code
files and marks proof status as open until a human/AI hardening pass reviews each formula,
constant, unit, and verifier role.
"""

from __future__ import annotations

import re
from pathlib import Path


DOCS_ROOT = Path(__file__).resolve().parents[2]
TOPICS_ROOT = DOCS_ROOT / "topics"
AUDIT_REPORT = DOCS_ROOT / "meta" / "core_research_hardening_audit.md"

CODE_PILLARS = ["01_Engine", "02_Proof", "03_Research", "04_Competitor"]


def topic_index(name: str) -> int | None:
    match = re.match(r"^0\.(\d+)_", name)
    if not match:
        return None
    return int(match.group(1))


def formula_prefix(topic_name: str) -> str:
    idx = topic_index(topic_name)
    if idx is None:
        return "TOPIC"
    return f"T{idx:02d}"


def discover_code_surfaces(topic_dir: Path) -> list[Path]:
    code_root = topic_dir / "Code"
    if not code_root.exists():
        return []
    paths: list[Path] = []
    for pillar in CODE_PILLARS:
        pillar_dir = code_root / pillar
        if pillar_dir.exists():
            paths.extend(sorted(pillar_dir.glob("*.py")))
    return paths


def detect_terms(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    terms = []
    patterns = {
        "trigonometry": r"\b(sin|cos|tan|exp|sqrt|log)\b",
        "mass/energy scale": r"\b(mass|energy|binding|GeV|MeV|eV|kg)\b",
        "field/density": r"\b(field|density|entropy|pressure|temperature|phase)\b",
        "benchmark constants": r"\b(PDG|CODATA|NuFIT|KATRIN|Planck|benchmark|experimental)\b",
        "matrix/vector": r"\b(matrix|vector|eigen|np\.array|linalg)\b",
    }
    for label, pattern in patterns.items():
        if re.search(pattern, text, flags=re.IGNORECASE):
            terms.append(label)
    return ", ".join(terms) if terms else "calculation path present; detailed term scan required"


def relation_label(path: Path) -> str:
    stem = path.stem
    if stem.startswith("Engine_"):
        return f"engine calculation path in `{path.name}`"
    if stem.startswith("Proof_"):
        return f"proof-oriented calculation path in `{path.name}`"
    if stem.startswith("Research_"):
        return f"research/benchmark comparison path in `{path.name}`"
    if stem.startswith("Competitor_"):
        return f"baseline/comparator path in `{path.name}`"
    return f"calculation path in `{path.name}`"


def render_formula_audit(topic_dir: Path, code_surfaces: list[Path]) -> str:
    topic_name = topic_dir.name
    prefix = formula_prefix(topic_name)
    lines = [
        f"# Formula Audit: {topic_name}",
        "",
        "Bootstrap status: generated scaffold from current code surfaces.",
        "",
        "This file is the first-pass formula registry for the topic. It does not claim that",
        "the listed relations are derived or correct. Each row identifies a calculation path",
        "that must be reviewed for variables, units, constants, proof status, verifier role,",
        "failure modes, and next hardening steps.",
        "",
        "## Formula Registry",
        "",
        "| formula_id | relation | code surface | variables and units | constant_origin | proof_status | verification_role | failure_mode | next_hardening_step |",
        "| :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |",
    ]
    if not code_surfaces:
        lines.append(
            f"| `{prefix}-OPEN-001` | no audited code formula surface found | `Code/` absent or empty | open | `open_placeholder` | `open` | none yet | Topic cannot support calculation claims until code or derivation is identified. | Add or locate the primary derivation/verifier path. |"
        )
    for index, path in enumerate(code_surfaces, start=1):
        rel = path.relative_to(topic_dir).as_posix()
        lines.append(
            "| `{fid}` | {relation} | `{rel}` | {terms}; unit audit required | `open_placeholder` | `open` | exploratory until linked to `VERIFICATION_SPEC.md` | Hidden unit mismatch, untracked benchmark anchor, or unsupported claim. | Review formulas/constants in this file and replace this scaffold row with explicit entries. |".format(
                fid=f"{prefix}-{index:03d}",
                relation=relation_label(path),
                rel=rel,
                terms=detect_terms(path),
            )
        )
    lines.extend(
        [
            "",
            "## Required Follow-Up",
            "",
            "- Replace each scaffold row with explicit formulas or pseudo-formulas.",
            "- Define every variable and dimensional unit used by the calculation.",
            "- Label constants as source-locked, benchmark anchors, topic-derived, heuristic bridges, or open placeholders.",
            "- Link each important formula to `METHOD.md`, `VERIFICATION_SPEC.md`, and the verifier artifact.",
            "- Keep README claims conservative until open rows are reviewed.",
            "",
            "## Audit Link",
            "",
            f"- Core audit report: `{AUDIT_REPORT.relative_to(DOCS_ROOT.parent).as_posix()}`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    created = []
    skipped = []
    for topic_dir in sorted(TOPICS_ROOT.iterdir(), key=lambda path: (topic_index(path.name) is None, topic_index(path.name) or 999, path.name)):
        idx = topic_index(topic_dir.name)
        if idx is None or idx > 26:
            continue
        target = topic_dir / "FORMULA_AUDIT.md"
        if target.exists():
            skipped.append(topic_dir.name)
            continue
        target.write_text(render_formula_audit(topic_dir, discover_code_surfaces(topic_dir)), encoding="utf-8")
        created.append(topic_dir.name)

    print(f"Created formula audits: {len(created)}")
    for name in created:
        print(f"- {name}")
    print(f"Skipped existing formula audits: {len(skipped)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
