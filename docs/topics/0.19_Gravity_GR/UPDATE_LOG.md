# Update Log: 0.19 Gravity & General Relativity

## 2026-07-22 - Core GR Program Dependency Gate

**What changed:**
- Added `CORE_GR_PROGRAM_DEPENDENCY_SPEC.md`, a deterministic dependency verifier, generated dependency artifact, and twelve regression tests.
- Connected Topic 0.19 to the current core GR program without rewriting the topic's CODATA primary artifact or branch claim gate.
- Separated the exact implemented `epsilon_nc = 0` response-null from metric-PDE derivation, physical GR validation, and global universe closure.

**Which verifier was run:**
- `.\.venv\Scripts\python.exe docs/topics/0.19_Gravity_GR/Code/03_Research/Research_Core_GR_Program_Dependency_Gate.py`
- `.\.venv\Scripts\python.exe -m pytest docs/core/test/test_core_gr_topic_0_19_dependency.py -q`

**Which blocker narrowed:**
- The topic can now reference a machine-readable core candidate chain: exact response-null, local covariant balance, flat local 1+1 causal kernel, partial response reduction, and bounded Noether coordinate layer.
- These layers remain candidate mathematics and do not replace the topic's physical benchmarks.
- The dependency controller is narrowed to `topic_0_19_classical_gr_tests_and_covariant_completion_missing`.

**Next controlling blocker:**
- Add source-backed light-bending, perihelion, MICROSCOPE eta, and Eot-Wash artifacts, then close curved 3+1, equation-of-state, coarse-graining, transport/KMS, entropy-current, and dissipative-Bianchi requirements.
- Compare `epsilon_nc != 0` against the exact `epsilon_nc = 0` GR null on independent holdout evidence.

**Current topic-level status after wave:**
- Topic 0.19 remains `Draft / Tier B`; the CODATA checkpoint remains the independent primary artifact and its export controller remains `WARN`.
- Global universe closure remains `UNRESOLVED`; no GR-validation, global-open/closed, singularity, quantum-gravity, external-validation, or solved-theory claim is upgraded.
