import pvporcupine
import pyaudio
import struct
import threading
import time
import simpleaudio as sa
import speech_recognition as sr

ACCESS_KEY = "I2FzB0ROEKTLiBLnLa8jByF9b7wu+o6h4Z9PvWFKRwTpmZ9gmBpeaw=="
KEYWORD_PATH = "data/hotwords/raspberry.ppn"
AUDIO_PLAY_PATH = "data/sound.wav"  # file WAV, không dùng mp3

class WakewordListener:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH]
        )
        self.pa = pyaudio.PyAudio()
        self.indexAudio = None
        self.stream = None
        self.running = False
        self.thread = None

        print("🔍 Đang dò mic USB...")
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            name = info['name']
            max_input = info['maxInputChannels']
            if 'usb' in name.lower() and max_input > 0:
                self.indexAudio = i
                print(f"🎤 Tìm thấy mic USB tại index {i}: {name}")
                break
        if self.indexAudio is None:
            raise RuntimeError("❌ Không tìm thấy mic USB")

    def start(self):
        if self.running:
            print("⚠️ WakewordListener đã chạy.")
            return
        self.stream = self.pa.open(
            input_device_index=self.indexAudio,
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
        )
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("🎧 WakewordListener khởi động.")

    def stop(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            import threading as th
            if th.current_thread() != self.thread:
                self.thread.join()
            else:
                print("⚠️ Đang gọi stop từ chính thread, không join để tránh lỗi")
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.thread = None
        print("🛑 WakewordListener đã dừng.")

    def _run(self):
        print("👂 Đang lắng nghe wake word...")
        try:
            while self.running:
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm_unpacked = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                result = self.porcupine.process(pcm_unpacked)
                if result >= 0:
                    print("🔔 Wakeword phát hiện!")
                    self.on_wakeword()
        except Exception as e:
            print(f"🔥 Lỗi trong wakeword_listener: {e}")
            self.stop()

    def on_wakeword(self):
        # Ghi đè xử lý khi phát hiện wakeword
        pass

    def terminate(self):
        self.stop()
        self.pa.terminate()
        self.porcupine.delete()


def play_sound(path):
    print(f"🔊 Phát âm thanh: {path}")
    wave_obj = sa.WaveObject.from_wave_file(path)
    play_obj = wave_obj.play()
    play_obj.wait_done()


def recognize_speech():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    with mic as source:
        print("🎙️ Bắt đầu nghe giọng nói, nói đi...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
    try:
        text = recognizer.recognize_google(audio, language="vi-VN")
        print(f"🗣️ Bạn nói: {text}")
    except sr.UnknownValueError:
        print("❌ Không nhận dạng được giọng nói.")
    except sr.RequestError as e:
        print(f"❌ Lỗi dịch vụ nhận dạng giọng nói: {e}")


if __name__ == "__main__":
    wakeword_listener = WakewordListener()

    def on_wakeword_detected():
        def handler():
            wakeword_listener.stop()
            play_sound(AUDIO_PLAY_PATH)
            recognize_speech()
            wakeword_listener.start()
        threading.Thread(target=handler).start()

    wakeword_listener.on_wakeword = on_wakeword_detected

    wakeword_listener.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("🛑 Dừng chương trình.")
        wakeword_listener.terminate()
