# Hong 2016 Source Lineage Note

## Purpose

This file records a narrower provenance risk inside the current `0.13` Landauer lane:
the legacy runtime value `0.028 eV` now appears more consistent with a later
nanomagnetic-memory experiment narrative than with the currently pinned
`Jun 2014` feedback-trap source identity.

This is not yet a closed source-lock artifact.
It is a conservative lineage note that keeps the runtime row from being treated
as if it only needed a missing `Jun 2014` uncertainty field.

## Why this note exists

Current local evidence shows all of the following at once:

- the pinned `Jun 2014` source identity is `High-Precision Test of Landauer's Principle in a Feedback Trap`
- the current archived `Jun 2014` source-facing summary is expressed in `kT`
- the legacy runtime surface still uses `0.028 eV`
- old runtime wording also says `44% above limit` and even labels the point as `Experimental (2016)`

That mixed wording is difficult to reconcile with a clean `Jun 2014` row-level mapping.
It is more consistent with the possibility that the legacy `0.028 eV` row inherited
part of a later nanomagnetic-memory benchmark branch.

## Current authority

- Machine-readable artifact: `Data/03_Research/hong_2016_source_lineage_note.json`
- Supporting files:
  - `Data/03_Research/experimental_data.py`
  - `Code/03_Research/Research_Landauer.py`
  - `JUN_2014_RUNTIME_MAPPING_CONFLICT.md`
  - `docs/data/external/thermodynamics/landauer/jun_2014/source_record.json`
  - `docs/data/external/thermodynamics/landauer/hong_2016/source_record.json`
  - `docs/meta/core_verification_artifacts/0_13_thermodynamic_bridge_run_contract.json`

## Current reading

- `Jun 2014` remains the pinned source identity for the feedback-trap branch
- the runtime `0.028 eV` row is not currently trustworthy as a clean `Jun 2014` row
- the old `44% above limit` wording is now best treated as a cross-source lineage warning
- a candidate `Hong 2016` source record now exists, and an accessible same-author preprint precursor now exposes Hong-side numeric candidates
- but final-source capture and runtime-target selection are still open
- until the `Hong 2016` source package is upgraded beyond source-record-only status, this note stays at the level of
  a likely lineage conflict, not a closed reassignment

## Minimum closure rule

Do not relabel the runtime row as `Hong 2016` or restore it as a clean `Jun 2014` row
unless the topic package has:

1. one exact upstream paper identity for the `0.028 eV` branch
2. one declared choice of which explicit Hong-side source-facing quantity or row is the intended branch target
3. one archived unit basis and conversion path into the runtime `eV` row
4. one source-backed uncertainty attached to the same quantity
5. one update to the main Landauer row contract and source-evidence workflow files

## Current claim boundary

While this note remains open, the legacy `0.028 eV` row may support only:

- lower-bound context for a legacy summary value with mixed lineage

It must not support:

- a clean `Jun 2014` source-mapped benchmark claim
- a clean `Hong 2016` source-mapped benchmark claim
- an uncertainty-aware row closure claim for either branch

## Use rule

Use this note when deciding whether the next hardening move is:

- a `Jun 2014` cleanup pass
- a `Hong 2016` source-intake pass
- or a relabel/split of the current runtime row

It is a blocker-navigation note, not a promotion artifact.
