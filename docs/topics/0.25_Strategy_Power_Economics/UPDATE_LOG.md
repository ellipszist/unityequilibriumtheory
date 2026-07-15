# UPDATE LOG: 0.25 Strategy Power Economics

> **Scope:** `docs/topics/0.25_Strategy_Power_Economics`
> **Purpose:** Record auditable hardening waves for the economic diagnostic lane.

## Entries

### 2026-07-16 - Optional-source semantics and legacy-claim quarantine

- Scope: source manifest semantics and whole-topic claim-boundary audit.
- Added or changed: optional missing exports now use `OPTIONAL_EXPORT_PENDING` rather than `MISSING_REQUIRED_EXPORT`; each source record now carries coverage and UTC retrieval timestamp; the panel enforces SHA-256 integrity; aggregate verifier now records `legacy_claim_quarantine`, panel/source-transform references, command failures, and a self-contained evidence bundle.
- Verified with: `Verify_UET_Economics_Hardening.py`; source readiness `PASS` (`15/15`), panel `PASS` (`66` rows), all commands exit zero, legacy quarantine `PASS` (`12/12` markdown files).
- Result: aggregate remains `WARN` only because `energy_density: WARN` is intentionally unresolved; Claim Class C and `DESCRIPTIVE_DIAGNOSTIC_ONLY` are unchanged.
- Next controller: source-lock the 1776-1945 energy mix and common heat-content basis; optional LBMA/S&P total-return exports remain separate.

### 2026-07-15 - Source closure, unit correction, and execution-gate hardening

- Scope: U.S. historical Book 1 economics diagnostic lane.
- Wave type: source pass, artifact pass, formula/unit pass, and claim-boundary pass.
- Added or changed: BEA/EIA/EPI transform manifest and normalized subsets; truthful BEA quantity-index labels; median rolling-origin acceptance rule with two resource baselines; aggregate command-failure and panel-status gates; synchronized topic standards docs and code README.
- Files touched: `Code/03_Research/`, `Data/03_Research/`, `Result/artifacts/`, `README.md`, `METHOD.md`, `DATA_MANIFEST.md`, `FORMULA_AUDIT.md`, `BASELINE_COMPARISON.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`.
- Verified with: `.\.venv\Scripts\python.exe -m py_compile` for all hardening scripts; `Research_UET_Economics_External_Source_Transform.py`; `Research_UET_Economics_Source_Package.py --vintage 2026-07-12`; `Verify_UET_Economics_Hardening.py`.
- Result: source readiness `PASS` (`15/15`); panel `PASS` (`66` rows, `1959-2024`); all executed subcommands exit zero; aggregate artifact `WARN`.
- Blocker narrowed: the prior broad missing-source blocker is closed for the primary panel. The remaining machine-readable controller is `energy_density: WARN`; the asset lane is separately `BLOCKED` pending LBMA and licensed S&P total-return inputs.
- Still open: EIA 1776-1945 source-mix export, source-locked common heat-content basis, optional exact asset exports, external replication, and legacy working-copy provenance.
- Next controller: `energy_density_definition_gate` / `energy_density: WARN`.
- Claim impact: wording upgraded only to `Structured / Tier A` package readiness; Claim Class C and `DESCRIPTIVE_DIAGNOSTIC_ONLY` remain unchanged. No economic-law, fiat-causality, policy, asset, or strategy claim was upgraded.
- Workflow linkage: this pilot follows the For_Work hardening sequence of source package, stable artifact, machine-readable blocker, documentation sync, update log, and scoped commit.
- Notes: the primary 3-year resource candidate signal is false; Stone mismatch does not beat the autoregression; EPI and BLS constructions are reported separately.

### 2026-07-12 - Book 1 historical economics source and gate package

- Scope: U.S. historical Book 1 economics diagnostic lane.
- Wave type: source pass and artifact/gate pass.
- Added or changed: source-lock manifest, readiness/parameter/holdout/formula/claim gates, seven research scripts, and aggregate verifier artifact.
- Files touched: `Code/03_Research/`, `Data/03_Research/`, `Result/artifacts/`, and topic standards docs.
- Verified with: `Research_UET_Economics_Source_Package.py --refresh --vintage 2026-07-12`; `Verify_UET_Economics_Hardening.py`.
- Result: `WARN`; 12 public FRED inputs were archived and hashed, while BEA fixed assets, EIA annual energy, and versioned EPI chart data remain missing.
- Blocker narrowed: broad Book 1 economics ambiguity is now a machine-readable three-source primary-panel gate; asset and literal-energy-density lanes have separate explicit gates.
- Still open: acquire and normalize the three required exports without substituting local convenience data.
- Next controller: `uet_us_historical_source_readiness` remains `WARN`.
- Claim impact: no change; Claim Class C and `DESCRIPTIVE_DIAGNOSTIC_ONLY` remain controlling.
- Workflow linkage: follows the Topic 0.25 source-packaging and formula-audit hardening workflow.
