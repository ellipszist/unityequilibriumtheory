# Topic 0.5: Nuclear Binding and Hadrons - Code

This folder contains nuclear-binding, hadron, QCD-bridge, proof, research, and competitor
scripts. The current primary verifier is the source-locked selected-subset nuclear-binding
gate plus proton-radius anchor check. It is not a complete strong-force theory, QCD
derivation, hadron-mass validation, or confinement proof.

## 5x4 Structure

```text
Code/
  01_Engine/
    Engine_Nuclear_Binding.py      # Binding-energy engine used by strict verifier
    Engine_Hadron_Model.py         # Diagnostic hadron branch
    Engine_Light_Nuclei.py         # Light-nuclei diagnostic branch
    Engine_QCD_Bridge.py           # QCD bridge diagnostic branch
  02_Proof/
    Proof_Color_Confinement.py     # Legacy proof script; audit-grade gate still open
  03_Research/
    Research_Nuclear_Binding_SourceLocked.py       # Primary strict gate
    Research_Nuclear_Binding_FullTable_Diagnostic.py # Full-table diagnostic
    Research_Nuclear_Binding.py                    # Legacy/older benchmark path
    Research_Strong_Force.py                       # Diagnostic strong-force branch
    Research_Proton_Radius.py                      # Proton-radius anchor branch
    Research_QCD_Running.py                        # QCD running branch; blocked for export
    Research_Quark_Masses.py                       # Quark-mass diagnostic branch
  04_Competitor/
    Competitor_Nuclear_Baseline.py # SEMF/comparator work
```

## Run Commands

```powershell
cd c:\Users\santa\Desktop\uet_harness

$env:PYTHONIOENCODING='utf-8'; $env:PYTHONUTF8='1'
.\.venv\Scripts\python.exe docs\topics\0.5_Nuclear_Binding_Hadrons\Code\03_Research\Research_Nuclear_Binding_SourceLocked.py
.\.venv\Scripts\python.exe docs\topics\0.5_Nuclear_Binding_Hadrons\Code\03_Research\Research_Nuclear_Binding_FullTable_Diagnostic.py
```

Additional diagnostic scripts can be run from the same topic folder, but their results do
not override the primary artifact claim gate.

## Current Verification Status

Current authority: `../Result/artifacts/nuclear_binding_source_locked_validation.json` and
`../VERIFICATION_SPEC.md`.

| Lane | Evidence | Current status | Claim boundary |
|:--|:--|:--|:--|
| Heavy-nucleus selected subset | raw-derived AME2020 subset, `A >= 16` gate | `PASS` | Internal selected-subset benchmark only |
| Proton-radius anchor | source-backed local benchmark | `PASS` | Benchmark-anchor compatibility, not independent prediction |
| Full AME2020 table | parsed table diagnostic | `DIAGNOSTIC_ONLY` | Not a full-table pass |
| Light nuclei | H2, He4, C12 excluded from heavy gate | `EXCLUDED_FROM_PASS` | Cannot inherit heavy-nucleus PASS |
| QCD / hadron / confinement | branch gate | `BLOCKED` | No QCD derivation, hadron validation, or formal confinement proof |
| Claim-scope controller | `nuclear_claim_scope_gate` | `WARN` | Export remains limited to selected benchmark lanes |

## Data Sources

- AME2020 raw table under `docs/data/external/particle_physics/ame2020/`
- Topic-local selected subset and parsed-table artifacts under `../Data/03_Research/`
- Proton-radius benchmark data under `../Data/03_Research/Data_Proton_Radius.json`
- PDG quark and hadron/QCD constants remain lower-readiness branches until source-locked at
  the same standard.

## Engine / Proof Analysis

`Engine_Nuclear_Binding.py` is the active strict-gate engine surface. The confinement proof,
QCD running, hadron-mass, and light-nuclei scripts remain useful research branches, but they
do not currently export strong claims.

## Claim Boundary

Allowed now:

- source-backed selected heavy-nucleus subset benchmark
- proton-radius anchor compatibility check
- full-table parsing as diagnostic coverage

Blocked now:

- full AME2020 nuclear-binding pass
- light-nuclei validation
- general QCD derivation
- hadron mass model validation
- formal confinement proof
- complete strong-force theory

## Key Physics

```text
E_binding = V_volume + V_surface + V_coulomb + V_asymmetry + V_yukawa
```

See `../FORMULA_AUDIT.md` for formula roles, proof status, and failure modes.
