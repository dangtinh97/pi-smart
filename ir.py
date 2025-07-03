import pigpio
import time
import config_pinout
IR_GPIO = config_pinout.GPIO_IR_RECEIVER  # chân OUT của IR nối với GPIO17

class IR_Recorder:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self.code = 0
        self.bits = 0
        self.last_tick = 0
        self.in_code = False

        # Bắt cạnh xuống (FALLING)
        self.cb = pi.callback(gpio, pigpio.FALLING_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        dt = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick

        # Bắt đầu chuỗi mới nếu thấy header NEC (~9ms)
        if 8500 <= dt <= 9500:
            self.in_code = True
            self.code = 0
            self.bits = 0
            return

        if self.in_code:
            # Bit 0: ~560us
            # Bit 1: ~1680us
            if 400 <= dt <= 700:
                self.code = (self.code << 1) | 0
                self.bits += 1
            elif 1500 <= dt <= 1800:
                self.code = (self.code << 1) | 1
                self.bits += 1

            if self.bits == 32:
                print(f">> Mã IR nhận được: 0x{self.code:08X}")
                self.in_code = False

pi = pigpio.pi()
if not pi.connected:
    print("Không kết nối được với pigpiod. Chạy `sudo pigpiod` trước.")
    exit()

pi.set_mode(IR_GPIO, pigpio.INPUT)
pi.set_pull_up_down(IR_GPIO, pigpio.PUD_UP)

decoder = IR_Recorder(pi, IR_GPIO)

print(">> Đang lắng nghe mã IR... Nhấn nút remote (Ctrl+C để thoát).")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n>> Thoát.")
finally:
    pi.stop()
