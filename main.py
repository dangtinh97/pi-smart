from typing import Union

from fastapi import FastAPI
import config_pinout
import RPi.GPIO as GPIO
import time
# import speech_recognition as sr
# r = sr.Recognizer()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}




def setup_ir():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(config_pinout.GPIO_IR_RECEIVER, GPIO.IN)
setup_ir()
def read_ir():
    if GPIO.input(config_pinout.GPIO_IR_RECEIVER) == GPIO.LOW:
        print("IR nhận tín hiệu")
    print("Đang lắng nghe IR trong 5 giây...")
    time.sleep(5)
read_ir()

# with sr.Microphone() as source:
#     print("Bắt đầu nhận giọng nói... (Ctrl+C để dừng)")
#
#     while True:
#         try:
#             print("⏺️ Đang lắng nghe...")
#             audio = r.listen(source)
#
#             print("🔍 Đang xử lý...")
#             text = r.recognize_google(audio, language="vi-VN")
#             print("🗣️ Bạn nói:", text)
#
#         except sr.UnknownValueError:
#             print("⚠️ Không hiểu được âm thanh.")
#         except sr.RequestError as e:
#             print("❌ Lỗi kết nối API:", e)
#         except KeyboardInterrupt:
#             print("\n🛑 Dừng lại bởi người dùng.")
#             break