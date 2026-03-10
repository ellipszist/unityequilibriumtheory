---
title: "Python Client SDK"
description: "Reference สำหรับ Python SDK เพื่อใช้งานแบบจำลองและเชื่อมต่อ API"
---

# Python Client SDK Reference

คลาสและเมธอดหลักๆ ในแพ็คเกจ `uet-sdk` สำหรับใช้งานบน Python

---

## 1. Class: `UETClient`
(อยู่ใน `uet.client`)

คลาสนี้ใช้สำหรับเชื่อมต่อกับ REST API เพื่อดึงข้อมูล หรือคุยกับฐานข้อมูล Knowledge Base

**Constructor:**
```python
UETClient(api_key: str, base_url: str = "https://api.uet.tech")
```

**Methods:**
- `get_topics() -> List[dict]`
  ดึงรายชื่อโดเมนทั้งหมดของทฤษฎี

- `get_equation(name: str) -> dict`
  ดึงข้อมูลของสมการ เช่น `master_equation` หรือ `scale_equation` พร้อมพารามิเตอร์

- `search_knowledge_base(query: str, limit: int = 5) -> List[dict]`
  ค้นหาเอกสารเชิงความหมาย คืนค่าข้อความที่เกี่ยวข้องพร้อมคะแนน (Score)

---

## 2. Class: `EquilibriumSimulator`
(อยู่ใน `uet.simulation`)

เครื่องมือสร้างแบบจำลองทางคณิตศาสตร์เพื่อดูพัฒนาการของระบบ

**Constructor:**
```python
EquilibriumSimulator(scale: float, time_step: float = 0.1)
```

**Methods:**
- `set_initial_state(capacity: float, information_density: float, inflow: float, outflow: float)`
  กำหนดค่าเริ่มต้นของระบบ

- `set_parameters(kappa: float = None, beta: float = None, lambda_factor: float = None)`
  ปรับจูนพารามิเตอร์ของสมการ UET

- `run(steps: int) -> SimulationResult`
  รันแบบจำลองตามจำนวนรอบที่ระบุ คืนค่าผลลัพธ์เป็นออบเจกต์ที่เก็บประวัติ

---

## 3. Class: `SimulationResult`
(คืนค่ามาจาก `simulator.run()`)

**Properties & Methods:**
- `history: List[dict]` - ประวัติค่าต่างๆ ในแต่ละ time-step
- `final_capacity: float` - พลังงาน/ทรัพยากรสุดท้ายที่เหลืออยู่
- `to_dataframe() -> pandas.DataFrame` - แปลงประวัติเป็น DataFrame
- `plot_trajectory(x_axis: str, y_axis: List[str], title: str)` - (ต้องการ `matplotlib`) พล็อตกราฟเส้นแนวโน้ม

---

## 4. Module: `uet.constants`

ตัวแปรคงที่ (Constants) ที่จำเป็นต้องใช้ในการคำนวณ:
- `PLANCK_SCALE`: `1e-35`
- `MACRO_SCALE`: `1.0`
- `ASTRO_SCALE`: `1e20`
- `DEFAULT_KAPPA`: `0.01`
- `DEFAULT_BETA`: `0.5`
