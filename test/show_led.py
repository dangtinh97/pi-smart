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
    exit()

# Thử cả hai kích thước màn hình: 128x64 và 128x32
for width, height in [(128, 64), (128, 32)]:
    print(f"Thử kích thước {width}x{height}...")
    try:
        # Khởi tạo OLED
        oled = adafruit_ssd1306.SSD1306_I2C(width, height, i2c, addr=0x3C)
        print(f"OLED {width}x{height} khởi tạo thành công")

        # Xóa màn hình
        oled.fill(0)
        oled.show()

        # Tạo hình ảnh
        image = Image.new("1", (oled.width, oled.height))
        draw = ImageDraw.Draw(image)

        # Tải font mặc định
        try:
            font = ImageFont.load_default()
        except Exception as e:
            print(f"Lỗi tải font: {e}")
            exit()

        # Vẽ văn bản kiểm tra
        text = "Test OLED"
        draw.text((0, 0), text, font=font, fill=255)

        # Hiển thị
        oled.image(image)
        oled.show()
        print(f"Hiển thị văn bản '{text}' trên màn hình {width}x{height}")

        # Chờ 5 giây để kiểm tra
        time.sleep(5)

        # Xóa màn hình
        oled.fill(0)
        oled.show()
        break  # Thoát nếu thành công
    except Exception as e:
        print(f"Lỗi với kích thước {width}x{height}: {e}")
        if height == 32:  # Nếu cả hai kích thước đều lỗi
            print("Kiểm tra địa chỉ I2C bằng 'i2cdetect -y 1' hoặc kết nối phần cứng")
            exit()

# Giữ màn hình
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Dừng chương trình")
    oled.fill(0)
    oled.show()