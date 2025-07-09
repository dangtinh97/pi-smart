import pigpio
import time

# Thiết lập GPIO
IR_TX_PIN = 13  # GPIO 26
CARRIER_FREQ = 38000  # 38kHz

# Kết nối với pigpiod
pi = pigpio.pi()
if not pi.connected:
    print("Không thể kết nối với pigpiod. Đảm bảo pigpiod đang chạy!")
    exit()

# Thiết lập chân GPIO làm đầu ra
pi.set_mode(IR_TX_PIN, pigpio.OUTPUT)


# Hàm tạo sóng carrier 38kHz
def send_carrier(duration_us):
    # Tạo sóng PWM 38kHz trong khoảng thời gian duration_us
    pi.hardware_PWM(IR_TX_PIN, CARRIER_FREQ, 500000)  # 50% duty cycle
    time.sleep(duration_us / 1000000.0)
    pi.hardware_PWM(IR_TX_PIN, 0, 0)  # Tắt PWM


# Hàm gửi tín hiệu NEC
def send_nec_code(address, command):
    # Header: 9ms bật + 4.5ms tắt
    send_carrier(9000)
    time.sleep(0.0045)

    # Gửi 32 bit (address + ~address + command + ~command)
    data = (address << 24) | ((255 - address) << 16) | (command << 8) | (255 - command)
    for i in range(31, -1, -1):  # Gửi từ bit cao xuống thấp
        bit = (data >> i) & 1
        send_carrier(560)  # Xung 560µs
        time.sleep(0.00168 if bit else 0.00056)  # Logic 1: 1680µs, Logic 0: 560µs

    # Kết thúc bằng xung 560µs
    send_carrier(560)


# Hàm gửi tín hiệu lặp (repeat code)
def send_repeat_code():
    send_carrier(9000)
    time.sleep(0.00225)
    send_carrier(560)
    time.sleep(0.108 - 0.009 - 0.00225 - 0.00056)  # Khoảng cách 108ms giữa các repeat code

# Địa chỉ: 0xc1, Lệnh: 0xe0
try:
    print("Bắt đầu phát tín hiệu IR liên tục...")
    # Gửi mã NEC ban đầu (ví dụ: address=0xC1, command=0x00)
    send_nec_code(0xC1, 0xE0)
    time.sleep(0.108)  # Khoảng cách 108ms

    # Lặp lại tín hiệu lặp (repeat code) liên tục
    while True:
        send_repeat_code()
except KeyboardInterrupt:
    print("Dừng phát tín hiệu")
    pi.hardware_PWM(IR_TX_PIN, 0, 0)  # Tắt PWM
    pi.stop()