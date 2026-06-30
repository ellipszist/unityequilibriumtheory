# Formula Audit Template

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `<formula_id>`

**Relation**

```text
<write the formula or calculation path>
```

**Variables**

| Symbol | Mathematical/Physical Definition | Unit |
| :-- | :-- | :-- |
| `<x>` | `<continuous field / scalar / tensor / exact meaning>` | `<unit>` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | `<unit conversion or normalization>` |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `<constant>` | `<source_locked_physics_constant / heuristic_bridge / ...>` | `<source or caveat>` |

**Status**

| Field | Value |
| :-- | :-- |
| `unit_closure_status` | `<Closed (exact match) / Proxy (approximate) / Open (unresolved)>` |
| `proof_status` | `<identity / derived / checked local / heuristic bridge / open>` |
| `verification_role` | `<gate / benchmark input / diagnostic-only / exploratory>` |
| `code_path` | `<script or engine path>` |
| `artifact_path` | `<artifact path or N/A>` |

**Failure mode**

- `<what goes wrong if this term or unit path is wrong>`

**Next hardening step**

- `<what should be derived, source-locked, or tested next>`
