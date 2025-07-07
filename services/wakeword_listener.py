def restart_wakeword_listener(listener):
    import threading
    import time

    def restart():
        print("🛑 Dừng wakeword listener...")
        listener.running = False
        if listener.thread and listener.thread.is_alive():
            listener.thread.join()
        if listener.stream:
            listener.stream.stop_stream()
            listener.stream.close()
            listener.stream = None

        # Không terminate PyAudio để giữ device ổn định
        time.sleep(5)  # delay đủ lâu cho ALSA xử lý

        print("▶️ Mở lại stream wakeword listener...")
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