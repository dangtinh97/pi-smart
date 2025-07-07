import pigpio
import time
import config_pinout

IR_GPIO = config_pinout.GPIO_IR_RECEIVER

class NECDecoderPure:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self.last_tick = 0
        self.last_level = 1
        self.pulses = []
        self.in_frame = False
        self.frame_timeout = 0.12  # giây

        self.cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        dt = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick

        if not self.in_frame and level == 0:
            self.in_frame = True
            self.pulses = []
            return

        if self.in_frame:
            self.pulses.append(dt)

    def decode_nec(self, pulses):
        if len(pulses) < 66:
            print("[DEBUG] Không đủ pulse NEC")
            return None

        # Header
        if not (8500 <= pulses[0] <= 9500 and 4000 <= pulses[1] <= 5000):
            print("[DEBUG] Không phải header NEC hợp lệ")
            return None

        bits = []
        for i in range(2, 66, 2):  # từng cặp (mark, space)
            mark = pulses[i]
            space = pulses[i + 1]

            if 400 <= mark <= 700:
                if 400 <= space <= 700:
                    bits.append(0)
                elif 1500 <= space <= 2500:
                    bits.append(1)
                else:
                    print(f"[DEBUG] space lạ: {space} µs")
                    return None
            else:
                print(f"[DEBUG] mark lạ: {mark} µs")
                return None

        if len(bits) != 32:
            print("[DEBUG] Không đủ 32 bit")
            return None

        code = 0
        for b in bits:
            code = (code << 1) | b

        return code

    def listen_and_decode(self):
        try:
            while True:
                time.sleep(self.frame_timeout)
                if self.in_frame and len(self.pulses) > 10:
                    print(f"[DEBUG] Pulses thu được: {len(self.pulses)}")
                    code = self.decode_nec(self.pulses)
                    if code:
                        print(f">> Mã IR: 0x{code:08X}")
                    self.pulses = []
                    self.in_frame = False
        except KeyboardInterrupt:
            print(">> Thoát.")
        finally:
            self.cb.cancel()

def main():
    pi = pigpio.pi()
    if not pi.connected:
        print("⛔ Chạy `sudo pigpiod` trước khi chạy script.")
        return

    pi.set_mode(IR_GPIO, pigpio.INPUT)
    pi.set_pull_up_down(IR_GPIO, pigpio.PUD_UP)

    print(f">> Lắng nghe IR NEC trên GPIO {IR_GPIO}...")

    decoder = NECDecoderPure(pi, IR_GPIO)
    decoder.listen_and_decode()

    pi.stop()

if __name__ == "__main__":
    main()
