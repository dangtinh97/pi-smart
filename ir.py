import pigpio
import time
import config_pinout

IR_GPIO = config_pinout.GPIO_IR_RECEIVER  # ví dụ: GPIO26

class IR_NEC_Listener:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self.last_tick = 0
        self.bits = 0
        self.code = 0
        self.in_code = False
        self.cb = pi.callback(gpio, pigpio.FALLING_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        dt = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick

        # Header NEC: ~9ms
        if 7000 <= dt <= 12000:
            print(f"[DEBUG] HEADER STARTED (dt = {dt} µs)")
            self.in_code = True
            self.bits = 0
            self.code = 0
            return

        if self.in_code:
            if 150 <= dt <= 1000:  # bit 0
                self.code = (self.code << 1) | 0
                self.bits += 1
                print(f"[DEBUG] Bit {self.bits}: 0 (dt={dt})")
            elif 800 <= dt <= 2800:  # bit 1
                self.code = (self.code << 1) | 1
                self.bits += 1
                print(f"[DEBUG] Bit {self.bits}: 1 (dt={dt})")
            else:
                print(f"[DEBUG] Invalid pulse: dt = {dt} µs → Reset")
                self.in_code = False
                self.bits = 0
                self.code = 0
                return

            if self.bits == 32:
                if self.code != 0xFFFFFFFF:
                    print(f">> Mã IR nhận được: 0x{self.code:08X}")
                else:
                    print("[DEBUG] Bỏ qua repeat code (0xFFFFFFFF)")
                self.in_code = False

def main():
    pi = pigpio.pi()
    if not pi.connected:
        print("⛔ Không kết nối được pigpiod. Chạy `sudo pigpiod` trước.")
        return

    pi.set_mode(IR_GPIO, pigpio.INPUT)
    pi.set_pull_up_down(IR_GPIO, pigpio.PUD_UP)

    print(f">> Đang lắng nghe tín hiệu IR trên GPIO {IR_GPIO}. Nhấn 1 nút bất kỳ...")
    listener = IR_NEC_Listener(pi, IR_GPIO)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n>> Thoát.")
    finally:
        pi.stop()

if __name__ == "__main__":
    main()
