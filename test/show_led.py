from luma.core.interface.serial import i2c
from luma.core.render import canvas
from luma.oled.device import ssd1306
import time

# Thử các cấu hình
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
        serial = i2c(port=1, address=addr)
        device = ssd1306(serial, width=width, height=height)
        print(f"Khởi tạo OLED thành công: 0x{addr:02X}, {width}x{height}")
        break
    except Exception as e:
        print(f"Lỗi với địa chỉ 0x{addr:02X}, kích thước {width}x{height}: {e}")
        continue

if device is None:
    print("Không thể khởi tạo OLED. Kiểm tra kết nối I2C bằng 'i2cdetect -y 1'.")
    exit()

try:
    # Bước 1: Hiển thị toàn màn hình đen
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="black")
    print("Hiển thị toàn màn hình đen")
    time.sleep(3)

    # Bước 2: Hiển thị toàn màn hình trắng
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="white")
    print("Hiển thị toàn màn hình trắng")
    time.sleep(3)

    # Bước 3: Hiển thị văn bản ở các vị trí khác nhau
    for y_offset in [0, 8, 16, 24]:  # Thử các vị trí để tránh đường đen
        with canvas(device) as draw:
            draw.rectangle(device.bounding_box, fill="black")  # Xóa màn hình
            draw.text((0, y_offset), "Test OLED", fill="white")
            draw.text((0, y_offset + 16), "IR Code: 02FD08F7", fill="white")
        print(f"Hiển thị văn bản tại y={y_offset}: Test OLED, IR Code: 02FD08F7")
        time.sleep(3)

except KeyboardInterrupt:
    print("Dừng chương trình")
    with canvas(device) as draw:
        draw.rectangle(device.bounding_box, fill="black")
except Exception as e:
    print(f"Lỗi hiển thị: {e}")