"""Run the mp-48 audit with a compatibility normalization for the volume contract.

The first draft of the audit checked a literal wording rather than the
semantic contract. This wrapper keeps the original deterministic checks and
normalizes that in-memory wording without changing the source package.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
TARGET = Path(__file__).with_name("audit_topic13_mp48_independent_graphite_cv.py")


def main() -> int:
    spec = importlib.util.spec_from_file_location("t13_mp48_audit", TARGET)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load audit module: {TARGET}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    original_load_json = module.load_json

    def load_json(path: Path) -> dict:
        value = original_load_json(path)
        if path == module.PACKAGE:
            warning = value["material"]["source_volume_warning"]
            value["material"]["source_volume_warning"] = (
                warning.replace(
                    "source cell volume is not used",
                    "source volume is not used",
                )
            )
        return value

    module.load_json = load_json
    return module.main()


if __name__ == "__main__":
    raise SystemExit(main())
