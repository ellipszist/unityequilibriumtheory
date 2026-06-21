# Hong 2016 Runtime Target Policy

## Purpose

This file records the current conservative topic-level policy for deciding which
visible `Hong 2016` quantity best matches the inherited legacy runtime wording:

- `Experimental (2016)`
- `44% above limit`
- `~0.026 eV` style summaries
- local legacy runtime value `0.028 eV`

The point is not to force closure.
The point is to stop the branch from staying ambiguous now that multiple
source-facing Hong-side quantities are visible in the accessible same-author
preprint precursor.

## Current authority

- Machine-readable artifact:
  `Data/03_Research/hong_2016_runtime_target_policy.json`
- Supporting files:
  - `HONG_2016_NUMERIC_MISMATCH_NOTE.md`
  - `HONG_2016_SOURCE_ACQUISITION_BLOCKER.md`
  - `HONG_2016_SOURCE_LINEAGE_NOTE.md`
  - `docs/data/external/thermodynamics/landauer/hong_2016/source_record.json`

## Current reading

The accessible same-author precursor `arXiv:1411.6730` exposes at least two
Hong-side dissipation summaries:

- room-temperature five-trial average:
  `6.09 +/- 1.43 zJ` -> about `0.0380 +/- 0.0089 eV`
- separate temperature-series mean:
  `4.2 +/- 0.9 zJ` -> about `0.0262 +/- 0.0056 eV`

Under the current `0.13` verifier baseline, the inherited phrase `44% above
limit` implies about `0.025804 eV`.

That means the current best fit to the inherited legacy runtime narrative is:

- provisionally prefer the `4.2 +/- 0.9 zJ` temperature-series mean

and not:

- the `6.09 +/- 1.43 zJ` room-temperature five-trial average
- the local legacy `0.028 eV` row as-is

## Current claim boundary

This policy may support only:

- a provisional topic-level decision about which visible Hong-side quantity best
  matches the inherited `2016 / 44% above limit / ~0.026 eV` narrative

It must not support:

- a claim that the `Hong 2016` branch is now source-closed
- a claim that `0.028 eV` is now justified
- a claim that the final publisher article has already been confirmed to use the
  same target statistic

## Next move

The next best action is:

1. keep the provisional preferred target as `4.2 +/- 0.9 zJ`
2. seek final-source confirmation for that exact quantity
3. then decide whether the legacy `0.028 eV` row should be replaced, rounded,
   or removed
