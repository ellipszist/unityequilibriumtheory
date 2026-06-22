# Berut 2012 Figure 3 Digitization Protocol

## Purpose

This note defines the minimum protocol for digitizing the official Berut
`Figure 3` quantitative raster candidate. It now incorporates the semantic asset
review that separates the likely procedure schematic from the likely average-heat
plot.

## Candidate Selection

| Role | Asset | Dimensions | SHA-256 |
|:--|:--|:--|:--|
| preferred quantitative digitization candidate | `jpeg_2` | `946 x 1669` | `95823a29ed7f979d3979eb6fa776bce7df8eaa4485632073347874b5c868b188` |
| demoted schematic/procedure support candidate | `jpeg_3` | `646 x 815` | `c22dd0c37b145d4b1759d55b77f07fc6c79daff1e4ed48a15f85bf12087b921d` |

`jpeg_2` is now selected as the first quantitative digitization candidate
because the semantic asset review points to an average-heat `Q` versus duration
`tau` visual, and the automated candidate pass found stronger full-panel frame
candidates in `jpeg_2`. `jpeg_3` remains useful as procedure/schematic context
only unless later evidence shows it contains the numeric heat plot.

## Required Landmarks

Before numeric capture, the next pass must record: selected quantitative panel,
two or more x-axis tick mappings for duration `tau`, two or more y-axis tick
mappings for average heat `Q` or normalized heat, the Landauer reference line or
limit marker, and the selected curve or point with pixel coordinates.

## Claim Boundary

This protocol is a workflow artifact. It does not transcribe a Berut value, does
not replace the current topic-summary value, and does not upgrade the Landauer
lane beyond source-referenced lower-bound consistency.
