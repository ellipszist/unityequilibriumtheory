# Formula Audit: 0.29_Ocean_Recovery

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `Passive_Radiative_Cooling_Power`

**Relation**

```text
P_rad_out = A * epsilon * sigma * (T_surf^4 - T_sky^4)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `P_rad_out` | Net radiated power out | `W` |
| `A` | Surface Area of the Net | `m^2` |
| `epsilon` | Emissivity of Graphene Foam | `dimensionless` |
| `sigma` | Stefan-Boltzmann constant | `W/(m^2*K^4)` |
| `T_surf` | Surface temperature of the net | `K` |
| `T_sky` | Effective sky temperature | `K` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | Combine with `P_sun` and `P_conv` to determine net cooling/heating flux. |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `sigma` | `source_locked_physics_constant` | 5.67e-8 |
| `epsilon` | `heuristic_bridge` | Currently set to 0.95. Requires material verification of the specific Graphene aerogel used. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `derived` |
| `verification_role` | `gate` |
| `code_path` | `Code/01_Engine/Engine_Ocean_Cooling.py` |

**Failure mode**

- If `epsilon` is too low, the net will not radiate enough heat into the atmospheric window to overcome daytime solar heating.

---

### Entry 2: `Thermoelectric_Generation`

**Relation**

```text
P_thermal = (N * S * dT)^2 / (4 * R)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `P_thermal` | Max matched power output | `W` |
| `N` | Number of TEG couples | `count` |
| `S` | Seebeck coefficient | `V/K` |
| `dT` | Temperature differential | `K` |
| `R` | Internal resistance | `Ohm` |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `S` | `source_locked_physics_constant` | Based on Bi2Te3 properties (~200 uV/K). |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `identity` |
| `verification_role` | `exploratory` |
| `code_path` | `Code/01_Engine/Engine_Ocean_Power.py` |

**Failure mode**

- If the expected temperature differential `dT` drops too low (e.g., at night when the net and water reach equilibrium), power generation stops.


