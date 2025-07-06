import sounddevice as sd
import pvporcupine

porcupine = ...
stream = None

def start():
    global stream
    stream = sd.InputStream(...)  # hoặc mở lại porcupine
    stream.start()

def stop():
    if stream:
        stream.stop()
        stream.close()
