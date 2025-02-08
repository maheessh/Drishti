import speech_recognition as sr
import time
import threading

class SpeechService:
    def __init__(self, wake_word_callback):
        self.speech_recognizer = sr.Recognizer()
        self.wake_word_callback = wake_word_callback
        self.wake_word = "hello"

        # ✅ Start Wake Word Detection in a Separate Thread
        threading.Thread(target=self.listen_for_wake_word, daemon=True).start()

    def listen_for_wake_word(self):
        while True:
            try:
                with sr.Microphone() as source:
                    print("Listening for wake word...")
                    audio = self.speech_recognizer.listen(source)
                    text = self.speech_recognizer.recognize_google(audio).lower()
                    print(f"Heard: {text}")

                    if self.wake_word in text:
                        print("Wake word detected! Responding...")
                        self.wake_word_callback()

                        # ✅ Give time to speak, then restart wake word detection
                        time.sleep(3)  # Prevents immediate retriggering
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                print("Speech recognition service error.")
                break

            time.sleep(1)  # ✅ Restart wake word detection after a short pause
