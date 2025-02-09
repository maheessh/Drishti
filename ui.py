import tkinter as tk
from tkinter import ttk, messagebox
import threading
from bluetooth_service import BluetoothService
from speech_service import SpeechService
from tts_service import TextToSpeechService

class BluetoothApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dristhi - Assistive Wearable App")
        self.root.geometry("800x700")  
        self.root.configure(bg="#1E1E1E")  

        # ✅ Initialize Services
        self.bluetooth_service = BluetoothService()
        self.tts_service = TextToSpeechService()
        self.speech_service = SpeechService(self.on_wake_word_detected, self.bluetooth_service)

        # ✅ Custom Styling
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12, "bold"), padding=10, background="#007BFF", foreground="white")
        self.style.map("TButton", background=[("active", "#0056b3")])  

        # ✅ Title Label
        self.label = tk.Label(
            root,
            text="Dristhi - Assistive Wearable",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1E1E1E"
        )
        self.label.pack(pady=15)

        # ✅ Bluetooth Control Frame
        self.control_frame = tk.Frame(root, bg="#1E1E1E")
        self.control_frame.pack(pady=10, padx=20, fill=tk.X)

        # ✅ Scan Bluetooth Button
        self.scan_button = tk.Button(
            self.control_frame,
            text="Scan Bluetooth Devices",
            command=self.scan_bluetooth,
            font=("Arial", 12, "bold"),
            bg="#007BFF",
            fg="white",
            relief="raised",
            bd=3
        )
        self.scan_button.pack(pady=10, fill=tk.X)

        # ✅ Device List with Scrollbar
        self.list_frame = tk.Frame(root, bg="#1E1E1E")
        self.list_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

        self.device_listbox = tk.Listbox(
            self.list_frame,
            width=50,
            height=10,
            font=("Arial", 12),
            bg="#2C2C2C",
            fg="white",
            selectbackground="#007BFF",
            selectforeground="white",
            relief="flat",
            highlightthickness=2,
            highlightbackground="#007BFF"
        )
        self.device_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.list_frame, orient=tk.VERTICAL, command=self.device_listbox.yview)
        self.device_listbox.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # ✅ Connect Button
        self.connect_button = tk.Button(
            self.control_frame,
            text="Connect to Device",
            command=self.connect_bluetooth,
            font=("Arial", 12, "bold"),
            bg="#007BFF",
            fg="white",
            relief="raised",
            bd=3
        )
        self.connect_button.pack(pady=10, fill=tk.X)

        # ✅ Object Detection Button
        self.camera_button = tk.Button(
            self.control_frame,
            text="Start Object Detection",
            command=self.start_object_detection,
            font=("Arial", 12, "bold"),
            bg="#28A745",
            fg="white",
            relief="raised",
            bd=3
        )
        self.camera_button.pack(pady=10, fill=tk.X)

        # ✅ Status Label
        self.status_label = tk.Label(
            root,
            text="Status: Waiting for connection...",
            font=("Arial", 12, "italic"),
            fg="#BDC3C7",
            bg="#1E1E1E"
        )
        self.status_label.pack(pady=10)

        # ✅ Person Distance Label
        self.face_label = tk.Label(
            root,
            text="Person Distance: Not detected",
            font=("Arial", 14),
            fg="#FFC107",
            bg="#1E1E1E"
        )
        self.face_label.pack(pady=10)

        # ✅ Listening Label
        self.speech_label = tk.Label(
            root,
            text="Listening for wake word...",
            font=("Arial", 12, "italic"),
            fg="#00A8E8",
            bg="#1E1E1E"
        )
        self.speech_label.pack(pady=10)

        # ✅ Devices & Connection Storage
        self.devices = []
        self.connected_device = None
        self.object_detection_callback = None  

    def scan_bluetooth(self):
        """Scans for Bluetooth devices and updates the listbox in the UI."""
        def update_ui(device_names):
            """Callback function to update the UI listbox with scanned device names."""
            self.device_listbox.delete(0, tk.END)
            for name in device_names: 
                self.device_listbox.insert(tk.END, name)
        self.bluetooth_service.scan(update_ui)

    def connect_bluetooth(self):
        """Connect to a selected Bluetooth device."""
        selected_index = self.device_listbox.curselection()
        if selected_index:
            device_name = self.devices[selected_index[0]].name
            success = self.bluetooth_service.connect_to_device(device_name)
            if success: 
                self.status_label.config(text=f"Connected to {device_name}")
            else: 
                self.status_label.config(text=f"Failed to connect to {device_name}")
        else: 
            messagebox.showwarning("Connection Error", "Please select a device first!")        

    def on_wake_word_detected(self):
        """Trigger voice response and restart wake word detection."""
        self.speech_label.config(text="Wake word detected! Responding...")
        self.tts_service.speak("Hi, how can I help you?")

        threading.Thread(target=self.speech_service.listen_for_wake_word, daemon=True).start()

    def update_distance_display(self, distance):
        """Update UI with detected person's distance."""
        self.face_label.config(text=f"Person Distance: {distance:.2f} cm")

    def set_object_detection_callback(self, callback):
        """Allow main.py to trigger object detection"""
        self.object_detection_callback = callback

    def start_object_detection(self):
        """Call object detection function from main"""
        if self.object_detection_callback:
            self.object_detection_callback()

    def update_detection_results(self, detected_text):
        """Update the UI with detected objects/text"""
        self.detection_label.config(text=f"Detected: {detected_text}")

if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)
    root.mainloop()
