import pigpio
import time

pi = pigpio.pi()
PIN_IR=26
pi.set_mode(PIN_IR, pigpio.OUTPUT)
pi.set_PWM_frequency(PIN_IR, 38000)
pi.set_PWM_dutycycle(PIN_IR, 128)

print("PWM đang phát 38kHz trên GPIO13 (5 giây)...")
time.sleep(5)

pi.set_PWM_dutycycle(13, 0)
pi.stop()
