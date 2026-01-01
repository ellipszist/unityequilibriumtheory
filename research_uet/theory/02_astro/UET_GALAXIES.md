# UET: Galaxy Rotation Curves

**Status:** ✅ **VALIDATED**
**Validation:** SPARC (154 galaxies), LITTLE THINGS (26 dwarfs)
**Data Source:** [sparc_175.csv](../../data_vault/sources/sparc_175.csv)
**Key Insight:** "Dark Matter Halos" are emergent from Vacuum Stiffness equilibration.

---

## 1. The Problem

Galaxy rotation curves remain flat at large radii, implying more mass than visible. Standard solutions require invisible "Dark Matter."

## 2. The UET Solution

UET derives the Dark Matter Halo from the **Universal Density Law**:

$$\frac{M_{halo}}{M_{disk}} = \frac{k}{\sqrt{\rho_{baryon}}}$$

Low-density galaxies (like LSBs and Dwarfs) require proportionally larger halos—exactly as observed!

## 3. Validation Results

### SPARC Database (154 Galaxies)
| Type | Count | Pass Rate | Avg Error |
| :--- | :---: | :---: | :---: |
| **LSB** | 68 | **93%** | 7.1% |
| **Spiral** | 45 | 60% | 12.2% |
| **Dwarf** | 22 | 59% | 14.6% |
| **Ultrafaint** | 14 | 57% | 13.5% |
| **Compact** | 5 | 40% | 23.8% |
| **Overall** | **154** | **73%** | **10.8%** |

### LITTLE THINGS (26 Dwarf Galaxies)
| Model | Pass Rate | Avg Error |
| :--- | :---: | :---: |
| UET v3 (NFW) | 4% | 39.7% |
| UET v6 (Mass-dependent k) | **69%** | **14.3%** |

**Improvement:** 63.9%

## 4. Limitations
- Compact galaxies (40% pass) need further work
- The constant $k$ is calibrated, not derived

---

*See [UET_FULL_PAPER.md](../../UET_FULL_PAPER.md) for complete validation details.*
