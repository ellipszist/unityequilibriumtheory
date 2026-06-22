# Berut 2012 Figure 3 Landmark Candidate Capture

Date: 2026-06-22

## Scope

This note records an automated, non-accepted landmark-candidate pass over the
official Berut Figure 3 raster candidates extracted from the Nature/Springer PPT.
It narrows the digitization blocker, but it does not yet close axis calibration,
curve/point selection, or numeric transcription.

## Inputs

- Official Figure 3 PPT route: `BERUT_2012_FIGURE3_PPT_SOURCE_ROUTE.md`
- Raster inventory: `BERUT_2012_FIGURE3_RASTER_ASSET_INVENTORY.md`
- Digitization protocol: `BERUT_2012_FIGURE3_DIGITIZATION_PROTOCOL.md`
- Candidate files inspected locally:
  - `C:\tmp\berut_latest_asset_jpeg_3.jpg`
  - `C:\tmp\berut_latest_asset_jpeg_2.jpg`

## Automated Detection Result

The automated pass found that `jpeg_2` exposes clearer panel-frame candidates
than the previously selected first calibration candidate `jpeg_3`.

Detected `jpeg_2` frame-like dark components:

| Candidate | Pixel bbox `[x0, y0, x1, y1]` | Width | Height | Interpretation |
|:--|:--|--:|--:|:--|
| upper panel | `[89, 17, 945, 494]` | 857 | 478 | candidate full upper-panel frame/component |
| middle panel | `[89, 587, 945, 1055]` | 857 | 469 | candidate full middle-panel frame/component |
| lower panel | `[89, 1126, 945, 1593]` | 857 | 468 | candidate full lower-panel frame/component |

Detected strong line segments in `jpeg_2`:

- Horizontal: `17-18`, `493-494`, `587-588`, `1053-1055`,
  `1126-1127`, `1511-1512`, `1592-1593`.
- Vertical: `89-91`, `474-475`, `943-945`.

The same pass did not find robust full-axis line segments in `jpeg_3`, though it
did find several dark/medium components that look like cropped subfigure regions.

## Claim Boundary

These coordinates are candidate visual landmarks only. They may guide manual
or visual review, but they are not accepted axis calibration coordinates and do
not justify a machine-transcribed heat value.

The next controller is therefore narrowed from generic axis-landmark capture to
manual review of candidate panel frames, tick marks, Landauer reference line or
limit marker, and selected curve/point coordinates.
