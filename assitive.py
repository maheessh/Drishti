import tkinter as tk
from tkinter import messagebox
import asyncio
from bleak import BleakScanner, BleakClient
import speech_recognition as sr
import pyttsx3
import threading

class BluetoothApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Assistive Wearable App")

        # Initialize Bluetooth & Speech Services
        self.speech_recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()

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

        self.start_speech_button = tk.Button(root, text="Start Listening", command=self.listen_for_wake_word)
        self.start_speech_button.pack(pady=5)

        self.devices = []  # Store discovered Bluetooth devices
        self.connected_device = None

    # ✅ Scan for Bluetooth Devices using `bleak`
    async def discover_devices(self):
        self.status_label.config(text="Scanning for Bluetooth devices...")
        self.device_listbox.delete(0, tk.END)
        self.devices = []

        devices = await BleakScanner.discover()
        if devices:
            for device in devices:
                self.devices.append(device)
                self.device_listbox.insert(tk.END, f"{device.name} ({device.address})")
            self.status_label.config(text="Scan complete. Select a device.")
        else:
            self.status_label.config(text="No devices found.")
            messagebox.showinfo("Bluetooth", "No devices found. Make sure Bluetooth is enabled.")

    def scan_bluetooth(self):
        asyncio.run(self.discover_devices())

    # ✅ Connect to Selected Bluetooth Device using `bleak`
    async def connect_device(self, address):
        try:
            self.connected_device = BleakClient(address)
            await self.connected_device.connect()
            self.status_label.config(text=f"Connected to {address}")
            messagebox.showinfo("Bluetooth", f"Connected to {address}")
        except Exception as e:
            self.status_label.config(text=f"Connection failed: {e}")
            messagebox.showerror("Bluetooth", f"Failed to connect: {e}")

    def connect_bluetooth(self):
        selected_index = self.device_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("Bluetooth", "Please select a device to connect.")
            return

        address = self.devices[selected_index[0]].address
        asyncio.run(self.connect_device(address))

    # ✅ Wake Word Detection ("Hello") to Activate Listening
    def listen_for_wake_word(self):
        self.speech_label.config(text="Listening for wake word...")

        def recognize():
            while True:
                try:
                    with sr.Microphone() as source:
                        audio = self.speech_recognizer.listen(source)
                        text = self.speech_recognizer.recognize_google(audio).lower()
                        print(f"Heard: {text}")

                        if "hello" in text:
                            self.speech_label.config(text="Wake word detected! Listening for command...")
                            self.speak("Wake word detected. Please say your command.")
                            self.listen_for_command()
                            break  # Stop wake-word loop after activation
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    self.speech_label.config(text="Speech recognition service error.")
                    break

        threading.Thread(target=recognize, daemon=True).start()

    # ✅ Listen for Commands After Wake Word
    def listen_for_command(self):
        def recognize():
            try:
                with sr.Microphone() as source:
                    self.speech_label.config(text="Listening for command...")
                    audio = self.speech_recognizer.listen(source)
                    command = self.speech_recognizer.recognize_google(audio)
                    self.speech_label.config(text=f"Command: {command}")
                    print(f"Command recognized: {command}")

                    self.speak(f"You said: {command}")

            except sr.UnknownValueError:
                self.speech_label.config(text="Could not understand. Try again.")
            except sr.RequestError:
                self.speech_label.config(text="Speech recognition service error.")

        threading.Thread(target=recognize, daemon=True).start()

    # ✅ Text-to-Speech Function
    def speak(self, text):
        self.speaker.say(text)
        self.speaker.runAndWait()

# Run the Tkinter Application
if __name__ == "__main__":
    root = tk.Tk()
    app = BluetoothApp(root)
    root.mainloop()
