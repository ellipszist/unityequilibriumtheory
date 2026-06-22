# Jun 2014 Source Summary Locator

## Purpose

This file records the exact source-summary surface behind the active `Jun 2014` summary interval used by the `0.13` verifier.

## Current Locator

- Source: `High-precision test of Landauer's principle in a feedback trap`
- DOI: `10.1103/PhysRevLett.113.190601`
- Primary-facing surface currently used: `arXiv:1408.5089`
- Figure locator: `Figure 4`
- Table locator: `Table 1`
- Fit equation: `Equation (3)`
- Fit target: `full erasure (p=1)` asymptotic work from the `tau^-1` extrapolation
- Reported value: `0.71 +/- 0.03 kT`

## Runtime Mapping Boundary

At the current verifier baseline of `300 K`, this source-facing summary maps to about `0.01835 +/- 0.00078 eV`.
That is the active Jun lower-bound support row.

The legacy `0.028 eV` row remains outside active Jun logic unless a different final-source quantity later justifies it.

## What This Closes

This file closes the generic source-summary identity blocker for the active Jun interval:

- the source family is known
- the source surface is named
- the table/figure/equation locator is named
- the fit target is named
- the unit basis and runtime conversion are explicit

## What Remains Open

This file does not close:

- final PRL page/PDF parity against the arXiv source surface
- local archival of the final article PDF or source table
- row-level numeric transcription beyond the summary target
- any restoration of the legacy `0.028 eV` row as a clean Jun quantity
- the broader UET bridge derivation

## Machine-Readable Artifact

- `Data/03_Research/jun_2014_source_summary_locator.json`
