# Limitations

- The benchmark comparator is simplified and not a full survey of fluid solvers.
- Reported speedups are environment-sensitive.
- Current repository benchmark evidence does not justify proof-level Navier-Stokes claims on its own.
- No external CFD/turbulence validation dataset is packaged as a primary gate yet.
- Finite stress-test output is a useful diagnostic, not a proof of global regularity.
- The branch claim gate now accepts only the internal speed benchmark and stress diagnostic branches; external CFD validation and theorem-level claims remain blocked.
- The artifact-level `fluid_claim_scope_gate` is the export controller: internal PASS can
  coexist with topic-level `WARN` until external CFD data, physical Reynolds-number cases,
  and a separate proof package are available.
