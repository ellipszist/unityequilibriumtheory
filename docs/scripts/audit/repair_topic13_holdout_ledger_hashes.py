from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
LEDGER = ROOT / "WORK_LEDGER/2026/2026-08-13.md"


def main() -> int:
    text = LEDGER.read_text(encoding="utf-8-sig")
    marker = "## Topic 13 holdout access-semantics correction wave"
    start = text.rfind(marker)
    if start < 0:
        raise RuntimeError("holdout ledger entry not found")
    prefix, block = text[:start], text[start:]
    replacements = {
        "full `093745ba4aabaad9b315a470ee0285fee86bae0c897dd3ac7e94764e01b6b147`": "full `736d13925ed90b580e9c2161ae5f9172960ee87a20bef929cab6fdb7d9df9cf5`",
        "register `f83d4cda8a87f78ef073bf680b7ee9ba2eb7430e60e10b32ec0cb9f32fcd5a11`": "register `d81505d505b6b39748c87a52f69d080a9f94d1259ffe3a3bc5607065cbc11952`",
        "dependency `88319f7a1c37eb631ae7db1f4c53a8c42a39890451c736be58c07c691a9e150e`": "dependency `a23e3d38f5178775243f5dd0e7be37ae79af65e88f259cc29af4d2d97661c609`",
    }
    for old, new in replacements.items():
        if block.count(old) != 1:
            raise RuntimeError(f"expected one ledger hash replacement: {old}")
        block = block.replace(old, new)
    LEDGER.write_text(prefix + block, encoding="utf-8")
    print("updated final Topic 13 holdout ledger hashes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
