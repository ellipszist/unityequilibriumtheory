# Topic 0.25 Research Code

This directory contains exploratory strategy simulations and the source-locked Book 1 economics
hardening lane. The two are separate evidence classes.

## Book 1 hardening scripts

| Script | Role | Output |
| :-- | :-- | :-- |
| `Research_UET_Economics_External_Source_Transform.py` | download/parse official BEA/EIA files and a provider-supplied EPI chart export | raw-cache hashes and transform manifest |
| `Research_UET_Economics_Source_Package.py` | lock source identity, terms, units, coverage, and hashes | source/formula/parameter/holdout/claim gates |
| `Research_UET_Economics_Panel.py` | annualize FRED, validate coverage, construct indexed proxies, reject imputation | normalized panel and panel-status gate |
| `Research_UET_Resource_Equation_Audit.py` | test the predeclared `R/N/K/I` diagnostic and rolling-origin candidate rule | resource artifact |
| `Research_Stone_Balloon_Audit.py` | test monetary-resource mismatch and inflation baselines; gate assets | Stone artifact |
| `Research_Energy_Density_Audit.py` | separate throughput history from literal density definition | energy artifact |
| `Research_Wage_Productivity_Audit.py` | reproduce EPI chart construction and report BLS separately | wage artifact |
| `Verify_UET_Economics_Hardening.py` | execute and aggregate all lanes; fail on subcommand errors and missing legacy boundary warnings | aggregate verifier artifact |

## Rerun

```powershell
cd C:\Users\santa\Desktop\uet_harness
.\.venv\Scripts\python.exe docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Research_UET_Economics_External_Source_Transform.py --vintage 2026-07-12 --epi-csv <provider-export.csv>
.\.venv\Scripts\python.exe docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Research_UET_Economics_Source_Package.py --vintage 2026-07-12
.\.venv\Scripts\python.exe docs/topics/0.25_Strategy_Power_Economics/Code/03_Research/Verify_UET_Economics_Hardening.py
```

## Evidence boundary

A `PASS` source or panel gate means only that the declared input contract is present. A
`DIAGNOSTIC_COMPLETE` artifact means the predeclared comparison ran. Neither status supports
claims of economic-law confirmation, fiat causality, policy validation, asset superiority, or
strategic superiority. The current aggregate is intentionally `WARN` because the literal
energy-density and architecture WARN gates remain open.

The older engine/proof/research scripts remain exploratory model proposals and are not included
in the Book 1 primary panel.

The verifier also embeds the preregistered research register, variable dictionary, causal DAG,
claim matrix, and 12-gate WARN registry from Data/03_Research. These contracts define the
ten-wave path from Package Tier A to the Evidence Grade A target; they do not change the
current Claim Class C boundary.
