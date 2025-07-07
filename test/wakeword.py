import pyaudio
import sys

# Redirect ALSA warnings
sys.stderr = open(os.devnull, 'w')
pa = pyaudio.PyAudio()

stream = pa.open(
    rate=16000,
    channels=1,
    format=pyaudio.paInt16,
    input=True,
    frames_per_buffer=1024,
)

print("Ghi âm OK!")
