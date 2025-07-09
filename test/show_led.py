import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Thiết lập I2C
try:
    i2c = busio.I2C(board.SCL, board.SDA)
except Exception as e:
    print(f"Lỗi thiết lập I2C: {e}")
    exit()

# Khởi tạo màn hình OLED (128x64, địa chỉ I2C 0x3C)
try:
    oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)
    print("Khởi tạo OLED thành công")
except Exception as e:
    print(f"Lỗi khởi tạo OLED: {e}")
    print("Kiểm tra địa chỉ I2C bằng 'i2cdetect -y 1'")
    exit()

# Xóa màn hình
oled.fill(0)
oled.show()

# Tạo đối tượng hình ảnh
image = Image.new("1", (oled.width, oled.height))  # 1-bit (đen/trắng)
draw = ImageDraw.Draw(image)

# Tải font mặc định
try:
    font = ImageFont.load_default()
except Exception as e:
    print(f"Lỗi tải font: {e}")
    exit()

# Văn bản cần hiển thị
text = "IR Code: 02FD08F7"

# Vẽ văn bản
try:
    draw.text((0, 0), text, font=font, fill=255)  # fill=255 là màu trắng
    oled.image(image)
    oled.show()
    print("Hiển thị văn bản thành công")
except Exception as e:
    print(f"Lỗi hiển thị văn bản: {e}")

# Giữ màn hình
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Dừng hiển thị")
    oled.fill(0)
    oled.show()