# Method

## Problem target

This topic studies whether UET-style condensate and pairing ideas can reproduce selected superconducting or superfluid benchmark behavior.

## Core components

### Engine components
- `Code/01_Engine/Engine_Superconductivity.py`

### Proof-oriented components
- `Code/02_Proof/Proof_Cooper_Pairing.py`

### Research and comparison components
- `Code/03_Research/Experiment_Superconductor_Data.py`
- `Code/03_Research/Research_Hydrides.py`
- `Code/03_Research/Research_Plasma.py`
- `Data/03_Research/source_evidence_intake_stub.json`
- `Data/03_Research/source_evidence_readiness_matrix.json`
- `Data/03_Research/branch_claim_gate.json`

## Variable framing

- Primary modeled quantities: critical temperature, order-parameter-like quantities, coupling terms, and material descriptors
- Formula registry: see `FORMULA_AUDIT.md` for the distinction between McMillan/Allen-Dynes baseline formulas, calibrated material inputs, heuristic UET coherence terms, and superfluid/plasma diagnostics.

## Assumptions

- The current scripts behave like phenomenological internal models tied to selected materials and curated datasets.

## Domain of validity

- Selected superconducting materials, hydrides, and related transition benchmarks.

## Excluded cases

- A microscopic many-body derivation for all superconductors or a universal superfluid theory.

## Parameter sensitivity note

- Material selection and calibration choices still affect reported fits.
- The current primary verifier is the raw McMillan baseline because it produces a simple auditable artifact from the topic-local working-copy table.
- The verifier now includes an inverse-McMillan diagnostic: holding `Theta_D_K` and `mu_star` fixed, it solves for the `lambda_ep` that would reproduce the observed `Tc`. This identifies whether the current row-level coupling package is over- or under-driving the baseline.
- The verifier also records signed-error bias and grouped summaries by material type and source so the baseline failure can be localized to parameter-package clusters instead of treated as one undifferentiated miss.
- The verifier now also compares the raw gate table against the broader comprehensive package on overlapping materials and writes a row-level provenance manifest for drift tracking.
- A secondary sensitivity step now re-evaluates the raw gate with `lambda_ep` and `mu_star` substituted from the broader package on overlapping rows, while keeping `Theta_D_K` fixed. This is diagnostic only and is used to estimate how much row drift contributes to the FAIL.
- The verifier now turns that sensitivity result into `row_normalization_queue.json`, which ranks materials by projected error reduction and drift severity so row-level provenance work can proceed systematically.
- The verifier also writes `row_normalization_status.json`, which records source-status, current row package, internal comparison package, and next actions for each queued material.
- The verifier now also writes `row_normalization_candidates.json`, which marks whether a row has a plausible internal consensus candidate or still requires explicit external resolution.
- The verifier now also materializes `provisional_normalized_superconductors.json` and reruns the McMillan gate on that provisional table. This is an internal sensitivity experiment to estimate how much of the FAIL is driven by row-package drift.
- The verifier also writes `provisional_residual_blockers.json`, which separates rows that still fail after the provisional substitutions from rows that mainly await source locking.
- The verifier also writes `residual_blocker_row_dossiers.json`, which translates the remaining blockers into explicit row-resolution packets with source targets, required fields, and unit-choice questions.
- The verifier also writes `residual_blocker_field_lock_matrix.json`, which turns those packets into a field-level lock table for `Tc`, phonon proxy, `lambda_ep`, and `mu_star`.
- The verifier also writes `residual_blocker_proxy_sensitivity.json`, which compares `Theta_D_K` and `omega_log_K` under the same internal candidate package for the remaining blocker rows.
- The verifier also writes `vanadium_source_lock_packet.json`, which condenses the current best internal state for the single remaining borderline conventional row into one execution packet.
- The verifier also writes `a15_external_resolution_packet.json`, which condenses the shared unresolved state of `Nb3Sn` and `Nb3Ge` into one execution packet for the A15 pair.
- The verifier also writes `vanadium_candidate_patch_preview.json`, which turns the current Vanadium packet into a ready-to-apply row patch preview that still awaits source confirmation.
- The verifier also writes `a15_candidate_patch_preview.json`, which documents why the A15 pair remains unpatchable until external row evidence resolves the key fields.
- The verifier also writes `row_evidence_intake_stub.json`, which is the structured handoff layer for row-level evidence before any patch preview is promoted into an edit.
- The verifier now pre-fills that intake layer with working-copy row context from the Vanadium and A15 packets wherever the repo already knows the current benchmark values or unresolved proxy alternatives.
- The verifier also writes `row_evidence_readiness_matrix.json`, which converts that intake layer into an explicit gate for whether patch review can begin and now distinguishes source-complete fields from context-only fields.
- The verifier also writes `row_evidence_execution_queue.json`, which converts the same blocker rows into a concrete evidence-collection order so the next source pass can start from a stable row and field target.
- The verifier also writes `row_evidence_source_review_packets.json`, which turns that queue into a field-by-field review form so the next literature or source-table pass can attach evidence without inventing structure on the fly.
- The verifier also writes `row_evidence_decision_gate.json`, which translates those review forms into a concrete compatibility checklist so row evidence can be evaluated consistently before patch review.
- The source-lock layer now also points to an external row-resolution target manifest under `docs/data/external/condensed_matter/superconductivity/...` so the next evidence-acquisition pass starts from pinned upstream targets instead of chat-only intent.
- That external target folder now also carries an intake stub and readiness matrix so raw row archiving can be tracked in the external-data layer before values are promoted into topic-local review.
- The same external target folder now also carries an acquisition queue and topic handoff gate so archive work can be sequenced and then checked before entering topic-local compatibility review.
- It now also carries one archive dossier per residual blocker material so raw capture requirements are tracked at the row level before the topic-local review packets are touched.
- It now also carries a local-anchor manifest so the next archive pass can reuse existing repo hints while still treating them as below the threshold of real external row evidence.
- The verifier also writes topic-level `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, and `branch_claim_gate.json`, which separate the raw baseline FAIL from normalization workflow, Allen-Dynes/UET branches, and high-Tc future lanes.
- The Allen-Dynes/UET engine must be promoted through a separate verifier that reports per-material residuals and labels calibrated inputs before it can support stronger claims.
- The source-lock layer now pins McMillan 1968, Allen-Dynes 1975, and NIMS SuperCon provenance records, but this is not the same as row-level upstream normalization.

## Dependency policy

- `0.11_Phase_Transitions` may reference this topic only as a condensate/transition benchmark dependency until the formula and data gates are stronger.
- `0.13_Thermodynamic_Bridge` may use superfluid entropy or condensation-energy notes only with explicit unit conventions.
- `0.0_Grand_Unification` should treat UET coherence terms here as heuristic bridge terms, not proof-level support.

## Next model-hardening experiment

1. Build a row-level material table where each `Tc`, phonon-temperature proxy, `lambda`, and `mu_star` value has a source row or explicit literature citation.
2. Use the inverse-McMillan audit to flag rows where the declared `lambda_ep` strongly disagrees with the coupling implied by the observed `Tc`.
3. Run the raw McMillan gate against the normalized table without inverse calibration.
4. Run a separate Allen-Dynes/UET candidate gate with labels for source-locked, calibrated, and heuristic inputs.
5. Require a held-out material split before promoting any prediction-strength language.
