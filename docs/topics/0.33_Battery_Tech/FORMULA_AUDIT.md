# Formula Audit: 0.33_High_Energy_Density_Battery_Materials

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `SEI_Resistance_Kinetics`

**Relation**

```text
R_sei = d_sei / sigma_sei
j0_eff = j0_raw / (1 + j0_raw * R_sei)
Symmetry_Ratio = j0_anode_eff / j0_cathode
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `R_sei` | SEI Resistance | `Ohm*cm^2` (approx scaling) |
| `d_sei` | SEI Thickness | `nm` |
| `sigma_sei` | SEI Ionic Conductivity | `S/cm` |
| `j0_eff` | Effective exchange current density | `mA/cm^2` |
| `Symmetry_Ratio` | Balance of kinetic rates | `dimensionless` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | Calculate `R_sei` based on whether ALD is applied (thinner, more conductive) vs standard SEI. |
| `2` | Attenuate the raw anode exchange current `j0_raw` by the SEI resistance. |
| `3` | Compare anode and cathode effective currents to check for Lithium plating risk (Symmetry Ratio < 1.0). |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `sigma_sei` | `heuristic_bridge` | Assumed `1e-4` S/cm for ALD fast-ion conductors, vs `1e-6` for traditional SEI. Requires specific ALD material (e.g., Al2O3 vs LiPON) derivation. |
| `j0_cathode` | `heuristic_bridge` | Assumed 2.5 mA/cm2 for High-Nickel cathodes. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `heuristic bridge` |
| `verification_role` | `exploratory` |
| `code_path` | `Code/01_Engine/Engine_High_Energy_Battery.py` |

**Failure mode**

- If kinetic symmetry is not balanced, the simulation will inaccurately predict high capacity retention when in reality lithium plating would rapidly destroy the cell.

---

### Entry 2: `Lithium_Inventory_Loss`

**Relation**

```text
Li_loss = degradation_rate * scaling_factor * cycles
Retention = 1.0 - Li_loss
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `Li_loss` | Fraction of active lithium consumed | `%` |
| `degradation_rate` | SEI fracture rate * applied current | `dimensionless/cycle` |
| `Retention` | Remaining usable capacity | `%` |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `sei_fracture_rate` | `heuristic_bridge` | Assumed 1% for ALD (flexible), 15% for standard (brittle) due to 300% Silicon volume expansion. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `heuristic bridge` |
| `verification_role` | `benchmark input` |
| `code_path` | `Code/01_Engine/Engine_High_Energy_Battery.py` |

**Failure mode**

- Underestimating Si volume expansion fracture rates leads to an engine that falsely validates physically impossible battery life cycles.


