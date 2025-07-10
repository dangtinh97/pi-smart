import board
import neopixel
import time

# ================================
# CẤU HÌNH MATRIX
# ================================
LED_PIN = board.D18          # Chỉ dùng được GPIO18
NUM_PIXELS = 64              # 8x8
BRIGHTNESS = 0.05

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
    #0x183c7effffff6600,  # Icon 2
]
IMAGES_LEN = len(IMAGES)

# ================================
# DEMO HIỂN THỊ TUẦN TỰ
# ================================

COLOR_PALETTE = [
    (255, 0, 0),       # Đỏ tươi
    (255, 105, 180),   # Hồng (Hot Pink)
    (255, 165, 0),     # Cam (Orange)
    (255, 255, 0),     # Vàng
    (0, 255, 0),       # Xanh lá
    (0, 255, 255),     # Cyan
    (0, 0, 255),       # Xanh dương
    (138, 43, 226),    # Tím (BlueViolet)
    (255, 0, 255),     # Magenta
    (255, 255, 255),   # Trắng
]
def lerp_color(c1, c2, t):
    """Nội suy màu giữa c1 và c2 với t từ 0.0 đến 1.0"""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def fade_between_colors(img, c1, c2, steps=10, delay=0.05):
    """Hiệu ứng chuyển từ màu c1 sang c2 trên ảnh img"""
    for i in range(steps + 1):
        t = i / steps
        color = lerp_color(c1, c2, t)
        draw_bitmap(img, fg=color)
        time.sleep(delay)

def show_led_matrix():
    while True:
        for i in range(len(COLOR_PALETTE)):
            c1 = COLOR_PALETTE[i]
            c2 = COLOR_PALETTE[(i + 1) % len(COLOR_PALETTE)]
            for img in IMAGES:
                fade_between_colors(img, c1, c2, steps=10, delay=0.03)
