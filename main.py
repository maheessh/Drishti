import tkinter as tk
import threading
from ui import BluetoothApp
from face_detection import FaceDetector
from hardware_data import HardwareMonitor

stop_face_detection = threading.Event()

def run_face_detection(app):
    face_detector = FaceDetector(update_ui_callback=app.update_distance_display)

    while True:
        if not stop_face_detection.is_set():
            distance = face_detector.get_smoothed_distance(0)
            if distance is not None:
                app.update_distance_display(distance)
        else:
            print("[INFO] Face detection paused...")
        threading.Event().wait(0.1)

def run_object_detection():
    global stop_face_detection
    stop_face_detection.set()

    object_detector = ObjectDetector()
    object_detector.detect_objects()

    stop_face_detection.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)

    face_thread = threading.Thread(target=run_face_detection, args=(app,), daemon=True)
    face_thread.start()

    try:
        app.hardware_monitor = HardwareMonitor(app.health_tab)
    except Exception as e:
        print(f"Error initializing hardware monitor: {e}")

    root.mainloop()
