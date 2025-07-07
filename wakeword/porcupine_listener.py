# services/wakeword_listener.py

import pvporcupine
import pyaudio
import struct
import threading
from core.event_bus import event_bus

from config import ACCESS_KEY, KEYWORD_PATH

class WakewordListener:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH]
        )
        self.indexAudio = 0
        self.pa = pyaudio.PyAudio()
        self.stream = None
        self.running = False
        self.thread = None
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            name = info['name']
            max_input = info['maxInputChannels']
            max_output = info['maxOutputChannels']
            print(f"[{i}] {name} | Input: {max_input} | Output: {max_output}")
            if 'usb' in name.lower() and info['maxInputChannels'] > 0:
                print(f"🎤 Tìm thấy mic USB tại index {i}: {info['name']}")
                self.indexAudio = i
    def start(self):
        if self.running:
            print("⚠️ WakewordListener đã chạy rồi, không khởi động lại.")
            return

        # 💡 Luôn tạo lại stream mới để tránh lỗi AUHAL -50 trên macOS
        self.stream = self.pa.open(
            rate=self.porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=self.porcupine.frame_length,
            input_device_index=self.indexAudio
        )

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("🎧 WakewordListener khởi động.")

    def stop(self):
        self.running = False

        if self.stream and self.stream.is_active():
            self.stream.stop_stream()
        if self.stream:
            self.stream.close()
            self.stream = None

        if self.thread and self.thread != threading.current_thread():
            self.thread.join()
        self.thread = None

    def _run(self):
        print("🎧 Đang lắng nghe wake word...")
        try:
            while self.running:
                pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                pcm_unpacked = struct.unpack_from("h" * self.porcupine.frame_length, pcm)

                result = self.porcupine.process(pcm_unpacked)
                if result >= 0:
                    print("🔔 Wakeword phát hiện!")
                    event_bus.emit("wakeword.detected")

        except Exception as e:
            print(f"🔥 Lỗi trong wakeword_listener: {e}")

    def terminate(self):
        self.stop()
        self.pa.terminate()
        self.porcupine.delete()

# Global instance (có thể import từ nơi khác)
wakeword_listener = WakewordListener()
