# UET Simulation Harness

The Universal Evolution Thermodynamics (UET) harness is a simulation framework designed to explore phase transitions, symmetry breaking, and transient dynamics in coupled field systems (Conscience vs Instinct).

## Quick Start

To generate all final summaries and phase maps from existing "official" simulation runs:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all.ps1
```

This will:
1. Aggregate data from all `runs_*` folders into `reports/`.
2. Generate phase map plots (`mean_grade`, `strength`) for relevant sweeps.
3. Create a merged master summary `reports/UET_final_summary_ALL.csv`.

## Parameter Documentation

See [UET_PARAMETERS.md](UET_PARAMETERS.md) for detailed definitions of physical parameters like `beta`, `s_tilt`, `kappa`, `delta`, and `Mr`.

## Key Directories

- **`scripts/`**: Python scripts for simulation (`run_suite.py`), validation (`validate_*.py`), and analysis (`make_final_summary.py`, `plot_phase_maps.py`).
- **`matrices/`**: CSV files defining parameter sweeps (Beta x S, coupling ratio, etc.).
- **`runs_*/`**: Output directories containing simulation data (`timeseries.csv`, `config.json`).
- **`reports/`**: Final aggregated results and plots.

## Core Workflows

1. **Generate Matrix**: Use `scripts/make_*_matrix.py` to create a sleep plan.
2. **Run Simulation**: `python scripts/run_suite.py --matrix ...`
3. **Analyze**: Use `run_all.ps1` or individual scripts in `scripts/`.
