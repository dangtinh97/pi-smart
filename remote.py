import pigpio
import time

GPIO_IR = 13  # ✅ Sửa từ 18 → 13

pi = pigpio.pi()
if not pi.connected:
    exit(1)

pi.set_mode(GPIO_IR, pigpio.OUTPUT)
pi.set_PWM_frequency(GPIO_IR, 38000)      # 38kHz carrier
pi.set_PWM_dutycycle(GPIO_IR, 128)        # Duty cycle ~50%

print("Đang gửi sóng IR...")
time.sleep(5)

pi.set_PWM_dutycycle(GPIO_IR, 0)
pi.stop()
