# AI Conversations — บทสนทนา AI

> โฟลเดอร์นี้เก็บบทสนทนากับ AI ที่สร้าง insight เกี่ยวกับ UET
> จัดเก็บแยกตาม discipline เพื่อให้ค้นหาง่ายเมื่อต้องสรุปใน Layer 2

---

## จุดประสงค์

บทสนทนากับ AI (ChatGPT, Claude, Gemini ฯลฯ) เป็นแหล่งข้อมูลดิบที่สำคัญ
ของการพัฒนา UET — หลาย concept และ derivation เกิดขึ้นจากกระบวนการสนทนา

ที่นี่เก็บ **transcript ตามที่เป็น** ก่อนจะถูกวิเคราะห์และสรุปไปเป็น digest ใน Layer 2

---

## โครงสร้าง

```
ai_conversations/
├── Philosophy/
├── Physics/
├── Ethics/
├── Psychology/
├── Mathematics/
├── Economics/
├── Biology/
├── Chemistry/
├── History/
├── Political_Science/
├── Technology/
├── Legal_Philosophy/
└── Interdisciplinary/
```

---

## รายชื่อ Disciplines และวิธีเลือก

| # | Discipline | เลือกเมื่อเนื้อหาหลักเกี่ยวกับ... | UET Mapping Rule (ข้อควรจำ) |
|---|-----------|----------------------------------|---------------------------|
| 1 | **Philosophy** | การวิพากษ์วิจารณ์ (Critique) ระบบคิด/กรอบเดิม | ใน UET "ปรัชญา" คือการวิพากษ์วิจารณ์ล้วนๆ |
| 2 | **Physics** | กฎฟิสิกส์, สมการพลังงาน, สนาม, อุณหพลศาสตร์, **อภิปรัชญา (Metaphysics)** | อภิปรัชญาใน UET จัดเป็นฟิสิกส์ (ธรรมชาติของระบบและสนาม) |
| 3 | **Ethics** | คุณธรรม, จริยศาสตร์, moral framework | |
| 4 | **Psychology** | จิตสำนึก, การรับรู้, Frame of Reference, **ญาณวิทยา (Epistemology)** | ญาณวิทยาใน UET สัมพันธ์โดยตรงกับจิตวิทยา (การเกิดตัวรู้/การรับรู้) |
| 5 | **Mathematics** | สมการ, การพิสูจน์, ตรรกศาสตร์, โครงสร้างนามธรรม | |
| 6 | **Economics** | ระบบเศรษฐกิจ, ตลาด, **ญาณวิทยาเชิงเศรษฐศาสตร์ (Epistemology)** | ญาณวิทยาของ UET จะเชื่อมโยงไปถึงการตีมูลค่าในเศรษฐศาสตร์ด้วย |
| 7 | **Biology** | ระบบชีวภาพ, วิวัฒนาการ, สิ่งมีชีวิต | |
| 8 | **Chemistry** | ปฏิกิริยาเคมี, โมเลกุล, พันธะ | |
| 9 | **History** | บริบทเชิงประวัติศาสตร์, พัฒนาการของแนวคิด | |
| 10 | **Political_Science** | รัฐศาสตร์, ระบบการเมือง, ธรรมาภิบาล | |
| 11 | **Technology** | AI, computing, เทคโนโลยีประยุกต์ | |
| 12 | **Legal_Philosophy** | ปรัชญากฎหมาย, นิติศาสตร์, ระบบกฎหมาย | |
| 13 | **Interdisciplinary** | หัวข้อข้ามศาสตร์ เช่น ญาณวิทยาที่คาบเกี่ยวจิตวิทยาและเศรษฐศาสตร์ | |

### วิธีเลือก Discipline

```
                    เนื้อหาหลักอยู่ในศาสตร์เดียวชัดเจนไหม?
                           /                    \
                         ใช่                    ไม่ใช่
                          |                       |
                   เลือกศาสตร์นั้น          ข้ามกี่ศาสตร์?
                                            /          \
                                         2-3           มากกว่า 3
                                          |               |
                                   เลือกศาสตร์ที่      Interdisciplinary
                                   claim หลักอยู่       + ระบุศาสตร์ใน tags
```

**กฎง่าย ๆ:**
1. ถามว่า "claim หลักของบทสนทนาอยู่ในศาสตร์ไหน?" → เลือกศาสตร์นั้น
2. ถ้าข้ามหลายศาสตร์มาก → ใช้ `Interdisciplinary`
3. ใส่ศาสตร์ที่เกี่ยวข้องทั้งหมดไว้ใน `tags` ของ frontmatter

---

## วิธีเก็บบทสนทนา

### ขั้นตอน

1. **คัดเลือกบทสนทนา** — เก็บเฉพาะที่มีคุณค่า ไม่ต้องเก็บทุกบทสนทนา
2. **ระบุ discipline** — ใช้ตารางด้านบน
3. **ตั้งชื่อไฟล์:**
   ```
   YYYY-MM-DD_topic_name.md
   ```
4. **เพิ่ม frontmatter** ที่ต้นไฟล์
5. **วาง transcript** ใต้ frontmatter

### Frontmatter Template

```yaml
---
id: raw-YYYY-MM-DD-NNN
title: "ชื่อหัวข้อบทสนทนา"
date: YYYY-MM-DD
type: ai_conversation
source: claude                   # claude | chatgpt | gemini | other
discipline: Psychology           # เลือก 1 จาก 13 disciplines
tags: [tag1, tag2, tag3]
status: pending                  # pending | done
conversation_turns: 15           # (optional) จำนวนรอบการสนทนา
ai_model: claude-3.5-sonnet      # (optional) โมเดลที่ใช้
---
```

### ตัวอย่างไฟล์

```markdown
---
id: raw-2026-06-30-001
title: "Equilibrium dynamics ในระบบจิตสำนึก"
date: 2026-06-30
type: ai_conversation
source: claude
discipline: Psychology
tags: [consciousness, equilibrium, perception, Physics]
status: pending
---

# Equilibrium Dynamics ในระบบจิตสำนึก

## User
อยากให้วิเคราะห์ว่า concept ของ equilibrium ใน UET สัมพันธ์กับ...

## Assistant
จากกรอบของ UET สมดุลในระบบจิตสำนึกสามารถมองได้ว่า...

## User
แล้วถ้าเราพิจารณา Frame of Reference ด้วยล่ะ?

## Assistant
Frame of Reference เป็นตัวกำหนดว่า...
```

---

## ข้อควรระวัง

- **เก็บตามที่เป็น** — ไม่ต้องแก้ไขหรือ polish บทสนทนา การวิเคราะห์ทำใน Layer 2
- **AI-generated content** — ต้องตระหนักว่าเนื้อหาจาก AI ยังไม่ใช่หลักฐาน
  ต้องผ่านการ verify ก่อนใช้เป็น claim (ดู `docs/topics/For Work/03_AI_Usage_and_Governance.md`)
- **Claim discipline** — อย่าเขียน frontmatter ที่ทำให้ดูเหมือน claim แรงกว่าที่เป็น
  ใน raw data ให้ใช้ `status: pending` เสมอจนกว่าจะถูกสรุปใน Layer 2
