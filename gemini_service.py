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
คุณคือ "น้องไอ" (Nong I) ผู้ช่วยและพนักงานต้อนรับเสมือนจริงของ {HOTEL_INFO['name_th']}
หน้าที่ของคุณคือบริการต้อนรับ ให้ข้อมูลห้องพัก ราคา สิ่งอำนวยความสะดวก การเดินทาง และช่วยเหลือลูกค้าที่สอบถามผ่าน Facebook Messenger

กฎการตอบคำถาม:
1. บุคลิกภาพ: สุภาพ อบอุ่น เป็นมิตร กระตือรือร้นในการให้บริการ พูดจาไพเราะ (ลงท้ายด้วย "ค่ะ" เสมอ)
2. ข้อมูลต้องถูกต้อง: ยึดตามข้อมูลโรงแรมที่กำหนดให้อย่างเคร่งครัด ห้ามแต่งเติมราคาหรือเงื่อนไขที่ไม่มีจริง
3. กระชับ ชัดเจน: ตอบให้เข้าใจง่าย มีการแบ่งบรรทัด ใช้อิโมจิ (เช่น 🏨, 🛏️, 📍, ✨, 📞) ประกอบให้อ่านง่าย สบายตา
4. การจองห้องพัก: หากลูกค้าสนใจจอง ให้ขอข้อมูล:
   - วันที่เช็คอิน / เช็คเอาท์
   - จำนวนผู้เข้าพัก
   - ประเภทห้องพักที่สนใจ
   - เบอร์โทรติดต่อ
   และแจ้งว่าจะมีเจ้าหน้าที่ประสานงานคอนเฟิร์มการจองให้ทันที
