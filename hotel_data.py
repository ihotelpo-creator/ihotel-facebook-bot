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
        "phone": "043-000-000, 080-000-0000",
        "line_oa": "@ihotelkhonkaen",
        "facebook": "https://www.facebook.com/ihotelkhonkaen",
        "email": "contact@ihotelkhonkaen.com",
        "website": "https://www.ihotelkhonkaen.com"
    },
    
    "location": {
        "address": "ถ.เลี่ยงเมือง ต.บ้านเป็ด อ.เมืองขอนแก่น จ.ขอนแก่น 40000",
        "google_maps_url": "https://maps.app.goo.gl/example",
        "nearby_places": [
            "สนามบินนานาชาติขอนแก่น (ขับรถประมาณ 10-15 นาที)",
            "มหาวิทยาลัยขอนแก่น (มข.) (ขับรถประมาณ 10 นาที)",
            "บึงหนองโคตร (ขับรถประมาณ 5-7 นาที)",
            "เซ็นทรัลพลาซา ขอนแก่น (ขับรถประมาณ 12 นาที)",
            "โรงพยาบาลศรีนครินทร์ และ โรงพยาบาลกรุงเทพขอนแก่น"
        ]
    },
    
    "policies": {
        "check_in": "ตั้งแต่ 14:00 น. เป็นต้นไป (เช็คอินก่อนเวลาขึ้นอยู่กับห้องว่าง)",
        "check_out": "ก่อน 12:00 น. (เที่ยงวัน)",
        "front_desk": "เปิดบริการ 24 ชั่วโมง มีเจ้าหน้าที่ดูแลตลอดเวลา",
        "pets": "ไม่อนุญาตให้นำสัตว์เลี้ยงเข้าพัก (เพื่อสุขอนามัยของผู้เข้าพักทุกท่าน)",
        "smoking": "ห้ามสูบบุหรี่ภายในห้องพัก (มีจุดสูบบุหรี่จัดไว้ภายนอกอาคาร)",
        "payment": "รับเงินสด, โอนเงินผ่าน QR Code พร้อมเพย์, บัตรเครดิต/เดบิต"
    },
    
    "amenities": [
        "ฟรี Wi-Fi ความเร็วสูงทั่วบริเวณโรงแรมและในห้องพัก",
        "ที่จอดรถยนต์ส่วนตัวกว้างขวาง สะดวกสบาย มีกล้องวงจรปิด",
        "ระบบรักษาความปลอดภัย CCTV และระบบ Keycard 24 ชั่วโมง",
        "สมาร์ททีวี (Smart TV) พร้อมช่องเคเบิล",
        "เครื่องปรับอากาศ (แอร์) ทุกห้อง",
        "เครื่องทำน้ำอุ่น พร้อมชุดผ้าเช็ดตัวและเครื่องใช้ในห้องน้ำ",
        "ตู้เย็น, กาต้มน้ำร้อน, ชา/กาแฟ/น้ำดื่มฟรี",
        "บริการมุมกาแฟและเครื่องดื่มบริเวณล็อบบี้",
        "บริการลิฟต์โดยสาร"
    ],
    
    "rooms": [
        {
            "id": "standard_double",
            "name": "Standard Double Room (เตียงเดี่ยว คิงไซส์)",
            "description": "ห้องพักเตียงเดี่ยวขนาดใหญ่ เหมาะสำหรับ 1-2 ท่าน พร้อมสิ่งอำนวยความสะดวกครบครัน",
            "price_starting": 750,
            "unit": "บาท / คืน",
            "capacity": "ผู้ใหญ่ 2 ท่าน",
            "bed_type": "เตียงเดี่ยว King Size 6 ฟุต",
            "image_url": "https://images.unsplash.com/photo-1590490360182-c33d57733427?w=600"
        },
        {
            "id": "standard_twin",
            "name": "Standard Twin Room (เตียงคู่)",
            "description": "ห้องพักเตียงคู่ 2 เตียง สำหรับเพื่อนร่วมเดินทางหรือครอบครัวขนาดเล็ก",
            "price_starting": 750,
            "unit": "บาท / คืน",
            "capacity": "ผู้ใหญ่ 2 ท่าน",
            "bed_type": "เตียงเดี่ยว 3.5 ฟุต จำนวน 2 เตียง",
            "image_url": "https://images.unsplash.com/photo-1566665797739-1674de7a421a?w=600"
        },
        {
            "id": "deluxe_room",
            "name": "Deluxe King Room (ห้องดีลักซ์)",
            "description": "ห้องพักกว้างขวางเป็นพิเศษ ตกแต่งโมเดิร์น พร้อมโซฟานั่งเล่นและวิวเปิดโล่ง",
            "price_starting": 850,
            "unit": "บาท / คืน",
            "capacity": "ผู้ใหญ่ 2 ท่าน (เสริมเตียงได้)",
            "bed_type": "เตียง King Size พรีเมียม",
            "image_url": "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?w=600"
        },
        {
            "id": "family_suite",
            "name": "Family Suite (ห้องครอบครัว)",
            "description": "ห้องพักขนาดใหญ่พิเศษสำหรับครอบครัวหรือกลุ่มเพื่อน พักผ่อนได้อย่างสบาย",
            "price_starting": 1200,
            "unit": "บาท / คืน",
            "capacity": "ผู้ใหญ่ 3-4 ท่าน",
            "bed_type": "1 เตียงใหญ่ + 1 เตียงเดี่ยว หรือ 2 เตียงใหญ่",
            "image_url": "https://images.unsplash.com/photo-1578683010236-d716f9a3f461?w=600"
        }
    ],
    
    "faqs": [
        {
            "question": "มีอาหารเช้าไหม?",
            "answer": "ทางโรงแรมมีบริการมุมชากาแฟ โอวัลติน และขนมปังบริการฟรีบริเวณล็อบบี้ช่วงเช้า (สำหรับเซ็ตอาหารเช้าแบบจานหลัก สามารถสอบถามพนักงานต้อนรับเพิ่มเติมได้ค่ะ)"
        },
        {
            "question": "เช็คอินดึกได้ไหม?",
            "answer": "สามารถเช็คอินได้ตลอด 24 ชั่วโมงค่ะ แผนกต้อนรับมีเจ้าหน้าที่ประจำการตลอดคืน หากเดินทางมาถึงดึกสามารถแจ้งเวลาโดยประมาณไว้ล่วงหน้าได้ค่ะ"
        },
        {
            "question": "มีที่จอดรถไหม?",
            "answer": "มีลานจอดรถส่วนตัวของโรงแรมกว้างขวาง จอดฟรี ปลอดภัย มีไฟส่องสว่างและกล้องวงจรปิดดูแลตลอด 24 ชม. ค่ะ"
        },
        {
            "question": "จองห้องพักอย่างไร?",
            "answer": "สามารถแจ้งวันที่เข้าพัก จำนวนคืน และประเภทห้องพักในแชทนี้ได้เลยค่ะ หรือโทรติดต่อเจ้าหน้าที่โดยตรงที่ 043-000-000 ค่ะ"
        }
    ]
}


