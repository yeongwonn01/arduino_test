import asyncio
from bleak import BleakClient

address = "48:27:E2:FC:9A:ED"
# 읽기/쓰기용 캐릭터리스틱 uuid
read_write_charcteristic_uuid = "12345678-1234-5678-1234-56789abcdef2"

async def run(address):
    async with BleakClient(address) as client:
        while True:
            # 데이터를 읽기
            read_data = await client.read_gatt_char(read_write_charcteristic_uuid)
            
            # 읽은 데이터는 바이트 배열이므로 디코딩하여 문자열로 변환
            decoded_data = read_data.decode("utf-8")
            print('read_data:', decoded_data)
            
            # 특정 단어 "STOP"이 들어오면 루프 종료
            if "STOP" in decoded_data:
                print('STOP signal received, stopping...')
                break

    
    print('disconnect')

loop = asyncio.get_event_loop()
loop.run_until_complete(run(address))
print('done')

