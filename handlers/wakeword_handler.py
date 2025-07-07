import threading
import time
from services import speech_recognizer
from wakeword.porcupine_listener import wakeword_listener
import os
from config import PATH_MPG123
from services.play_audio import play_audio_wav
is_listening = False
lock = threading.Lock()
from services.text_to_speech import  play_voice
from services.wakeword_listener import restart_wakeword_listener
def on_wakeword_detected():
    global is_listening
    def play_sound():
        try:
            play_audio_wav("./data/sound.wav")
            #os.system(f"{PATH_MPG123} -o alsa -a hw:1,0 ./data/sound.mp3")
        except Exception as e:
            print(f"Error play sound.mp3: {e}")

    with lock:
        if is_listening:
            print("⚠️ Đã trong quá trình nhận lệnh, bỏ qua wakeword")
            return
        is_listening = True

    def handle():

        global is_listening
        is_listening = True

        try:
            restart_wakeword_listener(wakeword_listener)
            print("🛑 Stopping wakeword listener...")
            # wakeword_listener.stop()
            time.sleep(1)
            # print("🎙️ Bắt đầu ghi âm từ mic...")
            speech_recognizer.listen_and_recognize()
        except Exception as e:
            print(f"🔥 Lỗi trong xử lý wakeword: {e}")
        finally:
            print("▶️ Bật lại wakeword listener")
            wakeword_listener.start()
            is_listening = False

    threading.Thread(target=lambda: (play_sound(), handle()), daemon=True).start()
