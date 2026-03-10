---
title: "Rust Engine"
description: "การคอมไพล์และติดตั้ง UET Core Engine ด้วย Rust เพื่อประสิทธิภาพสูงสุด"
---

# Rust Engine Installation

**UET Core Engine** ถูกเขียนด้วยภาษา Rust เพื่อมอบประสิทธิภาพสูงสุดในการคำนวณ แยกระบบ Thread ได้ดีเยี่ยม และรับประกันความปลอดภัยของหน่วยความจำ (Memory Safety) ซึ่งเหมาะสำหรับการคำนวณสมการ UET ที่มีความซับซ้อนสูงและต้องการทำ High-Frequency Simulation

## Prerequisites (สิ่งที่ต้องเตรียม)

- **Rust Toolchain** (เวอร์ชันล่าสุด) ติดตั้งผ่าน `rustup`
- **PostgreSQL** (หรือใช้ Docker เพื่อรัน Database)
- **C++ Build Tools** (สำหรับคอมไพล์ไลบรารีบางตัว เช่น FastEmbed)
  - Ubuntu: `sudo apt install build-essential`
  - Windows: `Visual Studio Build Tools` หรือ `MinGW`
  - macOS: `xcode-select --install`

## การติดตั้งและการคอมไพล์ (Build from Source)

1. โคลนโปรเจกต์และเข้าไปที่โฟลเดอร์ `uet_api`:

```bash
git clone https://github.com/unityequilibrium/UnityEquilibriumTheory.git
cd UnityEquilibriumTheory/uet_api
```

2. กำหนดค่าตัวแปรสภาพแวดล้อม (Environment Variables) โดยการคัดลอกไฟล์ `.env.example` เป็น `.env` และแก้ไขค่า `DATABASE_URL`:

```bash
cp ../.env.example ../.env
# แก้ไขไฟล์ .env ให้ DATABASE_URL ชี้ไปยัง PostgreSQL ของคุณ
```

3. คอมไพล์โปรเจกต์ (โหมด Release เพื่อประสิทธิภาพสูงสุด):

```bash
cargo build --release
```

*หมายเหตุ: การคอมไพล์ครั้งแรกอาจใช้เวลานาน เนื่องจากมีการดาวน์โหลดและคอมไพล์ไลบรารี FastEmbed และ ONNX Runtime*

4. รัน Database Migrations (เพื่อให้แน่ใจว่าตารางข้อมูลครบถ้วน):

```bash
cargo sqlx migrate run
```

5. รันเซิร์ฟเวอร์:

```bash
./target/release/uet_api
# หรือรันผ่าน cargo โดยตรง: cargo run --release
```

เซิร์ฟเวอร์จะเริ่มต้นทำงานที่ `http://127.0.0.1:3000`

## โครงสร้างของ Rust Engine

โค้ดใน `uet_api/src/` ประกอบด้วยโมดูลสำคัญดังนี้:

- `main.rs`: จุดเริ่มต้นของแอปพลิเคชัน การตั้งค่า Axum Router และ Middleware
- `mcp.rs`: โลจิกสำหรับ Model Context Protocol รวมถึง Vector Search และ LLM Integration
- `db.rs`: การเชื่อมต่อและจัดการฐานข้อมูล PostgreSQL ผ่าน SQLx
- `auth.rs`: ระบบยืนยันตัวตนและการสร้าง/ตรวจสอบ JWT Token
- `handlers.rs`: ฟังก์ชัน API Endpoints ต่างๆ (เช่น `/api/auth/login`, `/api/mcp/query`)
- `models.rs`: โครงสร้างข้อมูล (Structs) ที่ใช้ในการรับส่งข้อมูลแบบ JSON

## การพัฒนาและทดสอบ (Development)

หากคุณต้องการแก้ไขโค้ด แนะนำให้รันด้วยคำสั่ง `cargo watch` เพื่อให้เซิร์ฟเวอร์รีสตาร์ทอัตโนมัติเมื่อมีการแก้ไขไฟล์:

```bash
cargo install cargo-watch
cargo watch -x run
```

สำหรับรัน Unit Tests:

```bash
cargo test
```
