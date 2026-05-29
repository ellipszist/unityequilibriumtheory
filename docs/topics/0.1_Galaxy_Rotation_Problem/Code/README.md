# Topic 0.1: Galaxy Rotation Problem - Code

This folder runs internal UET galaxy-rotation experiments against repository working-copy
galaxy data. The current primary artifact is a summary-row benchmark, not a full SPARC
curve replication or a dark-matter replacement result.

- Information-field coupling appears through topic-specific gamma/bridge terms.
- Current bridge constants and scaling anchors remain heuristic until derivation or
  sensitivity audits close.

## 5x4 Structure

```text
Code/
  01_Engine/
    Engine_Galaxy_V3.py            # Main solver used by the current benchmark
  02_Proof/
    Proof_Unity_Density_Law.py     # Symbolic flat-curve check
  03_Research/
    Research_Galaxy_Rotation.py    # Primary 154-row summary benchmark
    Research_Dwarf_Galaxies.py     # LITTLE THINGS diagnostic branch
    Research_Alpha_Learning.py     # Exploratory alpha-law discovery tool
    Research_Residual_Analysis.py  # Residual diagnostic
```

## Run Commands

```powershell
cd c:\Users\santa\Desktop\uet_harness

python docs/topics/0.1_Galaxy_Rotation_Problem/Code/03_Research/Research_Galaxy_Rotation.py
python docs/topics/0.1_Galaxy_Rotation_Problem/Code/03_Research/Research_Dwarf_Galaxies.py
python docs/topics/0.1_Galaxy_Rotation_Problem/Code/01_Engine/Engine_Galaxy_V3.py
python docs/topics/0.1_Galaxy_Rotation_Problem/Code/02_Proof/Proof_Unity_Density_Law.py
python docs/topics/0.1_Galaxy_Rotation_Problem/Code/03_Research/Research_Alpha_Learning.py
python docs/topics/0.1_Galaxy_Rotation_Problem/Code/03_Research/Research_Residual_Analysis.py
python docs/topics/0.1_Galaxy_Rotation_Problem/Code/04_Competitor/Competitor_NFW.py
```

## Current Verification Status

Current authority: `../Result/artifacts/galaxy_rotation_validation.json` and
`../VERIFICATION_SPEC.md`.

| Lane | Evidence | Current status | Claim boundary |
|:--|:--|:--|:--|
| Run contract | `Research_Galaxy_Rotation.py` processed 154 rows | `PASS` | Verifier ran on the checked-in working copy |
| Summary-row model gate | average error about `61.4%`, pass rate `0%` | `FAIL` | Model residual blocker remains open |
| Source lock | working-copy summary rows | `OPEN` | Not full upstream SPARC archive replication |
| Baselines | competitor code exists, but no same-row artifact gate | `OPEN` | No MOND/dark-matter superiority claim |
| Replacement / closure claims | `galaxy_claim_scope_gate` | `BLOCKED` | No dark-matter replacement or galaxy-closure wording |

## Data Sources

- SPARC reference: Lelli et al. 2016, DOI `10.3847/1538-3881/152/6/157`
- LITTLE THINGS reference: Hunter et al. 2012, DOI `10.1088/0004-6256/144/5/134`

The checked-in SPARC-like package is a repository working copy. Do not describe it as the
full upstream SPARC release until source identity, row semantics, radial curve arrays, and
preprocessing hashes are closed.

## Engine / Proof Analysis

Uses `Engine_Galaxy_V3.py` with heuristic bridge terms documented in `../FORMULA_AUDIT.md`.
The current artifact keeps the model-residual gate blocked.

- Engine work remains useful because it is the active implementation surface for the
  internal benchmark.
- Symbolic proof work remains useful for theoretical grounding, but symbolic flat-curve
  checks do not override the failed residual gate.

## Claim Boundary

Allowed now:

- The repository verifier runs over a 154-row summary working copy.
- The current artifact reports a model-residual blocker.
- Existing formulas and bridge constants remain heuristic until derivation or sensitivity
  audits close.

Blocked now:

- dark-matter replacement
- full SPARC replication
- galaxy-rotation problem solved
- zero curve fitting
- out-of-sample prediction validation
- MOND/dark-matter superiority

## Key Physics

```text
v^2 = G * (M_b + M_I) / r
M_I = M_b * (rho / rho_unity)^(-gamma)
```

See `../FORMULA_AUDIT.md` for current formula role, origin, and failure modes.
