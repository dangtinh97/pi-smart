import pygame

def play_audio_mp3(path="data/sound.mp3"):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
    except Exception as e:
        logger.error(f"🔊 Lỗi khi phát bằng pygame: {e}")
    finally:
        pygame.mixer.quit()
