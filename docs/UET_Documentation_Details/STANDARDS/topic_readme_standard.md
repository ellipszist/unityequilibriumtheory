# Topic README Standard

Every public topic README should follow the same evidence-aware structure.

## Required sections

1. `Problem`
2. `Assumptions and scope`
3. `Data sources`
4. `Method summary`
5. `Parameters and fitting status`
6. `Metrics and thresholds`
7. `Baselines or comparator models`
8. `Limitations and open risks`
9. `Reproducibility`
10. `Current readiness status`

## Required conventions

- State the exact local dataset path or explicitly say the topic currently references
  published values without a normalized raw-data package.
- If a script optimizes a parameter, the README must call the result `calibration` or
  `fitting`, not `zero curve fitting`.
- If a topic contains a failed benchmark, keep it visible instead of collapsing it into a
  summary success badge.
- Link to supporting files for method, verification spec, data manifest, baseline
  comparison, and limitations when those files exist.

## Readiness vocabulary

- `Archived`
- `Draft`
- `Structured`
- `Reproducible internally`
- `Academic-ready`
