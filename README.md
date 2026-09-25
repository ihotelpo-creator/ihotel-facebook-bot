# 🏨 I Hotel Khonkaen - Facebook Messenger AI Bot

ระบบแชทบอทตอบลูกค้าอัตโนมัติสำหรับ **โรงแรม ไอ โฮเทล ขอนแก่น (I Hotel Khonkaen)** ขับเคลื่อนด้วย **Google Gemini AI** รองรับการทำงานทั้งแบบตอบคำถามภาษาไทยอย่างสุภาพ แม่นยำ และระบบปุ่มลัด (Quick Replies / Carousel) ดูห้องพัก ราคา แผนที่ และการเดินทาง

---

## 🌟 ฟีเจอร์เด่น
- 🧠 **AI อัจฉริยะ (Gemini 1.5 Flash)**: เข้าใจภาษาไทย สำนวน วลี ตอบคำถามข้อมูลโรงแรมได้อย่างเป็นธรรมชาติ
- 🛏️ **ปุ่มลัดดูห้องพัก & ราคา (Carousels)**: แสดงการ์ดห้องพักพร้อมรูปภาพและราคาเริ่มต้น
- 📍 **แนะนำที่ตั้ง & การเดินทาง**: คำนวณเวลาเดินทางไป มข., สนามบินขอนแก่น, บึงหนองโคตร
- 🕒 **ข้อมูลเช็คอิน/เช็คเอาท์**: ชี้แจงเวลาและแผนกต้อนรับ 24 ชม.
- 📞 **ส่งต่อพนักงาน**: แจ้งเบอร์โทรติดต่อและ Line OA สำหรับเคสพิเศษ
- 💸 **ฟรี 100%**: ไม่มีค่าธรรมเนียมรายเดือน

---

## 📁 โครงสร้างโปรเจกต์

```text
facebook/
├── hotel_data.py        # ข้อมูลโรงแรม I Hotel Khonkaen (Knowledge Base)
├── gemini_service.py    # สมอง AI เชื่อมต่อกับ Google Gemini API
├── facebook_service.py  # เชื่อมต่อ Meta Graph Send API (ส่งข้อความ, ปุ่ม, การ์ด)
├── main.py              # FastAPI Webhook Server
├── server.py            # Standalone Webhook Server (รันได้ทันทีโดยไม่ต้องติดตั้ง lib เพิ่ม)
├── test_bot.py          # สคริปต์จำลองแชททดสอบใน Terminal
├── requirements.txt     # รายการ Library
├── .env.example         # ตัวอย่างการตั้งค่า Environment Variables
└── README.md            # คู่มือการติดตั้งและใช้งาน
```

---

## 🚀 วิธีเริ่มต้นใช้งาน (Quick Start)

### 1. การทดสอบแชทในเครื่อง (ไม่ต้องต่อ Facebook)
สามารถทดสอบการตอบคำถามของบอทได้ทันทีผ่าน Terminal:
```bash
python3 test_bot.py
```

---

### 2. การตั้งค่า Environment Variables (`.env`)
คัดลอกไฟล์ `.env.example` เป็น `.env` และกรอกข้อมูล:
```bash
cp .env.example .env
```

แก้ไขไฟล์ `.env`:
- `PAGE_ACCESS_TOKEN`: ได้จาก Meta Developer App (Messenger Settings)
- `VERIFY_TOKEN`: กำหนดเอง เช่น `ihotel_khonkaen_secure_token_2026`
- `GEMINI_API_KEY`: ขอฟรีได้จาก [Google AI Studio](https://aistudio.google.com/app/apikey)

---

### 3. รัน Webhook Server

**วิธีที่ 1: รันแบบ Standalone (เร็วที่สุด ไม่ต้องลง pip เพิ่ม)**
```bash
python3 server.py
```
เซิร์ฟเวอร์จะเปิดทำงานที่ `http://localhost:8000`

**วิธีที่ 2: รันด้วย FastAPI & Uvicorn (สำหรับ Production)**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

---

## 🔗 วิธีเชื่อมต่อกับ Facebook Page (Meta for Developers)

### ขั้นตอนที่ 1: ขอ Gemini API Key (ฟรี)
1. ไปที่ [Google AI Studio](https://aistudio.google.com/app/apikey)
2. ล็อกอินด้วยบัญชี Google แล้วกด **Create API Key**
3. นำคีย์มาใส่ใน `GEMINI_API_KEY` ในไฟล์ `.env`

### ขั้นตอนที่ 2: สร้าง App บน Meta for Developers
1. ไปที่ [developers.facebook.com](https://developers.facebook.com/)
2. เข้าสู่ระบบและกด **My Apps** > **Create App**
3. เลือก Use case เป็น **Other** หรือ **Business**
4. ในหน้า Dashboard เพิ่มผลิตภัณฑ์ **Messenger** เข้ามาใน App

### ขั้นตอนที่ 3: ดึง Page Access Token
1. ในเมนูด้านซ้าย ไปที่ **Messenger** > **Settings** (หรือ App Settings)
2. ในส่วน **Access Tokens** ให้กด **Add or Remove Pages** และเลือกเพจ **I Hotel Khonkaen**
3. กดปุ่ม **Generate Token** แล้วคัดลอก Token มาใส่ใน `PAGE_ACCESS_TOKEN` ในไฟล์ `.env`

### ขั้นตอนที่ 4: เชื่อมต่อ Webhook (Callback URL)
1. สำหรับการทดสอบในเครื่อง ให้เปิด Public URL ด้วย `cloudflared` หรือ `ngrok`:
   ```bash
   # หากใช้ cloudflared (แนะนำ ฟรี ไม่ต้องสมัคร)
   cloudflared tunnel --url http://localhost:8000
   
   # หรือหากใช้ ngrok
   ngrok http 8000
   ```
2. บนหน้า Meta for Developers ในหัวข้อ **Webhooks**:
   - **Callback URL:** `https://YOUR-TUNNEL-URL.ngrok-free.app/webhook` (หรือ cloudflared URL)
   - **Verify Token:** `ihotel_khonkaen_secure_token_2026` (ตามที่ตั้งไว้ใน `.env`)
3. กด **Verify and Save**
4. ในช่อง **Webhook Fields** ให้กด Subscribe:
   - ✅ `messages`
   - ✅ `messaging_postbacks`

---

## ☁️ วิธีนำขึ้น Cloud ฟรี 24 ชั่วโมง (Render.com)

1. นำโฟลเดอร์โปรเจกต์นี้ขึ้น **GitHub**
2. ไปที่ [Render.com](https://render.com/) (สมัครฟรี)
3. กด **New +** > **Web Service** แล้วเลือกเชื่อมต่อ GitHub Repository นี้
4. ตั้งค่า:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python3 -m uvicorn main:app --host 0.0.0.0 --port $PORT`
5. ในแท็บ **Environment Variables** ให้เพิ่มตัวแปร:
   - `PAGE_ACCESS_TOKEN`
   - `VERIFY_TOKEN`
   - `GEMINI_API_KEY`
6. นำ URL ที่ได้จาก Render (เช่น `https://ihotel-bot.onrender.com/webhook`) ไปกรอกใน Meta Developer Webhook ได้ตลอด 24 ชม. ฟรี!
