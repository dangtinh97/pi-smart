import pvporcupine
import pyaudio
import struct
import threading
import os
import time
import logging

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

ACCESS_KEY = "I2FzB0ROEKTLiBLnLa8jByF9b7wu+o6h4Z9PvWFKRwTpmZ9gmBpeaw=="
KEYWORD_PATH = "data/hotwords/raspberry.ppn"

def is_audio_device_ready(index, rate, frame_length):
    try:
        pa = pyaudio.PyAudio()
        stream = pa.open(
            input_device_index=index,
            rate=rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=frame_length
        )
        stream.close()
        pa.terminate()
        return True
    except Exception as e:
        logger.warning(f"⏳ Thiết bị chưa sẵn sàng: {e}")
        return False

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

        logger.info("🔍 Đang dò thiết bị âm thanh...")
        for i in range(self.pa.get_device_count()):
            info = self.pa.get_device_info_by_index(i)
            name = info['name']
            max_input = info['maxInputChannels']
            max_output = info['maxOutputChannels']
            logger.info(f"[{i}] {name} | Input: {max_input} | Output: {max_output}")
            if 'usb' in name.lower() and max_input > 0:
                logger.info(f"🎤 Tìm thấy mic USB tại index {i}: {name}")
                self.indexAudio = i
                break

        if self.indexAudio is None:
            logger.error("❌ Không tìm thấy mic USB. WakewordListener sẽ không hoạt động.")

    def play_audio(self, audio_file="data/sound_converted.wav"):
        """Phát âm thanh và đặt lại ALSA sau khi hoàn tất."""
        logger.info("🔊 Phát âm thanh...")
        os.system("mpg123 -o alsa -a hw:1,0 %s" % audio_file)
        time.sleep(1)  # Chờ giải phóng tài nguyên
        os.system("sudo alsactl init")
        time.sleep(0.5)
        logger.info("🔄 Đã đặt lại trạng thái ALSA.")

    def start(self):
        if self.running:
            logger.warning("⚠️ WakewordListener đã chạy rồi, không khởi động lại.")
            return
        if self.indexAudio is None:
            logger.error("🛑 Không có thiết bị input phù hợp. Hủy khởi động WakewordListener.")
            return

        os.system("sudo alsactl init")
        time.sleep(0.5)

        self.pa = pyaudio.PyAudio()
        logger.info(f"🔍 Device index: {self.indexAudio}, Sample rate: {self.porcupine.sample_rate}, Frame length: {self.porcupine.frame_length}")
        try:
            self.stream = self.pa.open(
                input_device_index=self.indexAudio,
                rate=self.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=1024
            )
            logger.info("🎧 Stream opened successfully")
        except Exception as e:
            logger.error(f"🛑 Không thể mở stream âm thanh: {e}")
            self.pa.terminate()
            return

        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info("🎧 WakewordListener khởi động.")

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
        logger.info("🛑 WakewordListener đã dừng.")

    def _run(self):
        logger.info("👂 Đang lắng nghe wake word...")
        try:
            while self.running:
                try:
                    pcm = self.stream.read(self.porcupine.frame_length, exception_on_overflow=False)
                    pcm_unpacked = struct.unpack_from("h" * self.porcupine.frame_length, pcm)
                    result = self.porcupine.process(pcm_unpacked)
                    if result >= 0:
                        logger.info("🔔 Wakeword phát hiện!")
                        self.play_audio(audio_file="data/sound.mp3")

                        self.running = False
                        self.stop()

                        logger.info("⏳ Đợi thiết bị âm thanh sẵn sàng trước khi restart...")
                        for _ in range(10):  # Chờ tối đa 5 giây
                            if is_audio_device_ready(self.indexAudio, self.porcupine.sample_rate, self.porcupine.frame_length):
                                break
                            time.sleep(0.5)

                        self.start()
                except Exception as e:
                    logger.error(f"🔥 Lỗi khi đọc stream: {e}")
                    break
        except Exception as e:
            logger.error(f"🔥 Lỗi trong wakeword_listener: {e}")
        finally:
            self.stop()

    def play_and_restart(self, audio_file="data/sound_converted.wav"):
        """Phát âm thanh và khởi động lại listener."""
        self.stop()
        self.play_audio(audio_file)
        logger.info("⏳ Đợi thiết bị âm thanh sẵn sàng trước khi restart...")
        for _ in range(10):
            if is_audio_device_ready(self.indexAudio, self.porcupine.sample_rate, self.porcupine.frame_length):
                break
            time.sleep(0.5)
        self.start()

    def terminate(self):
        self.stop()
        self.pa.terminate()
        self.porcupine.delete()
        logger.info("🗑️ WakewordListener đã được hủy.")

if __name__ == "__main__":
    wakeword_listener = WakewordListener()
    wakeword_listener.start()
    try:
        while True:
            time.sleep(1)  # Giữ chương trình chính chạy
    except KeyboardInterrupt:
        logger.info("🛑 Dừng WakewordListener bởi người dùng...")
        wakeword_listener.terminate()
