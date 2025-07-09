import board
import busio
from adafruit_ssd1306 import SSD1306_I2C
from PIL import Image, ImageDraw, ImageFont

# Khởi tạo I2C + OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)

# Hàm hiển thị nội dung
def show_text(text):
    oled.fill(0)  # clear screen
    oled.show()

    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    draw.text((0, 0), text, font=font, fill=255)

    oled.image(image)
    oled.show()
