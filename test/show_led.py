from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# Thử các cấu hình: địa chỉ I2C và kích thước màn hình
configs = [
    (0x3C, 128, 64),
    (0x3C, 128, 32),
    (0x3D, 128, 64),
    (0x3D, 128, 32)
]

device = None
for addr, width, height in configs:
    print(f"Thử địa chỉ I2C 0x{addr:02X}, kích thước {width}x{height}...")
    try:
        # Khởi tạo giao diện I2C và thiết bị SSD1306
        serial = i2c(port=1, address=addr)
        device = ssd1306(serial, width=width, height=height)
        print(f"Khởi tạo OLED thành công: 0x{addr:02X}, {width}x{height}")
        break
    except Exception as e:
        print(f"Lỗi với địa chỉ 0x{addr:02X}, kích thước {width}x{height}: {e}")
        continue

if device is None:
    print("Không thể khởi tạo OLED. Kiểm tra kết nối I2C hoặc địa chỉ bằng 'i2cdetect -y 1'.")
    exit()

try:
    # Xóa màn hình (toàn đen)
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="black")
    print("Xóa màn hình (toàn đen)")
    time.sleep(2)

    # Thử hiển thị toàn màn hình trắng
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="white")
    print("Hiển thị toàn màn hình trắng")
    time.sleep(2)

    # Xóa lại màn hình
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="black")
    print("Xóa màn hình")

    # Hiển thị văn bản kiểm tra
    while True:
        with canvas(device) as draw:
            draw.text((0, 0), "Test OLED", fill="white")
            draw.text((0, 16), "IR Code:", fill="white")
            draw.text((0, 32), "02FD08F7", fill="white")
        print("Hiển thị văn bản: Test OLED, IR Code: 02FD08F7")
        time.sleep(1)
except KeyboardInterrupt:
    print("Dừng chương trình")
    # Xóa màn hình khi thoát
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="black")
except Exception as e:
    print(f"Lỗi hiển thị: {e}")