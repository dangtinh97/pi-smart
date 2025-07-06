from collections import defaultdict
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self.listeners: Dict[str, List[Callable]] = defaultdict(list)

    def on(self, event_name: str, handler: Callable):
        """
        Đăng ký một handler (hàm callback) cho event.
        """
        self.listeners[event_name].append(handler)

    def emit(self, event_name: str, *args, **kwargs):
        """
        Kích hoạt tất cả handler đã đăng ký cho event.
        """
        for handler in self.listeners.get(event_name, []):
            try:
                handler(*args, **kwargs)
            except Exception as e:
                print(f"[ERROR][event_bus] Handler lỗi: {e}")

# Global event_bus có thể import ở mọi module
event_bus = EventBus()
