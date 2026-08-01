# UPDATE LOG: 0.13_Thermodynamic_Bridge

> **Scope:** `docs/topics/0.13_Thermodynamic_Bridge/`
> **Owner:** `AI-assisted hardening with human review required for any upward promotion`
> **Purpose:** Record multi-wave hardening progress for the thermodynamic bridge so later reviewers can reconstruct what changed, what was verified, and which blockers still control claim scope.

## When to use

Use this log when `0.13` changes in a way that narrows a provenance blocker, adds or tightens a verifier/gate, changes the claim boundary, or reorganizes the topic toward a stronger research package.

## Log rules

- Log real work, not intentions alone.
- Record verifier or audit commands only when actually run.
- Keep blocker names aligned with the verifier artifact and claim-gate language.
- Treat this file as coordination history, not as the canonical status source.
- One entry should correspond to one coherent hardening wave when possible.

## Entries

### 2026-07-20 - Spacetime thermodynamic trace contract

- Scope: separate simulation-only trace diagnostic lane.
- Wave type: artifact pass and claim-boundary pass.
- Added or changed: `docs/core/TRACE_RESEARCH_SPEC.md`, trace
  ontology/formula artifacts, and the opt-in `spacetime_trace_v1` benchmark.
- Files touched: trace benchmark script, Cattaneo artifact, README and this log.
- Verified with: 10 trace tests, 24 combined targeted regression tests, and
  `Code/03_Research/Research_Spacetime_Trace.py`.
- Result: normalized internal gates `PASS`; Cattaneo artifact remains
  `SIMULATION_ONLY` and topic status remains `WARN`.
- Blocker narrowed: trace history now has an explicit non-independent ontology.
- Still open: SI units/ledger closure and source-backed external benchmark.
- Next controller: an observable mapping with dimensional units; the existing
  Landauer source-normalization blocker remains the topic-level controller.
- Claim impact: no upgrade; the trace lane cannot support a UET bridge proof.
- Workflow linkage: core trace checkpoint before the matter-space pilot.


### 2026-06-22 - Berut Figure 3 digitization-protocol pass

- Scope: narrow the active Berut row beyond raster-asset inventory by selecting a first calibration candidate and defining the required landmark fields before any numeric transcription
- Wave type: `gate pass`
- Added or changed: added `BERUT_2012_FIGURE3_DIGITIZATION_PROTOCOL.md` and `berut_2012_figure3_digitization_protocol.json`; updated the raster inventory, source route, Berut source record, row-closure matrix, verifier intake/gate wording, root docs, and manifest so the active Berut controller is now `berut_figure_3_axis_landmark_coordinates_required`
- Files touched: `BERUT_2012_FIGURE3_DIGITIZATION_PROTOCOL.md`, `Data/03_Research/berut_2012_figure3_digitization_protocol.json`, `Data/03_Research/berut_2012_figure3_raster_asset_inventory.json`, `Data/03_Research/berut_2012_figure3_ppt_source_route.json`, `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`, `Data/03_Research/row_closure_matrix.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: local artifact inspection of the raster inventory plus verifier rerun
- Result: `WARN`
- Blocker narrowed: Berut is no longer blocked by deciding how to structure the first digitization attempt; the package now selects `jpeg_3` for first calibration, keeps `jpeg_2` as fallback, and requires plot-frame, axis tick, reference-line, and point/curve landmarks
- Still open: machine-readable landmark coordinates, point/curve pixel coordinates, numeric transcription, and explicit mapping into the topic-summary runtime row
- Next controller: `berut_figure_3_axis_landmark_coordinates_required`
- Claim impact: no upgrade; this wave creates a controlled digitization protocol but does not create a numeric Berut source row
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by turning an open digitization procedure into a named machine-readable protocol before any numeric row claims


### 2026-06-22 - Berut Figure 3 embedded-raster inventory pass

- Scope: narrow the active Berut row beyond official PPT route capture by enumerating the valid embedded raster assets and naming primary digitization candidates
- Wave type: `source pass`
- Added or changed: added `BERUT_2012_FIGURE3_RASTER_ASSET_INVENTORY.md` and `berut_2012_figure3_raster_asset_inventory.json`; updated the Berut source route, Berut source record, row-closure matrix, verifier intake/gate wording, root docs, and manifest so the active Berut controller is now `berut_figure_3_axis_calibration_and_point_selection_required`
- Files touched: `BERUT_2012_FIGURE3_RASTER_ASSET_INVENTORY.md`, `Data/03_Research/berut_2012_figure3_raster_asset_inventory.json`, `Data/03_Research/berut_2012_figure3_ppt_source_route.json`, `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`, `Data/03_Research/row_closure_matrix.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: re-download of the official Nature/Springer Figure 3 PPT route, byte-signature scan for valid JPEG/PNG streams, and PIL validation of embedded image dimensions; then rerun the primary verifier
- Result: `WARN`
- Blocker narrowed: Berut is no longer blocked by identifying which embedded raster assets exist inside the official Figure 3 PPT; the package now names `jpeg_2` and `jpeg_3` as primary digitization candidates with hashes and dimensions
- Still open: axis calibration, point/curve selection, numeric transcription, and explicit mapping into the topic-summary runtime row
- Next controller: `berut_figure_3_axis_calibration_and_point_selection_required`
- Claim impact: no upgrade; this wave strengthens source acquisition and digitization readiness but does not create a numeric Berut source row
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by converting one raster-asset identity ambiguity into a named machine-readable inventory before numeric transcription claims


### 2026-06-22 - Jun arXiv Table I local-transcription pass

- Scope: narrow the active Jun row from `final parity or local archive` to final PRL parity/APS access by locally transcribing the arXiv Table I/Figure 4 source-summary surface for the `0.71 +/- 0.03 kT` full-erasure asymptotic-work row
- Wave type: `source pass`
- Added or changed: added `JUN_2014_SOURCE_SUMMARY_TRANSCRIPTION.md` and `jun_2014_source_summary_transcription.json`; updated the Jun source record, Jun source-summary locator, row-closure matrix, verifier intake/gate wording, root docs, and manifest so the active Jun controller is now `jun_final_prl_parity_or_aps_access_resolution_required`
- Files touched: `JUN_2014_SOURCE_SUMMARY_TRANSCRIPTION.md`, `Data/03_Research/jun_2014_source_summary_transcription.json`, `docs/data/external/thermodynamics/landauer/jun_2014/source_record.json`, `Data/03_Research/jun_2014_source_summary_locator.json`, `Data/03_Research/row_closure_matrix.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: arXiv PDF `https://arxiv.org/pdf/1408.5089`, targeted page-4 text extraction showing `TABLE I`, `FIG. 4`, `full erasure (p = 1) 0.71 1.39 8.2`, and the `Work ... divided by kT` caption; APS abstract/PDF/DOI routes returned `403 Forbidden` in this environment; then rerun the primary verifier
- Result: `WARN`
- Blocker narrowed: Jun is no longer blocked by local source-summary transcription; the active summary surface now has a machine-readable local transcription
- Still open: final PRL parity or APS access resolution, plus continued exclusion of the legacy `0.028 eV` row from active Jun logic unless future final-source evidence reassigns it
- Next controller: `jun_final_prl_parity_or_aps_access_resolution_required`
- Claim impact: no upgrade; this wave strengthens Jun source handling but does not make the row final-source-normalized
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by converting one source-summary archive ambiguity into a named machine-readable transcription before broader source-normalization claims


### 2026-06-22 - Berut Figure 3 PPT source-route pass

- Scope: narrow the active Berut row beyond preview-level locator capture by identifying and download-testing the official publisher PowerPoint route for `Figure 3`
- Wave type: `source pass`
- Added or changed: added `BERUT_2012_FIGURE3_PPT_SOURCE_ROUTE.md` and `berut_2012_figure3_ppt_source_route.json`; updated the Berut source record, row-closure matrix, verifier intake wording, README, ROW_CLOSURE_MATRIX, and manifest so the active Berut controller is now `berut_figure_3_ppt_raster_digitization_or_source_data_required`
- Files touched: `BERUT_2012_FIGURE3_PPT_SOURCE_ROUTE.md`, `Data/03_Research/berut_2012_figure3_ppt_source_route.json`, `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`, `Data/03_Research/row_closure_matrix.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: Nature article page `https://www.nature.com/articles/nature10872`, which exposes `PowerPoint slide for Fig. 3 (download PPT)`, and download test of `https://static-content.springer.com/esm/art%3A10.1038%2Fnature10872/MediaObjects/41586_2012_BFnature10872_MOESM77_ESM.ppt`; then rerun the primary verifier
- Result: `WARN`
- Blocker narrowed: Berut is no longer blocked by finding the official Figure 3 file route; the package now records the file name, URL, byte size, SHA-256, embedded raster observation, and no-numeric-table boundary
- Still open: calibrated raster digitization or a stronger source-data surface, plus explicit mapping from any captured point/curve to the topic-summary runtime row
- Next controller: `berut_figure_3_ppt_raster_digitization_or_source_data_required`
- Claim impact: no upgrade; this wave strengthens source acquisition but does not create a numeric Berut source row
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by converting one source-route ambiguity into a named machine-readable route and leaving the numeric row blocker explicit


### 2026-06-22 - Jun Table 1 source-summary locator pass

- Scope: narrow the active Jun row from a generic source-summary file/table identity blocker to a captured Table 1/Figure 4 fit-target locator for the `0.71 +/- 0.03 kT` asymptotic-work summary
- Wave type: `source pass`
- Added or changed: added `JUN_2014_SOURCE_SUMMARY_LOCATOR.md` and `jun_2014_source_summary_locator.json`; updated the Jun source record, Jun uncertainty/runtime conflict artifacts, row-closure matrix, verifier intake, foundation gate, uncertainty summaries, root docs, and manifest so the active Jun controller is now `jun_final_source_parity_or_local_archive_before_row_level_normalization`
- Files touched: `JUN_2014_SOURCE_SUMMARY_LOCATOR.md`, `Data/03_Research/jun_2014_source_summary_locator.json`, `docs/data/external/thermodynamics/landauer/jun_2014/source_record.json`, `Data/03_Research/jun_2014_uncertainty_gap.json`, `Data/03_Research/jun_2014_runtime_mapping_conflict.json`, `Data/03_Research/row_closure_matrix.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: primary-facing arXiv surface `https://arxiv.org/abs/1408.5089`, where Figure 4/Table 1/Eq. (3) identify the full-erasure `p=1` asymptotic work as `0.71 +/- 0.03 kT`; then `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: Jun is no longer blocked by finding the active summary file/table/fit target; the package now names the arXiv source surface, Figure 4, Table 1, Eq. (3), and the full-erasure `p=1` fit target
- Still open: final PRL page/PDF parity or local article/table archival, row-level normalization, and any reassignment of the legacy `0.028 eV` row remain open
- Next controller: `jun_final_source_parity_or_local_archive_before_row_level_normalization`
- Claim impact: no upgrade; this wave strengthens the Jun source-summary package but does not make the row final-source-normalized or restore the legacy `0.028 eV` row
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by turning one source-summary identity ambiguity into a named machine-readable locator before broader source-normalization claims

