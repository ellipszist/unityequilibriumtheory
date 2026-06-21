# Units Contract

## Purpose

This file defines the symbol-to-unit boundary for `0.13`.

It exists because this topic currently contains both:

- source-backed SI calculations such as Landauer, Unruh, Hawking, and Bekenstein formulas
- topic-local proxy dynamics such as entropy/contact engine variables and synthetic bridge demos

Those two layers must not be silently mixed.

## Current status

`partial_contract_dimensional_and_proxy_layers_separated`

Current meaning:

- the topic now declares which symbols belong to the SI physical layer
- the topic now declares which symbols are still only proxies
- the topic does **not** yet close a full proxy-to-SI conversion contract for the UET bridge

## Layer split

| Layer | What belongs here | Current use |
| :-- | :-- | :-- |
| SI physical layer | `E_min`, physical `T`, `a`, `R`, black-hole `M`, converted `E_eV`, computed `S_BH` | constraint and benchmark calculations |
| Topic proxy layer | `E`, `N`, `S_proxy`, `T_proxy`, synthetic `q`, synthetic `grad(T)`, vacuum-sink labels | engine sandbox and exploratory hypothesis work |

## Symbol table

| Symbol | Meaning | Unit | Status | Rule |
| :-- | :-- | :-- | :-- | :-- |
| `E_min` | Landauer lower-bound energy cost | `J` | physical quantity | may be converted to eV only through `E_eV = E_J / e` |
| `T` | physical temperature in Landauer/Unruh/Hawking formulas | `K` | physical quantity | SI kelvin only |
| `E_eV` | energy in electron-volts for benchmark comparison | `eV` | converted physical quantity | derived from joules via exact `e` |
| `R` | radius used in Bekenstein bound examples | `m` | physical quantity | SI meter |
| `M` | black-hole mass | `kg` at runtime; often `M_sun` in sources | physical quantity with source conversion | convert source masses explicitly before use |
| `S_BH` | Bekenstein-Hawking entropy | dimensionless Planck-unit normalization | computed theoretical observable | not a direct measured source column |
| `a` | proper acceleration in Unruh relation | `m/s^2` | physical quantity | SI acceleration |
| `E` | engine energy quanta | dimensionless quanta | proxy only | no justified Joule mapping yet |
| `N` | particle-count proxy | count | combinatorial count | no dimensional conversion needed |
| `S_proxy` | engine entropy proxy | dimensionless proxy | proxy only | not physical entropy in `J/K` |
| `T_proxy` | engine temperature-like proxy | dimensionless proxy | proxy only | must not be called kelvin |
| `q` | synthetic heat-flux-like variable in Cattaneo demo | synthetic flux proxy | proxy only | not a sourced SI observable |
| `grad(T)` | synthetic gradient driver in Cattaneo demo | synthetic gradient proxy | proxy only | not a sourced SI observable |
| `T_vac`, `T_sys` | vacuum-sink sandbox labels | mixed labels, not closed | hypothesis-only | do not merge with SI temperature claims |

## Hard rules

- Do not report `T13-002` engine temperature as kelvin.
- Do not report `T13-001` entropy proxy as physical entropy in `J/K`.
- Do not treat synthetic Cattaneo `q` or `grad(T)` as sourced SI observables.
- Do not mix vacuum-sink temperature labels with the source-backed Landauer or gravity temperature layer.

## What remains open

### 1. Proxy energy scale

Open question:
Can engine energy quanta `E` be mapped to a physically justified energy scale?

Current answer:
Not yet.

### 2. Proxy entropy convention

Open question:
Can `S_proxy` be mapped onto a declared physical entropy convention?

Current answer:
Not yet. It remains a combinatorial/statistical proxy.

### 3. Bridge conversion layer

Open question:
Does UET define a tested bridge term that converts between proxy and SI layers without circular reuse of imported formulas?

Current answer:
Not yet.

## Artifact link

The machine-readable version of this contract is:

- [units_contract.json](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.13_Thermodynamic_Bridge/Data/03_Research/units_contract.json:1)

It should stay aligned with:

- [FORMULA_AUDIT.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.13_Thermodynamic_Bridge/FORMULA_AUDIT.md:1)
- [DERIVATION_MAP.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.13_Thermodynamic_Bridge/DERIVATION_MAP.md:1)
- [METHOD.md](/C:/Users/santa/Desktop/uet_harness/docs/topics/0.13_Thermodynamic_Bridge/METHOD.md:1)
