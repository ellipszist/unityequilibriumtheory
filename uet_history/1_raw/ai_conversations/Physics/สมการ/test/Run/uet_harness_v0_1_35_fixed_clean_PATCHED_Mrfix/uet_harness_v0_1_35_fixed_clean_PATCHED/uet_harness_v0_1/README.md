# UET Verification Harness v0.1 (Strict Mode)
This is an **implementation kickoff pack** for the UET Round-0 verification harness:

- Core models:
  - C-only (Allen–Cahn type)
  - C+I (two-field coupled gradient flow)
- Baseline integrator:
  - Semi-implicit diffusion + explicit reaction/coupling
  - **Accept/Reject** step with **backtracking** to enforce monotone Ω in closed mode
- Logging:
  - run folder contract (config/meta/timeseries/summary)
  - fail/warn codes

## Quick start
1) Put a test matrix CSV (e.g. `UET_R0-C1.3_Tier1_Test_Matrix_v0.1.csv`) somewhere.
2) Run Tier-0/Tier-1 suite:

```bash
python scripts/run_suite.py --matrix /path/to/matrix.csv --out runs --max_cases 999
```

## Notes
- Default is periodic BC with **spectral Laplacian** (FFT).
- Energy uses spectral gradient energy for consistency with spectral operators.
- Neumann/FD is left as TODO for v0.2 (can be added later under the same invariants).

This pack is designed to be **hard to lie**: any energy increase trips fail codes unless it is below tolerance and disappears under dt refinement.


## Golden regression
Run the golden set from a full matrix:

```bash
python scripts/run_golden.py --matrix <tier1.csv> --golden <golden.csv> --out runs_golden --dt_refine
```


## Tier-1 full suite
```bash
python scripts/run_tier1.py --matrix <tier1.csv> --out runs_tier1 --dt_refine --grid_refine_policy boundary
```


## Atlas tools
```bash
python scripts/gen_atlas_matrix.py --preset stage1 --out atlas_stage1.csv
python scripts/run_atlas.py --matrix atlas_stage1.csv --out atlas_runs
python scripts/summarize_atlas.py --runs_root atlas_runs --out atlas_outputs
```


## Boundary refinement (Stage-2)
```bash
python scripts/boundary_select.py --atlas_csv atlas_outputs/atlas.csv --out boundary_candidates.csv
python scripts/gen_stage2_matrix.py --atlas_csv atlas_outputs/atlas.csv --candidates_csv boundary_candidates.csv --out atlas_stage2.csv --grid 128 --T 0.6 --seeds 0,1,2,3,4
python scripts/run_atlas.py --matrix atlas_stage2.csv --out atlas_runs_stage2
python scripts/summarize_atlas.py --runs_root atlas_runs_stage2 --out atlas_outputs_stage2
```


## Demo regime lock & bands map
```bash
python scripts/demo_select.py --atlas_csv atlas_outputs_stage2/atlas.csv --out demo_candidates.csv --top_k 10
python scripts/band_map.py --atlas_csv atlas_outputs_stage2/atlas.csv --out bands.csv
```


## Demo pack
```bash
python scripts/demo_select.py --atlas_csv atlas_outputs_stage2/atlas.csv --out demo_candidates.csv --top_k 10
python scripts/make_demo_pack.py --demo_selected demo_selected.csv --atlas_csv atlas_outputs_stage2/atlas.csv --runs_root atlas_runs_stage2 --out demo_pack --make_plots
python scripts/demo_pack_report.py --demo_pack_index demo_pack/demo_pack_index.csv --out demo_pack/DEMO_REPORT.md
```


## Demo narratives
```bash
python scripts/make_demo_narratives.py --demo_pack_index demo_pack/demo_pack_index.csv
```


## Baseline lock
```bash
python scripts/freeze_baseline.py --harness_root . --out baseline_lock --smoke_ledger runs_smoke/ledger.csv --golden_ledger runs_golden/ledger_golden.csv --tier1_ledger runs_tier1/ledger_tier1.csv --demo_pack demo_pack
```


## Variational sanity check
```bash
python scripts/check_variational.py --model C_only --params "kappa=1,M=1, V=quartic(a=1,delta=1,s=0), init=random"
```


## Units & nondimensionalization (R0-E3)
See docs in `docs/`.

Optional audit (physical mode):
```bash
python scripts/dim_audit.py --config <run_dir>/config.json
```


## dt ladder (R0-E6)
```bash
python scripts/dt_ladder_matrix.py --out dt_ladder_matrix.csv
python scripts/run_dt_ladder.py --matrix dt_ladder_matrix.csv --out dt_ladder_runs --overwrite
python scripts/summarize_dt_ladder.py --ledger dt_ladder_runs/dt_ladder_ledger.csv
python scripts/plot_dt_ladder.py --summary_csv dt_ladder_runs/dt_ladder_summary/dt_ladder_summary.csv
```


## dt presets from ladder (R0-E7)
```bash
python scripts/extract_dt_presets.py --ledger dt_ladder_runs/dt_ladder_ledger.csv --pass_threshold 1.0
python scripts/apply_dt_presets_to_matrix.py --matrix_in atlas_stage1.csv --presets_json dt_ladder_runs/dt_presets/dt_presets.json --matrix_out atlas_stage1_dt.csv --mode cap_to_preset
```


