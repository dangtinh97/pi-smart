import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Tạo I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Khởi tạo OLED 128x64
oled = SSD1306_I2C(128, 64, i2c)

# Xoá màn hình
oled.fill(0)
oled.show()

# Tạo ảnh đen trắng
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Font mặc định
font = ImageFont.load_default()

# Ghi nội dung
draw.text((0, 0), "OLED 128x64", font=font, fill=255)
draw.text((0, 20), "Dia chi I2C: 0x3C", font=font, fill=255)
draw.text((0, 40), "Chao Dai ca!", font=font, fill=255)

# Gửi ảnh lên màn
oled.image(image)
oled.show()
