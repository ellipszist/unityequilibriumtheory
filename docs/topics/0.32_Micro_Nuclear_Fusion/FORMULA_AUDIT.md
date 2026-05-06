# Formula Audit: 0.32_Micro_Nuclear_Fusion

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `Phonon_Thermal_Extraction`

**Relation**

```text
E_elec = (Q_gross * eta_therm) * eta_teg
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `E_elec` | Electricity Generated | `W/m^3` |
| `Q_gross` | Gross fusion heating | `K/timestep` (scaled to W) |
| `eta_therm` | Thermal conductivity efficiency | `dimensionless` |
| `eta_teg` | Thermoelectric conversion efficiency | `dimensionless` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | Calculate `cooling_drain = Q_gross * eta_therm` |
| `2` | Convert cooling drain to `E_elec` by multiplying by `eta_teg` (and scaling factor 1000.0) |
| `3` | Deduct `cooling_drain` from lattice temperature to prevent vaporization. |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `eta_therm` | `heuristic_bridge` | Currently 0.85 (85%). Relies on pristine graphene's massive phonon mean free path. |
| `eta_teg` | `heuristic_bridge` | Currently 0.30 (30%). Future high-Z TEG materials embedded in lattice. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `heuristic bridge` |
| `verification_role` | `exploratory` |
| `code_path` | `Code/01_Engine/Engine_Nuclear_Fusion.py` |

**Failure mode**

- If `eta_therm` is lower than expected, the lattice cannot sink the fusion heat fast enough, leading to rapid vaporization of the containment structure.

---

### Entry 2: `Effective_Coulomb_Barrier`

**Relation**

```text
E_eff = E_classical * (1.0 - beta)
```

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `E_eff` | Effective Coulomb Barrier | `eV` |
| `E_classical` | Classical Coulomb Barrier | `eV` |
| `beta` | Informational Coupling / Electron Screening factor | `dimensionless` |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `beta` | `derived` | UET Global parameter. Represents screening by dense lattice electrons. |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `derived` |
| `verification_role` | `gate` |
| `code_path` | `Code/01_Engine/Engine_Nuclear_Fusion.py` |

**Failure mode**

- If `beta` is overestimated, the engine predicts p-B11 fusion at impossibly low temperatures, turning into pseudoscience.


