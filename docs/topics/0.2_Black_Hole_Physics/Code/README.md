# Topic 0.2: Black Hole Physics - Code

This folder contains black-hole engine, proof, research, competitor, and visualization
scripts. The current primary verifier is an internal EHT shadow-size benchmark. It does not
prove singularity resolution, replace GR, validate EHT images, validate ringdown physics,
or prove CCBH cosmological coupling.

## 5x4 Structure

```text
Code/
  01_Engine/
    Engine_BlackHole.py              # Saturation-core diagnostic engine
  02_Proof/
    Proof_Singularity_Resolution.py  # Potential-minimum diagnostic check
  03_Research/
    Research_EHT_Validation.py       # Primary selected EHT shadow-size benchmark
    Research_CCBH_Analysis.py        # Blocked until upstream data are archived
    Research_GW_Validation.py        # Diagnostic branch; not primary-gated
    Research_Singularity_Sweep.py    # Heuristic saturation-core sweep
  04_Competitor/
    Competitor_GR_Benchmark.py       # GR comparator bookkeeping
```

## Run Commands

```powershell
cd c:\Users\santa\Desktop\uet_harness

python docs/topics/0.2_Black_Hole_Physics/Code/03_Research/Research_EHT_Validation.py
python docs/topics/0.2_Black_Hole_Physics/Code/01_Engine/Engine_BlackHole.py
python docs/topics/0.2_Black_Hole_Physics/Code/02_Proof/Proof_Singularity_Resolution.py
python docs/topics/0.2_Black_Hole_Physics/Code/03_Research/Research_CCBH_Analysis.py
python docs/topics/0.2_Black_Hole_Physics/Code/03_Research/Research_GW_Validation.py
python docs/topics/0.2_Black_Hole_Physics/Code/03_Research/Research_Singularity_Sweep.py
python docs/topics/0.2_Black_Hole_Physics/Code/04_Competitor/Competitor_GR_Benchmark.py
```

## Current Verification Status

Current authority: `../Result/artifacts/0_2_black_hole_physics_verification.json` and
`../VERIFICATION_SPEC.md`.

| Lane | Evidence | Current status | Claim boundary |
|:--|:--|:--|:--|
| EHT shadow-size benchmark | M87* and Sgr A* compact `5.2 R_s` comparison | `PASS` | Selected internal benchmark only |
| Comparator geometry | Schwarzschild radius and GR shadow approximation | `COMPARATOR_ONLY` | Bookkeeping, not UET replacement dynamics |
| Claim-scope controller | `black_hole_claim_scope_gate` | `WARN` | Export remains warning-gated |
| Source evidence | topic-local working copy | `OPEN` / blocked | Not a full normalized upstream archive |
| Saturation-core / singularity branch | heuristic engine and sweep diagnostics | `BLOCKED` for proof claims | physical core scale and artifact gate missing |
| GW/ringdown and CCBH branches | scripts exist | `BLOCKED` for strong claims | upstream archives, thresholds, and primary artifacts missing |

## Data Sources

- EHT M87* / Sgr A* working-copy data in `../Data/03_Research/`
- Shen et al. 2011 and Farrah et al. 2023 are relevant to CCBH work, but the CCBH branch
  is blocked until upstream files are archived and hashed under `docs/data/external/...`.
- GW150914/LIGO references are diagnostic context only until a source-backed ringdown
  verifier and thresholds exist.

## Engine / Proof Analysis

The saturation-core engine and potential-minimum proof are useful for mechanism
development, but they do not override the artifact-level claim gate. The current artifact
allows selected EHT shadow-size benchmark claims and GR-style comparator bookkeeping only.

## Claim Boundary

Allowed now:

- selected internal EHT shadow-size benchmark within the declared 2-sigma gate
- compact GR shadow geometry as comparator bookkeeping
- heuristic saturation-core diagnostics as proposed mechanism work

Blocked now:

- black-hole singularity resolved
- GR replacement validated
- EHT image-domain validation
- ringdown validated
- CCBH cosmological coupling proven
- black-hole information problem solved

## Key Physics

```text
Potential: V(r) = -GM/r + (beta * GM * R_core) / r^2
Shadow comparator: D_shadow = 5.2 R_s
Entropy law: E_rad = (ln 2 / pi) * T_H * Delta_S
```

See `../FORMULA_AUDIT.md` for formula roles, proof status, and failure modes.
