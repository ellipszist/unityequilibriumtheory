# Berut 2012 Figure 3 Digitization Protocol

## Purpose

This note defines the minimum protocol for digitizing the official Berut `Figure 3` raster candidates. It chooses a first calibration candidate and records what must be captured before any numeric transcription can affect the topic row.

## Candidate Selection

| Role | Asset | Dimensions | SHA-256 |
|:--|:--|:--|:--|
| first calibration candidate | `jpeg_3` | `646 x 815` | `c22dd0c37b145d4b1759d55b77f07fc6c79daff1e4ed48a15f85bf12087b921d` |
| fallback candidate | `jpeg_2` | `946 x 1669` | `95823a29ed7f979d3979eb6fa776bce7df8eaa4485632073347874b5c868b188` |

`jpeg_3` is selected only as the first calibration attempt because it is the smaller large raster candidate and may be easier to calibrate. This does not mean the row is digitized or source-normalized.

## Required Landmarks

Before numeric capture, the next pass must record: plot frame bounds, two or more x-axis tick mappings, two or more y-axis tick mappings, the Landauer reference line or limit marker, and the selected curve or point with pixel coordinates.

## Claim Boundary

This protocol is a workflow artifact. It does not transcribe a Berut value, does not replace the current topic-summary value, and does not upgrade the Landauer lane beyond source-referenced lower-bound consistency.