### 2026-06-21 - CODATA 2022 G direct-extraction pass

- Scope: replace the measured-constant `G` uncertainty proxy inherited from the local `0.19` CODATA 2018 checkpoint with a direct CODATA 2022/NIST extract inside the active `0.13` gravity-context interval package
- Wave type: `source pass`
- Added or changed: added `docs/data/external/constants/codata/codata_2022_measured_constants_extract.json`; updated the measured-constants source record, row-closure matrix, primary verifier, source-evidence intake/readiness, measured-constant package, uncertainty summary, foundation gate, verification artifact, and topic docs so the gravity-context rows now use `direct_2022_g_threaded` instead of `provisional_g_proxy_threaded`
- Files touched: `docs/data/external/constants/codata/codata_2022_measured_constants_extract.json`, `docs/data/external/constants/codata/measured_constants_2022_source_record.json`, `Data/03_Research/measured_constant_uncertainty_package.json`, `Data/03_Research/uncertainty_propagation_summary.json`, `Data/03_Research/row_closure_matrix.json`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Code/03_Research/Research_Landauer.py`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `MEASURED_CONSTANT_UNCERTAINTY_PACKAGE.md`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `DERIVATION_MAP.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: NIST/CODATA 2022 complete ASCII listing at `https://physics.nist.gov/cuu/Constants/Table/allascii.txt`, row `Newtonian constant of gravitation 6.674 30 e-11 0.000 15 e-11 m^3 kg^-1 s^-2`; then `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the measured-constant support layer is no longer blocked by direct 2022 `G` numeric extraction; that value and uncertainty now live in a local source extract and are threaded into the gravity-context combined intervals
- Still open: systematic astrophysical terms, object-level black-hole source-row capture, broader CODATA table archival, and the core Landauer row controllers remain open
- Next controller: `systematic_term_policy_after_direct_2022_g_extraction`
- Claim impact: no upgrade; this wave improves uncertainty provenance for gravity-context rows without changing the UET bridge proof ceiling
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by converting one support-layer source blocker into a direct local extract before broadening the uncertainty package

### 2026-06-21 - Jun legacy-row policy threading pass

- Scope: thread the existing legacy `0.028 eV` row policy into the active Jun row controller so the topic no longer treats Jun as blocked by an undecided legacy-row branch choice
- Wave type: `gate pass`
- Added or changed: updated `jun_2014_uncertainty_gap.json`, `jun_2014_runtime_mapping_conflict.json`, `row_closure_matrix.json`, and the primary verifier wording so the inherited legacy `0.028 eV` row is demoted to legacy context outside active Jun logic; regenerated the verifier artifact, foundation gate, source-intake/readiness, uncertainty, derivation, units, beta, and Landauer-UET control artifacts; synced README, METHOD, LIMITATIONS, VERIFICATION_SPEC, ROW_CLOSURE_MATRIX, DERIVATION_MAP, and DATA_MANIFEST wording to the narrower Jun controller
- Files touched: `Data/03_Research/jun_2014_uncertainty_gap.json`, `Data/03_Research/jun_2014_runtime_mapping_conflict.json`, `Data/03_Research/row_closure_matrix.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `ROW_CLOSURE_MATRIX.md`, `DERIVATION_MAP.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: Jun is no longer blocked by deciding whether the legacy `0.028 eV` row belongs in active Jun logic; that row is now declared legacy context outside the active Jun benchmark lane
- Still open: original source-summary file/table identity, exact source row or fit-target locator, explicit source-unit basis, and archived source surface for the pinned Jun asymptotic-work summary remain open
- Next controller: `jun_source_summary_file_identity_and_table_locator_required`
- Claim impact: no upgrade; this wave only narrows Jun from legacy-row branch ambiguity to source-summary identity and locator closure
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by moving one controlling blocker into artifact/gate state and recording the resulting controller in the topic update log

### 2026-06-21 - Berut figure-locator mapping pass

- Scope: narrow the primary Berut provenance blocker beyond selected policy choice by attaching one exact preview-level locator to the current topic-summary row
- Wave type: `gate pass`
- Added or changed: added `BERUT_2012_FIGURE_LOCATOR_MAPPING.md` and `berut_2012_figure_locator_mapping.json`; updated the Berut source record, provenance gap, transcription-policy blocker, row-closure matrix, Landauer row contract, verifier intake/gate wording, and root docs so the package now names `Figure 3: Erasure rate and approach to the Landauer limit.` as the current authoritative preview-level locator for the Berut summary row
- Files touched: `BERUT_2012_FIGURE_LOCATOR_MAPPING.md`, `Data/03_Research/berut_2012_figure_locator_mapping.json`, `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`, `BERUT_2012_PROVENANCE_GAP.md`, `Data/03_Research/berut_2012_provenance_gap.json`, `BERUT_2012_TRANSCRIPTION_POLICY_BLOCKER.md`, `Data/03_Research/berut_2012_transcription_policy_blocker.json`, `ROW_CLOSURE_MATRIX.md`, `Data/03_Research/row_closure_matrix.json`, `Data/03_Research/landauer_row_contract.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: preview-surface inspection of `https://www.nature.com/articles/nature10872` showing `Figure 3: Erasure rate and approach to the Landauer limit.`; then rerun the primary verifier
- Result: `WARN`
- Blocker narrowed: Berut is no longer blocked by figure-locator choice itself; the package now fixes `Figure 3` as the current preview-level locator and makes the next Berut controller numeric-point capture or one stronger upstream numeric surface
- Still open: one numeric point/curve within `Figure 3`, one machine-transcribed value or stronger numeric surface, and one explicit rule mapping that figure-level support into the current runtime value and uncertainty remain open
- Next controller: `figure_3_locator_captured_numeric_point_or_stronger_surface_still_required`
- Claim impact: no upgrade; this wave only narrows the Berut provenance path from locator choice to numeric-capture closure
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by closing one locator-choice ambiguity in a machine-readable way before any stronger provenance wording

### 2026-06-21 - Berut transcription-policy decision pass

- Scope: narrow the primary Berut provenance blocker beyond an open policy choice by selecting one conservative normalization path for the visible figure-level preview surface
- Wave type: `gate pass`
- Added or changed: added `BERUT_2012_TRANSCRIPTION_POLICY_DECISION.md` and `berut_2012_transcription_policy_decision.json`; updated the Berut transcription-policy blocker, row-closure matrix, verifier intake wording, and root docs so the repo now selects `figure_level_locator_capture` as the preferred path and pushes the next Berut controller to one exact figure/panel locator plus runtime mapping
- Files touched: `BERUT_2012_TRANSCRIPTION_POLICY_DECISION.md`, `Data/03_Research/berut_2012_transcription_policy_decision.json`, `BERUT_2012_TRANSCRIPTION_POLICY_BLOCKER.md`, `Data/03_Research/berut_2012_transcription_policy_blocker.json`, `ROW_CLOSURE_MATRIX.md`, `Data/03_Research/row_closure_matrix.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: Berut is no longer blocked by a fully open transcription-policy choice; the package now explicitly selects `figure_level_locator_capture`, so the remaining controller is one exact figure/panel locator and explicit runtime mapping under that policy
- Still open: exact figure/panel locator capture, explicit figure-to-runtime mapping, and broader row-level source normalization remain open
- Next controller: `figure_level_locator_capture_then_runtime_mapping`
- Claim impact: no upgrade; this wave only selects one conservative provenance path and makes the next Berut evidence requirement narrower
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by converting an open policy choice into one named machine-readable decision before any stronger provenance language

### 2026-06-21 - Peterson branch-identity policy pass

- Scope: narrow the Peterson branch one step beyond `composite source conflict` by separating the incompatible candidate families behind the legacy local `Peterson 2018` label
- Wave type: `source pass`
- Added or changed: added `PETERSON_BRANCH_IDENTITY_POLICY.md` and `peterson_branch_identity_policy.json`; updated the Peterson conflict note, the staged Peterson source record, the local runtime placeholder wording, the row-closure matrix, and the verifier/source-intake wording so the branch now explicitly separates the Peterson-led `2016` Proc. R. Soc. A paper, the trapped-ion PRL `2018` quantum-Landauer paper, and the Nature Physics `2018` mesoscopic-entropy DOI instead of treating `Peterson 2018` as one fuzzy paper label
- Files touched: `PETERSON_BRANCH_IDENTITY_POLICY.md`, `Data/03_Research/peterson_branch_identity_policy.json`, `PETERSON_2018_SOURCE_CONFLICT.md`, `Data/03_Research/peterson_2018_source_conflict.json`, `docs/data/external/thermodynamics/landauer/peterson_2018/source_record.json`, `Data/03_Research/experimental_data.py`, `Data/03_Research/row_closure_matrix.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: primary-source inspection of `https://doi.org/10.1098/rspa.2015.0813` together with previously checked DOI metadata for `10.1103/PhysRevLett.120.210601` and `10.1038/s41567-018-0250-5`; then `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: Peterson is no longer blocked only by a generic one-paper conflict; the package now explicitly separates the Peterson-led `2016` authorship cue from the trapped-ion `2018` PRL cue and from the Nature Physics `2018` DOI, so the unsupported local `Peterson 2018` label is demoted to legacy-placeholder status
- Still open: one exact upstream paper identity is still required before any Peterson-side row capture, unit normalization, uncertainty propagation, or benchmark use
- Next controller: `exact_one_paper_identity_before_any_row_capture`
- Claim impact: no upgrade; this wave only removes a misleading local paper label and tightens the provenance boundary around the quantum-Landauer branch
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by narrowing one controlling blocker into a more explicit machine-readable policy before any attempt at numeric repair or broader promotion

### 2026-06-19 - Hong provisional-target policy pass

- Scope: narrow the Hong branch one step beyond `multiple candidate values visible` by declaring which currently visible Hong-side quantity best matches the inherited `2016 / 44% above limit / ~0.026 eV` runtime narrative
- Added or changed: added `HONG_2016_RUNTIME_TARGET_POLICY.md` and `hong_2016_runtime_target_policy.json` so the topic now machine-readably provisionally prefers the preprint temperature-series mean `4.2 +/- 0.9 zJ (~0.0262 eV)` over the room-temperature five-trial average `6.09 +/- 1.43 zJ (~0.0380 eV)` for the inherited legacy runtime narrative; updated `row_closure_matrix.json`, `landauer_row_contract.json`, `LANDAUER_ROW_CONTRACT.md`, and the verifier-generated Hong intake wording so the next controller is no longer generic target selection but final-source confirmation plus a keep/replace/remove policy for the local `0.028 eV` row; then reran the verifier and synced root docs/manifests
- Files touched: `HONG_2016_RUNTIME_TARGET_POLICY.md`, `Data/03_Research/hong_2016_runtime_target_policy.json`, `Data/03_Research/row_closure_matrix.json`, `Data/03_Research/landauer_row_contract.json`, `LANDAUER_ROW_CONTRACT.md`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `README.md`, `LIMITATIONS.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: Hong no longer stops at `which statistic is the intended target?`; the package now provisionally prefers the `4.2 +/- 0.9 zJ` target for the inherited legacy narrative and pushes the next controller to final-source confirmation plus the local `0.028 eV` row policy
- Still open: the repo still lacks a final archived publisher article page, a final-source confirmation for the provisionally preferred target, and a declared keep/replace/remove decision for the local `0.028 eV` row
- Next controller: `final_source_confirmation_for_provisionally_selected_temperature_series_target`
- Claim impact: no upgrade; this wave only turns Hong target selection into an explicit conservative topic policy
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by turning one open choice into a named machine-readable controller before broadening scope

