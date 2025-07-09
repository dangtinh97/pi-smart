import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Thiết lập I2C
try:
    i2c = busio.I2C(board.SCL, board.SDA)
    print("I2C khởi tạo thành công")
except Exception as e:
    print(f"Lỗi khởi tạo I2C: {e}")
    print("Kiểm tra kết nối SDA (Pin 3), SCL (Pin 5), VCC, GND")
    exit()

# Thử cả hai kích thước màn hình và địa chỉ I2C
for addr in [0x3C, 0x3D]:
    for width, height in [(128, 64), (128, 32)]:
        print(f"Thử địa chỉ I2C 0x{addr:02X}, kích thước {width}x{height}...")
        try:
            # Khởi tạo OLED
            oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=addr)
            print(f"OLED khởi tạo thành công: 0x{addr:02X}, {width}x{height}")

            # Xóa màn hình
            oled.fill(0)
            oled.show()
            time.sleep(1)  # Đợi để kiểm tra màn hình đen

            # Tạo hình ảnh
            image = Image.new("1", (width, height))
            draw = ImageDraw.Draw(image)

            # Tải font mặc định
            try:
                font = ImageFont.load_default()
            except Exception as e:
                print(f"Lỗi tải font: {e}")
                continue

            # Vẽ văn bản kiểm tra
            text = "Test OLED"
            draw.text((0, 0), text, font=font, fill=255)

            # Hiển thị
            oled.image(image)
            oled.show()
            print(f"Hiển thị '{text}' trên màn hình {width}x{height}")

            # Chờ 5 giây để kiểm tra
            time.sleep(5)

            # Thử hiển thị toàn màn hình trắng
            oled.fill(1)
            oled.show()
            print("Hiển thị toàn màn hình trắng")
            time.sleep(2)

            # Xóa lại màn hình
            oled.fill(0)
            oled.show()
            print("Xóa màn hình")

            break  # Thoát nếu thành công
        except Exception as e:
            print(f"Lỗi với địa chỉ 0x{addr:02X}, kích thước {width}x{height}: {e}")
    else:
        continue
    break
else:
    print("Không thể khởi tạo OLED. Kiểm tra kết nối phần cứng hoặc địa chỉ I2C.")
    exit()

# Giữ màn hình hiển thị văn bản
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Dừng chương trình")
    oled.fill(0)
    oled.show()