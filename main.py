import tkinter as tk
import threading
from ui import DristhiApp
from object_detection import ObjectDetector

def run_detection(app):
    """Start object detection using shared camera feed."""
    detector = ObjectDetector(update_ui_callback=app.update_camera_display, shared_cap=app.cap)
    detector.detect_objects()

if __name__ == "__main__":
    root = tk.Tk()
    app = DristhiApp(root)

    # Start detection thread
    detection_thread = threading.Thread(target=run_detection, args=(app,), daemon=True)
    detection_thread.start()

    root.mainloop()
