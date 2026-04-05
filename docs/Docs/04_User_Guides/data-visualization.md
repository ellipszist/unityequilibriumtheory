---
title: "Data Visualization"
description: "การแปลงข้อมูลเชิงนามธรรมจากสมการ UET ให้กลายเป็นกราฟที่เข้าใจได้"
---

# Data Visualization

เนื่องจาก Unity Equilibrium Theory (UET) เกี่ยวข้องกับมิติของข้อมูลที่ซับซ้อนและการเปลี่ยนแปลงตามกาลเวลา (Time-series) การใช้เครื่องมือ Visualize ข้อมูลจึงเป็นสิ่งที่หลีกเลี่ยงไม่ได้

UET SDK มาพร้อมกับระบบแสดงผลที่ถูกออกแบบมาเป็นพิเศษเพื่อให้เห็นถึงปฏิสัมพันธ์ระหว่าง พลังงาน (Energy) และ ข้อมูล (Information)

## 1. 2D Trajectory Plots

วิธียอดนิยมที่สุดในการดูว่าระบบกำลังเข้าสู่สมดุล (Equilibrium) หรือกำลังล่มสลาย (Collapse) คือการพล็อตกราฟเปรียบเทียบ Capacity ($C$) กับเวลา ($t$)

```python
from uet.visualization import UETPlotter

# ดึงผลลัพธ์จากการจำลองที่รันไว้แล้ว
plotter = UETPlotter(simulation_results)

# สร้างกราฟ 2 มิติ
plotter.plot_trajectory(
    x_axis="time",
    y_axis=["capacity", "information_density"],
    title="System Approach to Equilibrium"
)
```

**สิ่งที่ควรมองหาในกราฟ:**
- หากเส้น $C$ แกว่งตัวรุนแรง แสดงว่าระบบมีความขัดแย้งภายในสูง (High Game Penalty)
- หากเส้น $C$ และ $I$ เคลื่อนที่ลู่เข้าหากัน แสดงว่าระบบเริ่มตกผลึกข้อมูลและใช้พลังงานอย่างมีประสิทธิภาพ

## 2. Phase Space Diagrams (3D)

เพื่อดูว่าระบบถูกดึงดูดเข้าหาสถานะใดสถานะหนึ่ง (Attractor) หรือไม่ การพล็อตใน Phase Space คือคำตอบ

```python
plotter.plot_phase_space(
    x="capacity",      # แกน X = พลังงาน
    y="information",   # แกน Y = ข้อมูล
    z="entropy",       # แกน Z = ความไร้ระเบียบ
    interactive=True   # เปิดให้หมุนกราฟดูได้ใน Jupyter Notebook
)
```

หากจุดข้อมูลวิ่งวนเป็นวงกลมซ้ำๆ แสดงว่าระบบเข้าสู่ **Limit Cycle** (ระบบที่มีชีวิตและทำงานเป็นจังหวะ เช่น การเต้นของหัวใจ หรือวงจรเศรษฐกิจ)

## 3. Network Coherence Map

สำหรับแบบจำลอง Multi-agent ที่มีหลายๆ ระบบย่อยเชื่อมต่อกัน (เช่น การทำงานของสมอง หรือระบบนิเวศ) เราสามารถดูว่าพวกมัน "เข้าขากัน" หรือไม่ผ่าน Network Map

```python
plotter.plot_network_coherence(
    edge_weight_metric="lambda_penalty",
    node_size_metric="capacity",
    layout="force_directed"
)
```
- **Node ที่ใหญ่** = Agent ที่มีพลังงาน/อิทธิพลสูง
- **เส้นขอบสีแดง/หนา** = Agent สองตัวที่ขัดแย้งกันอย่างรุนแรง (ถูก $\lambda$ ลงโทษหนัก)
- **เส้นขอบสีเขียว/บาง** = Agent ที่มีความสอดคล้องกัน (Coherent)

## 4. Exporting Visuals

คุณสามารถบันทึกกราฟเพื่อนำไปใช้ใน Paper หรืองานวิจัยได้โดยตรง:

```python
plotter.save_figure("uet_results.png", dpi=300, format="png")
plotter.save_animation("system_evolution.mp4", fps=30)
```
