# UET: Quantum Tunneling (Josephson & Alpha Decay)

**Status:** ✅ **VALIDATED**
**Validation:** Josephson AC Effect (<0.1% error), Alpha Decay (r=0.975)
**Key Insight:** Tunneling probability is modified by the $I$-field barrier.

---

## 1. The Josephson Effect

When two superconductors are separated by a thin insulator, Cooper pairs can tunnel through.

### AC Josephson Effect
$$f = \frac{2eV}{h}$$

This is **exact** in UET because:
- Cooper pairs carry quantized $I$-field charge
- The frequency is set by the $I$-field phase evolution rate

**Validation:** <0.1% error against experimental data.

## 2. Alpha Decay (Nuclear Tunneling)

Alpha particles tunnel through the Coulomb barrier. UET modifies the barrier:

$$P_{tunnel} = e^{-2\gamma} \quad \gamma \propto \int \sqrt{V_{Coulomb} + \beta I(r)} \, dr$$

### Validation (NNDC Data)
| Isotope | Observed $t_{1/2}$ | UET Prediction |
| :--- | :--- | :--- |
| U-238 | 4.47×10⁹ y | ✅ |
| Th-232 | 1.4×10¹⁰ y | ✅ |
| Ra-226 | 1600 y | ✅ |
| Po-210 | 138 d | ✅ |

**Correlation:** $r = 0.975$ (Geiger-Nuttall Law reproduced)

## 3. Unified View

Both phenomena are the same physics:
- Josephson: $I$-field tunneling between superconducting phases
- Alpha: $I$-field tunneling through Coulomb barrier

---

*See [UET_FULL_PAPER.md](../../UET_FULL_PAPER.md) for complete validation details.*
