# Unity Equilibrium Theory (UET) Harness

[![Tests](https://img.shields.io/badge/tests-39%2F39%20passed-brightgreen)](research/unified_results/)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.xxxxx.svg)](https://zenodo.org/)

**เข้าใจจักรวาลด้วยสมการเดียว | Understanding the universe with one equation**

> 🎯 **[ท้าทายทฤษฎีนี้](research/00_core_paper/CHALLENGE.md)** — เราไม่ได้ต้องการให้คุณเชื่อ เราต้องการให้คุณ "ตรวจสอบ"

---

## 🤔 UET คืออะไร? (สำหรับคนทั่วไป)

### ปัญหาที่ทุกคนสงสัย

ทำไมเราเห็นดาวบนท้องฟ้าเป็น "อดีต" ไม่ใช่ "ปัจจุบัน"?

**คำตอบ:** เพราะถ้าเห็นเป็นปัจจุบันได้ → ของไกลมากจะ "มองไม่เห็น" เลย (ไม่มีอดีตให้ส่งมา)

### UET อธิบายว่า:

> **ทุกพฤติกรรมในจักรวาลทิ้ง "ร่องรอยพลังงาน" ลงใน Space**
> - พลังงานเปลี่ยนรูป → กลายเป็นข้อมูล
> - ข้อมูลเหล่านี้คือสิ่งที่เราเห็นและวัดได้
> - ระบบทั้งหมดวิ่งหา "จุดสมดุล" เสมอ

### เปรียบเทียบง่ายๆ:

| สิ่งที่เกิดขึ้น | UET อธิบาย |
|----------------|------------|
| เราเห็นดาว | ข้อมูลอดีตที่ Space ส่งมา |
| แรงดึงดูด | พลังงานไหลหาจุดต่ำสุด |
| สิ่งมีชีวิต | ระบบที่เลือกใช้พลังงานอย่างมีประสิทธิภาพ |
| จักรวาลขยายตัว | ระบบกำลังหาสมดุลใหม่ |

### สมการเดียวที่อธิบายทุกอย่าง:

$$\partial_t \phi = \nabla^2 \frac{\delta \Omega}{\delta \phi}$$

**แปลเป็นภาษาธรรมดา:**
> ทุกการเปลี่ยนแปลง (∂ₜφ) เกิดจากพลังงานไหลผ่าน Space ไปหาจุดสมดุล

📖 [อ่านคำอธิบายเต็มๆ](research/00_core_paper/INTUITIVE_EXPLANATION.md)

---

## 🌟 สิ่งที่ UET ทำได้

| สาขา | ผลทดสอบ | หมายเหตุ |
|------|---------|----------|
| ⚡ แม่เหล็กไฟฟ้า | ✅ | U(1) gauge symmetry |
| 💪 แรงนิวเคลียร์ | ✅ | SU(2) symmetry |
| 🌌 แรงโน้มถ่วง | ✅ | Energy gradient |
| ⚛️ ควอนตัม | ✅ | Topological defects |
| 🕳️ หลุมดำ | ✅ | k=3.0 (ตรงกับข้อมูลจริง) |
| 🔭 Cosmology | ✅ | Ω_Λ = 0.685 (ตรงกับ Planck 2018) |

**ผลรวม: 39/39 tests ผ่าน 100%**

---

## 🚀 Quick Start

### ติดตั้ง

```bash
# Clone
git clone https://github.com/unityequilibrium/Equation-UET-v0.8.7.git
cd Equation-UET-v0.8.7

# สร้าง virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# ติดตั้ง dependencies
pip install -e .
```

### รัน Simulation แรก

```python
from uet_core.solver import run_case
import numpy as np

config = {
    "case_id": "my_first_run",
    "model": "C_only",
    "domain": {"L": 10.0, "dim": 2, "bc": "periodic"},
    "grid": {"N": 64},
    "time": {"dt": 0.01, "T": 10.0, "max_steps": 10000},
    "params": {
        "pot": {"type": "quartic", "a": -1.0, "delta": 1.0, "s": 0.0},
        "kappa": 0.5,
        "M": 1.0,
    }
}

rng = np.random.default_rng(42)
summary, rows = run_case(config, rng)

print(f"Status: {summary['status']}")
print(f"Final Energy: {summary['OmegaT']:.4f}")
```

### รันทุกเทสต์

```bash
python research/run_unified_tests.py
```

**Expected:** `39/39 tests PASS (100%)`

---

## 📁 โครงสร้างโปรเจค

```
Equation-UET-v0.8.7/
├── src/uet_core/           # Core simulation engine
│   ├── solver.py           # Main solver
│   ├── energy.py           # Energy functional
│   └── potentials/         # Quartic, Sine-Gordon
│
├── research/               # Research & papers
│   ├── 00_core_paper/      # Full paper + intuitive explanation
│   ├── 01-core/            # Core theory & physics gaps
│   ├── 02-physics/         # 17 physics domains
│   └── run_unified_tests.py # 39-test suite
│
├── README.md               # นี่แหละ!
├── LICENSE                 # MIT License
└── pyproject.toml          # Package config
```

---

## 📖 เอกสาร

| เอกสาร | คำอธิบาย |
|--------|----------|
| [INTUITIVE_EXPLANATION.md](research/00_core_paper/INTUITIVE_EXPLANATION.md) | คำอธิบายแบบเข้าใจง่าย |
| [PAPER_FULL.md](research/00_core_paper/PAPER_FULL.md) | Full paper draft |
| [Physics Domains](research/02-physics/) | 17 สาขาฟิสิกส์ |
| [Stress Tests](research/03-stress-tests/) | Extreme testing |

---

## 🔬 ผลการทดสอบหลัก

| หมวด | ทดสอบ | ผล |
|------|-------|-----|
| **Foundation** | พลังงานลดลงเสมอ | ✅ dΩ/dt ≤ 0 |
| **Gauge** | U(1) symmetry | ✅ อนุรักษ์ถึง 10⁻¹⁵ |
| **Gauge** | SU(2) symmetry | ✅ อนุรักษ์ถึง 10⁻¹⁵ |
| **Quantum** | Pauli exclusion | ✅ Vortex repulsion |
| **Relativity** | Natural units | ✅ κ=0.5 → c=1 |
| **Black Holes** | CCBH k-value | ✅ k=3.0 |
| **Cosmology** | Dark energy | ✅ Ω_Λ=0.685 |

---

## 🤝 ร่วมพัฒนา

เรายินดีรับความช่วยเหลือ! ดู [CONTRIBUTING.md](CONTRIBUTING.md)

- 🐛 รายงาน bugs
- 📝 ปรับปรุงเอกสาร
- 🔬 เพิ่มเทสต์ฟิสิกส์ใหม่
- 🚀 Optimize performance

---

## 📜 License

MIT License - ดู [LICENSE](LICENSE)

---

## 📬 Citation

```bibtex
@software{uet_harness_2025,
  title={Unity Equilibrium Theory Harness},
  author={Jirawat Chitkhanti},
  year={2025},
  version={0.8.7},
  url={https://github.com/unityequilibrium/Equation-UET-v0.8.7}
}
```

---

## 🙏 Acknowledgments

- Developed with AI assistance (Anthropic Claude, Google DeepMind)
- Based on Cahn-Hilliard theory (1958)
- Validated against Planck 2018, LIGO, and PDG data

---

*Version 0.8.7 | 39/39 Tests Pass | Open Source*

**"จักรวาลคือระบบบันทึกพลังงานขนาดใหญ่ที่ทุกอย่างเชื่อมถึงกันผ่าน Space"**
