import bluetooth
import threading

class BluetoothService:
    def __init__(self):
        self.devices = []  # Store device names
        self.device_map = {}  # Store name-address mapping

    def scan(self, update_ui_callback):
        """Scans for Bluetooth devices and updates UI."""
        def scan_thread():
            print("Scanning for Bluetooth devices...")
            self.devices.clear()
            self.device_map.clear()
            
            found_devices = bluetooth.discover_devices(duration=8, lookup_names=True)
            for addr, name in found_devices:
                self.devices.append(name)
                self.device_map[name.lower()] = addr  # Store lowercase for easy voice matching

            print("Scan complete. Devices found:", self.devices)

            # ✅ Update UI (Pass names to callback)
            update_ui_callback(self.devices)

        thread = threading.Thread(target=scan_thread, daemon=True)
        thread.start()

    def connect_to_device(self, device_name):
        """Connect to a device by its name."""
        device_name = device_name.lower()
        if device_name in self.device_map:
            device_address = self.device_map[device_name]
            print(f"Connecting to {device_name} at {device_address}...")
            # Add actual Bluetooth connection logic if needed
            return True
        else:
            print(f"Device {device_name} not found.")
            return False
