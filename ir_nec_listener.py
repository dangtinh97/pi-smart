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
            pulses = decoder.read_pulses(ir_receiver, blocking=True, pulse_window=0.5, max_pulse=10000)
            print(f"Xung nhận được: {pulses}")

            # Kiểm tra xem chuỗi có phải là tín hiệu lặp
            if len(pulses) == 2 and pulses[0] > 8000 and pulses[1] < 3000:
                print("Tín hiệu lặp (repeat code)")
                continue

            try:
                # Giải mã tín hiệu
                code = decoder.decode_bits(pulses, debug=False)
                if len(code) == 4:  # NEC có 4 byte
                    hex_code = ''.join([f"{x:02X}" for x in code])
                    print(f"Mã nhận được: {hex_code}")
                else:
                    print("Dữ liệu không đúng định dạng NEC (không đủ 4 byte)")
            except adafruit_irremote.IRNECRepeatException:
                print("Tín hiệu lặp (repeat code)")
            except adafruit_irremote.IRDecodeException as e:
                print(f"Lỗi giải mã tín hiệu: {e}")
                print("Thử phân tích thủ công...")
                # Phân tích thủ công
                if len(pulses) >= 34:  # Header + 32 bit
                    bits = []
                    for i in range(2, len(pulses), 2):  # Bỏ header
                        if i + 1 < len(pulses):
                            space = pulses[i + 1]
                            bit = 1 if space > 1000 else 0
                            bits.append(bit)
                        if len(bits) == 32:
                            break
                    if len(bits) == 32:
                        address = int(''.join(map(str, bits[:8])), 2)
                        address_inv = int(''.join(map(str, bits[8:16])), 2)
                        command = int(''.join(map(str, bits[16:24])), 2)
                        command_inv = int(''.join(map(str, bits[24:32])), 2)
                        print(f"Địa chỉ: {hex(address)}, Lệnh: {hex(command)}")
        except Exception as e:
            print(f"Lỗi chung: {e}")
        time.sleep(0.1)
except KeyboardInterrupt:
    ir_receiver.deinit()
    print("Dừng chương trình")