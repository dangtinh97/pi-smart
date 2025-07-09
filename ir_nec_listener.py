import board
import adafruit_irremote
import pulseio
import time

# Thiết lập GPIO 26
IR_PIN = board.D26  # GPIO 26

# Khởi tạo PulseIn với tham số tối ưu
ir_receiver = pulseio.PulseIn(IR_PIN, maxlen=200, idle_state=True)

# Khởi tạo đối tượng giải mã
decoder = adafruit_irremote.GenericDecode()

print("Đang chờ tín hiệu hồng ngoại...")

try:
    while True:
        try:
            # Đọc các xung với thời gian chờ dài hơn
            pulses = decoder.read_pulses(ir_receiver, blocking=True, pulse_window=0.5)
            print(f"Xung nhận được: {pulses}")  # In xung để kiểm tra
            try:
                # Giải mã tín hiệu
                code = decoder.decode_bits(pulses)
                hex_code = ''.join([f"{x:02X}" for x in code])
                print(f"Mã nhận được: {hex_code}")
            except adafruit_irremote.IRNECRepeatException:
                print("Tín hiệu lặp (repeat code)")
            except adafruit_irremote.IRDecodeException as e:
                print(f"Lỗi giải mã tín hiệu: {e}")
        except Exception as e:
            print(f"Lỗi chung: {e}")
        time.sleep(0.1)
except KeyboardInterrupt:
    ir_receiver.deinit()
    print("Dừng chương trình")