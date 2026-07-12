# Method

## Problem Target

This topic studies whether UET-style social and economic models can be connected
to measurable market and macroeconomic diagnostics. The current hardening pass
limits accepted evidence to data integrity and descriptive benchmark metrics.

## Evidence Lanes

| Lane | Files | Current role |
| :-- | :-- | :-- |
| Market time-series diagnostics | Yahoo-style CSVs, `source_lock_manifest.json`, `Research_Economic_Data_Audit.py` | primary verifier lane |
| Economy baseline sanity | `Global_Economy_2024.json`, `source_lock_manifest.json`, verifier artifact | primary verifier lane |
| Daily indicator snapshot | `daily_economic_snapshot.json`, `source_lock_manifest.json` | local context only until upstream source is recorded |
| Source evidence workflow | `source_evidence_intake_stub.json`, `source_evidence_readiness_matrix.json`, `source_lock_manifest.json` | provenance gate before data or claim upgrades |
| Social power engine | `Engine_Power_Dynamics.py` | model proposal; not causal evidence |
| Stability/proof scripts | `Proof_Social_Stability.py`, `Research_8_Billion_Resonance.py` | heuristic simulations; require seeded artifact gates |
| Policy/strategy scripts | world lease, leverage, water, ecosystem scripts | future scenario lanes; blocked by `model_claim_gate.json` |

## Variables

| Symbol / field | Meaning | Unit |
| :-- | :-- | :-- |
| `P_t` | close price or index level at date `t` | source unit |
| `r_t` | log return | dimensionless |
| `sigma_ann` | annualized volatility | dimensionless fraction/year |
| `corr` | Pearson correlation of returns | dimensionless |
| `Gini` | inequality index | 0-100 |
| `GDP_PPP_USD` | purchasing-power-parity GDP | USD |
| `Population` | human population | count |
| `Omega` | simulation resource-spread proxy | dimensionless, heuristic |

## Procedure

1. Parse each market CSV and count valid close-price rows.
2. Compute log returns and annualized volatility.
3. Compute descriptive cross-market return correlations.
4. Parse the economy JSON and check Gini values against the declared 0-100 unit convention.
5. Record all input hashes and provenance blockers.
6. Regenerate source-lock, source-evidence, and model-claim workflow files.
7. Write a machine-readable artifact with metrics, thresholds, checks, blockers,
   and limitations.

## Domain of Validity

The current method supports only internal descriptive diagnostics for the local
market/economy data package. It does not prove policy causality, strategic
superiority, social stabilization, or game-theory dominance.

## Dependency Policy

Simulation claims from the power engine must not be treated as evidence for real
economic outcomes until they are calibrated against source-locked data and pass a
separate deterministic verifier with seeds and thresholds.

## Claim Workflow

1. Run `Research_Economic_Data_Audit.py` to regenerate the artifact and workflow files.
2. Read `source_lock_manifest.json` as the normative map of which files are Yahoo-style working copies, local macroeconomic working tables, or local gateway snapshots.
3. Fill `source_evidence_intake_stub.json` only with real upstream market, macro, and snapshot metadata.
4. Use `source_evidence_readiness_matrix.json` as the provenance gate before changing working-copy data or claim class.
5. Check `model_claim_gate.json` before treating any simulation or policy lane as evidence.

## Current provenance gate state

- Market lanes: partial but nearly complete (`5/6` fields each), blocked only by retrieval date
- Global economy lane: partial (`4/6`), blocked by missing upstream URL/DOI and retrieval date
- Daily snapshot lane: partial (`5/6`), blocked by missing upstream URL/API
- No lane is source-review-ready yet, but all five are now field-mapped instead of blank placeholders

## Book 1 historical diagnostic lane

The Book 1 lane uses a U.S. annual 1959-2024 panel only after every source is
locked. `R` is an equal-weight geometric index of real GDP per capita, output per
hour, and primary energy per capita. `N` is a training-window-standardized proxy
formed from CPI-energy inflation and unemployment. `K` is real intellectual-property
investment per employee, and `I` is a geometric infrastructure proxy built from
private tangible nonresidential and government fixed assets per employee.

The operational regression, monetary-resource mismatch, asset tracking, energy
history, and wage-productivity checks are diagnostic-only. They neither identify
fiat-currency causality nor validate a policy, asset, or strategy claim.
