# Legacy Claim Surface Audit

## Purpose

This file tracks legacy `0.13` surfaces whose wording can outrun the current claim ceiling.

It is not a scientific result.
It is a claim-discipline control file.

## Current rule

The authority for allowed `0.13` claims remains:

- `README.md`
- `METHOD.md`
- `LIMITATIONS.md`
- `VERIFICATION_SPEC.md`
- `FORMULA_AUDIT.md`
- `Result/artifacts/0_13_thermodynamic_bridge_verification.json`

## High-risk surfaces

| Surface | Risk type | Current action |
| :-- | :-- | :-- |
| `Code/README.md` | older summary language overstates proof/validation strength | downgraded to legacy code map with explicit boundary |
| `Code/03_Research/Research_Thermodynamic_Bridge.py` | calls itself foundational/most important and presents bridge verification language | downgraded to legacy integration script |
| `Code/03_Research/Research_Real_Data_Validation.py` | states beta*C*I term has thermodynamic basis as if this were current status | downgraded to legacy diagnostic script |
| `Ref/BIBLIOGRAPHY_ANALYSIS.md` | narrative language claims first-principles derivation and “proved” phrasing | retained as legacy bibliography note only |
| `Data/03_Research/berut_2012.json` | working-copy field says Landauer limit verified experimentally | changed to conservative lower-bound wording |
| `Data/landauer/berut_2012.json` | duplicate legacy working-copy field repeats the same overclaim | changed to conservative lower-bound wording |

## What still remains

- Many `Doc/keed/` legacy notes already carry warning banners, but they may still contain strong internal prose below the banner.
- Legacy research scripts may still print strong phrasing during interactive runs even after header cleanup.
- Any future migration should prefer boundary artifacts over large-scale prose rewrites unless a file is actively being used.

## Use rule

If a legacy surface conflicts with the current verifier artifact, the verifier artifact wins.
