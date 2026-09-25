# -*- coding: utf-8 -*-
"""
Interactive Terminal Test Script สำหรับจำลองการแชทกับบอทโรงแรม I Hotel Khonkaen
สามารถใช้ทดสอบความฉลาดของคำตอบ AI ได้ทันทีโดยไม่ต้องต่อ Facebook Messenger
"""

import os
import sys
import env_loader
from hotel_data import HOTEL_INFO
import gemini_service

def run_chat_simulator():
    print("=" * 60)
    print(f"🏨 ระบบจำลองแชท: {HOTEL_INFO['name_th']}")
    print("=" * 60)
    
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key == "YOUR_GEMINI_API_KEY_HERE":
        print("⚠️  หมายเหตุ: ยังไม่ได้ใส่ GEMINI_API_KEY ในไฟล์ .env")
        print("   (ระบบจะทำงานด้วยโหมด Fallback Rule-based อัตโนมัติ)")
    else:
        print("✨ สถานะ: AI Engine (Gemini 1.5 Flash) พร้อมทำงาน")
        
    print("\nพิมพ์ข้อความเพื่อทดสอบ เช่น:")
    print("  1. 'มีห้องพักแบบไหนบ้าง ราคาเท่าไหร่'")
    print("  2. 'อยู่แถวไหน ใกล้ มข ไหม'")
    print("  3. 'เช็คอินกี่โมง เช็คอินตี 2 ได้ไหม'")
    print("  4. 'มีที่จอดรถไหมคะ'")
    print("  (พิมพ์ 'exit' หรือ 'q' เพื่อออกจากโปรแกรม)\n")
    print("-" * 60)

    chat_history = []

    while True:
        try:
            user_input = input("\n👤 ลูกค้า: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit", "q", "ออก"]:
                print("\nขอบคุณที่ร่วมทดสอบค่ะ สวัสดีค่ะ 🙏")
                break

            # บันทึกประวัติ
            chat_history.append({"sender": "user", "text": user_input})
            
            # ดึงคำตอบจาก AI
            reply = gemini_service.generate_reply(user_input, chat_history)
            
            # บันทึกประวัติ
            chat_history.append({"sender": "bot", "text": reply})
            
            print(f"\n🤖 น้องไอ (I Hotel):")
            print(reply)
            print("\n[🔘 Quick Replies: 🛏️ ห้องพัก | 📍 แผนที่ | 🕒 เช็คอิน | 🍳 อาหารเช้า | 📞 ติดต่อ]")
            print("-" * 60)

        except KeyboardInterrupt:
            print("\n\nสิ้นสุดการทดสอบ สวัสดีค่ะ 🙏")
            break
        except Exception as e:
            print(f"\nเกิดข้อผิดพลาด: {e}")

if __name__ == "__main__":
    run_chat_simulator()