### 2026-06-19 - Hong preprint numeric-target narrowing pass

- Scope: move the Hong branch beyond `candidate source family with Crossref only` by attaching one accessible same-author primary-facing precursor surface and threading its numeric consequences through the row-governance package
- Added or changed: updated the staged `Hong 2016` source record so it now records the accessible arXiv precursor `1411.6730` plus two source-facing dissipation summaries (`6.09 +/- 1.43 zJ` and `4.2 +/- 0.9 zJ`); added a corresponding `HONG_2016_CANDIDATE` block to `experimental_data.py`; updated the Hong acquisition, lineage, and numeric-mismatch notes/JSON so the blocker is now `which Hong statistic is the intended runtime target?` rather than only `missing primary source`; updated the row-closure matrix so Hong now exposes `numeric_target_resolution_then_final_source_confirmation`; then reran the verifier and synced the README, limitations, verification spec, row-closure prose, and manifest wording
- Files touched: `docs/data/external/thermodynamics/landauer/hong_2016/source_record.json`, `Data/03_Research/experimental_data.py`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/row_closure_matrix.json`, `HONG_2016_SOURCE_ACQUISITION_BLOCKER.md`, `Data/03_Research/hong_2016_source_acquisition_blocker.json`, `HONG_2016_SOURCE_LINEAGE_NOTE.md`, `Data/03_Research/hong_2016_source_lineage_note.json`, `HONG_2016_NUMERIC_MISMATCH_NOTE.md`, `Data/03_Research/hong_2016_numeric_mismatch_note.json`, `ROW_CLOSURE_MATRIX.md`, `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: primary-facing inspection of `https://arxiv.org/abs/1411.6730` / `https://arxiv.org/pdf/1411.6730`; then `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: Hong is no longer blocked mainly by `no primary-facing numeric surface`; the package now records that one accessible same-author preprint exposes at least two Hong-side dissipation candidates, one near `~0.026 eV` and another near `~0.038 eV`, so the next Hong controller is provisional target selection plus final-source confirmation rather than generic source discovery
- Still open: the repo still lacks a final archived publisher article page, a declared keep/replace/remove policy for the legacy `0.028 eV` runtime row, and a final-source confirmation for whichever Hong statistic is chosen
- Next controller: `numeric_target_resolution_then_final_source_confirmation`
- Claim impact: no upgrade; this wave only strengthens Hong-side provenance and makes the numeric blocker more specific without closing the runtime row
- Workflow linkage: follows `For Work/18_Research_Hardening_Workflow.md` by narrowing one controlling blocker into a more explicit machine-readable next move before broadening scope

### 2026-06-18 - Jun runtime-separation and summary-interval pass

- Scope: move the narrowed Jun blocker out of prose only by separating the pinned Jun source-facing asymptotic-work quantity from the legacy `0.028 eV` mixed-lineage row inside the live verifier
- Added or changed: updated `Research_Landauer.py` so the main lower-bound metric now uses the pinned Jun source-facing asymptotic-work summary (`0.71 +/- 0.03 kT`) converted into `eV`, while the legacy `0.028 eV` value is retained only as mixed-lineage context; threaded the resulting Jun summary-layer interval into `uncertainty_preprocessing_manifest.json`, `uncertainty_propagation_summary.json`, `measured_constant_uncertainty_package.json`, the main verification artifact, and the generated source-evidence intake; then aligned `JUN_2014_UNCERTAINTY_GAP.md`, `jun_2014_uncertainty_gap.json`, `JUN_2014_RUNTIME_MAPPING_CONFLICT.md`, `jun_2014_runtime_mapping_conflict.json`, `ROW_CLOSURE_MATRIX.md`, `row_closure_matrix.json`, and the root docs/manifests to the new state
- Files touched: `Code/03_Research/Research_Landauer.py`, `Data/03_Research/experimental_data.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/uncertainty_preprocessing_manifest.json`, `Data/03_Research/uncertainty_propagation_summary.json`, `Data/03_Research/measured_constant_uncertainty_package.json`, `Data/03_Research/row_closure_matrix.json`, `ROW_CLOSURE_MATRIX.md`, `JUN_2014_UNCERTAINTY_GAP.md`, `Data/03_Research/jun_2014_uncertainty_gap.json`, `JUN_2014_RUNTIME_MAPPING_CONFLICT.md`, `Data/03_Research/jun_2014_runtime_mapping_conflict.json`, `README.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: `Jun` is no longer represented by the legacy `0.028 eV` row inside the main lower-bound metric; the verifier now uses the pinned Jun source-facing asymptotic-work quantity and carries a first-pass summary-layer interval, while the remaining blocker is the split/replace/relabel policy for the legacy row plus tighter file/row identity for the Jun summary quantity
- Still open: the legacy `0.028 eV` row is still mixed-lineage context rather than a closed `Jun` or `Hong` benchmark row, Berut still needs stronger-surface-or-policy closure, Hong still needs primary-source capture then numeric-target resolution, Peterson still needs one exact paper identity before row capture, and the broader derivation/units/mapping/beta lanes remain open
- Claim impact: no upgrade; this wave only makes the Jun lane more internally honest, more source-facing, and easier to harden without silently keeping the mixed-lineage runtime row inside the main metric

### 2026-06-18 - Jun quantitative-mismatch pass

- Scope: narrow the Jun blocker from a generic runtime-mapping problem to an evidence-backed quantitative mismatch using the pinned Jun primary-source-facing asymptotic-work summary
- Added or changed: updated the staged `Jun 2014` source record so it now records the source-facing `0.71 +/- 0.03 kT` asymptotic-work summary and the `+/- 0.10 kT` measurement-statistics scale; updated `JUN_2014_RUNTIME_MAPPING_CONFLICT.md`, `jun_2014_runtime_mapping_conflict.json`, `ROW_CLOSURE_MATRIX.md`, and `row_closure_matrix.json` so the next Jun controller is now a split/replace/relabel decision on the legacy `0.028 eV` runtime row before uncertainty closure; reran the verifier and synced root docs/manifests to the new controller wording and hashes
- Files touched: `docs/data/external/thermodynamics/landauer/jun_2014/source_record.json`, `JUN_2014_RUNTIME_MAPPING_CONFLICT.md`, `Data/03_Research/jun_2014_runtime_mapping_conflict.json`, `ROW_CLOSURE_MATRIX.md`, `Data/03_Research/row_closure_matrix.json`, `README.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: primary-source inspection of the Jun arXiv/PRL preprint text (`High-precision test of Landauer's principle in a feedback trap`), including the asymptotic-work summary `0.71 +/- 0.03 kT`; then `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the pinned Jun branch is no longer blocked only by a vague mapping/uncertainty statement; the current package now records that the pinned Jun asymptotic-work quantity sits near `0.01836 eV` at the current `300 K` verifier baseline and therefore does not match the legacy `0.028 eV` runtime row
- Still open: the repo still must decide whether the legacy `0.028 eV` row belongs in a non-Jun branch, whether a different Jun quantity can justify keeping it, or whether the row should be removed from Jun-facing closure logic entirely; source-backed uncertainty and propagated intervals for the final Jun-facing quantity also remain open
- Claim impact: no upgrade; this wave only makes the Jun-side blocker more evidence-backed and reduces the risk of treating the legacy runtime row as a clean Jun benchmark quantity

### 2026-06-18 - Claim-gate row-controller threading pass

- Scope: align the dependency/export gates with the same row-controller chain already exposed by the main verifier artifact, then sync the topic docs to the rerun outputs
- Added or changed: updated `Research_Landauer.py` so both `thermodynamic_claim_scope_gate` and `thermodynamic_bridge_foundation_claim_gate.json` now carry row-controller-aware blockers for `Berut`, `Jun`, `Hong`, and `Peterson`; synced `README.md`, `VERIFICATION_SPEC.md`, and `DATA_MANIFEST.md` to the new gate wording and refreshed manifest hashes/sizes for the rerun outputs
- Files touched: `Code/03_Research/Research_Landauer.py`, `README.md`, `VERIFICATION_SPEC.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the claim gates and the row-closure matrix now point to the same machine-readable next controllers, so dependent-topic inheritance and topic-level blocked claims no longer require separate blocker reconstruction paths
- Still open: Berut still needs stronger-surface-or-policy closure, Jun still needs runtime mapping then source-backed uncertainty, Hong still needs primary-source capture then numeric-target resolution, Peterson still needs one exact paper identity before row capture, and the derivation/units/mapping/beta lanes remain open
- Claim impact: no upgrade; this wave only unifies blocker navigation across the main artifact, the foundation gate, and the local docs

### 2026-06-18 - Main-artifact row-controller export pass

- Scope: move the active Landauer row controllers into the main verifier artifact so the current blocker chain can be reconstructed from the artifact itself instead of only from the separate row-closure matrix
- Added or changed: updated `Research_Landauer.py` so `row_closure_matrix.json` is now a declared verifier input and the main artifact exports `row_controller_summary` for `Berut`, `Jun`, `Hong`, and `Peterson`; synced `README.md`, `VERIFICATION_SPEC.md`, and `DATA_MANIFEST.md` to the new input chain and artifact field
- Files touched: `Code/03_Research/Research_Landauer.py`, `README.md`, `VERIFICATION_SPEC.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the main artifact now exposes the next controller for each active Landauer row without requiring a second manual reconstruction pass through `row_closure_matrix.json`
- Still open: the controllers themselves remain unchanged; Berut still needs stronger-surface-or-policy closure, Jun still needs runtime mapping then uncertainty, Hong still needs primary-source capture then numeric-target resolution, and Peterson still needs one exact paper identity before any row capture
- Claim impact: no upgrade; this wave only centralizes blocker visibility and improves artifact-first status reconstruction
- Notes: the rerun kept `3/3` primary tests passing and added `row_closure_matrix.json` to the declared verifier input chain.

