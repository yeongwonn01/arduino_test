import asyncio
from bleak import BleakClient

address = "48:27:E2:FC:9A:ED"
# 읽기/쓰기용 캐릭터리스틱 uuid
read_write_charcteristic_uuid = "12345678-1234-5678-1234-56789abcdef2"

async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        # 서비스내에 있는 캐릭터리스틱 정보 보기
        for service in services:
            print(service)                
            print('\tuuid:', service.uuid)
            print('\tcharacteristic list:')
            for characteristic in service.characteristics:
                print('\t\t', characteristic)
                print('\t\tuuid:', characteristic.uuid)
                print('\t\tdescription :', characteristic.description)
                # ['write-without-response', 'write', 'read', 'notify']
                print('\t\tproperties :', characteristic.properties)
        
        # 읽기/쓰기 캐릭터리스틱 uuid를 이용해 데이터 읽기
        # 해당 캐릭터리스틱의 속성에는 read가 존재해야만 읽기가 가능하다.
        read_data = await client.read_gatt_char(read_write_charcteristic_uuid)
        # 읽근 데이터 출력
        print('read_data: ',read_data)
    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')

