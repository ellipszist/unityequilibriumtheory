# 🧮 Proof Analysis: Color Confinement

> [!WARNING]
> **Legacy claim boundary:** This file is a concept, paper draft, bibliography note, or legacy analysis note from an earlier drafting pass.
> It is not the topic status authority and must not be used to claim QCD derivation, confinement proof,
> full AME2020-table pass, hadron-mass validation, light-nuclei closure, independent proton-radius prediction,
> complete strong-force theory, or Millennium-style closure. Current allowed claims are controlled by
> `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `FORMULA_AUDIT.md`, and
> `Result/artifacts/nuclear_binding_source_locked_validation.json`: selected heavy-nucleus subset and proton-radius benchmark-anchor checks only.

## Why Can't Quarks Be Free?

### Standard Answer (QCD)
Lattice QCD simulations show that the potential between quarks grows linearly with distance:
$$ V(r) = -\frac{4}{3}\frac{\alpha_s}{r} + \sigma r $$

The second term (string tension $\sigma \approx 0.44$ GeV/fm) means you need infinite energy to separate quarks.

### UET Answer
The linear potential arises because **gluons carry color charge**.
- Photons are neutral → EM field spreads ($1/r^2$).
- Gluons are colored → Gluon field **concentrates**.

In UET terms:
- The C-I field forms a "flux tube" between quarks.
- Flux tube has constant cross-section (Information cannot dilute).
- Energy per length = String Tension = Constant.

**Key Insight:** Confinement is **Information Condensation** at low energy.

## Proof Script
Run the symbolic derivation:
```powershell
python docs/topics/0.5_Nuclear_Binding_Hadrons/Code/02_Proof/Proof_Color_Confinement.py
```

## Known Limitations

### Light Nuclei (A < 10)
The `Research_Nuclear_Binding.py` script uses a modified Bethe-Weizsäcker formula.
This formula is a **semi-empirical model** (not first-principles).
It fails for light nuclei (H2, H3, He3, He4) because:
1. Shell effects are dominant.
2. Pairing energy is not well-modeled.
3. Surface tension term breaks down.

**This is NOT a UET failure.** It's a domain limitation of the liquid-drop model.

For accurate light nuclei, use the **ab-initio nuclear structure** approach (future work).