### 2026-06-18 - For Work status-reconstruction sync pass

- Scope: sync the remaining local prose surfaces to the current controlling artifact/gate language after reconstructing `0.13` state in the `For Work` order
- Added or changed: reviewed `For Work/00_README.md`, `02_Project_Workflow_and_Lifecycle.md`, `04_Claim_and_Evidence_Rubric.md`, and `18_Research_Hardening_Workflow.md`; then aligned `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, and the README core-status line so they now match the current artifact/gate framing for Berut, Jun, and verifier inputs instead of older broader wording
- Files touched: `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `README.md`, `UPDATE_LOG.md`
- Verified with: direct consistency inspection against `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `thermodynamic_bridge_foundation_claim_gate.json`, `source_evidence_readiness_matrix.json`, and the updated local docs
- Result: no verifier rerun required because this wave did not modify a declared verifier input
- Blocker narrowed: the local prose package now points more directly to the current controlling blockers instead of older shorthand such as `raw-table source-lock`
- Still open: Berut stronger-surface-or-policy closure, Jun runtime-quantity mapping plus uncertainty capture, Hong primary-source capture plus numeric-target resolution, Peterson one-paper identity closure, and the broader derivation/uncertainty gates
- Claim impact: no upgrade; this wave only restores status-first consistency between `For Work` workflow expectations and the current `0.13` topic package

### 2026-06-16 - Jun/Hong/Peterson next-controller pass

- Scope: make the remaining non-Berut Landauer-row blockers easier to advance one step at a time by adding explicit `next_controller` states instead of leaving the next move to prose inference
- Added or changed: updated `row_closure_matrix.json` so `Jun`, `Hong`, and `Peterson` now expose explicit next-controller states; updated `jun_2014_uncertainty_gap.json`, `jun_2014_runtime_mapping_conflict.json`, `hong_2016_source_lineage_note.json`, and `peterson_2018_source_conflict.json` so each artifact now states the one next controlling closure move in machine-readable form
- Files touched: `Data/03_Research/row_closure_matrix.json`, `Data/03_Research/jun_2014_uncertainty_gap.json`, `Data/03_Research/jun_2014_runtime_mapping_conflict.json`, `Data/03_Research/hong_2016_source_lineage_note.json`, `Data/03_Research/peterson_2018_source_conflict.json`, `UPDATE_LOG.md`
- Verified with: direct consistency inspection against the current verifier artifact, source-evidence workflow files, and the updated row-governance JSON files
- Result: no verifier rerun required because this wave did not modify a declared verifier input
- Blocker narrowed: `Jun` now points first to runtime-quantity mapping and then uncertainty capture, `Hong` now points first to primary-source capture and then numeric-target resolution, and `Peterson` now points first to one exact paper identity before any numeric repair
- Still open: none of the three branches has closed its next controller yet, so the main claim ceiling and artifact status remain unchanged
- Claim impact: no upgrade; this wave only makes the next closure move for each remaining Landauer-row blocker more explicit and less guess-dependent

### 2026-06-16 - Berut row-governance narrowing pass

- Scope: align the manual Berut row-governance artifacts with the narrower `stronger surface or declared policy` framing already used by the verifier-driven workflow
- Added or changed: updated `row_closure_matrix.json`, `ROW_CLOSURE_MATRIX.md`, `berut_2012_provenance_gap.json`, `BERUT_2012_PROVENANCE_GAP.md`, and the matching README summary line so Berut is no longer described mainly as a generic raw/supplement-table problem; these artifacts now say more precisely that the next controlling blocker is one stronger upstream numeric surface or one explicit transcription/normalization policy, followed by source-row capture and mapping
- Files touched: `Data/03_Research/row_closure_matrix.json`, `ROW_CLOSURE_MATRIX.md`, `Data/03_Research/berut_2012_provenance_gap.json`, `BERUT_2012_PROVENANCE_GAP.md`, `README.md`, `UPDATE_LOG.md`
- Verified with: direct consistency inspection against `berut_2012_source_surface_note.json`, `berut_2012_transcription_policy_blocker.json`, the current verifier artifact, and the updated row-governance files
- Result: no verifier rerun required because this wave did not modify a declared verifier input
- Blocker narrowed: the row-governance layer now matches the main artifact in treating Berut as a `surface-or-policy` controller problem, not just a vague missing-table problem
- Still open: no stronger Berut numeric surface is archived, no transcription policy has been chosen, and no source-row-to-runtime mapping exists yet
- Claim impact: no upgrade; this wave only reduces wording drift between manual governance files and the verifier-driven claim ceiling

### 2026-06-16 - Berut blocker-language alignment pass

- Scope: align the remaining generated artifact language with the narrower Berut surface/transcription-policy framing instead of leaving some sections on the older generic raw-table wording
- Added or changed: updated `Research_Landauer.py` so the generated `evidence_lanes`, derivation-step question for uncertainty/source closure, tier-promotion requirements, and final interpretation now all describe the Berut blocker in the same narrower terms used by the source-evidence intake and readiness workflow; reran the verifier and synced manifest hashes to the new artifact
- Files touched: `Code/03_Research/Research_Landauer.py`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the main artifact no longer describes the Berut problem only as `raw table not archived`; it now says more precisely that Berut still lacks either a stronger upstream numeric surface or one declared transcription policy tied to a row locator
- Still open: the stronger Berut surface is still not archived, no explicit transcription policy has been chosen, Jun uncertainty is still open, and the bridge-proof lane remains blocked
- Claim impact: no upgrade; this wave only improves internal consistency and makes the main artifact harder to overread
- Notes: the rerun kept `3/3` primary tests passing, kept the topic artifact at `WARN`, and preserved the high-level source-readiness summary at `3/7` ready and `4/7` partial.

### 2026-06-16 - Berut intake/workflow threading pass

- Scope: move the narrowed Berut surface/transcription-policy blocker back into the verifier-generated workflow artifacts instead of leaving it only in dedicated side-note files
- Added or changed: `Research_Landauer.py` now treats `berut_2012_source_surface_note.json` and `berut_2012_transcription_policy_blocker.json` as declared verifier inputs; the generated source-evidence intake target for Berut now states that the currently visible Nature surface is still figure-level, and it now requires one explicit transcription-policy choice in addition to any future row locator; the readiness matrix now keeps Berut blocked by those named workflow fields instead of only by a generic missing-table description; synced `README.md`, `METHOD.md`, and `DATA_MANIFEST.md` to match the tighter machine-readable workflow boundary
- Files touched: `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `README.md`, `METHOD.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the Berut source-evidence lane no longer stops at `raw table still missing`; it now machine-readably says that the currently accessible source surface is still preview-level and that one declared normalization/transcription policy is still missing before row-level closure
- Still open: no stronger Berut source surface has been archived, no authoritative figure/table locator is attached, no transcription policy has been selected, and no source-row-to-runtime mapping exists yet
- Claim impact: no upgrade; this wave only makes the verifier-driven workflow more honest and harder to overread
- Notes: the rerun kept `3/3` primary tests passing, kept the topic artifact at `WARN`, preserved the high-level readiness counts at `3/7` ready and `4/7` partial, and added the Berut surface-note plus transcription-policy JSON files to the declared verifier input chain.

### 2026-06-16 - Peterson composite-misreference hardening pass

- Scope: move the `Peterson 2018` blocker beyond a generic `source identity unresolved` label by attaching direct DOI-metadata evidence showing that the local runtime branch is composite
- Added or changed: verified two candidate DOI routes via Crossref metadata; updated the staged Peterson source record so it now records both DOI checks, candidate paper metadata, and a `composite_misreference_detected` resolution state; updated the Peterson conflict note/JSON to record that the local runtime branch mixes incompatible DOI, title, system, and authorship cues; downgraded both local `experimental_data.py` Peterson entries to explicit legacy composite placeholders; updated the verifier intake wording so the generated source-evidence intake now reflects the stronger blocker language
- Files touched: `docs/data/external/thermodynamics/landauer/peterson_2018/source_record.json`, `PETERSON_2018_SOURCE_CONFLICT.md`, `Data/03_Research/peterson_2018_source_conflict.json`, `Data/03_Research/experimental_data.py`, `Data/landauer/experimental_data.py`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/row_closure_matrix.json`, `ROW_CLOSURE_MATRIX.md`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: Crossref work-record fetches for `10.1103/PhysRevLett.120.210601` and `10.1038/s41567-018-0250-5`; then `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the Peterson branch is no longer described only as an unresolved one-paper citation problem; the repo now records machine-readably that the local runtime branch is composite and therefore unsafe to treat as a source-ready benchmark lane
- Still open: one exact upstream paper still has not been chosen for this branch, no row-level numeric capture or uncertainty row exists, and the branch should still be removed rather than repaired if no exact source-to-runtime mapping can be justified
- Claim impact: no upgrade; this wave only strengthens claim discipline by replacing a vague citation conflict with a directly evidenced composite-misreference blocker
- Notes: the rerun kept the main artifact at `WARN`, preserved `3/3` primary test passes, kept the readiness summary at `3/7` ready and `4/7` partial, and updated the Peterson intake row so `doi_or_url` and `reported_energy_value` now remain explicitly partial because the branch is composite rather than merely underspecified.

### 2026-06-16 - Berut source-surface narrowing pass

- Scope: narrow the `Berut 2012` provenance blocker from a generic missing-row-label statement to a more precise description of what the currently visible primary source surface actually exposes
- Added or changed: inspected the currently accessible Nature preview surface for `10.1038/nature10872`; updated the Berut external source record so it now records that the visible surface exposes the abstract plus Figure 1-3 labels but not a directly visible row table or supplementary identifier; added a dedicated Berut source-surface note/JSON; synced root topic docs and the data manifest to reflect that the next Berut provenance move may require supplementary capture, figure-level locator capture, or explicit transcription policy
- Files touched: `docs/data/external/thermodynamics/landauer/berut_2012/source_record.json`, `BERUT_2012_SOURCE_SURFACE_NOTE.md`, `Data/03_Research/berut_2012_source_surface_note.json`, `BERUT_2012_PROVENANCE_GAP.md`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: direct inspection of the Nature preview page for `https://www.nature.com/articles/nature10872`; then `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the Berut row-locator problem is now explicitly tied to a preview surface that currently looks figure-level rather than table-level
- Still open: the repo still lacks an archived source row, a supplementary-file identity, a figure-to-runtime transcription policy, and an explicit source-row-to-runtime mapping
- Claim impact: no upgrade; this wave only makes the Berut provenance blocker more precise and harder to overread
- Notes: the rerun kept the main artifact at `WARN`, preserved `3/3` primary test passes, and updated the declared Berut source-record input hash without changing the high-level readiness counts.

### 2026-06-16 - Berut transcription-policy narrowing pass

