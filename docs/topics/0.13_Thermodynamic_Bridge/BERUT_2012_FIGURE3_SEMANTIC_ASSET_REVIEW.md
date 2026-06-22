# Berut 2012 Figure 3 Semantic Asset Review

Date: 2026-06-22

## Scope

This note resolves a raster-role ambiguity in the Berut Figure 3 digitization path.
It does not transcribe a heat value and does not close axis calibration.

## Source Semantics

The Antoine Berut research page describes two relevant Landauer visuals:

- an erasure-procedure sketch for the reset-to-zero one-bit memory protocol;
- an average-heat plot described as average heat `Q` dissipated by the memory erasure procedure as a function of duration `tau`.

That external semantic cue matters because the first protocol candidate `jpeg_3`
looks like a six-panel erasure-procedure schematic, while `jpeg_2` exposes large
stacked panel-frame candidates and is therefore the better quantitative heat-plot
candidate for the Berut summary-row path.

## Decision

`jpeg_2` is promoted to the preferred quantitative digitization candidate.
`jpeg_3` is demoted to schematic/procedure support unless later evidence proves
it contains the numeric heat plot needed for row closure.

## Remaining Blocker

The next controller is not numeric transcription yet. The next pass must select
the relevant quantitative panel in `jpeg_2`, map x/y tick values, identify the
Landauer reference or limit marker, and capture the selected curve/point pixels.

## Claim Boundary

This semantic review corrects candidate priority. It does not produce a
source-normalized Berut row, does not replace the current topic-summary value,
and does not upgrade the Landauer lane beyond lower-bound consistency.
