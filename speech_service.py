import speech_recognition as sr
import threading

class SpeechService:
    def __init__(self, wake_word="hello"):
        self.speech_recognizer = sr.Recognizer()
        self.wake_word = wake_word
        self.is_listening = False

    def listen_for_wake_word(self, callback):
        """Listens for a wake word to activate speech recognition."""
        def recognize():
            while True:
                try:
                    with sr.Microphone() as source:
                        print("Listening for wake word...")
                        audio = self.speech_recognizer.listen(source)
                        text = self.speech_recognizer.recognize_google(audio).lower()
                        print(f"Heard: {text}")

                        if self.wake_word in text:
                            print("Wake word detected! Listening for command...")
                            callback()
                            break  # Stop wake-word loop after activation
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    print("Speech recognition service error.")
                    break

        threading.Thread(target=recognize, daemon=True).start()

    def listen_for_command(self, callback):
        """Listens for voice commands after wake-word activation."""
        def recognize():
            try:
                with sr.Microphone() as source:
                    print("Listening for command...")
                    audio = self.speech_recognizer.listen(source)
                    command = self.speech_recognizer.recognize_google(audio)
                    print(f"Command recognized: {command}")
                    callback(command)
            except sr.UnknownValueError:
                print("Could not understand. Try again.")
            except sr.RequestError:
                print("Speech recognition service error.")

        threading.Thread(target=recognize, daemon=True).start()
