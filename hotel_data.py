# -*- coding: utf-8 -*-
"""
ข้อมูลสารสนเทศโรงแรม I Hotel Khonkaen (โรงแรมไอ โฮเทล ขอนแก่น)
ใช้เป็น Knowledge Base ให้กับ AI และใช้แสดงข้อมูล Quick Replies
"""

HOTEL_INFO = {
    "name_th": "โรงแรม ไอ โฮเทล ขอนแก่น (I Hotel Khonkaen)",
    "name_en": "I Hotel Khon Kaen",
    "slogan": "ที่พักสไตล์โมเดิร์น บรรยากาศอบอุ่น สะอาด สะดวก ปลอดภัย ใจกลางเมืองขอนแก่น",
    
    "contact": {
        "phone": "080-457-9889",
        "phone_raw": "0804579889",
        "line_oa": "@ihotelkk",
        "facebook": "https://www.facebook.com/ihotelkhonkaen",
        "email": "contact@ihotelkhonkaen.com",
        "website": "https://www.ihotelkhonkaen.com"
    },
    
    "location": {
        "address": "999/99 หมู่ 3 ถนนมิตรภาพ ตำบลศิลา อำเภอเมือง จังหวัดขอนแก่น 40000",
        "google_maps_url": "https://maps.app.goo.gl/E6sbBJwRwNMSm4cB7",
        "nearby_places": [
            "เทสโก้ โลตัส โนนม่วง (โลตัส ขอนแก่น 3) (แผนที่: https://maps.app.goo.gl/eZ231QLWHQ8kCzFn9)",
            "มหาวิทยาลัยขอนแก่น (มข.)",
            "โรงพยาบาลศรีนครินทร์",
            "สนามบินนานาชาติขอนแก่น (15-20 นาที)"
        ]
    },
    
    "policies": {
        "booking": "การจองห้องพักทุกประเภท ต้องดำเนินการจองผ่าน LINE OA: @ihotelkk เท่านั้น (คลิก: https://line.me/R/ti/p/@ihotelkk)",
        "check_in": "ตั้งแต่ 14:00 น. เป็นต้นไป",
        "check_out": "ก่อน 12:00 น. (เที่ยงวัน)",
        "front_desk": "เปิดบริการ 24 ชั่วโมง มีเจ้าหน้าที่ดูแลตลอดเวลา",
        "pets": "ไม่อนุญาตให้นำสัตว์เลี้ยงเข้าพัก (เพื่อสุขอนามัยของผู้เข้าพักทุกท่าน)",
        "smoking": "ห้ามสูบบุหรี่ภายในห้องพัก (มีจุดสูบบุหรี่จัดไว้ภายนอกอาคาร)",
        "payment": "รับเงินสด, โอนเงินผ่าน QR Code พร้อมเพย์, บัตรเครดิต/เดบิต"
    },
    
    "breakfast_info": {
        "type": "อาหารเช้าแบบบุฟเฟต์ (Buffet Breakfast)",
        "menu_items": [
            "ขนมปังโฮลวีท ขนมปังปอนด์ และเบเกอรี่ พร้อมเนย/แยม",
            "น้ำส้มคั้น น้ำผลไม้สด และน้ำดื่มเย็นชื่นใจ",
            "อาหารไทยปรุงสดตามฤดูกาล ผัดผัก แกง และข้าวสวยร้อนๆ",
            "ชุดสลัดบาร์ผักสดพร้อมน้ำสลัด",
            "เมนูไทยทอดร้อนๆ เช่น ไข่กระทะ ไส้กรอก แฮม",
            "กาแฟสด ชงสดใหม่จากเครื่อง พร้อมชาและโอวัลติน",
            "เมนูอาหารพิเศษประจำวัน"
        ],
        "price_with_room": "100 บาท / ท่าน / วัน (เมื่อซื้อพร้อมห้องพัก)",
        "price_after_booking": "120 บาท / ท่าน / วัน (เมื่อซื้อเพิ่มหลังการจอง)",
        "included_rooms": "รวมฟรีในห้อง Deluxe และ Grand Deluxe"
    },
    
    "meeting_rooms": {
        "description": "บริการห้องประชุม สัมมนา และจัดเลี้ยง",
        "total_rooms": "4 ห้อง",
        "max_capacity": "รองรับได้สูงสุด 200 ท่าน",
        "contact_note": "สนใจจองหรือขอใบเสนอราคา ติดต่อได้ที่เบอร์ 080-457-9889 หรือ LINE OA: @ihotelkk"
    },
    
    "amenities": [
        "ฟรี Wi-Fi ความเร็วสูงทั่วบริเวณโรงแรมและในห้องพัก",
        "ที่จอดรถยนต์ส่วนตัวกว้างขวาง สะดวกสบาย มีกล้องวงจรปิด",
        "ระบบรักษาความปลอดภัย CCTV และระบบ Keycard 24 ชั่วโมง",
        "สมาร์ททีวี (Smart TV) พร้อมช่องเคเบิล",
        "เครื่องปรับอากาศ (แอร์) ทุกห้อง",
        "เครื่องทำน้ำอุ่น พร้อมชุดผ้าเช็ดตัวและเครื่องใช้ในห้องน้ำ",
        "ตู้เย็น, กาต้มน้ำร้อน, ชา/กาแฟ/น้ำดื่มฟรี",
        "ห้องประชุมสัมมนาจัดเลี้ยง 4 ห้อง รองรับได้ถึง 200 ท่าน",
        "บริการลิฟต์โดยสาร"
    ],
    
    "rooms": [
        {
            "id": "superior_twin",
            "name": "Superior Twin Bed (เตียงคู่)",
            "size": "28 ตร.ม.",
            "description": "ห้องสุพีเรียเตียงคู่ 2 เตียง ขนาด 28 ตร.ม. กว้างขวาง สะอาด สิ่งอำนวยความสะดวกครบ (ราคานี้ยังไม่รวมอาหารเช้า)",
            "price_starting": 750,
            "unit": "บาท / ห้อง / คืน",
            "capacity": "ผู้ใหญ่ 2 ท่าน",
            "bed_type": "เตียงเดี่ยว 3.5 ฟุต 2 เตียง",
            "breakfast": "ไม่รวมอาหารเช้า (ซื้อเพิ่มพร้อมห้อง 100 บ./ท่าน, หลังจอง 120 บ./ท่าน)",
            "image_url": "https://raw.githubusercontent.com/ihotelpo-creator/ihotel-facebook-bot/main/static/images/superior_2.jpg"
        },
        {
            "id": "superior_double",
            "name": "Superior Double Bed (เตียงเดี่ยว)",
            "size": "28 ตร.ม.",
            "description": "ห้องสุพีเรียเตียงเดี่ยวขนาดใหญ่ ขนาด 28 ตร.ม. เหมาะสำหรับ 1-2 ท่าน (ราคานี้ยังไม่รวมอาหารเช้า)",
            "price_starting": 750,
            "unit": "บาท / ห้อง / คืน",
            "capacity": "ผู้ใหญ่ 2 ท่าน",
            "bed_type": "เตียงเดี่ยว King Size ใหญ่",
            "breakfast": "ไม่รวมอาหารเช้า (ซื้อเพิ่มพร้อมห้อง 100 บ./ท่าน, หลังจอง 120 บ./ท่าน)",
            "image_url": "https://raw.githubusercontent.com/ihotelpo-creator/ihotel-facebook-bot/main/static/images/superior_1.jpg"
        },
        {
            "id": "deluxe_twin",
            "name": "Deluxe Twin Bed (เตียงคู่)",
            "size": "28 ตร.ม.",
            "description": "ห้องดีลักซ์เตียงคู่ ขนาด 28 ตร.ม. พร้อมชุดกาแฟ ผ้าดูเว่นุ่มสบาย และราคารวมอาหารเช้าบุฟเฟต์สำหรับ 2 ท่าน",
            "price_starting": 1000,
            "unit": "บาท / ห้อง / คืน",
            "capacity": "ผู้ใหญ่ 2 ท่าน",
            "bed_type": "เตียงเดี่ยว 3.5 ฟุต 2 เตียง (ผ้าดูเว่)",
            "breakfast": "รวมอาหารเช้าบุฟเฟต์ 2 ท่าน",
            "highlights": "ชุดกาแฟ, ผ้าดูเว่",
            "image_url": "https://raw.githubusercontent.com/ihotelpo-creator/ihotel-facebook-bot/main/static/images/deluxe_green.jpg"
        },
        {
            "id": "deluxe_double",
            "name": "Deluxe Double Bed (เตียงเดี่ยว)",
            "size": "28 ตร.ม.",
            "description": "ห้องดีลักซ์เตียงเดี่ยว ขนาด 28 ตร.ม. พร้อมชุดกาแฟ ผ้าดูเว่นุ่มสบาย และราคารวมอาหารเช้าบุฟเฟต์สำหรับ 2 ท่าน",
            "price_starting": 1000,
            "unit": "บาท / ห้อง / คืน",
            "capacity": "ผู้ใหญ่ 2 ท่าน",
            "bed_type": "เตียงเดี่ยว King Size ใหญ่ (ผ้าดูเว่)",
            "breakfast": "รวมอาหารเช้าบุฟเฟต์ 2 ท่าน",
            "highlights": "ชุดกาแฟ, ผ้าดูเว่",
            "image_url": "https://raw.githubusercontent.com/ihotelpo-creator/ihotel-facebook-bot/main/static/images/deluxe_blue.jpg"
        },
        {
            "id": "grand_deluxe_double",
            "name": "Grand Deluxe Double Bed (เตียงเดี่ยว)",
            "size": "48 ตร.ม.",
            "description": "ห้องแกรนด์ดีลักซ์ขนาดใหญ่พิเศษ 48 ตร.ม. มีห้องแต่งตัวเป็นสัดส่วน พร้อมชุดกาแฟ และราคารวมอาหารเช้าบุฟเฟต์สำหรับ 2 ท่าน",
            "price_starting": 1300,
            "unit": "บาท / ห้อง / คืน",
            "capacity": "ผู้ใหญ่ 2 ท่าน",
            "bed_type": "เตียง King Size พรีเมียม",
            "breakfast": "รวมอาหารเช้าบุฟเฟต์ 2 ท่าน",
            "highlights": "มีห้องแต่งตัวในตัว, ชุดกาแฟ",
            "image_url": "https://raw.githubusercontent.com/ihotelpo-creator/ihotel-facebook-bot/main/static/images/grand_deluxe_triple_3.jpg"
        },
        {
            "id": "grand_deluxe_triple",
            "name": "Grand Deluxe Triple Room (พัก 3 ท่าน)",
            "size": "48 ตร.ม.",
            "description": "ห้องแกรนด์ดีลักซ์ขนาดใหญ่ 48 ตร.ม. สำหรับ 3 ท่าน มีห้องแต่งตัวเป็นสัดส่วน พร้อมชุดกาแฟ และราคารวมอาหารเช้าบุฟเฟต์สำหรับ 3 ท่าน",
            "price_starting": 1600,
            "unit": "บาท / ห้อง / คืน",
            "capacity": "ผู้ใหญ่ 3 ท่าน",
            "bed_type": "เตียงสำหรับ 3 ท่าน",
            "breakfast": "รวมอาหารเช้าบุฟเฟต์ 3 ท่าน",
            "highlights": "มีห้องแต่งตัวในตัว, ชุดกาแฟ",
            "image_url": "https://raw.githubusercontent.com/ihotelpo-creator/ihotel-facebook-bot/main/static/images/grand_deluxe_triple_1.jpg"
        },
        {
            "id": "grand_deluxe_quad",
            "name": "Grand Deluxe 4 ท่าน Room (พัก 4 ท่าน)",
            "size": "48 ตร.ม.",
            "description": "ห้องแกรนด์ดีลักซ์ขนาดใหญ่ 48 ตร.ม. สำหรับ 4 ท่าน เหมาะสำหรับครอบครัวหรือกลุ่มเพื่อน มีห้องแต่งตัว ชุดกาแฟ และราคารวมอาหารเช้าบุฟเฟต์สำหรับ 4 ท่าน",
            "price_starting": 1800,
            "unit": "บาท / ห้อง / คืน",
            "capacity": "ผู้ใหญ่ 4 ท่าน",
            "bed_type": "เตียงสำหรับ 4 ท่าน",
            "breakfast": "รวมอาหารเช้าบุฟเฟต์ 4 ท่าน",
            "highlights": "มีห้องแต่งตัวในตัว, ชุดกาแฟ",
            "image_url": "https://raw.githubusercontent.com/ihotelpo-creator/ihotel-facebook-bot/main/static/images/grand_deluxe_triple_2.jpg"
        }
    ],
    
    "faqs": [
        {
            "question": "มีอาหารเช้าไหม ราคาเท่าไหร่?",
            "answer": "โรงแรมมีบริการอาหารเช้าแบบบุฟเฟต์ค่ะ\n- ห้อง Deluxe และ Grand Deluxe รวมอาหารเช้าฟรีตามจำนวนผู้เข้าพัก\n- ห้อง Superior ไม่รวมอาหารเช้า สามารถซื้อเพิ่มพร้อมห้องพักได้ในราคาพิเศษ 100 บาท/ท่าน/วัน (หากซื้อเพิ่มหลังการจอง 120 บาท/ท่าน)"
        },
        {
            "question": "โรงแรมตั้งอยู่ที่ไหน ใกล้ที่ไหนบ้าง?",
            "answer": "ตั้งอยู่ที่ 999/99 หมู่ 3 ถนนมิตรภาพ ต.ศิลา อ.เมือง จ.ขอนแก่น (ใกล้เทสโก้โลตัสโนนม่วง / โลตัสขอนแก่น 3)\n📍 แผนที่โรงแรม: https://maps.app.goo.gl/E6sbBJwRwNMSm4cB7"
        },
        {
            "question": "มีห้องประชุมสัมมนาไหม?",
            "answer": "มีค่ะ! โรงแรมมีห้องประชุมสัมมนาจัดเลี้ยงทั้งหมด 4 ห้อง รองรับได้สูงสุดถึง 200 ท่าน ติดต่อสอบถามหรือขอใบเสนอราคาได้ที่เบอร์ 080-457-9889 หรือ LINE OA: @ihotelkk ค่ะ"
        },
        {
            "question": "จองห้องพักอย่างไร / จองทางไหน?",
            "answer": "การจองห้องพักของโรงแรม I Hotel Khonkaen ลูกค้าจะต้องดำเนินการจองผ่าน LINE OA: @ihotelkk เท่านั้นค่ะ (คลิกเพิ่มเพื่อนเพื่อจอง: https://line.me/R/ti/p/@ihotelkk) เพื่อความสะดวกรวดเร็วในการเช็คห้องว่างและยืนยันการจองค่ะ ✨"
        },
        {
            "question": "เบอร์โทรและช่องทางติดต่อโรงแรม?",
            "answer": "โทร: 080-457-9889 หรือ LINE OA: @ihotelkk (มีเจ้าหน้าที่ดูแลตลอด 24 ชั่วโมงค่ะ)"
        }
    ]
}


