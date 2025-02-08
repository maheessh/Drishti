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
        self.root.geometry("600x700")  # Improved Window Size
        self.root.configure(bg="#1E1E1E")  # Dark Background for Modern UI

        # Initialize Services
        self.bluetooth_service = BluetoothService()
        self.tts_service = TextToSpeechService()
        self.speech_service = SpeechService(self.on_wake_word_detected, self.bluetooth_service)

        # Title Label
        self.label = tk.Label(
            root,
            text="Dristhi - Assistive Wearable",
            font=("Arial", 20, "bold"),
            fg="white",
            bg="#1E1E1E"
        )
        self.label.pack(pady=15)

        # Bluetooth Control Frame
        self.control_frame = tk.Frame(root, bg="#1E1E1E")
        self.control_frame.pack(pady=10, padx=20, fill=tk.X)

        # Bluetooth Scan Button
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

        # Device List with Scrollbar
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

        # Connect Button
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

        # Status Label
        self.status_label = tk.Label(
            root,
            text="Status: Waiting for connection...",
            font=("Arial", 12, "italic"),
            fg="#BDC3C7",
            bg="#1E1E1E"
        )
        self.status_label.pack(pady=10)

        # Listening Label
        self.speech_label = tk.Label(
            root,
            text="Listening for wake word...",
            font=("Arial", 12, "italic"),
            fg="#00A8E8",
            bg="#1E1E1E"
        )
        self.speech_label.pack(pady=10)

        # Devices & Connection Storage
        self.devices = []
        self.connected_device = None

    def scan_bluetooth(self):
        """Scan for Bluetooth devices and update the UI."""
        self.device_listbox.delete(0, tk.END)
        self.bluetooth_service.scan(self.update_device_list)

    def update_device_list(self, devices):
        """Update the list box with scanned Bluetooth device names."""
        self.device_listbox.delete(0, tk.END)
        self.devices = devices  # Store for later reference
        for name in devices:
            self.device_listbox.insert(tk.END, name)

    def connect_bluetooth(self):
        """Connect to a selected Bluetooth device."""
        selected_index = self.device_listbox.curselection()
        if selected_index:
            device_name = self.devices[selected_index[0]]
            if self.bluetooth_service.connect_to_device(device_name):
                self.status_label.config(text=f"Connected to {device_name}")
                messagebox.showinfo("Bluetooth", f"Connected to {device_name}")
            else:
                messagebox.showerror("Bluetooth", f"Could not connect to {device_name}")

    def on_wake_word_detected(self):
        """Trigger voice response and restart wake word detection."""
        self.speech_label.config(text="Wake word detected! Responding...")
        self.tts_service.speak("Hi, how can I help you?")

        # Restart wake word detection
        threading.Thread(target=self.speech_service.listen_for_wake_word, daemon=True).start()

# Launch Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)
    root.mainloop()
