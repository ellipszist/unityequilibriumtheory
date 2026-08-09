# Section 3 Dependency Map

Status: `PASS`  
Section Blueprint: `section-03-v1`  
Profile: `THREE_BOOK_SECTION`  

---

## 1. Cross-Volume Dependency Matrix

| Dependency ID | From | To | Dependency & Shared Concept | Handoff Description | Current Status | Controller |
| :---: | :---: | :---: | :--- | :--- | :---: | :---: |
| `D03-01` | Volume 1 | Volume 2 | **Discourse & 4-Power Model $\rightarrow$ Hardened Tradition** | เล่ม 1 ส่งมอบมโนทัศน์เรื่อง *วาทกรรม, การเลือกพูด (Selective Framing)* และ *ทฤษฎีอำนาจ 4 มิติ* ให้เล่ม 2 นำไปใช้ผ่ากลไกการตกผลึกเป็น *จารีต (Tradition)* | `PASS` | `S05` |
| `D03-02` | Volume 2 | Volume 3 | **Authoritarian Anatomy & Pluralistic Ignorance $\rightarrow$ New Tradition Design** | เล่ม 2 ส่งมอบผลการวิเคราะห์ปัญหากายวิภาคอำนาจนิยม สภาวะสมยอมเทียม (*Pluralistic Ignorance*) และจารีตที่กดทับ ให้เล่ม 3 นำไปสลายอคติและสถาปนา *จารีตใหม่ที่ดี* | `PASS` | `S05` |
| `D03-03` | Volume 1 | Volume 3 | **Selective Framing Mechanism $\rightarrow$ Ethical Selective Framing** | เล่ม 1 ส่งมอบกลไกการเลือกพูด (Selective Framing) ให้เล่ม 3 นำไปใช้เชิงจริยธรรม (*Ethical Selective Framing*) สกัดมรดกดีเดิม (พุทธ/เล่าจื้อ) | `PASS` | `S05` |
| `D03-04` | Section | Volumes 1-3 | **Shared Terms & Controlled Definitions** | ศัพท์สากลประจำเซกชัน (*Discourse, Selective Framing, 4-Power Model, Tradition, Pluralistic Ignorance, Moral-Legal Tech*) ถูกควบคุมนิยามตรงกันที่ `SHARED_TERMS.md` | `PASS` | `SHARED_TERMS.md` |
| `D03-05` | Volume 3 | Section | **Section Synthesis & Bounded Conclusion** | เล่ม 3 สรุปบทสังเคราะห์ของ Section 3 ทั้งหมด โดยแยกแยะชัดเจนระหว่าง *สิ่งที่พิสูจน์แล้ว*, *ข้อเสนอเชิงโครงสร้าง*, และ *ขอบเขตข้อจำกัด* | `PASS` | `S07` |

---

## 2. Handoff Safeguards & Reopen Rules

1. **Prerequisite Guarantee:** เล่ม 2 จะไม่อธิบายจารีตลอยๆ โดยไม่เชื่อมกลับมายังกรอบวาทกรรมและอำนาจ 4 มิติที่เล่ม 1 สร้างไว้
2. **Solution Alignment:** เล่ม 3 จะไม่ออกแบบทางออกเชิงจริยธรรมโดยไม่ตอบโจทย์ปัญหากายวิภาคอำนาจนิยมและกลไกสมองที่เล่ม 2 วิเคราะห์ไว้
3. **Reopen Rule:** หากเล่มใดเปลี่ยนแปลงนิยามศัพท์ร่วม หรือเปลี่ยนบทบาทการส่งต่อ (Handoff) ให้ทำการ Reopen เกต S04-S05 ทันที
