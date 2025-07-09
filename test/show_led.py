import board
import busio
import adafruit_ssd1306
from PIL import Image, ImageDraw, ImageFont
import time

# Thiết lập I2C
i2c = busio.I2C(board.SCL, board.SDA)

# Khởi tạo màn hình OLED (128x64, địa chỉ I2C 0x3C)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C)

# Xóa màn hình
oled.fill(0)
oled.show()

# Tạo đối tượng hình ảnh để vẽ
image = Image.new("1", (oled.width, oled.height))  # Chế độ 1-bit (đen/trắng)
draw = ImageDraw.Draw(image)

# Tải font mặc định (hoặc font tùy chỉnh)
font = ImageFont.load_default()

# Văn bản cần hiển thị (mã IR từ yêu cầu trước)
text = "IR Code: 020208F7"

# Vẽ văn bản lên hình ảnh
draw.text((0, 0), text, font=font, fill=255)  # fill=255 là màu trắng

# Hiển thị hình ảnh lên màn hình
oled.image(image)
oled.show()

# Giữ màn hình hiển thị
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Dừng hiển thị")
    oled.fill(0)  # Xóa màn hình khi thoát
    oled.show()