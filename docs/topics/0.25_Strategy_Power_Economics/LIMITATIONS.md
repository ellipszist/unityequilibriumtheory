# Limitations: Topic 0.25

## Current boundary

The topic is `Structured / Tier A` as an internally auditable package, while its scientific
claim remains `Claim Class C` and `DESCRIPTIVE_DIAGNOSTIC_ONLY`. The tier change reflects the
presence and rerunnability of standards artifacts; it is not a theory confirmation.

## Data limitations

- The primary panel is U.S.-only, annual, and 1959-2024. It is not a global causal comparison.
- BEA fixed-asset inputs are chain-type quantity indexes (2017=100), not dollar-valued stocks.
  Dividing them by employees creates indexed proxies, not physical capital measures.
- EIA primary energy measures throughput in quadrillion Btu. It is not a literal fuel-energy
  density measure.
- The EIA 1776-1945 historical energy-mix export is absent.
- A source-locked heat-content table with a common physical basis and explicit treatment of
  nuclear, hydro, wind, and solar is absent.
- LBMA annual gold and licensed S&P 500 total-return exports are absent; Yahoo price-only
  files are not substitutes.
- The EPI export is a current provider chart construction. It is not silently relabeled as the
  Book's typical-worker series. BLS is reported as a separate comparator.
- Legacy Yahoo-style market files, the global economy JSON, and daily snapshot have incomplete
  upstream metadata and remain descriptive working copies only.
- Fed Z.1 S11.1.i.a now supplies a complete annual sectoral accounting bridge, but it does not
  identify invoice-level payer/payee, funding provenance for a particular investment, or a
  concordant labor and natural-resource extraction quantity. The current release is revised
  2026:Q1, so historical-as-of vintage testing remains open.
- The official BLS I-O source is identified for 1997-2024, but the repository retrieval was
  access-denied and the provider has a 2026-02-06 quality notice for removed matrix files. No
  BLS matrix result is used until an approved, hashed replacement archive passes validation.

- Z.1 funding-mix ratios are signed net transactions, not gross financing shares: debt can be
  refinancing or repayment, equity can be issuance or repurchase, and saving is not earmarked
  to a specific investment.
- The ten-award account-outlay sample is deterministic but nonrepresentative. Even when account obligation and outlay fields are complete, they are not bank settlement or supplier-invoice observations.
- The award funding-account probe links only the returned FY2024 subset (4/10 fixed awards) to federal account, agency, and object-class reporting fields. Six missing award-year rows remain `WARN` and un-imputed; an account/program label is not the ultimate financing source or bank settlement.
- The federal-account budget-resource lane covers only the two accounts observed in that fixed sample. FY2024 budget authority, appropriations, obligations, outlays, and unobligated balances are account-reporting quantities; even a passing authority identity does not reveal the tax/debt/cash instrument or a payment to a supplier.
- The downstream subaward lane is dominated by one award with 3,168 reported rows; nine fixed awards report zero subawards. Subaward reporting is an agreement/recipient disclosure and can be incomplete; it does not establish invoice settlement, payroll, physical delivery, or financing source.
- The award-to-outlay comparison reports DOE FY2024 grouped award obligations of about `$46.04B` versus Treasury DOE net outlays of about `$49.32B` (`NOT_ONE_TO_ONE`). This gap cannot be labeled unpaid awards, profit funding, debt funding, or money creation because the constructs and scopes differ.
- Treasury Fiscal Data now supplies a fixed FY2024 aggregate bridge for receipts, outlays, deficit financing, and debt. It cannot determine whether a particular award was funded by tax receipts, borrowing, cash balances, or another aggregate category.
- USAspending.gov now supplies a bounded DOE FY2024 award-obligation sample with agency, recipient, date, amount, and NAICS/PSC metadata. An award obligation is not necessarily a cash settlement or final supplier payment, and the federal financing source is not identified.
- The payer-resource join gate is `BLOCKED`: the frozen package now validates a BEA 1997 benchmark make/use and requirements structure, a BLS public-API industry-hours sample, and selected USGS material quantities. Only 11 of 202 predeclared NAICS4 candidates returned BLS rows, but those 11 returned series are complete for 1987-2024 (418 rows); 16 other candidate-batch requests remain unavailable because of the provider daily quota. USGS quantities are national and not industry-mapped, and SEC public-firm ratios cover only 10 firms from current-vintage 10-K facts. A project payment ledger remains unavailable. Aggregate energy throughput is present but is not a complete physical-resource ledger.

## Model and inference limitations

- `R=N+K+I` is a heuristic bridge through indexed proxies, not a dimensional identity or law.
- Equal weights, base year, horizons, and proxy choices are predeclared benchmark policy, not
  fitted constants or first-principles derivations.
- Rolling-origin forecasts are internal temporal diagnostics. They are not external validation,
  structural estimates, or causal identification.
- The 1971-1973 exclusion makes pre/post summaries descriptive; it does not identify the Nixon
  Shock, fiat regime, or any intervention effect.
- The small pre-1971 sample (`n=11`) limits regime comparison precision.
- The candidate signal is false at all tested horizons. A negative or mixed result is retained;
  it is not tuned away.
- No social-power, strategy, policy, or Nash-equilibrium lane is calibrated to real intervention
  data or accepted as evidence.

## Claim restrictions

Do not export the current package as evidence that:

- an economic law has been proved or verified;
- fiat currency caused inflation, wage divergence, or wealth transfer;
- gold, equities, or any asset is a validated scaling peg or superior store of value;
- a policy, strategy, social stabilizer, or Nash-equilibrium improvement is validated.

The aggregate research-architecture controller is the 12-gate WARN registry in
Data/03_Research/uet_economics_warn_gate_registry.json. Energy density remains a concrete
sub-lane blocker, while source/revision/license/unit/measurement/missingness/leakage,
baseline, causal, external, and publication gates also remain open for Evidence Grade A.
Closing one gate would not by itself raise Claim Class C or establish causality.
