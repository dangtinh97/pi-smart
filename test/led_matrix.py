import board
import neopixel
import time

# Matrix 8x8 dùng 64 LED
pixel_pin = board.D18  # GPIO18
num_pixels = 64

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False, pixel_order=neopixel.GRB)

def xy_to_index(x, y):
    """Chuyển (x, y) sang chỉ số 1 chiều"""
    if y % 2 == 0:
        return y * 8 + x
    else:
        return y * 8 + (7 - x)  # Zigzag wiring

def set_pixel(x, y, color):
    i = xy_to_index(x, y)
    pixels[i] = color

# Hiển thị chéo màu đỏ
for i in range(8):
    set_pixel(i, i, (255, 0, 0))
pixels.show()
