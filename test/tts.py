from gtts import gTTS
import os
from config import PATH_MPG123
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
    os.system(PATH_MPG123+" ./welcome.mp3")
    os.remove("./welcome.mp3")

play_voice("Xin xin")