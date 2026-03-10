---
title: "Working with the API"
description: "วิธีการเชื่อมต่อ แลกเปลี่ยนข้อมูล และเรียกใช้งาน UET REST API"
---

# Working with the API

UET Platform เปิดให้บริการ **REST API** เพื่อให้นักพัฒนาสามารถนำทฤษฎี สมการ และ AI Knowledge Base ไปประยุกต์เชื่อมต่อกับแอปพลิเคชันของคุณเองได้

## 1. การรับ API Key (Authentication)

ในการเรียกใช้ API (ส่วนใหญ่) คุณจำเป็นต้องมี API Key
1. ล็อกอินเข้าสู่หน้าเว็บ UET Platform
2. ไปที่เมนู **Dashboard** > **API Keys**
3. กดปุ่ม `Generate New Key`
4. คัดลอก Key ที่ได้ไว้ให้ดี (ระบบจะไม่แสดง Key นี้ซ้ำอีก)

เมื่อต้องการเรียกใช้ API ให้แนบ Key ใน HTTP Header ดังนี้:
```http
Authorization: Bearer uet_your_api_key_here
```

## 2. API Endpoints หลักๆ

### ก. การเรียกดูรายการหัวข้อทั้งหมด (Topics)
ไม่ต้องใช้ Authentication ดึงรายการโดเมนทั้งหมด 31 โดเมนของ UET

**Request:**
```bash
curl -X GET http://localhost:3000/api/mcp/topics
```

### ข. การค้นหาข้อมูล (Natural Language Query)
ใช้ AI (FastEmbed) ในการค้นหาความหมายจากเอกสารในฐานข้อมูล

**Request:**
```bash
curl -X POST http://localhost:3000/api/mcp/query \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer uet_your_api_key_here" \
  -d '{"query": "ทำไม UET ถึงมองว่าเศรษฐศาสตร์เป็นฟิสิกส์แขนงหนึ่ง?"}'
```

**Response:**
```json
{
  "query": "ทำไม UET ถึงมองว่าเศรษฐศาสตร์เป็นฟิสิกส์แขนงหนึ่ง?",
  "results": [
    {
      "doc_id": "concept_001",
      "content": "UET อธิบายว่า Value is Physical...",
      "score": 0.89
    }
  ]
}
```

### ค. การเรียกดูสมการแบบเจาะจง (Equation Fetching)
ดึงข้อมูลสมการ ตัวแปร และคำอธิบาย เพื่อนำไป Render บนหน้าเว็บของคุณ (เช่น การใช้ KaTeX)

**Request:**
```bash
curl -X GET http://localhost:3000/api/mcp/equation/master_equation \
  -H "Authorization: Bearer uet_your_api_key_here"
```

## 3. ข้อจำกัดและ Quota (Rate Limits)

API มีการจำกัดการใช้งานตามแผน (Plan) ของคุณ:
- **Free Tier:** 100 requests / day
- **Pro Tier:** 10,000 requests / day
- **Enterprise:** Unlimited

หากคุณเรียกใช้งานเกินขีดจำกัด ระบบจะตอบกลับด้วย `429 Too Many Requests` พร้อมข้อความแจ้งเตือน

## 4. การจัดการ Errors

UET API ใช้ HTTP Status Codes มาตรฐาน:
- `200 OK` - สำเร็จ
- `400 Bad Request` - ข้อมูลที่ส่งมาไม่ถูกต้อง
- `401 Unauthorized` - API Key ไม่ถูกต้อง หรือไม่ได้แนบมา
- `403 Forbidden` - ไม่มีสิทธิ์เข้าถึง Resource นี้น
- `429 Too Many Requests` - เกินโควต้า
- `500 Internal Server Error` - เกิดข้อผิดพลาดที่เซิร์ฟเวอร์

ตัวอย่าง Error Response:
```json
{
  "error": "Rate limit exceeded",
  "message": "You have reached your daily limit of 100 requests."
}
```
