# Core Topic Dependency Map

This map defines the first-pass dependency structure for core research topics `0.0` through
`0.26`. It is a governance artifact: it prevents future topics or weak bridge claims from
silently becoming evidence for the core theory.

## Layer Model

| Layer | Topics | Role | Current control rule |
| :-- | :-- | :-- | :-- |
| Integration index | `0.0` | Cross-topic integration and claim routing | Must not act as a proof source unless downstream formula/data/verifier artifacts exist |
| Astrophysics/cosmology | `0.1`, `0.2`, `0.3`, `0.19`, `0.26` | Large-scale empirical and geometric checks | Requires external data provenance and verifier artifacts before public claims |
| Quantum/field foundations | `0.4`, `0.9`, `0.10`, `0.11`, `0.12`, `0.13`, `0.14`, `0.21`, `0.23` | Mathematical and physical mechanism layer | Requires formula audits before any theorem/solved language |
| Particle/nuclear physics | `0.5`, `0.6`, `0.7`, `0.8`, `0.16`, `0.17`, `0.20` | Constants, masses, interactions, and benchmark-heavy checks | Requires source-locked benchmark inputs, unit discipline, and verifier artifacts |
| Complex/life/society extension within core | `0.15`, `0.18`, `0.22`, `0.24`, `0.25` | Model extension and applied reasoning | Must inherit limitations from foundation/physics layers |

## Dependency Rules

- `0.0_Grand_Unification` is an index and integration layer, not an independent proof layer.
- Any topic depending on an open formula bridge inherits that bridge's limitation.
- A benchmark-fed value cannot be reused in another topic as if it were a derived UET constant.
- External datasets shared across topics must live under `docs/data/external/...` and be named
  in each dependent topic's `DATA_MANIFEST.md`.
- Future topics `0.27+` cannot support core claims until promoted through the same data,
  formula, verification, and limitation gates.

## Known Core Blockers From Latest Audit

| Blocker class | Affected topics | Required repair |
| :-- | :-- | :-- |
| Bootstrap/open formula audits | Most core topics after Wave 1 bootstrap | Replace scaffold rows with reviewed formula entries |
| Weak or placeholder data status | `0.5`, `0.6`, `0.8`, `0.13`, `0.18`, `0.22`, `0.26` | Upgrade provenance, units, and benchmark roles |
| Embedded-local-only data | `0.9`, `0.14`, `0.23` | Identify upstream source or label as internal working copy |
| Machine-readable verifier FAIL | `0.7` | Rework live engine angle path or revise benchmark threshold honestly |
| Overclaim wording signals | Listed in `core_research_hardening_audit.md` | Downgrade after formula/data/verifier status is known |

## First Cross-Topic Hardening Threads

1. **Particle benchmark thread**: `0.5 -> 0.6 -> 0.7 -> 0.8 -> 0.17 -> 0.20`.
   Focus: constants, units, external benchmark data, and source-locked comparison artifacts.
2. **Cosmology/astrophysics thread**: `0.1 -> 0.2 -> 0.3 -> 0.19 -> 0.26`.
   Focus: observed datasets, baseline models, metric thresholds, and limitations.
3. **Mathematical mechanism thread**: `0.9 -> 0.10 -> 0.11 -> 0.12 -> 0.13 -> 0.14 -> 0.21 -> 0.23`.
   Focus: proof status, open bridges, and avoiding theorem-level language before derivation review.
4. **Applied extension thread**: `0.15 -> 0.18 -> 0.22 -> 0.24 -> 0.25`.
   Focus: inherited assumptions and preventing applied claims from feeding back as core evidence.

## Maintenance

Update this file after each hardening wave if a topic's dependency role changes. The audit
report remains the operational queue; this map explains why a blocker matters across topics.
