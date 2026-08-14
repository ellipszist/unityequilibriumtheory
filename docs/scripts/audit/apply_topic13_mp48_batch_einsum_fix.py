"""Fix the q-point einsum signature in the non-canonical batch probe."""

from pathlib import Path


TARGET = Path(__file__).with_name("probe_topic13_mp48_mesh_batch.py")


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    old = '"nkd,rkd->nrk", q_chunk'
    new = '"nd,rkd->nrk", q_chunk'
    if old not in text:
        raise SystemExit("expected batch einsum signature was not found")
    TARGET.write_text(text.replace(old, new), encoding="utf-8")


if __name__ == "__main__":
    main()
