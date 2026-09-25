# -*- coding: utf-8 -*-
"""
Helper module สำหรับโหลด Environment Variables จากไฟล์ .env
โดยไม่ต้องพึ่งพาไลบรารีภายนอก
"""

import os

def load_env_file(env_path: str = ".env"):
    """อ่านและโหลดค่าจากไฟล์ .env เข้าสู่ os.environ"""
    if not os.path.exists(env_path):
        return
        
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip().strip("'\"")
                    if key and key not in os.environ:
                        os.environ[key] = value
    except Exception as e:
        print(f"Error reading .env: {e}")

# โหลดทันทีเมื่อถูก import
load_env_file()
