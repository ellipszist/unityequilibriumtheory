---
title: "Quickstart"
description: "เริ่มต้นใช้งาน UET Platform อย่างรวดเร็วที่สุด"
---

# Quickstart

บทความนี้จะแนะนำวิธีที่รวดเร็วที่สุดในการติดตั้งและเริ่มต้นใช้งาน **UET Platform** บนเครื่องของคุณ

## Prerequisites (สิ่งที่ต้องมี)

ก่อนเริ่มต้น ตรวจสอบให้แน่ใจว่าเครื่องของคุณมี:
- **Node.js** (v18+) - สำหรับรัน Web Frontend
- **Python** (v3.10+) - สำหรับระบบประมวลผลและการจำลอง
- **Rust** (Cargo) - สำหรับ Core Engine (ถ้าต้องการคอมไพล์ใหม่)
- **Docker** - (ทางเลือก) สำหรับการรันแบบ Containerized

## 1. Installation (การติดตั้งเบื้องต้น)

โคลน Repository ลงมาที่เครื่องของคุณ:

```bash
git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
cd UnityEquilibriumTheory
```

## 2. Start the Backend API (รันระบบหลังบ้าน)

API ของ UET เขียนด้วย Rust (Axum framework)

```bash
cd uet_api
cargo run
```
*API จะทำงานที่พอร์ต `http://localhost:3000` (หรือพอร์ตตามที่ระบุในไฟล์ `.env`)*

## 3. Start the Web Frontend (รันหน้าเว็บ)

เปิดอีกหน้าต่าง Terminal แล้วเข้าไปที่โฟลเดอร์ Web Frontend:

```bash
cd uet_web
npm install
npm run dev
```
*หน้าเว็บจะทำงานที่ `http://localhost:3002` (หรือพอร์ตถัดไปที่ว่าง)*

## 4. Play with the Knowledge Base (ทดสอบระบบ)

UET มาพร้อมกับระบบ Knowledge Base (MCP) ที่สามารถคุยและถามคำถามเกี่ยวกับฟิสิกส์และสมการได้
ไปที่เมนู **Dashboard** ในหน้าเว็บ หรือเรียกผ่าน API โดยตรง:

```bash
curl -X POST http://localhost:3000/api/mcp/query \
     -H "Content-Type: application/json" \
     -d '{"query": "อธิบาย Master Equation ให้ฟังหน่อย"}'
```

## Next Steps

เมื่อติดตั้งสำเร็จแล้ว คุณสามารถเลือกอ่านตามความสนใจของคุณ:
- [Architecture Overview](/docs/01_Introduction/architecture) - เพื่อทำความเข้าใจโครงสร้างของระบบทั้งหมด
- [Running Simulations](/docs/04_User_Guides/running-simulations) - เพื่อเรียนรู้วิธีการจำลองโมเดลต่างๆ ของ UET
