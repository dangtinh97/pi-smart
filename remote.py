# 0xF9FE4FCF on
# 0xF87CFFFC off

import pigpio
import time

GPIO_IR = 13  # chân GPIO nối IR LED

# NEC protocol parameters
CARRIER_FREQ = 38000  # 38kHz
DUTY_CYCLE = 0.33     # 33% typical

# Hàm tạo waveform dạng on-off (us)
def send_code(pi, gpio, waveform):
    pulses = []
    for i in range(len(waveform)):
        duration = waveform[i]
        if i % 2 == 0:
            pulses.append(pigpio.pulse(1 << gpio, 0, duration))
        else:
            pulses.append(pigpio.pulse(0, 1 << gpio, duration))

    pi.set_mode(gpio, pigpio.OUTPUT)
    pi.wave_add_new()
    pi.wave_add_generic(pulses)
    wave_id = pi.wave_create()
    if wave_id >= 0:
        pi.wave_send_once(wave_id)
        while pi.wave_tx_busy():
            time.sleep(0.01)
        pi.wave_delete(wave_id)

# Mã NEC ví dụ: 0x20DF10EF (VD: POWER của LG TV)
# Tạo waveform theo chuẩn NEC
def nec_encode(code):
    def burst(on, off):
        return [on, off]

    seq = []
    # Header
    seq += burst(9000, 4500)

    # 32 bits
    for i in range(32):
        bit = (code >> (31 - i)) & 1
        if bit == 1:
            seq += burst(560, 1690)
        else:
            seq += burst(560, 560)

    # Stop bit
    seq += burst(560, 0)
    return seq

# ----- GỬI -----
pi = pigpio.pi()
if not pi.connected:
    exit(1)

pi.set_PWM_frequency(GPIO_IR, CARRIER_FREQ)
pi.set_PWM_dutycycle(GPIO_IR, 128)  # dùng khi cần test PWM

code = 0x20DF10EF  # NEC mã POWER
waveform = nec_encode(code)
send_code(pi, GPIO_IR, waveform)

pi.stop()
