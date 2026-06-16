"""
Audit core research hardening coverage for topics 0.0 through 0.26.

This script is intentionally stricter than the general topic standards audit. It does not
certify scientific truth. It creates a reviewer-facing map of the core topics that most need
hardening before public claims are upgraded.
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


DOCS_ROOT = Path(__file__).resolve().parents[2]
TOPICS_ROOT = DOCS_ROOT / "topics"
READINESS_FILE = DOCS_ROOT / "meta" / "topic_readiness.json"
REPORT_FILE = DOCS_ROOT / "meta" / "core_research_hardening_audit.md"
RUN_REPORT_DIR = DOCS_ROOT / "meta" / "core_research_hardening_runs"
NEXT_ACTIONS_FILE = DOCS_ROOT / "meta" / "core_research_next_actions.json"

CORE_REQUIRED = [
    "README.md",
    "METHOD.md",
    "DATA_MANIFEST.md",
    "VERIFICATION_SPEC.md",
    "BASELINE_COMPARISON.md",
    "LIMITATIONS.md",
]

OVERCLAIM_PATTERNS = [
    ("100% PASS", re.compile(r"\b100%\s+PASS\b")),
    ("Axiomatic Truth", re.compile(r"\bAxiomatic Truth\b", re.IGNORECASE)),
    ("definitive", re.compile(r"\bdefinitive(?:ly)?\b", re.IGNORECASE)),
    ("solved", re.compile(r"\bsolved\b", re.IGNORECASE)),
    ("All Systems PASS", re.compile(r"\bAll Systems PASS\b", re.IGNORECASE)),
    ("proof complete", re.compile(r"\bproof complete\b", re.IGNORECASE)),
    ("theorem-level", re.compile(r"\btheorem-level\b", re.IGNORECASE)),
]

DATA_RISK_ORDER = {
    "no data path": 4,
    "manual or placeholder": 3,
    "embedded local only": 3,
    "real source referenced": 2,
    "manifested real dataset": 0,
}


@dataclass
class TopicAudit:
    name: str
    status: str
    tier: str
    data_status: str
    missing_docs: list[str]
    formula_audit_status: str
    verification_command: str | None
    artifact_target: str | None
    artifact_status: str
    overclaim_hits: list[str]
    scores: dict[str, int]
    priority: int
    next_action: str


def topic_index(name: str) -> int | None:
    match = re.match(r"^0\.(\d+)_", name)
    if not match:
        return None
    return int(match.group(1))


def load_readiness() -> dict[str, dict]:
    data = json.loads(READINESS_FILE.read_text(encoding="utf-8"))
    return {entry["name"]: entry for entry in data["topics"]}


def extract_primary_command(spec_path: Path) -> str | None:
    return extract_spec_value(spec_path, "Primary command")


def extract_artifact_target(spec_path: Path) -> str | None:
    return extract_spec_value(spec_path, "Artifact target")


def extract_spec_value(spec_path: Path, marker: str) -> str | None:
    if not spec_path.exists():
        return None
    lines = spec_path.read_text(encoding="utf-8", errors="replace").splitlines()
    for index, line in enumerate(lines):
        if marker in line:
            for candidate in lines[index + 1 : index + 6]:
                match = re.search(r"`([^`]+)`", candidate)
                if match:
                    return match.group(1).strip()
    return None


def read_json_status(path: Path) -> str | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if isinstance(data, dict):
        results = data.get("results")
        if isinstance(results, dict) and isinstance(results.get("status"), str):
            return results["status"]
        if isinstance(data.get("status"), str):
            return data["status"]
        if isinstance(data.get("passed_run_contract"), bool):
            return "PASS" if data["passed_run_contract"] else "FAIL"
    return None


def artifact_status(topic_dir: Path) -> str:
    artifact_dir = topic_dir / "Result" / "artifacts"
    if not artifact_dir.exists():
        return "no artifact dir"
    statuses = []
    for path in sorted(artifact_dir.glob("*.json")):
        status = read_json_status(path)
        if status:
            statuses.append(f"{path.name}:{status}")
    if not statuses:
        return "no machine-readable status"
    if any(item.endswith(":FAIL") for item in statuses):
        return "FAIL present"
    if any(item.endswith(":PASS") for item in statuses):
        return "PASS present"
    return "; ".join(statuses[:3])


def overclaim_hits(readme_path: Path) -> list[str]:
    if not readme_path.exists():
        return []
    text = readme_path.read_text(encoding="utf-8", errors="replace")
    return [label for label, pattern in OVERCLAIM_PATTERNS if pattern.search(text)]


def formula_audit_status(topic_dir: Path) -> str:
    path = topic_dir / "FORMULA_AUDIT.md"
    if not path.exists():
        return "missing"
    text = path.read_text(encoding="utf-8", errors="replace")
    if "Bootstrap status" in text or "generated scaffold" in text:
        return "bootstrap/open"
    if "open_placeholder" in text or "`open`" in text:
        return "present/open"
    return "present"


def score_priority(entry: dict, missing_docs: list[str], formula_status: str, artifact: str, claims: list[str]) -> int:
    priority = 0
    priority += len(missing_docs) * 3
    if formula_status == "missing":
        priority += 8
    elif formula_status == "bootstrap/open":
        priority += 5
    elif formula_status == "present/open":
        priority += 3
    priority += DATA_RISK_ORDER.get(entry.get("data_reality_status"), 2) * 2
    priority += max(0, 2 - int(entry.get("verification_score") or 0)) * 3
    priority += max(0, 2 - int(entry.get("mathematical_rigor_score") or 0)) * 3
    priority += 6 if artifact == "FAIL present" else 0
    priority += min(len(claims), 4) * 2
    return priority


def next_action(audit: TopicAudit) -> str:
    if audit.missing_docs:
        return "Create or repair missing root standards docs before claim work."
    if audit.formula_audit_status == "missing":
        return "Add FORMULA_AUDIT.md and map formulas/constants/units to code."
    if audit.formula_audit_status == "bootstrap/open":
        return "Harden bootstrap formula audit entries into reviewed formula/constant/unit records."
    if audit.formula_audit_status == "present/open":
        return "Close open formula-audit entries or keep matching limitations explicit."
    if audit.artifact_status == "FAIL present":
        return "Treat verifier failure as blocker; document cause and fix model or threshold."
    if audit.data_status != "manifested real dataset":
        return "Upgrade DATA_MANIFEST.md with source, local path, unit convention, and benchmark role."
    if audit.overclaim_hits:
        return "Downgrade README wording to match verifier and formula-audit status."
    return "Run topic verifier and harden remaining limitations."


def current_blocker(audit: TopicAudit) -> str:
    if audit.missing_docs:
        return "Missing root standards docs: " + format_list(audit.missing_docs)
    if audit.formula_audit_status == "missing":
        return "Missing formula audit coverage."
    if audit.formula_audit_status == "bootstrap/open":
        return "Formula audit exists but still has bootstrap or scaffold entries."
    if audit.formula_audit_status == "present/open":
        return "Formula audit still has open entries that must stay visible in limitations."
    if audit.artifact_status == "FAIL present":
        return "Machine-readable verifier artifact records FAIL."
    if audit.data_status != "manifested real dataset":
        return f"Data provenance is not yet manifested real dataset: {audit.data_status}."
    if audit.overclaim_hits:
        return "README wording contains overclaim signals: " + format_list(audit.overclaim_hits)
    return "No top-level standards blocker; rerun verifier and harden remaining limitations."


def recommended_files(audit: TopicAudit) -> list[str]:
    topic_root = f"docs/topics/{audit.name}"
    if audit.missing_docs:
        return [f"{topic_root}/{name}" for name in audit.missing_docs]
    if audit.formula_audit_status in {"missing", "bootstrap/open", "present/open"}:
        return [
            f"{topic_root}/FORMULA_AUDIT.md",
            f"{topic_root}/LIMITATIONS.md",
            f"{topic_root}/README.md",
        ]
    if audit.artifact_status == "FAIL present":
        files = [
            f"{topic_root}/VERIFICATION_SPEC.md",
            f"{topic_root}/Result/artifacts/",
            f"{topic_root}/LIMITATIONS.md",
        ]
        if audit.verification_command:
            files.append("primary command target from VERIFICATION_SPEC.md")
        return files
    if audit.data_status != "manifested real dataset":
        return [
            f"{topic_root}/DATA_MANIFEST.md",
            f"{topic_root}/LIMITATIONS.md",
            f"{topic_root}/UPDATE_LOG.md",
        ]
    if audit.overclaim_hits:
        return [
            f"{topic_root}/README.md",
            f"{topic_root}/METHOD.md",
            f"{topic_root}/LIMITATIONS.md",
            f"{topic_root}/VERIFICATION_SPEC.md",
            f"{topic_root}/FORMULA_AUDIT.md",
        ]
    return [
        f"{topic_root}/VERIFICATION_SPEC.md",
        f"{topic_root}/LIMITATIONS.md",
        f"{topic_root}/UPDATE_LOG.md",
    ]


def stop_condition(audit: TopicAudit) -> str:
    if audit.missing_docs:
        return "Stop when the missing standards docs exist and the standards audit no longer reports this topic as structurally incomplete."
    if audit.formula_audit_status in {"missing", "bootstrap/open", "present/open"}:
        return "Stop when the formula audit blocker is narrower and any remaining open formula status is mirrored in LIMITATIONS.md."
    if audit.artifact_status == "FAIL present":
        return "Stop when the FAIL cause is named in the topic docs or the verifier/model path has been repaired and rerun."
    if audit.data_status != "manifested real dataset":
        return "Stop when DATA_MANIFEST.md records source identity, local path, unit convention, and benchmark role, or clearly keeps the data limitation explicit."
    if audit.overclaim_hits:
        return "Stop when README/METHOD wording no longer outruns VERIFICATION_SPEC.md, LIMITATIONS.md, and FORMULA_AUDIT.md."
    return "Stop after the declared verifier is rerun or the next limitations blocker is made explicit."


def expected_artifact(audit: TopicAudit) -> str | None:
    if audit.artifact_target:
        return f"docs/topics/{audit.name}/{audit.artifact_target}"
    return f"docs/topics/{audit.name}/Result/artifacts/"


def packet_for(audit: TopicAudit) -> dict[str, object]:
    return {
        "topic": audit.name,
        "priority": audit.priority,
        "current_blocker": current_blocker(audit),
        "next_action": audit.next_action,
        "data_status": audit.data_status,
        "artifact_status": audit.artifact_status,
        "verification_command": audit.verification_command,
        "expected_artifact": expected_artifact(audit),
        "recommended_files": recommended_files(audit),
        "stop_condition": stop_condition(audit),
    }


def build_next_actions(queue_audits: list[TopicAudit], summary_audits: list[TopicAudit], generated_at: str) -> dict[str, object]:
    return {
        "generated_at": generated_at,
        "scope": "0.0_Grand_Unification through 0.26_Cosmic_Dynamic_Frame",
        "summary": {
            "audited_core_topics": len(summary_audits),
            "queue_items": len(queue_audits),
            "missing_formula_audits": sum(1 for item in summary_audits if item.formula_audit_status == "missing"),
            "bootstrap_or_open_formula_audits": sum(1 for item in summary_audits if item.formula_audit_status == "bootstrap/open"),
            "missing_root_standards_docs": sum(1 for item in summary_audits if item.missing_docs),
            "machine_readable_fail_artifacts": sum(1 for item in summary_audits if item.artifact_status == "FAIL present"),
            "readme_overclaim_signals": sum(1 for item in summary_audits if item.overclaim_hits),
        },
        "queue": [packet_for(audit) for audit in queue_audits],
    }


def render_packets(next_actions: dict[str, object]) -> str:
    lines = [
        "# Core Research Wave Packets",
        "",
        f"Generated at: `{next_actions['generated_at']}`",
        f"Scope: `{next_actions['scope']}`",
        "",
    ]
    for item in next_actions["queue"]:
        packet = item
        lines.extend(
            [
                f"## {packet['topic']}",
                "",
                f"- Priority: {packet['priority']}",
                f"- Current blocker: {packet['current_blocker']}",
                f"- Next action: {packet['next_action']}",
                f"- Data status: {packet['data_status']}",
                f"- Artifact status: {packet['artifact_status']}",
                f"- Verification command: `{packet['verification_command']}`" if packet["verification_command"] else "- Verification command: n/a",
                f"- Expected artifact: `{packet['expected_artifact']}`" if packet["expected_artifact"] else "- Expected artifact: n/a",
                "- Recommended files: " + ", ".join(f"`{path}`" for path in packet["recommended_files"]),
                f"- Stop condition: {packet['stop_condition']}",
                "",
            ]
        )
    return "\n".join(lines)


def audit_topics() -> list[TopicAudit]:
    readiness = load_readiness()
    audits: list[TopicAudit] = []
    for topic_dir in sorted(TOPICS_ROOT.iterdir(), key=lambda path: (topic_index(path.name) is None, topic_index(path.name) or 999, path.name)):
        idx = topic_index(topic_dir.name)
        if idx is None or idx > 26:
            continue
        entry = readiness.get(topic_dir.name, {})
        missing_docs = [name for name in CORE_REQUIRED if not (topic_dir / name).exists()]
        formula_status = formula_audit_status(topic_dir)
        spec_path = topic_dir / "VERIFICATION_SPEC.md"
        command = extract_primary_command(spec_path)
        artifact_target = extract_artifact_target(spec_path)
        artifact = artifact_status(topic_dir)
        claims = overclaim_hits(topic_dir / "README.md")
        scores = {
            "data": int(entry.get("data_reality_score") or 0),
            "verification": int(entry.get("verification_score") or 0),
            "math": int(entry.get("mathematical_rigor_score") or 0),
            "physical": int(entry.get("physical_rigor_score") or 0),
            "claim": int(entry.get("claim_integrity_score") or 0),
        }
        audit = TopicAudit(
            name=topic_dir.name,
            status=str(entry.get("status", "missing metadata")),
            tier=str(entry.get("audit_tier", "missing")),
            data_status=str(entry.get("data_reality_status", "missing")),
            missing_docs=missing_docs,
            formula_audit_status=formula_status,
            verification_command=command,
            artifact_target=artifact_target,
            artifact_status=artifact,
            overclaim_hits=claims,
            scores=scores,
            priority=0,
            next_action="",
        )
        audit.priority = score_priority(entry, missing_docs, formula_status, artifact, claims)
        audit.next_action = next_action(audit)
        audits.append(audit)
    return sorted(audits, key=lambda item: (-item.priority, topic_index(item.name) or 999))


def format_list(values: list[str]) -> str:
    return ", ".join(values) if values else "-"


def render_report(audits: list[TopicAudit]) -> str:
    lines = [
        "# Core Research Hardening Audit",
        "",
        "Generated by `docs/scripts/audit/audit_core_research_hardening.py`.",
        "",
        "Scope: `0.0_Grand_Unification` through `0.26_Cosmic_Dynamic_Frame`.",
        "",
        "Purpose: identify which core topics need real standards hardening before any public",
        "claim language is upgraded. This report is an audit map, not a scientific proof.",
        "",
        "## Summary",
        "",
        f"- Audited core topics: {len(audits)}",
        f"- Topics missing `FORMULA_AUDIT.md`: {sum(1 for item in audits if item.formula_audit_status == 'missing')}",
        f"- Topics with bootstrap/open formula audits: {sum(1 for item in audits if item.formula_audit_status == 'bootstrap/open')}",
        f"- Topics with at least one missing root standards doc: {sum(1 for item in audits if item.missing_docs)}",
        f"- Topics with machine-readable FAIL artifacts: {sum(1 for item in audits if item.artifact_status == 'FAIL present')}",
        f"- Topics with README overclaim signals: {sum(1 for item in audits if item.overclaim_hits)}",
        "",
        "## Priority Table",
        "",
        "| Priority | Topic | Status | Tier | Data status | Formula audit | Artifact status | Missing docs | Overclaim signals | Next action |",
        "| --: | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- | :-- |",
    ]
    for item in audits:
        lines.append(
            "| {priority} | `{name}` | {status} | {tier} | {data_status} | {formula} | {artifact} | {missing} | {claims} | {next_action} |".format(
                priority=item.priority,
                name=item.name,
                status=item.status,
                tier=item.tier,
                data_status=item.data_status,
                formula=item.formula_audit_status,
                artifact=item.artifact_status,
                missing=format_list(item.missing_docs),
                claims=format_list(item.overclaim_hits),
                next_action=item.next_action,
            )
        )
    lines.extend(
        [
            "",
            "## Hardening Rules",
            "",
            "- A topic with missing root standards docs cannot be treated as `Structured` in practice.",
            "- A topic without reviewed `FORMULA_AUDIT.md` entries cannot support strong mathematical or physical claims.",
            "- A FAIL artifact is a model or verifier blocker, not a documentation nuisance.",
            "- `manifested real dataset` is the target data status for benchmark-backed core claims.",
            "- README language must not exceed `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, and `FORMULA_AUDIT.md`.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="write the token-saving next-actions JSON queue")
    parser.add_argument("--top", type=int, default=None, help="limit JSON/packet output to the top N queue items")
    parser.add_argument("--topic", action="append", default=[], help="limit JSON/packet output to one or more exact topic directory names")
    parser.add_argument("--emit-packets", action="store_true", help="print compact research wave packets to stdout")
    args = parser.parse_args()

    audits = audit_topics()
    report = render_report(audits)
    REPORT_FILE.write_text(report, encoding="utf-8")
    RUN_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    run_stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_report = RUN_REPORT_DIR / f"core_research_hardening_audit_{run_stamp}.md"
    run_report.write_text(report, encoding="utf-8")
    print(f"Wrote {REPORT_FILE}")
    print(f"Wrote {run_report}")
    print(f"Audited core topics: {len(audits)}")
    print(f"Missing formula audits: {sum(1 for item in audits if item.formula_audit_status == 'missing')}")
    print(f"Bootstrap/open formula audits: {sum(1 for item in audits if item.formula_audit_status == 'bootstrap/open')}")
    print(f"Missing root standards docs: {sum(1 for item in audits if item.missing_docs)}")
    print(f"FAIL artifacts: {sum(1 for item in audits if item.artifact_status == 'FAIL present')}")

    filtered_audits = audits
    if args.topic:
        requested = set(args.topic)
        filtered_audits = [item for item in filtered_audits if item.name in requested]
        missing = sorted(requested - {item.name for item in filtered_audits})
        if missing:
            print("Missing requested topics: " + ", ".join(missing))
            return 1
    if args.top is not None:
        if args.top < 1:
            print("--top must be at least 1")
            return 1
        filtered_audits = filtered_audits[: args.top]

    if args.json or args.emit_packets:
        generated_at = datetime.now(timezone.utc).isoformat()
        next_actions = build_next_actions(filtered_audits, audits, generated_at)
        NEXT_ACTIONS_FILE.write_text(json.dumps(next_actions, indent=2), encoding="utf-8")
        print(f"Wrote {NEXT_ACTIONS_FILE}")
        if args.emit_packets:
            print()
            print(render_packets(next_actions))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