## Band-aware dt presets + baseline manifest (R0-E8)
```bash
python scripts/extract_band_dt_presets.py --ledger dt_ladder_runs/dt_ladder_ledger.csv --band_map band_map.csv --pass_threshold 1.0
python scripts/apply_band_dt_presets_to_matrix.py --matrix_in atlas_stage1.csv --matrix_out atlas_stage1_dt.csv --band_presets_json dt_ladder_runs/band_dt_presets/band_dt_presets.json --global_presets_json dt_ladder_runs/dt_presets/dt_presets.json --mode cap_to_preset
python scripts/freeze_baseline_manifest.py --out baseline/baseline_manifest.json --ledger dt_ladder_runs/dt_ladder_ledger.csv --dt_presets dt_ladder_runs/dt_presets/dt_presets.json --band_dt_presets dt_ladder_runs/band_dt_presets/band_dt_presets.json --pass_threshold 1.0 --overwrite
```


## Auto band map (R0-E9)
```bash
python scripts/auto_band_map_from_ledger.py --ledger dt_ladder_runs/dt_ladder_ledger.csv --out band_map.csv
python scripts/add_band_to_matrix.py --matrix_in atlas_stage1.csv --band_map band_map.csv --matrix_out atlas_stage1_with_band.csv --extract_from_case_id
```


## Seed-robust dt presets + threshold calibration (R0-E12)
```bash
python scripts/compute_run_metrics.py --ledger dt_ladder_runs_seeds/dt_ladder_ledger.csv
python scripts/calibrate_metric_thresholds.py --run_metrics dt_ladder_runs_seeds/run_metrics.csv --use_only_pass
python scripts/extract_dt_presets_strict.py --ledger dt_ladder_runs_seeds/dt_ladder_ledger.csv --strict_all_seeds --require_seed_coverage --metrics dt_ladder_runs_seeds/run_metrics.csv --thresholds_json dt_ladder_runs_seeds/metric_thresholds.json
python scripts/extract_band_dt_presets_strict.py --ledger dt_ladder_runs_seeds/dt_ladder_ledger.csv --band_map band_map_metrics.csv --strict_all_seeds --require_seed_coverage --metrics dt_ladder_runs_seeds/run_metrics.csv --thresholds_json dt_ladder_runs_seeds/metric_thresholds.json
```


## Preset stress test + gate (R0-E13)
```bash
python scripts/generate_stress_matrix.py --spec stress_spec.json --band_dt_presets band_dt_presets.json --dt_presets dt_presets.json --out stress_matrix.csv
python scripts/run_dt_ladder.py --matrix stress_matrix.csv --out stress_runs --overwrite
python scripts/summarize_stress_test.py --ledger stress_runs/dt_ladder_ledger.csv
python scripts/gate_stress_results.py --summary_csv stress_runs/stress_summary/stress_summary.csv --min_pass_rate 0.95 --min_ci_lo 0.90
```


## Adaptive stress (R0-E14)
```bash
python scripts/failure_mode_report.py --ledger stress_runs/dt_ladder_ledger.csv
python scripts/make_adaptive_stress_matrix.py --stress_matrix_in stress_matrix.csv --stress_ledger stress_runs/dt_ladder_ledger.csv --out adaptive_stress_matrix.csv --dt_scales 1.0;0.5
python scripts/run_dt_ladder.py --matrix adaptive_stress_matrix.csv --out adaptive_runs --overwrite
python scripts/summarize_stress_test.py --ledger adaptive_runs/dt_ladder_ledger.csv --group band_model_integrator_variant
```


## Auto-fix proposals + baseline refresh (R0-E15)
```bash
python scripts/propose_preset_updates_from_variant_summary.py --variant_summary_csv adaptive_runs/stress_summary/stress_summary.csv --band_presets_json band_dt_presets_strict.json --out preset_update_proposals.csv
python scripts/render_preset_update_report.py --updates_csv preset_update_proposals.csv --out_md preset_update_report.md --only_changes
python scripts/apply_preset_updates.py --presets_in band_dt_presets_strict.json --updates_csv preset_update_proposals.csv --presets_out band_dt_presets_strict_updated.json --mode band --apply_only_gate_pass
```


## One-command loop driver (R0-E16)
```bash
python scripts/loop_driver.py --config loop_config.json
python scripts/loop_driver.py --config loop_config.json --dry
```


## Zoom dt search (R0-E17)
```bash
python scripts/loop_driver.py --config loop_config.json
# set params.adaptive_mode=zoom and zoom_rounds
```


## Band-aware zoom policy + smoothing (R0-E18)
```bash
# in loop_config.json:
# params.zoom_use_smoothing=true
# params.zoom_band_policy_json=band_zoom_policy.json
python scripts/loop_driver.py --config loop_config.json
```


## Band-aware proposals + monotonic guard (R0-E19)
```bash
# band-aware updates + monotonic guard are enabled by params in loop_config.json
python scripts/loop_driver.py --config loop_config.json
```


## Auto-resample on monotonic block (R0-E20)
```bash
# enable params.resample_on_block=true
python scripts/loop_driver.py --config loop_config.json
```


## Escalation on persistent monotonic BLOCK (R0-E21)
```bash
python scripts/loop_driver.py --config loop_config.json
```


## Metric triage report (R0-E22)
```bash
python scripts/loop_driver.py --config loop_config.json
```


## Evidence budgeter (R0-E25)
```bash
# evidence_budgeter runs before evidence executor; it sets per-group extra_seeds schedules and stop rules
python scripts/loop_driver.py --config loop_config.json
```


## Lock guard + expanded action types (R0-E27)
- targeted_action_executor supports --respect_lock and do_not_touch.