def get_hotel_knowledge_prompt() -> str:
    """สร้าง Context ข้อมูลโรงแรมเพื่อส่งให้ System Prompt ของ Gemini AI"""
    rooms_text = "\n".join([
        f"- {r['name']} ({r['size']}): ราคา {r['price_starting']} {r['unit']}\n"
        f"  * พักได้: {r['capacity']} | รูปแบบเตียง: {r['bed_type']}\n"
        f"  * อาหารเช้า: {r['breakfast']}\n"
        f"  * รายละเอียด: {r['description']}"
        for r in HOTEL_INFO["rooms"]
    ])
    
    amenities_text = "\n".join([f"- {a}" for a in HOTEL_INFO["amenities"]])
    nearby_text = "\n".join([f"- {n}" for n in HOTEL_INFO["location"]["nearby_places"]])
    faqs_text = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in HOTEL_INFO["faqs"]])
    
    return f"""
ข้อมูลโรงแรม:
ชื่อ: {HOTEL_INFO['name_th']} ({HOTEL_INFO['name_en']})
สโลแกน: {HOTEL_INFO['slogan']}

ที่ตั้งและแผนที่:
- ที่อยู่: {HOTEL_INFO['location']['address']}
- แผนที่โรงแรม (Google Maps): {HOTEL_INFO['location']['google_maps_url']}
- สถานที่ใกล้เคียง:
{nearby_text}

ข้อมูลการติดต่อ:
- โทรศัพท์: {HOTEL_INFO['contact']['phone']}
- LINE OA: {HOTEL_INFO['contact']['line_oa']}

ข้อมูลอาหารเช้า (Buffet):
- ประเภท: {HOTEL_INFO['breakfast_info']['type']}
- ราคาซื้อพร้อมห้องพัก: {HOTEL_INFO['breakfast_info']['price_with_room']}
- ราคาซื้อเพิ่มหลังการจอง: {HOTEL_INFO['breakfast_info']['price_after_booking']}
- หมายเหตุ: ห้อง Deluxe และ Grand Deluxe รวมอาหารเช้าฟรีแล้ว

ประเภทห้องพักและราคา:
{rooms_text}

ห้องประชุมสัมมนาจัดเลี้ยง:
- จำนวน: {HOTEL_INFO['meeting_rooms']['total_rooms']}
- ความจุ: {HOTEL_INFO['meeting_rooms']['max_capacity']}
- {HOTEL_INFO['meeting_rooms']['description']}
- การติดต่อ: {HOTEL_INFO['meeting_rooms']['contact_note']}

สิ่งอำนวยความสะดวก:
{amenities_text}

นโยบายและเวลาทำการ:
- เช็คอิน: {HOTEL_INFO['policies']['check_in']}
- เช็คเอาท์: {HOTEL_INFO['policies']['check_out']}
- แผนกต้อนรับ: {HOTEL_INFO['policies']['front_desk']}
- สัตว์เลี้ยง: {HOTEL_INFO['policies']['pets']}
- การสูบบุหรี่: {HOTEL_INFO['policies']['smoking']}
- การชำระเงิน: {HOTEL_INFO['policies']['payment']}

คำถามที่พบบ่อย (FAQ):
{faqs_text}
"""
