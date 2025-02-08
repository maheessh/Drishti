import asyncio
from bleak import BleakScanner, BleakClient

class BluetoothService:
    def __init__(self):
        self.devices = []
        self.connected_device = None

    async def discover_devices(self):
        """Scans for Bluetooth devices asynchronously."""
        print("Scanning for Bluetooth devices...")
        self.devices = await BleakScanner.discover()
        return [(device.name or "Unknown", device.address) for device in self.devices]

    async def connect_device(self, address):
        """Connects to a selected Bluetooth device."""
        try:
            self.connected_device = BleakClient(address)
            await self.connected_device.connect()
            print(f"Connected to {address}")
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
