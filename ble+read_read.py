import asyncio
from bleak import BleakClient

address = "48:27:E2:FC:9A:ED"
# 읽기/쓰기용 캐릭터리스틱 uuid
read_write_charcteristic_uuid = "12345678-1234-5678-1234-56789abcdef2"

async def run(address):    
    async with BleakClient(address) as client:
        print('connected')

        
        services = await client.get_services()        
        for service in services:
            for characteristic in service.characteristics:
                # 각 캐릭터리스틱의 uuid를 읽기용 캐릭터리스틱 uuid와 비교
                if characteristic.uuid == read_write_charcteristic_uuid:
                    # 해당 캐릭터리스틱에 읽기 속성이 있는지 확인
                    if 'read' in characteristic.properties:
                        # 데이터 읽기
                        read_data = await client.read_gatt_char(characteristic)
                        print('read_data: ',read_data)



    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')

