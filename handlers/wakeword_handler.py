import threading
import time
from services import speech_recognizer
from services.play_audio import play_audio_wav
from services.text_to_speech import play_voice
from services.wakeword_listener import restart_wakeword_listener
from services.speech_recognizer import listen_and_recognize
from services.led_matrix import start_led_loop, stop_led_loop
# Trạng thái ngăn chặn lắng nghe song song
is_listening = False
lock = threading.Lock()

def on_wakeword_detected(listener):
    global is_listening

    if is_listening:
        print("⚠️ Đã trong quá trình nhận lệnh, bỏ qua wakeword")
        return

    is_listening = True

    def handle():
        global is_listening  # cần khai báo lại nếu gán
        try:
            print("🛑 Dừng WakewordListener để tránh xung đột mic...")
            # start_led_loop()
            listener.stop()
            time.sleep(1.0)
            print("🔔 Wake word detected!")
            play_audio_wav("./data/sound.wav")
            print("🎙️ Bắt đầu ghi âm từ mic...")
            listen_and_recognize()
            # stop_led_loop()
        except Exception as e:
            print(f"🔥 Lỗi trong xử lý wakeword: {e}")

        finally:
            print("▶️ Khởi động lại WakewordListener...")
            time.sleep(0.5)
            listener.start()
            is_listening = False

    # ✅ Thread được tạo đúng chỗ
    threading.Thread(target=handle, daemon=True).start()
