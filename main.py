import tkinter as tk
import threading
from ui import BluetoothApp
from face_detection import FaceDetector
from object_detection import ObjectDetector

stop_face_detection = threading.Event()

def run_face_detection(app):
    """Continuously detect faces and update UI while allowed."""
    face_detector = FaceDetector(update_ui_callback=app.update_distance_display)

    while True:
        if not stop_face_detection.is_set():  
            distance = face_detector.get_smoothed_distance(0)  # Ensure UI gets a value
            if distance is not None:
                app.update_distance_display(distance)
        else:
            print("[INFO] Face detection paused...")
        threading.Event().wait(0.1)

def run_object_detection():
    """Pauses face detection, runs object detection, then resumes face detection."""
    global stop_face_detection
    stop_face_detection.set()  # Pause face detection

    object_detector = ObjectDetector()
    object_detector.detect_objects()

    stop_face_detection.clear()  # Resume face detection

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)

    # ✅ Start face detection in a separate thread
    face_thread = threading.Thread(target=run_face_detection, args=(app,), daemon=True)
    face_thread.start()

    # ✅ Connect object detection button to function
    app.set_object_detection_callback(run_object_detection)

    root.mainloop()
