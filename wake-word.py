import pvporcupine
import sounddevice as sd
import numpy as np

# === Load hotword ===
KEYWORD_PATH = "/Users/dangtinhvu/Documents/Pi/Hey-Pi-Smart_en_mac_v3_0_0/Hey-Pi-Smart_en_mac_v3_0_0.ppn"  # chỉnh đúng path file .ppn

porcupine = pvporcupine.create(
    access_key="",
    keyword_paths=[KEYWORD_PATH]
)

# === Callback xử lý âm thanh ===
def audio_callback(indata, frames, time, status):
    if status:
        print('Status:', status)

    # Chuyển từ bytes -> int16
    pcm = np.frombuffer(indata, dtype=np.int16)
    result = porcupine.process(pcm)
    if result >= 0:
        print("✅ Phát hiện từ khóa: 'Hey Pi'")
        raise sd.CallbackStop  # dừng stream ngay

# === Mở stream âm thanh ===
with sd.InputStream(
    channels=1,
    samplerate=porcupine.sample_rate,
    blocksize=porcupine.frame_length,
    dtype='int16',
    callback=audio_callback
):
    print("🎧 Đang lắng nghe từ khóa 'Hey Pi'...")
    sd.sleep(60 * 1000)  # Lắng nghe trong 60 giây (hoặc until được trigger)
