from PIL import Image, ImageDraw, ImageFont
import board, busio
from adafruit_ssd1306 import SSD1306_I2C

# Tạo kết nối I2C và màn hình
i2c = busio.I2C(board.SCL, board.SDA)
oled = SSD1306_I2C(128, 64, i2c)

# Xoá màn hình
oled.fill(0)
oled.show()

# Tạo khung vẽ ảnh trắng đen
image = Image.new("1", (oled.width, oled.height))
draw = ImageDraw.Draw(image)

# Load font mặc định hoặc font TrueType
font = ImageFont.load_default()
# font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 14)

# Ghi nội dung
draw.text((0, 0), "Xin chao Dai ca!", font=font, fill=255)
draw.text((0, 20), "Man OLED 128x64", font=font, fill=255)
draw.text((0, 40), "Sang & Rach net", font=font, fill=255)

# Hiển thị lên màn hình
oled.image(image)
oled.show()
