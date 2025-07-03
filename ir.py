import pigpio
import time
import config_pinout
IR_PIN = config_pinout.GPIO_IR_RECEIVER  # GPIO nhận tín hiệu IR

class NECDecoder:
    def __init__(self, pi, gpio_pin):
        self.pi = pi
        self.gpio = gpio_pin
        self.cb = self.pi.callback(self.gpio, pigpio.EITHER_EDGE, self._cb)
        self.in_code = False
        self.last_tick = 0
        self.code = 0
        self.bits = 0

    def _cb(self, gpio, level, tick):
        if level == pigpio.TIMEOUT:
            if self.in_code and self.bits >= 32:
                print(f">> Mã IR: 0x{self.code:08X}")
            self.in_code = False
            self.bits = 0
            self.code = 0
            return

        time_diff = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick

        if level == 1:
            if 8000 <= time_diff <= 10000:
                self.in_code = True
                self.bits = 0
                self.code = 0
                self.pi.set_watchdog(self.gpio, 50)  # 50ms watchdog
        elif level == 0 and self.in_code:
            if 400 <= time_diff <= 700:
                self.code = (self.code << 1) | 0
                self.bits += 1
            elif 1400 <= time_diff <= 1800:
                self.code = (self.code << 1) | 1
                self.bits += 1

            if self.bits >= 32:
                self.pi.set_watchdog(self.gpio, 0)

pi = pigpio.pi()
if not pi.connected:
    print("Không kết nối được pigpio daemon.")
    exit()

pi.set_mode(IR_PIN, pigpio.INPUT)
pi.set_pull_up_down(IR_PIN, pigpio.PUD_UP)

decoder = NECDecoder(pi, IR_PIN)

print(">> Đang chờ tín hiệu IR (ấn nút trên remote)... Ctrl+C để thoát.")
try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\n>> Thoát.")
finally:
    pi.stop()
