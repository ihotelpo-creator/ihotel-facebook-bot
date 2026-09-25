# -*- coding: utf-8 -*-
"""
I Hotel Khonkaen - Facebook Messenger Webhook Server
รองรับการรับ-ส่งข้อความ, Webhook Verification, AI Reply (Gemini), และ Quick Replies
"""

import os
import sys
import json
import logging
from typing import Dict, List

# โหลด .env หากมี python-dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from hotel_data import HOTEL_INFO
import gemini_service
import facebook_service

# ตั้งค่า Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("IHotelBot")

# เก็บประวัติการแชทชั่วคราวใน Memory (sender_id -> list of messages)
chat_sessions: Dict[str, List[dict]] = {}

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "ihotel_khonkaen_secure_token_2026")
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")


def handle_payload_action(sender_id: str, payload: str):
    """จัดการเมื่อผู้ใช้กดปุ่ม Quick Reply หรือปุ่มบน Card"""
    logger.info(f"รับ Payload จาก User {sender_id}: {payload}")
    
    if payload == "QR_ROOMS_AND_PRICES":
        facebook_service.send_text_message(sender_id, "🏨 ด้านล่างนี้คือประเภทห้องพักและราคาของ I Hotel Khonkaen ค่ะ:")
        facebook_service.send_room_carousel(sender_id)
        
    elif payload == "QR_LOCATION_MAP":
        location_msg = (
            f"📍 แผนที่และการเดินทางมายัง {HOTEL_INFO['name_th']} ค่ะ 🚗✨\n\n"
            f"🏢 ที่อยู่: {HOTEL_INFO['location']['address']}\n"
            f"(ติดถนนมิตรภาพ ใกล้โลตัสโนนม่วง / มข.)\n\n"
            f"⏱️ ระยะทางไปยังสถานที่สำคัญ:\n"
            f"• โลตัส โนนม่วง (ขอนแก่น 3): 1-2 นาที (~500 ม.)\n"
            f"• มหาวิทยาลัยขอนแก่น (มข.): 5-10 นาที (~3-4 กม.)\n"
            f"• โรงพยาบาลศรีนครินทร์: 8-10 นาที (~4-5 กม.)\n"
            f"• เซ็นทรัล แคมปัส (Central Campus): 5-7 นาที (~3-4 กม.)\n"
            f"• เซ็นทรัลพลาซา ขอนแก่น: 12-15 นาที (~7-8 กม.)\n"
            f"• สนามบินนานาชาติขอนแก่น: 15-20 นาที (~10-12 กม.)\n\n"
            f"🗺️ แผนที่ Google Maps: {HOTEL_INFO['location']['google_maps_url']}\n"
            f"☎️ สอบถามเส้นทางโทร: {HOTEL_INFO['contact']['phone']} ได้ตลอด 24 ชม. ค่ะ"
        )
        facebook_service.send_text_message(sender_id, location_msg)
        
    elif payload == "QR_CHECKIN_INFO":
        checkin_msg = (
            f"🕒 ข้อมูลเวลาเช็คอิน - เช็คเอาท์ ค่ะ ✨\n\n"
            f"👉 เช็คอินได้ตั้งแต่: {HOTEL_INFO['policies']['check_in']}\n"
            f"👉 เช็คเอาท์ก่อน: {HOTEL_INFO['policies']['check_out']}\n"
            f"👉 แผนกต้อนรับบริการตลอด 24 ชม. มีเจ้าหน้าที่คอยดูแลตลอดเวลาค่ะ ✨"
        )
        facebook_service.send_text_message(sender_id, checkin_msg)
        
    elif payload == "QR_AMENITIES_BREAKFAST":
        breakfast_msg = (
            f"🍳 ข้อมูลอาหารเช้าแบบบุฟเฟต์ (Buffet Breakfast) {HOTEL_INFO['name_th']} ค่ะ ✨\n\n"
            f"⏰ เวลาให้บริการ: {HOTEL_INFO['breakfast_info']['service_time']} (06:30 - 10:00 น.)\n"
            f"🍽️ เมนูในไลน์บุฟเฟต์: ขนมปัง, น้ำผลไม้, อาหารไทยตามฤดูกาล, สลัดบาร์, เมนูทอดร้อนๆ เช่น ไข่กระทะ ไส้กรอก แฮม, กาแฟสดชงสดใหม่\n\n"
            f"💵 ราคาอาหารเช้า:\n"
            f"• ห้อง Deluxe / Grand Deluxe: รวมอาหารเช้าฟรีค่ะ\n"
            f"• ห้อง Superior: ซื้อเพิ่มพร้อมห้องเพียง {HOTEL_INFO['breakfast_info']['price_with_room']} (ซื้อหลังจอง {HOTEL_INFO['breakfast_info']['price_after_booking']}) ค่ะ"
        )
        facebook_service.send_text_message(sender_id, breakfast_msg)
        facebook_service.send_breakfast_photos(sender_id)
        
    elif payload == "QR_CONTACT_STAFF":
        contact_msg = (
            f"📞 ช่องทางการติดต่อเจ้าหน้าที่ {HOTEL_INFO['name_th']}\n\n"
            f"☎️ โทร: {HOTEL_INFO['contact']['phone']}\n"
            f"💬 Line OA: {HOTEL_INFO['contact']['line_oa']}\n"
            f"📍 ที่ตั้ง: {HOTEL_INFO['location']['address']}\n\n"
            f"สามารถพิมพ์คำถามหรือแจ้งเรื่องที่ต้องการให้ช่วยเหลือไว้ในแชทนี้ได้เลยนะคะ น้องไอและทีมงานยินดีดูแลค่ะ 😊"
        )
        facebook_service.send_text_message(sender_id, contact_msg)
        
    elif payload.startswith("BOOK_ROOM_"):
        room_id = payload.replace("BOOK_ROOM_", "")
        room_name = next((r["name"] for r in HOTEL_INFO["rooms"] if r["id"] == room_id), "ห้องพัก")
        booking_prompt = (
            f"ยินดีต้อนรับค่ะ สำหรับการจองห้องพัก {room_name} 🛏️✨\n\n"
            f"🏨 การจองห้องพักของโรงแรม I Hotel Khonkaen ลูกค้าจะต้องดำเนินการจองผ่าน LINE OA เท่านั้นนะคะ เพื่อความสะดวกรวดเร็วในการเช็คห้องว่างและยืนยันการจองค่ะ\n\n"
            f"📲 **คลิกเพื่อจองผ่าน LINE OA:**\n"
            f"👉 https://line.me/R/ti/p/@ihotelkk\n"
            f"(หรือค้นหา ID LINE: @ihotelkk)\n\n"
            f"☎️ สอบถามข้อมูลเพิ่มเติมโทร: {HOTEL_INFO['contact']['phone']} ได้ตลอด 24 ชม. ค่ะ"
        )
        facebook_service.send_text_message(sender_id, booking_prompt)
        
    else:
        reply = gemini_service.generate_reply(payload)
        facebook_service.send_text_message(sender_id, reply)


