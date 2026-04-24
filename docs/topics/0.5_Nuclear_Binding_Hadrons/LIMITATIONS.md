# Limitations

- The current strict binding-energy verifier uses a source-backed extracted subset of AME2020, while the wider parsed table is reported through a separate diagnostic artifact rather than a hard pass/fail gate.
- Heavy nuclei pass the current gate, but light nuclei are still intentionally excluded from the strict liquid-drop validation regime.
- The full-table diagnostic layer is expected to show much weaker performance for lighter nuclei, so the topic should not be described as uniformly accurate across the whole AME2020 parsed table.
- The engine uses fixed semi-empirical coefficients plus a UET correction term, so this topic should not yet be presented as fully parameter-free.
- PDG quark-mass and hadron-mass layers are still partly legacy local snapshots and should be upgraded separately.
- Internal script execution does not by itself establish external replication, theorem-level proof, or broad physical closure.
