import pigpio
import time
from ir_remote import NECDecoder
import config_pinout  # Đảm bảo có GPIO_IR_RECEIVER = 26 hoặc GPIO bạn dùng

IR_GPIO = config_pinout.GPIO_IR_RECEIVER

class IRCombinedDecoder:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self.last_tick = 0
        self.pulses = []
        self.in_frame = False
        self.last_level = 1
        self.frame_timeout = 0.1
        self.decoder = NECDecoder()

        self.bits = 0
        self.code = 0
        self.in_code = False

        self.cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        dt = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick

        # Lưu pulse cho py-ir-remote
        if self.in_frame:
            self.pulses.append(dt)

        # Bắt đầu khung tín hiệu nếu gặp cạnh FALLING
        if not self.in_frame and level == 0:
            self.in_frame = True
            self.pulses = []

        # === Giải mã NEC thủ công bằng tickDiff giữa các cạnh FALLING ===
        if level != 0:
            return

        if dt < 100:
            return  # Bỏ nhiễu

        if 7000 <= dt <= 12000:
            print(f"[NEC] HEADER STARTED (dt = {dt} µs)")
            self.in_code = True
            self.bits = 0
            self.code = 0
            return

        if self.in_code:
            if 1000 <= dt <= 1300:  # bit 0
                self.code = (self.code << 1) | 0
                self.bits += 1
                print(f"[NEC] Bit {self.bits}: 0 (dt={dt})")
            elif 2000 <= dt <= 2500:  # bit 1
                self.code = (self.code << 1) | 1
                self.bits += 1
                print(f"[NEC] Bit {self.bits}: 1 (dt={dt})")
            else:
                print(f"[NEC] Invalid pulse: dt = {dt} µs → Reset")
                self.in_code = False
                self.bits = 0
                self.code = 0
                return

            if self.bits == 32:
                print(f"✅ [NEC] Mã IR (thủ công): 0x{self.code:08X}")
                self.in_code = False

    def listen_and_decode(self):
        try:
            while True:
                time.sleep(self.frame_timeout)
                if self.in_frame and len(self.pulses) > 10:
                    try:
                        code = self.decoder.decode(self.pulses)
                        if code:
                            print(f"✅ [py-ir-remote] Mã IR: 0x{code:08X}")
                        else:
                            print("[py-ir-remote] Không giải mã được")
                    except Exception as e:
                        print(f"[ERROR] py-ir-remote decode fail: {e}")
                    self.pulses = []
                    self.in_frame = False
        except KeyboardInterrupt:
            print("\n>> Đã thoát.")
        finally:
            self.cb.cancel()


def main():
    pi = pigpio.pi()
    if not pi.connected:
        print("⛔ Không kết nối được pigpiod. Chạy `sudo pigpiod` trước.")
        return

    pi.set_mode(IR_GPIO, pigpio.INPUT)
    pi.set_pull_up_down(IR_GPIO, pigpio.PUD_UP)

    print(f">> Đang lắng nghe IR trên GPIO {IR_GPIO}...")

    listener = IRCombinedDecoder(pi, IR_GPIO)
    listener.listen_and_decode()

    pi.stop()


if __name__ == "__main__":
    main()
