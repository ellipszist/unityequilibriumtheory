# Legacy Doc Surface Inventory

## Purpose

This file tracks the legacy documentation surfaces under `Doc/` and `Doc/keed/` for topic `0.13`.

It is not a scientific result.
It is a documentation-control and claim-discipline file.

## Current rule

If any legacy note under `Doc/` or `Doc/keed/` conflicts with:

- `README.md`
- `METHOD.md`
- `LIMITATIONS.md`
- `VERIFICATION_SPEC.md`
- `FORMULA_AUDIT.md`
- `DATA_MANIFEST.md`
- `Result/artifacts/0_13_thermodynamic_bridge_verification.json`

then the root topic package and verifier artifact win.

## Inventory

| Surface | Current role | Current status |
| :-- | :-- | :-- |
| `Doc/ANALYSIS_01_Thermodynamics.md` | legacy thermodynamics interpretation note | bounded legacy note |
| `Doc/ANALYSIS_Engine_Thermodynamics.md` | legacy engine-analysis note | bounded legacy note |
| `Doc/ANALYSIS_Proof_Entropy_Max.md` | legacy proof-oriented note | bounded legacy note |
| `Doc/ANALYSIS_Thermodynamic_Bridge.md` | legacy bridge overview note | bounded legacy note |
| `Doc/ANALYSIS_Thermodynamic_Bridge_Research.md` | legacy research-summary note | bounded legacy note |
| `Doc/keed/ANALYSIS_01_Engine_Thermo.md` | legacy engine-analysis note | bounded legacy note |
| `Doc/keed/ANALYSIS_03_Bridge_Logic.md` | legacy bridge-logic note | bounded legacy note |
| `Doc/keed/ANALYSIS_03_Data_Loader.md` | legacy utility/provenance note | bounded legacy note |
| `Doc/keed/ANALYSIS_03_Landauer.md` | legacy Landauer orientation note | bounded legacy note |
| `Doc/keed/ANALYSIS_03_Real_Data.md` | legacy mixed-benchmark note | bounded legacy note |
| `Doc/keed/03_Research/analysis.md` | legacy conversion-rate/bridge framing note | bounded legacy note |
| `Doc/keed/03_Research/before.md` | legacy motivation note | bounded legacy note |
| `Doc/keed/03_Research/Final_Paper_Bekenstein.md` | legacy Bekenstein-facing paper note | bounded legacy note |
| `Doc/keed/03_Research/Final_Paper_Jacobson.md` | legacy Jacobson-facing paper note | bounded legacy note |
| `Doc/keed/03_Research/Final_Paper_Landauer.md` | legacy Landauer-facing paper note | bounded legacy note |
| `Doc/keed/03_Research/result_summary.md` | legacy execution-summary note | bounded legacy note |
| `Doc/keed/03_Research/solution.md` | legacy Bekenstein-bound framing note | bounded legacy note |

## Meaning of "bounded legacy note"

A file counted as a bounded legacy note should:

- carry an explicit warning that it is not the current topic authority
- defer claim scope to the root topic package and verifier artifact
- avoid presenting itself as proof, final validation, source-lock closure, or completed derivation
- remain useful only as historical framing, orientation, or limited conceptual context

## What still remains

- This inventory controls doc-surface interpretation, not scientific closure.
- Topic-level blockers remain unchanged: source-normalized Landauer rows, fuller uncertainty closure, and a non-circular UET bridge derivation are still open.
- Future sweeps should update this file if new legacy notes are added or if any historical note is promoted, deleted, or replaced.
