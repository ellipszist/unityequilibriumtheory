# Formula Audit: 0.28_Material_Synthesis

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `Flash_Joule_Temperature_Rise`

**Relation**

```text
delta_T = (P * t) / (m * c_p)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `delta_T` | Temperature rise | `K` |
| `P` | Power (V^2 / R) | `W` (J/s) |
| `t` | Pulse duration | `s` |
| `m` | Mass of carbon sample | `g` |
| `c_p` | Specific heat capacity of carbon | `J/(g*K)` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | Check if `T_initial + delta_T > 2800 K` to determine if graphitization occurs. |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `c_p` | `source_locked_physics_constant` | Graphite specific heat (~0.710 J/g/K) |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `identity` |
| `verification_role` | `gate` |
| `code_path` | `Code/01_Engine/Engine_Flash_Joule.py` |

**Failure mode**

- If `c_p` is miscalculated, the reactor will either under-heat (failing to vaporize carbon) or over-heat (wasting energy).

---

### Entry 2: `SAW_Acoustic_Capture_Probability`

**Relation**

```text
P_capture = exp(- (dx^2 + dy^2) / Lambda^2)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `P_capture` | Probability of capturing an atom | `dimensionless` (0-1) |
| `dx, dy` | Distance to nearest standing wave node | `lattice_units` |
| `Lambda` | Acoustic trapping range | `lattice_units` |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `Lambda` | `heuristic_bridge` | Currently set to 2.5. Needs to be derived from precise SAW amplitude and thermal noise ratio. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `heuristic bridge` |
| `verification_role` | `exploratory` |
| `code_path` | `Code/01_Engine/Engine_Resonant_CVD.py` |

**Failure mode**

- If `Lambda` is set too high, the engine over-predicts the speed and purity of graphene assembly.


