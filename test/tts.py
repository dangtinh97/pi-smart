from gtts import gTTS
import os

import pyaudio
def play_voice(mytext):

    # Language for the speech
    language = 'vi'

    # Create a gTTS object
    myobj = gTTS(text=mytext, lang=language, slow=False)

    # Save the converted audio to an MP3 file
    myobj.save("./welcome.mp3")

    # Optionally, play the audio file (requires an audio player)
    # os.system("start welcome.mp3") # For Windows
    # os.system("mpg321 welcome.mp3") # For Linux
    os.system("/usr/bin/mpg123 ./welcome.mp3")
    os.remove("./welcome.mp3")



def startMic():
    pa = pyaudio.PyAudio()

    stream = pa.open(
        rate=16000,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=1024,
    )
play_voice("Xin xin")
startMic()