def get_hotel_knowledge_prompt() -> str:
    """สร้าง Context ข้อมูลโรงแรมเพื่อส่งให้ System Prompt ของ Gemini AI"""
    rooms_text = "\n".join([
        f"- {r['name']}: ราคาเริ่มต้น {r['price_starting']} {r['unit']} (พักได้ {r['capacity']}, รูปแบบเตียง: {r['bed_type']}) - {r['description']}"
        for r in HOTEL_INFO["rooms"]
    ])
    
    amenities_text = "\n".join([f"- {a}" for a in HOTEL_INFO["amenities"]])
    nearby_text = "\n".join([f"- {n}" for n in HOTEL_INFO["location"]["nearby_places"]])
    faqs_text = "\n".join([f"Q: {f['question']}\nA: {f['answer']}" for f in HOTEL_INFO["faqs"]])
    
    return f"""
ข้อมูลโรงแรม:
ชื่อ: {HOTEL_INFO['name_th']} ({HOTEL_INFO['name_en']})
สโลแกน: {HOTEL_INFO['slogan']}

ที่ตั้ง: {HOTEL_INFO['location']['address']}
สถานที่ใกล้เคียง:
{nearby_text}

ประเภทห้องพักและราคา:
{rooms_text}

สิ่งอำนวยความสะดวก:
{amenities_text}

นโยบายและเวลาทำการ:
- เช็คอิน: {HOTEL_INFO['policies']['check_in']}
- เช็คเอาท์: {HOTEL_INFO['policies']['check_out']}
- แผนกต้อนรับ: {HOTEL_INFO['policies']['front_desk']}
- สัตว์เลี้ยง: {HOTEL_INFO['policies']['pets']}
- การสูบบุหรี่: {HOTEL_INFO['policies']['smoking']}
- การชำระเงิน: {HOTEL_INFO['policies']['payment']}

การติดต่อ:
- โทรศัพท์: {HOTEL_INFO['contact']['phone']}
- Line OA: {HOTEL_INFO['contact']['line_oa']}

คำถามที่พบบ่อย (FAQ):
{faqs_text}
"""
