# Method

## Problem Target

This topic studies whether UET-style social and economic models can be connected
to measurable market and macroeconomic diagnostics. The current hardening pass
limits accepted evidence to data integrity and descriptive benchmark metrics.

## Evidence Lanes

| Lane | Files | Current role |
| :-- | :-- | :-- |
| Market time-series diagnostics | Yahoo-style CSVs, `Research_Economic_Data_Audit.py` | primary verifier lane |
| Economy baseline sanity | `Global_Economy_2024.json`, verifier artifact | primary verifier lane |
| Daily indicator snapshot | `daily_economic_snapshot.json` | local context only until upstream source is recorded |
| Social power engine | `Engine_Power_Dynamics.py` | model proposal; not causal evidence |
| Stability/proof scripts | `Proof_Social_Stability.py`, `Research_8_Billion_Resonance.py` | heuristic simulations; require seeded artifact gates |
| Policy/strategy scripts | world lease, leverage, water, ecosystem scripts | future scenario lanes |

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
6. Write a machine-readable artifact with metrics, thresholds, checks, blockers,
   and limitations.

## Domain of Validity

The current method supports only internal descriptive diagnostics for the local
market/economy data package. It does not prove policy causality, strategic
superiority, social stabilization, or game-theory dominance.

## Dependency Policy

Simulation claims from the power engine must not be treated as evidence for real
economic outcomes until they are calibrated against source-locked data and pass a
separate deterministic verifier with seeds and thresholds.
