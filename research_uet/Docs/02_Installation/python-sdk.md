---
title: "Python SDK"
description: "การติดตั้งและใช้งาน UET Python SDK สำหรับนักวิจัยและ Data Scientist"
---

# Python SDK

**UET Python SDK** เป็นไลบรารีที่ออกแบบมาเพื่อให้นักวิจัย, Data Scientist, และวิศวกรสามารถดึงข้อมูลสมการ ทฤษฎี และรันแบบจำลอง (Simulations) ของ Unity Equilibrium Theory ได้อย่างง่ายดายผ่านภาษา Python

## การติดตั้ง (Installation)

*(กำลังอยู่ในช่วงพัฒนา ยังไม่เปิดให้ดาวน์โหลดผ่าน PyPI สาธารณะ)*

คุณสามารถติดตั้งได้จาก Source code โดยตรง:

```bash
git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
cd UnityEquilibriumTheory/research_uet/python_sdk
pip install -e .
```

หรือหากคุณมีไฟล์ `requirements.txt` สามารถรัน:

```bash
pip install -r requirements.txt
```

## การใช้งานเบื้องต้น (Basic Usage)

### 1. การดึงข้อมูลสมการหลัก (The Master Equation)

```python
from uet.core import MasterEquation

# โหลดสมการหลักของ UET
eq = MasterEquation.load()

# แสดงผลสมการแบบ LaTeX
print(eq.to_latex())

# แสดงรายชื่อตัวแปรทั้งหมดและคำอธิบาย
for param in eq.parameters:
    print(f"{param.symbol}: {param.description} (Value: {param.value})")
```

### 2. การจำลองสภาวะ (Running a Simulation)

คุณสามารถสร้างการจำลองโดยใช้สัจพจน์และพารามิเตอร์ของ UET

```python
from uet.simulation import KappaSimulator
from uet.constants import PLANCK_SCALE

# สร้าง Simulator ที่สเกลของพลังงานระดับ Planck
sim = KappaSimulator(scale=PLANCK_SCALE)

# กำหนดค่าตัวแปรเบื้องต้น
sim.set_initial_state(
    gradient_penalty=0.5,
    coupling_constant=1.0,
    exchange_rate=0.1
)

# รันแบบจำลอง 1,000 steps
results = sim.run(steps=1000)

# พล็อตกราฟผลลัพธ์
results.plot_energy_distribution()
```

### 3. การเชื่อมต่อกับ UET Knowledge Base (ผ่าน API)

SDK สามารถดึงข้อมูลจาก API ของ UET Platform ได้โดยตรง

```python
from uet.client import UETClient

# เชื่อมต่อ API (ต้องใช้ API Key ที่ได้จากหน้า Dashboard)
client = UETClient(api_key="your_api_key_here")

# ค้นหาข้อมูลทฤษฎีด้วย Natural Language
response = client.search_knowledge_base("อธิบายความเชื่อมโยงระหว่าง Graphene กับ UET")

print(response.content)
```

## โมดูลหลักใน SDK

- `uet.core` - โครงสร้างหลัก, สมการ, และสัจพจน์ (Axioms)
- `uet.simulation` - เครื่องมือสำหรับการรันแบบจำลองทางคณิตศาสตร์
- `uet.constants` - ค่าคงที่ทางฟิสิกส์และค่าคงที่เฉพาะของ UET
- `uet.visualization` - เครื่องมือสร้างกราฟและ Visualize ข้อมูลแบบ 3D
- `uet.client` - HTTP Client สำหรับคุยกับ UET Backend API
