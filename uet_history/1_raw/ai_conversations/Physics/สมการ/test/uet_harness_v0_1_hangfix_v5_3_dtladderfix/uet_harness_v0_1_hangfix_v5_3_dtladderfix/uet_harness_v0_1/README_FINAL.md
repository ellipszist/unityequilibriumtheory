# UET Harness (v0.1.35) — Run/Validate/Report

This repo is a simulation/validation harness for the UET toy models (C-only / C–I) used to stress-test parameters, measure equilibrium vs transient behavior, and produce reproducible summary reports + phase maps.

## What we consider “done” (before any Mapping)
- Parameters affect the **correct channel**:
  - **Equilibrium** (final state): e.g. `OmegaT`, `mean_C/mean_I`, `bias_CI`, `grade_bias`
  - **Transient** (timescale): e.g. `t_relax`, `AUC_Omega_norm`, `slope_init`, `Omega_half`
- Differential tilt works: `s_tilt > 0 → BIAS_C`, `s_tilt < 0 → BIAS_I`, `s_tilt = 0 → random/SYM`
- One-click generation of:
  - `UET_final_summary.csv`
  - `phase_mean_grade.png`, `phase_strength.png`

---

## Requirements
- Python 3.10+ recommended
- `pip install -r requirements.txt` (or your existing environment that already runs `scripts/run_suite.py`)

---

## Quick Start

### 1) Run a matrix
Example (differential tilt beta×s sweep):
```powershell
python scripts/run_suite.py --matrix matrices/UET_Cross_CI_beta_s_tiltCOnly_seed10.csv --out runs_betaXs_tiltCOnly --progress_every_s 5
```

### 2) Build a single summary file (no external validation CSVs needed)
```powershell
python scripts/make_final_summary.py --runs runs_betaXs_tiltCOnly
```

Output:
- `runs_betaXs_tiltCOnly/UET_final_summary.csv`

### 3) Plot phase maps (beta × s_tilt)
```powershell
python scripts/plot_phase_maps.py --csv runs_betaXs_tiltCOnly/UET_final_summary.csv --outdir runs_betaXs_tiltCOnly/phase_maps
```

Outputs:
- `runs_betaXs_tiltCOnly/phase_maps/phase_mean_grade.png`
- `runs_betaXs_tiltCOnly/phase_maps/phase_strength.png`
- (optional) `phase_prob.csv` if you enable it

---

## Recommended “tilt” spec (important)
To get **real differential tilt** (C vs I):
- `potC.s = s_tilt`
- `potI.s = 0`

If you set `potC.s == potI.s` then `s_tilt = 0` everywhere → phase strength can appear flat (this is expected).

---

## Where to look
- Per-run time series:
  - `<runs_dir>/**/timeseries.csv`
- Canonical summary:
  - `<runs_dir>/UET_final_summary.csv`
- Phase maps:
  - `<runs_dir>/phase_maps/*.png`

---

## Key outputs (interpretation)
- `OmegaT`: final energy (equilibrium)
- `t_relax`: time to reach equilibrium tolerance
- `AUC_Omega_norm`: integrated transient deviation (normalized)
- `mean_C, mean_I, bias_CI`: symmetry-breaking / chosen side
- `grade_bias`: `BIAS_C`, `BIAS_I`, `SYM`
