# UET: Gravity (The First Force)

**Status:** ✅ **VALIDATED**
**Validation:** SPARC Database (154 Galaxies, 73% Pass Rate)
**Data Source:** [sparc_175.csv](../../data_vault/sources/sparc_175.csv)

---

## 1. The Concept

In UET, Gravity is not a separate force but an **emergent effect of Vacuum Stiffness gradients**. Mass creates a local reduction in $\kappa$ (Stiffness), and other masses "fall" toward this lower-stiffness region.

$$\vec{g} = -\nabla \kappa$$

This explains why gravity is always attractive (stiffness gradients always point outward from mass concentrations) and why it's the weakest force (stiffness variations are extremely subtle).

## 2. The Universal Density Law

The key prediction is the **Universal Density Law (UDL)**:

$$\frac{M_{halo}}{M_{disk}} = \frac{k}{\sqrt{\rho_{baryon}}}$$

This naturally explains "Dark Matter" as a consequence of vacuum stiffness equilibration, not as a new particle.

## 3. Validation Results

| Dataset | Galaxies | Pass Rate | Avg Error |
| :--- | :---: | :---: | :---: |
| **SPARC** | 154 | **73%** | 10.8% |
| **LITTLE THINGS** | 26 | **69%** | 14.3% |

### By Galaxy Type (SPARC)
| Type | Count | Pass Rate | Error |
| :--- | :---: | :---: | :---: |
| LSB | 68 | **93%** | 7.1% |
| Spiral | 45 | 60% | 12.2% |
| Dwarf | 22 | 59% | 14.6% |
| Ultrafaint | 14 | 57% | 13.5% |
| Compact | 5 | 40% | 23.8% |

## 4. Limitations
- Compact galaxies remain challenging (40% pass rate)
- The constant $k$ is fitted, not derived from first principles

---

*See [UET_FULL_PAPER.md](../../UET_FULL_PAPER.md) for complete validation details.*
