# Formula Audit: 0.39_Bio_Smart_City

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `Hydrodynamic_Routing_Net_Cost`

**Relation**

```text
UET_Net_Cost = Damage_Cost(Overflow - Absorbed) - Value_Generated(Utilized_Water)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `UET_Net_Cost` | Net economic impact of a flood event on the Bio-Smart City | `USD` |
| `Damage_Cost(x)` | Cost incurred by water that breaches the primary levee and cannot be absorbed | `USD` |
| `Overflow` | Total water volume exceeding levee capacity | `m^3` |
| `Absorbed` | Water successfully routed into the UET reservoir network | `m^3` |
| `Value_Generated(x)` | Agricultural and thermal cooling value extracted from stored floodwater | `USD` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | Calculate total daily inflow from river/monsoon forcing. |
| `2` | Determine overflow past primary bio-synthetic levees. |
| `3` | Route a percentage (`reservoir_absorption_rate`) into reservoirs up to maximum capacity. |
| `4` | Convert unabsorbed overflow into damage, and utilized reservoir water into economic value. |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `reservoir_absorption_rate` | `heuristic_bridge` | Assumed 50%. Represents the physical limit of the city's canal and pumping network. |
| `damage_multiplier` | `heuristic_bridge` | Assumed $100 per m^3 of uncontained floodwater. |
| `agri_value_multiplier` | `heuristic_bridge` | Assumed $2 per m^3 of water utilized for crops/cooling. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `derived` |
| `verification_role` | `benchmark input` |
| `code_path` | `Code/01_Engine/Engine_Hydrodynamic_City.py` |

**Failure mode**

- If the `reservoir_absorption_rate` is physically impossible (e.g., pipes aren't wide enough to move 5 million m^3 a day), the simulation will falsely predict a profitable outcome for an event that actually destroys the city.

---

### Entry 2: `Catastrophic_Failure_Penalty`

**Relation**

```text
Legacy_Damage = Overflow * Damage_Multiplier * Catastrophic_Penalty
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `Catastrophic_Penalty` | Multiplier for damage when static concrete fractures | `dimensionless` |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `Catastrophic_Penalty` | `heuristic_bridge` | Set to 1.5. Concrete levees don't just overtop; they break and release concentrated energy, causing non-linear damage compared to flexible bio-synthetic levees. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `identity` |
| `verification_role` | `diagnostic-only` |
| `code_path` | `Code/01_Engine/Engine_Hydrodynamic_City.py` |

**Failure mode**

- If this penalty is ignored, the model under-represents the systemic fragility of traditional infrastructure, making the UET bio-smart transition look less economically necessary than it truly is.
