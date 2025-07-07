import pvporcupine
import pyaudio
porcupine = pvporcupine.create(
            access_key="I2FzB0ROEKTLiBLnLa8jByF9b7wu+o6h4Z9PvWFKRwTpmZ9gmBpeaw==",
            keyword_paths=["data/hotwords/raspberry.ppn"]
        )
# pa = pyaudio.PyAudio()
# stream = pa.open(
#     rate=porcupine.sample_rate,
#     channels=1,
#     format=pyaudio.paInt16,
#     input=True,
#     frames_per_buffer=porcupine.frame_length,
#     input_device_index=1
# )