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
        self.pa = pyaudio.PyAudio()
        self.indexAudio = None
        self.stream = None
        self.running = False
        self.thread = None

        print("🔍 Đang dò thiết bị âm thanh...")
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            name = info['name']
            max_input = info['maxInputChannels']
            max_output = info['maxOutputChannels']
            print(f"[{i}] {name} | Input: {max_input} | Output: {max_output}")
            if 'usb' in name.lower() and max_input > 0:
                print(f"🎤 Tìm thấy mic USB tại index {i}: {name}")
                self.indexAudio = i
                break

        if self.indexAudio is None:
            print("❌ Không tìm thấy mic USB. WakewordListener sẽ không hoạt động.")

    def start(self):
        if self.running:
            print("⚠️ WakewordListener đã chạy rồi, không khởi động lại.")
            return

        if self.indexAudio is None:
            print("🛑 Không có thiết bị input phù hợp. Hủy khởi động WakewordListener.")
            return

        # Đảm bảo không có stream cũ còn mở
        if self.stream:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                print(f"⚠️ Lỗi khi đóng stream cũ: {e}")
            self.stream = None

        # Re-initialize PyAudio để tránh xung đột sau khi stop
        try:
            self.pa.terminate()
        except:
            pass
        self.pa = pyaudio.PyAudio()

        try:
            self.stream = self.pa.open(
                input_device_index=self.indexAudio,
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self.porcupine.frame_length,
            )
        except Exception as e:
            print(f"🛑 Không thể mở stream âm thanh: {e}")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("🎧 WakewordListener khởi động.")

    def stop(self):
        print("🛑 Đang dừng WakewordListener...")
        self.running = False

        # Dừng stream nếu còn hoạt động
        if self.stream:
            try:
                if self.stream.is_active():
                    self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                print(f"⚠️ Lỗi khi dừng/đóng stream: {e}")
            finally:
                self.stream = None

        # Dừng thread nếu không phải thread hiện tại
        if self.thread and self.thread.is_alive():
            if self.thread != threading.current_thread():
                self.thread.join()
            else:
                print("⚠️ Không thể join chính thread hiện tại.")
        self.thread = None

        print("✅ WakewordListener đã dừng.")

    def _run(self):
        print("👂 Đang lắng nghe wake word...")
        try:
            while self.running:
                if self.stream is None:
                    print("⚠️ Stream không tồn tại. Thoát listener.")
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
        self.pa.terminate()
        self.porcupine.delete()

# Global instance
wakeword_listener = WakewordListener()
