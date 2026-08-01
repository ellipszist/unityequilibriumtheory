# Verification Specification: Topic 0.25

## Primary hardening commands

Run the source transformation first when the official BEA/EIA files or the EPI provider export
change. Then lock the manifest and run the non-network verifier:

```powershell
cd C:\Users\santa\Desktop\uet_harness
.\.venv\Scripts\python.exe docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Research_UET_Economics_External_Source_Transform.py --vintage 2026-07-12 --epi-csv <provider-export.csv>
.\.venv\Scripts\python.exe docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Research_UET_Economics_Source_Package.py --vintage 2026-07-12
.\.venv\Scripts\python.exe docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Verify_UET_Economics_Hardening.py
```

The transform script archives provider inputs and creates normalized subsets. The source
package verifies the frozen vintage and writes source/formula/parameter/holdout/claim gates.
The aggregate verifier runs the panel and all four audits with network disabled. It records
non-zero subcommand exits in `execution_gate.command_failures`; stale artifacts cannot mask a
runtime failure.

The legacy descriptive command is separate:

```powershell
.\.venv\Scripts\python.exe docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Research_Economic_Data_Audit.py
```

## Required gates

- `uet_us_economics_source_readiness.json`: `15/15` required primary inputs.
- `uet_us_macro_panel_status.json`: complete 1959-2024 coverage, no imputation.
- `uet_us_economics_formula_gate.json`: formula IDs, units, origin, proof status, and limits.
- `uet_us_economics_parameter_policy.json`: horizons, proxy definitions, baselines, and
  candidate threshold declared before model execution.
- `uet_us_economics_holdout_policy.json`: rolling origins 2000-2024 and transition split.
- uet_economics_claim_gate.json: allowed and blocked export language.
- 0_25_uet_measurement_validity_audit.json: declared proxy-family correlations, three-year
  combinations, sign stability, and missing-family blockers.
- 0_25_uet_welfare_audit.json: source-locked rent/OER/income/house-price coverage and
  no-imputation welfare outcomes.
- `0_25_fed_z1_funding_mapping_probe.json`: source-locked 1959-2024 sectoral flow mapping,
  rounded capital-account identity check, and explicit payer/resource visibility blockers.
- `0_25_bls_io_source_gate.json`: BLS input-output source identity, 1997-2024 coverage claim,
  access observation, provider quality notice, and no-use-until-validated gate.
- `0_25_fed_z1_funding_mix_audit.json`: signed net-flow associations, payment-flow scale,
  period summaries, and explicit `NOT_IDENTIFIED` gross funding-share gate.
- `0_25_payer_resource_join_readiness.json`: source/hash/readiness records for the funding,
  industry-use, labor-hours, physical-resource, project-ledger, and concordance links; no
  imputation and no payment-level inference. The BEA code concordance may pass with boundary,
  while the flow join remains blocked.
- `0_25_bea_1997_io_benchmark_audit.json`: byte-hash and layout checks for the official 1997 BEA make/use, direct-requirements, and industry-by-industry total-requirements archives. It is a one-year benchmark with an explicit not-time-series boundary.
- `0_25_bls_industry_hours_source_package.json`: official API request/response hashes, returned NAICS4 coverage, annual-hours units, missing-code list, and provider-quota failures; no imputation.
- `0_25_usgs_material_quantity_audit.json`: raw workbook hashes, commodity/quantity-column mapping, coverage, and explicit no-industry/project-allocation boundary.
- `0_25_sec_public_firm_funding_proxy.json` and `0_25_sec_public_firm_funding_mix_audit.json`: current-vintage 10-K fact hashes, tag/unit/date coverage, descriptive firm ratios, and `NOT_IDENTIFIED` funding-share status.
- `0_25_usaspending_federal_project_ledger.json`: cached USAspending.gov request/response hashes, fixed DOE FY2024 five-page coverage, normalized obligation units, and explicit non-settlement/non-financing boundary.
- `0_25_usaspending_award_level_outlay_audit.json`: ten fixed award-detail response hashes, account-level obligation/outlay completeness, differences/ratios, nonrepresentative sample policy, and explicit non-settlement boundary.
- `0_25_usaspending_award_funding_account_audit.json`: ten fixed `/awards/funding/` response hashes, FY2024 federal-account/agency/object-class fields, explicit six-award missingness, no-imputation coverage, and the source-WARN/bounded-join boundary.
- `0_25_federal_award_outlay_reconciliation.json`: grouped USAspending DOE obligation response hash, Treasury DOE MTS Table 5 row hash, normalized comparison, obligation/outlay difference and ratio, and explicit `NOT_ONE_TO_ONE` settlement boundary.
- `0_25_treasury_funding_source_audit.json`: Treasury Fiscal Data request/response hashes for MTS tables 1/2/4/5/6 and debt-to-the-penny at 2024-09-30, normalized current-dollar rows, aggregate summary, and explicit no-award-level-attribution boundary.
- `0_25_project_payment_ledger_gate.json`: public-data restriction, approved restricted-use route, and controlling `PROJECT_PAYMENT_LEDGER_NOT_PUBLIC` blocker.
- aggregate `execution_gate`: all verifier subcommands exit zero.
- aggregate legacy_claim_quarantine: every legacy markdown note contains the required
  Legacy claim boundary warning before it can be treated as topic documentation.