- Scope: turn the newly narrowed Berut surface blocker into one explicit policy-choice blocker rather than leaving future row normalization method implicit
- Added or changed: added a Berut transcription-policy blocker note/JSON; updated the Berut provenance-gap JSON and row-closure matrix so they now require one declared policy choice if Berut remains figure-level at the accessible source surface; synced root topic docs and the data manifest to reflect the new policy-choice blocker
- Files touched: `BERUT_2012_TRANSCRIPTION_POLICY_BLOCKER.md`, `Data/03_Research/berut_2012_transcription_policy_blocker.json`, `BERUT_2012_PROVENANCE_GAP.md`, `Data/03_Research/berut_2012_provenance_gap.json`, `ROW_CLOSURE_MATRIX.md`, `Data/03_Research/row_closure_matrix.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: direct consistency inspection against `BERUT_2012_SOURCE_SURFACE_NOTE.md`, `berut_2012_source_surface_note.json`, and the current row-closure state
- Result: no verifier rerun required because this wave did not modify a declared verifier input
- Blocker narrowed: the Berut provenance lane no longer stops at `row locator missing`; it now also records that the repo must choose one explicit normalization policy before claiming row-level closure
- Still open: no supplementary file has been archived, no figure panel has been declared authoritative, no machine-transcribed non-preview row has been attached, and no source-row-to-runtime mapping exists yet
- Claim impact: no upgrade; this wave only reduces ambiguity about what kind of future Berut evidence would count as credible closure

### 2026-06-15 - Hong branch machine-readable workflow pass

- Scope: bring the staged `Hong 2016` alternate Landauer branch into the verifier-driven evidence workflow instead of leaving it only in prose-side blocker notes
- Added or changed: `Research_Landauer.py` now reads the staged `Hong 2016` source record as a declared verifier input and emits a seventh source-evidence target for the nanomagnetic-memory candidate branch; the row-closure matrix was expanded so Hong now appears as its own machine-readable row-level blocker rather than only as adjacent narrative; the Hong source package and acquisition blocker were then tightened again so the repo now records a candidate DOI/PMID/PMCID trail, a confirmed Crossref DOI metadata anchor, a locally archived Crossref work-record snapshot, current direct-fetch access blockers, and a numeric-lane note that now distinguishes Crossref's qualitative abstract from the still-missing source-facing number while also quantifying what the current `44% above limit` wording implies against the verifier baseline
- Files touched: `Code/03_Research/Research_Landauer.py`, `VERIFICATION_SPEC.md`, `ROW_CLOSURE_MATRIX.md`, `Data/03_Research/row_closure_matrix.json`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `README.md`, `DATA_MANIFEST.md`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `UPDATE_LOG.md`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the Hong branch is no longer just a side note to the Jun blocker; it is now an explicit source-evidence target and row-level closure lane with its own pending DOI/page, numeric-target, and uncertainty requirements
- Still open: direct publisher-page or PDF acquisition beyond the current `403`/Cloudflare challenge, exact source-facing row extraction, formal `0.026 eV` versus `0.028 eV` reconciliation, and any propagated interval for the alternate branch
- Claim impact: no upgrade; this wave only makes the alternate-source blocker visible in the same machine-readable workflow that already controls Berut, Jun, and Peterson
- Notes: the rerun kept the main artifact at `WARN`, preserved `3/3` primary test passes, kept the source-evidence workflow at `3/7` targets ready for source review and `4/7` still partial, moved the Hong intake row to `4/8` complete fields with bibliographic identity now closed by Crossref metadata while direct page capture remains partial, and added the local `crossref_work_record.json` snapshot to the verifier input chain.

### 2026-05-28 - Source-evidence and foundation-gate hardening pass

- Scope: `0.13` verifier artifact, source-evidence workflow files, and dependency export gate
- Added or changed: source-evidence intake stub, readiness matrix, foundation claim gate, and artifact-level claim-scope controller
- Files touched: `Code/03_Research/Research_Landauer.py`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `.venv\Scripts\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: broad provenance uncertainty became named blockers for raw Landauer numeric tables, uncertainty propagation, and UET-specific derivation
- Still open: source-normalized row capture, uncertainty-aware preprocessing, and a derivation map from UET variables to standard thermodynamic identities
- Claim impact: wording stayed capped at lower-bound and standard-formula consistency only
- Notes: foundation exports were split into allowed lower-bound/formula lanes and blocked bridge-proof/source-normalized/external-validation lanes

### 2026-06-12 - Source-normalization and uncertainty-preprocessing pass

