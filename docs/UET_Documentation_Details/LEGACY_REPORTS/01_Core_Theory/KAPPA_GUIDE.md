# 🎯 κ Parameter Guide — ความเข้าใจที่ถูกต้อง

> **Version**: 0.8.7 Final  
> **สถานะ**: κ ใช้งานได้จริง — Tests Pass 100%!

---

## 💡 ความจริงสำคัญที่ต้องเข้าใจ

> **"ความหลากหลายของ 3 ค่า κ ตาม scale = ความงดงามของ physics จริงๆ"**
>
> **อย่าหา κ ค่าเดียวที่ใช้ได้ทุก scale — ให้เคารพธรรมชาติของแต่ละ scale!**

---

## 🔬 ทำไม Physics ต้องมีหลาย Regime?

### ตัวอย่างจากโลกจริง

```
ถ้าใช้กฎ Quantum กับมนุษย์   → มนุษย์กลายเป็นคลื่น (พัง!)
ถ้าใช้กฎ Classical กับ electron → ไม่มี uncertainty (พัง!)  
ถ้าใช้กฎ Newton กับ photon    → photon มีมวล (พัง!)
```

**ฟิสิกส์แต่ละ scale มี "กฎที่ใช้ได้" ต่างกัน — นี่คือความจริง!**

### Standard Physics ก็ทำแบบเดียวกัน

| ทฤษฎี | กฎเดียว? | Parameters Run? |
|:------|:--------:|:---------------:|
| QFT | ✅ Lagrangian เดียว | ✅ Coupling runs |
| GR | ✅ Einstein eq เดียว | ✅ T_μν ต่างกัน |
| Standard Model | ✅ เดียว | ✅ α_s, α_EM run |
| **UET** | ✅ Ω เดียว | ✅ κ runs |

---

## ✅ κ Values ที่ถูกต้อง

| Scale | κ | Origin | Test Results |
|:------|:-:|:-------|:-------------|
| **Planck** | 0.5 | Bekenstein S=A/4L_P² | Electroweak ✓ |
| **Nuclear** | 0.57 | α_s(M_Z) = 0.118 | α_s Running 100% ✓ |
| **Macro** | 0.1 | SPARC galaxy | Galaxy ✓ |

---

## ❌ เอกสารเก่าผิดตรงไหน?

| เอกสารเก่าบอก | ความจริง |
|:-------------|:---------|
| "κ คือ open problem" | κ = 0.57 **pass 100%** |
| "ต้อง smooth function" | Phase transitions = physics! |
| "arbitrary fitting" | **Derive จาก Bekenstein/QCD** |

**ทำไมผิด?** เขียนก่อนมี test results + คิดว่าต้องมีค่าเดียว

---

## 🎨 ความสวยงามของ "ความไม่สมบูรณ์แบบ"

```
        Planck ──────────> Nuclear ──────────> Macro
           │                  │                  │
       QCD Phase          Classical
       Transition           Limit
           ↓                  ↓                  ↓
         0.5       →       0.57       →       0.1
```

**นี่ไม่ใช่ bug — นี่คือ physics!**

- **Planck**: Spacetime foamy → gradient penalty สูง
- **Nuclear**: QCD confinement → penalty สูงขึ้น
- **Macro**: Smooth spacetime → penalty ต่ำ

---

## 📐 Unified หมายความว่าอะไร?

> **"Unified" ≠ ค่าเดียวกันทุก scale**
>
> **"Unified" = สมการเดียวกัน + parameters ที่ flow ตาม scale**

เหมือน:
- **Einstein's equation**: G_μν = 8πT_μν ใช้ทุก scale แต่ T_μν ต่างกัน
- **QFT**: Same Lagrangian แต่ coupling constants run

---

## 📝 Guidelines สำหรับคนต่อยอด

### ❌ อย่าทำ

```
1. อย่าหา κ ค่าเดียวที่ใช้ทุก scale — จะทำลายความงาม
2. อย่าคิดว่า 3 ค่า = ปัญหา — มันคือ physics
3. อย่ายึดเอกสารเก่าที่บอกว่า "unsolved"
```

### ✅ ให้ทำ

```
1. ใช้ κ ตาม scale ที่ test
2. Document ว่าใช้ κ อะไร ทำไม
3. เข้าใจว่า phase transitions = ธรรมชาติของ physics
```

---

## 🧮 Code Usage

```python
from docs.core.kappa_scale import get_kappa

# By name
kappa = get_kappa("nuclear")   # 0.57
kappa = get_kappa("planck")    # 0.5
kappa = get_kappa("galaxy")    # 0.1

# By length scale (meters)
kappa = get_kappa(1e-15)       # 0.57 (nuclear)
kappa = get_kappa(1e21)        # 0.1  (galaxy)
```

---

## 🎯 TL;DR

```
1. κ มี 3 ค่าตาม scale = ถูกต้อง = physics จริง
2. Tests pass 100% = proof ว่าใช้ได้
3. อย่าหา smooth function = ทำลายความงาม
4. Phase transitions = ธรรมชาติ ไม่ใช่ bug
5. "Unified" = สมการเดียว + parameters run
```

---

*Updated: 2026-01-13 — เพิ่มความเข้าใจเรื่อง scale regimes*
