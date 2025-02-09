import cv2
import torch
import easyocr
import pyttsx3
import threading
import time

class ObjectDetector:
    def __init__(self, update_ui_callback=None, shared_cap=None):
        """Initialize object detection and text-to-speech."""
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)  # Adjust speech speed

        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)  # YOLOv5 model
        self.reader = easyocr.Reader(['en'])  # OCR reader for text detection

        self.update_ui_callback = update_ui_callback  # Callback to update UI

        # ✅ Use shared camera from UI if available, otherwise open a new one
        self.cap = shared_cap if shared_cap else cv2.VideoCapture(0)
        self.running = True  # Flag to control detection loop

    def speak(self, text):
        """Convert text to speech asynchronously."""
        threading.Thread(target=lambda: self._speak(text), daemon=True).start()

    def _speak(self, text):
        """Speak text."""
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def detect_objects(self):
        """Detect objects continuously and speak detected items every 8 seconds."""
        def run_detection():
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    print("[ERROR] Couldn't read frame from webcam!")
                    break

                # Run YOLO object detection
                results = self.model(frame)
                labels = results.pandas().xyxy[0]['name'].tolist()  # Extract object names

                # Speak detected items every 8 seconds
                detected_items = labels
                if detected_items:
                    detected_str = ", ".join(detected_items)
                    print(f"Detected: {detected_str}")
                    self.speak(detected_str)  # Speak detected objects

                    # ✅ Update UI with detected objects (No distance info for now)
                    if self.update_ui_callback:
                        self.update_ui_callback(detected_str, None)

                cv2.imshow("Object Detection", frame)  # Show camera feed

                # ✅ Wait for 8 seconds before detecting again
                time.sleep(8)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            self.cap.release()
            cv2.destroyAllWindows()

        threading.Thread(target=run_detection, daemon=True).start()

    def stop(self):
        """Stop object detection."""
        self.running = False
