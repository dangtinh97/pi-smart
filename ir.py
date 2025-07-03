import pigpio
import config_pinout
import time

IR_GPIO = config_pinout.GPIO_IR_RECEIVER

class IR_Recorder:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self.code = 0
        self.bits = 0
        self.last_tick = 0
        self.in_code = False

        self.cb = pi.callback(gpio, pigpio.FALLING_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        dt = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick

        # print(f"[DEBUG] dt={dt} μs")  # ← in thời gian giữa các xung

        if 8500 <= dt <= 9500:  # Header ~9ms
            print("[DEBUG] Header detected")
            self.in_code = True
            self.code = 0
            self.bits = 0
            return

        if self.in_code:
            if 400 <= dt <= 700:  # bit 0
                self.code = (self.code << 1) | 0
                self.bits += 1
            elif 1500 <= dt <= 1800:  # bit 1
                self.code = (self.code << 1) | 1
                self.bits += 1
            else:
                print(f"[DEBUG] Invalid pulse: {dt} μs → reset")
                self.in_code = False
                self.bits = 0
                self.code = 0

            if self.bits == 32:
                print(f">> Mã IR: 0x{self.code:08X}")
                self.in_code = False
pi = pigpio.pi()
if not pi.connected:
    print("Không kết nối được pigpiod.")
    exit()

pi.set_mode(IR_GPIO, pigpio.INPUT)
pi.set_pull_up_down(IR_GPIO, pigpio.PUD_UP)

decoder = IR_Recorder(pi, IR_GPIO)

print(">> Đang lắng nghe tín hiệu IR (bấm remote)...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n>> Thoát.")
finally:
    pi.stop()
