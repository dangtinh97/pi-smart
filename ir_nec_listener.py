import board
import pulseio
import adafruit_irremote

IR_PIN = board.D26  # GPIO 26
ir_receiver = pulseio.PulseIn(IR_PIN, maxlen=120, idle_state=True)
decoder = adafruit_irremote.GenericDecode()

while True:
    pulses = decoder.read_pulses(ir_receiver)
    try:
        code = decoder.decode_bits(pulses)
        hex_code = ''.join([f"{x:02X}" for x in code])
        print(f"Mã nhận được: {hex_code}")
    except adafruit_irremote.IRNECRepeatException:
        pass  # Bỏ qua tín hiệu lặp
    except adafruit_irremote.IRDecodeException:
        print("Lỗi giải mã")