from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]

UPDATE_ENTRY = """

### 2026-08-13 - Topic 13 formal open-system SK/KMS and entropy lane

MAJOR_RESULT_CLOSURE: CLOSED_FOR_LANE for T13_UET_O2_OPEN_SYSTEM_SK_KMS_ENTROPY_LANE.
WHAT_IS_ACTUALLY_CLOSED: A declared local doubled-field SK ansatz now has a retarded dissipative kernel, lower-half-plane poles, positive spectral density, greater/lesser KMS ratio, FDT noise identity, and a nonnegative formal entropy-production witness with an equilibrium zero limit.
WHAT_REMAINS_OPEN: The lane uses formal verifier parameters only. Microscopic interacting SK matching, physical Kubo provenance, finite-temperature transport, SI Phi anchor, independent alpha_Phi_K, and TTG material mapping remain open.
DEPENDENCY_UNLOCKED: Formal open-system SK/KMS, FDT, retardedness, and entropy-positivity lane only; no physical transport, full Topic 13, Core, Gravity, Galaxy, or external-validation unlock.
STATUS: PASS_FORMAL_OPEN_SYSTEM_SK_KMS_ENTROPY_LANE; Full Topic 13 remains BLOCKED_OPEN_T13_FULL_BRIDGE.
WHAT_CHANGED: Added module 92b2beb2d531d2c907953b42e4a381f1442dc035ab0cdebd7edf8a5ed0a9b063, focused audit ad703a6cc1fbcd0fa3ef7fdfd45a865808f02ab2d51f55d182d5ae26d4898487, artifact 4b8aa86cd3f7b7a88c2c1aff356a0af1a531501fcb97f3600167c149cb0eb422, full-gate projection eddd9895dccb764f2cbd8bad962821c1852f1fe955767816d3c9fa00c00d17eb, register cef102bf13032107b4438e4e2cb4fb5c08f28a9ba3471111bad8cc9070051432, and dependency record d4e94c4ef22a7591b502c58e95d9fb215175f760cff67d22b862546a56a12534.
EQUATION_OR_MAPPING: `S_SK = integral dt [Phi_a (K_R Phi_r) + i Phi_a N Phi_a / 2]`; `K_R(omega)=kappa-chi omega^2-i gamma omega`; `rho=-2 Im K_R`; `N=rho coth(beta_th omega/2)`; `sigma_formal=gamma (d_t Phi_r)^2/T`. No SI `Delta_Tq=alpha_Phi_K*Delta_Phi` calibration is emitted.
VERIFICATION: Audit passes with maximum relative KMS residual 1.7932013029545094e-16, maximum FDT residual 2.220446049250313e-16, retarded-pole and positivity checks pass, and focused tests pass (3 passed). No source rows, fitting, target data, or holdout data were used.
CONTROLLING_BLOCKER: `microscopic_interacting_SK_match_and_physical_Kubo_provenance_missing` controls this lane; full Topic 13 remains controlled by `dimensional_phi_energy_anchor_or_independent_alpha_calibration_missing` plus source, bridge/beta, EOS/transport, and uncertainty blockers. The independent `alpha_Phi_K` calibration remains open. :codex-annotation{index="1"}
NEXT_ACTION: Obtain a state-matched microscopic or source-locked retarded correlator with units, uncertainty, space-response definition, and provenance; do not promote formal gamma/noise to physical transport or alpha calibration.
CLAIM_BOUNDARY: Formal open-system KMS/FDT and entropy-positivity lane only. It is not a microscopic interacting match, physical Kubo coefficient, SI Phi calibration, TTG prediction, external validation, Core closure, or global UET closure.
"""

LEDGER_ENTRY = """

## Topic 13 formal open-system SK/KMS and entropy lane
- area: `research-core` (secondary: `result-artifacts`)
- workspace: `docs/topics/0.13_Thermodynamic_Bridge`
- files/artifacts: open-system SK/KMS module; focused test; audit artifact; full-gate projection; major-result register/dependency sync; Topic 13 update log
- verifier: `PASS_FORMAL_OPEN_SYSTEM_SK_KMS_ENTROPY_LANE`; focused tests 3 passed; full gate remains `BLOCKED_OPEN_T13_FULL_BRIDGE`
- public-safety: `partial`
- result: formal local retarded kernel, KMS/FDT identity, causal poles, and entropy-positivity witness closed for lane; no physical Kubo or SI promotion
- hashes: module `92b2beb2d531d2c907953b42e4a381f1442dc035ab0cdebd7edf8a5ed0a9b063`; audit `ad703a6cc1fbcd0fa3ef7fdfd45a865808f02ab2d51f55d182d5ae26d4898487`; artifact `4b8aa86cd3f7b7a88c2c1aff356a0af1a531501fcb97f3600167c149cb0eb422`; full `eddd9895dccb764f2cbd8bad962821c1852f1fe955767816d3c9fa00c00d17eb`; register `cef102bf13032107b4438e4e2cb4fb5c08f28a9ba3471111bad8cc9070051432`; dependency `d4e94c4ef22a7591b502c58e95d9fb215175f760cff67d22b862546a56a12534`
- remains: microscopic SK/KMS match, physical Kubo, independent `alpha_Phi_K`, base-Phi SI anchor, Ding `C_src`, source-grade uncertainty, and full EOS/transport/entropy closure
- next action: obtain a state-matched source-locked or microscopic retarded correlator; retain formal parameters as verifier-only
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
        "Topic 13 formal open-system SK/KMS and entropy lane",
    )
    append_once(
        ROOT / "WORK_LEDGER/2026/2026-08-13.md",
        LEDGER_ENTRY,
        "Topic 13 formal open-system SK/KMS and entropy lane",
    )
    print("updated Topic 13 log and work ledger")