def process_user_message(sender_id: str, message_text: str):
    """ประมวลผลข้อความที่ลูกค้าพิมพ์ส่งมา"""
    logger.info(f"ข้อความจาก User [{sender_id}]: {message_text}")
    
    # 1. แจ้งเตือนสถานะอ่านแล้ว & กำลังพิมพ์
    facebook_service.mark_seen(sender_id)
    facebook_service.send_typing_indicator(sender_id, is_typing=True)
    
    # 2. บันทึกประวัติการแชท
    if sender_id not in chat_sessions:
        chat_sessions[sender_id] = []
    
    chat_sessions[sender_id].append({"sender": "user", "text": message_text})
    
    # 3. ให้ Gemini AI ช่วยประมวลผลคำตอบ
    reply = gemini_service.generate_reply(message_text, chat_sessions[sender_id])
    
    # 4. บันทึกคำตอบกลับ
    chat_sessions[sender_id].append({"sender": "bot", "text": reply})
    
    # 5. ส่งข้อความกลับหาผู้ใช้
    facebook_service.send_text_message(sender_id, reply, with_quick_replies=True)
    
    # 6. หากลูกค้าถามหารูปภาพห้องพัก ให้ส่งรูปจริงประกอบไปด้วย
    lower_text = message_text.lower()
    if any(w in lower_text for w in ["รูป", "ภาพ", "photo", "picture", "ดูห้อง", "หน้าตาห้อง", "ห้องเป็นยังไง", "ตึก", "ฟร้อน", "ล็อบบี้", "อาหารเช้า", "บุฟเฟ่", "breakfast"]):
        if any(w in lower_text for w in ["อาหารเช้า", "บุฟเฟ่", "กินข้าว", "breakfast", "สลัด", "ไข่กระทะ"]):
            facebook_service.send_breakfast_photos(sender_id)
        elif any(w in lower_text for w in ["ตึก", "อาคาร", "โรงแรม", "ภายนอก", "ข้างนอก", "building"]):
            facebook_service.send_hotel_building_photos(sender_id)
        elif any(w in lower_text for w in ["ฟร้อน", "ฟร้อนท์", "ล็อบบี้", "lobby", "front", "เคาน์เตอร์"]):
            facebook_service.send_lobby_photos(sender_id)
        elif any(w in lower_text for w in ["deluxe", "ดีลักซ์", "1000", "ผ้าดูเว่"]):
            facebook_service.send_deluxe_photos(sender_id)
        elif any(w in lower_text for w in ["3 ท่าน", "สามท่าน", "grand deluxe", "แกรนด์", "triple", "1600", "ครอบครัว"]):
            facebook_service.send_grand_deluxe_triple_photos(sender_id)
        elif any(w in lower_text for w in ["superior", "สุพีเรีย", "750", "28"]):
            facebook_service.send_superior_photos(sender_id)
        else:
            facebook_service.send_hotel_building_photos(sender_id)
            facebook_service.send_superior_photos(sender_id)
            facebook_service.send_deluxe_photos(sender_id)







