# services/speech_recognizer.py

import speech_recognition as sr
#from core.event_bus import event_bus

recognizer = sr.Recognizer()
mic = sr.Microphone()

def listen_and_recognize():
    print("🎙️ Đang nghe từ mic trực tiếp...")

    try:
        with mic as source:
            print("✅ Đã vào with mic")
            # recognizer.adjust_for_ambient_noise(source)
            # print("⌛ Đang lắng nghe...")
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=7)

        print("🔊 Đã thu âm xong, đang xử lý...")
        text = recognizer.recognize_google(audio, language="vi-VN")
        print("📝 Văn bản:", text)

    except sr.WaitTimeoutError:
        print("⏱️ Không có tiếng trong thời gian chờ.")
    except sr.UnknownValueError:
        print("❌ Không nhận được nội dung.")
    except sr.RequestError as e:
        print(f"⚠️ Lỗi Speech API: {e}")
    except Exception as e:
        print(f"🔥 Lỗi bất ngờ: {e}")