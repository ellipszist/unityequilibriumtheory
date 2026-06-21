# Hong 2016 Source Acquisition Blocker

## Purpose

This file records the current state of the `Hong 2016` source-intake effort for
topic `0.13`.

The blocker is no longer that the alternate branch is unnamed or that no
primary-facing numeric surface exists.
It is now narrower:

- the likely bibliographic identity is visible from multiple secondary summaries
- `Crossref` now confirms the DOI metadata anchor
- an accessible same-author `arXiv` preprint precursor now exposes source-facing
  numeric text
- but the repo still does not archive a final publisher article page or an
  equivalent final-source surface for that paper

This matters because the runtime row cannot be reassigned safely on secondary summaries alone.

## Current authority

- Machine-readable artifact: `Data/03_Research/hong_2016_source_acquisition_blocker.json`
- Supporting files:
  - `docs/data/external/thermodynamics/landauer/hong_2016/source_record.json`
  - `HONG_2016_SOURCE_LINEAGE_NOTE.md`
  - `HONG_2016_NUMERIC_MISMATCH_NOTE.md`

## Current result

The current search state supports the following conservative reading:

- likely paper title:
  `Experimental test of Landauer's principle in single-bit operations on nanomagnetic memory bits`
- likely authors:
  `Jeongmin Hong`, `Brian Lambson`, `Scott Dhuey`, `Jeffrey Bokor`
- likely publication surface:
  `Science Advances`
- likely publication date:
  `2016-03-01`

What is still missing:

- direct archived DOI landing page or official article page
- source-facing table or numeric row
- source-backed uncertainty attached to the same row

What is now narrower than before:

- a secondary-reference trail now points to candidate identifiers:
  `DOI 10.1126/sciadv.1501492`, `PMID 26998519`, `PMCID PMC4795654`
- a `Crossref` work record now confirms the DOI plus article metadata and points to the publisher resource URL
- that Crossref metadata is now also archived locally at
  `docs/data/external/thermodynamics/landauer/hong_2016/crossref_work_record.json`
- an accessible same-author preprint precursor is now visible at
  `https://arxiv.org/abs/1411.6730`
- that preprint surface exposes two source-facing dissipation summaries:
  `6.09 +/- 1.43 zJ` and `4.2 +/- 0.9 zJ`
- but the topic package still does not treat the branch as a closed final-source anchor
  until one direct official landing page or article page is archived locally and
  the intended runtime comparison target is chosen explicitly

What the current environment does on direct fetch attempts:

- `https://arxiv.org/pdf/1411.6730`
  is accessible and exposes source-facing numeric text, but it is a precursor
  surface rather than the final Science Advances article page
- `https://doi.org/10.1126/sciadv.1501492`
  does not currently return a stable page body through the available tooling
- `https://www.science.org/doi/10.1126/sciadv.1501492`
  currently returns `403 Forbidden`
- the same publisher-page route still returns `403` with `Cf-Mitigated: challenge`
  even when probed with a browser-like user agent
- known `PubMed` and `PMC` routes currently hit a browser-check or reCAPTCHA layer

This means the blocker is now narrower than "unknown DOI" or "no primary-facing number":

- the machine-readable bibliographic metadata anchor is now closed
- one accessible primary-facing precursor surface is now visible
- but the direct final-source page archive is still open under current access conditions
- and the final runtime-target selection is still missing

## Current claim boundary

While this blocker remains open, the `Hong 2016` branch may support only:

- candidate alternate-source-family context with preprint-level numeric support

It must not support:

- a closed row reassignment
- a clean numeric closure for `0.026 eV`, `0.028 eV`, or `~0.038 eV`
- an uncertainty-aware benchmark lane

## Next move

The next best action is to capture one of:

1. the official article page
2. the DOI landing page
3. the source PDF or equivalent primary bibliographic page

Because an accessible preprint PDF is now known, the next practical move is:

1. decide which Hong-side quantity is actually the intended runtime comparison target
2. then seek final-publisher confirmation for that chosen quantity
