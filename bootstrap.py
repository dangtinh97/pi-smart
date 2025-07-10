import threading
from core.event_bus import event_bus
from wakeword.porcupine_listener import wakeword_listener
from handlers.wakeword_handler import on_wakeword_detected
def start_system():
    print("🚀 Khởi động hệ thống")
    wakeword_listener.start()
    # threading.Thread(target=wakeword_listener.start, daemon=True).start()
    event_bus.on("wakeword.detected", lambda: on_wakeword_detected(wakeword_listener))
