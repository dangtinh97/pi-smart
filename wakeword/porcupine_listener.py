import pvporcupine
import pyaudio
import struct
import threading
import time
from core.event_bus import event_bus
from config import ACCESS_KEY, KEYWORD_PATH

class WakewordListener:
    def __init__(self):
        self.porcupine = pvporcupine.create(
            access_key=ACCESS_KEY,
            keyword_paths=[KEYWORD_PATH]
        )
        self.pa = None
        self.indexAudio = None
        self.stream = None
        self.running = False
        self.thread = None

        self._detect_input_device()

    def _detect_input_device(self):
        print("🔍 Đang dò thiết bị âm thanh...")
        pa = pyaudio.PyAudio()
        for i in range(pa.get_device_count()):
            info = pa.get_device_info_by_index(i)
            name = info['name']
            max_input = info['maxInputChannels']
            if 'usb' in name.lower() and max_input > 0:
                print(f"🎤 Tìm thấy mic USB tại index {i}: {name}")
                self.indexAudio = i
                break
        pa.terminate()
        if self.indexAudio is None:
            print("❌ Không tìm thấy mic USB. WakewordListener sẽ không hoạt động.")

    def start(self):
        if self.running:
            print("⚠️ WakewordListener đã chạy rồi.")
            return
        if self.indexAudio is None:
            print("🛑 Không có thiết bị input phù hợp.")
            return

        try:
            if self.pa:
                self.pa.terminate()
                time.sleep(0.3)
            self.pa = pyaudio.PyAudio()
            self.stream = self.pa.open(
                input_device_index=self.indexAudio,
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length
            )
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            print("🎧 WakewordListener khởi động.")
        except Exception as e:
            print(f"🛑 Không mở được stream: {e}")
            self.running = False
            if self.pa:
                self.pa.terminate()
            self.pa = None

    def stop(self):
        if not self.running:
            print("⚠️ WakewordListener đã dừng rồi.")
            return
        print("🛑 Đang dừng WakewordListener...")
        self.running = False

        try:
            if self.stream:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
        except Exception as e:
            print(f"⚠️ Lỗi khi dừng/đóng stream: {e}")
        self.stream = None

        if self.thread and self.thread.is_alive() and self.thread != threading.current_thread():
            try:
                self.thread.join(timeout=1)
            except RuntimeError:
                print("⚠️ Không thể join chính thread hiện tại.")
        self.thread = None
        print("✅ WakewordListener đã dừng.")
    def _run(self):
        print("👂 Đang lắng nghe wake word...")
        try:
            while self.running:
                if not self.stream:
                    print("⚠️ Stream không tồn tại. Thoát.")
                    break
                try:
                    pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                    pcm_unpacked = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                    result = self.porcupine.process(pcm_unpacked)
                    if result >= 0:
                        print("🔔 Wakeword phát hiện!")
                        event_bus.emit("wakeword.detected")
                except IOError as e:
                    print(f"⚠️ IOError khi đọc stream: {e}")
                    break
                except Exception as e:
                    print(f"⚠️ Lỗi không xác định khi đọc stream: {e}")
                    break
        except Exception as e:
            print(f"🔥 Lỗi lớn trong _run: {e}")
        finally:
            self.stop()
            print("🧹 Đã dọn dẹp sau khi lắng nghe xong.")

    def terminate(self):
        self.stop()
        if self.pa:
            try:
                self.pa.terminate()
            except Exception as e:
                print(f"⚠️ Lỗi khi terminate PyAudio: {e}")
        self.pa = None
        self.porcupine.delete()
        print("🗑️ WakewordListener đã được hủy.")
wakeword_listener = WakewordListener()