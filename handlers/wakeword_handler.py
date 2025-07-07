import threading
import time
from services import speech_recognizer
from wakeword.porcupine_listener import wakeword_listener
from services.play_audio import play_audio_wav
from services.text_to_speech import play_voice
from services.wakeword_listener import restart_wakeword_listener

# Trạng thái ngăn chặn lắng nghe song song
is_listening = False
lock = threading.Lock()

def on_wakeword_detected():
    global is_listening

    def handle_wakeword():
        global is_listening

        with lock:
            if is_listening:
                print("⚠️ Đã trong quá trình nhận lệnh, bỏ qua wakeword")
                return
            is_listening = True

        try:
            print("🔁 Restart WakewordListener để giải phóng thiết bị ghi âm")
            restart_wakeword_listener(wakeword_listener)

            print("🔊 Phát âm thanh phản hồi")
            play_audio_wav("./data/sound.wav")

            print("🎙️ Bắt đầu nhận giọng nói...")
            speech_recognizer.listen_and_recognize()
        except Exception as e:
            print(f"🔥 Lỗi khi xử lý wakeword: {e}")
        finally:
            is_listening = False
            print("✅ Hoàn tất xử lý wakeword")

    threading.Thread(target=handle_wakeword, daemon=True).start()
