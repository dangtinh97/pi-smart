import pigpio
import time
import config_pinout

IR_GPIO = config_pinout.GPIO_IR_RECEIVER

class IR_DebugLogger:
    def __init__(self, pi, gpio):
        self.pi = pi
        self.gpio = gpio
        self.last_tick = 0
        self.pulses = []

        # Đăng ký callback bắt mọi cạnh (cả lên và xuống)
        self.cb = pi.callback(gpio, pigpio.EITHER_EDGE, self._cb)

    def _cb(self, gpio, level, tick):
        dt = pigpio.tickDiff(self.last_tick, tick)
        self.last_tick = tick
        self.pulses.append((level, dt))
        print(f"level={level}, dt={dt} µs")

    def stop(self):
        self.cb.cancel()

    def dump_summary(self):
        print("\n>> Tổng số xung nhận được:", len(self.pulses))
        if len(self.pulses) < 10:
            print("⚠️ Xung quá ít. Kiểm tra lại remote hoặc IR.")
            return

        print(">> 10 xung đầu:")
        for i in range(min(10, len(self.pulses))):
            lvl, dt = self.pulses[i]
            print(f"  [{i}] level={lvl}, dt={dt} µs")

        # Thử phát hiện header NEC
        for i in range(len(self.pulses)-1):
            lvl1, dt1 = self.pulses[i]
            lvl2, dt2 = self.pulses[i+1]
            if 8000 <= dt1 <= 10000 and 4000 <= dt2 <= 5000:
                print("\n✅ Phát hiện header NEC-like tại index", i)
                break
        else:
            print("\n⛔ Không phát hiện header NEC.")

def main():
    pi = pigpio.pi()
    if not pi.connected:
        print("⛔ Không kết nối được pigpiod. Chạy `sudo pigpiod` trước.")
        return

    pi.set_mode(IR_GPIO, pigpio.INPUT)
    pi.set_pull_up_down(IR_GPIO, pigpio.PUD_UP)

    logger = IR_DebugLogger(pi, IR_GPIO)

    print(f">> Đang ghi xung IR trên GPIO {IR_GPIO}. Bấm 1 nút remote...")
    time.sleep(5)

    logger.stop()
    logger.dump_summary()
    pi.stop()

if __name__ == "__main__":
    main()
