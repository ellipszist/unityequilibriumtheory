# Hong 2016 Numeric Mismatch Note

## Purpose

This file narrows the `0.13` legacy runtime-row problem one step further.

The current evidence no longer supports only a binary choice between:

- `Jun 2014` is correct
- `Hong 2016` is correct

There is now a second issue:

- secondary summaries for the staged `Hong 2016` branch point to about `0.026 eV` at `300 K`
- the local legacy runtime row still uses `0.028 eV`
- an accessible same-author preprint precursor now also exposes a larger room-temperature
  five-trial average near `0.038 eV`

So even if the row ultimately belongs to the `Hong 2016` family, the local runtime value
may still require replacement, a target-selection policy, or a different source-facing quantity.

## Current authority

- Machine-readable artifact: `Data/03_Research/hong_2016_numeric_mismatch_note.json`
- Supporting files:
  - `docs/data/external/thermodynamics/landauer/hong_2016/source_record.json`
  - `HONG_2016_SOURCE_LINEAGE_NOTE.md`
  - `Data/03_Research/experimental_data.py`
  - `docs/meta/core_verification_artifacts/0_13_thermodynamic_bridge_run_contract.json`

## Current reading

- `Hong 2016` remains only a staged candidate branch
- the candidate branch improves the source-family explanation for `Experimental (2016)` and `44% above limit`
- but the candidate branch does not yet explain why the local runtime row is `0.028 eV` instead of the currently visible secondary `~0.026 eV` wording

What the current primary-facing surfaces do and do not add:

- the archived `Crossref` work record confirms a qualitative abstract summary:
  the measured switching energy is consistent with the Landauer limit of `k_B T ln(2)`
- an accessible same-author preprint precursor now exposes two source-facing quantities:
  `6.09 +/- 1.43 zJ` for a room-temperature five-trial average and `4.2 +/- 0.9 zJ`
  for a separate temperature-series mean
- those convert to about `0.0380 +/- 0.0089 eV` and `0.0262 +/- 0.0056 eV`, respectively
- so the current blocker is no longer only `0.026 eV` versus `0.028 eV`; it is also
  which Hong statistic the repo intends to compare against the runtime row
- the publisher article-page route is known, but still returns `403` with a Cloudflare
  challenge even when probed with a browser-like user agent
- the publisher PDF route is known, but the current environment hits `403` with a
  Cloudflare challenge before numeric extraction can be attempted from that surface

What the current verifier arithmetic implies:

- the current `0.13` verifier uses a `300 K` Landauer baseline of about `0.017919 eV`
- if the phrase `44% above limit` is taken literally against that baseline, the implied
  value is about `0.025804 eV`
- that implied value is close to the visible secondary `~0.026 eV` wording
- that implied value is also close to the preprint temperature-series mean
  `4.2 +/- 0.9 zJ -> ~0.0262 +/- 0.0056 eV`
- it is not close to the preprint room-temperature five-trial average
  `6.09 +/- 1.43 zJ -> ~0.0380 +/- 0.0089 eV`
- the local legacy runtime row `0.028 eV` corresponds instead to about `56.26% above`
  the current verifier baseline

This does not close the Hong row.
It only means that the current repository arithmetic is more compatible with the
`~0.026 eV / 44% above limit` pair and the preprint temperature-series mean than with
the local `0.028 eV / 44% above limit` pair, while also showing that another Hong-side
preprint statistic exists near `0.038 eV`.

## Minimum closure rule

Do not move the legacy runtime row into a closed `Hong 2016` lane unless the topic package has:

1. one primary article page or DOI for the Hong paper
2. one declared choice of which Hong-side quantity actually matches the runtime comparison target
3. one declared rule explaining whether `~0.026 eV`, `0.028 eV`, `~0.038 eV`, or another quantity is the correct row value
4. one source-backed uncertainty attached to that same chosen quantity
5. one propagated interval in the same runtime unit basis

## Current claim boundary

While this mismatch remains open, the staged `Hong 2016` branch may support only:

- candidate source-family context for the `Experimental (2016)` wording, plus a
  narrower statement that the current source family exposes multiple plausible Hong-side
  quantities and that the `~0.026 eV` wording is better supported than `0.028 eV`

It must not support:

- a claim that the local `0.028 eV` runtime row already matches the `Hong 2016` numeric target
- a claim that the row has already been successfully reassigned away from `Jun 2014`

## Use rule

Use this note when deciding whether the next pass should focus on:

- primary DOI/article-page capture
- exact numeric-target selection from the Hong source family
- or runtime-row replacement/splitting policy

It is a blocker-navigation note, not a promotion artifact.
