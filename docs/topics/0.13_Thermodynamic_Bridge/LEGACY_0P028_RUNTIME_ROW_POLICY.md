# Legacy 0.028 eV Runtime Row Policy

## Purpose

This file records the current conservative handling policy for the inherited
`0.028 eV` runtime row in topic `0.13`.

The question is not whether the row once appeared in local runtime surfaces.
The question is whether it should still count as an active benchmark row while
the `Jun` and `Hong` branches remain open.

## Current authority

- Machine-readable artifact:
  `Data/03_Research/legacy_0p028_runtime_row_policy.json`
- Supporting files:
  - `JUN_2014_RUNTIME_MAPPING_CONFLICT.md`
  - `HONG_2016_RUNTIME_TARGET_POLICY.md`
  - `HONG_2016_NUMERIC_MISMATCH_NOTE.md`
  - `HONG_2016_SOURCE_LINEAGE_NOTE.md`

## Current reading

Current evidence supports all of the following at once:

- the pinned `Jun 2014` source-facing quantity is near `0.01836 eV`, not `0.028 eV`
- the staged `Hong 2016` branch now provisionally prefers a target near
  `0.0262 eV`, not `0.028 eV`
- the local `0.028 eV` row therefore remains mixed-lineage

That means the current safest policy is:

- do not keep `0.028 eV` as an active `Jun` benchmark row
- do not yet promote `0.028 eV` into an active `Hong` benchmark row
- retain it only as legacy mixed-lineage context until final-source confirmation

## Current claim boundary

While this policy remains open, the `0.028 eV` row may support only:

- legacy lower-bound context
- historical explanation for why the Jun/Hong cleanup lane exists

It must not support:

- active row-level Jun closure
- active row-level Hong closure
- uncertainty-aware source-normalized benchmark wording

## Next move

The next best action is:

1. confirm the provisionally preferred Hong target at the final-source layer
2. then explicitly replace or remove the legacy `0.028 eV` row from active
   benchmark logic
