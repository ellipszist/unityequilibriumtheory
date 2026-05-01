# Method

- 2D solver: `Code/01_Engine/Engine_UET_2D.py`
- 3D solver: `Code/01_Engine/Engine_UET_3D.py`
- Benchmark workflow: `Code/02_Proof/Proof_Turbulence_Benchmarks.py`
- Supporting research workflows: `Code/03_Research/`

Method boundary:

- Current repository evidence is benchmark-oriented.
- The topic should be described as an internal solver and benchmark program, not as a
  conclusive theorem package.
- The primary benchmark uses an embedded simplified Navier-Stokes-style comparator and a
  UET master-equation update under a fixed grid, step count, trial count, and timing statistic.
- The source-lock manifest records that this is an internal benchmark package and identifies
  the future need for external CFD validation cases.
