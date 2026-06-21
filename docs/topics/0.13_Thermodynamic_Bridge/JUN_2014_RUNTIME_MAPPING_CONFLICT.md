# Jun 2014 Runtime Mapping Conflict

## Purpose

This file isolates a narrower `Jun 2014` blocker than the existing uncertainty-gap note.

The problem is no longer only that the topic package lacks a source-backed uncertainty field.
There is also a runtime-to-source mapping conflict:

- the current local runtime row uses `0.028 eV`
- the `Jun 2014` source identity points to `High-Precision Test of Landauer's Principle in a Feedback Trap`
- the source-facing summary visible in the current archived preprint shows an asymptotic full-erasure work of about `0.71 +/- 0.03 kT`, with statistical errors around `+/- 0.10 kT` for the mean-work measurements
- using the current `0.13` verifier's `300 K` baseline, that asymptotic `Jun 2014` quantity corresponds to about `0.01836 +/- 0.00078 eV`, with a statistical measurement scale of about `0.00259 eV`

This means the blocker is now narrower and stronger than a generic missing conversion note: under the current verifier baseline, the pinned `Jun 2014` asymptotic-work quantity does not numerically match the legacy `0.028 eV` runtime row.

Until the topic package explains why a different `Jun 2014` quantity should control the runtime row, or else removes/splits that row from the `Jun` branch, the uncertainty blocker cannot honestly be treated as only a missing error-bar field.

## Current authority

- Machine-readable artifact: `Data/03_Research/jun_2014_runtime_mapping_conflict.json`
- Supporting files:
  - `docs/data/external/thermodynamics/landauer/jun_2014/source_record.json`
  - `JUN_2014_UNCERTAINTY_GAP.md`
  - `Data/03_Research/source_evidence_intake_stub.json`
  - `Data/03_Research/source_evidence_readiness_matrix.json`

## Current runtime state

- local runtime value: `0.028 eV`
- local lower-bound comparator at `300 K`: `0.0179192407638041 eV`
- current source identity: `Phys. Rev. Lett. 113, 190601 (2014)`
- current mapping status: unresolved, but now with a concrete quantitative mismatch between the source-facing `0.71 kT` asymptotic-work summary and the legacy `0.028 eV` runtime row

## Minimum closure rule for this row

Do not treat `Jun 2014` as row-mapped unless the topic package has:

1. one declared decision on whether the legacy `0.028 eV` row stays in the `Jun` branch at all
2. if it stays, one exact source row, fit target, or other `Jun 2014` quantity that is not just the current asymptotic `0.71 kT` summary
3. one explicit unit basis for that chosen source quantity
4. one explicit conversion path from that source quantity into the runtime `eV` row
5. one source-backed uncertainty attached to the same quantity being converted
6. one propagated interval in the same runtime unit basis

## Current claim boundary

While this conflict remains open, `Jun 2014` may support:

- source identity plus summary-layer interval-bearing lower-bound context

It must not support:

- row-level source-normalized Jun closure
- any claim that the runtime `0.028 eV` row is already directly normalized to the pinned `Jun 2014` asymptotic-work quantity

## Use rule

Use this file when deciding whether the next Jun pass is:

- legacy-row split/replacement
- source-row identification for a different Jun quantity, if one exists
- unit/conversion reconstruction
- or uncertainty propagation after the branch identity is cleaned up

It is a blocker-navigation note, not a promotion artifact.
