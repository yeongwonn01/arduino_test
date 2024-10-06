import asyncio
from bleak import BleakClient

address = "48:27:E2:FC:9A:ED"
async def run(address):    
    async with BleakClient(address) as client:
        print('connected')
        services = await client.get_services()        
        for service in services:
            print(service)             
            # 서비스의 UUID 출력   
            print('\tuuid:', service.uuid)
            print('\tcharacteristic list:')
            # 서비스의 모든 캐릭터리스틱 출력용
            for characteristic in service.characteristics:
                # 캐릭터리스틱 클래스 변수 전체 출력
                print('\t\t', characteristic)
                # UUID 
                print('\t\tuuid:', characteristic.uuid)
                # decription(캐릭터리스틱 설명)
                print('\t\tdescription :', characteristic.description)
                # 캐릭터리스틱의 속성 출력
                # 속성 값 : ['write-without-response', 'write', 'read', 'notify']
                print('\t\tproperties :', characteristic.properties)

    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')
