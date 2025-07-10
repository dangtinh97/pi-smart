# services/speech_recognizer.py

import speech_recognition as sr
import asyncio
import threading
from services.ai_agent import aiAgent
def listen_and_recognize():
    import speech_recognition as sr

    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # tùy mic
    recognizer.pause_threshold = 2.0   # 💥 im lặng 2 giây thì kết thúc câu

    mic = sr.Microphone()

    print("🎙️ Đang nghe từ mic trực tiếp...")
    with mic as source:
        print("✅ Đã vào with mic")
        audio = recognizer.listen(source)  # tự dừng sau khi im 2 giây
        print("🔊 Đã thu âm xong, đang xử lý...")

    try:
        text = recognizer.recognize_google(audio, language="vi-VN")
        print("📝 Văn bản:", text)

        # ✅ Gọi bất đồng bộ mà không chờ
        def run_async():
            asyncio.run(aiAgent.question(text))

        threading.Thread(target=run_async).start()
    except sr.UnknownValueError:
        print("🤷‍♂️ Không nhận diện được nội dung")
    except sr.RequestError as e:
        print(f"🔥 Lỗi kết nối tới Google Speech: {e}")
