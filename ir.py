import pigpio
import time

import config_pinout

def cbf(gpio, level, tick):
    print(">> Có xung IR - level:", level, "tick:", tick)

pi = pigpio.pi()
pi.set_mode(config_pinout.GPIO_IR_RECEIVER, pigpio.INPUT)

cb = pi.callback(config_pinout.GPIO_IR_RECEIVER, pigpio.FALLING_EDGE, cbf)

print("Đang đọc xung IR... Nhấn nút trên remote.")
time.sleep(5)

cb.cancel()
pi.stop()