import pyttsx3

class TextToSpeechService:
    def __init__(self):
        self.speaker = pyttsx3.init()

    def speak(self, text):
        self.speaker.say(text)
        self.speaker.runAndWait()
