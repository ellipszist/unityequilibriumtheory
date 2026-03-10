---
title: "REST Endpoints"
description: "เอกสารอ้างอิงสำหรับ API Endpoint ทั้งหมดของแพลตฟอร์ม"
---

# REST API Reference

ระบบ API ของ UET ถูกออกแบบมาตามมาตรฐาน RESTful รองรับการรับ-ส่งข้อมูลในรูปแบบ JSON

**Base URL:** `http://localhost:3000/api` (สำหรับ Local) หรือ `https://api.uet.tech` (สำหรับ Production)

---

## Authentication

### `POST /auth/register`
สร้างบัญชีผู้ใช้ใหม่
- **Body:** `{"username": "...", "email": "...", "password": "..."}`
- **Response:** `200 OK` พร้อมข้อมูล User ID

### `POST /auth/login`
เข้าสู่ระบบเพื่อรับ JWT Token
- **Body:** `{"email": "...", "password": "..."}`
- **Response:** `200 OK` พร้อมแนบ Cookie `jwt=...` และข้อมูลสิทธิ์

### `POST /auth/logout`
ออกจากระบบ ลบ JWT Cookie

---

## User & Account

### `GET /users/me`
ดึงข้อมูล Profile ของตัวเอง (ต้องแนบ JWT)
- **Headers:** `Cookie: jwt=...`
- **Response:** ข้อมูล `id`, `username`, `email` และบทบาท (Role)

### `GET /users/quota`
ตรวจสอบโควต้าการใช้งาน API ที่เหลืออยู่
- **Headers:** `Cookie: jwt=...` หรือ `Authorization: Bearer <API_KEY>`
- **Response:** `{"requests_used": 45, "requests_limit": 100, "plan": "free"}`

### `GET /api_keys`
ดึงรายการ API Keys ทั้งหมดของคุณ

### `POST /api_keys`
สร้าง API Key ใหม่ (สูงสุด 5 keys ต่อบัญชี)
- **Body:** `{"name": "Production Key"}`

---

## Model Context Protocol (MCP)

กลุ่ม Endpoint ที่ใช้สำหรับดึงข้อมูลทฤษฎี (AI Agents มักจะเรียกใช้กลุ่มนี้)

### `GET /mcp/topics`
ดึงรายชื่อหัวข้อและโดเมนทั้ง 31 รายการของ UET
- **Response:** Array ของ Topics พร้อมคำอธิบายย่อ

### `GET /mcp/equation/:name`
ดึงสมการเชิงคณิตศาสตร์และคำอธิบายของตัวแปร โดยระบุชื่อ (เช่น `master_equation`, `value_equation`)
- **Response:**
  ```json
  {
    "name": "master_equation",
    "latex": "\\Omega = \\int ...",
    "parameters": [...]
  }
  ```

### `POST /mcp/query`
ค้นหาข้อมูลจาก Knowledge Base แบบ Semantic Search (ใช้ AI Embedding)
- **Body:** `{"query": "อธิบายเรื่องความสัมพันธ์ของพลังงานและข้อมูล", "limit": 3}`
- **Response:** รายการข้อความหรือเอกสารที่มีความหมายใกล้เคียงกับคำถามมากที่สุด พร้อมคะแนนความแม่นยำ (Score)

---

## การจัดการ Error (Error Handling)

API จะส่งคืนรหัส HTTP พร้อม JSON body แจ้งรายละเอียดของข้อผิดพลาดเสมอ:

```json
{
  "error": "UNAUTHORIZED",
  "message": "Invalid or expired token provided."
}
```
