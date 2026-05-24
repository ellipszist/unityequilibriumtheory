# 🔬 ANALYSIS: การจำลองปฏิกิริยานิวเคลียร์ฟิชชัน (Fission Solver)

> [!WARNING]
> **Legacy claim boundary:** This file is a concept, paper draft, bibliography note, or legacy analysis note from an earlier drafting pass.
> It is not the topic status authority and must not be used to claim evaluated U-235 fission Q-value validation,
> fragment-mass prediction, broad heavy-binding validation, island-of-stability prediction, magic-number derivation,
> first-principles nuclear closure, or replacement of strong/weak nuclear forces. Current allowed claims are controlled by
> `README.md`, `LIMITATIONS.md`, `VERIFICATION_SPEC.md`, `FORMULA_AUDIT.md`, and
> `Result/artifacts/0_16_heavy_nuclei_verification.json`: U-235 checkpoint plus exothermic fission sanity only.

> **ไฟล์/สคริปต์:** `Code/01_Engine/Engine_Fission_Solver.py`
> **หน้าที่:** Engine (ตัวคำนวณหลัก)
> **สถานะ:** 🟢 สมบูรณ์ (FINAL)
> **ศักยภาพในการตีพิมพ์:** ⭐️ ปานกลาง

---

## 1. 📄 บทสรุปผู้บริหาร (Executive Summary)

> **"ฟิชชันไม่ใช่การแตกตัวของอนุภาค แต่คือการฉีกขาดของสนามพลังงาน (Field Topology Rupture)"**

*   **ปัญหาเดิม (Problem):** แบบจำลองมาตรฐาน (Liquid Drop Model) ใช้สมการกึ่งทดลอง (Semi-empirical) อธิบายการแตกตัว แต่ไม่ได้อธิบายว่า *ทำไม* นิวเคลียสถึงตัดสินใจแยกตัวในระดับพื้นฐานของสนามพลังงาน
*   **ทางออก (Solution):** UET จำลองนิวเคลียสในฐานะ "คลื่นโซลิตอน" (Soliton Field $C(x)$) โดยแปลงแรงผลักทางไฟฟ้า (Coulomb Repulsion) ให้อยู่ในรูปของ **เทอมแกมมา ($\gamma C^3$)** ในสมการหลัก
*   **ผลลัพธ์ (Result):** การจำลองแสดงให้เห็นว่า เมื่อค่า $\gamma$ สูงเกินค่าวิกฤต ($\gamma_{crit}$), นิวเคลียสจะยืดออกและขาดออกจากกันเองตามธรรมชาติ (Natural Fission) โดยที่เราไม่ต้องเขียนโค้ดสั่งให้มันตัดแบ่ง

---

## 2. 🧱 กรอบแนวคิดทฤษฎี

### 2.1 ตรรกะหลัก (The Core Logic)
เราใช้การแข่งขันของ 3 แรงในสมการเดียว:
1.  **แรงยึดเหนี่ยว ($\alpha$):** ทำหน้าที่ดึงดูดเนื้อสารเข้าหากัน (สร้างหลุมพลังงาน)
2.  **โครงสร้างผิว ($\kappa$):** ทำหน้าที่เป็นแรงตึงผิว พยายามรักษารูปทรงให้กลมเกลี้ยง
3.  **แรงผลักดัน ($\gamma$):** ทำหน้าที่เหมือนประจุบวกผลักกัน ถ้ามีมากเกินไปจะฉีกโครงสร้างออก

### 2.2 รากฐานคณิตศาสตร์
$$ \frac{\partial C}{\partial t} = -\alpha C - \gamma C^3 + \kappa \nabla^2 C $$
*   **สถานะเสถียร (Stable):** ค่า $\gamma$ ต่ำ (เช่น ตะกั่ว Pb-208) → นิวเคลียสรวมเป็นก้อนเดียว
*   **สถานะไม่เสถียร (Unstable):** ค่า $\gamma$ สูง (เช่น ธาตุหนัก Z>120) → นิวเคลียสจะยืดและขาด (Fission)

---

## 3. 🔬 การทำงานของโค้ด

### 3.1 ขั้นตอนการทำงาน (Algorithm Flow)
1.  **เตรียมการ:** สร้าง "หยดสาร" (Gaussian Drop) ที่เป็นตัวแทนของนิวเคลียส
2.  **วิวัฒนาการ:** รันสมการ Master Equation ข้ามเวลา (`dt=0.005`) เพื่อดูการเปลี่ยนแปลง
3.  **ตรวจจับ:** เฝ้าดู "ความหนาแน่นตรงกลาง" (Center Density) ถ้ามันลดลงจนเกือบศูนย์ในขณะที่มวลยังอยู่รอบๆ แสดงว่าเกิด "รู" ตรงกลาง -> **เกิดฟิชชัน (Fission)**

### 3.2 ตัวแปรสำคัญ
*   `gamma` (แรงผลัก): 0.05 สำหรับธาตุเสถียร vs 2.0 สำหรับธาตุหนักที่พร้อมแตกตัว
*   `alpha` (แรงยึด): -0.5 (ค่าติดลบแปลว่าดึงดูด)

---

## 4. 📊 ผลการทดลอง (Validation Results)

| เงื่อนไขการทดลอง | ค่า Gamma | ผลลัพธ์ที่ได้ | ผ่านเกณฑ์? |
| :--- | :--- | :--- | :--- |
| **นิวเคลียสเสถียร** | 0.05 | รัศมีคงที่ (RMS Radius ~0.85) ไม่แตกตัว | ✅ |
| **นิวเคลียสไม่เสถียร** | 2.0 | ตรวจพบการแตกตัว (Fission) ที่ Step 49 | ✅ |

> **บทพิสูจน์:** กราฟการจำลองแสดงให้เห็นการเปลี่ยนแปลงรูปร่างจากทรงกลม -> ทรงรี -> และขาดออกจากกัน (Topology Break) ได้จริงตามทฤษฎี

---

## 5. 🧠 วิเคราะห์ผลเชิงลึก

### 5.1 ทำไมธรรมชาติถึงยอม? (Why it works?)
เทอม $\gamma C^3$ สร้างความไม่เสถียรแบบ Non-linear เมื่อความหนาแน่น $C$ สูงเกินไป แรงผลักจะชนะแรงยึดเหนี่ยว ($\kappa$) ส่งผลให้ระบบต้อง "ลดพลังงาน" ด้วยการแบ่งตัวเองออกเป็น 2 ก้อนเล็ก ซึ่งมีพื้นที่ผิวรวมมากกว่าแต่พลังงานศักย์ต่ำกว่า

### 5.2 ข้อจำกัด (Limitation)
*   **เป็นเชิงคุณภาพ:** ค่า $\gamma$ ที่ใช้ยังเป็นหน่วยจำลอง (Simulation Units) ไม่ใช่หน่วย MeV จริง
*   **2 มิติ:** การจำลองนี้ทำในระนาบ 2D (ของจริงเป็น 3D)

---

## 6. 📝 บทสรุป
UET สามารถจำลอง "กลไก" ของนิวเคลียร์ฟิชชันได้จากสมการพื้นฐาน (Field Dynamics) โดยไม่ต้องใช้สูตรสำเร็จรูป
