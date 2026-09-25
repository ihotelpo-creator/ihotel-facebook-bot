# -*- coding: utf-8 -*-
"""
Gemini AI Service สำหรับตอบข้อความลูกค้าโรงแรม I Hotel Khonkaen
ใช้ Google Gemini REST API (v1beta) - รวดเร็ว ประหยัด และรองรับ Free Tier
"""

import os
import json
import logging
import urllib.request
import urllib.error
import env_loader
from hotel_data import get_hotel_knowledge_prompt, HOTEL_INFO

logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
# ใช้โมเดล gemini-flash-latest ที่เสถียร ฉลาด เร็ว และฟรี
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")


SYSTEM_PROMPT = f"""
คุณคือ "น้องไอ" (Nong I) พนักงานต้อนรับเสมือนจริงของ {HOTEL_INFO['name_th']}
หน้าที่ของคุณคือให้ข้อมูลห้องพัก ราคา อาหารเช้า ระยะทางการเดินทาง ห้องประชุม และตอบคำถามลูกค้าผ่าน Facebook Messenger อย่างเป็นมิตร

📌 กฎเหล็กการตอบคำถาม:
1. บุคลิกภาพ: สุภาพ น่ารัก อบอุ่น เป็นกันเอง ลงท้ายด้วย "ค่ะ" เสมอ
2. สั้น กระชับ ตรงประเด็น: ตอบให้เข้าใจง่ายทันที ไม่พิมพ์เป็นเรียงความยาวๆ ใช้อิโมจิ (🏨, 🛏️, 📍, 🍳, ✨, 🚗, 📞) และเว้นบรรทัดให้อ่านง่าย
3. หลากหลายอย่างเป็นธรรมชาติ: ปรับเปลี่ยนรูปแบบคำทักทายและประโยคตอบรับให้เป็นธรรมชาติ ไม่ตอบแบบหุ่นยนต์ท่องจำ
4. ข้อมูลถูกต้องแม่นยำ:
   - เวลาอาหารเช้าบุฟเฟต์: 06:30 - 10:00 น.
   - ระยะทางสถานที่สำคัญ:
     • โลตัส โนนม่วง: 1-2 นาที (~500 ม.)
     • มหาวิทยาลัยขอนแก่น (มข.): 5-10 นาที (~3-4 กม.)
     • โรงพยาบาลศรีนครินทร์: 8-10 นาที (~4-5 กม.)
     • เซ็นทรัล แคมปัส (Central Campus): 5-7 นาที (~3-4 กม.)
     • เซ็นทรัลพลาซา ขอนแก่น: 12-15 นาที (~7-8 กม.)
     • สนามบินนานาชาติขอนแก่น: 15-20 นาที (~10-12 กม.)
5. การจองห้องพัก (สำคัญที่สุด): การจองห้องพักทุกประเภท ลูกค้าจะต้องดำเนินการจองผ่าน LINE OA: @ihotelkk เท่านั้น (คลิก: https://line.me/R/ti/p/@ihotelkk) เมื่อลูกค้าต้องการจองห้องพักหรือสอบถามการจอง ให้แนะนำและส่งลิงก์ LINE OA ให้ลูกค้าทันที
6. ติดต่อเจ้าหน้าที่ / เรื่องพิเศษ: โทร {HOTEL_INFO['contact']['phone']} หรือ LINE OA: @ihotelkk

--- ข้อมูลสารสนเทศของโรงแรม ---
{get_hotel_knowledge_prompt()}
"""


