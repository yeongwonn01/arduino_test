import asyncio
from bleak import BleakClient

address = "48:27:e2:fc:9a:ed"
write_charcteristic_uuid = "12345678-1234-5678-1234-56789abcdef1"
read_charcteristic_uuid = "12345678-1234-5678-1234-56789abcdef2"


async def read_data_task(client):
    last = ""
    while True:
        try:
            read_data = await client.read_gatt_char(read_charcteristic_uuid)
            if last != read_data:
                print('Read data:', str(read_data.decode()))
                last = read_data
        except Exception as e:
            print(f"Read error: {e}")
        await asyncio.sleep(1) 


async def write_data_task(client):
    while True:
        try:
            user_input = await asyncio.get_event_loop().run_in_executor(None, input, "Enter data to write: ")
            await client.write_gatt_char(write_charcteristic_uuid, bytes(user_input.encode()))
            print("Data written successfully")
        except Exception as e:
            print(f"Write error: {e}")


async def run(address):
    async with BleakClient(address) as client:
        print('Connected')
        services = await client.get_services()
        for service in services:
            for characteristic in service.characteristics:
                if characteristic.uuid == write_charcteristic_uuid:
                    if 'write' in characteristic.properties:
                        print(f"Found writable characteristic: {write_charcteristic_uuid}")
                if characteristic.uuid == read_charcteristic_uuid:
                    if 'read' in characteristic.properties:
                        print(f"Found readable characteristic: {read_charcteristic_uuid}")

        await asyncio.gather(
            read_data_task(client),
            write_data_task(client)
        )

    print('Disconnected')


loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('Done')