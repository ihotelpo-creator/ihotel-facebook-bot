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
หน้าที่ของคุณคือบริการแชตให้ข้อมูลลูกค้าทาง Facebook Messenger ด้วยความเป็นกันเอง น่ารัก สุภาพ และเหมือนคนจริงมากที่สุด

📌 หลักการสนทนาแบบคนจริง (สั้น กระชับ ชัดเจน):
1. **สั้น กระชับ อ่านง่าย**: ตอบตรงประเด็น ไม่พิมพ์ยาวเป็นเรียงความ ไม่ใส่หัวข้อเยอะเกินไป ให้พิมพ์เหมือนแชตคุยกันสั้นๆ (2-4 บรรทัด) ใช้อิโมจิน่ารักประกอบ (🏨, 🛏️, 📍, 🍳, ✨, 🚗, 💕)
2. **ถามกลับอย่างใส่ใจ**: เมื่อลูกค้าถามเรื่องห้องพัก ให้ถามกลับสั้นๆ เพื่อช่วยเลือก เช่น "เข้าพักกี่ท่าน และมีวันที่ในใจหรือยังคะ? น้องไอช่วยดูห้องที่เหมาะที่สุดให้ค่ะ 😊"
3. **ส่งต่อ LINE OA อย่างนุ่มนวล**: เมื่อลูกค้าจะจองห้อง ให้แนะนำอย่างสุภาพและส่งลิงก์ LINE OA ทันที เช่น "เพื่อเช็คห้องว่างทันทีและรับการยืนยันเข้าเครื่อง จองผ่าน LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk มีแอดมินดูแลต่อทันทีค่ะ"
4. **กูรูท้องถิ่น (Local Insider)**: แนะนำของกินและการเดินทางใกล้ๆ ได้สั้นๆ เช่น "โรงแรมอยู่ใกล้โลตัสโนนม่วง 500 ม. หาของกินง่ายมากค่ะ มีที่จอดรถกว้างขวาง ปลอดภัย 24 ชม."
5. **ความถูกต้อง**:
   - เวลาอาหารเช้าบุฟเฟต์: 06:30 - 10:00 น. (Deluxe/Grand Deluxe ฟรีฟรี, Superior ซื้อเพิ่ม 100 บ.)
   - ระยะทาง: มข. (5-10 นาที), รพ.ศรีนครินทร์ (8-10 นาที), เซ็นทรัลแคมปัส (5-7 นาที), เซ็นทรัลขอนแก่น (12-15 นาที), สนามบิน (15-20 นาที)

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
            "temperature": 0.65,
            "maxOutputTokens": 400,
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
    ระบบตอบกลับสำรองกรณีไม่มี API Key หรือ AI ขัดข้องชั่วคราว (สั้น กระชับ เป็นกันเอง)
    """
    msg = user_message.lower()
    
    # สอบถามระยะทาง / สถานที่ใกล้เคียง
    if any(w in msg for w in ["ห่าง", "กี่กิโล", "กี่นาที", "มข", "ศรีนครินทร์", "เซ็นทรัล", "แคมปัส", "สนามบิน", "ไกลไหม", "เดินทาง"]):
        return (
            f"🚗 การเดินทางจาก {HOTEL_INFO['name_th']} ค่ะ ✨\n\n"
            f"• มข.: 5-10 นาที (~3-4 กม.)\n"
            f"• รพ.ศรีนครินทร์: 8-10 นาที (~4-5 กม.)\n"
            f"• เซ็นทรัลแคมปัส: 5-7 นาที | เซ็นทรัลใหญ่: 12-15 นาที\n"
            f"• สนามบินขอนแก่น: 15-20 นาที\n"
            f"• โลตัสโนนม่วง: แค่ 500 เมตร หาของกินง่ายมากค่ะ 😊\n\n"
            f"📍 แผนที่: {HOTEL_INFO['location']['google_maps_url']}"
        )

    # ห้องประชุม
    elif any(w in msg for w in ["ประชุม", "สัมมนา", "จัดเลี้ยง", "meeting", "event", "hall"]):
        return (
            f"🏨 บริการห้องประชุมและจัดเลี้ยงค่ะ ✨\n"
            f"มี 4 ห้อง รองรับได้ถึง 200 ท่าน มีโปรเจคเตอร์ เครื่องเสียง และเบรกครบชุดเลยค่ะ\n\n"
            f"📞 ขอใบเสนอราคา โทร: {HOTEL_INFO['contact']['phone']} หรือ LINE OA: @ihotelkk นะคะ"
        )
        
    # อาหารเช้า
    elif any(w in msg for w in ["อาหารเช้า", "breakfast", "บุฟเฟ่", "บุฟเฟต์", "กินข้าว", "ไข่กระทะ", "กาแฟ"]):
        return (
            f"🍳 อาหารเช้าบุฟเฟต์ทานได้ตั้งแต่ 06:30 - 10:00 น. ค่ะ ✨\n"
            f"มีไข่กระทะ อาหารไทยปรุงสด สลัดบาร์ กาแฟสด และขนมปังสดใหม่ทุกเช้าค่ะ\n\n"
            f"• Deluxe / Grand Deluxe: ฟรีอาหารเช้าค่ะ\n"
            f"• Superior: ซื้อเพิ่มพร้อมห้องเพียง 100 บ./ท่าน เท่านั้นค่ะ 😊"
        )

    # ราคา / จองห้องพัก
    elif any(w in msg for w in ["จอง", "ราคา", "ห้องพัก", "มีห้อง", "room", "price", "ว่าง", "เตียง"]):
        return (
            f"สวัสดีค่ะ ยินดีต้อนรับสู่ {HOTEL_INFO['name_th']} นะคะ 🏨✨\n\n"
            f"• Superior: เริ่มต้น 750 บ.\n"
            f"• Deluxe (รวมอาหารเช้า 2 ท่าน): เริ่มต้น 1,000 บ.\n"
            f"• Grand Deluxe (พัก 2-4 ท่าน รวมอาหารเช้า): เริ่มต้น 1,300 บ.\n\n"
            f"วางแผนเข้าพักวันไหน และพักกี่ท่านคะ? จองและเช็คห้องว่างผ่าน LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk 💕"
        )
    
    # ที่ตั้ง
    elif any(w in msg for w in ["ที่ตั้ง", "แผนที่", "อยู่แถวไหน", "พิกัด", "ทางไป", "map", "location", "โลตัส", "โนนม่วง"]):
        return (
            f"📍 โรงแรมตั้งอยู่ติดถนนมิตรภาพ ต.ศิลา อ.เมืองขอนแก่น ค่ะ\n"
            f"ใกล้โลตัสโนนม่วงเพียง 500 เมตร เดินทางเข้า มข. สะดวกมากค่ะ ✨\n\n"
            f"🗺️ Google Maps: {HOTEL_INFO['location']['google_maps_url']}\n"
            f"☎️ สอบถามเส้นทางโทร: {HOTEL_INFO['contact']['phone']} (24 ชม.)"
        )
        
    # เช็คอิน เช็คเอาท์
    elif any(w in msg for w in ["เช็คอิน", "เช็คเอาท์", "check in", "check out", "เวลา"]):
        return (
            f"🕒 เวลาเช็คอิน 14:00 น. / เช็คเอาท์ เที่ยงวัน (12:00 น.) ค่ะ ✨\n"
            f"แผนกต้อนรับมีเจ้าหน้าที่คอยดูแลตลอด 24 ชั่วโมง เข้าพักเวลาไหนก็สะดวกค่ะ 😊"
        )
        
    # ช่องทางติดต่อ
    elif any(w in msg for w in ["เบอร์", "ติดต่อ", "โทร", "call", "line", "แอดไลน์", "เจ้าหน้าที่"]):
        return (
            f"📞 ช่องทางการติดต่อค่ะ ✨\n\n"
            f"☎️ โทร: {HOTEL_INFO['contact']['phone']} (ตลอด 24 ชม.)\n"
            f"📲 จองห้องพัก LINE OA: @ihotelkk (https://line.me/R/ti/p/@ihotelkk)"
        )
        
    else:
        return (
            f"สวัสดีค่ะ น้องไอยินดีให้บริการค่ะ 🏨✨\n"
            f"สอบถามราคาห้องพัก อาหารเช้า หรือเส้นทางได้เลยนะคะ\n\n"
            f"📲 จองห้องพักผ่าน LINE OA: @ihotelkk (คลิก: https://line.me/R/ti/p/@ihotelkk)\n"
            f"☎️ โทรด่วน: {HOTEL_INFO['contact']['phone']} (24 ชม.)"
        )


