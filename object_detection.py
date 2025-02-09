import cv2
import pytesseract
import easyocr
import torch
import sqlite3
import pyttsx3
import threading
from datetime import datetime

class ObjectDetector:
    def __init__(self, update_ui_callback=None):
        """Initialize object detection, database, and text-to-speech."""
        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty('rate', 150)

        # ✅ Load YOLOv5 model properly
        self.model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)

        # ✅ OCR Reader for text recognition
        self.reader = easyocr.Reader(['en'])

        # ✅ SQLite Database Setup
        self.conn = sqlite3.connect("detections.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                detected_item TEXT,
                timestamp TEXT
            )
        """)
        self.conn.commit()

        self.update_ui_callback = update_ui_callback  # ✅ UI Callback Function

    def speak(self, text):
        """Convert text to speech asynchronously."""
        threading.Thread(target=lambda: self._speak(text), daemon=True).start()

    def _speak(self, text):
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()

    def save_detection(self, item):
        """Save detected object in the database."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute("INSERT INTO history (detected_item, timestamp) VALUES (?, ?)", (item, timestamp))
        self.conn.commit()

    def detect_objects(self):
        """Detect objects and read text using OCR continuously in a thread."""
        def run_detection():
            cap = cv2.VideoCapture(0)
            while True:
                ret, frame = cap.read()
                if not ret:
                    print("[ERROR] Couldn't read frame from webcam!")
                    break

                # ✅ Detect objects with YOLOv5
                results = self.model(frame)
                labels = results.pandas().xyxy[0]['name'].tolist()

                # ✅ Detect text with EasyOCR
                text_results = self.reader.readtext(frame, detail=0)

                # ✅ Draw bounding boxes for detected objects
                for index, row in results.pandas().xyxy[0].iterrows():
                    x1, y1, x2, y2 = int(row['xmin']), int(row['ymin']), int(row['xmax']), int(row['ymax'])
                    label = row['name']
                    confidence = row['confidence']

                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label} ({confidence:.2f})", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

                # ✅ Draw bounding boxes for detected text
                for result in text_results:
                    if len(result) == 2:  # Fix unpacking error
                        (bbox, text) = result
                    elif len(result) == 3:  # Some versions return confidence value
                        (bbox, text, prob) = result

                    (top_left, top_right, bottom_right, bottom_left) = bbox
                    top_left = tuple(map(int, top_left))
                    bottom_right = tuple(map(int, bottom_right))

                    cv2.rectangle(frame, top_left, bottom_right, (255, 0, 0), 2)
                    cv2.putText(frame, text, (top_left[0], top_left[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                detected_items = labels + [text for (_, text, *_) in text_results]

                # ✅ Speak detected items and save to history
                if detected_items:
                    detected_str = ", ".join(detected_items)
                    print(f"Detected: {detected_str}")
                    self.speak(detected_str)
                    self.save_detection(detected_str)

                    # ✅ Update UI if callback is set
                    if self.update_ui_callback:
                        self.update_ui_callback(detected_str)

                # ✅ Show webcam feed with detections
                cv2.imshow("Object Detection", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

        threading.Thread(target=run_detection, daemon=True).start()
