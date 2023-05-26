from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play

def text_to_speech(text):
    speech = gTTS(text=text, lang="en")

    temp_file = "temp.mp3"
    speech.save(temp_file)

    audio = AudioSegment.from_file(temp_file, format="mp3")

    play(audio)