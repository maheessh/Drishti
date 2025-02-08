import asyncio
from bleak import BleakScanner, BleakClient

class BluetoothService:
    def __init__(self):
        self.devices = []

    async def discover_devices(self):
        self.devices = await BleakScanner.discover()
        return self.devices

    def scan_bluetooth(self):
        return asyncio.run(self.discover_devices())

    async def connect_device(self, address):
        client = BleakClient(address)
        await client.connect()

    def connect_device(self, address):
        asyncio.run(self.connect_device(address))
