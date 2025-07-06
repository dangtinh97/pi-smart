import threading
import time
from services import speech_recognizer
from wakeword.porcupine_listener import wakeword_listener
import os
is_listening = False
from services.text_to_speech import  play_voice
def on_wakeword_detected():
    global is_listening
    os.system("/opt/homebrew/bin/mpg123 './data/sound.mp3'")
    if is_listening:
        print("⚠️ Đã trong quá trình nhận lệnh, bỏ qua wakeword")
        return

    def handle():
        global is_listening
        is_listening = True

        try:
            print("🛑 Stopping wakeword listener...")
            wakeword_listener.stop()
            time.sleep(0.2)
            print("🎙️ Bắt đầu ghi âm từ mic...")
            speech_recognizer.listen_and_recognize()
        except Exception as e:
            print(f"🔥 Lỗi trong xử lý wakeword: {e}")
        finally:
            print("▶️ Bật lại wakeword listener")
            wakeword_listener.start()
            is_listening = False

    threading.Thread(target=handle, daemon=True).start()
