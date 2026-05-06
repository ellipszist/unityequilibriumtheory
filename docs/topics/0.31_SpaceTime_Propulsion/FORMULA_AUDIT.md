# Formula Audit: 0.31_SpaceTime_Propulsion

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `Singularity_Energy_Injection`

**Relation**

```text
E_inject = M * c^2 / kappa_omega
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `E_inject` | Energy required to create Singularity | `J` |
| `M` | Mass of the target Singularity | `kg` |
| `c` | Speed of light | `m/s` |
| `kappa_omega` | UET Coupling Constant | `dimensionless` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | Amplifies input energy by the coupling factor to achieve Schwarzschild density locally. |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `c` | `source_locked_physics_constant` | Exact constant |
| `kappa_omega` | `heuristic_bridge` | Currently ~10^12, represents systemic coupling amplifier. Needs derivation. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `heuristic bridge` |
| `verification_role` | `exploratory` |
| `code_path` | `Code/01_Engine/Engine_Slingshot_v2.py` |
| `artifact_path` | `N/A` |

**Failure mode**

- If `kappa_omega` is incorrect or ungrounded, the engine assumes unrealistic energy generation, violating the 2nd law of thermodynamics.

**Next hardening step**

- `kappa_omega` must be derived from first principles or source-locked to a known cosmological constant.

---

### Entry 2: `Relativistic_Velocity_Addition`

**Relation**

```text
v_new = (v + dv) / (1 + (v * dv) / c^2)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `v_new` | Resulting velocity | `m/s` |
| `v` | Current velocity | `m/s` |
| `dv` | Delta velocity from slingshot | `m/s` |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `c` | `source_locked_physics_constant` | Einstein's postulate |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `identity` |
| `verification_role` | `gate` |
| `code_path` | `Code/01_Engine/Engine_Slingshot_v2.py` |

**Failure mode**

- If omitted, the ship can exceed the speed of light `c`, breaking causality and making the engine scientifically invalid.


---
+
+### Entry 3: `Hawking_Radiation_Decay`
+
+**Relation**
+
+```text
+t_evap = (5120 * pi * G^2 * M^3) / (hbar * c^4)
+```
+
+**Variables**
+
+| Symbol | Meaning | Unit |
+| :-- | :-- | :-- |
+| `t_evap` | Evaporation time | `s` |
+| `G` | Gravitational constant | `N*m^2/kg^2` |
+| `M` | Mass of singularity | `kg` |
+| `hbar` | Reduced Planck constant | `J*s` |
+
+**Constant origins**
+
+| Term | Origin class | Note |
+| :-- | :-- | :-- |
+| `G, hbar, c` | `source_locked_physics_constant` | Fundamental constants |
+
+**Status**
+
+| Field | Value |
+| :-- | :-- |
+| `proof_status` | `identity` |
+| `verification_role` | `gate` |
+| `code_path` | `Code/01_Engine/Engine_Slingshot.py` |
+
+**Failure mode**
+
+- Incorrect evaporation time leads to either premature singularity loss or infinite energy source assumptions, violating physical constraints on micro-black hole stability.
