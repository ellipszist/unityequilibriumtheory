# 🌡️ Temperature in Macro Systems

> *How to apply Landauer's principle beyond thermodynamics*

---

## The Challenge

Landauer says: **E = kT ln(2)** per bit

But what is **T** for:
- A galaxy?
- A market?
- A social network?

---

## The Solution: Effective Temperature

### Definition

**Effective Temperature (T_eff)** = A measure of "fluctuation energy" in any system.

```
T_eff = (variance of observable) / k_B
```

---

## Domain-Specific Definitions

### 🌌 Galaxies

| Concept | Definition |
|:--------|:-----------|
| **T_virial** | Kinetic energy of stars |
| **Formula** | T = (m × v²) / (3 × k_B) |
| **Typical value** | ~10⁶ K |
| **Meaning** | How "hot" the stellar motion is |

### 💹 Markets

| Concept | Definition |
|:--------|:-----------|
| **T_market** | Volatility energy |
| **Formula** | T = (price_variance) / k_B |
| **Proxy** | VIX index (scaled) |
| **Meaning** | How "hot" the trading is |

### 🧠 Brain

| Concept | Definition |
|:--------|:-----------|
| **T_neural** | Firing rate variance |
| **Formula** | T = (spike_variance) / k_B |
| **Meaning** | How "active" the network is |

---

## Why This Works

1. **Dimensional consistency**: T has units of energy/k_B ✅
2. **Physical meaning**: Higher variance = higher "temperature" ✅
3. **Universal applicability**: Works for any measurable system ✅

---

## Limitations

- This is **effective** temperature, not thermodynamic temperature
- Only applies to systems with measurable fluctuations
- Scaling factor may vary by domain

---

## Connection to UET

```
E_bit = k_B × T_eff × ln(2)

For markets:
E_bit = k_B × (volatility²/k_B) × ln(2)
      = volatility² × ln(2)
```

**Interpretation:** Cost of information = proportional to variance.

---

*Temperature defined. Landauer now applicable to macro systems.*