5. ปัญหาพิเศษ/ติดต่อคน: หากลูกค้าสอบถามเรื่องที่ไม่ทราบแน่ชัด, ขอลดราคาพิเศษ, ขอใบกำกับภาษี, หรือต้องการคุยกับคน ให้แจ้งเบอร์โทรติดต่อ {HOTEL_INFO['contact']['phone']} หรือ Line: {HOTEL_INFO['contact']['line_oa']}

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
            "temperature": 0.5,
            "maxOutputTokens": 600,
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
    ระบบตอบกลับสำรองกรณีไม่มี API Key หรือ AI ขัดข้องชั่วคราว
    """
    msg = user_message.lower()
    
    if any(w in msg for w in ["ประชุม", "สัมมนา", "จัดเลี้ยง", "meeting", "event", "hall"]):
        return (
            f"🏨 บริการห้องประชุมสัมมนาและจัดเลี้ยง {HOTEL_INFO['name_th']} ค่ะ ✨\n\n"
            f"• มีห้องประชุมทั้งหมด {HOTEL_INFO['meeting_rooms']['total_rooms']}\n"
            f"• {HOTEL_INFO['meeting_rooms']['max_capacity']}\n"
            f"• พร้อมสิ่งอำนวยความสะดวก โปรเจคเตอร์ เครื่องเสียง และอาหารว่าง/เบรก\n\n"
            f"📞 สอบถามข้อมูลเพิ่มเติมหรือขอใบเสนอราคา:\n"
            f"โทร: {HOTEL_INFO['contact']['phone']}\n"
            f"LINE OA: {HOTEL_INFO['contact']['line_oa']}"
        )
        
    elif any(w in msg for w in ["อาหารเช้า", "breakfast", "บุฟเฟ่", "บุฟเฟต์", "กินข้าว"]):
        return (
            f"🍳 ข้อมูลอาหารเช้า {HOTEL_INFO['name_th']} ค่ะ\n\n"
            f"• บริการแบบ: {HOTEL_INFO['breakfast_info']['type']}\n"
            f"• ห้อง Deluxe และ Grand Deluxe: รวมอาหารเช้าฟรี 2-4 ท่านตามประเภทห้องพักค่ะ\n"
            f"• ห้อง Superior: สามารถซื้อเพิ่มพร้อมห้องพักเพียง {HOTEL_INFO['breakfast_info']['price_with_room']} (ซื้อหลังจอง {HOTEL_INFO['breakfast_info']['price_after_booking']})\n\n"
            f"สอบถามเพิ่มเติมโทร: {HOTEL_INFO['contact']['phone']} ได้เลยนะคะ 😊"
        )

    elif any(w in msg for w in ["ราคา", "ห้องพัก", "มีห้อง", "room", "price", "ว่าง", "เตียง"]):
        room_list = "\n".join([
            f"✨ {r['name']} ({r['size']})\n   ราคา {r['price_starting']} {r['unit']}\n   ({r['breakfast']})"
            for r in HOTEL_INFO["rooms"]
        ])
        return (
            f"สวัสดีค่ะ ยินดีต้อนรับสู่ {HOTEL_INFO['name_th']} ค่ะ 🏨✨\n\n"
            f"ประเภทห้องพักและราคา:\n{room_list}\n\n"
            f"ต้องการเข้าพักวันที่เท่าไหร่ และพักกี่ท่าน สามารถแจ้งน้องไอหรือโทรจองที่ {HOTEL_INFO['contact']['phone']} ได้เลยนะคะ 😊"
        )
    
    elif any(w in msg for w in ["ที่ตั้ง", "แผนที่", "อยู่แถวไหน", "พิกัด", "ทางไป", "map", "location", "โลตัส", "โนนม่วง"]):
        return (
            f"📍 ที่ตั้ง {HOTEL_INFO['name_th']}\n"
            f"{HOTEL_INFO['location']['address']}\n\n"
            f"🚗 สถานที่ใกล้เคียง: เทสโก้ โลตัส โนนม่วง (โลตัส ขอนแก่น 3), ม.ขอนแก่น, รพ.ศรีนครินทร์\n\n"
            f"🗺️ แผนที่โรงแรม (Google Maps):\n{HOTEL_INFO['location']['google_maps_url']}\n\n"
            f"สอบถามเส้นทางโทร: {HOTEL_INFO['contact']['phone']} ได้ตลอด 24 ชม. ค่ะ"
        )
        
    elif any(w in msg for w in ["เช็คอิน", "เช็คเอาท์", "check in", "check out", "เวลา"]):
        return (
            f"🕒 เวลาเช็คอิน - เช็คเอาท์ ของโรงแรมค่ะ\n\n"
            f"👉 เช็คอิน: {HOTEL_INFO['policies']['check_in']}\n"
            f"👉 เช็คเอาท์: {HOTEL_INFO['policies']['check_out']}\n"
            f"👉 แผนกต้อนรับเปิดบริการตลอด 24 ชั่วโมงค่ะ เข้าพักเวลาไหนก็สะดวกสบาย ✨"
        )
        
    elif any(w in msg for w in ["เบอร์", "ติดต่อ", "โทร", "call", "line", "แอดไลน์", "เจ้าหน้าที่"]):
        return (
            f"📞 ช่องทางการติดต่อ {HOTEL_INFO['name_th']} ค่ะ\n\n"
            f"☎️ โทร: {HOTEL_INFO['contact']['phone']}\n"
            f"💬 LINE OA: {HOTEL_INFO['contact']['line_oa']}\n"
            f"📍 แผนที่: {HOTEL_INFO['location']['google_maps_url']}\n\n"
            f"ยินดีให้บริการตลอด 24 ชั่วโมงค่ะ 😊"
        )
        
    else:
        return (
            f"สวัสดีค่ะ ยินดีต้อนรับสู่ {HOTEL_INFO['name_th']} ค่ะ 🏨✨\n\n"
            f"น้องไอยินดีให้บริการค่ะ คุณลูกค้าสามารถสอบถามข้อมูลห้องพัก, ราคา, อาหารเช้า, ห้องประชุม, หรือติดต่อจองห้องพักได้เลยนะคะ 😊\n\n"
            f"☎️ โทรด่วน: {HOTEL_INFO['contact']['phone']}\n"
            f"💬 LINE OA: {HOTEL_INFO['contact']['line_oa']}"
        )
