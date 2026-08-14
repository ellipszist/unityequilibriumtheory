from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
PACKAGE = ROOT / (
    "docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/"
    "bipm_2006_01_graphite_specific_heat_source_package.json"
)


def main() -> int:
    text = PACKAGE.read_text(encoding="utf-8")
    old = "1889.357285"
    new = "1890.0596392706766"
    if old not in text:
        print("old value not present")
        return 0
    PACKAGE.write_text(text.replace(old, new), encoding="utf-8")
    print("repaired BIPM volumetric cp uncertainty")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
