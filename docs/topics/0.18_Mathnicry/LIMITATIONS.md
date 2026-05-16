# Limitations

- The root baseline comparison is present, but numeric acceptance boundaries are still provisional until a saved artifact is generated and reviewed.
- Current data posture is "manual or placeholder", which is below a fully normalized archival dataset package.
- Presence of proof scripts does not by itself establish theorem-level correctness, so proof scope must stay explicit.
- Internal script execution does not by itself establish external replication, theorem-level proof, or broad physical closure.
- The current BSD verifier uses a surrogate rank rule `(a+b)%2`, not actual elliptic-curve rank or L-function computation.
- `Data/source_evidence_intake_stub.json`, `Data/source_evidence_readiness_matrix.json`, and `Data/branch_claim_gate.json` are workflow controls only. They do not count as theorem evidence or proof closure.
- `Data/theorem_boundary_gate.json` is also a workflow/export control. It can block theorem-level inheritance, but it is not proof evidence by itself.
- Riemann scripts that evaluate `mpmath.zetazero(n)` check library-provided zeros; they do not search for or exclude off-critical-line zeros.
- Grover/P-vs-NP scaling scripts demonstrate quantum-search behavior and do not imply NP-complete problems are polynomial-time solvable.
- Collatz scripts are bounded/heuristic and include code hygiene issues such as unreachable logic after a `return` in `Engine_Collatz_Field.py`.
- Figure and report names containing `Proof` are not theorem-level evidence unless linked to a formal theorem statement and closed proof.

## Current Claim Boundary

| Claim area | Allowed wording now | Blocker to stronger wording |
| :-- | :-- | :-- |
| BSD branch | surrogate run-contract artifact | source-backed rank/L-function data and non-surrogate computation |
| Riemann branch | numerical/library zero sandbox | zero table, precision manifest, and off-line exclusion proof |
| Grover/P-vs-NP | quantum-search scaling sandbox | formal reduction and complexity proof boundary |
| Collatz | bounded/heuristic exploration | search manifest, range, counterexample policy, and proof argument |
| Quantum engine | sandbox diagnostics | deterministic fixtures for gates, states, norm, and entropy |
