import pyttsx3

class TextToSpeechService:
    def __init__(self):
        self.speaker = pyttsx3.init()

    def speak(self, text):
        """Speaks out the given text using TTS."""
        self.speaker.say(text)
        self.speaker.runAndWait()
