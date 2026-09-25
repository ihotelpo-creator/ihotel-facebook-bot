# -*- coding: utf-8 -*-
"""
Facebook Messenger Graph API Service
สำหรับส่งข้อความกลับหาผู้ใช้ผ่าน Send API (v19.0)
รองรับ Text, Quick Replies, Generic Templates (Carousels), และ Typing Indicators
"""

import os
import json
import logging
import urllib.request
import urllib.error
import env_loader
from hotel_data import HOTEL_INFO

logger = logging.getLogger(__name__)

GRAPH_API_VERSION = "v19.0"
GRAPH_URL = f"https://graph.facebook.com/{GRAPH_API_VERSION}/me/messages"


def get_page_access_token() -> str:
    return os.getenv("PAGE_ACCESS_TOKEN", "")


def send_raw_message(payload: dict) -> bool:
    """ส่ง payload ไปยัง Facebook Graph Send API"""
    token = get_page_access_token()
    if not token or token == "YOUR_PAGE_ACCESS_TOKEN_HERE":
        logger.warning("PAGE_ACCESS_TOKEN ยังไม่ได้ตั้งค่า ไม่สามารถส่งข้อความผ่าน Facebook API ได้")
        return False

    url = f"{GRAPH_URL}?access_token={token}"
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            logger.info(f"ส่งข้อความ Facebook สำเร็จ: message_id={data.get('message_id')}")
            return True
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        logger.error(f"Facebook Graph API Error {e.code}: {error_body}")
        return False
    except Exception as e:
        logger.error(f"เกิดข้อผิดพลาดในการส่งข้อความ Facebook: {e}")
        return False


def send_typing_indicator(recipient_id: str, is_typing: bool = True):
    """แสดงสถานะ กำลังพิมพ์... (Typing indicator) หรือ Mark Seen"""
    action = "typing_on" if is_typing else "typing_off"
    payload = {
        "recipient": {"id": recipient_id},
        "sender_action": action
    }
    send_raw_message(payload)


def mark_seen(recipient_id: str):
    """ทำเครื่องหมายว่าอ่านแล้ว (Mark seen)"""
    payload = {
        "recipient": {"id": recipient_id},
        "sender_action": "mark_seen"
    }
    send_raw_message(payload)


def get_default_quick_replies() -> list:
    """ปุ่มลัด (Quick Replies) ยอดนิยมสำหรับลูกค้าโรงแรม"""
    return [
        {
            "content_type": "text",
            "title": "🛏️ ดูห้องพักและราคา",
            "payload": "QR_ROOMS_AND_PRICES"
        },
        {
            "content_type": "text",
            "title": "📍 แผนที่และการเดินทาง",
            "payload": "QR_LOCATION_MAP"
        },
        {
            "content_type": "text",
            "title": "🕒 เวลาเช็คอิน/เช็คเอาท์",
            "payload": "QR_CHECKIN_INFO"
        },
        {
            "content_type": "text",
            "title": "🍳 อาหารเช้า/บริการ",
            "payload": "QR_AMENITIES_BREAKFAST"
        },
        {
            "content_type": "text",
            "title": "📞 ติดต่อพนักงาน",
            "payload": "QR_CONTACT_STAFF"
        }
    ]


def send_text_message(recipient_id: str, text: str, with_quick_replies: bool = True) -> bool:
    """ส่งข้อความตัวอักษร พร้อมปุ่มลัด Quick Replies ด้านล่าง"""
    message_obj = {"text": text}
    
    if with_quick_replies:
        message_obj["quick_replies"] = get_default_quick_replies()

    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": message_obj
    }
    return send_raw_message(payload)


def send_room_carousel(recipient_id: str) -> bool:
    """ส่งการ์ดห้องพัก (Generic Template Carousel) แสดงประเภทห้อง รูปภาพ และราคา"""
    elements = []
    
    for room in HOTEL_INFO["rooms"]:
        elements.append({
            "title": f"{room['name']} - เริ่มต้น {room['price_starting']} {room['unit']}",
            "image_url": room.get("image_url", ""),
            "subtitle": f"👥 {room['capacity']} | {room['bed_type']}\n{room['description']}",
            "buttons": [
                {
                    "type": "postback",
                    "title": "🛎️ สนใจจองห้องนี้",
                    "payload": f"BOOK_ROOM_{room['id']}"
                },
                {
                    "type": "phone_number",
                    "title": "📞 โทรสอบถาม",
                    "payload": HOTEL_INFO["contact"]["phone"].split(",")[0].strip().replace("-", "")
                }
            ]
        })

    payload = {
        "recipient": {"id": recipient_id},
        "messaging_type": "RESPONSE",
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "generic",
                    "elements": elements
                }
            },
            "quick_replies": get_default_quick_replies()
        }
    }
    return send_raw_message(payload)
