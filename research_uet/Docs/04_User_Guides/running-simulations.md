---
title: "Running Simulations"
description: "คู่มือการรันแบบจำลองและตั้งค่าพารามิเตอร์ของ UET"
---

# Running Simulations

การจำลอง (Simulation) เป็นวิธีหลักในการพิสูจน์และใช้งาน Unity Equilibrium Theory (UET) บทความนี้จะสอนวิธีรันแบบจำลองพื้นฐานโดยใช้ UET Python SDK

## 1. การเตรียมสภาพแวดล้อม

ตรวจสอบให้แน่ใจว่าคุณได้ติดตั้ง Python SDK แล้ว (ดูคู่มือ [Python SDK Installation](/docs/02_Installation/python-sdk))

```python
import uet
from uet.simulation import EquilibriumSimulator
from uet.constants import MACRO_SCALE
```

## 2. การสร้าง Simulator

ขั้นตอนแรกคือการสร้างอินสแตนซ์ของ Simulator และกำหนดสเกลที่คุณต้องการจำลอง

```python
# สร้างแบบจำลองในระดับ Macro (เช่น ระบบสิ่งแวดล้อมหรือเศรษฐกิจขนาดเล็ก)
sim = EquilibriumSimulator(scale=MACRO_SCALE)
```

## 3. การกำหนดเงื่อนไขเริ่มต้น (Initial Conditions)

คุณต้องตั้งค่าตัวแปรเบื้องต้นสำหรับสมการหลัก (The Master Equation):

```python
sim.set_initial_state(
    capacity=100.0,          # พลังงานหรือทรัพยากรตั้งต้น (C)
    information_density=0.8, # ความหนาแน่นของข้อมูล (I)
    inflow=5.0,              # อัตราทรัพยากรไหลเข้า (J_in)
    outflow=2.0              # อัตราทรัพยากรไหลออก (J_out)
)

# ปรับจูนพารามิเตอร์ความต้านทานและกฎเกณฑ์
sim.set_parameters(
    kappa=0.01,  # แรงต้านการเปลี่ยนแปลง (Inertia)
    beta=0.5     # ความเชื่อมโยงของข้อมูลกับพลังงาน
)
```

## 4. รันการจำลอง (Execution)

เมื่อทุกอย่างพร้อม ให้รันการจำลองตามจำนวน Step ที่ต้องการ:

```python
# รันการจำลองจำนวน 500 Time-steps
results = sim.run(steps=500)

print(f"Simulation completed. Final Capacity: {results.final_capacity:.2f}")
```

## 5. การวิเคราะห์ผลลัพธ์

คุณสามารถดึงข้อมูลที่บันทึกไว้ในแต่ละ Time-step ออกมาวิเคราะห์เป็น Pandas DataFrame หรือพล็อตกราฟได้:

```python
# ดึงเป็น DataFrame
df = results.to_dataframe()
print(df.head())

# พล็อตกราฟพฤติกรรมระบบ
results.plot_trajectory(
    metrics=['capacity', 'information', 'entropy'],
    title="System Evolution Over Time"
)
```

## Advanced: Multi-Agent Simulation

UET รองรับการรันแบบจำลองที่ซับซ้อนขึ้นซึ่งมีหลายๆ ระบบย่อย (Agents) โต้ตอบกัน

```python
from uet.simulation import MultiAgentSimulator

multi_sim = MultiAgentSimulator(num_agents=10)
multi_sim.apply_game_theory_rules(strategy="cooperative_nash")

results = multi_sim.run(steps=1000)
results.plot_network_coherence()
```

ผลลัพธ์นี้จะแสดงให้เห็นว่า $\lambda$ (Coherence term) ทำงานอย่างไรเมื่อเกิดความแตกต่างกันระหว่าง Agents
