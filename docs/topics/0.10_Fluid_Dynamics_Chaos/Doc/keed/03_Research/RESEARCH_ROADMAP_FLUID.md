> [!WARNING]
> **Legacy claim boundary:** This file is a legacy analysis, paper draft, research note, or bibliography note, not the topic status authority. It must not be used to claim Navier-Stokes/Millennium proof, global regularity or smoothness proof, turbulence closure, production CFD replacement, universal fluid-engine superiority, external CFD validation, or theorem-level physical closure. Current allowed claims are controlled by `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `FORMULA_AUDIT.md`, and `Result/artifacts/fluid_benchmark_validation.json`: internal speed benchmark and finite-output stress diagnostic only.
# UET vs Classical Equations: Long-Term Research Plan

> **Purpose**: แผนวิจัยจริงจังเพื่อเปรียบเทียบ UET กับสมการดั้งเดิม  
> **Timeline**: 6-12 เดือน  
> **Goal**: พิสูจน์ว่า UET มีประโยชน์จริงหรือไม่

---

## 🎯 Research Questions

1. **UET alone**: สมการ UET อธิบายปรากฏการณ์เดียวกับ Navier-Stokes ได้ไหม?
2. **Comparison**: ผลลัพธ์ต่างกันยังไง? ดีกว่าหรือแย่กว่า?
3. **Combination**: ถ้าผสมกัน (Modified Navier-Stokes + UET term) ได้ผลยังไง?
4. **Practical**: มีกรณีที่ UET ดีกว่าจริงๆ ไหม?

---

## 📋 Phase 1: Baseline Establishment (เดือน 1-2)

### 1.1 เลือก Benchmark Cases

| Case | ข้อมูลจริง | ความยาก |
|:-----|:----------|:-------|
| **Poiseuille Flow** | Pipe flow experiments | ง่าย |
| **Lid-Driven Cavity** | Standard CFD benchmark | กลาง |
| **Flow Past Cylinder** | Re = 100, 1000 | กลาง |
| **Turbulent Channel** | DNS data (Johns Hopkins) | ยาก |

### 1.2 Implement Standard Navier-Stokes Solver

```python
# Baseline: Standard Navier-Stokes solver
# Method: Finite Difference / Finite Volume
# Validation: Compare with published benchmark data
```

**Deliverable:**
- [ ] Working Navier-Stokes solver
- [ ] Validated against 4 benchmark cases
- [ ] Error metrics documented

---

## 📋 Phase 2: UET Implementation (เดือน 2-3)

### 2.1 Derive UET Fluid Equations

**จาก Master Equation:**
$$\Omega[C,I] = \int \left[ V(C) + \frac{\kappa}{2}|\nabla C|^2 + \beta C I \right] dx$$

**ต้องหา:**
- C = ? (Density? Velocity magnitude?)
- I = ? (Entropy? Vorticity?)
- V(C) = ? (What potential?)

### 2.2 Implement UET Fluid Solver

```python
# UET-based fluid solver
# C = fluid density
# I = entropy density
# Evolve using Euler-Lagrange equations from Ω
```

**Deliverable:**
- [ ] Clear mapping: UET terms → Fluid variables
- [ ] Working UET fluid solver
- [ ] Same benchmark cases as Phase 1

---

## 📋 Phase 3: Head-to-Head Comparison (เดือน 3-5)

### 3.1 Metrics to Compare

| Metric | ความหมาย | วิธีวัด |
|:-------|:---------|:-------|
| **Accuracy** | ถูกต้องแค่ไหน | Error vs benchmark data |
| **Stability** | Blow-up หรือไม่ | Max timestep before crash |
| **Speed** | เร็วแค่ไหน | Runtime for same problem |
| **Interpretability** | อธิบายได้ไหม | ค่า physical ตีความได้ไหม |

### 3.2 Test Matrix

| Case | NS Result | UET Result | Better? |
|:-----|:----------|:-----------|:--------|
| Poiseuille | ? | ? | ? |
| Cavity | ? | ? | ? |
| Cylinder | ? | ? | ? |
| Turbulent | ? | ? | ? |

### 3.3 Focus: High Reynolds Number

**ทำไมสำคัญ:**
- Navier-Stokes อาจ blow-up ที่ high Re
- UET มี V(C) bounded → ไม่ควร blow-up
- ถ้าจริง = **major advantage**

**Deliverable:**
- [ ] Comparison tables for all metrics
- [ ] High Re stability comparison
- [ ] Publication-ready figures

---

## 📋 Phase 4: Modified Navier-Stokes (เดือน 5-7)

### 4.1 Add UET Term to Navier-Stokes

**Modified Equation:**
$$\frac{\partial \mathbf{v}}{\partial t} + (\mathbf{v} \cdot \nabla)\mathbf{v} = -\frac{1}{\rho}\nabla p + \nu \Delta \mathbf{v} + \underbrace{\beta \nabla I}_{\text{UET term}}$$

**Questions:**
- ช่วย stabilize หรือไม่?
- Accuracy ดีขึ้นหรือแย่ลง?
- Physical interpretation?

### 4.2 Test Modified Equation

| Case | Original NS | Modified NS + UET | Improvement? |
|:-----|:-----------|:-----------------|:------------|
| High Re Stability | ❌ Blow-up | ✅ Stable? | Yes? |
| Accuracy | Baseline | ? | ? |

**Deliverable:**
- [ ] Modified solver implementation
- [ ] Stability improvement quantified
- [ ] Paper draft: "UET-regularized Navier-Stokes"

---

## 📋 Phase 5: Real-World Application (เดือน 7-10)

### 5.1 เลือก Application ที่ Navier-Stokes มีปัญหา

| Application | ปัญหาของ NS | UET ช่วยได้? |
|:-----------|:----------|:-----------|
| **Atmospheric Flow** | Multi-scale, turbulence | ? |
| **Blood Flow** | Non-Newtonian, pulsatile | ? |
| **Combustion** | Reaction + flow | ? |
| **Microfluidics** | Slip, rarefied gas | ? |

### 5.2 Validate with Real Data

**ต้องหา:**
- Experimental data (published)
- Compare predictions
- Error analysis

**Deliverable:**
- [ ] Real-world validation
- [ ] Error comparison with NS
- [ ] Case study paper

---

## 📋 Phase 6: Publication & Documentation (เดือน 10-12)

### 6.1 Papers to Write

| Paper | Journal | Theme |
|:------|:--------|:------|
| **Paper 1** | Journal of Computational Physics | UET vs NS benchmark comparison |
| **Paper 2** | Physics of Fluids | Modified NS + UET regularization |
| **Paper 3** | arXiv preprint | Complete theory document |

### 6.2 Open Source Release

- [ ] Clean codebase
- [ ] Documentation
- [ ] Reproducible benchmarks
- [ ] Docker container

---

## 📊 Summary: Timeline

| Month | Phase | Deliverable |
|:------|:------|:-----------|
| 1-2 | Baseline | Working NS solver + benchmarks |
| 2-3 | UET Implementation | UET fluid solver |
| 3-5 | Comparison | Head-to-head results |
| 5-7 | Modified NS | UET-regularized NS |
| 7-10 | Application | Real-world validation |
| 10-12 | Publication | Papers + open source |

---

## ⚠️ Risks & Honest Assessment

### อาจได้ผลลัพธ์:

| ผลลัพธ์ที่เป็นไปได้ | ความหมาย |
|:------------------|:---------|
| **UET ดีกว่า NS** | ค้นพบสำคัญ → Publish |
| **UET เท่า NS** | Alternative framework → ยังมีคุณค่า |
| **UET แย่กว่า NS** | ต้อง refine หรือ abandon → Honest |

### Key Success Factors:

1. **Real Data**: ต้องเปรียบเทียบกับ experimental data จริง
2. **Reproducible**: คนอื่นต้องทำซ้ำได้
3. **Honest**: รายงานทั้ง success และ failure
4. **Peer Review**: Submit to journals

---

## 🔥 Immediate Next Steps

1. **Phase 1 เริ่มทันที:**
   - [ ] เลือก CFD library (OpenFOAM? Fenics? Custom?)
   - [ ] Setup benchmark cases
   - [ ] Implement NS solver

2. **ขนานกัน:**
   - [ ] Derive UET fluid equations อย่างละเอียด
   - [ ] Document mapping: UET → fluid variables

---

*"งานวิจัยจริงจัง = มีข้อมูลจริง, ทดสอบได้จริง, รายงานตรงไปตรงมา"*
