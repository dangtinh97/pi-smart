from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# Khởi tạo SH1106 I2C, rotate=2 (xoay ngược 180 độ nếu gắn lộn)
serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=2)

def show_text(text: str):
    # Tạo ảnh trắng đen
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    # Font mặc định
    font = ImageFont.load_default()

    # Ghi text (nhiều dòng nếu cần)
    lines = text.split('\n')
    for i, line in enumerate(lines):
        draw.text((0, i * 12), line, font=font, fill=255)

    # Hiển thị lên màn
    device.display(image)
