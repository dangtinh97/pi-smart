import pigpio
import time

pi = pigpio.pi()
pi.set_mode(13, pigpio.OUTPUT)
pi.set_PWM_frequency(13, 38000)
pi.set_PWM_dutycycle(13, 128)

print("PWM đang phát 38kHz trên GPIO13 (5 giây)...")
time.sleep(5)

pi.set_PWM_dutycycle(13, 0)
pi.stop()
