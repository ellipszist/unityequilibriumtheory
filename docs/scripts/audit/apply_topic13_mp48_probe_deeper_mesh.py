"""Update the non-canonical MP48 probe to test deeper refinement meshes."""

from pathlib import Path


TARGET = Path(__file__).with_name("probe_topic13_mp48_finer_mesh.py")


def main() -> None:
    text = TARGET.read_text(encoding="utf-8")
    old = "for shape in ((25, 25, 10),):"
    new = "for shape in ((30, 30, 12), (35, 35, 14)):\n"
    if old not in text:
        raise SystemExit("expected probe mesh declaration was not found")
    TARGET.write_text(text.replace(old, new.rstrip("\n")), encoding="utf-8")


if __name__ == "__main__":
    main()
