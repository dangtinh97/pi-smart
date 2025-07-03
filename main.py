from typing import Union

from fastapi import FastAPI
import speech_recognition as sr
r = sr.Recognizer()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


with sr.Microphone() as source:
    print("Bắt đầu nhận giọng nói... (Ctrl+C để dừng)")

    while True:
        try:
            print("⏺️ Đang lắng nghe...")
            audio = r.listen(source)

            print("🔍 Đang xử lý...")
            text = r.recognize_google(audio, language="vi-VN")
            print("🗣️ Bạn nói:", text)

        except sr.UnknownValueError:
            print("⚠️ Không hiểu được âm thanh.")
        except sr.RequestError as e:
            print("❌ Lỗi kết nối API:", e)
        except KeyboardInterrupt:
            print("\n🛑 Dừng lại bởi người dùng.")
            break