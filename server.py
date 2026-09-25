# -*- coding: utf-8 -*-
"""
Standalone Lightweight HTTP Webhook Server (Zero External Dependencies)
สามารถรันได้ทันทีด้วย: python3 server.py
"""

import os
import json
import logging
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

import env_loader
from hotel_data import HOTEL_INFO
import gemini_service
import facebook_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("IHotelBotServer")

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "ihotel_khonkaen_secure_token_2026")
PORT = int(os.getenv("PORT", "8000"))
HOST = os.getenv("HOST", "0.0.0.0")

chat_sessions = {}

class FacebookWebhookHandler(BaseHTTPRequestHandler):
    def _send_response(self, content: str, content_type: str = "text/html", status_code: int = 200):
        self.send_response(status_code)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)

        # หน้าแรก Health Check
        if path == "/" or path == "":
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <title>{HOTEL_INFO['name_th']} - Facebook Bot</title>
                <style>
                    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; padding: 40px; background: #f0f2f5; }}
                    .card {{ background: white; max-width: 650px; margin: auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
                    h1 {{ color: #1877f2; margin-top: 0; }}
                    .status {{ display: inline-block; padding: 6px 14px; background: #e7f3ff; color: #1877f2; border-radius: 20px; font-weight: bold; margin-bottom: 20px; }}
                    .box {{ background: #f8f9fa; border: 1px solid #e4e6eb; padding: 15px; border-radius: 8px; margin: 15px 0; }}
                    code {{ background: #eee; padding: 2px 6px; border-radius: 4px; font-family: monospace; color: #d63384; }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>🏨 {HOTEL_INFO['name_th']}</h1>
                    <div class="status">🟢 Webhook Server Online (Port {PORT})</div>
                    <p>ระบบบอท Facebook Messenger ของโรงแรมพร้อมทำงานเรียบร้อยแล้วค่ะ</p>
                    
                    <div class="box">
                        <h3 style="margin-top:0;">📌 ข้อมูลสำหรับตั้งค่าบน Meta for Developers:</h3>
                        <p><strong>Callback URL:</strong> <code>https://YOUR-PUBLIC-URL/webhook</code></p>
                        <p><strong>Verify Token:</strong> <code>{VERIFY_TOKEN}</code></p>
                        <p><strong>Subscription Fields:</strong> <code>messages</code>, <code>messaging_postbacks</code></p>
                    </div>
                </div>
            </body>
            </html>
            """
            self._send_response(html, "text/html", 200)
            return

        # Webhook Verification
        elif path == "/webhook":
            hub_mode = query_params.get("hub.mode", [None])[0]
            hub_verify_token = query_params.get("hub.verify_token", [None])[0]
            hub_challenge = query_params.get("hub.challenge", [None])[0]

            logger.info(f"ได้รับ Verification request: mode={hub_mode}, token={hub_verify_token}")

            if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
                logger.info("✅ ยืนยัน Webhook Token สำเร็จ!")
                self._send_response(hub_challenge, "text/plain", 200)
            else:
                logger.warning("❌ ยืนยัน Webhook Token ไม่ถูกต้อง!")
                self._send_response("Verification token mismatch", "text/plain", 403)
            return

        else:
            self._send_response("Not Found", "text/plain", 404)

    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path

        if path == "/webhook":
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            try:
                body = json.loads(post_data)
            except Exception as e:
                logger.error(f"JSON Parse error: {e}")
                self._send_response("Bad Request", "text/plain", 400)
                return

            logger.info(f"ได้รับ Webhook Event: {json.dumps(body, ensure_ascii=False)}")

            if body.get("object") == "page":
                for entry in body.get("entry", []):
                    for messaging_event in entry.get("messaging", []):
                        sender_id = messaging_event.get("sender", {}).get("id")
                        if not sender_id:
                            continue

                        # จัดการข้อความทั่วไป
                        if "message" in messaging_event:
                            msg_obj = messaging_event["message"]
                            
                            # ตรวจสอบว่าเป็นการกดปุ่ม Quick Reply หรือไม่
                            if "quick_reply" in msg_obj:
                                payload = msg_obj["quick_reply"].get("payload")
                                self._handle_payload(sender_id, payload)
                            elif "text" in msg_obj:
                                text = msg_obj["text"]
                                self._process_text(sender_id, text)
                                
                        # จัดการ Postback Buttons
                        elif "postback" in messaging_event:
                            payload = messaging_event["postback"].get("payload")
                            self._handle_payload(sender_id, payload)

                self._send_response(json.dumps({"status": "EVENT_RECEIVED"}), "application/json", 200)
            else:
                self._send_response("Not Found", "text/plain", 404)
        else:
            self._send_response("Not Found", "text/plain", 404)

    def _process_text(self, sender_id: str, text: str):
        facebook_service.mark_seen(sender_id)
        facebook_service.send_typing_indicator(sender_id, is_typing=True)

        if sender_id not in chat_sessions:
            chat_sessions[sender_id] = []

        chat_sessions[sender_id].append({"sender": "user", "text": text})
        reply = gemini_service.generate_reply(text, chat_sessions[sender_id])
        chat_sessions[sender_id].append({"sender": "bot", "text": reply})

        facebook_service.send_text_message(sender_id, reply, with_quick_replies=True)

        lower_text = text.lower()
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






    def _handle_payload(self, sender_id: str, payload: str):
        from main import handle_payload_action
        handle_payload_action(sender_id, payload)


def run_server():
    server_address = (HOST, PORT)
    httpd = HTTPServer(server_address, FacebookWebhookHandler)
    print("=" * 60)
    print(f"🚀 I Hotel Khonkaen Facebook Webhook Server ทำงานอยู่ที่:")
    print(f"👉 http://127.0.0.1:{PORT}")
    print("=" * 60)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nหยุดการทำงานของเซิร์ฟเวอร์")
        httpd.server_close()

if __name__ == "__main__":
    run_server()
