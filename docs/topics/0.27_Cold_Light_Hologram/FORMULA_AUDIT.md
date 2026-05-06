# Formula Audit: 0.27_Cold_Light_Hologram

Use this template to document important formulas in a topic.

## Formula Audit

### Entry 1: `Acoustic_Levitation_Force`

**Relation**

```text
F_rad = (5 * pi / 6) * a^3 * (P_0^2 / (rho_0 * c_0^2)) * k
```
*(Simplified max force from Gork'ov potential)*

**Variables**

| Symbol | Meaning | Unit |
| :-- | :-- | :-- |
| `F_rad` | Acoustic Radiation Force | `N` |
| `a` | Particle radius | `m` |
| `P_0` | Acoustic pressure amplitude | `Pa` |
| `rho_0` | Air density | `kg/m^3` |
| `c_0` | Speed of sound | `m/s` |
| `k` | Wave number | `rad/m` |

**Conversion steps**

| Step | Description |
| :-- | :-- |
| `1` | Check if `F_rad > F_gravity` to determine levitation state. |

**Constant origins**

| Term | Origin class | Note |
| :-- | :-- | :-- |
| `c_0` | `source_locked_physics_constant` | Speed of sound in air at 20C (~343 m/s) |
| `rho_0` | `source_locked_physics_constant` | Density of air at 20C (~1.204 kg/m^3) |

**Status**

| Field | Value |
| :-- | :-- |
| `proof_status` | `derived` |
| `verification_role` | `gate` |
| `code_path` | `Code/01_Engine/Engine_Cold_Light.py` |
| `artifact_path` | `Result/artifacts/Acoustic_Levitation.json` |

**Failure mode**

- If wave number or pressure is calculated incorrectly, the force will not be sufficient to levitate the Perovskite particles, resulting in a failed 3D canvas.

**Next hardening step**

- Formalize the exact acoustic frequency (40kHz vs 20kHz) safety limits regarding human and animal hearing using medical source-locked limits.


---
+
+### Entry 2: `Acoustic_Haptic_Feedback`
+
+**Relation**
+
+```text
+I = P_0^2 / (2 * rho_0 * c_0)
+F_haptic = (2 * I / c_0) * A_finger
+```
+
+**Variables**
+
+| Symbol | Meaning | Unit |
+| :-- | :-- | :-- |
+| `I` | Acoustic Intensity | `W/m^2` |
+| `F_haptic` | Radiation pressure force on finger | `N` |
+| `A_finger` | Contact area of fingertip (~1 cm^2) | `m^2` |
+
+**Constant origins**
+
+| Term | Origin class | Note |
+| :-- | :-- | :-- |
+| `A_finger` | `heuristic_bridge` | Standardized at 1e-4 m^2 for haptic benchmarks. |
+
+**Status**
+
+| Field | Value |
+| :-- | :-- |
+| `proof_status` | `identity` |
+| `verification_role` | `exploratory` |
+| `code_path` | `Code/01_Engine/Engine_Cold_Light.py` |
+
+**Failure mode**
+
+- If the intensity calculation is wrong, the predicted haptic force will be incorrect, potentially leading to ultrasonic output that is painfully strong or unnoticeably weak for the user.
