# UET v0.8.5 – Tier3 Stress Pack

This pack adds:

- `matrices/UET_v0_8_5_pre_Tier3_STRESS_matrix.csv` (lots of PASS-expected stress tests)
- `matrices/UET_v0_8_5_pre_Tier3_FAIL_HARD_matrix.csv` (FAIL-expected "prove the checker works" tests)
- `scripts/plot_tier3_dashboard.py` (quick plots from a ledger)
- `scripts/validate_expected_failures.py` (makes sure FAIL-expected really FAIL)

## Quick run (PowerShell)

From harness root (`uet_harness_v0_1/`):

```powershell
# 1) Stress (should mostly PASS, unless you found a real instability)
python scripts/run_suite.py --matrix matrices/UET_v0_8_5_pre_Tier3_STRESS_matrix.csv --out runs_tier3

# 2) Hard FAIL (should FAIL on purpose)
python scripts/run_suite.py --matrix matrices/UET_v0_8_5_pre_Tier3_FAIL_HARD_matrix.csv --out runs_tier3_fail

# 3) Validate FAIL expectations
python scripts/validate_expected_failures.py --matrix matrices/UET_v0_8_5_pre_Tier3_FAIL_HARD_matrix.csv --ledger runs_tier3_fail/ledger.csv

# 4) Dashboard plots
python scripts/plot_tier3_dashboard.py --ledger runs_tier3/ledger.csv --out reports/tier3_dashboard
```

If the validator says some FAIL-expected case did **not** fail, that is the *best kind* of bug: it means your guardrails/checks are not catching what you think they catch.
