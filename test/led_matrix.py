import board
import neopixel
import time

# ================================
# CẤU HÌNH MATRIX
# ================================
LED_PIN = board.D18          # Chỉ dùng được GPIO18
NUM_PIXELS = 64              # 8x8
BRIGHTNESS = 0.3

pixels = neopixel.NeoPixel(
    LED_PIN,
    NUM_PIXELS,
    brightness=BRIGHTNESS,
    auto_write=False,
    pixel_order=neopixel.GRB
)

# ================================
# WIRING ZIGZAG: TỌA ĐỘ → INDEX
# ================================
def xy_to_index(x, y):
    return y * 8 + x if y % 2 == 0 else y * 8 + (7 - x)

def set_pixel(x, y, color):
    i = xy_to_index(x, y)
    pixels[i] = color

def clear():
    pixels.fill((0, 0, 0))
    pixels.show()

# ================================
# HIỂN THỊ ẢNH 8x8 (TỪ uint64)
# ================================
def draw_bitmap(bits, fg=(255, 255, 255), bg=(0, 0, 0)):
    for y in range(8):
        for x in range(8):
            bit_index = y * 8 + x
            bit = (bits >> (63 - bit_index)) & 1
            color = fg if bit else bg
            set_pixel(x, y, color)
    pixels.show()

# ================================
# DANH SÁCH ICON DẠNG uint64
# ================================
IMAGES = [
    0x00183c7effffff66,  # Icon 1
    0x183c7effffff6600,  # Icon 2
]
IMAGES_LEN = len(IMAGES)

# ================================
# DEMO HIỂN THỊ TUẦN TỰ
# ================================
if __name__ == "__main__":
    try:
        while True:
            for img in IMAGES:
                draw_bitmap(img, fg=(255, 105, 180))  # Màu xanh lá
                time.sleep(0.5)
    except KeyboardInterrupt:
        clear()
