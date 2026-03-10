---
title: "Docker Deployment"
description: "การติดตั้งและรัน UET Platform ทั้งระบบด้วย Docker และ Docker Compose"
---

# Docker Deployment

วิธีที่ง่ายที่สุดและมั่นใจได้ว่าระบบจะทำงานได้เหมือนกันในทุกสภาพแวดล้อมคือการใช้ **Docker** เราได้เตรียมไฟล์ `docker-compose.yml` ไว้ให้แล้ว ซึ่งจะช่วยให้คุณสามารถเปิดรันทั้งระบบ (Frontend, Backend, Database) ได้ด้วยคำสั่งเดียว

## Prerequisites

- **Docker Engine** (เวอร์ชันล่าสุด)
- **Docker Compose** (เวอร์ชัน v2 ขึ้นไป)

## การรันด้วย Docker Compose (แนะนำ)

1. คัดลอกและตั้งค่า Environment variables:

```bash
cp .env.example .env
```
*(คุณสามารถปล่อยค่า Default ไว้ได้สำหรับการรันบน Local)*

2. สร้างและเริ่มการทำงานของ Containers:

```bash
docker-compose up --build
```
*(ถ้าต้องการรันแบบ Background ให้เติม flag `-d` ต่อท้าย)*

เมื่อกระบวนการเสร็จสิ้น ระบบจะทำงานดังนี้:
- **Web Frontend:** เข้าถึงได้ที่ `http://localhost:3000` (หรือ 3002 หาก 3000 ไม่ว่าง)
- **API Backend:** เข้าถึงได้ที่ `http://localhost:3000/api` (มีการตั้งค่า Proxy จาก Frontend ไปหา Backend)
- **Database:** PostgreSQL (พร้อม pgvector) พอร์ต `5432` 

## โครงสร้างของ Docker Services

ไฟล์ `docker-compose.yml` ประกาศ Services หลักๆ ไว้ดังนี้:

### 1. `db` (PostgreSQL)
- ใช้ Image: `ankane/pgvector:latest` (PostgreSQL ที่ติดตั้ง Vector Extension แล้ว)
- รันสคริปต์ `init.sql` อัตโนมัติเมื่อสร้าง Container ครั้งแรก เพื่อสร้างตารางข้อมูลและตั้งค่าพื้นฐาน

### 2. `api` (Rust Backend)
- สร้างจาก `Dockerfile.api`
- ใช้ Base Image เป็น `ubuntu:24.04` พร้อมติดตั้ง Build Tools สำหรับคอมไพล์โค้ด Rust และ FastEmbed
- ทำงานเชื่อมต่อกับ `db` ผ่าน `DATABASE_URL`

### 3. `web` (Next.js Frontend)
- สร้างจาก `Dockerfile.web`
- ใช้ Node.js เพื่อ Build และรันโหมด Production
- เปิดพอร์ต 3000 และตั้งค่า Proxy คำขอ `/api` ไปยัง Service `api`

## การจัดการข้อมูล (Data Ingestion)

เมื่อรันระบบด้วย Docker ครั้งแรก ฐานข้อมูล Knowledge Base (MCP) อาจจะยังว่างเปล่า คุณต้องรันสคริปต์ Python เพื่อนำเข้าข้อมูลเอกสารเข้าสู่ฐานข้อมูล Vector:

```bash
# ในเครื่องโฮสต์ (ที่ติดตั้ง Python แล้ว)
cd research_uet/knowledge_base
pip install -r requirements.txt
python ingest_to_pg.py
```
*(สคริปต์นี้จะอ่านไฟล์ Markdown ทั้งหมดในโฟลเดอร์ Docs, แปลงเป็น Vector Embeddings และบันทึกลงฐานข้อมูล `uetlab`)*

## การปิดระบบและลบข้อมูล

เพื่อหยุดการทำงานของ Containers:
```bash
docker-compose down
```

ถ้าต้องการหยุดและ **ลบข้อมูลในฐานข้อมูล** ทิ้งทั้งหมด:
```bash
docker-compose down -v
```
