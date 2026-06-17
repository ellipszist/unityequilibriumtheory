# UPDATE LOG: 0.5 Nuclear Binding Hadrons

> **Scope:** `docs/topics/0.5_Nuclear_Binding_Hadrons`
> **Owner:** AI collaborator under UET standards
> **Purpose:** Track hardening waves for nuclear-binding, hadron, QCD, and confinement claim boundaries.

## Entries

### 2026-06-17 - PDG Hadron/Quark Source-Linkage Package

- Scope: `0.5_Nuclear_Binding_Hadrons` PDG hadron/quark source package and diagnostic linkage artifact
- Added or changed: added `Code/03_Research/Research_PDG_Hadron_Source_Linkage.py`, generated `Data/03_Research/pdg_hadron_quark_reference_package.json`, generated `Result/artifacts/pdg_hadron_quark_source_linkage.json`, and updated `pdg_hadron_qcd_source_mapping_gate.json` from source-exists to source-mapped diagnostic package status
- Files touched: `Code/03_Research/Research_PDG_Hadron_Source_Linkage.py`, `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json`, `Data/03_Research/pdg_hadron_quark_reference_package.json`, `Result/artifacts/pdg_hadron_quark_source_linkage.json`, `Result/artifacts/nuclear_binding_source_locked_validation.json`, `README.md`, `DATA_MANIFEST.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `FORMULA_AUDIT.md`, `BASELINE_COMPARISON.md`, `UPDATE_LOG.md`
- Verified with: bundled Codex Python run of `Research_PDG_Hadron_Source_Linkage.py`; bundled Codex Python rerun of `Research_Nuclear_Binding_SourceLocked.py`
- Result: PDG source-linkage diagnostic produced `16/16` records found with `0` unit mismatches; strict verifier remained `PASS` at `2026-06-17T01:21:22.180783+00:00`; PDG gate embedded with `controller_status=SOURCE_MAPPED_PACKAGE_READY_DIAGNOSTIC`
- Blocker narrowed: PDG quark/hadron source access is now a generated package and artifact instead of only a mapping note
- Still open: make hadron/quark model verification read the generated package, add QCD `alpha_s` source mapping, fix `alpha_s_uet_v2`, and keep confinement diagnostic until it returns real pass/fail status
- Next controller: `pdg_hadron_qcd_source_mapping_gate.json` and `pdg_hadron_quark_reference_package.json` control hadron/quark source-integration wording; `semf_coefficient_provenance_gate.json` still controls nuclear-binding parameter-free wording
- Claim impact: wording narrowed; no hadron/QCD validation upgrade and no stronger nuclear-binding claim
- Notes: the source-linkage package is diagnostic provenance, not a model-performance artifact

### 2026-06-17 - SEMF Coefficient Provenance Gate

- Scope: `0.5_Nuclear_Binding_Hadrons` coefficient provenance and claim-boundary docs
- Added or changed: added `Data/03_Research/semf_coefficient_provenance_gate.json` and `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json`, then wired the primary verifier to embed both gates in the strict artifact
- Files touched: `Data/03_Research/semf_coefficient_provenance_gate.json`, `Data/03_Research/pdg_hadron_qcd_source_mapping_gate.json`, `Code/03_Research/Research_Nuclear_Binding_SourceLocked.py`, `README.md`, `DATA_MANIFEST.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `FORMULA_AUDIT.md`, `BASELINE_COMPARISON.md`
- Verified with: `git diff --check -- docs/topics/0.5_Nuclear_Binding_Hadrons`; primary verifier rerun with bundled Codex Python; full-table diagnostic rerun with bundled Codex Python
- Result: `PASS` for diff hygiene; strict verifier `PASS` at `2026-06-17T01:14:27.709551+00:00`; full-table diagnostic `DIAGNOSTIC` at `2026-06-17T01:08:33.803330+00:00`; SEMF gate embedded with `controller_status=BLOCKED_FOR_PARAMETER_FREE_CLAIMS`; PDG mapping gate embedded with `controller_status=SOURCE_EXISTS_NOT_INTEGRATED`
- Blocker narrowed: SEMF coefficient provenance is now a machine-readable blocker instead of only prose; PDG 2025 quark and several hadron mass records are mapped but not integrated into topic scripts
- Still open: source-lock the exact SEMF coefficient set, decide the Yukawa-term policy, generate a topic-local PDG-derived hadron/quark package, and add QCD alpha_s source mapping
- Next controller: `semf_coefficient_provenance_gate.json` controls parameter-free and first-principles wording; `pdg_hadron_qcd_source_mapping_gate.json` controls hadron/QCD source-integration wording
- Claim impact: wording narrowed; no readiness upgrade and no stronger nuclear-binding claim
- Notes: local PDG 2025 SQLite sources exist for particle data; this wave maps several relevant records but intentionally leaves hadron/QCD branches diagnostic until scripts read a generated source package

### 2026-06-16 - SEMF Decomposition Surface

- Scope: `0.5_Nuclear_Binding_Hadrons` primary binding verifier and root standards docs
- Added or changed: added engine-level SEMF/component decomposition and verifier fields for SEMF-only, entropy-correction, Yukawa-correction, total prediction, and correction delta metrics
- Files touched: `Code/01_Engine/Engine_Nuclear_Binding.py`, `Code/03_Research/Research_Nuclear_Binding_SourceLocked.py`, `README.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `FORMULA_AUDIT.md`, `BASELINE_COMPARISON.md`
- Verified with: `$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'; & 'C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe' docs\topics\0.5_Nuclear_Binding_Hadrons\Code\03_Research\Research_Nuclear_Binding_SourceLocked.py`
- Result: `PASS`; strict artifact regenerated at `2026-06-17T01:11:10.996359+00:00`
- Blocker narrowed: the previous broad "split SEMF baseline and UET correction metrics" blocker is now narrowed to coefficient provenance and correction-term policy; artifact shows heavy SEMF-only mean error about `0.86%` versus total-path mean error about `1.68%`
- Still open: source-lock SEMF coefficients and decide whether the Yukawa term is baseline physics, a UET bridge term, or a separate diagnostic lane
- Next controller: `semf_coefficient_provenance_gate.json` controls parameter-free and first-principles wording
- Claim impact: wording narrowed; no readiness upgrade and no stronger nuclear-binding claim
- Notes: the decomposition is now artifact-current, and it narrows rather than strengthens the claim because the current correction terms worsen the heavy selected-subset mean error relative to SEMF-only