def generate_reply(user_message: str, chat_history: list = None) -> str:
    """
    ส่งข้อความของลูกค้าไปให้ Gemini AI เพื่อสร้างคำตอบที่เหมาะสม
    """
    api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        logger.warning("GEMINI_API_KEY ยังไม่ได้ตั้งค่า กำลังใช้ Fallback rule-based")
        return fallback_rule_based_reply(user_message)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    
    # สร้าง contents payload
    contents = []
    
    # หากมีประวัติการสนทนา ให้ใส่ลงไป
    if chat_history:
        for turn in chat_history[-6:]: # เก็บ 6 ข้อความล่าสุด
            contents.append({
                "role": "user" if turn.get("sender") == "user" else "model",
                "parts": [{"text": turn.get("text", "")}]
            })
            
    contents.append({
        "role": "user",
        "parts": [{"text": user_message}]
    })

    payload = {
        "system_instruction": {
            "parts": [{"text": SYSTEM_PROMPT}]
        },
        "contents": contents,
        "generationConfig": {
            "temperature": 0.6,
            "maxOutputTokens": 500,
            "topP": 0.95
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            candidates = result.get("candidates", [])
            if candidates:
                reply_text = candidates[0].get("content", {}).get("parts", [{}])[0].get("text", "")
                if reply_text.strip():
                    return reply_text.strip()
                    
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        logger.error(f"Gemini API HTTPError {e.code}: {error_body}")
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการเรียก Gemini API: {e}")

    # หาก API ขัดข้อง ให้ใช้ Fallback Rule-based ตอบอัตโนมัติ
    return fallback_rule_based_reply(user_message)


def fallback_rule_based_reply(user_message: str) -> str:
    """
    ระบบตอบกลับสำรองกรณีไม่มี API Key หรือ AI ขัดข้องชั่วคราว (สั้น กระชับ ชัดเจน)
    """
    msg = user_message.lower()
    
    # สอบถามระยะทาง / สถานที่ใกล้เคียง
    if any(w in msg for w in ["ห่าง", "กี่กิโล", "กี่นาที", "มข", "ศรีนครินทร์", "เซ็นทรัล", "แคมปัส", "สนามบิน", "ไกลไหม", "เดินทาง"]):
        return (
            f"🚗 ระยะทางและการเดินทางจาก {HOTEL_INFO['name_th']} ค่ะ ✨\n\n"
            f"• มหาวิทยาลัยขอนแก่น (มข.): 5-10 นาที (~3-4 กม.)\n"
            f"• โรงพยาบาลศรีนครินทร์: 8-10 นาที (~4-5 กม.)\n"
            f"• เซ็นทรัล แคมปัส: 5-7 นาที (~3-4 กม.)\n"
            f"• เซ็นทรัลพลาซา ขอนแก่น: 12-15 นาที (~7-8 กม.)\n"
            f"• สนามบินนานาชาติขอนแก่น: 15-20 นาที (~10-12 กม.)\n"
            f"• โลตัส โนนม่วง: 1-2 นาที (~500 ม.)\n\n"
            f"📍 แผนที่: {HOTEL_INFO['location']['google_maps_url']}\n"
            f"📞 สอบถามเส้นทางโทร: {HOTEL_INFO['contact']['phone']} ได้ตลอด 24 ชม. ค่ะ"
        )

    # ห้องประชุม
    elif any(w in msg for w in ["ประชุม", "สัมมนา", "จัดเลี้ยง", "meeting", "event", "hall"]):
        return (
            f"🏨 บริการห้องประชุมและจัดเลี้ยง {HOTEL_INFO['name_th']} ค่ะ ✨\n\n"
            f"• มี {HOTEL_INFO['meeting_rooms']['total_rooms']} รองรับได้สูงสุด {HOTEL_INFO['meeting_rooms']['max_capacity']}\n"
            f"• มีโปรเจคเตอร์ เครื่องเสียง และบริการอาหารว่าง/เบรกครบวงจร\n\n"
            f"📞 จองห้องประชุม/ขอใบเสนอราคา:\n"
            f"โทร: {HOTEL_INFO['contact']['phone']}\n"
            f"LINE OA: {HOTEL_INFO['contact']['line_oa']}"
        )
        
    # อาหารเช้า
    elif any(w in msg for w in ["อาหารเช้า", "breakfast", "บุฟเฟ่", "บุฟเฟต์", "กินข้าว", "ไข่กระทะ", "กาแฟ"]):
        return (
            f"🍳 อาหารเช้าแบบบุฟเฟต์ (Buffet Breakfast) {HOTEL_INFO['name_th']} ค่ะ ✨\n\n"
            f"⏰ เวลาให้บริการ: {HOTEL_INFO['breakfast_info']['service_time']}\n"
            f"🍽️ เมนู: ขนมปัง, น้ำผลไม้, อาหารไทยตามฤดูกาล, สลัดบาร์, เมนูทอดร้อนๆ เช่น ไข่กระทะ, กาแฟสด\n\n"
            f"💵 ราคา:\n"
            f"• ห้อง Deluxe / Grand Deluxe: รวมอาหารเช้าฟรีค่ะ\n"
            f"• ห้อง Superior: ซื้อเพิ่มพร้อมห้องเพียง 100 บ./ท่าน (ซื้อหลังจอง 120 บ./ท่าน) ค่ะ 😊"
        )

    # ราคา / จองห้องพัก
    elif any(w in msg for w in ["จอง", "ราคา", "ห้องพัก", "มีห้อง", "room", "price", "ว่าง", "เตียง"]):
        room_list = "\n".join([
            f"• {r['name']}: {r['price_starting']} {r['unit']} ({r['breakfast']})"
            for r in HOTEL_INFO["rooms"]
        ])
        return (
            f"🏨 ราคาห้องพัก {HOTEL_INFO['name_th']} ค่ะ ✨\n\n"
            f"{room_list}\n\n"
            f"👉 ลูกค้าสามารถจองห้องพักได้ทาง LINE OA เท่านั้นนะคะ:\n"
            f"📲 LINE OA: @ihotelkk (คลิก: https://line.me/R/ti/p/@ihotelkk)\n"
            f"☎️ โทร: {HOTEL_INFO['contact']['phone']} (24 ชม.)"
        )
    
    # ที่ตั้ง
    elif any(w in msg for w in ["ที่ตั้ง", "แผนที่", "อยู่แถวไหน", "พิกัด", "ทางไป", "map", "location", "โลตัส", "โนนม่วง"]):
        return (
            f"📍 ที่ตั้ง {HOTEL_INFO['name_th']}\n"
            f"{HOTEL_INFO['location']['address']}\n"
            f"(ติดถนนมิตรภาพ ใกล้โลตัสโนนม่วง / มข.)\n\n"
            f"🗺️ แผนที่ (Google Maps): {HOTEL_INFO['location']['google_maps_url']}\n"
            f"☎️ โทร: {HOTEL_INFO['contact']['phone']} ได้ตลอด 24 ชม. ค่ะ"
        )
        
    # เช็คอิน เช็คเอาท์
    elif any(w in msg for w in ["เช็คอิน", "เช็คเอาท์", "check in", "check out", "เวลา"]):
        return (
            f"🕒 เวลาเช็คอิน - เช็คเอาท์ ค่ะ ✨\n\n"
            f"• เช็คอิน: {HOTEL_INFO['policies']['check_in']}\n"
            f"• เช็คเอาท์: {HOTEL_INFO['policies']['check_out']}\n"
            f"• แผนกต้อนรับเปิดบริการตลอด 24 ชม. ค่ะ 😊"
        )
        
    # ช่องทางติดต่อ
    elif any(w in msg for w in ["เบอร์", "ติดต่อ", "โทร", "call", "line", "แอดไลน์", "เจ้าหน้าที่"]):
        return (
            f"📞 ช่องทางการติดต่อ {HOTEL_INFO['name_th']} ค่ะ ✨\n\n"
            f"☎️ โทร: {HOTEL_INFO['contact']['phone']} (ตลอด 24 ชม.)\n"
            f"📲 LINE OA (จองห้องพัก): @ihotelkk (https://line.me/R/ti/p/@ihotelkk)\n"
            f"📍 แผนที่: {HOTEL_INFO['location']['google_maps_url']}"
        )
        
    else:
        return (
            f"สวัสดีค่ะ น้องไอ ยินดีต้อนรับสู่ {HOTEL_INFO['name_th']} ค่ะ 🏨✨\n\n"
            f"สอบถามข้อมูลห้องพัก ราคา อาหารเช้า ระยะทาง หรือติดต่อจองห้องพักได้เลยนะคะ 😊\n\n"
            f"📲 จองห้องพักผ่าน LINE OA: @ihotelkk (คลิก: https://line.me/R/ti/p/@ihotelkk)\n"
            f"☎️ โทรด่วน: {HOTEL_INFO['contact']['phone']} (24 ชม.)"
        )

