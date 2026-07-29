# UET Research Dependency Graph — Waves 0–10

```mermaid
flowchart TD
  F0["Wave 0: inventory"] --> F1["Wave 1: ontology and correspondence"]
  F1 --> F2["Wave 2: units and derivation"]
  F2 --> F3["Wave 3: conserved-C vs finite-cone-C"]
  F3 --> F4["Wave 4: observable mapping"]
  F4 --> P11["Wave 5: 0.11 phase pilot"]
  F4 --> P13["Wave 6: 0.13 thermal pilot"]
  F3 --> E["Wave 7: O(2) EOS and transport"]
  F4 --> C["Wave 8: carrier and observer"]
  E --> G["Wave 9: GR, orbit, cosmology"]
  C --> G
  P11 --> A["Wave 10: galaxy and cosmic comparisons"]
  P13 --> A
  G --> A
```

The graph is a dependency map, not a statement that every arrow is already
closed. The current foundation gate is the controlling cut: downstream
artifacts may remain useful as diagnostics, but they cannot promote a claim
while the upstream ontology, units, correspondence, or numerical gate is
blocked.

## Two-arm C decision

The conserved-C branch and the finite-cone-C branch are deliberately separate:

1. conserved C is the phase/order comparator and retains its conservation
   interpretation;
2. finite-cone C is a non-conserved telegraph realization with a separate
   order/behaviour ontology;
3. a conserved Cattaneo current is a negative control until a derived UV or
   nonlocal regularization removes its high-(k) unbounded speed.

No edge in this graph maps (C) directly to mass, maps (R_{gen}) to a
particle, or promotes a detector record to a physical field.
