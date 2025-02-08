import tkinter as tk
from tkinter import messagebox
import asyncio
from bluetooth_service import BluetoothService
from speech_service import SpeechService
from tts_service import TextToSpeechService

class BluetoothApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistive Wearable App")

        # Initialize services
        self.bluetooth_service = BluetoothService()
        self.speech_service = SpeechService()
        self.tts_service = TextToSpeechService()

        # UI Components
        self.label = tk.Label(root, text="Assistive Wearable App", font=("Arial", 14, "bold"))
        self.label.pack(pady=10)

        self.scan_button = tk.Button(root, text="Scan Bluetooth Devices", command=self.scan_bluetooth)
        self.scan_button.pack(pady=5)

        self.device_listbox = tk.Listbox(root, width=50, height=10)
        self.device_listbox.pack(pady=5)

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_bluetooth)
        self.connect_button.pack(pady=5)

        self.status_label = tk.Label(root, text="Status: Waiting...", font=("Arial", 12))
        self.status_label.pack(pady=5)

        self.speech_label = tk.Label(root, text="Listening for wake word...", font=("Arial", 12, "italic"))
        self.speech_label.pack(pady=5)

        self.start_speech_button = tk.Button(root, text="Start Listening", command=self.start_listening)
        self.start_speech_button.pack(pady=5)

        self.devices = []  # Store discovered Bluetooth devices
        self.connected_device = None

    def scan_bluetooth(self):
        """Scans for Bluetooth devices asynchronously."""
        async def run_scan():
            devices = await self.bluetooth_service.discover_devices()
            self.device_listbox.delete(0, tk.END)
            self.devices = devices
            if devices:
                for name, address in devices:
                    self.device_listbox.insert(tk.END, f"{name} ({address})")
                self.status_label.config(text="Scan complete. Select a device.")
            else:
                self.status_label.config(text="No devices found.")
                messagebox.showinfo("Bluetooth", "No devices found. Make sure Bluetooth is enabled.")

        asyncio.run(run_scan())

    def connect_bluetooth(self):
        """Connects to a selected Bluetooth device."""
        selected_index = self.device_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Bluetooth", "Please select a device to connect.")
            return

        address = self.devices[selected_index[0]][1]

        async def run_connect():
            success = await self.bluetooth_service.connect_device(address)
            if success:
                self.status_label.config(text=f"Connected to {address}")
                messagebox.showinfo("Bluetooth", f"Connected to {address}")
            else:
                messagebox.showerror("Bluetooth", "Failed to connect.")

        asyncio.run(run_connect())

    def start_listening(self):
        """Starts wake-word detection and speech recognition."""
        self.speech_service.listen_for_wake_word(self.process_speech_command)

    def process_speech_command(self):
        """Processes speech commands after wake-word is detected."""
        def handle_command(command):
            self.speech_label.config(text=f"Command: {command}")
            self.tts_service.speak(f"You said: {command}")

        self.speech_service.listen_for_command(handle_command)

# Run the Tkinter Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)
    root.mainloop()
