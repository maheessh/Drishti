import pyttsx3

class TextToSpeechService:
    def __init__(self):
        self.speaker = pyttsx3.init()
        self.speaker.setProperty("rate", 150)  # Adjust speed
        self.speaker.setProperty("volume", 1.0)

    def speak(self, text):
        """Speak the given text."""
        self.speaker.say(text)
        self.speaker.runAndWait()
