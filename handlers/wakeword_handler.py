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

def on_wakeword_detected(listener):
    global is_listening
    print("Ohh.... Wake word detected")
    play_audio_wav("./data/sound.wav")
