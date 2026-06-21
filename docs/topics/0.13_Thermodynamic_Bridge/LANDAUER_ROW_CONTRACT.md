# Landauer Row Contract

## Purpose

This file narrows the closure requirements for the active Landauer benchmark rows
that matter most for current `0.13` hardening:

- `Berut 2012`
- `Jun 2014`
- `Hong 2016` candidate branch

The broader row-closure matrix is still useful, but these two rows deserve their own contract because they are the shortest path to improving the primary Landauer lane.

## Current authority

- Machine-readable contract: `Data/03_Research/landauer_row_contract.json`
- Supporting row blocker map: `ROW_CLOSURE_MATRIX.md`
- Supporting uncertainty files:
  - `Data/03_Research/uncertainty_preprocessing_manifest.json`
  - `Data/03_Research/uncertainty_propagation_summary.json`

## Why these rows

`Berut`, `Jun`, and `Hong` are the rows most directly tied to the current
Landauer-facing claim ceiling.

- `Berut` already has a propagated interval, but it is still only a topic-summary row
- `Jun` already has a summary-layer interval, but it still lacks final branch/file closure
- `Hong` now has preprint-visible candidate values, but it still lacks final-source confirmation and a closed replace/remove policy for the legacy runtime row

That means the rows now have different closure problems:

- `Berut` is blocked more by row-level provenance
- `Jun` is blocked more by branch/file identity
- `Hong` is blocked more by final-source confirmation of the provisionally preferred runtime target

## Minimum closure rule

A Landauer row should not be treated as closed for `0.13` unless it has:

1. a stable source identity
2. an explicit row or table locator
3. an explicit unit basis
4. a clear mapping from source row to runtime value
5. a source-backed uncertainty value if the row is being used for propagated-interval support

## Current row split

| Row | Main current strength | Main blocker |
| :-- | :-- | :-- |
| Berut 2012 | source identity plus summary value and propagated interval | missing row-level source locator and raw or machine-transcribed source row |
| Jun 2014 | source identity plus summary-layer interval | legacy-row split/relabel policy plus original-file or row identity |
| Hong 2016 candidate | DOI metadata anchor plus accessible preprint-level candidate values and provisional target policy | final-source confirmation for the preferred `4.2 +/- 0.9 zJ` target plus keep/replace/remove policy for the local `0.028 eV` row |

## Use rule

Use this contract when choosing the next Landauer-lane hardening step.
It is a closure-navigation tool, not a promotion artifact by itself.

