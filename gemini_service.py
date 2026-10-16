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
คุณคือ "น้องไอ" (Nong I) พนักงานต้อนรับของ {HOTEL_INFO['name_th']}
ตอบแชตลูกค้าทาง Facebook Messenger ให้เหมือนคนจริงพิมพ์คุยกัน สุภาพ อบอุ่น เป็นกันเอง สั้นกระชับ (ไม่เกิน 2-4 บรรทัด)

🛑 กฎเหล็กห้ามทำเด็ดขาด:
- ห้ามพิมพ์เป็นตารางหรือแสดงลิสต์ห้องพักยาวๆ ซ้ำซาก
- ห้ามพิมพ์ประโยคยาวเป็นเรียงความ หรือข้อความเกิน 4 บรรทัด
- ห้ามพูดแข็งเป็นทางการเกินไป ให้พิมพ์เหมือนพนักงานคนจริงตอบแชตเพจ

📌 กฎสำคัญเกี่ยวกับการเช็คห้องว่าง / จองห้องพัก / ราคา:
- **กรณีลูกค้าถามว่า "มีห้องว่างวันที่ ... ไหม", "คืนนี้ว่างไหม", "พรุ่งนี้ว่างไหม" หรือต้องการเช็คห้องว่าง/จองห้องพัก**:
  • ให้ตอบสั้นๆ สุภาพว่า การเช็คห้องว่างและจองห้องพักจะต้องดำเนินการผ่าน **LINE OA: @ihotelkk** เท่านั้น เพื่อให้แอดมินตรวจสอบสถานะห้องว่างแบบเรียลไทม์ให้ทันที พร้อมส่งข้อมูลติดต่อ:
    - 📲 **LINE OA**: `@ihotelkk` (คลิก: https://line.me/R/ti/p/@ihotelkk)
    - ☎️ **โทร**: `080-457-9889` (ตลอด 24 ชม.)
- **ห้อง Superior (750 บาท)**: **ไม่รวมอาหารเช้า** (หากลูกค้าต้องการ สามารถซื้อเพิ่มเพียง 100 บาท/ท่าน)
- **ห้อง Deluxe และ Grand Deluxe (1,000 บาทขึ้นไป)**: **รวมอาหารเช้าบุฟเฟต์ฟรีสำหรับ 2 ท่านแล้ว**
- **กรณีลูกค้าถามหาห้องพัก 3 คน (ให้ตอบเฉพาะข้อมูลห้อง 3 ท่านเท่านั้น)**:
  • แนะนำ **Grand Deluxe Triple Room** (ขนาดใหญ่ 48 ตร.ม. มีห้องแต่งตัวในตัว ชุดกาแฟ) ราคา **1,600 บาท/คืน** (**รวมอาหารเช้าบุฟเฟต์ฟรี 3 ท่าน**)
- **กรณีลูกค้าถามหาห้องพัก 4 คน (ให้ตอบเฉพาะข้อมูลห้อง 4 ท่านเท่านั้น)**:
  • แนะนำ **Grand Deluxe 4 ท่าน Room** (ขนาดใหญ่ 48 ตร.ม. มีห้องแต่งตัวในตัว ชุดกาแฟ) ราคา **1,800 บาท/คืน** (**รวมอาหารเช้าบุฟเฟต์ฟรี 4 ท่าน**)

✅ สิ่งที่ต้องทำ:
- ตอบสั้นกระชับ อ่านง่าย ใช้ภาษาพูดที่เป็นธรรมชาติ **ห้ามตอบข้อความเดิมซ้ำๆ**
- เมื่อลูกค้าถามเช็คห้องว่างหรือจะจองห้อง ให้ส่งลิงก์ LINE OA: @ihotelkk (https://line.me/R/ti/p/@ihotelkk) และเบอร์โทร 080-457-9889 เสมอ

💡 ตัวอย่างรูปแบบคำตอบที่ถูกต้อง (สั้นกระชับ ละมุน เหมือนคนจริง):

ลูกค้า: มีห้องว่างวันที่ 20 ตุลาคม ไหมคะ / คืนนี้มีห้องว่างไหม
น้องไอ: สำหรับการเช็คห้องว่างและจองห้องพัก รบกวนคุณลูกค้าทักผ่าน **LINE OA: @ihotelkk** เท่านั้นนะคะ มีแอดมินเช็คตารางห้องว่างให้ทันทีเลยค่ะ 😊
📲 คลิกแอดไลน์: https://line.me/R/ti/p/@ihotelkk
☎️ โทรด่วน: 080-457-9889 (ตลอด 24 ชม. ค่ะ) ✨

ลูกค้า: ขอทราบราคาห้องพักหน่อยค่ะ
น้องไอ: ยินดีต้อนรับค่ะ 😊 มีห้อง Superior 750 บ. (ไม่รวมอาหารเช้า ซื้อเพิ่ม 100 บ./ท่าน) และ Deluxe 1,000 บ. (รวมอาหารเช้าฟรี 2 ท่าน) ค่ะ เช็คห้องว่างจองทาง LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk ✨

ลูกค้า: มีห้องพัก 3 คนไหมคะ
น้องไอ: มีค่ะ 😊 สำหรับพัก 3 ท่านจะเป็นห้อง **Grand Deluxe Triple Room** ขนาดใหญ่ 48 ตร.ม. มีห้องแต่งตัวเป็นสัดส่วนและชุดกาแฟ ราคา 1,600 บ./คืน (รวมอาหารเช้าบุฟเฟต์ฟรี 3 ท่านค่ะ) สนใจเช็คห้องว่างจองผ่าน LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk 💕

ลูกค้า: มีห้องพัก 4 คนไหมคะ
น้องไอ: มีค่ะ 😊 สำหรับพัก 4 ท่านจะเป็นห้อง **Grand Deluxe 4 ท่าน** ขนาดใหญ่ 48 ตร.ม. มีห้องแต่งตัวเป็นสัดส่วนและชุดกาแฟ ราคา 1,800 บ./คืน (รวมอาหารเช้าบุฟเฟต์ฟรี 4 ท่านค่ะ) สนใจเช็คห้องว่างจองผ่าน LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk 💕

--- ข้อมูลสารสนเทศของโรงแรม ---
{get_hotel_knowledge_prompt()}
"""


def generate_reply(user_message: str, chat_history: list = None) -> str:
    """
    ส่งข้อความของลูกค้าไปให้ Gemini AI เพื่อสร้างคำตอบที่เหมาะสมอย่างรวดเร็ว
    """
    msg_lower = user_message.lower()
    # หากลูกค้าถามเช็คห้องว่างระบุวันที่ หรือถามว่าว่างไหม ให้ตอบตรงประเด็นให้จองผ่าน LINE OA ทันที
    availability_keywords = ["ว่างไหม", "ว่างมั้ย", "มีห้องว่าง", "เช็คห้องว่าง", "คืนนี้ว่าง", "พรุ่งนี้ว่าง", "วันที่"]
    if any(k in msg_lower for k in availability_keywords) and not any(k in msg_lower for k in ["ราคา", "กี่บาท", "เท่าไหร่", "3 คน", "3คน", "สามคน", "3 ท่าน", "4 คน", "4คน", "สี่คน", "4 ท่าน"]):
        return (
            f"สำหรับการเช็คห้องว่างและจองห้องพัก คุณลูกค้าสามารถดำเนินการผ่าน **LINE OA: @ihotelkk** เท่านั้นนะคะ มีเจ้าหน้าที่เช็คสถานะห้องว่างให้ทันทีค่ะ 😊✨\n\n"
            f"📲 **LINE OA**: @ihotelkk\n"
            f"👉 คลิก: https://line.me/R/ti/p/@ihotelkk\n"
            f"☎️ **โทรติดต่อ**: {HOTEL_INFO['contact']['phone']} (บริการ 24 ชม. ค่ะ)"
        )

    api_key = os.getenv("GEMINI_API_KEY", GEMINI_API_KEY)
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        logger.warning("GEMINI_API_KEY ยังไม่ได้ตั้งค่า กำลังใช้ Fallback rule-based")
        return fallback_rule_based_reply(user_message)

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={api_key}"
    
    # สร้าง contents payload (ใช้ประวัติล่าสุด 4 ข้อความเพื่อความรวดเร็ว)
    contents = []
    if chat_history:
        for turn in chat_history[-4:]:
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
            "temperature": 0.4,
            "maxOutputTokens": 280,
            "topP": 0.9
        }
    }

    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        
        # ปรับ timeout ให้ตอบกลับเร็วภายใน 5 วินาที
        with urllib.request.urlopen(req, timeout=5) as response:
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
        logger.error(f"เกิดข้อผิดพลาดในการเรียก Gemini API (ใช้ Fallback): {e}")

    # หาก API ขัดข้องหรือตอบช้า ให้ใช้ Fallback Rule-based ทันที
    return fallback_rule_based_reply(user_message)


def fallback_rule_based_reply(user_message: str) -> str:
    """
    ระบบตอบกลับสำรองกรณีไม่มี API Key หรือ AI ขัดข้องชั่วคราว (สั้น กระชับ เป็นกันเอง)
    """
    msg = user_message.lower()
    
    is_three = any(w in msg for w in ["3 คน", "3คน", "สามคน", "3 ท่าน", "3ท่าน", "สามท่าน", "triple", "1600"])
    is_four = any(w in msg for w in ["4 คน", "4คน", "สี่คน", "4 ท่าน", "4ท่าน", "สี่ท่าน", "quad", "1800"])

    # 1. กรณีถามทั้ง 3 และ 4 คนพร้อมกัน หรือถามห้องครอบครัวทั่วไป
    if (is_three and is_four) or any(w in msg for w in ["ครอบครัว", "หลายท่าน", "หลายคน"]):
        return (
            f"มีค่ะ 😊 สำหรับเข้าพัก 3 - 4 ท่าน เรามีห้องใหญ่พิเศษ ขนาด 48 ตร.ม. มีห้องแต่งตัวเป็นสัดส่วนและชุดกาแฟค่ะ ✨\n\n"
            f"• **Grand Deluxe Triple Room (พัก 3 ท่าน)**: 1,600 บ./คืน (รวมอาหารเช้าบุฟเฟต์ฟรี 3 ท่าน)\n"
            f"• **Grand Deluxe 4 ท่าน Room (พัก 4 ท่าน)**: 1,800 บ./คืน (รวมอาหารเช้าบุฟเฟต์ฟรี 4 ท่าน)\n\n"
            f"เช็คห้องว่างและจองผ่าน LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk 💕"
        )
    # 2. กรณีถามเฉพาะห้อง 3 คน
    elif is_three:
        return (
            f"มีค่ะ 😊 สำหรับพัก 3 ท่าน แนะนำห้อง **Grand Deluxe Triple Room** ค่ะ 🛏️✨\n\n"
            f"• ขนาดใหญ่พิเศษ 48 ตร.ม. มีห้องแต่งตัวเป็นสัดส่วนและชุดกาแฟ\n"
            f"• ราคา **1,600 บาท/คืน** (**รวมอาหารเช้าบุฟเฟต์ฟรี 3 ท่าน**)\n\n"
            f"เช็คห้องว่างและจองผ่าน LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk 💕"
        )
    # 3. กรณีถามเฉพาะห้อง 4 คน
    elif is_four:
        return (
            f"มีค่ะ 😊 สำหรับพัก 4 ท่าน แนะนำห้อง **Grand Deluxe 4 ท่าน Room** ค่ะ 🛏️✨\n\n"
            f"• ขนาดใหญ่พิเศษ 48 ตร.ม. มีห้องแต่งตัวเป็นสัดส่วนและชุดกาแฟ\n"
            f"• ราคา **1,800 บาท/คืน** (**รวมอาหารเช้าบุฟเฟต์ฟรี 4 ท่าน**)\n\n"
            f"เช็คห้องว่างและจองผ่าน LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk 💕"
        )

    # 4. กรณีถามเช็คห้องว่าง / ว่างวันที่ ... ไหม / จองห้อง
    elif any(w in msg for w in ["ว่างไหม", "ว่างมั้ย", "มีห้องว่าง", "เช็คห้องว่าง", "คืนนี้ว่าง", "พรุ่งนี้ว่าง", "วันที่", "จอง"]):
        return (
            f"สำหรับการเช็คห้องว่างและจองห้องพัก คุณลูกค้าสามารถดำเนินการผ่าน **LINE OA: @ihotelkk** เท่านั้นนะคะ มีเจ้าหน้าที่เช็คสถานะห้องว่างให้ทันทีค่ะ 😊✨\n\n"
            f"📲 **LINE OA**: @ihotelkk\n"
            f"👉 คลิก: https://line.me/R/ti/p/@ihotelkk\n"
            f"☎️ **โทรติดต่อ**: {HOTEL_INFO['contact']['phone']} (บริการ 24 ชม. ค่ะ)"
        )

    # สอบถามระยะทาง / สถานที่ใกล้เคียง
    elif any(w in msg for w in ["ห่าง", "กี่กิโล", "กี่นาที", "มข", "ศรีนครินทร์", "เซ็นทรัล", "แคมปัส", "สนามบิน", "ไกลไหม", "เดินทาง"]):
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
            f"มีไข่กระทะ อาหารไทยปรุงสด สลัดบาร์ กาแฟสด ขนมปังสดใหม่ทุกเช้าค่ะ\n\n"
            f"• ห้อง Deluxe / Grand Deluxe: รวมอาหารเช้าฟรี 2-4 ท่านตามประเภทห้องค่ะ\n"
            f"• ห้อง Superior (750 บ.): ไม่รวมอาหารเช้า (ซื้อเพิ่มพร้อมห้องเพียง 100 บ./ท่าน) ค่ะ 😊"
        )

    # ราคาห้องพัก
    elif any(w in msg for w in ["ราคา", "ห้องพัก", "มีห้อง", "room", "price", "เตียง"]):
        return (
            f"สวัสดีค่ะ ยินดีต้อนรับสู่ {HOTEL_INFO['name_th']} นะคะ 🏨✨\n\n"
            f"• Superior: 750 บ. (ไม่รวมอาหารเช้า ซื้อเพิ่ม 100 บ./ท่าน)\n"
            f"• Deluxe / Grand Deluxe: เริ่มต้น 1,000 บ. (รวมอาหารเช้าฟรี 2 ท่าน)\n"
            f"• ห้องสำหรับ 3-4 ท่าน (Grand Deluxe): 1,600 - 1,800 บ. (รวมอาหารเช้าฟรี)\n\n"
            f"เช็คห้องว่างและจองผ่าน LINE OA: @ihotelkk ได้เลยนะคะ 👉 https://line.me/R/ti/p/@ihotelkk 💕"
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
            f"📲 เช็คห้องว่าง/จองผ่าน LINE OA: @ihotelkk (คลิก: https://line.me/R/ti/p/@ihotelkk)\n"
            f"☎️ โทรด่วน: {HOTEL_INFO['contact']['phone']} (24 ชม.)"
        )



