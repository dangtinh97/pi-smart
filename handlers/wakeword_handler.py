import threading
import time
from services import speech_recognizer
from services.play_audio import play_audio_wav
from services.text_to_speech import play_voice
from services.wakeword_listener import restart_wakeword_listener
from services.speech_recognizer import listen_and_recognize
# Trạng thái ngăn chặn lắng nghe song song
is_listening = False
lock = threading.Lock()

def on_wakeword_detected(listener):
    global is_listening
    print("Ohh.... Wake word detected")
    play_audio_wav("./data/sound.wav")
    # time.sleep(5)
    # listen_and_recognize()
    # listener.start()
