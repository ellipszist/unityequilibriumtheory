# Verification Spec

## Primary Command

```powershell
python docs/topics/0.19_Gravity_GR/Code/03_Research/Research_G_Constant.py
```

## Inputs

| Input | Role | Required identity |
| :-- | :-- | :-- |
| `Data/03_Research/codata_2018_gravity.json` | CODATA 2018 constants working copy | SHA256 and DOI recorded in artifact |
| `Code/01_Engine/Engine_Gravity_GR.py` | Engine constant package and Planck-unit definitions | Formula IDs `GR19-CONSTANT-PACKAGE`, `GR19-PLANCK-UNITS` |

## Metrics

- `G_engine`
- `G_codata`
- relative error percent
- threshold percent, based on CODATA relative uncertainty with a minimum numerical tolerance
- Planck length/time/mass values derived from the engine constants

## Fixed Threshold

| Metric | PASS threshold |
| :-- | :-- |
| Relative error between `G_engine` and `G_codata` | `<= max(CODATA relative uncertainty percent, 0.0001%)` |

## Artifact Target

- `Result/artifacts/0_19_gravity_gr_verification.json`
- `Data/03_Research/source_evidence_intake_stub.json`
- `Data/03_Research/source_evidence_readiness_matrix.json`
- `Data/03_Research/branch_claim_gate.json`

The artifact must record:

- PASS/FAIL status and claim class
- command and timestamp
- dataset path, SHA256, source, and DOI
- formula IDs
- threshold and metrics
- machine-readable `gravity_claim_scope_gate.controller_status`
- limitations

## Interpretation

A PASS supports only a Claim Class C internal source-constant checkpoint. It does not derive `G`, validate general relativity, prove the equivalence principle, predict light bending/perihelion precession, or resolve singularities.
Topic-level source-evidence and branch-claim gates further limit this topic to constants and derived-unit checkpoint usage unless dedicated GR artifacts are added.
`gravity_claim_scope_gate.controller_status == WARN` is expected when the CODATA checkpoint passes while G derivation, weak-field validation, MICROSCOPE eta comparison, Eot-Wash comparison, Einstein-equation, singularity, and quantum-gravity branches remain open.
