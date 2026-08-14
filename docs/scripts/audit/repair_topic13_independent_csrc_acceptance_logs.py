from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

UPDATE_ENTRY = """

### 2026-08-13 - Independent C_src acceptance contract wave

MAJOR_RESULT_CLOSURE: `CLOSED_FOR_LANE` for `T13_INDEPENDENT_C_SRC_ACCEPTANCE_CONTRACT`.
WHAT_IS_ACTUALLY_CLOSED: The source gate now distinguishes raw-author Ding `C_src` from an accepted independent PBTE reproduction. The acceptance contract requires source identity/hash, raw numeric or reproduction payload, material/state mapping, mode-resolved `C_src` units, uncertainty, convergence, independence, and holdout/fit audit. Current MP48 evidence is evaluated and remains comparison-only.
WHAT_REMAINS_OPEN: Ding author numeric payload or a genuinely matched independent PBTE reproduction remains absent. MP48 fails the current material-regime, PBTE-response, and acceptance conditions.
DEPENDENCY_UNLOCKED: Source acceptance policy only; no Ding `C_src`, alpha calibration, bridge, transport, Core, Gravity, or Galaxy dependency unlock.
STATUS: `PASS_SCOPED_INDEPENDENT_C_SRC_ACCEPTANCE_CONTRACT`; the acceptance result is `BLOCKED` and Full Topic 13 remains `BLOCKED_OPEN_T13_FULL_BRIDGE`.
WHAT_CHANGED: Added acceptance artifact `447584738a9b5e676345b692570ac899c51b97e0950ddf2307c7a29efb0e8b68`, connected the full-gate generator `fc9fccf55bad968f2141734d5cd293ea91e3f3bc24f1381b185de9543a81abc3`, and synchronized register/dependency artifacts `371aba8fde74c469bc0be9e7cafedaf8a06977635b940da1507a050a2506689a` / `5ab8b4716eaabcfd06d89d8a826e24ea11947042759576f7ed40304b610b75ba`.
EQUATION_OR_MAPPING: `C_src(T)=sum_mu c_mu(T)` and `Delta_Tq=Delta_u_ph/C_src`; independent acceptance requires a declared PBTE response contract and does not relabel harmonic `c_v` as Ding `C_src`.
VERIFICATION: Full gate rerun reports `BLOCKED_OPEN_T13_FULL_BRIDGE` with the same 10 blockers; source route reports raw-author `false`, independent-reproduction `false`, and holdout/fit restrictions remain intact. Focused Topic 13 tests passed 20/22; two existing Core constraint persisted-artifact/hash drift tests remain failing outside this wave.
CONTROLLING_BLOCKER: `ding_pbte_C_src_numeric_or_accepted_independent_reproduction_missing`; `alpha_Phi_K` remains independently unresolved. :codex-annotation{index="1"}
NEXT_ACTION: Obtain an authorized Ding numeric package or a permitted same-regime PBTE reproduction that satisfies the new contract; do not change thresholds or promote MP48.
CLAIM_BOUNDARY: This closes the source-acceptance policy and candidate boundary only. It emits no `C_src`, no `alpha_Phi_K`, no holdout result, and no Full Topic 13 closure.
"""

LEDGER_ENTRY = """

## Topic 13 independent C_src acceptance-contract wave
- area: `research-core` (secondary: `result-artifacts`)
- workspace: `docs/topics/0.13_Thermodynamic_Bridge`
- files/artifacts: independent C_src acceptance contract; full-gate source-route integration; major-result register/dependency sync; Topic 13 update log
- verifier: `PASS_SCOPED_INDEPENDENT_C_SRC_ACCEPTANCE_CONTRACT`; full gate `BLOCKED_OPEN_T13_FULL_BRIDGE`; focused tests 20 passed and 2 pre-existing Core persisted-artifact/hash drift tests failed
- public-safety: `partial`
- result: raw-author Ding and accepted-independent-reproduction routes are now separate machine-readable gates; current candidates remain blocked without substitution
- hashes: acceptance `447584738a9b5e676345b692570ac899c51b97e0950ddf2307c7a29efb0e8b68`; full `ea02ea87e689e844ed8cf514843b1722a78ff8dc5cf638efce40b5cefac27c5e`; register `371aba8fde74c469bc0be9e7cafedaf8a06977635b940da1507a050a2506689a`; dependency `5ab8b4716eaabcfd06d89d8a826e24ea11947042759576f7ed40304b610b75ba`
- remains: authorized Ding numeric payload or matched PBTE reproduction, independent `alpha_Phi_K`, base-Phi SI anchor, bridge/beta, physical Kubo, finite-temperature transport, and EOS/SK/KMS/entropy completion
- next action: source acquisition under the new contract; keep MP48 harmonic evidence comparison-only and do not consume Xie holdout
- commit/push action: no commit requested; keep scoped changes identifiable in the dirty worktree
"""


def append_once(path: Path, entry: str, marker: str) -> None:
    text = path.read_text(encoding="utf-8-sig")
    if marker in text:
        return
    path.write_text(text.rstrip() + entry, encoding="utf-8")


if __name__ == "__main__":
    append_once(
        ROOT / "docs/topics/0.13_Thermodynamic_Bridge/UPDATE_LOG.md",
        UPDATE_ENTRY,
        "Independent C_src acceptance contract wave",
    )
    append_once(
        ROOT / "WORK_LEDGER/2026/2026-08-13.md",
        LEDGER_ENTRY,
        "Topic 13 independent C_src acceptance-contract wave",
    )
    print("updated Topic 13 log and work ledger")