- Scope: verifier-driven provenance and uncertainty hardening for the `0.13` foundation topic
- Added or changed: lane-based method/baseline docs, gravity/measured-constant source records, partially populated source-evidence intake, readiness matrix with partial-evidence counts, uncertainty-preprocessing manifest, and rerun artifact
- Files touched: `METHOD.md`, `BASELINE_COMPARISON.md`, `README.md`, `DATA_MANIFEST.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `UPDATE_LOG.md`, `Code/03_Research/Research_Landauer.py`, `docs/core/uet_parameters.py`, `docs/core/uet_master_equation.py`, `docs/data/external/gravity/ligo_black_hole_mergers/source_record.json`, `docs/data/external/gravity/eht_black_hole_masses/source_record.json`, `docs/data/external/constants/codata/measured_constants_2022_source_record.json`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/uncertainty_preprocessing_manifest.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: source readiness moved from an all-pending state to `3/6` targets ready for source review and `3/6` targets with partial evidence; uncertainty preprocessing moved from a generic plan to a `5`-row machine-readable manifest
- Still open: Berut raw/supplement row capture, Jun row-level file identity, Peterson source-resolution closure, propagated uncertainty outputs, and UET bridge derivation map
- Claim impact: no upgrade; documentation now makes the current claim ceiling easier to audit
- Notes: the verifier rerun passed all `3/3` primary formula/lower-bound tests; artifact stayed `WARN` because plot rendering lacks `plotly` in the bundled runtime and because the topic's source/uncertainty/derivation blockers remain open

### 2026-06-12 - Partial uncertainty-propagation artifact pass

- Scope: move `0.13` from uncertainty planning only toward machine-readable propagated intervals
- Added or changed: verifier now writes `Data/03_Research/uncertainty_propagation_summary.json` and threads its status into the main artifact, claim scope gate, and dependency gate wording
- Files touched: `Code/03_Research/Research_Landauer.py`, `README.md`, `VERIFICATION_SPEC.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `Data/03_Research/uncertainty_propagation_summary.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: uncertainty moved from preprocessing-only to a partial propagated-interval package covering `4/5` tracked rows
- Still open: Jun uncertainty row, measured-constant uncertainty package, Berut raw-row locator/source closure, Peterson source-resolution closure, and UET bridge derivation map
- Claim impact: no upgrade; the artifact now makes it explicit that Berut's topic-summary `1 sigma` interval still crosses the Landauer lower bound, so lower-bound wording remains conservative
- Notes: plot rendering still warns because the bundled runtime lacks `plotly`; this did not block the machine-readable uncertainty outputs

### 2026-06-12 - Bridge derivation-boundary mapping pass

- Scope: make the UET bridge-proof gap explicit instead of leaving it as a generic blocker label
- Added or changed: root `DERIVATION_MAP.md`, verifier-generated `Data/03_Research/bridge_derivation_map.json`, and documentation/spec references to the new derivation-boundary files
- Files touched: `DERIVATION_MAP.md`, `Code/03_Research/Research_Landauer.py`, `README.md`, `METHOD.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `Data/03_Research/bridge_derivation_map.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the bridge-proof blocker is now decomposed into explicit open steps for units contract, Landauer-to-UET mapping, gravity-identity mapping, and uncertainty/source closure
- Still open: all four derivation steps remain open or partial; the new map is a boundary artifact, not a derivation itself
- Claim impact: no upgrade; the claim ceiling is clearer and harder to overread

### 2026-06-12 - Units-contract boundary pass

- Scope: separate physical SI observables from topic-local proxies before any stronger bridge wording
- Added or changed: root `UNITS_CONTRACT.md`, verifier-generated `Data/03_Research/units_contract.json`, and documentation/spec references to the new units-boundary files
- Files touched: `UNITS_CONTRACT.md`, `Code/03_Research/Research_Landauer.py`, `README.md`, `METHOD.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `Data/03_Research/units_contract.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the topic now explicitly declares which symbols are SI quantities and which remain proxies, reducing the risk of overreading engine outputs as physical thermodynamic observables
- Still open: no justified proxy-to-SI bridge conversion exists yet; the units contract is a boundary artifact, not a closure artifact

### 2026-06-12 - Landauer-to-UET mapping honesty pass

- Scope: make the Landauer bridge lane say exactly what current code supports and nothing more
- Added or changed: root `LANDAUER_UET_MAPPING.md`, verifier-generated `Data/03_Research/landauer_uet_mapping.json`, and documentation/spec references to the new lane-specific mapping files
- Files touched: `LANDAUER_UET_MAPPING.md`, `Code/03_Research/Research_Landauer.py`, `README.md`, `METHOD.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `Data/03_Research/landauer_uet_mapping.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the topic now records machine-readably that the current engine path imports the standard lower bound as a constraint and does not yet expose a nontrivial UET-added Landauer term
- Still open: a non-circular mapping from UET variables to erasure cost; parameter-origin closure for any bridge coefficient; and a test that distinguishes imported baseline from UET-added structure

### 2026-06-12 - Beta-role clarification pass

- Scope: make the role of `beta` in the 0.13 Landauer lane explicit and evidence-backed
- Added or changed: root `BETA_ROLE.md`, verifier-generated `Data/03_Research/beta_role_clarification.json`, and documentation/spec references to the new beta-role files
- Files touched: `BETA_ROLE.md`, `Code/03_Research/Research_Landauer.py`, `README.md`, `METHOD.md`, `VERIFICATION_SPEC.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `Data/03_Research/beta_role_clarification.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: `$env:PYTHONUTF8='1'; C:\Users\santa\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe docs\topics\0.13_Thermodynamic_Bridge\Code\03_Research\Research_Landauer.py`
- Result: `WARN`
- Blocker narrowed: the topic now records machine-readably that `beta` is present in topic code/language but is not closed as a derived bridge coefficient in the current verifier lane
- Still open: decide whether beta remains a placeholder, normalization tag, or future derived coefficient; if derived, attach a nontrivial tested output path

### 2026-06-13 - Legacy claim-surface cleanup pass

- Scope: reduce overclaim risk in older `0.13` code, bibliography, and working-copy data surfaces
- Added or changed: `LEGACY_CLAIM_SURFACE_AUDIT.md`; downgraded `Code/README.md` to a legacy code map; downgraded `Research_Thermodynamic_Bridge.py` and `Research_Real_Data_Validation.py` to legacy diagnostic surfaces; softened legacy bibliography wording; replaced overstrong `verification` strings in duplicate Berut working copies; softened legacy summary labels in duplicate `experimental_data.py` copies; replaced one legacy `Doc/keed` analysis note with bounded status wording
- Files touched: `LEGACY_CLAIM_SURFACE_AUDIT.md`, `Code/README.md`, `Code/03_Research/Research_Thermodynamic_Bridge.py`, `Code/03_Research/Research_Real_Data_Validation.py`, `Ref/BIBLIOGRAPHY_ANALYSIS.md`, `Data/03_Research/berut_2012.json`, `Data/landauer/berut_2012.json`, `Data/03_Research/experimental_data.py`, `Data/landauer/experimental_data.py`, `Doc/keed/ANALYSIS_03_Landauer.md`, `UPDATE_LOG.md`
- Verified with: targeted file inspection plus string-level consistency checks on the edited legacy surfaces
- Result: claim-boundary cleanup completed; topic status remains unchanged
- Blocker narrowed: legacy surfaces are less likely to outrun the root-topic verifier and claim-gate ceiling
- Still open: additional legacy notes may still contain strong internal prose below warning banners, and legacy scripts are still secondary to `Research_Landauer.py`
- Claim impact: no upgrade; this wave only reduces the chance that readers confuse legacy diagnostic surfaces with current topic authority

### 2026-06-13 - Legacy analysis-note boundary pass

- Scope: continue reducing overclaim risk by rewriting high-risk legacy analysis notes under `Doc/` and `Doc/keed/`
- Added or changed: replaced several legacy analysis files with bounded summary notes that now defer explicitly to the root topic package and verifier artifact instead of carrying forward closed-result wording
- Files touched: `Doc/ANALYSIS_Thermodynamic_Bridge.md`, `Doc/ANALYSIS_01_Thermodynamics.md`, `Doc/keed/ANALYSIS_03_Real_Data.md`, `Doc/keed/ANALYSIS_01_Engine_Thermo.md`, `Doc/keed/03_Research/before.md`, `UPDATE_LOG.md`
- Verified with: targeted file inspection and repo-local string scan for high-risk wording after the rewrites
- Result: bounded-note rewrites completed for the highest-risk legacy analysis surfaces inspected in this wave
- Blocker narrowed: legacy note surfaces now align more clearly with the current `0.13` claim ceiling and are less likely to be mistaken for live status authority
- Still open: more legacy notes remain in `Doc/keed/03_Research/` and adjacent `Doc/` files, so the legacy-surface audit is not yet exhaustive
- Claim impact: no upgrade; this wave only improves documentation discipline and reduces stale overclaim pathways

### 2026-06-13 - Remaining legacy paper-note boundary pass

- Scope: continue the `0.13` documentation-hardening sweep across remaining high-risk legacy analysis and paper-note files
- Added or changed: replaced additional `Doc/ANALYSIS_*.md` and `Doc/keed/03_Research/*` files with short bounded notes that now defer explicitly to the current verifier artifact and root topic package
- Files touched: `Doc/ANALYSIS_Engine_Thermodynamics.md`, `Doc/ANALYSIS_Proof_Entropy_Max.md`, `Doc/ANALYSIS_Thermodynamic_Bridge_Research.md`, `Doc/keed/03_Research/analysis.md`, `Doc/keed/03_Research/result_summary.md`, `Doc/keed/03_Research/Final_Paper_Bekenstein.md`, `Doc/keed/03_Research/Final_Paper_Landauer.md`, `UPDATE_LOG.md`
- Verified with: targeted file inspection and repo-local string scans after the rewrites
- Result: the highest-risk remaining note surfaces inspected in this wave were downgraded to bounded historical notes
- Blocker narrowed: legacy analysis and paper-note files are now less likely to be mistaken for live evidence or final-status authority
- Still open: more legacy surfaces remain, especially `Doc/keed/03_Research/solution.md` and `Final_Paper_Jacobson.md`, so the full legacy-note audit remains incomplete
- Claim impact: no upgrade; this wave only improves claim discipline and consistency across historical notes

### 2026-06-13 - Remaining bridge-logic and Jacobson-note boundary pass

- Scope: continue the `0.13` legacy-note sweep across the remaining bridge-logic, Jacobson, Bekenstein-framing, and data-loader note surfaces
- Added or changed: replaced the remaining high-risk note files with bounded historical notes that now point readers back to the root topic package, provenance files, and verifier artifact
- Files touched: `Doc/keed/03_Research/solution.md`, `Doc/keed/03_Research/Final_Paper_Jacobson.md`, `Doc/keed/ANALYSIS_03_Bridge_Logic.md`, `Doc/keed/ANALYSIS_03_Data_Loader.md`, `UPDATE_LOG.md`
- Verified with: targeted file inspection and repo-local string scans after the rewrites
- Result: the inspected bridge-logic and Jacobson-facing legacy notes no longer present themselves as current proof or verification authority
- Blocker narrowed: the set of stale legacy files that can be mistaken for live `0.13` status is smaller again
- Still open: additional historical notes may still exist elsewhere, but the most obvious remaining overclaim surfaces in `Doc/keed/03_Research/` are now substantially reduced
- Claim impact: no upgrade; this wave only tightens documentation discipline and reduces stale overclaim pathways

### 2026-06-13 - Legacy doc-surface inventory pass

- Scope: convert the ad hoc legacy-note cleanup into a tracked inventory for `Doc/` and `Doc/keed/`
- Added or changed: added `LEGACY_DOC_SURFACE_INVENTORY.md` to list the current legacy documentation surfaces and their bounded-note status
- Files touched: `LEGACY_DOC_SURFACE_INVENTORY.md`, `UPDATE_LOG.md`
- Verified with: direct inventory check against the current `Doc/` and `Doc/keed/` file set plus repo-local scans for stale note wording
- Result: the current legacy documentation surfaces for `0.13` now have a dedicated control file instead of relying only on repeated search passes
- Blocker narrowed: future hardening waves can verify doc-surface coverage from one inventory file instead of reconstructing the note set from memory
- Still open: this inventory controls legacy documentation posture only; it does not close the scientific blockers around source-normalized Landauer data, uncertainty propagation, or UET bridge derivation
- Claim impact: no upgrade; this wave only improves documentation governance and auditability

### 2026-06-13 - Row-closure matrix pass

- Scope: move `0.13` from broad source/uncertainty blocker wording toward row-by-row closure planning
- Added or changed: `ROW_CLOSURE_MATRIX.md` and `Data/03_Research/row_closure_matrix.json`; updated root docs to reference the new row-level blocker map
- Files touched: `ROW_CLOSURE_MATRIX.md`, `Data/03_Research/row_closure_matrix.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: direct inspection against the current source-evidence intake, readiness matrix, uncertainty preprocessing manifest, and uncertainty propagation summary
- Result: `0.13` now has an explicit row-by-row closure map for Berut, Jun, Peterson, LIGO/EHT context rows, and the measured-constant uncertainty support layer
- Blocker narrowed: next hardening work can now target one row or support layer at a time instead of using only broad labels like `source` or `uncertainty`
- Still open: the matrix itself does not close any row; Berut raw-row provenance, Jun uncertainty capture, Peterson source identity, and measured-constant runtime uncertainty remain open
- Claim impact: no upgrade; this wave only improves blocker precision and auditability

### 2026-06-13 - Landauer row-contract pass

- Scope: further narrow the main `0.13` benchmark lane to the two most actionable rows, `Berut` and `Jun`
- Added or changed: `LANDAUER_ROW_CONTRACT.md` and `Data/03_Research/landauer_row_contract.json`; updated root docs to reference the new Berut/Jun closure contract
- Files touched: `LANDAUER_ROW_CONTRACT.md`, `Data/03_Research/landauer_row_contract.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: direct inspection against the current runtime rows, source records, row-closure matrix, and uncertainty artifacts
- Result: `0.13` now has an explicit minimum-closure contract for the two Landauer rows most relevant to near-term hardening
- Blocker narrowed: Berut is now explicitly framed as a row-level provenance problem, while Jun is explicitly framed as a missing source-backed uncertainty problem
- Still open: neither row is closed; the contract is a navigation artifact only
- Claim impact: no upgrade; this wave only sharpens the Landauer-lane blocker map

### 2026-06-13 - Jun uncertainty-gap pass

- Scope: isolate the narrowest remaining Landauer-row blocker in `0.13`, namely the missing `Jun 2014` source-backed uncertainty field
- Added or changed: `JUN_2014_UNCERTAINTY_GAP.md` and `Data/03_Research/jun_2014_uncertainty_gap.json`; updated the source-evidence intake/readiness files to make the missing Jun uncertainty field explicit; updated root docs to reference the new Jun-specific blocker artifact
- Files touched: `JUN_2014_UNCERTAINTY_GAP.md`, `Data/03_Research/jun_2014_uncertainty_gap.json`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: direct inspection against the current Jun runtime row, Jun source record, uncertainty preprocessing manifest, and uncertainty propagation summary
- Result: the `Jun` blocker is now isolated as a missing source-backed uncertainty field rather than only a broad `uncertainty open` label
- Blocker narrowed: future work can now target one specific missing field set for the `Jun 2014` row
- Still open: the row remains central-value only until a source-backed uncertainty value or interval is archived and propagated
- Claim impact: no upgrade; this wave only sharpens the Jun-specific blocker map

### 2026-06-13 - Berut provenance-gap pass

- Scope: isolate the row-level provenance blocker on the strongest current Landauer row in `0.13`
- Added or changed: `BERUT_2012_PROVENANCE_GAP.md` and `Data/03_Research/berut_2012_provenance_gap.json`; updated root docs to reference the new Berut-specific blocker artifact
- Files touched: `BERUT_2012_PROVENANCE_GAP.md`, `Data/03_Research/berut_2012_provenance_gap.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: direct inspection against the current Berut runtime row, Berut source record, row-closure matrix, and uncertainty propagation summary
- Result: the `Berut` blocker is now isolated as a row-level provenance and table-mapping problem rather than only a broad source-lock label
- Blocker narrowed: future work can now target one specific missing field set for the `Berut 2012` row
- Still open: the row remains summary-level provenance only until an archived row locator and row-to-runtime mapping are attached
- Claim impact: no upgrade; this wave only sharpens the Berut-specific blocker map

### 2026-06-14 - Peterson source-conflict pass

- Scope: isolate the `Peterson 2018` blocker as a one-paper source-identity conflict rather than only an unresolved-source placeholder
- Added or changed: `PETERSON_2018_SOURCE_CONFLICT.md` and `Data/03_Research/peterson_2018_source_conflict.json`; updated `docs/data/external/thermodynamics/landauer/peterson_2018/source_record.json`; threaded the conflict into the row-closure and intake workflow plus root docs
- Files touched: `PETERSON_2018_SOURCE_CONFLICT.md`, `Data/03_Research/peterson_2018_source_conflict.json`, `docs/data/external/thermodynamics/landauer/peterson_2018/source_record.json`, `Data/03_Research/row_closure_matrix.json`, `Data/03_Research/source_evidence_intake_stub.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: direct inspection of the local `experimental_data.py` Peterson branch, the external source-resolution record, and targeted JSON syntax/reference checks
- Result: the quantum-Landauer branch is now explicitly blocked by a conflict between the local runtime DOI and the likely trapped-ion Landauer paper identity
- Blocker narrowed: future work can now resolve one exact source identity before attempting row capture, unit normalization, or uncertainty propagation
- Still open: the branch still has no resolved one-paper source identity, no row-level value capture, and no uncertainty package
- Claim impact: no upgrade; this wave only sharpens the Peterson-specific blocker map

### 2026-06-14 - Measured-constant uncertainty-package pass

- Scope: isolate the measured-constant uncertainty layer as an explicit runtime policy package rather than leaving gravity-context intervals described only as `mass-only`
- Added or changed: `MEASURED_CONSTANT_UNCERTAINTY_PACKAGE.md`; extended `Research_Landauer.py` so it now generates `Data/03_Research/measured_constant_uncertainty_package.json` and threads its status into the main verifier artifact; updated root docs to reference the new package
- Files touched: `MEASURED_CONSTANT_UNCERTAINTY_PACKAGE.md`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/measured_constant_uncertainty_package.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: rerun of `Research_Landauer.py`, JSON syntax check on the new machine-readable package, and direct inspection of the new package summary inside the main verifier artifact
- Result: `0.13` now states explicitly that a runtime proxy for `G` uncertainty exists, which rows would inherit it, and that the current black-hole intervals still exclude it
- Blocker narrowed: future work can now choose between `declare-only`, `thread into intervals`, or `replace provisional numeric proxy with direct 2022 extraction`
- Still open: the package is still provisional, the current intervals remain mass-only, and spin/systematic astrophysical terms are still out of scope
- Claim impact: no upgrade; this wave only sharpens the measured-constant uncertainty boundary

### 2026-06-14 - Gravity mass-plus-G-proxy interval pass

- Scope: advance the gravity-context uncertainty lane from `declare-only` measured-constant policy to provisional combined intervals while keeping the old mass-only baseline visible
- Added or changed: extended `Research_Landauer.py` so the uncertainty summary now emits `entropy_*_mass_plus_G_proxy` and `hawking_*_mass_plus_G_proxy` outputs for `GW150914`, `M87*`, and `Sgr A*`; updated the measured-constant package status and row policy; updated root docs and row-closure map to match
- Files touched: `Code/03_Research/Research_Landauer.py`, `Data/03_Research/measured_constant_uncertainty_package.json`, `Data/03_Research/uncertainty_propagation_summary.json`, `Data/03_Research/row_closure_matrix.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `MEASURED_CONSTANT_UNCERTAINTY_PACKAGE.md`, `UPDATE_LOG.md`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`
- Verified with: rerun of `Research_Landauer.py`, direct inspection of the new combined interval fields, and confirmation that the main artifact still remains `WARN`
- Result: gravity-context rows now expose both mass-only baseline intervals and provisional mass-plus-`G`-proxy combined intervals, while still labeling the added `G` term as a runtime proxy rather than a closed source-normalized uncertainty package
- Blocker narrowed: the next uncertainty decision is no longer `whether` to include measured-constant terms at all, but whether to replace the provisional `G` proxy with direct 2022 extraction and how to add spin/systematic terms
- Still open: Jun remains central-value only, raw-row source closure remains open, the `G` term is still a provisional local proxy, and systematic astrophysical uncertainty is still excluded
- Claim impact: no upgrade; this wave makes the gravity-context uncertainty lane more explicit without promoting it beyond provisional status

### 2026-06-14 - Jun runtime-mapping conflict pass

- Scope: narrow the `Jun 2014` blocker beyond `missing uncertainty` by making the runtime-to-source quantity mismatch explicit
- Added or changed: `JUN_2014_RUNTIME_MAPPING_CONFLICT.md` and `Data/03_Research/jun_2014_runtime_mapping_conflict.json`; updated the Jun source record next-step wording; updated the verifier's source-evidence intake generator so the `reported_energy_value` field is no longer treated as fully closed for Jun
- Files touched: `JUN_2014_RUNTIME_MAPPING_CONFLICT.md`, `Data/03_Research/jun_2014_runtime_mapping_conflict.json`, `docs/data/external/thermodynamics/landauer/jun_2014/source_record.json`, `Code/03_Research/Research_Landauer.py`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: direct inspection of the archived Jun source-facing summary, targeted consistency scans, and JSON syntax checks on the new Jun machine-readable artifact
- Result: `0.13` now states explicitly that the current `0.028 eV` Jun runtime row is not yet normalized to one named source-facing `Jun 2014` quantity, so the row cannot be treated as only awaiting an uncertainty field
- Blocker narrowed: the next Jun pass can now decide whether to replace the runtime row, split it into a differently labeled Jun quantity, or archive the missing conversion path
- Still open: the source-facing row/fit target is still not archived, the unit conversion path is still missing, and no propagated Jun interval exists
- Claim impact: no upgrade; this wave only sharpens the Jun-specific blocker map

### 2026-06-14 - Legacy 0.028 eV lineage-note pass

- Scope: narrow the remaining `0.13` Jun blocker again by separating `missing Jun mapping` from `possible cross-source lineage contamination`
- Added or changed: `HONG_2016_SOURCE_LINEAGE_NOTE.md` and `Data/03_Research/hong_2016_source_lineage_note.json`; softened the legacy `JUN_2014_DATA` runtime surface in both `experimental_data.py` copies; updated the Jun source record wording; updated the verifier intake generator so the Jun target now names the feedback-trap branch explicitly and flags the legacy `0.028 eV` value as possibly belonging to a later nanomagnetic-memory branch
- Files touched: `HONG_2016_SOURCE_LINEAGE_NOTE.md`, `Data/03_Research/hong_2016_source_lineage_note.json`, `Data/03_Research/experimental_data.py`, `Data/landauer/experimental_data.py`, `docs/data/external/thermodynamics/landauer/jun_2014/source_record.json`, `Code/03_Research/Research_Landauer.py`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: local lineage search for `0.028 eV`, `44% above limit`, and `Experimental (2016)` plus targeted web confirmation that a later nanomagnetic-memory Landauer narrative exists distinct from the pinned Jun 2014 feedback-trap source
- Result: `0.13` now treats the legacy `0.028 eV` row as a mixed-lineage blocker rather than only a Jun uncertainty/mapping blocker
- Blocker narrowed: future work can now split into either a clean `Jun 2014` row reconstruction or a separate `Hong 2016` source-intake pass instead of pretending both branches are already one row
- Still open: no primary `Hong 2016` source package is archived yet, no one-paper runtime-row reassignment is closed yet, and no propagated interval exists for the legacy `0.028 eV` row under a resolved source identity
- Claim impact: no upgrade; this wave only sharpens the provenance boundary around the legacy runtime row

### 2026-06-15 - Hong 2016 candidate-source staging pass

- Scope: give the possible later nanomagnetic-memory branch a real local source-package anchor instead of leaving it only as a narrative suspicion inside the lineage note
- Added or changed: `docs/data/external/thermodynamics/landauer/hong_2016/source_record.json`; updated the Hong lineage note and root `0.13` docs so the branch is now explicitly staged as a source-record-only candidate rather than an unnamed alternate source family
- Files touched: `docs/data/external/thermodynamics/landauer/hong_2016/source_record.json`, `HONG_2016_SOURCE_LINEAGE_NOTE.md`, `Data/03_Research/hong_2016_source_lineage_note.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: targeted web confirmation of the bibliographic identity `Jeongmin Hong et al., Science Advances, 2016-03-01` plus local consistency checks against the legacy `0.028 eV / Experimental (2016) / 44% above limit` wording
- Result: `0.13` now has a separate local source-package anchor for the likely alternate branch behind the legacy runtime row
- Blocker narrowed: future work can now pursue a concrete `Hong 2016` intake pass with DOI/page capture and row extraction, instead of reconstructing the alternate branch from prose clues alone
- Still open: the staged Hong record is still secondary-confirmed only, the official DOI/page is not archived locally, and the runtime row is still not reassigned or uncertainty-closed
- Claim impact: no upgrade; this wave only improves provenance structure and blocker navigation

### 2026-06-15 - Hong numeric-mismatch pass

- Scope: narrow the alternate-branch blocker again by separating `candidate Hong source family` from `candidate Hong numeric closure`
- Added or changed: `HONG_2016_NUMERIC_MISMATCH_NOTE.md` and `Data/03_Research/hong_2016_numeric_mismatch_note.json`; updated root `0.13` docs so they now state explicitly that the staged Hong branch may fit the `2016` narrative while still not matching the local `0.028 eV` runtime number
- Files touched: `HONG_2016_NUMERIC_MISMATCH_NOTE.md`, `Data/03_Research/hong_2016_numeric_mismatch_note.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: targeted web review of secondary Hong summaries showing about `0.026 eV` at `300 K` together with local inspection of the current `0.028 eV` runtime row
- Result: `0.13` now treats the alternate-source blocker and the alternate-number blocker as separate issues
- Blocker narrowed: future work can now target exact numeric extraction from the Hong paper instead of treating source-family capture alone as enough
- Still open: primary DOI/page capture for Hong, source-facing quantity extraction, `0.026` versus `0.028` reconciliation, and uncertainty propagation all remain open
- Claim impact: no upgrade; this wave only tightens numeric provenance discipline around the staged Hong branch

### 2026-06-15 - Hong source-acquisition blocker pass

- Scope: make the remaining Hong bibliographic gap explicit instead of leaving it implicit inside source-record wording
- Added or changed: `HONG_2016_SOURCE_ACQUISITION_BLOCKER.md` and `Data/03_Research/hong_2016_source_acquisition_blocker.json`; updated root `0.13` docs so they now state explicitly that the staged Hong branch still lacks a primary DOI or official article page
- Files touched: `HONG_2016_SOURCE_ACQUISITION_BLOCKER.md`, `Data/03_Research/hong_2016_source_acquisition_blocker.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`
- Verified with: targeted web searches confirming the likely Hong title/authors/publication/date from repeated secondary summaries while still failing to capture a primary DOI/article page in this wave
- Result: `0.13` now tracks the Hong branch as blocked not only by lineage and numeric mismatch, but also by missing primary bibliographic anchoring
- Blocker narrowed: future work can now target `primary anchor capture` as its own explicit task instead of bundling it loosely into generic provenance cleanup
- Still open: DOI/page capture, exact numeric extraction, uncertainty extraction, and row reassignment all remain open
- Claim impact: no upgrade; this wave only sharpens bibliographic provenance control


### 2026-06-22 - Berut Figure 3 landmark-candidate capture pass

- Scope: narrow the remaining Berut Figure 3 digitization blocker from generic axis-landmark capture to candidate panel-frame review without claiming numeric transcription.
- Added or changed: `BERUT_2012_FIGURE3_LANDMARK_CANDIDATE_CAPTURE.md` and `Data/03_Research/berut_2012_figure3_landmark_candidate_capture.json`; threaded the candidate artifact into `Research_Landauer.py`, source-evidence intake, row-controller summary, foundation gate, and local docs.
- Files touched: `BERUT_2012_FIGURE3_LANDMARK_CANDIDATE_CAPTURE.md`, `Data/03_Research/berut_2012_figure3_landmark_candidate_capture.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/row_closure_matrix.json`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`.
- Verified with: automated PIL/NumPy raster pass over `jpeg_3` and `jpeg_2`, rerun of `Research_Landauer.py`, and JSON syntax checks on the new and regenerated machine-readable artifacts.
- Result: `jpeg_2` is now recorded as the automated-review-preferred candidate for visual panel-frame review because it exposes stronger full-panel frame candidates; `jpeg_3` remains documented as the prior protocol first candidate but did not expose robust full-axis segments under this automated pass.
- Blocker narrowed: Berut now moves from `berut_figure_3_axis_landmark_coordinates_required` to `berut_figure_3_candidate_panel_frame_review_required`.
- Still open: human or visual review of candidate panel frames, axis tick mapping, Landauer reference/limit marker identification, selected point/curve coordinates, and numeric transcription or a stronger source-data surface.
- Claim impact: no upgrade; this wave records candidate landmarks only and keeps the Berut row below source-normalized numeric closure.


### 2026-06-22 - Berut Figure 3 semantic asset-role review pass

- Scope: narrow the Berut Figure 3 digitization path by correcting which embedded raster should be treated as the quantitative heat-plot candidate.
- Added or changed: `BERUT_2012_FIGURE3_SEMANTIC_ASSET_REVIEW.md` and `Data/03_Research/berut_2012_figure3_semantic_asset_review.json`; updated the digitization protocol so `jpeg_2` is now the preferred quantitative digitization candidate and `jpeg_3` is demoted to schematic/procedure support unless later evidence proves otherwise.
- Files touched: `BERUT_2012_FIGURE3_SEMANTIC_ASSET_REVIEW.md`, `Data/03_Research/berut_2012_figure3_semantic_asset_review.json`, `BERUT_2012_FIGURE3_DIGITIZATION_PROTOCOL.md`, `Data/03_Research/berut_2012_figure3_digitization_protocol.json`, `Code/03_Research/Research_Landauer.py`, `Data/03_Research/row_closure_matrix.json`, `Data/03_Research/source_evidence_intake_stub.json`, `Data/03_Research/source_evidence_readiness_matrix.json`, `Data/03_Research/thermodynamic_bridge_foundation_claim_gate.json`, `Result/artifacts/0_13_thermodynamic_bridge_verification.json`, `README.md`, `METHOD.md`, `LIMITATIONS.md`, `ROW_CLOSURE_MATRIX.md`, `DATA_MANIFEST.md`, `UPDATE_LOG.md`.
- Verified with: author-page semantic check, local raster-candidate evidence from the previous landmark pass, rerun of `Research_Landauer.py`, and JSON syntax checks on the new and regenerated machine-readable artifacts.
- Result: Berut no longer starts numeric digitization from the likely reset-procedure schematic; the next quantitative pass should begin with `jpeg_2`.
- Blocker narrowed: Berut now moves from `berut_figure_3_candidate_panel_frame_review_required` to `berut_figure_3_quantitative_panel_tick_mapping_required`.
- Still open: select the relevant quantitative panel within `jpeg_2`, map duration and heat ticks, identify the Landauer reference/limit marker, capture selected point/curve pixels, and define digitization uncertainty before any numeric transcription.
- Claim impact: no upgrade; this wave corrects candidate priority only and keeps the Berut row below source-normalized numeric closure.

### 2026-07-21 - Matter-space thermal control pilot

- Scope: add the Wave 4 normalized thermal control lane without changing the main `0.13` Landauer verifier or its controlling source-lock blocker.
- Added or changed: pilot specification, five-way synthetic runner, locked preregistration, metadata-only second-sound source package, disclosed post-diagnostic numerical amendment, generated artifact/CSV/four figures, six artifact-boundary tests, and focused README/derivation/data-manifest updates.
- Files touched: `THERMAL_MATTER_SPACE_PILOT_SPEC.md`, `Code/03_Research/Research_Matter_Space_Thermal_Control.py`, three `Data/03_Research/matter_space_*` control files, `Result/artifacts/matter_space_thermal_control.json`, four `Result/03_show_Result/matter_space_thermal_*.png`, the generated CSV, `docs/core/test/test_matter_space_thermal_pilot.py`, `README.md`, `DERIVATION_MAP.md`, `DATA_MANIFEST.md`, and `UPDATE_LOG.md`.
- Verified with: deterministic pilot rerun; JSON/hash checks; visual review of all four figures; `pytest docs/core/test/test_matter_space_thermal_pilot.py -q` (`6 passed`).
- Result: analytical Cattaneo residual is `0`; phase, lag, and hysteresis relative errors are below `2.4e-7`; homogeneous core cross-check error is `0`; dissipation/trace source signs pass; refined ledger closure is `6.02e-7` against `1e-6`.
- Numerical disclosure: the initially locked `dt=2.5e-4` run produced ledger closure `1.49e-5` and remains recorded as failed; amendment 001 changed only analysis `dt` to `5e-5`, was informed by that failure, and is not presented as blind confirmation.
- Blocker narrowed: the pilot now isolates physical pre-arrival leakage (`0.01764` against `1e-6`) as the core causal controller, while the external source package remains separately blocked by absent local numeric rows and absent dimensional `Phi`-to-observable mapping.
- Still open: repair or replace the causal discretization/kernel under the unchanged cone gate; acquire a licensed numeric source package with locator, units, preprocessing, uncertainty, and hashes; define the dimensional observable map before any fit.
- Claim impact: no upgrade. Status remains `SIMULATION_ONLY / FAIL`; no external validation, thermodynamic derivation, second-sound prediction, or Landauer derivation is claimed.
- Workflow linkage: Wave 4 of the matter-space research plan; the main `0.13` verification artifact and Landauer controlling blocker were intentionally not rerun or changed.

### 2026-07-22 - Core thermodynamic constraint dependency gate

- Scope: expose exactly which Topic `0.13` results the core matter-space/GR program may inherit without converting thermodynamic constraints into a UET derivation.
- Added or changed: dependency contract, deterministic gate generator, machine-readable artifact, and artifact-boundary tests; synchronized `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, and the canonical topic summary.
- Verified with: `pytest docs/core/test/test_core_thermodynamic_topic_0_13_constraint.py -q` (`12 passed`) plus direct JSON/schema and scientific-input identity checks.
- Result: the gate is `BLOCKED / THERMODYNAMIC_CONSTRAINT_EXPORTS_AVAILABLE_CORE_CLOSURE_NOT_DERIVED`; only the Landauer lower bound and standard thermodynamic/gravity identities export as class-C constraints, while Cattaneo remains simulation-only.
- Controlling blocker: `topic_0_13_constraint_only_eos_transport_entropy_bridge_missing`.
- Preserved state: the main foundation remains `FOUNDATION_WARN`, Topic `0.13` remains `Draft / B`, the four Berut/Jun/Hong/Peterson row controllers are unchanged, and the failed thermal-pilot gates remain visible.
- Still open: non-circular bridge derivation, derived `beta`, charge EOS, covariant transport, entropy current and dissipative-Bianchi closure, dimensional `Phi/R` observable mapping, physical causal repair, and external numeric heat-transport evidence.
- Claim impact: none. The packet is a dependency boundary, not validation or status promotion.

### 2026-07-29 - Thermal source observable-map closure pass

- Scope: narrow the real-lane thermal blocker by separating the standard TTG measurement operator from the unresolved UET dimensional calibration.
- Added or changed: `THERMAL_SOURCE_OBSERVABLE_MAPPING_SPEC.md`, `matter_space_thermal_source_review.json`, `thermal_source_observable_map.py`, `audit_thermal_source_observable_mapping.py`, `matter_space_thermal_observable_map_readiness.json`, and the synchronized formula/data/verification/limitation/README records.
- Verified with: `.venv\\Scripts\\python.exe docs\\scripts\\audit\\audit_thermal_source_observable_mapping.py`; `.venv\\Scripts\\python.exe -m pytest docs\\core\\test\\test_thermal_source_observable_mapping.py docs\\core\\test\\test_thermal_observable_bridge.py docs\\core\\test\\test_persistence_energy_diagnostic.py docs\\core\\test\\test_matter_interaction_forward.py -q` (`15 passed`).
- Result: `PASS_WITH_BLOCKED_DIMENSIONAL_AND_DATA_LANES`; source identities and unit contexts are complete, normalized quasi-temperature TTG and normalized `Phi` operators are explicit, and no holdout or fitting input was consumed.
- Blocker narrowed: the previous generic “no observable map” blocker is now split into (1) missing local source-normalized numeric package, (2) open `alpha_Phi_K`, and (3) downstream heat-flux/entropy maps.
- Still open: archive a licensed numeric source with locator, preprocessing, uncertainty, and hash; independently derive or calibrate `alpha_Phi_K`; repair the thermal pilot causal gate before any external comparison.
- Next controller: `thermal_source_numeric_package_and_dimensional_calibration_missing`.
- Claim impact: no upgrade; the normalized operator is a definition/measurement target, not validation or a UET thermodynamic derivation.
- Workflow linkage: source pass plus observable-map gate pass under the UET formula-audit and data-provenance standards.

### 2026-08-01 - Source-backed TTG diagnostic contract pass

- Scope: extend the normalized TTG observable contract with source-backed wavevector and propagation-length diagnostics without opening a dimensional UET calibration.
- Added or changed: `ttg_wavevector`, `ttg_propagation_length`, public core exports, focused tests, source-review relation registry, generated readiness artifact, and this log/spec synchronization.
- Verified with: `pytest` focused thermal suite (`14 passed`) and `audit_thermal_source_observable_mapping.py`; artifact remains `PASS_WITH_BLOCKED_DIMENSIONAL_AND_DATA_LANES`.
- Result: `q_TTG=2*pi/Lambda`, `v_TTG=Lambda/(2*t_d)`, and `l_p=Lambda/(-2*ln(-DeltaT_d))` now have explicit units/domain checks and source-role metadata.
- Still open: local numeric source package with row-level provenance, independent `alpha_Phi_K` derivation/calibration, heat-flux/entropy maps, and the locked 2026 holdout.
- Claim impact: no upgrade; `Phi` is not identified with temperature and no external validation or fitting was performed.
- Next controller: `thermal_source_numeric_package_and_dimensional_calibration_missing`.