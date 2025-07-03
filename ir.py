import pigpio
import time
import config_pinout

IR_GPIO = config_pinout.GPIO_IR_RECEIVER

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

        if 8000 <= dt <= 10000:  # Header ~9ms
            self.in_code = True
            self.bits = 0
            self.code = 0
            return

        if self.in_code:
            if 200 <= dt <= 900:         # Bit 0
                self.code = (self.code << 1) | 0
                self.bits += 1
            elif 1000 <= dt <= 2500:     # Bit 1
                self.code = (self.code << 1) | 1
                self.bits += 1
            else:
                # Xung lỗi, reset chuỗi
                self.in_code = False
                self.bits = 0
                self.code = 0
                return

            if self.bits == 32:
                print(f">> Mã IR nhận được: 0x{self.code:08X}")
                self.in_code = False

def main():
    pi = pigpio.pi()
    if not pi.connected:
        print("⛔ Không kết nối được pigpiod. Chạy `sudo pigpiod` trước.")
        return

    pi.set_mode(IR_GPIO, pigpio.INPUT)
    pi.set_pull_up_down(IR_GPIO, pigpio.PUD_UP)

    print(f">> Đang lắng nghe tín hiệu IR trên GPIO {IR_GPIO}. Bấm nút trên remote...")
    listener = IR_NEC_Listener(pi, IR_GPIO)

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n>> Dừng.")
    finally:
        pi.stop()

if __name__ == "__main__":
    main()
