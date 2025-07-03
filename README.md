# Pi Smart

## Install


## Project
```plaintext
pi-smart/
├── main.py                     # Entrypoint: chạy FastAPI + WebSocket
├── config.py                   # Cấu hình toàn hệ thống (GPIO, địa chỉ I2C...)
├── requirements.txt            # Thư viện cần cài
│
├── hardware/                   # Điều khiển phần cứng
│   ├── __init__.py
│   ├── ir.py                   # Gửi tín hiệu hồng ngoại
│   └── oled.py                 # Giao tiếp màn hình SSD1306 (I2C)
│
├── services/                   # Các chức năng logic bổ sung (optional)
│   └── status_manager.py       # Quản lý trạng thái thiết bị (đang nghe, đang gửi lệnh...)
│
├── ui/                         # Giao diện người dùng
│   ├── web/                    # Giao diện web truy cập
│   │   ├── static/             # JS, CSS, hình ảnh
│   │   └── index.html          # Giao diện chính
│   └── screen/                 # Giao diện hiển thị trên màn hình nhỏ (OLED)
│       ├── screen_manager.py   # Quản lý layout/hiển thị
│       └── screens/            # Các layout cụ thể (boot, idle, error...)
│           ├── boot.py
│           ├── idle.py
│           └── listening.py
│
├── api/                        # Các route FastAPI
│   ├── __init__.py
│   ├── ir.py                   # API điều khiển IR
│   ├── display.py              # API gửi text lên OLED
│   └── ws.py                   # WebSocket handler
│
├── data/                       # Dữ liệu runtime
│   ├── logs/                   # File log
│   ├── settings.json           # Cấu hình runtime
│   └── ir_codes.json           # Mã lệnh IR đã học

```