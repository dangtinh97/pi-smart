# config.py

import os
from dotenv import load_dotenv

# Nạp biến từ file .env
load_dotenv()

# Hàm lấy biến từ môi trường, có fallback
def get(key, default=None, cast=str):
    val = os.getenv(key)
    return cast(val) if val is not None else default

# ==== Cấu hình chung ====

ACCESS_KEY     = get("ACCESS_KEY", "default-key")
KEYWORD_PATH   = get("KEYWORD_PATH", "data/hotwords/hey_pi_raspberry-pi.ppn")
GEMINI_API_KEY = get("GEMINI_API_KEY", "default-key")
PATH_MPG123 = get("PATH_MPG123", "/usr/bin/mpg123")