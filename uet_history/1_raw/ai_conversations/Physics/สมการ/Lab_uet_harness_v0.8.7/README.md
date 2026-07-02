# Unity Equilibrium Theory (UET) Harness

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

**Mathematical framework for gradient flow dynamics | กรอบทางคณิตศาสตร์สำหรับพลวัตการไหลแบบเกรเดียนท์**

> ⚠️ **[อ่านข้อจำกัด](research/00_core_paper/LIMITATIONS.md)** — ทฤษฎีนี้มีขอบเขตที่ชัดเจน
> 🎯 **[ท้าทายทฤษฎีนี้](research/00_core_paper/CHALLENGE.md)** — เราต้องการ peer review

---

## 🤔 UET คืออะไร?

### คำอธิบายง่ายๆ

UET เป็น **mathematical framework** สำหรับศึกษาระบบที่:
- วิ่งหาจุดสมดุล (gradient flow)
- มี phase separation (เหมือน oil-water)
- มี pattern formation (domains, defects)

### สมการหลัก: Cahn-Hilliard

$$\partial_t \phi = \nabla^2 \frac{\delta \Omega}{\delta \phi}$$

**ความหมาย:**
> Field φ เปลี่ยนแปลงตาม gradient ของ energy functional Ω
> ระบบ relax ไปหาจุดที่ Ω ต่ำสุด

---

## ✅ สิ่งที่ UET ทำได้

| ความสามารถ | สถานะ | หมายเหตุ |
|------------|-------|----------|
| Lyapunov stability | ✅ | dΩ/dt ≤ 0 เสมอ |
| Pattern formation | ✅ | Domains, vortices |
| Phase separation | ✅ | Goldstone modes |
| Thermodynamic analogs | ✅ | Energy-like behavior |

## ⚠️ สิ่งที่ UET ยังไม่สามารถทำได้

| Limitation | สาเหตุ | ดู |
|------------|--------|-----|
| Gauge symmetries | Gradient flow ≠ gauge structure | [LIMITATIONS.md](research/00_core_paper/LIMITATIONS.md) |
| Standard Model | Thermodynamics → gravity only | [LITERATURE_NOTES.md](research/00_core_paper/LITERATURE_NOTES.md) |
| Lorentz invariance | Euclidean formulation | [HONEST_POSITION.md](research/00_core_paper/HONEST_POSITION.md) |

---

## 🚀 Quick Start

### ติดตั้ง

```bash
git clone https://github.com/unityequilibrium/Equation-UET-v0.8.7.git
cd Equation-UET-v0.8.7

python -m venv .venv
.venv\Scripts\activate  # Windows

pip install -e .
```

### รัน Simulation

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
print(f"Status: {summary['status']}, Energy: {summary['OmegaT']:.4f}")
```

---

## 📁 โครงสร้างโปรเจค

```
Equation-UET-v0.8.7/
├── src/uet_core/           # Core simulation engine
├── research/               # Research & papers
│   ├── 00_core_paper/      # Papers + limitations
│   ├── 04-extensions/      # Mexican Hat, SU3, Memory tests
│   └── ปรับ/               # Original UECT documents
├── README.md
└── pyproject.toml
```

---

## 📖 เอกสารสำคัญ

| เอกสาร | คำอธิบาย |
|--------|----------|
| [LIMITATIONS.md](research/00_core_paper/LIMITATIONS.md) | **อ่านก่อน!** ข้อจำกัดของทฤษฎี |
| [HONEST_POSITION.md](research/00_core_paper/HONEST_POSITION.md) | สิ่งที่ทำได้/ไม่ได้ |
| [DEEP_ANALYSIS.md](research/00_core_paper/DEEP_ANALYSIS.md) | วิเคราะห์ปัญหา |
| [BEFORE_VS_NOW.md](research/00_core_paper/BEFORE_VS_NOW.md) | UECT vs UET |
| [LITERATURE_NOTES.md](research/00_core_paper/LITERATURE_NOTES.md) | Jacobson, Verlinde |

---

## 🔬 Extension Tests

| ทดสอบ | ผล | Plot |
|-------|-----|------|
| Mexican Hat (Goldstone) | ✅ Symmetry breaking | [View](research/04-extensions/01-mexican-hat/) |
| SU3 Network (Confinement) | ⚠️ Pattern, no conservation | [View](research/04-extensions/02-su3-network/) |
| Memory/Lorentz | ✅ Finite speed | [View](research/04-extensions/03-memory-lorentz/) |

---

## 🤝 ร่วมพัฒนา

เรายินดีรับ:
- 🐛 Bug reports
- 📝 Documentation improvements
- 🔬 Independent verification
- 📊 External peer review

ดู [CONTRIBUTING.md](CONTRIBUTING.md)

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

- Based on Cahn-Hilliard theory (Cahn & Hilliard, 1958)
- Developed with AI assistance
- Inspired by Jacobson (1995) and Verlinde (2010)

---

*Version 0.8.7 | Open Source | MIT License*

**"Mathematical exploration of gradient flow dynamics"**
