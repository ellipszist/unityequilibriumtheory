# Limitations

- The PDG-linked verifier now passes the current four-observable package: `sin2(theta_W)`, `m_W`, `m_H`, and `G_F`.
- The expanded benchmark also passes the current neutron-lifetime gate, but that neutron layer is still a checked local benchmark rather than a newly source-locked external package.
- Only three branches are currently accepted by the branch claim gate: the core PDG mass benchmark, the weak-angle/Fermi benchmark with provenance caveat, and the secondary neutron benchmark.
- `electroweak_claim_scope_gate` allows those selected benchmark exports while blocking running-angle, gauge-derivation, all-observable electroweak-fit, and Standard Model replacement exports.
- The Higgs branch is now internally more consistent because it follows the electroweak-running angle branch, but that is still a model-design choice that should be defended with a fuller derivation if this topic is pushed toward manuscript-level claims.
- The effective weak-mixing-angle and Fermi-constant layer now sit inside a structured electroweak reference package, but the weak-mixing-angle observable is still not mapped directly from the current PDG SQLite workflow.
- The running-angle layer is useful as a diagnostic, but with the current compiled-point workflow it still sits around a few-percent average error and should not be promoted to a primary benchmark gate.
- The source-lock manifest improves reproducibility, but checked-local layers still need direct upstream mappings before manuscript-grade promotion.
- The gauge-theory derivation and full Standard Model replacement lanes remain blocked and should not be implied by the current benchmark passes.
- Internal script execution does not by itself establish external replication, theorem-level proof, or broad physical closure.
