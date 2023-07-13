import httpx
import asyncio
from nats.aio.client import Client as NATS
import json

# 網路上的pypl名稱是舊的
# pip install nats-py

async def run():
    # 連線到Nats
    nc = NATS()
    await nc.connect("localhost:4222",name="python-connection")
    print('connect down, waiting for message')

    #接收到資料之後要做什麼
    async def message_handler(msg):
        #把資料取出來
        subject = msg.subject
        data = msg.data.decode()
        print(f"Received a message on '{subject}': {data}")
        # 取出filename
        # TODO: Extract filename from data
        print(type(data))
        data_dict = json.loads(data)
        #print(data_dict['Key'][6:])
        filename = data_dict['Key'][6:]

        # Send POST request to FastAPI service
        response = httpx.post('http://localhost:8121/scan', json={'filename': filename})

        print(f"Response from FastAPI service: {response.json()}")

    # Subscribe to subject
    await nc.subscribe("bucketevents", cb=message_handler)
    print('subscribe')

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.run_forever()
    loop.close()