- uet_economics_warn_gate_registry.json: all 12 Evidence Grade A gates, statuses, evidence
  requirements, and controlling effects.
- research register, variable dictionary, causal DAG, and claim matrix: preregistered
  architecture contracts embedded in the aggregate evidence bundle.

## Acceptance and model contract

Primary horizon: 3 years. Sensitivities: 1 and 5 years. Forecast origins: 2000 onward,
using only information available at each origin. The candidate rule requires at least 10%
lower median rolling-origin RMSE than every named baseline and a 95% block-bootstrap interval
for squared-error differences below zero. This rule is diagnostic-only and cannot upgrade
Claim Class C.

The resource baselines are constant-growth (training mean target) and zero-growth. The Stone
baselines are inflation autoregression, money-growth-only, and quantity-style M2 minus real GDP
per-capita growth. Pre/post regime summaries use 1959-1970 and 1974-2024, excluding 1971-1973.

## Artifact contract

`Result/artifacts/0_25_uet_economics_verification.json` must preserve:

- source, welfare-source, transform, panel, formula, parameter, holdout, claim, and
  sub-artifact hashes;
- retrieval vintage, coverage, units/proxy definitions, formulas, coefficients, and uncertainty;
- rolling-origin boundaries, baseline errors, median and aggregate RMSE, and bootstrap intervals;
- asset-lane status, energy-definition gate, measurement-validity result, failures, limitations,
  and blocked claims;
- funding-source mapping status, Fed Z.1 archive hash, series roles/units, accounting-bridge
  residuals, payer/resource visibility blockers, and no-imputation coverage;
- BLS I-O source gate status, URL, archive identity (when present), quality notice, and access
  blocker;
- funding-mix association rows, lag policy, signed-ratio definitions, and gross-share blocker;
- payer-resource join component statuses, local input hashes, missing components, and join claim boundary;
- BLS industry-hours, USGS material, SEC Company Facts, USAspending federal-award, Treasury funding-source, award-outlay reconciliation, award funding-account, and project-ledger artifact hashes, coverage, units, and bounded-join limitations;
- command exit codes, legacy-claim quarantine result, and the current controller status;
- a self-contained evidence_bundle containing source records/hashes, transform and panel
  payloads, formula/parameter/holdout contracts, research register, variable dictionary,
  causal DAG, claim matrix, WARN registry, and complete sub-artifact payloads.

## Current machine result

- Source readiness: `PASS`, `15/15`.
- Panel: `PASS`, `66` rows, 1959-2024.
- Resource, Stone, and wage sub-artifacts: `DIAGNOSTIC_COMPLETE`.
- Energy sub-artifact: `WARN`; postwar throughput is ready, historical energy-mix export and
  literal density basis are blocked.
- Aggregate: `WARN`; controller remains `DESCRIPTIVE_DIAGNOSTIC_ONLY`; legacy quarantine is
  `PASS` for 12 files.
- Candidate signals: false at all tested horizons.
- Measurement validity: WARN; R-family correlations exceed the declared 0.8 diagnostic threshold,
  but coefficient signs are not stable across combinations and the patent family is absent.
- Research architecture: WARN; current package is Package Tier A, target is Evidence Grade A,
  and the 12-gate registry still contains open controlling gates. Strategy/social claims remain
  quarantined.
- Payer-resource additions: USGS, SEC, the fixed USAspending DOE FY2024 public-award sample, the Treasury aggregate funding-source snapshot, the award-outlay reconciliation, and the award-level account-outlay audit are `PASS_WITH_BOUNDARY`; the award funding-account source is `WARN` (4/10 fixed awards with FY2024 rows, six explicit missing awards) while its bounded join component is `PASS_WITH_BOUNDARY`; the reconciliation is explicitly `NOT_ONE_TO_ONE`. BLS industry-hours remains `WARN` for candidate-set coverage but its 11 returned series are complete for 1987-2024 (418 rows). The join gate reports bounded public inputs, while the private project payment ledger is still `BLOCKED`.

## Interpretation boundary

PASS on a source or panel gate means that the declared input and transformation contract is
satisfied. DIAGNOSTIC_COMPLETE means the predeclared comparison ran. Neither status means
an economic law was confirmed. WARN is retained when a declared sub-lane or evidence-grade
gate is intentionally open; no average can hide a controlling WARN. Causal, policy,
asset-superiority, and strategic claims require separate human-reviewed identification and
external replication.