# =========================================================================
# FastAPI Server Implementation
# =========================================================================
try:
    from fastapi import FastAPI, Request, Response, Query
    from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse
    
    app = FastAPI(title="I Hotel Khonkaen Facebook Bot", version="1.0.0")

    @app.get("/", response_class=HTMLResponse)
    async def index():
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>{HOTEL_INFO['name_th']} - Facebook Bot</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px; background: #f0f2f5; }}
                .card {{ background: white; max-width: 600px; margin: auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                h1 {{ color: #1877f2; margin-top: 0; }}
                .status {{ display: inline-block; padding: 6px 12px; background: #e7f3ff; color: #1877f2; border-radius: 20px; font-weight: bold; margin-bottom: 20px; }}
                .code {{ background: #282c34; color: #61afef; padding: 12px; border-radius: 8px; font-family: monospace; overflow-x: auto; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🏨 {HOTEL_INFO['name_th']}</h1>
                <div class="status">🟢 Facebook Webhook Server is Online</div>
                <p>ระบบบอทสำหรับตอบ Facebook Messenger ของโรงแรมพร้อมทำงานแล้ว</p>
                <h3>📌 ข้อมูลสำหรับตั้งค่า Webhook บน Meta for Developers:</h3>
                <ul>
                    <li><strong>Callback URL:</strong> <code>https://YOUR_DOMAIN/webhook</code></li>
                    <li><strong>Verify Token:</strong> <code>{VERIFY_TOKEN}</code></li>
                </ul>
                <p>AI Engine: <strong>Gemini 1.5 Flash (Google AI)</strong></p>
            </div>
        </body>
        </html>
        """

    @app.get("/privacy", response_class=HTMLResponse)
    async def privacy_policy():
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Privacy Policy - {HOTEL_INFO['name_th']}</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px; max-width: 800px; margin: auto; line-height: 1.6; color: #333; }}
                h1, h2 {{ color: #1877f2; }}
            </style>
        </head>
        <body>
            <h1>Privacy Policy (นโยบายความเป็นส่วนตัว)</h1>
            <p><strong>{HOTEL_INFO['name_th']} ({HOTEL_INFO['name_en']})</strong></p>
            <p>อัปเดตล่าสุด: 25 กันยายน 2026</p>
            
            <h2>1. ข้อมูลที่เราเก็บรวบรวม</h2>
            <p>ระบบบอท Facebook Messenger เก็บรวบรวมเฉพาะข้อมูลที่จำเป็นต่อการให้บริการ เช่น ชื่อโปรไฟล์ Facebook, ID ผู้ใช้, และข้อความสอบถามข้อมูลห้องพัก การจอง และการบริการของโรงแรม</p>
            
            <h2>2. วัตถุประสงค์ในการใช้ข้อมูล</h2>
            <p>เพื่อตอบคำถาม ให้ข้อมูลห้องพัก ราคา บริการ และประสานงานการจองห้องพักของ {HOTEL_INFO['name_th']} เท่านั้น เราไม่มีนโยบายจำหน่ายหรือเปิดเผยข้อมูลส่วนบุคคลให้แก่บุคคลภายนอก</p>
            
            <h2>3. การติดต่อเรา</h2>
            <p>หากมีข้อสงสัยเกี่ยวกับนโยบายความเป็นส่วนตัว สามารถติดต่อได้ที่ {HOTEL_INFO['contact']['phone']} หรืออีเมล {HOTEL_INFO['contact']['email']}</p>
        </body>
        </html>
        """

    @app.get("/terms", response_class=HTMLResponse)
    async def terms_of_service():
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Terms of Service - {HOTEL_INFO['name_th']}</title>
            <style>
                body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px; max-width: 800px; margin: auto; line-height: 1.6; color: #333; }}
                h1, h2 {{ color: #1877f2; }}
            </style>
        </head>
        <body>
            <h1>Terms of Service (เงื่อนไขการใช้บริการ)</h1>
            <p><strong>{HOTEL_INFO['name_th']}</strong></p>
            <p>ระบบแชทอัตโนมัติจัดทำขึ้นเพื่อให้ข้อมูลห้องพักและสิ่งอำนวยความสะดวกของโรงแรม การจองห้องพักจะมีผลสมบูรณ์เมื่อได้รับการยืนยันจากทางโรงแรม</p>
        </body>
        </html>
        """

    @app.get("/webhook")
    async def verify_webhook(
        hub_mode: str = Query(None, alias="hub.mode"),
        hub_verify_token: str = Query(None, alias="hub.verify_token"),
        hub_challenge: str = Query(None, alias="hub.challenge")
    ):
        """Facebook Webhook Verification"""
        logger.info(f"ได้รับ Webhook Verification Request: mode={hub_mode}, token={hub_verify_token}")
        
        if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
            logger.info("✅ ยืนยัน Webhook Token สำเร็จ!")
            return PlainTextResponse(content=hub_challenge, status_code=200)
            
        logger.warning("❌ ยืนยัน Webhook Token ไม่ถูกต้อง!")
        return Response(content="Verification token mismatch", status_code=403)

    @app.post("/webhook")
    async def handle_webhook(request: Request):
        """รับ Events จาก Facebook Messenger"""
        body = await request.json()
        logger.info(f"ได้รับ Webhook Event: {json.dumps(body, ensure_ascii=False)}")
        
        if body.get("object") == "page":
            for entry in body.get("entry", []):
                for messaging_event in entry.get("messaging", []):
                    sender_id = messaging_event.get("sender", {}).get("id")
                    
                    if not sender_id:
                        continue
                        
                    # กรณีเป็นข้อความ Text ทั่วไป
                    if "message" in messaging_event:
                        msg_obj = messaging_event["message"]
                        
                        # ตรวจสอบว่าเป็นการกดปุ่ม Quick Reply หรือไม่
                        if "quick_reply" in msg_obj:
                            payload = msg_obj["quick_reply"].get("payload")
                            handle_payload_action(sender_id, payload)
                        elif "text" in msg_obj:
                            text = msg_obj["text"]
                            process_user_message(sender_id, text)
                            
                    # กรณีเป็นการกดปุ่ม Postback (เช่น ปุ่มบน Card หรือ Get Started)
                    elif "postback" in messaging_event:
                        payload = messaging_event["postback"].get("payload")
                        handle_payload_action(sender_id, payload)
                        
            return JSONResponse(content={"status": "EVENT_RECEIVED"}, status_code=200)
            
        return Response(content="Not Found", status_code=404)

except ImportError:
    app = None


if __name__ == "__main__":
    if app:
        import uvicorn
        logger.info(f"กำลังเริ่มระบบ Server ที่ http://{HOST}:{PORT}")
        uvicorn.run("main:app", host=HOST, port=PORT, reload=True)
    else:
        logger.error("โปรดติดตั้ง dependencies: pip install -r requirements.txt")
