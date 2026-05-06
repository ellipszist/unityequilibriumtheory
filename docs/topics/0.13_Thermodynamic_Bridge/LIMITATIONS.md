# Limitations

- The root baseline comparison is present, but numeric acceptance boundaries are still provisional until a saved artifact is generated and reviewed.
- Current data posture is source-referenced but still below a fully normalized archival dataset package.
- Berut 2012 and exact SI/CODATA source records are now pinned under `docs/data/external/...`, but the Berut numeric rows used by the verifier remain topic-derived summaries rather than raw archived tables.
- The data package still contains manual literature summaries, so the topic cannot yet claim fully standardized data provenance.
- `source_evidence_intake_stub.json` and `source_evidence_readiness_matrix.json` are process controls, not evidence by themselves; an empty or pending-ready gate cannot be cited as provenance closure.
- `Research_Landauer.py` verifies exact-constant consistency and lower-bound behavior; it does not prove the complete UET bridge mechanism.
- Bekenstein, Unruh, Hawking, and Josephson formulas are established physics/metrology identities. They constrain the bridge but do not independently validate UET dynamics.
- The Cattaneo benchmark is synthetic and fitted; it is useful for model-shape checking but cannot be cited as external experimental evidence.
- The vacuum entropy-sink script is an open hypothesis sandbox. It requires conservation-law accounting and an independently motivated physical mechanism before it can support core theory claims.
- Internal script execution does not by itself establish external replication, theorem-level proof, or broad physical closure.

## Current Claim Boundary

| Claim area | Allowed wording now | Blocker to stronger wording |
|:--|:--|:--|
| Landauer bridge | Source-record-backed lower-bound consistency check | Raw external source package, uncertainty table, and dynamic UET prediction beyond the lower bound. |
| Thermodynamic gravity links | Consistency with standard formulas | Formal derivation showing how UET field variables produce the relation, not only reuse it. |
| Non-equilibrium heat transport | Synthetic Cattaneo-style lag demonstration | Real dataset or declared simulation-only role with fixed parameters. |
| Vacuum entropy sink | Hypothesis sandbox | Physical mechanism, conservation accounting, and falsifiable test. |
| Provenance workflow | Intake/readiness gate exists for missing source packages | Filled evidence entries, archived upstream files, and source-review closure. |
