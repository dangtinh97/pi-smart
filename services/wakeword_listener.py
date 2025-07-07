def restart_wakeword_listener(listener):
    import threading
    import time
    import pyaudio
    import os

    def restart():
        print("🛑 Dừng wakeword listener...")
        listener.running = False
        if listener.thread and listener.thread.is_alive():
            listener.thread.join()
        if listener.stream:
            listener.stream.stop_stream()
            listener.stream.close()
            listener.stream = None
        listener.pa.terminate()

        print("🔄 Reset ALSA...")
        os.system("sudo alsa force-reload")
        time.sleep(4)  # Tăng thời gian chờ để ALSA ổn định

        print("▶️ Khởi động lại wakeword listener...")
        listener.pa = pyaudio.PyAudio()
        try:
            listener.stream = listener.pa.open(
                input_device_index=listener.indexAudio,
                rate=listener.porcupine.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=listener.porcupine.frame_length,
            )
        except Exception as e:
            print(f"❌ Không mở được stream: {e}")
            return
        listener.running = True
        listener.thread = threading.Thread(target=listener._run, daemon=True)
        listener.thread.start()
        print("🎧 WakewordListener đã restart thành công.")

    threading.Thread(target=restart).start()