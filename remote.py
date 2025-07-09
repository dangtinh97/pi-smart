import pigpio
import time

IR_GPIO = 13  # Chân GPIO hỗ trợ PWM (PIN 12 trên Pi)

pi = pigpio.pi()

def send_nec(code):
    marks = []
    # NEC header: 9ms mark + 4.5ms space
    marks += [1]*int(9000/26.3)
    marks += [0]*int(4500/26.3)

    # 32 bit data
    for i in range(32):
        bit = (code >> (31 - i)) & 1
        marks += [1]*int(560/26.3)
        if bit == 1:
            marks += [0]*int(1690/26.3)
        else:
            marks += [0]*int(560/26.3)

    # End pulse
    marks += [1]*int(560/26.3)

    # Build waveform
    wf = []
    for b in marks:
        if b == 1:
            wf.append(pigpio.pulse(1 << IR_GPIO, 0, 13))
            wf.append(pigpio.pulse(0, 1 << IR_GPIO, 13))
        else:
            wf.append(pigpio.pulse(0, 0, 560))  # space

    pi.wave_add_generic(wf)
    wid = pi.wave_create()

    # Send repeatedly for 5 seconds
    start_time = time.time()
    while time.time() - start_time < 5:
        pi.wave_send_once(wid)
        while pi.wave_tx_busy():
            time.sleep(0.01)
        # Mỗi mã NEC thường có delay giữa 2 lần phát (khoảng 110ms)
        time.sleep(0.11)

    pi.wave_delete(wid)

# Gửi mã "Power" của remote LG
send_nec(0x20DF10EF)
