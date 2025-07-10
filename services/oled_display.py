from luma.core.interface.serial import i2c
from luma.oled.device import sh1106
from PIL import Image, ImageDraw, ImageFont

# Khởi tạo SH1106 I2C, rotate=2 (xoay ngược 180 độ nếu gắn lộn)
serial = i2c(port=1, address=0x3C)
device = sh1106(serial, rotate=2)

image = Image.new("1", (device.width, device.height))
draw = ImageDraw.Draw(image)
font = ImageFont.load_default()
lineText=0
def show_text(text: str):
    # Tạo ảnh trắng đen
    global lineText, draw, font, image
    lines = text.split('\n')
    for line in lines:
        if (lineText + 1) * 12 > device.height:
            image = Image.new("1", (device.width, device.height))
            draw = ImageDraw.Draw(image)
            lineText = 0
        draw.text((0, lineText * 12), line, font=font, fill=255)
        lineText += 1
    device.display(image)

def clear_text():
    global lineText, draw, font, image
    image = Image.new("1", (device.width, device.height))
    device.display(image)
    lineText = 0