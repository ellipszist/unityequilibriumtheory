# Variable Dictionary — Topic 0.25 Economics

The canonical machine-readable dictionary is
[`uet_economics_variable_dictionary.json`](Data/03_Research/uet_economics_variable_dictionary.json).

## Construct policy

`R`, `N`, `K`, and `I` are indexed operationalizations, not directly observed economic
quantities. Provider units remain in the source manifest; rebasing, log differences,
standardization, deflators, and PPP choices are recorded before a quantity enters a model.
Primary evidence never silently imputes missing observations.

| Construct | Primary operationalization | Robustness families | Current status |
|---|---|---|---|
| `R` resource capacity | geometric index of real GDP/person, output/hour, primary energy/person | standardized additive index; PCA/latent factor | heuristic proxy |
| `N` necessity/constraint | standardized energy-price inflation plus unemployment | food/energy/housing stress; stress factor | explicit proxy, not biological measurement |
| `K` knowledge | real intellectual-property investment per worker | patents/person; R&D/worker | proxy family required |
| `I` infrastructure | real tangible nonresidential assets per worker | government assets/worker; combined index | proxy family required |
| `M` money | M2 December level | annual-average M2; broad money; credit | source-locked U.S. baseline |
| welfare | real median disposable income | housing/food/energy burden; regional panel | Wave 3 pending |
| wage gap | separate EPI and BLS constructions | ILOSTAT/OECD global comparators | source comparison only |
| energy density | heat content per mass/volume | source mix, efficiency, carbon intensity | blocked until common basis |
| asset retention | licensed real total-return paths | gold, Treasuries, cash, housing, CRSP | license gate open |

See the JSON dictionary for source candidates, units, benchmark roles, and revision status.
