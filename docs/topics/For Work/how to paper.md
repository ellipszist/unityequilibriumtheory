# คู่มือการเขียน Paper วิชาการ (UET Standard)

**กลยุทธ์:** เน้น "Modular Paper" (1 หัวข้อ = 1 เปเปอร์) เพื่อความรวดเร็ว กระชับ และใช้งานได้จริง ไม่ต้องเขียน Thesis เล่มยักษ์ที่รวมทุกอย่าง แต่เน้นเจาะลึกเป็นเรื่องๆ ไป

---

## 🛠️ เครื่องมือหลัก: LaTeX Template
เรามีเทมเพลตมาตรฐานอยู่ที่: 
`docs/topics/Work/UET_PAPER_TEMPLATE.tex`

**ทำไมต้อง LaTeX?**
- รูปเล่มดูเป็นมืออาชีพ (Professional Look) สำหรับส่งวารสาร (Journal)
- จัดการสมการคณิตศาสตร์และรูปภาพได้นิ่ง ไม่เด้งไปมาเหมือน Word
- รองรับการทำ Reference มาตรฐานสากล

---

## 📝 โครงสร้าง 8 หัวข้อหลัก (กระชับ & ตรงประเด็น)

### 1. Title & Abstract
- **Title:** สั้น กระชับ บอกชัดว่าแก้ปัญหาอะไร (เช่น "Room-Temperature Stopped Light via Graphene Lattice")
- **Abstract:** สรุป 15 บรรทัดจบ: ปัญหา -> วิธีแก้ (UET) -> ผลลัพธ์ (Data) -> ลิงค์ Open Source

### 2. Introduction
- **Background:** ปูพื้นฐานสั้นๆ
- **Gap:** ชี้จุดตายของทฤษฎีเดิมที่ยังทำไม่ได้ (นี่คือจุดที่เราจะเข้าไปเสียบ)

### 3. Literature Review
- อ้างอิงงานระดับโลก (Einstein, Hawking, NIST) เพื่อยืนยันว่าเราเข้าใจ Standard Model ดีพอ

### 4. Theoretical Framework (UET Master Equation)
- ใส่สมการหลัก $\Omega$ และอธิบายว่ามันลดรูปมาแก้ปัญหานี้ได้อย่างไร
- ระบุค่า Parameter ที่ใช้จาก `uet_parameters.py`

### 5. Methodology (Open Source Strategy)
- ระบุชื่อ `Engine` และ `Proof` ที่ใช้รัน
- ใส่ลิงค์ GitHub ของโปรเจกต์เพื่อให้คนอื่นมาตรวจสอบและรันซ้ำได้ทันที

### 6. Results
- ใส่กราฟจาก `Result/01_Showcase/` (สำหรับรูปสวย) หรือ `Result/02_Figures/` (สำหรับกราฟเทคนิค)
- เน้นความแม่นยำ (Accuracy) และประสิทธิภาพ (Efficiency)

### 7. Discussion & Comparison
- **UET vs Standard:** เปรียบเทียบผลของเรากับคู่แข่ง (Competitor)
- **Impact:** บอกว่าผลลัพธ์นี้เปลี่ยนโลกยังไง (เช่น ลดต้นทุนผลิต Graphene 10 เท่า)

### 8. Conclusion & Future Work
- สรุปสั้นๆ และบอกว่า Topic นี้จะไปเชื่อมกับ Topic ถัดไปใน Roadmap อย่างไร

## 🖼️ หัวใจสำคัญ: Visual Logic (ต้องมีรูปภาพ/ไดอะแกรม!)

**"ถ้าภาพเดียวอธิบายได้ อย่าใช้พันคำพูด"** 
ในวงการวิชาการยุคใหม่ เรียกว่า **Graphical Abstract** หรือ **Schematic Diagram** ครับ การใส่ไดอะแกรมไม่ใช่เรื่องผิดระเบียบ แต่เป็น **"แต้มต่อ"** ที่ทำให้เปเปอร์เราถูกอ้างอิง (Citing) ได้ง่ายขึ้น

**สิ่งที่ต้องใส่ในเปเปอร์ UET:**
1.  **Conceptual Logic Map:** รูปที่แสดงการเชื่อมโยงจาก "ปัญหา (Standard Model)" ผ่าน "สะพาน (UET)" ไปสู่ "ผลลัพธ์ (Solution)"
2.  **High-Fidelity Plots:** กราฟที่สะอาดตา บอกหน่วยชัดเจน (ดึงจากโฟลเดอร์ Result)
3.  **Matrix/Architecture Table:** หากเป็นเรื่อง Algorithm ให้ใส่ตารางเปรียบเทียบที่เห็นความต่างชัดเจน

---

## 🚀 ขั้นตอนการใช้งาน
1. Copy `UET_PAPER_TEMPLATE.tex` ไปไว้ในโฟลเดอร์ `Paper/` ของ Topic นั้นๆ
2. ดึงข้อมูลจากไฟล์ `ANALYSIS_xx.md` มาใส่ในหัวข้อที่เกี่ยวข้อง
3. **สร้างรูปภาพ:** แปลง Mermaid Diagram หรือ Logic ที่คุยกันเป็นไฟล์ภาพ (.png หรือ .pdf) แล้วประทับลงในเปเปอร์
4. Compile เป็น PDF และเตรียมส่ง Review!
