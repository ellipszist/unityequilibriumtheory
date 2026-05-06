# Formula Audit: 0.36_Orbital_Manufacturing

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `Vacuum_Radiative_Cooling`

**Relation**

```text
P_rad = A_fin * epsilon * sigma * (T^4 - T_space^4)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `P_rad` | Power radiated into space | `W` |
| `A_fin` | Total surface area of radiative fins | `m^2` |
| `epsilon` | Emissivity of the fin material (graphene) | `dimensionless` |
| `sigma` | Stefan-Boltzmann constant | `W / (m^2 * K^4)` |
| `T` | Current temperature of the shipyard | `K` |
| `T_space` | Cosmic Microwave Background temperature | `K` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | Calculate total radiated power based on current foundry temperature. |
| `2` | Convert power to energy extracted over timestep (`E_rad = P_rad * dt`). |
| `3` | Apply to thermal mass to determine temperature drop during cooling phases. |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `sigma` | `source_locked_physics_constant` | `5.670374419e-8` W/(m^2 K^4) |
| `T_space` | `source_locked_physics_constant` | ~2.7 K |
| `epsilon` | `heuristic_bridge` | Assumed 0.99 for UET's pristine carbon-black graphene fins. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `identity` |
| `verification_role` | `gate` |
| `code_path` | `Code/01_Engine/Engine_Orbital_Foundry.py` |

**Failure mode**

- If `A_fin` or `epsilon` are wildly overestimated, the simulation will predict continuous manufacturing, whereas reality would require extensive downtime, bottlenecking the entire orbital supply chain.

---

### Entry 2: `Foundry_Duty_Cycle`

**Relation**

```text
Duty_Cycle = T_uptime / (T_uptime + T_downtime)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `Duty_Cycle` | Percentage of time the foundry can actively manufacture | `%` |
| `T_uptime` | Total time spent in "FABRICATING" state | `s` |
| `T_downtime` | Total time spent in "COOLING" state | `s` |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `Operating_Limit` | `heuristic_bridge` | The temperature at which machinery/crew is endangered. Set to 500K currently. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `derived` |
| `verification_role` | `benchmark input` |
| `code_path` | `Code/01_Engine/Engine_Orbital_Foundry.py` |

**Failure mode**

- Determines economic viability. If Duty Cycle < 10%, it may be cheaper to launch from Earth than build the massive fin structure required for space manufacturing.
